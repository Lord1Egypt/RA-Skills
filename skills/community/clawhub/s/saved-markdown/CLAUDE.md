# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill ("saved-markdown") for publishing Markdown, HTML, and JSX pages anonymously to https://saved.md. No auth, no accounts — publish via API and get a shareable URL. Pages are immutable; edits create new pages via a remix flow.

## Architecture

- **`SKILL.md`** — Main skill definition: routing logic, publishing API spec, chart syntax, content generation rules, user workflow options (one-shot, interactive, local-only, enhance), and HTML styling preferences. Entry point that Claude Code loads when the skill triggers.
- **`entries.json`** — Append-only log of all published pages. Every publish must log here with id, url, deletePhrase, title, contentType, sizeBytes, and createdAt.
- **`templates/`** — Content-type template blueprints split into `markdowns/`, `htmls/`, and `jsx/`. Files define scaffold structure, styling guidance, interaction/data contracts, and validation checklists. Loaded based on the routing table in SKILL.md.
- **`agents/`** — Agent-facing documentation for external consumers:
  - `agents/llms/core.md` — Core API reference (source of truth for publishing, charts, images, sanitization)
  - `agents/llms/markdown.md`, `html.md`, `jsx.md` — Format-specific generation guides
  - `agents/install.md` — Installation instructions
  - `agents/savedmd-documents-skill/` — A bundled variant of the skill with its own SKILL.md, entries.json, and template files

## Key API

- **Publish:** `POST https://saved.md/api/pages` (JSON body preferred, 100 KB max)
- **Fetch source:** `GET /api/pages/{id}` — returns JSON with `markdown` and `contentType`
- **Remix:** Fetch source, apply edits, POST again to get a new URL (old page unchanged)
- **Content types:** markdown (default), `"html"`, `"jsx"` — set via `contentType` field

## Charts

Fenced code blocks tagged `markdown-ui-widget` with types: `chart-line`, `chart-bar`, `chart-pie`, `chart-scatter`. Data is CSV. Values must be plain numbers only (no K/M/B/% suffixes). No other widget types supported.

## Key Constraints

- Pages are **immutable** — changes always produce a new URL
- HTML pages: no interactive elements except `<a>` links (no buttons, menus, forms)
- HTML styling: dense layout, single container, `max-width: 1100px`, compact cards
- Only include scaffold sections where actual data exists — never invent content to fill gaps
