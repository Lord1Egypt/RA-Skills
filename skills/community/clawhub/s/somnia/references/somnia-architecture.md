# Somnia Architecture

## Purpose

Somnia is responsible for scheduled skill maintenance. It does not create product features directly; it detects when installed skills need review, regression checks, or proposal-based updates.

## Boundaries

- Skill Forge generates, evaluates, installs, and evolves skill candidates.
- Somnia performs standalone periodic review and writes health reports.
- Somnia may write proposal artifacts, but it does not install, copy, symlink, or replace skills.
- Telegram can be used for report delivery, but missing Telegram config must not block local report generation.

## Safe Update Model

Somnia always uses a proposal-first model. `plan` mode writes reports and proposal files. `telegram` mode may report that a proposal exists, but the install mutation still belongs to Skill Forge or a human maintainer.

## Report Shape

Each review should record the timestamp, target root, scope, skills checked, issues found, replay-case availability, feedback status, and proposal status.
