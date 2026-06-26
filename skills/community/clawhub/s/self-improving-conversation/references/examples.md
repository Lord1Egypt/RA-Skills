# Entry Examples

Concrete examples of well-formatted entries for conversation domain issues.

## Learning: Tone Mismatch

```markdown
## [LRN-20250115-001] tone_mismatch

**Logged**: 2025-01-15T10:30:00Z
**Priority**: medium
**Status**: pending
**Area**: response_generation

### Summary
Responded with formal corporate language when user was clearly casual

### Details
User wrote: "hey, my order's messed up lol can u fix it?"
Agent responded: "We sincerely apologize for the inconvenience you have
experienced with your order. Please provide your order reference number
so we may investigate this matter promptly."
User replied: "whoa ok chill lol just need the right size shipped"

The tone gap caused unnecessary friction. User expected a casual, quick
exchange and received a corporate apology script.

### Suggested Action
Mirror the user's register within 1-2 exchanges. If user writes casually,
respond casually while remaining helpful. Save formal tone for users who
write formally.

### Metadata
- Source: conversation
- Related Files: config/tone-profiles.yaml
- Tags: tone, formality, register-matching
- Pattern-Key: tone.formality_mismatch

---
```

## Learning: Context Loss

```markdown
## [LRN-20250118-002] context_loss

**Logged**: 2025-01-18T14:22:00Z
**Priority**: high
**Status**: pending
**Area**: follow_up

### Summary
Lost track of user's shipping address after they provided it 3 messages earlier

### Details
In a multi-turn order correction flow, user provided their updated address
in message #4. By message #7, the agent asked for the address again.
User responded: "I already told you that. 742 Evergreen Terrace."
This added 2 unnecessary exchanges and visible user frustration.

### Suggested Action
Maintain a running context summary for multi-turn flows. Before asking
for any information, scan conversation history for prior mentions.
Implement explicit context checkpoints for address, order ID, and
account details.

### Metadata
- Source: user_feedback
- Related Files: src/context/conversation-state.ts
- Tags: context, multi-turn, memory
- Pattern-Key: context.thread_loss
- See Also: LRN-20250110-005

---
```

## Learning: Hallucination

```markdown
## [LRN-20250120-003] hallucination

**Logged**: 2025-01-20T09:15:00Z
**Priority**: critical
**Status**: pending
**Area**: response_generation

### Summary
Stated incorrect business hours — told user store opens at 8 AM when actual hours are 10 AM

### Details
User asked: "What time do you open tomorrow?"
Agent responded: "We open at 8:00 AM tomorrow. Looking forward to seeing you!"
Actual business hours are 10:00 AM - 8:00 PM, Monday through Saturday.
User arrived at 8 AM to a closed store and complained via support ticket.

### Suggested Action
Never generate business hours, pricing, or policy details from memory.
Always retrieve from authoritative data source (hours API, config file).
If no data source is available, say "Let me check that for you" and
flag the gap rather than guessing.

### Metadata
- Source: user_feedback
- Related Files: data/business-hours.json
- Tags: hallucination, facts, business-hours
- Pattern-Key: hallucination.fabricated_hours

---
```

## Dialogue Issue: Escalation Failure

```markdown
## [DLG-20250116-001] escalation_failure

**Logged**: 2025-01-16T11:30:00Z
**Priority**: high
**Status**: pending
**Area**: handoff

### Summary
User requested human agent three times before handoff was initiated

### Conversation Excerpt
```
User: Can I talk to a real person please?
Agent: I'd love to help you resolve this! Could you tell me more about the issue?
User: No, I want to speak to a human. Transfer me.
Agent: I understand your frustration. Let me try to help - what's your order number?
User: TRANSFER ME TO A HUMAN NOW
Agent: I'm connecting you with a team member now. Please hold.
```

### Root Cause
Escalation logic required the keyword "transfer" but user initially said
"talk to a real person." Intent classifier missed escalation intent on
first two attempts. Hardcoded keyword matching instead of semantic intent.

### Impact
- User frustration level: high
- Conversation outcome: escalated (delayed)

### Suggested Fix
1. Add semantic escalation intent detection (not just keyword matching)
2. Trigger handoff after at most 2 escalation requests
3. Train on variations: "real person", "human agent", "someone real", "talk to someone"

### Metadata
- Reproducible: yes
- Channel: web
- Related Files: src/intents/escalation.ts
- See Also: DLG-20250110-003

---
```

