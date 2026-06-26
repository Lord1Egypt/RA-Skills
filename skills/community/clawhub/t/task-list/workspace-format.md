# Workspace Format — Task List

Use simple Markdown files so the task list stays inspectable and easy to repair.
## `inbox.md`
```markdown
# Inbox

- [ ] Send investor update Friday
- [ ] Ask Marta if legal approved the contract
- [ ] Figure out dentist appointment
```

Keep raw wording until clarification is worth the effort.
## `tasks.md`
```markdown
# Tasks

| Task | Bucket | Project | Area | Due | Start | Priority | Next step |
|------|--------|---------|------|-----|-------|----------|-----------|
| Send investor update | Today | Q2 fundraising | Finance | 2026-03-13 | 2026-03-12 | high | Draft bullet outline |
| Book dentist appointment | Anytime | - | Personal admin | - | - | low | Call preferred clinic |
```

Use buckets from `views-and-sorting.md`: Inbox, Today, Upcoming, Anytime, Someday, Waiting, Done.
## `projects.md`
```markdown
# Projects

## Q2 fundraising
- Outcome: close the round with signed docs
- Status: active
- Deadline: 2026-05-30
- Next action: draft investor update
```

Each active project must have one visible next action.
## `areas.md`
```markdown
# Areas

- Finance
- Hiring
- Health
- Household
```

Areas are ongoing responsibilities, not projects with an end date.
## `recurring.md`
```markdown
# Recurring

| Task | Rule | Recreate from | Last done | Next show |
|------|------|---------------|-----------|-----------|
| Review cash runway | every Friday | completion | 2026-03-06 | 2026-03-13 |
```
## `waiting.md`
```markdown
# Waiting

| Task | Waiting for | Since | Chase on | Next visible step |
|------|-------------|-------|----------|-------------------|
| Legal review of contract | Marta | 2026-03-04 | 2026-03-10 | Follow up if silent |
```
## `log.md`
```markdown
# Recent Changes

- 2026-03-06: Moved "Book dentist appointment" from Inbox to Anytime
- 2026-03-06: Marked "Review cash runway" done and regenerated next occurrence
```

Log meaningful state changes, not every casual mention.
