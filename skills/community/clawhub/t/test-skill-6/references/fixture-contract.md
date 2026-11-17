# Fixture contract

This directory is a minimal, portable OpenClaw skill fixture for testing skill
discovery and packaging. It intentionally requires no credentials, network
access, package installation, or OpenClaw configuration.

## Required runtime contract

- The folder name and frontmatter `name` are both `openclaw-test-skill`.
- `SKILL.md` is present and begins with YAML frontmatter.
- The skill runs on macOS and Linux with a POSIX `sh` shell.

## Expected packaged files

Every regular, non-hidden file in this directory is text-based and accepted by
ClawHub's skill packager:

- `SKILL.md`
- `agents/openai.yaml`
- `assets/expected-output.txt`
- `references/fixture-contract.md`
- `scripts/verify.sh`

No hidden install state, binary asset, lockfile, or unsupported extension is
part of the fixture.
