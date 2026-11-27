# Answer format for the user

```
Vouch: <task>

1. VERIFIED       <claim>
   Telegraph: <observed value> (<miner>, <as_of or date>)
   Cost $0.01, receipt <hash>

2. CONTRADICTED   <claim>
   Telegraph: <observed value> (<miner>)
   Cost $0.01, receipt <hash>

3. CANNOT VERIFY  <claim>
   Why: <no matching intent | future date | answer about a different entity | conflicting sources | miner error | budget cap | two miners disagree>
   Cost $<n>, receipts <hashes or "none">

Spend $0.03 of $0.25 task cap (per-claim cap $0.05).
Decision: <proceed on claim 1 only | do not proceed: claim 2 contradicted | need the user's call>
```

Rules: one block per claim; never merge a cannot verify into a pass; give the observed value on every contradiction; list every paid ask including recovery asks; say plainly when an answer came from an unproven miner.
