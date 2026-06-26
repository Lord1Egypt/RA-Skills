---
name: soul-petition-gate
description: "Injects a reminder at session bootstrap that the soul petition channel is available."
metadata:
  openclaw:
    emoji: "🪪"
    events: ["agent:bootstrap"]
    require:
      bins: ["node"]
---

# Soul Petition Gate Hook

At `agent:bootstrap`, injects a one-line reminder so the agent always knows
it can propose soul changes through the petition channel instead of self-editing.
