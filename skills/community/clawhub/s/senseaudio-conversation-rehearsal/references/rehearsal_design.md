## Product shape

This skill is for exposure-safe rehearsal, not just speech synthesis.

Target users:

- 害怕强势上级的人
- 汇报时容易卡壳的人
- 需要练晋升答辩、绩效面谈、预算申请的人

Core product loop:

1. User defines scenario, counterpart role, topic, and goal.
2. System builds a counterpart persona and pressure style.
3. Counterpart speaks back using:
   - proxy voice by default
   - authorized clone only with clear permission
4. User answers by voice.
5. ASR transcribes the answer.
6. The agent evaluates:
   - clarity
   - structure
   - ask quality
   - evidence quality
   - tone stability
7. Session ends with a debrief and better rewrites.

## Why this has commercial potential

- It is easier to sell than generic “AI roleplay” because the use case is clear.
- It fits HR, manager training, internal coaching, and executive communication prep.
- It uses audio to create emotional realism, which text-only mock interviews do not provide.

## Safety policy

Voice cloning risk is the biggest product risk.

Recommended policy:

- Default: `proxy_voice`
- Only allow `authorized_clone` when:
  - the sample owner has explicitly consented
  - the use is bounded to internal rehearsal
  - the session is not used to impersonate or publish

## Best MVP path

Phase 1:

- scenario input
- counterpart persona config
- proxy voice only
- user spoken reply ASR
- transcript scoring and debrief

Phase 2:

- authorized clone mode
- replay packs
- harder follow-up branches

Phase 3:

- multi-round live loop
- memory of the user's recurring weak points
- manager or coach dashboard
