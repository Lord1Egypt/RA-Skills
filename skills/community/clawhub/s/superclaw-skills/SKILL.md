---
name: superclaw
description: "14 production-tested agent workflow skills for disciplined, high-quality AI coding and task execution. Covers TDD, debugging, code review, planning, brainstorming, verification, subagent dispatch, and more. Built by operators who run agents in production daily."
---

# SuperClaw by Kamir Labs

A collection of 14 OpenClaw skills that enforce disciplined, verifiable agent workflows.

## What's Included

| Skill | When to Use |
|-------|------------|
| **brainstorming** | Before creative or feature-design work |
| **dispatching-parallel-agents** | 2+ independent tasks that can run in parallel |
| **executing-plans** | Execute a written plan with checkpointed reviews |
| **finishing-a-development-branch** | After implementation, choose merge/PR/cleanup path |
| **receiving-code-review** | Processing review feedback, especially ambiguous comments |
| **requesting-code-review** | Before merge to verify quality and requirements |
| **subagent-driven-development** | Execute plans via independent subagent tasks |
| **systematic-debugging** | Bugs and failures — root cause before fixes |
| **test-driven-development** | Before writing implementation code |
| **using-git-worktrees** | Feature work that needs workspace isolation |
| **using-superpowers** | Session start — identify the right skill first |
| **verification-before-completion** | Before any "done" claim — prove it works |
| **writing-plans** | Multi-step tasks that need concrete execution plans |
| **writing-skills** | Creating, editing, or validating skills |

## Install

```bash
npx clawhub@latest install superclaw
```

## Philosophy

Stop guessing. Stop claiming "done" without evidence. Stop debugging by random changes. These skills enforce the patterns that separate reliable agent work from chaos.
