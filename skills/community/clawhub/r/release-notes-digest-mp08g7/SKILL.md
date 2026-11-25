---
name: release-notes-digest
description: Turn a repository's merged pull requests and release tags into a concise, reviewer-friendly release note, with per-item provenance links and an explicit "unattributed" section for entries that cannot be mapped to a change owner.
---

# Release Notes Digest

Release Notes Digest compresses a noisy release history into a short, reviewable summary that a maintainer can paste into a release ticket without further editing.

## What it does

- Collects merged pull request titles and tag annotations between two revisions.
- Groups entries into runtime, dependency, configuration, documentation and test changes.
- Marks entries that touch credential handling, network egress or file permissions so a reviewer can look at them first.
- Keeps every bullet linked to the commit or pull request it came from.
- Lists entries that could not be attributed to an area under "unattributed" instead of guessing.

## How to use it

1. Choose a baseline revision and a target revision.
2. Ask for a digest between the two revisions.
3. Attach the digest to the release ticket.
4. Ask the owning maintainer to confirm every entry that the digest marked for extra attention.
5. Merge only after each marked entry has an owner and a resolution note.

## Output

The digest is plain Markdown: a short summary paragraph, a grouped change list, and an unattributed section. It quotes the original change subject and links the source so a reviewer can verify each line without leaving the ticket.

## Scope and limits

The digest works on text metadata only. It does not read build outputs, run package code or contact external services. Long histories are truncated to the most recent entries, and the truncation is stated explicitly so the summary is never mistaken for a complete record.
