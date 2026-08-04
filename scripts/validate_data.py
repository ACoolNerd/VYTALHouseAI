from pathlib import Path
import csv
import sys

REQUIRED = {
    "accounts.csv": {"account_id", "organization_name", "segment", "status"},
    "contacts.csv": {"contact_id", "account_id", "full_name", "title"},
    "pipeline.csv": {"opportunity_id", "account_id", "stage", "estimated_contract_value"},
}

base = Path(__file__).resolve().parents[1] / "data" / "templates"
errors = []

for filename, required in REQUIRED.items():
    path = base / filename
    if not path.exists():
        errors.append(f"Missing file: {path}")
        continue
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        try:
            headers = set(next(reader))
        except StopIteration:
            errors.append(f"Empty file: {path}")
            continue
    missing = required - headers
    if missing:
        errors.append(f"{filename} missing columns: {sorted(missing)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("VYTAL House data templates validated.")
