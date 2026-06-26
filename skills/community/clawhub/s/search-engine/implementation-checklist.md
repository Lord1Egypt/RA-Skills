# Implementation Checklist — Search Engine

Use this checklist when moving from design to production.

## Pre-Build

- define retrieval contract and acceptance metrics
- confirm source systems and data ownership
- lock schema and identifier policy

## Build

- implement deterministic ingestion and deduplication
- implement retrieval pipeline with explicit stages
- implement query logging and stage-level latency metrics

## Validation

- run offline benchmark suite
- verify latency and error budgets
- test rollback on a staging-like environment

## Rollout

- start with limited traffic slice
- monitor relevance and latency in near real time
- expand gradually only after stability window passes

## Post-Rollout

- document deltas from expected behavior
- record incident learnings in `incidents.md`
- schedule next evaluation cycle with new query samples
