---
name: text2qa
description: >
  Extract structured Q&A pairs and Selection Preferences from any text source — especially the current chat session or uploaded documents. Use this skill whenever the user asks to "extract Q&A", "generate questions and answers", "pull out questions from the chat", "create a quiz from this conversation", "identify preferences", "find selection criteria", or wants to summarize a session into a reusable knowledge base. Also trigger when users say things like "turn this chat into Q&A", "what did we decide?", "document my preferences from this conversation", or "make flashcards from this". Works on chat sessions, documents, articles, transcripts, or any freeform text.
---

# text2qa Skill

Extract **Q&A pairs** and **Selection Preferences** from the current chat session or any provided text.

---

## Output Format

Produce two clearly separated sections:

### Section 1: Q&A Pairs

Identify every implicit or explicit question-answer exchange. Format as:

```
## Q&A Pairs

**Q1: <question>**
A: <answer>

**Q2: <question>**
A: <answer>
...
```

Rules:
- Extract both **explicit** questions (user directly asked something) and **implicit** questions (Claude provided info that answers an unstated question).
- Rephrase conversational exchanges into clean, standalone Q&A pairs.
- If an answer spans multiple turns, synthesize into one coherent answer.
- Skip small talk or meta-conversation (e.g., "thanks!", "sure!").

---

### Section 2: Selection Preferences

Identify any preferences, constraints, choices, or criteria the user expressed or implied. Format as:

```
## Selection Preferences

| # | Preference / Constraint | Source (direct/inferred) |
|---|------------------------|--------------------------|
| 1 | <preference>           | direct / inferred        |
| 2 | <preference>           | direct / inferred        |
...
```

Preference types to look for:
- **Format preferences** — "I want markdown", "keep it short", "use bullet points"
- **Content preferences** — "focus on X", "skip Y", "I prefer Z style"
- **Tool/approach preferences** — "don't use files", "use Python not JS"
- **Persona/tone preferences** — "be concise", "explain like I'm a beginner"
- **Domain/topic constraints** — "only for production use", "target audience is X"
- **Decisions made** — explicit choices the user made during the session

Mark each as `direct` (user stated it outright) or `inferred` (implied by behavior/choices).

---

## Workflow

1. **Scan** the full conversation (or provided text).
2. **Identify** all Q&A exchanges and stated/implied preferences.
3. **Output** Section 1 (Q&A Pairs) then Section 2 (Selection Preferences).
4. **Optionally** offer to export as a `.md` file if the user might want to save it.

---

## Tips

- For chat sessions: scan from the very first message.
- For documents: treat headings/paragraphs as implicit questions when appropriate.
- If the session is very long, cluster related Q&As under sub-headings by topic.
- If no preferences are found, say so clearly rather than inventing them.
- Always note the total count: "Found X Q&A pairs and Y preferences."
