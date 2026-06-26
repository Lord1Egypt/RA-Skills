# Todo Command Reference

```bash
tronclass todo [--fields f1,f2,...]
tronclass td   [--fields f1,f2,...]
tronclass t    [--fields f1,f2,...]
```

Displays the user's current to-do list as a table.

## Default Fields

`id, course_name, title, end_time`

The `id` column is the **activity ID** — use it directly with `tronclass activities view <id>` or `tronclass activities download`.

## Available Fields

| Field | Description |
|---|---|
| `id` | Activity ID (use with `activities view`) |
| `title` | Task title |
| `course_name` | Name of the course |
| `course_id` | Course ID |
| `type` | Activity type (homework, quiz, etc.) |
| `end_time` / `due_at` | Deadline |
| `status` | Completion status |

## Examples

```bash
# Default view (id + course + title + deadline)
tronclass todo

# Show only title and deadline
tronclass todo --fields title,end_time

# Show course ID too
tronclass todo --fields id,course_id,course_name,title,end_time
```
