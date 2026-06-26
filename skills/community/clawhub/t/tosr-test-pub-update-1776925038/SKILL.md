# TOSR Publish Then Update Test

> TOSR Publish Then Update Test — version 0.2.0

## Description

This is an automated integration test skill (tosr-test-pub-update-1776925038) created by the TOSR project.
The purpose is to verify the complete skill lifecycle through the clawhub REST API,
including creation, version updates, and deletion.

## Test Identifier

- Slug: tosr-test-pub-update-1776925038
- Version: 0.2.0
- Created: 2026-04-23T14:17:42+08:00

## How It Works

This skill validates the following operations against the real clawhub API:

1. **Publish** — Creates a new skill via POST /api/v1/skills with multipart form data
2. **Inspect** — Retrieves skill metadata via GET /api/v1/skills/{slug}
3. **Update** — Publishes a new version of an existing skill
4. **Delete** — Removes the skill via DELETE /api/v1/skills/{slug}

## Notes

This skill is ephemeral and will be automatically deleted after the test completes.
If you see this skill listed on clawhub, it means a test run failed to clean up properly.
