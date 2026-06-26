---
name: resume-job-match-lab
description: Tailor resumes and project bullets to a target role, quantify gaps, and
  prepare an interview-ready evidence map.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Resume Job Match Lab

## Purpose

Tailor resumes and project bullets to a target role, quantify gaps, and prepare an interview-ready evidence map.

## Trigger phrases

- 简历匹配岗位
- tailor my resume
- ATS 优化
- job match analysis
- 面试证据图

## Ask for these inputs

- resume text
- job description
- target seniority
- region/industry
- portfolio or projects if any

## Workflow

1. Extract must-have and nice-to-have requirements from the job description.
2. Score resume coverage against the keyword template.
3. Rewrite bullets to emphasize outcome, scope, and tools without fabricating claims.
4. Generate a gap analysis and interview evidence map.
5. Return both a conservative ATS version and a human-friendly version.

## Output contract

- match scorecard
- rewritten bullets
- gap analysis
- interview evidence map

## Files in this skill

- Script: `{baseDir}/scripts/resume_match.py`
- Resource: `{baseDir}/resources/ats_keywords_template.csv`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 简历匹配岗位
- tailor my resume
- ATS 优化

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/resume_match.py`.
- Bundled resource is local and referenced by the instructions: `resources/ats_keywords_template.csv`.
