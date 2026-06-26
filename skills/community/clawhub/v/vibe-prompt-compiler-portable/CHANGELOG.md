# Changelog

## 2026-03-11

### Added

- added `Chinese-first` language preset across `compile_prompt.py` and `create_handoff.py`
- added dedicated Chinese templates for all supported task types
- added tool-specific wrapper presets for:
  - `generic`
  - `cursor`
  - `codex-cli`
  - `claude-code`
  - `gemini-cli`
- added prompt linting via `scripts/prompt_lint.py`
- added development rulesets:
  - `minimal-diff`
  - `test-first`
  - `repo-safe`
- added repository-aware rule merging via `--repo-rules-file`
- added automatic repository-rule extraction via:
  - `scripts/extract_repo_rules.py`
  - `--repo-root`
  - `--auto-repo-rules`
- added regression and fixture coverage for:
  - realistic web-style requests
  - golden prompt and handoff outputs
  - Chinese-first output
  - tool presets
  - prompt linting
  - development rulesets
  - repository-rule extraction

### Improved

- improved task routing for UI tweaks, architecture requests, and mixed Chinese-English inputs
- improved bugfix routing to reduce false positives from generic words like `error`
- improved handoff output so Chinese-first mode now localizes:
  - wrapper text
  - non-goals
  - deliverables
  - execution rules
- improved README with publish-ready usage examples for language presets, rulesets, and repository-aware flows

### Current Status

The skill now functions as a portable request-to-brief compiler with:

- task routing
- prompt compilation
- structured handoff generation
- language presets
- tool presets
- prompt linting
- development rule injection
- repository-aware rule extraction and merging
- broad regression coverage

## 2026-03-10

### Added

- added new task types:
  - `architecture-review`
  - `integration`
  - `automation-workflow`
- added richer routing rules for architecture, integration, workflow, and deployment requests
- added advanced templates for:
  - architecture review
  - integrations
  - automation workflows
- added tool examples for Gemini CLI and more complex multi-tool usage
- added realistic examples in `references/real-examples.md`
- added structured handoff fields:
  - `non_goals`
  - `deliverables`
- added regression tests:
  - `scripts/test_routing.py`
  - `scripts/test_handoff.py`

### Improved

- improved `README.md` with clearer positioning, usage guidance, and test instructions
- improved `SKILL.md` defaults and task taxonomy
- improved `compile_prompt.py` classification coverage and template support
- improved `create_handoff.py` execution-mode handling and handoff quality

### Current Status

The skill now functions as a portable request-to-brief compiler for coding agents, with:

- documentation
- routing rules
- templates
- realistic examples
- structured handoff output
- regression tests
