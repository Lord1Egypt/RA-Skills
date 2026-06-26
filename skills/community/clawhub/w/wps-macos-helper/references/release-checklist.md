# release-checklist

## Pre-release checks

### Trigger quality
- Skill should trigger only for macOS + WPS document workflow requests.
- Avoid triggering on generic office questions that `office` or `word-docx` already cover better.

### Safety
- Original files should not be overwritten by default.
- Scripts should create new outputs or workflow notes.
- No GUI automation should run by default.
- No external credential or cloud dependency should be required for the default workflow.

### Test cases
- Markdown input: route guidance should work and produce a next-step note when requested.
- PDF/docx input: conversion entry point should produce Markdown output when toolchain is available.
- Missing dependency case: script should fail safe and write a fallback workflow note when `uvx` is unavailable.
- Unknown format: script should fail safe and suggest inspection first.

### Documentation quality
- Core workflow is short and clear.
- Compatibility guidance is practical.
- Export checks are explicit.
- Troubleshooting gives a safe escalation path.

### Publish readiness
- Skill name is stable.
- Description is precise.
- References do not duplicate each other too much.
- Script is executable and tested on representative cases.
