# Project Skill Context

## 1. Purpose in This Project

- Skill name: release-notes-generator-skill
- Primary use in this project: generate markdown release notes for internal releases.
- Out of scope: publishing external marketing copy.
- Typical tasks this skill supports here: generate a draft release-notes file from structured JSON input.

## 2. Repository / Environment Context

- Repository name: release-notes-project
- Primary working directory: repository root
- Relevant subdirectories: `data/`, `dist/`
- Main language(s): Python
- Runtime / toolchain: Python 3.11+

## 3. Required Commands

- Generate notes: `python3 ../../reference-skills/release-notes-generator/scripts/generate_release_notes.py data/release-input.json dist/release-notes.md`
- Validate notes: `python3 ../../reference-skills/release-notes-generator/tests/test_generate_release_notes.py`

## 4. Inputs and Outputs

- Release-note input file path: `data/release-input.json`
- Generated output path: `dist/release-notes.md`
- Files or directories that must not be modified: anything outside `data/` and `dist/` for this workflow

## 5. Project Conventions

- Heading/title format: `# Release Notes - <version>`
- Required sections: `Highlights`, `Changes`
- Review expectations: confirm file exists and contains required sections

## 6. Constraints and Guardrails

- Never: overwrite unrelated docs
- Always: read the input file before generating output
- Ask before: changing output format or target path

## 7. Validation Requirements

- Required checks: generated file exists and contains required sections
- Evidence needed before completion: output path and validation result

## 8. Local Usage Examples

### Example 1
- Goal: generate release notes draft
- Files involved: `data/release-input.json`, `dist/release-notes.md`
- Commands: `python3 ../../reference-skills/release-notes-generator/scripts/generate_release_notes.py data/release-input.json dist/release-notes.md`
- Expected result: markdown file written to `dist/release-notes.md`

### Example 2
- Goal: validate the release-notes workflow
- Files involved: `../../reference-skills/release-notes-generator/tests/test_generate_release_notes.py`
- Commands: `python3 ../../reference-skills/release-notes-generator/tests/test_generate_release_notes.py`
- Expected result: test prints PASS and exits 0
