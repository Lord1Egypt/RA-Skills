# Routing Table

This table documents how `roundtable-forge` dispatches a user request into a roundtable shape.

## Main route: full roundtable

**Trigger signal**: user wants a multi-character discussion or cross-disciplinary analysis.

**Shape**:

1. Capture question.
2. Select 3–5 initial characters.
3. Initialize Memory file.
4. Run 2–4 rounds.
5. Assess seat expansion.
6. Synthesize and return output.

## Variant route: character-only roster

**Trigger signal**: user asks "帮我选几个适合讨论这个问题的人" or similar.

**Shape**: return a proposed roster with rationale, but do not run the discussion.

## Variant route: continue from Memory

**Trigger signal**: user provides an existing Memory file and asks to continue or deepen the discussion.

**Shape**: load Memory, assess what is missing, add rounds or seats, update Memory.

## Fallbacks

- **No clear question**: ask the user to clarify the topic and desired depth before selecting characters.
- **Single-character request**: route to a perspective skill instead of a roundtable.
- **Factual lookup**: route to a general Q&A or search workflow instead of a roundtable.
- **Code generation**: route to a coding skill or coding agent; naming this skill does not turn a code task into a roundtable.
- **Single-subject deep research**: route to `deep-research-forge`; a follow-up roundtable may discuss the resulting evidence from multiple perspectives.
- **Sensitive domain with real living people**: add an extra disclaimer and prefer archetypes or historical figures unless the user explicitly insists.

Fallbacks are evaluated before the generic `roundtable`/`召集` summon signal. An
explicit skill name is routing context, not sufficient evidence that an
out-of-scope request should run a full roundtable.
