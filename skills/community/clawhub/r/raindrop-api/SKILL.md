---
name: raindrop-api
description: Build, debug, and explain integrations with Raindrop.io, including OAuth 2 authorization, bearer-token REST API calls, collections and raindrops CRUD flows, tags and highlights, import or export and backups, and MCP server setup. Use when the user mentions Raindrop.io, bookmark sync, collections, raindrops, highlights, tags, filters, developer.raindrop.io, or wants to connect an app, script, or AI client to Raindrop.io.
---

# Raindrop.io API

## Overview

Use this skill to work against the official Raindrop.io developer platform at `https://developer.raindrop.io/`. Prefer the documented REST API v1 for application logic and the MCP server for AI-client integrations.

## Workflow

1. Decide whether the task belongs to the REST API or the MCP server.
2. Choose an authentication path before writing requests.
3. Map the user task to the smallest relevant endpoint group.
4. Preserve Raindrop.io-specific constraints such as rate limits, collection tree reconstruction, and usage terms.

## Choose The Surface

- Use REST API v1 when building scripts, backends, browser clients, importers, exporters, or bookmark-management features.
- Use the MCP server when connecting an AI client or agent directly to Raindrop.io bookmark data.
- Do not conflate them:
  - REST base: `https://api.raindrop.io/rest/v1`
  - MCP endpoint: `https://api.raindrop.io/rest/v2/ai/mcp`

## Authentication

- For quick personal testing, prefer the app console's test token if the user only needs access to their own data.
- For external applications, use the OAuth 2 authorization-code flow documented in `references/raindrop-reference.md`.
- For authenticated REST calls, send `Authorization: Bearer <access_token>`.
- For MCP clients, prefer interactive OAuth 2.1 when the client supports it. Bearer tokens also work.
- Ask the user for client credentials or a token if they want live API calls and those secrets are not already present in the environment.

## Endpoint Mapping

- Collections:
  - Use collection methods for list, get, create, update, delete, reorder, expand, empty, merge, and remove-many actions.
  - Read the nested-structure section before recreating a sidebar tree. The docs explicitly require multiple calls.
  - Read sharing when inviting collaborators or managing access.
- Raindrops:
  - Use single-raindrop methods for one bookmark at a time.
  - Use multiple-raindrop methods for search, pagination, filters, bulk update, move, and delete.
- Highlights:
  - Use highlight routes for bookmark text highlights and notes.
- User, tags, filters:
  - Use user routes for current-user and public-user data.
  - Use tags routes for list, rename, merge, and delete.
  - Use filters to surface broken links, duplicates, important items, untagged content, and grouped counts.
- Import, export, backups:
  - Use import helpers to parse URLs, check whether URLs already exist, or parse HTML bookmark export files.
  - Use export routes for `csv`, `html`, or `zip`.
  - Use backups routes when the user needs generated backup IDs or downloadable backup files.

## Guardrails

- Respect the published usage terms. The docs explicitly forbid building a product that harms, competes with, or replaces Raindrop.io.
- Assume a rate limit of `120 requests per minute per authenticated user` for OAuth-based requests unless the live headers indicate otherwise.
- Handle `429` with backoff based on the rate-limit headers.
- Send JSON bodies with `Content-Type: application/json`.
- Use ISO 8601 timestamps as documented.
- When exact payload fields matter, load `references/raindrop-reference.md` and follow the relevant section instead of guessing.

## Reference File

Load `references/raindrop-reference.md` when you need endpoint details, auth parameters, route examples, or MCP setup notes.
