# Activities Command Reference

```bash
tronclass activities <subcommand> [options]
tronclass a <subcommand> [options]
```

---

## `list <course_id>`

```bash
tronclass activities list <course_id> [--fields f1,f2,...]
tronclass a l <course_id>
```

Lists all activities in a course as a table.

**Default fields:** `id, title, type, status, end_time`

| Field | Description |
|---|---|
| `id` | Activity ID |
| `title` | Activity title |
| `type` | Type (homework, material, quiz, …) |
| `status` | Computed: 進行中 / 已結束 / 未開放 |
| `end_time` | End datetime |
| `start_time` | Start datetime |
| `deadline` | Deadline |

---

## `view <activity_id>`

```bash
tronclass activities view <activity_id> [--fields f1,f2,...]
tronclass a v <activity_id>
```

Displays a rich formatted layout:
1. **Metadata table** — id, title (bold), type, status (color-coded), deadline (red if overdue, yellow if within 7 days)
2. **Description** — HTML stripped, word-wrapped to terminal width
3. **Attachments table** — each file shows: `#`, filename (cyan, clickable OSC 8 hyperlink in supported terminals), `ref_id`, size

The Attachments section prints the exact `tronclass a download <ref_id> [output_file]` command for each file — copy-paste ready.

**Default fields:** `id, title, type, data, deadline, uploads`

When `--fields` is specified, shows a plain key-value table instead of the rich layout.

### Finding a ref_id

The `ref_id` shown in the Attachments table is what you pass to `activities download`. Example output:

```
Attachments (2 files)
┌───┬──────────────────────────┬──────────┬─────────┐
│ # │ name                     │ ref_id   │ size    │
├───┼──────────────────────────┼──────────┼─────────┤
│ 0 │ lecture_w3.pdf           │ 28409265 │ 1.4 MB  │
│ 1 │ exercises.pdf            │ 34147059 │ 338 KB  │
└───┴──────────────────────────┴──────────┴─────────┘
```

---

## `download <ref_id> [output_file]`

```bash
tronclass activities download <ref_id> [output_file] [--preview]
tronclass a d <ref_id>
tronclass a dl <ref_id> ./my_file.pdf
```

Downloads a file by its reference ID.

**`output_file` is optional.** When omitted, the filename is taken from the server's `Content-Disposition` header and saved to `~/Downloads/<filename>`.

| Option | Description |
|---|---|
| `output_file` | Local save path (optional; defaults to `~/Downloads/<filename>`) |
| `--preview` | Download preview/compressed version instead of the original |

### Full download workflow

```bash
# 1. Find course ID
tronclass courses list

# 2. Find activity ID
tronclass activities list <course_id>

# 3. View activity — note the ref_id in Attachments
tronclass activities view <activity_id>

# 4. Download (output defaults to ~/Downloads/)
tronclass activities download <ref_id>

# 4b. Or specify a path
tronclass activities download <ref_id> ./downloads/file.pdf
```
