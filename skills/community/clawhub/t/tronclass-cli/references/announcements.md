# Announcements Command Reference

```bash
tronclass ann <subcommand> [options]
```

The `ann` command reads TronClass announcements — both the school-wide feed and per-course announcements. It was added in CLI v0.3.0.

---

## `list [course_id]`

```bash
tronclass ann list [course_id]
tronclass ann l
tronclass ann ls <course_id>
```

Lists announcements as a table with columns: `id`, `title`, `author`, `date`.

| Form | What it shows |
|---|---|
| `tronclass ann list` | School-wide announcement feed (first page, ~30 items) |
| `tronclass ann list <course_id>` | Announcements for that specific course |

Dates are formatted in Taiwan locale. If there are no announcements, the command prints a friendly empty-state message and exits.

---

## `view <ann_id> [course_id]`

```bash
tronclass ann view <ann_id> [course_id]
tronclass ann v <ann_id>
tronclass ann v <ann_id> <course_id>
```

Displays a single announcement as a rich, formatted layout:

1. **Metadata** — title (bold), author, created date, and updated date (shown only if the announcement was edited).
2. **Body** — HTML content rendered directly in the terminal: bold text, hyperlinks (OSC 8 where supported), images, and list formatting are preserved. Not raw HTML and not stripped-to-plaintext — actually rendered.
3. **Attachments** — each file is shown with its `ref_id` and a clickable download link when available. Use the `ref_id` with `ann download`.

**Lookup strategy:**
- With `course_id`: the CLI fetches directly from that course's announcements (fast, exact).
- Without `course_id`: the CLI pages through up to 5 pages of the global feed looking for the ID. If the announcement is older or not in the global feed, pass the `course_id` explicitly.

**Tip:** If `ann view <ann_id>` can't find the announcement, try running `tronclass ann list <course_id>` to confirm the ID, then re-run `ann view` with both arguments.

---

## `download <ref_id> [output]`

```bash
tronclass ann download <ref_id> [output]
tronclass ann d <ref_id>
tronclass ann dl <ref_id> ./notice.pdf
```

Downloads an attachment from an announcement. `ref_id` is shown in the Attachments section of `ann view`. When `output` is omitted, the file is saved to `~/Downloads/<filename>` using the server-provided filename.

---

## Workflow Examples

**Browse latest school-wide announcements and read one:**
```bash
tronclass ann list                       # note the id of interest
tronclass ann view <ann_id>              # full HTML-rendered view
```

**Read a course-specific announcement:**
```bash
tronclass courses list                   # get course_id
tronclass ann list <course_id>           # note the ann_id
tronclass ann view <ann_id> <course_id>  # faster: skips global search
```

**Download an attachment from an announcement:**
```bash
tronclass ann view <ann_id>              # note ref_id in Attachments
tronclass ann download <ref_id>          # saves to ~/Downloads/
```