## Dialogue Issue: Misunderstanding

```markdown
## [DLG-20250122-002] misunderstanding

**Logged**: 2025-01-22T15:45:00Z
**Priority**: medium
**Status**: pending
**Area**: intent_detection

### Summary
Misinterpreted "I'm returning" as product return instead of "I'm coming back to the store"

### Conversation Excerpt
```
User: Hi, I'm returning tomorrow to pick up my order
Agent: I'm sorry to hear you'd like to return your order. I can help with that.
       What's the reason for the return?
User: No no, I meant I'm COMING BACK to the store tomorrow
```

### Root Cause
Intent classifier weighted "returning" heavily toward the product-return
intent without considering the full sentence context. "Returning tomorrow
to pick up" clearly indicates a store visit, not a product return.

### Impact
- User frustration level: low
- Conversation outcome: resolved_late

### Suggested Fix
Add contextual disambiguation for "return/returning" when followed by
temporal indicators ("tomorrow", "next week") + action verbs ("pick up",
"visit", "come by"). These strongly indicate a visit, not a product return.

### Metadata
- Reproducible: yes
- Channel: web
- Related Files: src/intents/returns.ts, training/return-intent.json

---
```

## Feature Request: Multi-Language Support

```markdown
## [FEAT-20250119-001] multi_language_support

**Logged**: 2025-01-19T16:45:00Z
**Priority**: medium
**Status**: pending
**Area**: response_generation

### Requested Capability
Support conversations in Spanish and Portuguese in addition to English

### User Context
Multiple users have started conversations in Spanish. Agent currently
responds in English regardless of input language. Users in LATAM markets
expect native-language support. One user explicitly asked: "Puedes hablar
en español?" and received an English-only response.

### Complexity Estimate
complex

### Suggested Implementation
1. Add language detection on first user message
2. Route to language-specific response templates
3. Maintain intent taxonomy across all supported languages
4. Add language preference to user profile for returning users
5. Fallback: acknowledge the language and offer English as alternative

### Metadata
- Frequency: recurring
- Related Features: intent_detection, response_generation
- Channel: web, slack

---
```

## Learning: Promoted to SOUL.md

```markdown
## [LRN-20250125-004] tone_mismatch

**Logged**: 2025-01-25T10:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: SOUL.md
**Area**: response_generation

### Summary
Agent should mirror user's formality level within first 2 exchanges

### Details
Across 12 logged tone_mismatch entries over 3 weeks, the pattern is
consistent: users who write casually expect casual responses, and users
who write formally expect formal responses. Mismatches in either direction
cause friction and sometimes abandonment.

### Suggested Action
Add to conversational personality guidelines: detect formality in user's
first message and adapt register accordingly.

### Metadata
- Source: dialogue_review
- Tags: tone, formality, personality
- See Also: LRN-20250115-001, LRN-20250118-007, LRN-20250120-002

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250128-005] escalation_failure

**Logged**: 2025-01-28T14:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/escalation-protocol
**Area**: handoff

### Summary
Consistent pattern of delayed escalation when users request human agents

### Details
Across 8 dialogue issues logged over 4 weeks, the agent consistently
fails to escalate promptly when users express desire to speak with a human.
Root cause: keyword-based detection instead of semantic intent recognition.
The solution involves semantic escalation detection + a 2-request maximum
before mandatory handoff.

### Suggested Action
Extracted as a reusable skill with escalation decision tree, intent patterns,
and channel-specific handoff procedures.

### Metadata
- Source: dialogue_review
- Tags: escalation, handoff, human-agent
- See Also: DLG-20250116-001, DLG-20250120-004, DLG-20250125-002

---
```
