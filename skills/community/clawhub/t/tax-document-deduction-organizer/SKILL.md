---
name: tax-document-deduction-organizer
description: >-
  Help users with Validated demand: Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and handoff checklists before filing or sending records to an accountant. This requirement is supported by 9 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.. Use when a user asks for business-and-operations, tax documents, deductions, receipts, estimated taxes, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Tax Document Deduction Organizer

## Requirement

Use this skill to help self-employed workers, small business owners, tax preparers, families, and finance admins preparing tax packets from scattered records with:

> Validated demand: Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and handoff checklists before filing or sending records to an accountant. This requirement is supported by 9 separate online signals across 1 source families, so it represents broader demand rather than a single isolated request.

Demand score: 90/100 (`70/70` demand, `30/30` local feasibility).
Evidence: 9 signals across 1 source families.

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Turn the operational problem into a repeatable process, checklist, template, or lightweight analysis.
3. Ask only for missing information that materially changes the output; otherwise make reasonable assumptions and continue.
4. Keep the implementation local-hardware friendly: prefer scripts, templates, checklists, and small-model or CPU-safe workflows over cloud-only or large-training approaches.
5. Produce the requested artifact, workflow, checklist, analysis, code change, or decision support.
6. Validate the output against the success criteria and list any remaining risks or follow-up work.

## Expected Outputs

- A tailored answer or artifact for the user's immediate situation.
- A reusable checklist or workflow when the task is repeatable.
- A verification note showing how the result was checked.

## Validation

- The output directly addresses the discovered requirement.
- The user can act on the result without reading the original source post.
- Assumptions, limits, and required inputs are visible.
- The final response includes a short usage or next-step note when helpful.

## Triggers

Keywords: `business-and-operations`, `tax documents`, `deductions`, `receipts`, `estimated taxes`, `filing checklist`

Example trigger sentences:

- `Help me Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
- `I need a practical workflow for Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
- `Use $tax-document-deduction-organizer to handle Tax preparers and taxpayers need practical help organizing income statements, receipts, deductions, estimated taxes, and.`
