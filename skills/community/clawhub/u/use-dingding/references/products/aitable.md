# AITable Reference

## Base Operations

### List Bases

```bash
dws aitable base list [--limit <N>]
```

**Example:**
```bash
dws aitable base list --jq '.result[] | {name: .name, baseId: .baseId}'
```

### Get Base Detail

```bash
dws aitable base get --base-id <baseId>
```

## Table Operations

### List Tables in Base

```bash
dws aitable table list --base-id <baseId>
```

**Example:**
```bash
dws aitable table list --base-id "base123" --jq '.result[] | {name: .name, tableId: .tableId}'
```

### Get Table Detail

```bash
dws aitable table get --base-id <baseId> --table-id <tableId>
```

### Create Table

```bash
dws aitable table create --base-id <baseId> --name "<table-name>" --fields '<field-definitions>'
```

## Record Operations

### Query Records

```bash
dws aitable record query --base-id <baseId> --table-id <tableId> [--limit <N>] [--filter '<filter-json>'}
```

**Parameters:**
- `--base-id`: Base ID (required)
- `--table-id`: Table ID (required)
- `--limit`: Max records (default: 100)
- `--filter`: Filter expression (optional)

**Example:**
```bash
# Get all records
dws aitable record query --base-id "base123" --table-id "table456" --limit 50

# With filter
dws aitable record query --base-id "base123" --table-id "table456" --filter '{"status": "open"}'

# Extract specific fields
dws aitable record query --base-id "base123" --table-id "table456" --jq '.result.records[] | {name: .fields.name, status: .fields.status}'
```

### Create Record

```bash
dws aitable record create --base-id <baseId> --table-id <tableId> --fields '<json-fields>'
```

**Example:**
```bash
dws aitable record create \
  --base-id "base123" \
  --table-id "table456" \
  --fields '{"name": "Task 1", "status": "open", "priority": "high"}'
```

### Update Record

```bash
dws aitable record update --base-id <baseId> --table-id <tableId> --record-id <recordId> --fields '<json-fields>'
```

**Example:**
```bash
dws aitable record update \
  --base-id "base123" \
  --table-id "table456" \
  --record-id "rec789" \
  --fields '{"status": "done"}'
```

### Delete Record

```bash
dws aitable record delete --base-id <baseId> --table-id <tableId> --record-ids <rec1,rec2,rec3>
```

### Batch Create Records

```bash
dws aitable record batch-create --base-id <baseId> --table-id <tableId> --records '<json-array>'
```

**Example:**
```bash
dws aitable record batch-create \
  --base-id "base123" \
  --table-id "table456" \
  --records '[{"name": "Task 1"}, {"name": "Task 2"}, {"name": "Task 3"}]'
```

## Field Operations

### List Fields

```bash
dws aitable field list --base-id <baseId> --table-id <tableId>
```

**Example:**
```bash
dws aitable field list --base-id "base123" --table-id "table456" --jq '.result[] | {name: .name, type: .type, fieldId: .fieldId}'
```

### Create Field

```bash
dws aitable field create --base-id <baseId> --table-id <tableId> --name "<field-name>" --type "<field-type>"
```

**Field Types:** `text`, `number`, `singleSelect`, `multiSelect`, `date`, `checkbox`, `attachment`, `member`, `link`

### Update Field

```bash
dws aitable field update --base-id <baseId> --table-id <tableId> --field-id <fieldId> --name "<new-name>"
```

### Delete Field

```bash
dws aitable field delete --base-id <baseId> --table-id <tableId> --field-id <fieldId>
```

## Attachment Operations

### Upload Attachment

```bash
dws aitable attachment upload --base-id <baseId> --table-id <tableId> --record-id <recordId> --field-id <fieldId> --file <path>
```

See bundled script: `scripts/upload_attachment.py`

## Common Patterns

### Import Records from CSV

See bundled script: `scripts/import_records.py`

```bash
python scripts/import_records.py --base-id <baseId> --table-id <tableId> data.csv
```

### Batch Add Fields

See bundled script: `scripts/bulk_add_fields.py`

```bash
python scripts/bulk_add_fields.py --base-id <baseId> --table-id <tableId> fields.json
```

### Query with Complex Filter

```bash
# Filter by multiple conditions
dws aitable record query \
  --base-id "base123" \
  --table-id "table456" \
  --filter '{"and": [{"status": "open"}, {"priority": "high"}]}'
```

### Get Record Count

```bash
dws aitable record query --base-id "base123" --table-id "table456" --limit 1 --jq '.result.total'
```
