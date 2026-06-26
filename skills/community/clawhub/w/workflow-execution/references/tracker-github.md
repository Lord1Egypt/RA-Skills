# Tracker Reference: GitHub Issues

How to use the workflow-execution skill with GitHub Issues as your project management system.

## Create an issue

```bash
gh issue create --title "Your task title" --body "Brief description" --label "priority:high"
```

Or via API:
```
POST /repos/{owner}/{repo}/issues
{ "title": "Your task title", "body": "Brief description", "labels": ["priority:high"] }
```

## Attach a plan document

GitHub Issues don't have a first-class documents API. Use the **issue body** for the plan:

```bash
gh issue create --title "Task title" --body-file plan.md
```

For additional context documents, use **issue comments** with clear headers:

```bash
gh issue comment {number} --body "## Design Document\n\n..."
gh issue comment {number} --body "## Context Document\n\n..."
```

### Alternative: linked files in the repo

For complex plans, commit a markdown file to the repo and link it from the issue:

```bash
# Commit the plan
echo "# Plan\n\n..." > docs/plans/SUP-490-skill-rewrite.md
git add docs/plans/SUP-490-skill-rewrite.md && git commit -m "Add plan for #42"

# Reference from issue
gh issue comment 42 --body "Plan: [docs/plans/SUP-490-skill-rewrite.md](link)"
```

## Read documents (executing agent)

```bash
gh issue view {number}            # Read issue body (plan)
gh issue view {number} --comments # Read all comments (design, context docs)
```

## Update progress

```bash
gh issue comment {number} --body "Completed step 2. Moving to step 3."
```

## Close the issue

```bash
gh issue close {number} --comment "All done criteria met. Evidence: [details]"
```

## Tips

- Use labels for priority and status tracking.
- Use milestones for grouping related issues.
- Branch naming: include issue number (e.g., `42-skill-rewrite`).
- PRs can auto-close issues with "Closes #42" in the description.
