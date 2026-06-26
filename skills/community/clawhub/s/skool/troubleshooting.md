# Troubleshooting - Skool

## First Triage Questions

- Is the blocker strategic, operational, or a live write failure?
- Is the issue native Skool behavior, Zapier setup, webhook delivery, or user expectation drift?
- Is the problem happening in one group, one member segment, or every path?

## Common Failures

### Wrong Group or Wrong URL

- Re-check the exact group URL before debugging credentials or plugin state.
- Multi-group operators often fix the wrong environment first.

### Access Looks Wrong

- Verify member type, pricing path, course permissions, and level gate together.
- Admin visibility is not enough. Reconstruct the actual member journey.

### Automation Fires but Outcome Is Wrong

- Check mapped fields, approval logic, and the downstream action separately.
- One automation can be technically successful while still granting the wrong course or contacting the wrong segment.

### Engagement Drops After a Change

- Review the first-week experience, not just the feed.
- Many retention dips come from unclear onboarding or dead calendar cadence, not from weak content quality alone.

### Spam or Low-Quality Applicants Surge

- Tighten membership questions, approval rules, and welcome path expectations.
- Treat repeated spam as a funnel and offer problem, not just a moderation queue problem.

## Recovery Pattern

1. freeze new risky writes
2. identify who was affected
3. restore the intended access or message path
4. document the failure in `incidents.md`
5. narrow the workflow before re-enabling it
