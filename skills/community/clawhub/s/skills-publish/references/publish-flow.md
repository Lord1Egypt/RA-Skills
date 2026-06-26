# Publish Flow

Use this reference when preparing the final ClawHub release command.

## Core Publish Command

ClawHub publishes a local skill folder with:

```sh
clawhub publish <path> --slug <slug> --name "<display-name>" --version <semver> --tags <tags>
```

Optional but common:

- `--changelog "<text>"`

## Required Inputs

- local skill folder path
- skill slug
- display name
- semver version

## Common Supporting Commands

```sh
clawhub login
clawhub login --token <token>
clawhub whoami
clawhub search "<query>"
clawhub sync --all
```

## Working Rules

- Review the generated publish command before execution.
- Keep the slug stable unless there is a strong reason to rename.
- Use semver for versioning.
- Default tags are usually `latest` unless the user has a release-channel strategy.
- Confirm `clawhub whoami` before the final publish when the CLI is available.
- Treat authentication as CLI login state, not as an app-specific API key field inside the skill package.

## Version Suggestions

Use these defaults only if the user does not have a stronger versioning policy:

| Scenario | Suggested version |
| --- | --- |
| First publish | `1.0.0` |
| Small fix | `1.0.1` |
| Meaningful improvement | `1.1.0` |
| Major rewrite | `2.0.0` |

## Notes

These commands are based on the current OpenClaw ClawHub docs and may evolve. If a command fails unexpectedly, confirm the installed CLI version and current docs.
