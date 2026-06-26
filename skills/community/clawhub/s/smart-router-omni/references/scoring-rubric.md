# Scoring Rubric

Score each viable candidate from 0 to 5 on every dimension, then apply the weights below.

## Weighted dimensions

- Capability fit: 35%
  - Does the skill description explicitly cover the requested job?
- Output fit: 20%
  - Does the skill naturally produce the artifact the user wants?
- Constraint and prerequisite fit: 15%
  - Can it work with the available tools, auth, platform, safety limits, and time constraints?
- Domain and context fit: 15%
  - Does it match the domain, content type, or technical surface?
- Workflow-stage fit: 10%
  - Is it the right skill for this phase, or only one step in a larger chain?
- User or workspace preference fit: 5%
  - Has the user named a preferred platform, tool family, or prior skill?

## Confidence bands

- High:
  - top weighted score >= 4.0 / 5
  - lead over second place >= 0.7
- Medium:
  - top weighted score >= 3.4 / 5
  - lead over second place >= 0.3
- Low:
  - anything weaker than the above
  - or any missing constraint that could materially change the route

## Hard filters

Reject a candidate before scoring if any of these are true:

- the skill is unavailable
- the skill requires tooling or access that is clearly absent
- the skill produces the wrong output type
- the request falls outside the skill's claimed scope
- the route would violate safety or policy

## Tie-breakers

- Prefer the more specific skill when both are equally compatible.
- Prefer the simpler chain when both paths can finish the task.
- Prefer the candidate with clearer metadata in `description` and `agents/openai.yaml`.
- Prefer the skill that operates directly on the current workspace over one that needs extra setup.
