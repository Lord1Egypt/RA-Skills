# Courses Command Reference

```bash
tronclass courses list [--all] [--raw] [--fields f1,f2,...]
tronclass c list ...
```

## Options

| Option | Description |
|---|---|
| *(none)* | Show only **ongoing** courses (default) |
| `--all` | Show all courses including past and future |
| `--raw` | Print raw JSON response — useful for inspecting all available fields |
| `--fields f1,f2,...` | Customize displayed columns |

## Default Fields

`id, name, instructors.name`

The `id` column is the **course ID** needed for `activities list` and `homework list`.

## Available Fields (common)

| Field | Description |
|---|---|
| `id` | Course ID |
| `name` | Course name |
| `course_code` | Course code |
| `department` | Department |
| `semester` | Semester label |
| `instructors.name` | Instructor name (nested field) |
| `start_date` / `end_date` | Course date range |

Use `--raw` to see the full JSON and discover additional fields.

## Examples

```bash
# List ongoing courses (default)
tronclass courses list

# All courses including old ones
tronclass courses list --all

# Raw JSON for full field inspection
tronclass courses list --raw

# Custom columns
tronclass courses list --fields id,name,semester
```
