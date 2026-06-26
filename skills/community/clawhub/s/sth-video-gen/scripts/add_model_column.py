#!/usr/bin/env python3
import csv

# Read the templates over 12s (these use keling3)
over_12s_ids = set()
with open('templates_over_12s.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        template_id = row.get('Template ID', '').strip()
        if template_id:
            over_12s_ids.add(template_id)

print(f"Found {len(over_12s_ids)} templates over 12s (will use keling3)")

# Read the full status report and add model column
rows = []
with open('FULL_TEMPLATE_STATUS_REPORT.csv', 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames + ['Model']
    for row in reader:
        template_id = row.get('Template ID', '').strip()
        if template_id in over_12s_ids:
            row['Model'] = 'keling3'
        else:
            row['Model'] = 'seedance1.5pro'
        rows.append(row)

# Write the updated CSV
with open('FULL_TEMPLATE_STATUS_REPORT.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} records with model information")

# Count models
keling3_count = sum(1 for r in rows if r['Model'] == 'keling3')
seedance_count = sum(1 for r in rows if r['Model'] == 'seedance1.5pro')
print(f"  - keling3: {keling3_count}")
print(f"  - seedance1.5pro: {seedance_count}")
