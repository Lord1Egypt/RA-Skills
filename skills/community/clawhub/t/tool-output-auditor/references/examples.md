# Real Output Patterns

## Success
```text
[OK] Successfully packaged skill to: /tmp/example.skill
```
Interpretation: success. The output explicitly proves the intended artifact exists.

## Failure
```text
Error: Path must be a folder
(Command exited with code 1)
```
Interpretation: failure. Stop and fix the path.

## Partial
```text
Command still running (session abc123)
```
Interpretation: partial. The process has not finished, so success is not established.

## Ambiguous
```text
Security: CLEAN
Warnings: yes
Checked: 2026-03-24T16:21:30.477Z
```
Interpretation: ambiguous. Something completed, but the remaining warning may still change the next action.

## Common agent mistake
```text
Preparing clawhub-release-auditor@0.1.0
```
Bad next step: "Published successfully."
Why wrong: preparation is activity, not proof of completion.
