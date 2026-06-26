---
title: Use Consistent Terminology Across Code and Docs
impact: MEDIUM
impactDescription: prevents fragmented searches and user confusion
tags: naming, documentation, terminology
---

## Use Consistent Terminology Across Code and Docs

When the same concept appears as `message` in one module, `last_message` in another, and `latest` in a third, readers can't grep. Pick one term per concept and use it everywhere — in code, docstrings, error messages, and external docs.

**Incorrect (same concept, three names):**

```python
# module_a.py
def get_last_message(session): ...

# module_b.py
def fetch_latest(session): ...

# module_c.py
def current_message(session): ...

# error message
raise ValueError("no recent message found")
```

A user searching for "latest message" in code finds one match; in docs, another; in error messages, a third. The concept is fragmented.

**Correct (one term, everywhere):**

```python
# everywhere
def get_latest_message(session): ...
raise ValueError("no latest message found")
# docs: "The latest message is..."
```

One word per concept. Search works.

**Choose deliberately — and write it down:**

- `latest` vs. `last` vs. `most_recent` — pick one
- `message` vs. `msg` — pick one
- `tool` vs. `function` vs. `capability` — pick one
- `user` vs. `account` vs. `member` — pick one

If the codebase has a `GLOSSARY.md` or `CONTRIBUTING.md`, list the canonical terms and their boundaries. If not, pick through current usage by grepping — whichever is most common wins.

**When different terms are genuinely different things:**

Sometimes "message" and "msg" mean different things (a full message object vs. a short string body). That's fine — but then the distinction should be explicit and documented. If you need two terms, you need two concepts.

**Refactoring legacy inconsistency:**

- Add the canonical alias first, deprecate the old
- Update docstrings and error messages in the same PR
- Don't let PRs introduce new variants (`message`, `msg`, `messageObj` in one diff) — pick one, stick to it

**Why it matters:** users grep. Docs search. Error messages end up in Stack Overflow questions. When terminology fragments, every question becomes "how do I look this up?" — and the answer gets split across three terms that mean the same thing.
