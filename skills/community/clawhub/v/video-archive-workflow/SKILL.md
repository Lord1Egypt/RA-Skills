---
name: video-archive-workflow
description: Video download, metadata extraction, deduplication, subtitle handling, and archive organization for URLs from YouTube/Shorts, Xiaohongshu, Bilibili, and X/Twitter. Use when the user wants to inspect, classify, dedupe, or build a downloadable/archiveable video record from a URL, including sheet field mapping and folder organization.
---

# Video Archive Workflow

## Overview

Use this skill to turn a video URL into a normalized record for a sheet and archive system. Prefer deterministic metadata from yt-dlp, parse tags from page text when needed, and keep the workflow moving with safe defaults unless a hard stop rule applies.

## Core workflow

1. Parse the input URL.
2. Identify platform, video_id, and video_type.
3. Check dedupe by video_id only.
4. Extract metadata from yt-dlp JSON first.
5. Clean title, description, and tags.
6. Resolve uploader and target folder.
7. Download or archive only when asked.
8. Write sheet fields in the required order.

## Use the reference

See [references/field-schema.md](references/field-schema.md) for the exact sheet field order, tagging rules, and platform-specific normalization rules.

## URL parsing rules

- Identify platform from hostname.
- Extract video_id from the platform’s native identifier.
- Set video_type by platform convention when possible.
- If video_type parsing fails, default to `normal` and continue.
- Do not block the workflow for an unknown type.
- If the URL does not point to a video, stop and report that no video record can be filled.

## Dedupe rules

- Use `video_id` only for dedupe.
- If a matching record exists, show a brief summary of the existing video and wait for user confirmation before proceeding.
- Do not require platform for dedupe.
- Do not auto-skip on an uncertain match.

## Metadata rules

- Prefer `yt-dlp -j` or `--dump-single-json` as the source of truth.
- Save the cleaned metadata fields into the sheet.
- Leave unknown or empty fields blank.
- Do not write placeholder text such as `(empty)`.
- Do not write raw JSON paths, download status, or command history into the sheet.

## Tag rules

- Extract tags from title and description first.
- Strip tags from title and description before writing them.
- Do not translate text.
- Keep the first-seen order.
- Remove duplicates.
- Output tags as a space-separated string in the sheet.
- For Bilibili, also parse page tags from `tag-link` text when title/description tags are missing or incomplete.
- For X/Twitter, use the tweet text if available; if the item is not a video, stop.

## Uploader and folder rules

- Use the uploader display name for the folder name.
- If uploader cannot be resolved, stop and ask the user before continuing.
- Do not fall back silently to uploader_id for folder naming.
- For Xiaohongshu, set uploader_id to the displayed Xiaohongshu number when available.
- For multi-uploader cases, keep uploader and uploader_id as comma-separated values in order.
- Use the first uploader as the folder root.
- Sanitize folder names to remove illegal filesystem characters.

## Archive rules

- Keep the original filename style.
- If the source container is mp4, archive to mkv with lossless conversion.
- Keep the source file as `原名_source.mkv`.
- Save the archived file with the original base name in the archive container.
- If a filename conflict exists, stop and ask the user what to do.
- Use the uploader folder directly under the main archive root unless the user asks for deeper nesting.

## Subtitle rules

- Download and embed subtitles only when subtitles exist.
- Skip silently when subtitles do not exist.
- Record subtitle language availability in metadata.
- Do not repeat subtitle presence in the remarks field.

## Field formatting rules

- Use Beijing time implicitly; do not label it.
- Format upload date as `YYYY-MM-DD`.
- Keep source container as the container field.
- Keep resolution in the format returned by yt-dlp when possible.
- Use units in field names where required: `秒`, `MB`, `fps`, `kbps`.

## Stop rules

Stop and ask the user when:

- uploader cannot be resolved
- the URL is not a video
- a filename conflict needs a decision
- the metadata is ambiguous enough to affect folder placement or dedupe

## Output style

Return only the fields the user asked for when they request a sheet preview. Keep it concise and do not add extra narrative unless the workflow is blocked.
