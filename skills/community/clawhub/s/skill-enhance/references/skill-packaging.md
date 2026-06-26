# Skill Packaging

Use this file when deciding how complete the skill package should be.

## Local Package

Good for:

- project-only use
- fast iteration
- internal experiments
- local installed-skill customization

Usually enough:

- `SKILL.md`
- minimal metadata
- a few references if needed

## Shareable Package

Good for:

- Git-based sharing
- team use
- installation through skill tooling
- locally downloaded skills that the user wants to adapt before reuse

Usually needs:

- `SKILL.md`
- `README.md`
- metadata
- eval prompts
- selected references

## Release-Oriented Package

Good for:

- public sharing
- marketplace submission
- release review

Usually needs:

- a strong description
- human-facing docs
- agent-facing docs
- eval prompts
- review-ready references
- release-note or changelog copy

## Local Modification Rule

If the package being improved already exists locally, treat it as a local-edit workflow:

- identify the exact target path
- verify whether the current environment can edit it
- confirm the path and user intent before applying edits
- if write access is unavailable, stay in analysis mode and say so explicitly
