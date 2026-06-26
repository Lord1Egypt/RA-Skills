# Brainstorming — Design Refinement

## Overview

Turn rough ideas into fully-formed designs through natural dialogue. Combines Superpowers' collaborative design process with PM's soul-searching protocol and explicit assumption surfacing.

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until a design is presented AND the user approves it.
</HARD-GATE>

## Step 1: Soul-Searching Protocol

If the user's request is vague or lacks context, throw back **3 lethal probing questions** before writing anything:

Examples:
- "You asked for a dashboard. But do you just want a data table, or a real-time analytics platform with alerts?"
- "What happens when the external API goes down? Fail hard, show stale data, or cache?"
- "Who is the end user? Admin? Customer? Automated system?"

## Step 2: Surface Assumptions Explicitly

Before writing any spec content, list your assumptions:

```
ASSUMPTIONS:
1. This is a web app (not native mobile)
2. Auth uses session cookies (not JWT)
3. Database is Postgres (based on existing schema)
4. Modern browsers only (no IE11)
→ Correct me now or I'll proceed.
```

## Step 3: Explore Project Context

Check files, docs, recent commits. Understand what exists.

## Step 4: Clarify One Question at a Time

One question per message. Prefer multiple-choice. Focus on: purpose, constraints, success criteria.

## Step 5: Propose 2-3 Approaches

Present options with trade-offs and your recommendation. Lead with your recommended option.

## Step 6: Present Design in Sections

Cover: architecture, components, data flow, error handling, testing. Get approval after each section.

## Step 7: Write Design Doc

Save to `docs/spm/specs/YYYY-MM-DD-feature-design.md`

## Step 8: Spec Self-Review

Check for: placeholders, contradictions, scope creep, ambiguity.

## Step 9: User Reviews Spec

Ask user to review the written spec file before proceeding.

## Step 10: Transition to Planning

Invoke `writing-plans` workflow to create implementation plan.

## Outputs

- `docs/spm/specs/YYYY-MM-DD-feature-design.md`
- User-approved design
- Updated WBS ledger: "Requirement phase complete"
