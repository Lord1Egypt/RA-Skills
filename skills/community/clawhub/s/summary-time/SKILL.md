---
name: summary_time_keep
description: Use this skill when the user wants the current local time written into a.txt in the current workspace directory, then wants the agent to fetch www.bytedance.com with web_fetch, summarize the returned content into b.txt, and keep both files.
---

# Summary Time Keep

## Overview

This skill performs a tiny filesystem action sequence in the current workspace directory. It writes the current local timestamp into `a.txt`, then uses `web_fetch` to inspect `www.bytedance.com`, writes a concise summary of the returned content into `b.txt`, keeps both files, and reports what happened.

Use this skill when the user asks for any of the following:

- Create or demonstrate the `summary_time_keep` behavior
- Write the current time into `a.txt`
- Fetch `www.bytedance.com` and summarize the returned content into `b.txt`
- Keep both files after writing
- Re-run the same demo in the current workspace directory without deleting files

## Workflow

1. Work directly in the current workspace directory for the active task.
2. Use shell built-ins and standard system tools only for filesystem changes. Do not create or rely on any helper script.
3. In the current workspace directory, create `a.txt`.
4. Fetch the machine's current local time with a system tool and write that timestamp content into `a.txt`.
5. Call `web_fetch` on `www.bytedance.com`.
6. Read the returned content and write a concise summary into `b.txt`.
7. Do not delete, rename, or move either file.
8. Inspect the current workspace directory and tell the user which files were written and confirm that both files remain.

## Behavior Notes

- The timestamp should use the machine's current local time.
- `a.txt` should contain the timestamp content.
- `b.txt` should contain a concise summary of the fetched page content.
- If either file already exists, overwrite it.
- Keep the filesystem changes simple and local. Network access is only needed for the `web_fetch` step.
- Do not ask the user for a target path unless they explicitly want behavior different from the current workspace directory.
- If you need to confirm the result, inspect the directory after writing with `ls` or equivalent.
- If `web_fetch` fails, report that clearly instead of inventing a summary.
