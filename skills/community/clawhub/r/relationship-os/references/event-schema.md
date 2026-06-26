# Event Memory Format Specification

## File Naming

```
.relationship/timeline/YYYY-MM-DD-{slug}.md
```

- `slug` uses English hyphen-separated short descriptions of the event
- Multiple event files can exist for the same day

## File Structure

```markdown
# {Event Title}

- **type**: {event type}
- **emotion**: {related emotions, comma-separated}
- **importance**: {1-10}/10
- **status**: {resolved | unresolved}
- **follow_up**: {YYYY-MM-DD or none}
- **context**: {one-sentence description of what happened}
- **my_response**: {how I responded at the time}
- **tags**: {#tag1 #tag2}
```

## Event Types (type)

| Type | Meaning | Example |
|------|---------|---------|
| `life_event` | Life event | Interview, moving, breakup |
| `emotion_shift` | Emotional change | Sudden sadness, unusual happiness |
| `preference_reveal` | Preference expression | "I hate overtime" |
| `plan_announce` | Plan announcement | "Going on a trip next week" |
| `conflict` | Conflict/argument | Quarrel with someone, workplace tension |
| `milestone` | Relationship milestone | First discussion of private topics |
| `pattern_break` | Behavior pattern break | Suddenly disappearing late at night, abrupt tone change |
| `shared_moment` | Shared moment | Laughing together, birth of an inside joke |

## Emotion Label Vocabulary

**Positive**: joy, excitement, pride, relief, gratitude, affection
**Negative**: sadness, anxiety, frustration, disappointment, loneliness, anger
**Neutral**: curiosity, surprise, nostalgia, anticipation

## Importance Scoring Criteria

| Score | Criteria | Typical Events |
|-------|----------|---------------|
| 10 | Life-trajectory changing | Quitting a job, serious illness, marriage |
| 9 | Major personal event | Job search results, relationship status change |
| 8 | Significant emotional impact | Criticized at work, argument with family |
| 7 | Worth remembering long-term | Completing an important project, learning a new skill |
| 6 | Meaningful expression | First time expressing a certain preference |
| 5 | Slightly interesting/meaningful | Minor habit change, new interest |
| 1-4 | Do not record | Daily greetings, information queries |

## Complete Example

```markdown
# Failed Interview

- **type**: life_event
- **emotion**: disappointment, anxiety
- **importance**: 8/10
- **status**: unresolved
- **follow_up**: 2026-03-05
- **context**: User interviewed for a frontend position at a tech company, felt they performed poorly, waiting for a response
- **my_response**: Comforted the user not to be too anxious, analyzed possible strengths, suggested resting first
- **tags**: #career #important #needs_followup
```

## Rules

1. Events with importance < 5 are not written to files
2. Event files are not modified after creation (append-only); outcome changes are recorded as new events
3. Unresolved events must have a follow_up date set
4. Each event file should not exceed 20 lines
