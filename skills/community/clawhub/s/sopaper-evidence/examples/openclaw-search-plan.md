# OpenClaw Search Plan Example

## Objective

Build a reviewer-safe evidence pack for an OpenClaw paper without assuming unsupported performance claims.

## Search scope

- manipulation systems
- long-horizon embodied task papers
- planner-policy hybrid methods
- real-world versus simulation evaluations
- benchmarks and datasets relevant to manipulation and sequential task completion

## Search passes

### Pass 1: Problem framing

Target outputs:

- canonical task names
- benchmark names
- standard metrics
- high-level baseline families

Questions:

- How do recent papers define the target task?
- What counts as success for this task family?
- Which datasets or benchmarks appear repeatedly?

### Pass 2: Direct baselines

Target outputs:

- methods that address closely related tasks
- official code or trusted repos
- evaluation settings that could be compared fairly

Questions:

- Which methods would a reviewer expect to see in the comparison table?
- Which of those methods are actually comparable under the same task and metric?

### Pass 3: Adjacent work

Target outputs:

- nearby methods that are relevant in related work but not fair baselines
- task differences that must be stated clearly

Questions:

- Which methods look similar on the surface but differ in task, embodiment, or evaluation protocol?
- Which papers are useful for framing the contribution even if they are not direct comparisons?

### Pass 4: Project-native evidence

Target outputs:

- local result tables
- configs
- experiment notes
- ablation artifacts
- evaluation scripts or metric definitions

Questions:

- Which internal results are reproducible and citable?
- Which claimed capabilities are supported by actual artifacts?
- Which gaps block a stronger abstract or contribution section?

## Deliverables

1. Evidence brief
2. Related work matrix
3. Claim-to-evidence map
4. Gap report
5. Outline-ready writing notes
