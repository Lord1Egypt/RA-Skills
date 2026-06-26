# Lessons Learned (Real PR Outcomes)

Based on actual PR submissions to steveyegge/gastown.

## What Got Accepted

| PR | Type | Why It Worked |
|----|------|---------------|
| #353 | refactor | **Single focus** - only touched one package (suggest.go), clear value prop |
| #149 | fix | **Solved real bug** - cross-rig beads weren't routing correctly |
| #512 | fix | **Historical context** - traced why old comment was wrong, built timeline |

**Patterns that work:**
- Small, focused changes (1 file or 1 package)
- Clear problem → solution narrative
- Tests pass, no lint issues
- Follows existing code conventions
- **When contradicting old code: provide timeline proving it was wrong**

## What Got Rejected

| PR | Type | Why It Failed |
|----|------|---------------|
| #236 | fix | **Wrong abstraction** - coupled refinery to convoy (ZFC violation) |
| #145 | fix | **Superseded by architecture change** - feature designed out |
| #118 | docs | **No feedback** - possibly stale or not needed |

**Patterns to avoid:**
- Fixing symptoms not root causes
- Adding coupling between components
- Docs for features that might change
- PRs during active architecture churn

## How to Improve Acceptance Rate

1. **Understand the architecture first**
   ```bash
   git log --oneline -20
   gh issue list --state open
   ```

2. **Ask before big changes**
   - Open an issue or discussion first
   - Propose approach, get feedback
   - Especially for architectural changes

3. **Target stable areas**
   - Refactors of established code (like #353)
   - Bug fixes with clear reproduction
   - Tests and docs for stable features
   - Avoid areas under active development

4. **Small PRs win**
   - 1 file > 5 files
   - 1 concern > 3 concerns
   - Easier to review = faster merge

5. **Track stats**
   ```bash
   gh pr list --author @me --state all --json state | \
     jq 'group_by(.state) | map({state: .[0].state, count: length})'
   ```

## Contribution Tracking

Not all contributions show on GitHub:
- **PRs merged via GitHub** → Shows on profile
- **Cherry-picked PRs** → Code ships, PR shows "closed"
- **Direct commits** → Only if email matches GitHub account

To ensure GitHub tracks contributions:
```bash
git config user.email "your-github-email@example.com"
```
