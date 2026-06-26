# Homework Command Reference

```bash
tronclass homework <subcommand> [options]
tronclass hw <subcommand>
tronclass h  <subcommand>
```

---

## `list <course_id>`

```bash
tronclass homework list <course_id> [--fields f1,f2,...]
tronclass hw l <course_id>
```

Lists all homework activities for a course.

**Default fields:** `id, title, deadline, status, score`

| Field | Description |
|---|---|
| `id` | Activity ID |
| `title` | Homework title |
| `deadline` / `due_at` | Submission deadline |
| `status` | Computed: 已繳交 / 草稿 / 待繳交 / 未繳 |
| `score` | Score received (if graded) |
| `max_score` | Maximum possible score |

---

## `view <activity_id>`

```bash
tronclass homework view <activity_id> [--raw]
tronclass hw v <activity_id>
```

Rich layout for a single homework. Sections:

1. **Metadata table** — id, title, type, status (`已繳交` / `草稿` / `未繳` / `待繳交`, color-coded), deadline (red if overdue, yellow if within 7 days), score if graded.
2. **Description** — assignment prompt with HTML rendered inline (bold, lists, hyperlinks).
3. **Attachments** — teacher-provided files. Each row shows `ref_id` and a clickable OSC 8 hyperlink. Pass the `ref_id` to `tronclass activities download` to save locally.
4. **My Submission** — your own state:
   - `已繳交` (submitted) → submission time, score and instructor feedback if graded, your comment, and `Submitted Files` with download URLs.
   - `草稿` (draft saved) → `Draft Files` with download URLs so you can verify what's queued before finalizing.
   - `(尚未繳交也未儲存草稿)` → nothing submitted yet.

| Option | Description |
|---|---|
| `--raw` | Print the raw JSON from each underlying endpoint (activity body, homework list match, submission list, resolved `user_id`). Useful for debugging tenants where the rendered output looks wrong. |

### Typical use

```bash
# Read the prompt and grab teacher attachments before starting
tronclass homework view 987654

# Save a draft, then view to confirm what's queued
tronclass homework submit 987654 ./essay.pdf --draft
tronclass homework view 987654
```

---

## `submit <activity_id> <file...>`

```bash
tronclass homework submit <activity_id> <file1> [file2 ...] [--draft]
tronclass hw s <activity_id> ./essay.pdf ./appendix.pdf
```

Uploads one or more files and submits them for the specified homework activity.

A confirmation prompt is shown before submitting, displaying the homework title and the file(s) to be submitted.

| Option | Description |
|---|---|
| `--draft` | Save as draft instead of final submission. Inspect with `homework view`. |

### Notes

- Multiple files can be submitted in one command.
- Folders are not supported — only individual files.
- Supported file types: any (MIME type detected automatically).
- The activity ID is the `id` from `homework list`.

### Example

```bash
# Find the homework ID
tronclass homework list <course_id>

# Read the prompt
tronclass homework view 2901222

# Submit a single file
tronclass homework submit 2901222 ./report.pdf

# Submit multiple files
tronclass homework submit 2901222 ./report.pdf ./data.xlsx

# Save as draft, then verify
tronclass homework submit 2901222 ./draft_report.pdf --draft
tronclass homework view 2901222
```
