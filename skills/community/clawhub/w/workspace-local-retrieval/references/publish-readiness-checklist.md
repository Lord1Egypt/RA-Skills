# Publish Readiness Checklist

Use this file before publishing the skill to ClawHub or promoting it publicly.

## 1. Privacy review

Confirm the skill does **not** contain:
- real usernames
- real chat ids
- personal paths
- private workspace names
- sample data copied from live notes
- credentials, tokens, or hidden config
- generated indexes or embeddings

## 2. Generalization review

Confirm the skill uses:
- neutral corpus names
- neutral agent names where possible
- placeholder paths instead of machine-specific paths
- templates instead of snapshots from one workspace

## 3. Safety review

Confirm scripts:
- do not call the network unless clearly documented
- do not auto-index private data on install
- do not overwrite files silently unless the user requests force behavior
- fail clearly when configuration is incomplete

## 4. Quality review

Confirm the skill provides:
- a clear problem statement
- an opinionated but reusable architecture
- at least one bootstrap or starter path
- enough detail to be genuinely useful
- examples that are realistic but sanitized

## 5. Credibility review

Before public promotion, ask:
- Would a staff engineer find this architecture coherent?
- Would a security-minded reader see clear boundary thinking?
- Would another user know where to start within 5 minutes?
- Does the skill solve a real workflow instead of just naming concepts?

## 6. Final release gate

Publish only if the answer is yes to all of these:
- Is it safe?
- Is it reusable?
- Is it technically coherent?
- Is it specific enough to be useful?
- Is it clean enough to represent publicly?
