---
created: 2026-10-08
updated: 2026-10-08
version: 2.0
author: Monika Zapisek (Product Designer / UX Team)
status: accepted
description: Installation instructions for ui-roi-audit in Claude Code, Claude web chat, and Cowork.
project: design-engineering-playbook
source-of-truth: true
url:
---

# Install ui-roi-audit

Install the complete `ui-roi-audit` folder. Keep its internal paths unchanged so `SKILL.md`
can load `references/`, `examples/`, `ATTRIBUTION.md`, and `EVIDENCE.md`.

## Claude Code CLI

Copy the folder to your personal Claude Code skills directory:

```text
~/.claude/skills/ui-roi-audit/
```

For a project-only installation, place it under the project's `.claude/skills/` directory instead.
Start a new session after copying, then ask for an ROI or conversion audit of one page.

## Claude web or chat

1. Create a ZIP whose top-level folder is `ui-roi-audit` and includes `SKILL.md`.
2. In Claude, enable code execution and file creation in Settings if required by your plan.
3. Open **Customize → Skills**, choose **+ → Create skill → Upload a skill**, and upload the ZIP.
4. Enable the skill in the skills list.

## Claude Cowork

Upload and enable the ZIP through **Customize → Skills** as above. Uploaded skills are shared
between Claude chat and Cowork for the same account. Start a Cowork task and request an ROI or
conversion audit; attach the page screenshot or content and provide its conversion goal.

## Verify the installation

Try:

> Run an ROI audit on this landing page. Goal: demo requests. I have monthly visits, conversion
> rate, lead value, and implementation cost.

The response should ask for any missing page or goal input, use source-cited criterion IDs, and
finish with a 12-month ROI range or an explicit qualitative estimate.
