
---
name: tosr-test-skill-1787627998
description: 一句话描述该 Skill 的功能和使用场景
---
	# TOSR Test Skill For Delete

> TOSR Test Skill For Delete — version 0.1.0

## Description

This is an automated integration test skill (tosr-test-skill-1787627998) created by the TOSR project.
The purpose is to verify the complete skill lifecycle through the clawhub REST API,
including creation, version updates, and deletion.

## Test Identifier

- Slug: tosr-test-skill-1787627998
- Version: 0.1.0
- Created: 2026-08-25T11:19:58+08:00

## How It Works

This skill validates the following operations against the real clawhub API:

1. **Publish** — Creates a new skill via POST /api/v1/skills with multipart form data
2. **Inspect** — Retrieves skill metadata via GET /api/v1/skills/{slug}
3. **Update** — Publishes a new version of an existing skill
4. **Delete** — Removes the skill via DELETE /api/v1/skills/{slug}

## Notes

This skill is ephemeral and will be automatically deleted after the test completes.
If you see this skill listed on clawhub, it means a test run failed to clean up properly.
