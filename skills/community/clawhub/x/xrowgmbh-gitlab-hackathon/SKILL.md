---
name: gitlab-hackathon
description: Plan and execute fair GitLab hackathon participation, including Quarterly and Transcend Hackathons, by analyzing rules, selecting qualifying issues/MRs, tracking scoring levers, and keeping an exploit watchlist.
metadata: { "openclaw": { "requires": { "bins": ["glab", "jq", "curl"] }, "primaryEnv": "GITLAB_TOKEN" } }

---

# GitLab Hackathon Skill

Use this skill to compete fairly in GitLab hackathons with a repeatable, evidence-based plan.
Prioritize real contributions that reviewers can merge quickly. Do not spam comments, pad commits,
mislabel issues, or close issues without a valid reason.

For GitLab operations, read and follow the `gitlab-agent` skill.

## Quick Start

1. Verify the current rules, dates, tracks, and prize requirements:
   - Quarterly Hackathon: `https://contributors.gitlab.com/hackathon`
   - Current hackathon API: `https://contributors.gitlab.com/api/v1/hackathons/current`
   - Transcend Hackathon: `https://contributors.gitlab.com/transcend-hackathon`
   - Contribution points: `https://contributors.gitlab.com/docs/user-guide#contribution-points`
2. Confirm eligibility before optimizing:
   - Quarterly Hackathon scoring requires at least one qualifying merge request to be merged.
   - Quarterly Hackathon MRs must be opened during the 7-day hackathon window and merged before the merge deadline.
   - Transcend Hackathon cash prizes require registration and a DevPost submission; verify the current page before starting.
3. Pick work that can merge:
   - Prefer quick-win issues, small bugs, documentation fixes, tests, and self-contained components.
   - Prefer issues with clear reproduction, clear acceptance criteria, and recent maintainer activity.
   - Avoid huge refactors, ambiguous product decisions, flaky areas, and changes that need protected-branch access.
4. Create a small qualifying MR first, then scale:
   - Link every MR to an issue when possible.
   - Keep each MR reviewable, tested, and easy to merge.
   - Ask for review through the project workflow only after CI passes and discussions are resolved.

## Fair Winning Plan

### 1. Analyze

Build a one-page campaign brief before coding:

- Hackathon name, UTC start/end, merge deadline, prize requirements, and qualifying projects.
- Tracks and labels that matter, including `Hackathon`, `quick-win`, or Transcend-specific labels.
- Current leaderboard leaders and their scoring mix.
- Personal constraints: available time, project permissions, and trusted language/tooling areas.

Useful commands:

```bash
curl -sS https://contributors.gitlab.com/api/v1/hackathons/current | jq .
glab api '/projects/:fullpath/issues?labels=quick-win&state=opened&per_page=50'
glab api '/merge_requests?state=opened&scope=created_by_me&per_page=100'
```

### 2. Qualify

Secure at least one merged MR early. This unlocks scoring for the Quarterly Hackathon and reduces
the risk of finishing with zero points.

- Choose a low-risk issue with a maintainer-friendly patch.
- Keep the diff small.
- Include a clear MR description with plan, acceptance criteria, and validation.
- Run local checks and CI lint before pushing.
- Respond to reviews quickly and resolve every thread.

### 3. Compound

After qualification is likely, add contributions that are legitimate and reviewable:

- Open and merge additional small MRs during the window.
- Link MRs to issues for the extra merged-with-issue credit.
- Add useful comments only when they move work forward.
- Label issues only when the label is correct.
- Close issues only when they are duplicates, invalid, completed, or otherwise clearly closable.
- Submit real events, content, translations, or AI catalog items only when they meet the published rules.

## Scoring Levers

Verify these values against the user guide before each event:

- MR created: 20 points.
- Commit merged: 20 points.
- MR merged: 60 points, plus 30 more when linked to an issue.
- Issue created: 5 points.
- Issue labeled: 1 point.
- Issue closed: 5 points.
- Issue/MR comment: 1 point.
- Discord message: 1 point; Discord reply: 2 points.
- Forum post: 1 point; Forum reply: 2 points.
- Event engagement: 500 points.
- Content publication: 200 points.
- Translation: 1 point.
- AI catalog item version: 10 points.
- Ad-hoc bonus: variable.

## Issue and MR Selection

Prefer work with all of these:

- Clear owner, label, or maintainer signal.
- Small blast radius.
- Existing tests or an obvious validation path.
- No dependency on secrets, production credentials, or protected branches.
- A path to merge within the hackathon merge window.

Avoid work with any of these unless there is a strong reason:

- Unclear product direction.
- Large migrations.
- Inactive maintainers.
- Required access you do not have.
- CI known to be unstable without a workaround accepted by maintainers.

## Transcend Hackathon

Before working on Transcend entries, re-open the live page and confirm current requirements.
As of the 2026 event page, the Transcend Hackathon runs June 10-24, 2026 UTC, focuses on
AI-native contributions to GitLab's Knowledge Graph, and requires both registration and
DevPost submission for cash prizes.

When choosing a Transcend path:

- For the Contribute track, select labeled Knowledge Graph issues and submit focused MRs.
- For agent/workflow entries, build a working demo with clear setup, test evidence, and a short explanation of how it uses the Knowledge Graph.
- Keep prize submission artifacts reproducible: repository link, demo instructions, screenshots or video, and a concise impact statement.

## Exploit Watchlist

Track edge cases discovered during research or execution. Use them to avoid accidental rule abuse
and to ask maintainers for clarification when needed.

- Qualification gate: Quarterly Hackathon points can become zero if no MR merges before the deadline.
- Timing edge: MRs must be opened during the hackathon window; opening too early may not qualify.
- Merge deadline edge: MRs merged after the post-hackathon merge window may not count.
- Commit-count edge: commits score only when merged; do not pad or fragment commits just for points.
- Comment edge: comments score, but spam comments harm reviewers and may be disqualified.
- Label/close edge: labels and closures score, but incorrect labels or invalid closures are unfair and create cleanup work.
- Linked-issue edge: linked MRs get extra credit; only link to real, relevant issues.
- Event/content edge: high point values require genuine eligible activity, not placeholder submissions.
- Transcend prize edge: leaderboard activity alone may not satisfy DevPost or registration requirements.

When a new edge case appears, append it here with:

- Source link.
- Observed behavior.
- Fair-use decision.
- Whether maintainers need to be notified.

## End-of-Run Checklist

- At least one qualifying MR merged or on track to merge.
- Every MR links to a real issue when possible.
- CI passes on all active MRs.
- Review threads are resolved.
- Time spent and useful status comments are recorded in GitLab.
- Leaderboard position and scoring mix are checked.
- Any exploit-like behavior is documented in the watchlist and avoided unless maintainers explicitly approve it.
