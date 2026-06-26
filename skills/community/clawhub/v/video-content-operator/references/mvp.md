# Video Content Operator MVP

## Purpose
This skill is the decision/orchestration layer above video execution.

It exists to validate whether users want help with:
- understanding their current creator situation
- deciding what content to make
- selecting which materials are worth using
- packaging content for different platforms
- generating draft directions
- deciding the next content move

Not just rendering a video.

## Critical MVP principle
The skill must begin from the **creator's current state**, not from a generic content template.

That means understanding:
- who the user is
- what they are building
- where they already post
- what content pattern they already have
- what their current bottleneck is

In OpenClaw main sessions, memory/context should be used first before asking.

## MVP scope

### In scope
- infer current creator state from memory/context when available
- ask only for missing decision-critical information
- clarify creator/content goal
- evaluate ideas or source materials
- recommend one best content move
- generate 1-3 draft packages
- recommend next action
- package a clean hand-off for execution

### Out of scope
- persistent memory system implementation
- team workflows
- analytics integrations
- automatic publishing
- CRM / monetization tooling
- deep project management

## Success condition
The MVP is successful if users repeatedly use Sparki not only to execute content, but to decide:
- what to make
- which materials to use
- how to package for different platforms
- what to do next after one piece performs or fails

## Failure condition
The MVP is failing if users only want direct video execution and skip this layer entirely.

That would mean the operating layer is either:
- unnecessary
- badly positioned
- too abstract
- or solving the wrong problem
