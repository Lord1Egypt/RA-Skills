---
name: socialkit-content-repurpose
description: Turns one source (a video script, blog post, transcript, talk or notes) into separate, platform-appropriate drafts for Facebook, Instagram, Threads and other connected platforms, each in its own post folder ready for approval and publishing. Use when the user wants to repurpose, cross-post or adapt one piece of content for several social platforms.
license: MIT
metadata:
  author: Ahmad Hussain
  requires: socialkit-social-core
---

# Content repurpose

Apply socialkit-social-core voice rules to every draft. Each platform gets its own text written
for that platform, not the same text pasted everywhere. See
[adapting guide](references/adapting.md).

## Steps

1. Ask which platforms, and read the source.
2. Get the limits and notes: `node scripts/repurpose.mjs --guide --platforms <ids>`
3. Create folders: `node scripts/repurpose.mjs --init --source <file> --out <folder> --platforms <ids>`
4. Write each `<folder>/<platform>/post.json`: pick the kind, write the text within the
   platform's limit, add media and alt text, keep claims identical to the source.
5. Validate all: `node scripts/repurpose.mjs --check --out <folder>`
6. Show every draft side by side. For each one the user wants, they approve it with the
   socialkit-social-core post script in their own terminal. Publish with the platform's posting
   skill, or add the folders to a socialkit-content-calendar.

## Output contract

One post folder per platform, all passing `--check`, plus a short summary of how each
draft differs from the source.

## Failure handling

- A platform is not available in `--guide`: it is not supported yet; say so.
- `--check` errors: fix the draft; never cut text in a way that changes its meaning
  without asking.
