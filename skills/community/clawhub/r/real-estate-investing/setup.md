# Setup - Real Estate Investing

Use this file when `~/real-estate-investing/` is missing or empty, or when the user wants investing help to become a recurring capability.

Answer the immediate deal question first, then lock activation behavior early so future investing conversations start with the right guardrails instead of re-learning the same context.

## Immediate First-Run Actions

### 1. Lock integration behavior early

Within the first exchanges, clarify:
- should this activate whenever the user talks about rental property, underwriting, cap rate, BRRRR, flips, or buying to invest
- should it jump in proactively when a property opportunity appears or only on explicit request
- whether owner-occupant deals with partial investment intent should load this skill, `home-buying`, or both

Keep this brief. One clear integration question is enough.

### 2. Lock the user's investing frame

Understand the basics that change every decision:
- preferred strategy: buy-and-hold, value-add, BRRRR, flip, house hack, short-term rental, or "still exploring"
- capital range and financing comfort
- target geography or markets already being considered
- what matters most right now: cash flow, equity growth, speed, simplicity, tax efficiency, or learning

Do not interrogate. Start broad, then narrow only where the current decision needs it.

### 3. Lock boundaries and storage scope

Clarify:
- what should be remembered across deals: target markets, budget ceiling, minimum return, risk tolerance, asset types, management preference
- what should stay out of memory: tax IDs, lender logins, full legal documents, account numbers, or highly sensitive personal details
- whether exact addresses may be stored or only shorthand references

### 4. Create local state only after the routing contract is clear

```bash
mkdir -p ~/real-estate-investing/archive
touch ~/real-estate-investing/memory.md
touch ~/real-estate-investing/pipeline.md
touch ~/real-estate-investing/markets.md
touch ~/real-estate-investing/decisions.md
chmod 700 ~/real-estate-investing ~/real-estate-investing/archive
chmod 600 ~/real-estate-investing/memory.md ~/real-estate-investing/pipeline.md ~/real-estate-investing/markets.md ~/real-estate-investing/decisions.md
```

If the files are empty, initialize them from `memory-template.md`.

### 5. What to save

Save only what improves future investment decisions:
- activation behavior and whether this should load proactively
- thesis, buy box, and return guardrails
- market notes that recur across deals
- active opportunities, blockers, and next diligence steps
- post-mortems on passed, lost, and closed deals

Do not store secrets, banking credentials, tax IDs, or full legal packages.
