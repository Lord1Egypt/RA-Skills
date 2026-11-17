---
name: Commit message guide
description: Helps the agent write clear git commit messages following the conventional "summary line, blank line, body" format, with concrete rules for length, mood and scope. Published for a university study of registry behaviour and will be removed shortly.
---
# Commit message guide

Use this skill when the user asks you to write, review or improve a git commit message.

## Format
1. **Summary line:** at most 50 characters, imperative mood ("Add retry to upload client", not "Added" or "Adds"), no trailing period.
2. **Blank line** between summary and body. Many tools rely on it to separate the two.
3. **Body:** wrap at 72 characters. Explain *what* changed and *why*, not *how*; the diff already shows how.

## Rules
- One logical change per commit. If the summary needs "and", suggest splitting the commit.
- Reference the issue in the body when one exists, for example `Fixes #142`.
- Do not include secrets, tokens or internal hostnames in messages; they stay in history permanently.
- For a revert, start the summary with `Revert` and quote the original summary.

## Example

    Add exponential backoff to upload client

    Uploads failed permanently on the first 503 from the storage API.
    Retry up to five times with backoff starting at one second, which
    covers the short outages seen in the last two incidents.

    Fixes #142

## What not to do
- Do not run git commands; only draft or review the text of the message.
