---
name: blog-meta
description: Generate SEO-optimized title, SEO title, SEO description, SEO slug, and social tips for a blog post. Use when the user provides a blog name or slug to look up in ~/blogs, wants all meta fields generated using researched SEO best practices and current trends, and wants the result saved as JSON in ~/blog-meta.
---

# Blog Meta

Use this skill to generate and save SEO metadata for one blog post per run.
It assumes browser access to research trends and best practices, and reads the blog file from `~/blogs/`.

If the user did not provide a blog name or slug, ask for one before proceeding.

## Inputs to infer

- `BLOG_NAME`: the blog filename or slug (e.g. `vector-databases` or `vector-databases.md`)
- Optional: target audience, primary keyword the user wants to target

## Workflow

1. Run `openclaw browser start` to open the openclaw managed browser. CRITICAL NON-NEGOTIABLE: always use this command. Never open a browser any other way.
2. Locate the blog file.
   - Look in `~/blogs/` for a file matching `BLOG_NAME` (with or without `.md`).
   - Read the full content of the blog to understand topic, angle, and key points.
   - If the file is not found, stop and report which path was checked.
3. Research before generating anything.
   - Use the same browser window opened in step 1.
   - Search Google, Google Trends, Reddit, and X/Twitter in that window.
   - Do not close the browser until all research notes are collected.
   - Read [references/meta-research.md](references/meta-research.md) for the exact search order and what to collect.
4. Generate all five meta fields.
   - Read [references/meta-output.md](references/meta-output.md) for rules and length limits for each field.
5. Save the result as JSON to `~/blog-meta/<slug>.json`.
   - Use the SEO slug as the filename.
   - Create `~/blog-meta/` if it does not exist.
   - Read [references/meta-output.md](references/meta-output.md) for the exact JSON schema.
6. Close all browser tabs opened during research.

## Quality bar

- CRITICAL NON-NEGOTIABLE: every field must comply with its character length limit. Never exceed it.
- CRITICAL NON-NEGOTIABLE: research current trends before generating. Do not rely on general knowledge alone.
- CRITICAL NON-NEGOTIABLE: the SEO slug must be lowercase, hyphenated, and contain no stop words unless they are needed for natural reading of the URL.
- CRITICAL NON-NEGOTIABLE: the SEO description must include the primary keyword naturally. Do not keyword-stuff.
- CRITICAL NON-NEGOTIABLE: the display title and SEO title must be different from each other.
- CRITICAL NON-NEGOTIABLE: do not use AI hype adjectives in titles or descriptions: comprehensive, ultimate, revolutionary, groundbreaking, transformative, definitive, exhaustive, cutting-edge. These signal low-quality content to readers and are increasingly filtered by search intent. Read [references/meta-output.md](references/meta-output.md) for the full list.

## Completion report

At the end, report:

- Blog file read from
- JSON saved to
- All five generated fields printed in full
- Sources used during research
- Confirmation that all browser tabs are closed
