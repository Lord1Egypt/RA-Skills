# Council Benchmarking

How to score and evaluate the quality of a Council run output.

## Scoring Criteria (0-100)

**1. Topic Classification and Persona Selection (0-15)**
- Did the executor pick the correct domain (Engineering, Sales, etc.)?
- Are the chosen personas relevant to the specific problem?
- Did they utilize appropriate add-ons (e.g., Budget Hawk) when constraints were obvious?

**2. Productive Friction / Disagreement (0-30)**
- *Failure mode*: All personas agree completely and just echo the same sentiment in different words (Cosplay).
- *Success mode*: Personas actively challenge each other based on their core focus (e.g., Product Engineer wanting speed vs Reliability Engineer wanting stability).
- Did the debate uncover non-obvious tradeoffs?

**3. Synthesis Quality (0-35)**
- Is there a clear separation between Consensus and Dissent?
- Did the final recommendation synthesize the best parts of the conflicting views?
- Is the tradeoff explicit? (e.g., "We are trading off long-term maintainability for speed to market.")

**4. Actionability (0-20)**
- Does the output end with a concrete, assignable Next Action?
- Are open questions clearly defined for a human to answer?

## Benchmarking Script

Executors should automatically grade their own Council outputs using this rubric before presenting them to the user.

If the score is below **70/100** (usually due to lack of disagreement or poor synthesis), the executor should silently re-run or prompt the personas to find the flaws in the "too-perfect" consensus.
