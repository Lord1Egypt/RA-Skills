# Skill Downloader

> Review-first skill discovery and installation from trusted sources, with explicit user approval before any write action.

## What it does

- Search for skills across trusted registries
- Compare candidates with source labels and available metadata
- Inspect ClawHub-hosted skills before installation
- Support approved installation to either a workspace or global skills directory
- Prefer official source workflows when available

## Safety model

- Discovery and comparison can use trusted network sources
- Installation or update only happens after explicit user approval
- Review source material before writing files
- Prefer official registry workflows over ad-hoc install steps
- Avoid symlink-based installs

## Typical use cases

Use this skill when the user wants to:

- find or compare skills
- check whether a skill exists for a task
- install or update a skill after review
- choose between multiple registry candidates

## Information levels

Results should clearly disclose how complete the information is:

- **Full**: enough information to compare and recommend
- **Partial**: some important fields are unavailable
- **Minimal**: only names or basic source information are available

If information is partial or minimal, disclose the gap before recommending a choice.

## Installation targets

- **Global**: `~/.openclaw/skills/`
- **Local**: `{workspace}/skills/`

## Notes

- Keep `SKILL.md` and `README.md` aligned
- Put low-level command examples and fallback mechanics in reference files rather than the main overview
