# Bug: agents can try to edit public mirrors directly instead of private source

Date: 2026-05-11
Status: open
Owner: unassigned
Component: release pipeline, deploy-public, DevOps Toolkit workflow guardrails
Severity: High

## Summary

An agent saw stale text in the public `wip-codex-remote-control` README and moved toward cloning the public repo to patch it directly. That is the wrong workflow.

For WIP repos with a `-private` counterpart, the public repo is published output, not an edit surface. Public drift must be fixed in the private source repo and then published through the approved release or public-sync path.

## Problem

The visible symptom was real:

- the live install spec said Remote Control public installs should use beta;
- the public GitHub README still showed alpha wording.

The agent optimized for the visible symptom and chose the fastest generic GitHub fix:

```text
clone public repo -> edit README -> public PR -> merge
```

That is normal open-source behavior, but it violates the WIP public/private repo model.

## Correct Invariant

For every WIP repo that has a public/private split:

- Private repo is editable source.
- Public repo is published artifact.
- If public output is stale, fix the private source or the release/sync pipeline.
- Do not clone, branch, commit, or PR against the public mirror to repair drift.
- Direct public repo work is read-only inspection unless Parker explicitly says to work in the public repo.

## Required Behavior

Update the guides and/or tooling so agents cannot miss this rule:

1. Public Dev Guide should state that public mirrors are not working surfaces when a `-private` counterpart exists.
2. Private WIP guide should state the same rule in WIP-specific language.
3. `deploy-public` or branch guard should warn or block when an agent attempts to create an editing branch in a WIP public repo that has a known private counterpart.
4. The rule should explicitly cover tiny README fixes and install-prompt drift.

## Acceptance

- The public and private dev guides say public mirrors are published output, not edit surfaces.
- The rule says public drift is fixed by private-source edits plus release or public sync.
- A guardrail exists in tooling or documented preflight to stop public-mirror edit PRs.
- The guardrail allows read-only inspection of public repos.
- The guardrail can be bypassed only when Parker explicitly directs work in the public repo.
- No em dashes are introduced.

## Non-Goals

- Do not change normal third-party fork workflows.
- Do not forbid read-only public repo inspection.
- Do not use this as a reason to patch public mirrors manually.

