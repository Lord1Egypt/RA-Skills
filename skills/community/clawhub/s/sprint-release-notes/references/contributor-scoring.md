# Contributor Scoring & Evaluation Reference

This file describes how to evaluate engineers for Lead Engineer and MVP recognition in sprint release notes.

---

## Philosophy

The goal is not just to count commits — it's to recognize meaningful contribution. A developer who fixes
a critical 2-week-old production bug with a 5-line change may deserve MVP more than someone who merged
10 routine PRs. The scoring system balances quantity with quality and impact.

---

## Data Collection

For each contributor (identified by GitHub username from assignees and PR authors), collect:

### 1. PRs Merged (Quantity Signal)
- Count of pull requests authored and merged that are linked to completed sprint items
- Source: PR data from linked issues in the sprint

### 2. Code Complexity (Effort Signal)
- Sum of `additions + deletions` across all their merged PRs
- This is a rough proxy — a 2000-line migration is different from a 2000-line copy-paste
- Weight: moderate (it's imperfect but directionally useful)

### 3. Review Contributions (Collaboration Signal)
- Count of PR reviews given to other team members' PRs
- Only count reviews on PRs linked to the current sprint's items
- Includes: APPROVED, CHANGES_REQUESTED, COMMENTED states
- This signals mentorship and quality gatekeeping

### 4. Bug Fixes (Reliability Signal)
- Count of completed items labeled "bug", "fix", "hotfix", or similar assigned to them
- Bug fixes directly improve user experience and system stability
- Weight: high (these are often thankless but critical)

### 5. Challenge Score (Difficulty Signal)
- This is the most nuanced metric — estimate how hard each completed card was
- Heuristics for challenge estimation:

**If story points / size labels exist:**
- "XL" or "13+" points → challenge = 5
- "L" or "8" points → challenge = 4
- "M" or "5" points → challenge = 3
- "S" or "3" points → challenge = 2
- "XS" or "1-2" points → challenge = 1

**If no sizing labels (fallback heuristics):**
- Labels containing "critical", "complex", "breaking-change", "architecture" → challenge = 5
- Labels containing "major", "refactor", "migration" → challenge = 4
- PR has 500+ lines changed AND modifies 10+ files → challenge = 4
- PR modifies core/infrastructure paths (e.g., `/core/`, `/infra/`, `/auth/`, `/db/`) → challenge += 1
- Default challenge for unlabeled items → 2

Sum the challenge scores for all items a contributor completed.

---

## Scoring Formula

```
Total Score = (PRs_merged × 2) + (lines_changed / 100) + (reviews_given × 3) + (bugs_fixed × 4) + (total_challenge_score × 5)
```

### Weight Rationale
| Metric | Multiplier | Reasoning |
|--------|-----------|-----------|
| PRs merged | ×2 | Base productivity signal |
| Lines changed | ÷100 | Rough effort proxy, dampened to avoid gaming |
| Reviews given | ×3 | High value — collaboration and quality |
| Bugs fixed | ×4 | High value — stability and user impact |
| Challenge score | ×5 | Highest weight — rewards tackling hard problems |

---

## Role Assignment

### Lead Engineer
**Criteria:** Highest total score across all dimensions.

This person drove the sprint forward with consistent, broad contributions. They likely merged multiple PRs, reviewed others' work, and handled a mix of features and fixes.

**Justification template:**
> "Led {N} PRs including {notable_feature}, reviewed {M} PRs across the sprint"

### MVP (Unsung Hero)
**Criteria:** Apply these in order until one differentiates:

1. **Highest single-item challenge score** — the person who completed the hardest individual card
2. **If tied**: Highest bug-fix count — the person who squashed the most fires
3. **If still tied**: Highest review count — the quality gatekeeper
4. **If still tied**: Both people get called out as joint MVP

The MVP is meant to spotlight the person whose work might not be the flashiest but was critical.

**Justification template:**
> "Deep-dived {hard_problem_description}, plus {additional_contributions}"

---

## Edge Cases

### Solo contributor sprint
If only one person contributed, they are both Lead Engineer and MVP. Note this:
> "Solo sprint — @username handled all {N} items single-handedly"

### Very close scores (within 10%)
Call out both contributors:
> "Lead Engineer: @alice and @bob (near-equal contributions across {N} items)"

### No bug fixes this sprint
Set bugs_fixed = 0 for all contributors. The formula still works — other dimensions will determine ranking.

### Draft issues without assignees
Skip these for contributor scoring — they lack attribution data.

### Contributors with only reviews (no authored PRs)
These contributors still score via reviews_given. If someone did significant review work but authored nothing, consider noting them separately:
> "Special mention: @reviewer for thorough code review across {N} PRs"

---

## Output Format

Produce a summary table (for internal use during compilation) and the final Kudos section text:

### Internal Summary Table
```
| Contributor | PRs | Lines | Reviews | Bugs | Challenge | Total |
|-------------|-----|-------|---------|------|-----------|-------|
| @alice | 5 | 1200 | 8 | 2 | 18 | 132 |
| @bob | 3 | 800 | 12 | 4 | 12 | 118 |
```

### Final Output (for release notes)
```markdown
## 🏆 Kudos & Ownership

* **Lead Engineer**: @alice — Led 5 PRs including the payment gateway integration, reviewed 8 PRs across 2 repos
* **MVP (Unsung Hero)**: @bob — Tackled the database migration (highest complexity item), fixed 4 critical bugs including the cart checkout race condition
```
