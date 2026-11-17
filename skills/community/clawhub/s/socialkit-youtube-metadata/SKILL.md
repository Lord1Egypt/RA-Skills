---
name: socialkit-youtube-metadata
description: Writes YouTube packaging for a video - title options, description with chapters and links, tags, category, made-for-kids declaration and a thumbnail brief - into metadata.json and validates it against YouTube limits. Use when the user needs a YouTube title, description, tags, chapters or thumbnail idea.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core
---

# YouTube metadata

Apply socialkit-social-core. Titles and thumbnails must describe what the video delivers.

## Steps

1. Read `script.md` (and the final video length if assembled).
2. Propose 3-5 title options (each 100 characters or fewer; aim for under 60 so it is
   not truncated) and let the user choose or edit.
3. Draft the description: first two lines carry the hook and main link; then summary,
   chapters (`00:00 Intro` format, from the script sections), links, disclosures.
4. Propose up to 15 relevant tags. Ask the user to choose the category and to declare
   whether the video is made for kids. Never assume `madeForKids`.
5. Write a thumbnail brief: one focal subject, at most 4-5 words of text, high contrast,
   1280x720. The user creates or supplies the image and saves it in the project folder.
6. Write `metadata.json`:
   ```json
   {
     "title": "...",
     "description": "...",
     "tags": ["..."],
     "categoryId": "22",
     "defaultLanguage": "en",
     "madeForKids": false,
     "thumbnail": "thumbnail.png"
   }
   ```
7. Validate: `node scripts/metadata-check.mjs --dir <project-folder>`. Fix every error
   and mention warnings to the user.

See [category IDs](references/categories.md).

## Output contract

A valid `metadata.json` (check exits 0) and a thumbnail brief in the reply.

## Failure handling

- Check fails: fix the reported fields and re-run. Do not shorten text in a way that
  changes its meaning without asking.
- No thumbnail yet: leave `thumbnail` out and tell the user YouTube will pick a frame.
