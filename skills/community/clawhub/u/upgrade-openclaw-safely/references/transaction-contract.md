# Legacy record-only transaction contract

This document describes the historical upgrade-transaction.mjs format. It is retained for interpreting old records, not for new upgrades. Start with [the current skill](../SKILL.md) and [native updater semantics](native-updater.md).

The legacy PLAN_READY / CORE_UPDATE_RUNNING / CORE_APPLIED / SERVICE_ACTION_RUNNING / SERVICE_RECONCILED states were recorded by a local guard that never executed OpenClaw itself. Its run confirmations and supplied pass values were not independent backup or runtime proof.

Known limits: one service action for the entire run, fixed tag/no-restart command generation, fixed 120-second stability threshold and a rolling tail of 20 samples. These cannot represent an approved multi-stage runtime plan or prove a longer complete observation interval. Do not edit a ledger or reset counters to bypass a refusal, and do not use this guard for a new update.

An unresolved old run must first be classified from actual installed/runtime state and its original evidence. Do not treat a new native run or a fresh legacy ledger as recovery of that unknown operation.
