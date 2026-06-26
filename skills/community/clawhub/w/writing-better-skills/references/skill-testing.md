# Skill Testing

A better skill should be testable in two ways: artifact testing and behavioral testing.

## 1. Artifact testing

Artifact testing verifies the files shipped with the skill.

Test these when present:
- scripts run successfully
- generated outputs exist where expected
- package/validation commands work
- examples stay coherent
- self-healing scripts fix only the intended narrow failure

Typical checks:
- unit tests for Python scripts
- shell smoke tests
- validation against expected files or text

## 2. Behavioral testing

Behavioral testing verifies that another agent can actually use the skill correctly.

Questions to test:
- Does the agent know when to use the skill?
- Does it read `project.skill.md` before acting when local context matters?
- Does it avoid editing the global skill for project-local setup?
- Does it load the right references at the right time?
- Does it use scripts instead of re-implementing deterministic logic?

## Recommended behavioral scenarios

### Scenario A: missing project-local context
Expected behavior:
- agent checks for `project.skill.md`
- if missing, it creates one from `project.skill.template.md`
- it does not guess local paths/commands unnecessarily

### Scenario B: local override exists
Expected behavior:
- agent follows `project.skill.md` instead of generic defaults when they differ

### Scenario C: script failure with safe remediation
Expected behavior:
- test fails for a narrow, known reason
- self-healing runs only if safe
- agent reruns the test
- if still failing, agent stops and reports clearly

## What not to confuse

Passing script tests does not prove the skill is discoverable or easy for another agent to use.

Likewise, a beautifully written `SKILL.md` does not prove the shipped scripts work.

You usually need both kinds of testing.
