---
name: qa-gate
description: Final quality validation gate for any artifact before human review. Run this skill on documents, skills, PRDs, blog posts, or code artifacts to validate factual accuracy, tone consistency, completeness, structural integrity, operational soundness, and sensitive data handling. Use when you need to "QA gate this", "validate before publish", run a "final check", perform "quality validation", proofread this, fact-check this, or otherwise validate, QA, or quality-gate an artifact before review, release, or publication.
---

# QA Gate

Final release gate for any artifact before human review. Every document, skill, blog post, PRD, or code output should pass this gate before the principal sees it.

This is **not** a code review skill. It is a read-only release gate that determines whether an artifact is ready to move forward. QA Gate inspects artifacts but does not modify them.

## When to Use

- After any ralphy loop completes a PRD
- Before presenting any deliverable to the principal
- When self-reviewing documents, code, skills, or blog posts
- As the final step before publishing to ClawHub or Gumroad
- When asked to "QA gate this," "validate before publish," "final check," or run a "quality gate"

## Optional Mode

- `--dual`: Use cross-model QA validation when the artifact is high-stakes, ambiguous, or worth the extra cost/latency for a second independent quality pass.

## Process

### Step 1: Read the artifact completely
Read the entire file. Do not skim. Understand the structure, voice, and intent.

### Step 2: Validate against 6 dimensions

**1. Factual Accuracy (Sequential Claim Verification)**
Extract every verifiable claim from the artifact into a mental checklist. Then verify each independently — do not batch-assess. For each claim:
- Is it verifiable from a known source or self-evident from context?
- If it references a citation (paper title, arXiv ID, finding), does the citation match?
- If it describes a technical procedure, is the procedure feasible as described?
- If it references a tool, API, or version, is the reference accurate and current?

Score: count of verified claims / total claims. If verification rate < 90%, flag for revision.

**2. Tone & Voice Consistency**
- Does the document maintain its intended voice throughout?
- No tonal drift between sections?
- No marketing fluff, tutorial-speak, or filler?
- Appropriate for the target audience (agent, human, or both)?

**3. Completeness**
- No placeholders (TODO, TBD, FIXME, PLACEHOLDER, [FILL IN])?
- All sections referenced in TOC/structure are present?
- All promised content is delivered?
- No orphaned references or dead links?

**4. Structural Integrity**
- Heading hierarchy is clean (no skipped levels)?
- Code blocks are properly fenced and syntactically valid?
- Section anchors work?
- Back-links resolve to valid targets?
- Markdown renders correctly?

**5. Operational Soundness** (for technical documents)
- Procedures are implementable as described?
- Configuration formats match the actual system?
- Commands and scripts are executable?
- Edge cases are addressed?

**6. Sensitive Data Check**
- No personal information (real names, schedules, addresses)?
- No API keys, tokens, or secrets?
- No internal-only references that shouldn't be public?
- Examples use fictional/generic data?

### Step 3: Produce gate verdict

Output must include a clear gate result:

```text
PASS — ready for human review
```
or
```text
PASS WITH FIXES
- MINOR [location]: issue description
```
or
```text
FAIL
- CRITICAL [location]: issue description
- MAJOR [location]: issue description
- MINOR [location]: issue description
```

### Step 4: If FAIL, fix and re-validate
Fix all CRITICAL and MAJOR issues. Re-run the gate. Only present to principal after PASS or PASS WITH FIXES.

## Integration with PRD Workflows

Add to any PRD as a verification step:

```markdown
### D) QA Gate
- [ ] Run QA Gate on all major artifacts produced in this PRD
- [ ] All artifacts must PASS before marking PRD complete
- [ ] Fix any CRITICAL or MAJOR issues identified
```

## Output Format

Write validation report to: `qa-gate/YYYY-MM-DD-<artifact-slug>.md` (relative to your workspace or evidence directory)

Use this structure:

```markdown
# QA Gate Report: <artifact name>

## Gate Result
PASS | PASS WITH FIXES | FAIL

## Artifact Type
Document | Skill | PRD | Blog Post | Code Artifact | Other

## Findings
- SEVERITY [location]: issue description

## Summary
Brief explanation of why the artifact passed, passed with fixes, or failed.
```

## Quality Standards

- CRITICAL: Blocks release. Factual errors, security issues, broken functionality.
- MAJOR: Should fix before release. Missing sections, tone drift, incomplete content.
- MINOR: Nice to fix. Typos, formatting inconsistencies, style preferences.

A PASS with only MINOR issues is acceptable. CRITICAL or MAJOR = must fix first.
