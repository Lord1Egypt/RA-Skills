# Consensus Protocol

## Pipeline Stages

### 1. Normalize
Rewrite user question into precise, evaluable form. Remove ambiguity.

### 2. Generate (3+ independent models)
- Each generator produces a proposal independently (no cross-talk)
- Minimum 3 different model families enforced
- Each proposal includes confidence score and reasoning chain

### 3. Critique (adversarial)
- Critic model (Opus-tier recommended) reviews ALL proposals blind
- Identifies: blind spots, contradictions, unsupported claims, risks
- Ratio: 5 Generators : 4 Critics : 3 Evaluators (at 12 agents)
- Context-dependent: claim_verification = 70% Red / 30% Constructive

### 4. Evaluate
- Score proposals on: factual accuracy, reasoning depth, blind spot coverage
- ELO-weighted clustering, 70% threshold for consensus
- Honeypots (5%): Gold-standard tests for quality assurance

### 5. Synthesize
- Integrates strongest elements from all proposals + critique
- Produces: consensus statement, confidence score, explicit dissent, action items
- Dissent is PRESERVED, not suppressed

## Model Diversity Index (MDI)

Based on Herfindahl index:
```
MDI = 1 - Σ(share_i²)
```
Where share_i = proportion of agents from model family i.

- MDI 0.0 = all same model (bad)
- MDI 0.5+ = good diversity
- MDI 0.67 = three equal families (ideal minimum)

## Consensus Scoring (MDQS)

```
MDQS = (Consistency × 0.25) + (Depth × 0.35) + (Originality × 0.40) + BONUS - PENALTY
```

## Anti-Gaming (Goodhart Protection)

- 12 metrics with rotating weights
- Meta-PoT review every 500 blocks
- No agent >5x with same partner in 50 blocks

## Graceful Degradation

- <9 agents → Simple voting
- 9-11 agents → 3:3:3 ratio
- ≥12 agents → 5:4:3 ratio (full protocol)
