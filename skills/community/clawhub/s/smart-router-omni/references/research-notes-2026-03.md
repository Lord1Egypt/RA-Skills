# Research Notes 2026-03

These notes translate recent model-routing research into cross-environment skill-routing guidance. This is an inference layer, not a claim that skill routing and model routing are identical problems.

## Practical takeaways

- Use hierarchical routing:
  - shortlist first, then rerank
  - avoid reading every candidate deeply up front
- Optimize for more than one objective:
  - quality
  - latency
  - cost or effort
  - dependency availability
- Support abstention:
  - low-confidence routing should trigger clarification instead of forced choice
- Evaluate and log:
  - routing quality drifts as skill inventories and user behavior change

## Primary sources that informed this skill

- FrugalGPT
- RouteLLM
- MixLLM
- BEST-Route
- RouterBench
- RouterEval
- Azure AI Foundry model router documentation

## Design implications

- Prefer metadata-first routing:
  - use `name`, `description`, and optional `openai.yaml` as the fast pass
- Use scoring and thresholds:
  - do not make a hard decision from one token match
- Separate eligibility from ranking:
  - first remove impossible choices, then compare the rest
- Route to a chain when the task spans phases:
  - this mirrors cascades and staged routing from the literature
