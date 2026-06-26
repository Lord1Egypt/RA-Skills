# TradeMirrorOS

TradeMirrorOS is a minimal Clawhub skill bundle for trading-memory workflows.

This package is intentionally instruction-only.
It keeps the capability map, memory architecture, and role-specific skill guidance, while leaving runtime code, tests, sync scripts, and remote transport outside the package.

- Public repo: <https://github.com/Topps-2025/TradeMirrorOS.git>
- Chinese README: [`README.zh-CN.md`](README.zh-CN.md)
- Promo copy: [`PUBLIC_PAGE_COPY.md`](PUBLIC_PAGE_COPY.md) / [`PUBLIC_PAGE_COPY.zh-CN.md`](PUBLIC_PAGE_COPY.zh-CN.md)

## What Stays In This Package

- workspace routing for Finance Journal tasks
- instruction-only skills for journaling, plans, reviews, and behavior reports
- architecture and concept docs for long-term trading memory
- lightweight reference docs for data contracts and evolution logic

## What Stays Out

- runtime source code
- tests, examples, and local configs
- git sync workflows, push/pull instructions, and prompt-execution templates
- credentialed operations and remote transport

## Core Structure

- `SKILL.md`: workspace router
- `finance-journal-orchestrator/`: journaling and memory-framing skill
- `trade-plan-assistant/`: planning skill
- `trade-evolution-engine/`: review and self-evolution skill
- `behavior-health-reporter/`: behavior-report skill
- `TRADE_MEMORY_ARCHITECTURE.md`: core architecture overview

## Safety Defaults

- this package should not require secrets, tokens, or git credentials
- any filesystem mutation, remote sync, or publishing action stays under direct user control
- private ledgers, broker exports, `_runtime*`, and `*.db` files do not belong in the public package
