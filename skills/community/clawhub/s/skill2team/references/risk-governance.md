# Risk Governance

| Level | Meaning | Action |
|---|---|---|
| P0 | blocks delivery if wrong or missing | verify, resolve, or stop |
| P1 | strongly affects decision or quality | resolve or downgrade conclusion |
| P2 | affects completeness or clarity | fix if practical, caveat allowed |
| P3 | style or convenience | usually non-blocking |

High-risk work should separate collector, verifier, analyst, composer/executor, and independent reviewer.

Never export real secrets. Use placeholders for API keys, tokens, passwords, and private endpoints.
