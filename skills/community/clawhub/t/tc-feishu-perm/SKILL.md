---
id: feishu-perm
name: Feishu Perm
description: Guidance-only playbook for planning and reviewing Feishu document and folder permission management.
category: Business
requires: []
examples:
  - "Help me design Feishu sharing permissions for our team docs."
  - "Use feishu-perm to review access levels before sharing."
---

# Feishu Permission Management

Use this guidance-only skill to design safe, least-privilege sharing for Feishu documents, folders, and collaborative workspaces.

## When to use

- You need a permission model before sharing internal docs.
- You want to audit existing collaborator access.
- You need a repeatable access review checklist for teams.

## Core principles

- Apply least privilege (`view` by default; elevate only when needed).
- Prefer group/role-based sharing over many individual grants.
- Time-box elevated access for external collaborators.
- Require explicit owner approval for `full_access` grants.

## Permission planning workflow

1. Classify document sensitivity (public/internal/restricted).
2. Identify user groups (owners, editors, reviewers, viewers).
3. Assign minimum required permission per group.
4. Define expiration/review cadence for non-owner access.
5. Document audit trail: who got access, why, and when.

## Access review checklist

- Is every collaborator still active and relevant?
- Do any users have `full_access` without business justification?
- Are external shares still required?
- Are inherited folder permissions too broad?
- Is there a scheduled review date?

## Output format

When asked for help, provide:

- A recommended permission matrix by role.
- High-risk findings in current access design.
- A short remediation plan (immediate fixes + periodic review cadence).
