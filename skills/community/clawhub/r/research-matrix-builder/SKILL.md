---
name: research-matrix-builder
description: Build literature matrices from papers, notes, and abstracts to compare
  methods, data, findings, and research gaps.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Research Matrix Builder

## Purpose

Build literature matrices from papers, notes, and abstracts to compare methods, data, findings, and research gaps.

## Trigger phrases

- 文献矩阵
- build a literature matrix
- 整理论文综述
- research gap table
- 做研究对比表

## Ask for these inputs

- paper list or notes
- research question
- matrix dimensions
- citation style if needed

## Workflow

1. Normalize each source into the bundled matrix schema.
2. Extract problem, method, data, metric, result, limitation, and gap.
3. Cluster similar methods and contradictory findings.
4. Generate a matrix CSV and a narrative synthesis outline.
5. Keep missing fields explicit and cite where possible.

## Output contract

- literature matrix CSV
- thematic clusters
- gap summary
- review outline

## Files in this skill

- Script: `{baseDir}/scripts/build_matrix.py`
- Resource: `{baseDir}/resources/matrix_schema.csv`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 文献矩阵
- build a literature matrix
- 整理论文综述

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/build_matrix.py`.
- Bundled resource is local and referenced by the instructions: `resources/matrix_schema.csv`.
