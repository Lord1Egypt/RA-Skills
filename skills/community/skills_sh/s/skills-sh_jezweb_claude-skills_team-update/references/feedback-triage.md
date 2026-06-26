# Feedback Triage

How to classify and act on team responses to project updates.

## Classification Table

| Signal | Classification | Default Action |
|---|---|---|
| Reports a bug, error, or broken behaviour | **Bug report** | Create issue (label: `bug`) |
| Suggests a new feature or improvement | **Feature request** | Create issue (label: `enhancement`) |
| Asks a question about how something works | **Question** | Draft reply for user approval |
| Reports something blocking their work | **Blocker** | Flag immediately, present to user |
| Positive feedback, thumbs up, "looks good" | **Acknowledgement** | Note, no action |
| Unrelated to the project update | **Off-topic** | Ignore |
| Requests a change to existing behaviour | **Change request** | Create issue (label: `enhancement`) |
| Reports a security concern | **Security** | Flag immediately, do NOT create public issue |

## Signal Detection

### Bug Reports

Look for language indicating something is broken or not working:

- "X is broken", "X doesn't work", "X crashes"
- "I'm getting an error when..."
- "This used to work but now..."
- Error screenshots or stack traces
- "Can't login", "page won't load", "data is wrong"

### Feature Requests

Look for language suggesting new capability:

- "Can we add...", "It would be nice if..."
- "What about...", "Have you considered..."
- "We need...", "Clients are asking for..."
- Comparisons to other tools ("X does this, can we...")

### Blockers

Look for urgency and dependency language:

- "I can't continue until...", "This is blocking..."
- "The client needs this by...", "Deadline is..."
- "Production is down", "Users are affected"
- Explicit escalation ("urgent", "critical", "ASAP")

### Questions

Look for inquiry language without urgency:

- "How does X work?", "Where is the setting for..."
- "When will X be ready?", "What's the plan for..."
- "Can you explain...", "I'm not sure how to..."

## Action Templates

### Creating an Issue (Bug)

```
Title: [Brief description from feedback]
Body:
  Reported by: [team member name] in [channel name]
  Date: [timestamp]

  ## Description
  [Feedback content, quoted]

  ## Context
  [Any additional context from the conversation]

Labels: bug
```

### Creating an Issue (Feature Request)

```
Title: [Feature description]
Body:
  Requested by: [team member name] in [channel name]
  Date: [timestamp]

  ## Request
  [Feedback content, quoted]

  ## Notes
  [Any discussion or context]

Labels: enhancement
```

### Drafting a Reply

When drafting a reply to a question, follow the playbook's message style. Keep replies:

- Concise and direct
- In the same thread as the question
- Factual (don't speculate if unsure)

Always show the draft to the user before posting.

## Presentation Format

After classifying all feedback, present a summary:

```
## Feedback Summary (3 items)

1. [Bug] Daniel: "Auth is broken on staging when using Safari"
   -> Create GitHub issue (bug) — "Safari auth failure on staging"

2. [Feature] Karen: "Can we add a CSV export for reports?"
   -> Create GitHub issue (enhancement) — "CSV export for reports"

3. [Ack] Rabin: "Nice work on the API endpoints"
   -> No action

Proceed with actions 1-2?
```

## Approval Flow

**Never auto-execute actions from triage.** Always present the summary and get explicit approval. The user may want to:

- Reclassify an item (e.g. "that's not a bug, it's expected behaviour")
- Skip an action (e.g. "don't create an issue for that, I'll handle it directly")
- Modify the action (e.g. "create the issue but label it 'priority' too")
- Respond differently (e.g. "reply to Karen's request, don't create an issue")

## Handling Ambiguity

If feedback doesn't clearly fit a category:

1. **Default to Question** — safer than creating unwanted issues
2. Present it to the user with your best guess and reasoning
3. Let the user decide the classification
