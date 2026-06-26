---
name: query-health
description: Query personal medical records including biochemical tests and imaging studies with filtering and formatting options.
argument-hint: <query_type(all/biochemical/imaging/recent/date/abnormal) [query_parameters]>
allowed-tools: Read, Write
schema: query-health/schema.json
---

# Medical Records Query Skill

Query records from the personal medical data center.

## Core Flow

```
User Input -> Parse Query Type -> Read Index File -> Filter Records -> Format Output -> Summary Statistics
```

## Step 1: Parse Query Type

| Input Keywords | Query Type | Description |
|----------------|------------|-------------|
| all | all | All records |
| biochemical | biochemical | Biochemical tests |
| imaging | imaging | Imaging studies |
| recent | recent | Recent N records |
| date | date | Specific date |
| abnormal | abnormal | Abnormal indicators |

## Step 2: Read Index File

Read all record index information from `data/index.json`.

If the file does not exist, return "No medical records available".

## Step 3: Filter Records

Filter records based on query type and read corresponding JSON files.

### Biochemical Test Output Format

```
Date: YYYY-MM-DD
Test Type: Complete Blood Count
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Item          | Value | Unit    | Reference Range | Status
────────────────────────────────────────
White Blood Cell   | 6.5   | ×10^9/L | 3.5-9.5         | ✅ Normal
Hemoglobin         | 145   | g/L     | 130-175         | ✅ Normal
Platelet Count     | 189   | ×10^9/L | 125-350         | ✅ Normal
```

### Imaging Study Output Format

```
Date: YYYY-MM-DD
Test Type: Ultrasound
Examined Area: Abdomen
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Findings:
[Description content]

Measurements:
- Size: XXX

Conclusion:
[Conclusion content]
```

## Step 4: Summary Statistics

Add statistical information after query results:
- Total record count
- Biochemical test count
- Imaging study count
- Time span

## Execution Instructions

```
1. Read data/index.json
2. Filter records based on query type
3. Read corresponding JSON files
4. Format output
5. Add summary statistics
```

## Example Interactions

### Query All Records
```
User: Query all records

Output:
📋 Medical Records Query Results
Total: 17 records
Biochemical tests: 12 records
Imaging studies: 5 records
```

### Query Abnormal Indicators
```
User: Query abnormal indicators

Output:
📋 Abnormal Indicators Summary
Found 5 abnormal indicators
- Elevated uric acid (486 μmol/L)
- Elevated total cholesterol (6.2 mmol/L)
...
```

### Query by Date
```
User: Query records for 2025-12

Output:
📋 December 2025 Records
Total: 3 test records
...
```
