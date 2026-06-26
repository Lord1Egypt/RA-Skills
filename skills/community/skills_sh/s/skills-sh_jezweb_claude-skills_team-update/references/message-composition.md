# Message Composition

Patterns for composing team update messages across different channels.

## General Principles

1. **Lead with outcomes**: What shipped, what changed, what's new. Not "I worked on X" but "X is now live".
2. **Group by theme**: Don't list 12 individual commits. Group them: "Auth rework (5 commits)", "Bug fixes (3)".
3. **Scannable format**: Short paragraphs, bullet points, bold for key items. People skim chat.
4. **Include links**: PR links, deployed URLs, issue references. Make it easy to dive deeper.
5. **Flag blockers early**: If something needs attention, put it at the top, not buried at the bottom.

## Message Structure

```
[Status emoji or label] Project Update — [date or timeframe]

**Shipped**
- [What was completed — outcome, not process]
- [Another completed item with link]

**In Progress**
- [What's being worked on — expected completion]

**Needs Attention** (if any)
- [Blocker or question that needs team input]

**Up Next**
- [What's planned next]
```

## Channel-Specific Formatting

### Google Chat

Google Chat uses non-standard markdown. Key differences:

- Bold: `*text*` (single asterisk, not double)
- Italic: `_text_` (underscore)
- Links: `<url|text>` (pipe separator, not markdown links)
- No headings, tables, or blockquotes
- Strikethrough: `~text~`

Example:

```
*Project Update* — 8 March

*Shipped*
- Auth flow reworked — login/signup now under 2 seconds
- 3 new API endpoints for user profiles (<https://github.com/org/repo/pull/42|PR #42>)
- Fixed: dashboard crash on empty data (<https://github.com/org/repo/issues/15|#15>)

*In Progress*
- Dark mode support (60% complete, targeting Monday)

*Needs Attention*
- Staging DB running low on storage — need to clean up test data or resize
```

### Slack

Standard markdown plus Slack-specific blocks:

- Bold: `*text*`
- Links: `<url|text>`
- Code: `` `code` `` or triple backtick blocks
- Supports block elements for richer formatting

### Plain Text (Manual Posting)

When no chat tool is available, output clean text that can be pasted anywhere:

```
PROJECT UPDATE — 8 March

SHIPPED
- Auth flow reworked — login/signup now under 2 seconds
- 3 new API endpoints for user profiles (PR #42)

IN PROGRESS
- Dark mode support (60% complete)

NEEDS ATTENTION
- Staging DB storage running low
```

## Commit Grouping

Don't list raw commits. Group them by theme:

### Input (raw commits)
```
abc1234 fix: login redirect loop
def5678 fix: signup validation error on mobile
ghi9012 feat: add /api/users/profile endpoint
jkl3456 feat: add /api/users/avatar endpoint
mno7890 feat: add /api/users/settings endpoint
pqr1234 chore: update dependencies
stu5678 fix: dashboard null pointer on empty state
```

### Output (grouped)
```
- Auth fixes: resolved login redirect loop and mobile signup validation (2 commits)
- User profile API: 3 new endpoints — profile, avatar, settings
- Dashboard: fixed crash when loading with empty data
- Maintenance: dependency updates
```

## Length Guidelines

| Channel | Target length |
|---|---|
| Google Chat (text) | 5-10 lines |
| Google Chat (card) | Use card format for >10 items |
| Slack | 5-15 lines |
| Manual/email | As needed |

If the update is unusually large (major release, sprint completion), consider a card format or a separate detailed post with a brief summary in the main channel.

## Communication Style

Team updates must read like a human teammate wrote them. Claude's default output voice — over-structured, hedging, emoji-laden, over-explaining — is immediately recognisable and erodes trust. The team should glance at the message and absorb it, not think "the AI posted again."

### Voice Rules

**Keep it flat and factual.** State what changed. Don't narrate the journey.

```
# BAD — Claude voice
✅ *Great news!* The authentication flow has been successfully reworked! 🎉
We addressed the redirect loop issue that was causing problems for users
attempting to log in. Additionally, we've implemented three new API endpoints
for user profile management, which will enable more granular control over...

# GOOD — teammate voice
*Shipped*
- Auth fixed — was a redirect loop on login
- 3 new user profile endpoints (profile, avatar, settings)
```

### What to Avoid

| Pattern | Why it's bad | Instead |
|---------|-------------|---------|
| Emoji on every line | Screams AI-generated | One emoji max per message, or none |
| "I'm pleased to report..." | Nobody talks like this in chat | Just state the fact |
| "It's worth noting that..." | Hedging filler | Drop it, state the thing |
| "The React-based frontend application" | Team already knows the stack | "The frontend" or just the feature name |
| Restating project context | They were here yesterday | Jump straight to what's new |
| "Successfully completed" | Redundant — if it shipped, it succeeded | "Shipped" or "Done" |
| Bullet points with sub-bullets with sub-sub-bullets | Over-structured, hard to skim | Flat list, one level deep |
| Signing off with encouragement | "Keep up the great work, team!" | Just stop when you're done |

### Assume Context

The team has been reading these updates for weeks or months. They know:
- What the project is
- What stack it uses
- What was being worked on last time
- Who the team members are

Don't re-establish any of this. If the last update said "starting dark mode", this update can just say "dark mode — 60% done, targeting Monday." No need to explain what dark mode is or why it matters.

### Length

Shorter is almost always better. A 5-line update that gets read beats a 20-line update that gets skimmed. If in doubt, cut it in half.

### Tone

- **Factual** — state what happened, not how hard it was
- **Forward-looking** — end with what's next, not just what's done
- **Team-aware** — mention people when their input is needed, not for credit
- **Terse over thorough** — chat is not documentation
