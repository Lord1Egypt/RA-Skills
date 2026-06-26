# Plan: README Formatter

**Date:** 2026-03-11
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private

## Goal

A tool that takes any repo and rewrites its README to follow the WIP Computer standard. Same way wip-release enforces the release pipeline, `wip-readme-format` enforces the README structure.

---

## The Standard

Every README follows this structure. Nothing else.

```
[badges]                           <- auto-generated from detected interfaces
# Tool Name
Tagline.                           <- what it solves, not what it is technically

## Teach Your AI to [verb]
[onboarding prompt block]          <- copy-paste into any AI

## Features
[feature list]                     <- name, description, stability tag

## Interface Coverage              <- (toolbox repos only)
[table]                            <- auto-generated from wip-install --json

## More Info
- Technical Documentation ... link
- Universal Interface Spec ... link
- [other docs]

## License
[standard block]
```

Reference implementations:
- Multi-tool toolbox: `wipcomputer/wip-ai-devops-toolbox`
- Single tool: `wipcomputer/memory-crystal`

Reference spec: `ai/product/notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md`

---

## Phase 1: Core Formatter

**What to build:**
- `wip-readme-format /path/to/repo` ... rewrites README.md to follow the standard
- `wip-readme-format /path/to/repo --dry-run` ... shows what would change without writing
- `wip-readme-format /path/to/repo --check` ... validates README matches standard, exits 0/1

**How it works:**
1. Run `wip-install --json /path/to/repo` to detect all interfaces
2. Read the existing README.md (if any)
3. Extract content that belongs in each section (parse headings, look for existing content)
4. Generate the new README from the standard template, filling in:
   - Badges from detected interfaces
   - Tool name from package.json
   - Tagline from package.json description (or existing README first line)
   - "Teach Your AI" block (templated, points to the repo's SKILL.md on GitHub)
   - Features from SKILL.md sections or existing README features
   - Interface coverage table from detection results (toolbox repos only)
   - More Info links (TECHNICAL.md if it exists, Universal Interface Spec, other detected docs)
   - License block from LICENSE file or `.license-guard.json`
5. Move anything that doesn't fit the standard to TECHNICAL.md (create if needed)

**Key decisions:**
- The formatter reads SKILL.md to generate the features list. SKILL.md is the source of truth for what a tool does.
- For toolbox repos, it generates the interface coverage table automatically. No more manual table maintenance.
- Content that doesn't fit any section (build instructions, API docs, architecture) gets moved to TECHNICAL.md, not deleted.
- The "Teach Your AI" block is templated. It uses the GitHub URL pattern: `github.com/{org}/{repo}/blob/main/SKILL.md`.

**Status:** TODO

---

## Phase 2: Badge Generation

**What to build:**
- Generate shields.io badges for each detected interface
- Match the DevOps Toolbox badge style: `[![CLI](https://img.shields.io/badge/interface-CLI-black)](...)`
- Link each badge to the relevant file (SKILL.md, mcp-server.mjs, openclaw.plugin.json, etc.)

**Status:** TODO

---

## Phase 3: Validation Mode

**What to build:**
- `--check` flag that validates an existing README without rewriting it
- Checks: has all required sections, sections are in the right order, no technical content in README that belongs in TECHNICAL.md
- Exit code 0 (pass) or 1 (fail) for CI integration
- Could be integrated into wip-release as a pre-release gate (like license-guard)

**Status:** TODO

---

## Phase 4: Toolbox Integration

**What to build:**
- Add to the DevOps Toolbox as a new tool in `tools/wip-readme-format/`
- CLI interface (package.json bin entry)
- Skill interface (SKILL.md)
- Universal Installer detects and deploys it
- Update the toolbox README and interface coverage table

**Status:** TODO

---

## Files to Create

```
tools/wip-readme-format/
  package.json
  format.mjs          <- the formatter
  templates/           <- README templates (single-tool, toolbox)
  SKILL.md
```

---

## Done Criteria

- [ ] `wip-readme-format /path/to/repo` generates a compliant README
- [ ] `wip-readme-format /path/to/repo --dry-run` previews without writing
- [ ] `wip-readme-format /path/to/repo --check` validates existing README
- [ ] Interface coverage table auto-generated from `wip-install --json`
- [ ] Technical content moved to TECHNICAL.md (not deleted)
- [ ] Badges generated from detected interfaces
- [ ] Dogfooded: run on wip-ai-devops-toolbox itself, output matches current README
- [ ] Added to toolbox, appears in interface coverage table
