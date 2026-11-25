---
name: SVG MIME Canary i44712
description: Inert canary skill used during an authorized ClawHub assessment to observe the HTTP headers applied when a published skill ships an SVG file.
version: 0.0.1
---

# SVG MIME Canary i44712

This skill is an inert canary created during an authorized assessment of the ClawHub publishing and file-serving pipeline. Its only purpose is to ship one static SVG file so that the HTTP representation of a published skill file with an `.svg` extension can be observed.

## Contents

- `SKILL.md` - this document
- `assets/icon.svg` - a 40x20 green rectangle, no script, no external references, no animation

## What it tests

1. Which `Content-Type` the platform returns for a stored `.svg` file (`image/svg+xml` expected).
2. Whether `Content-Disposition` is set to `attachment` for stored skill files.
3. Which `Content-Security-Policy` value is attached to stored skill files.
4. Whether a relative-path request to the platform's Vercel image optimizer (`/_vercel/image?url=/api/v1/skills/.../file?path=...`) will forward the file, and with which headers.

## Usage

There is no runtime behaviour and no agent instruction here. Nothing is executed. The SVG is a static green rectangle; it contains no script elements, no event attributes, no external references, and no CSS.

## Notes

The skill is intended to be public for the duration of the assessment and then left untouched. It does not contact any network endpoint at any point. Anyone reviewing the skill can confirm the entire artefact is the two files listed above.
