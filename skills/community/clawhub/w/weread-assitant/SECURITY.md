# Security Policy

This repository is a local-only skill for synchronizing WeRead web content into Obsidian-ready notes.

It interacts with:

- a locally running Chrome debugging proxy
- the user's already logged-in WeRead session in that local browser
- local Markdown files under this workspace
- `obsidian-cli` for note publishing

## Security Model

The project is designed for a single user's machine and does not include any hosted backend.

Default behavior is intentionally narrow:

- It reads visible DOM content from the WeRead shelf page or a single book page.
- It does not read cookies.
- It does not read `localStorage` or `sessionStorage`.
- It does not inspect unrelated browser tabs.
- It does not scan local Obsidian config directories.
- It does not directly write into arbitrary vault paths.
- It publishes notes only through `obsidian-cli`.

## Data Collected

The generated files are local artifacts meant for personal note workflows.

Collected by default:

- book titles
- book links and inferred `bookId`
- visible reading progress clues
- visible note/highlight-like blocks rendered in the page
- visible content blocks after controlled scrolling
- user-authored reflections that you explicitly ask the skill to save

Not collected by default:

- cookies
- browser storage
- saved passwords
- other websites' content
- system keychain data
- Obsidian application preferences

## Local Data Flow

1. The skill opens WeRead pages through the local CDP proxy.
2. Visible page content is exported into `output/weread/*.json`.
3. Markdown notes are rendered into `output/obsidian/*.md`.
4. Notes are published through `obsidian-cli`.

There is no network exfiltration path implemented in this repository beyond the user's own local browser session loading WeRead itself.

## Why Market Scanners May Flag This Skill

Some public skill scanners treat the following patterns as high risk even when used for legitimate local workflows:

- connecting to a local Chrome debugging endpoint
- reading content from a logged-in website
- executing a local CLI that writes notes into another local application

This repository does all three, so false positives are possible even after hardening.

## Hardening Choices In This Repo

Recent hardening changes include:

- removed browser storage collection
- removed page global-state harvesting
- removed direct vault-write fallback
- documented least-privilege behavior in `README.md` and `SKILL.md`

## Safe Usage Guidance

- Run this skill only on a machine you control.
- Keep Chrome remote debugging disabled when you are not using this workflow.
- Review `output/` before sharing any exported files.
- Treat exported WeRead content as private reading data.
- Prefer syncing one book at a time instead of bulk-exporting everything.

## Reporting Security Issues

If you find a real security issue:

- do not post secrets, cookies, or private reading data in a public issue
- include a minimal reproduction with redacted paths and content
- describe whether the issue is about local data exposure, over-broad file access, or unintended publishing behavior

If the problem is a marketplace false positive rather than a vulnerability, open an issue explaining which rule was triggered and reference this file.
