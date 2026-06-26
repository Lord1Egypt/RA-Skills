# Roadmap

## Near Term

- auto-extract more repository conventions from additional files:
  - `pyproject.toml`
  - `pytest.ini`
  - `biome.json`
  - `.eslintrc*`
- add conflict detection between user request scope and active rulesets
- add richer repo-aware output fields:
  - impacted validation commands
  - inferred style tools
  - doc update hints
- add publish metadata and examples for ClawHub release

## Mid Term

- support richer metadata in generated handoffs:
  - risk level
  - recommended first slice
  - suggested validation depth
  - dependency sensitivity
- add a lightweight prompt-lint mode to flag vague or weak compiled briefs
- add optional language presets for Chinese-first and English-first output

## Productization

- prepare a cleaner publish-ready package layout
- add packaging/release notes for sharing outside the current workspace
- add a small examples gallery for onboarding new users quickly
- document a recommended maintenance workflow for evolving templates and tests together

## Stretch Ideas

- add a compare mode that shows how one raw request maps to different task types
- add a "tighten scope" mode for overly broad product requests
- add a "handoff for reviewer" mode focused on evaluation and code review instructions
