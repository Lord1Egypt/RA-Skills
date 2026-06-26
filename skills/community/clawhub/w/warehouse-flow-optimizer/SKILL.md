---
name: warehouse-flow-optimizer
description: Turn warehouse process notes, bottleneck observations, labor constraints, slotting issues, and service targets into a practical flow optimization brief with bottleneck hypotheses, quick wins, pilot ideas, and operating guardrails. Use when ecommerce ops teams, 3PL managers, or consultants need warehouse improvement guidance without live WMS, OMS, or labor-system integrations.
---

# Warehouse Flow Optimizer

## Overview

Use this skill to structure warehouse improvement work when the team has pain signals but not a full industrial-engineering study. It helps operators turn rough observations into a focused bottleneck and pilot plan.

This MVP is heuristic. It does **not** connect to a live WMS, OMS, labor system, or automation controller. It relies on the user's process notes, KPI summaries, and constraints.

## Trigger

Use this skill when the user wants to:
- reduce pick, pack, or dock bottlenecks
- improve slotting, replenishment, or travel-time efficiency
- stabilize shift throughput during peak periods
- diagnose why order cutoff performance or SLA adherence is slipping
- turn warehouse pain points into a practical improvement memo

### Example prompts
- "Help me identify the biggest warehouse bottleneck from these shift notes"
- "Create a quick-win plan for picking congestion and replenishment delays"
- "How should we think about slotting and labor balance before peak?"
- "Turn these warehouse KPI notes into an optimization brief"

## Workflow

1. Clarify the flow objective, operating window, and service target.
2. Normalize bottleneck signals such as queueing, travel time, pick accuracy, and space use.
3. Separate root-cause hypotheses across receiving, putaway, replenishment, picking, packing, and dock flow.
4. Recommend a short list of quick wins and one pilot path.
5. Return a markdown brief with assumptions, guardrails, and next steps.

## Inputs

The user can provide any mix of:
- throughput, pick rate, pack rate, or dock timing notes
- layout, slotting, replenishment, or congestion observations
- labor plan, shift coverage, or cross-training constraints
- inventory accuracy, stockout, or replenishment delay notes
- carrier cutoff, SLA, or peak-season timing pressure
- automation limits, capex limits, or fixed-layout constraints

## Outputs

Return a markdown warehouse brief with:
- primary bottleneck focus
- flow summary and bottleneck map
- root-cause hypotheses
- quick wins and pilot moves
- operating guardrails and monitoring cues
- assumptions, confidence notes, and limits

## Safety

- Do not claim access to live WMS or labor data.
- Do not present bottleneck hypotheses as proven without observation or measurement.
- Avoid recommending irreversible layout or automation changes from sparse notes alone.
- Keep staffing, safety, and capex decisions human-approved.
- Downgrade confidence when KPI definitions or zone-level detail are unclear.

## Best-fit Scenarios

- ecommerce warehouses or 3PL nodes looking for fast operational triage
- teams preparing for peak, SLA recovery, or labor rebalancing
- operators who need a simple improvement brief before deeper engineering work
- consultants framing a first-pass warehouse optimization plan

## Not Ideal For

- greenfield facility design or detailed simulation modeling
- robotics control logic or automation system tuning
- fully quantified industrial-engineering studies with time-motion data
- workflows that must write changes directly into WMS or labor tools

## Acceptance Criteria

- Return markdown text.
- Include bottleneck, action, pilot, and assumption sections.
- Keep the advisory framing explicit.
- Make the output practical for warehouse operators and ops leaders.
