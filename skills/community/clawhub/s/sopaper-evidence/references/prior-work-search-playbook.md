# Prior Work Search Playbook

Use this playbook when the user needs a serious prior-work search rather than a loose literature summary.

## Goal

Build a search set that is broad enough to avoid obvious misses and strict enough to avoid weak or irrelevant citations.

## Search passes

Run the search in passes instead of one large query.

### Pass 1: Problem framing

Search for papers that define or directly target the core problem.

Collect:

- canonical task names
- standard metrics
- common dataset and benchmark names
- major method families

### Pass 2: Recent strong baselines

Search for:

- recent papers in the same task area
- official repos for high-visibility methods
- benchmark leaders when official sources exist

Collect:

- what the method does
- what it compares against
- where it was evaluated
- whether code or artifacts are public

### Pass 3: Adjacent approaches

Search for methods that solve nearby variants of the same problem.

Use this pass to avoid an over-narrow related work section.

Examples:

- policy-only versus planner-plus-policy approaches
- simulation-heavy versus real-world evaluations
- system papers versus algorithm papers

### Pass 4: Negative boundary scan

Search for papers that look similar but should not be treated as direct baselines.

The point of this pass is to prevent bad comparisons.

Record why each item is out of scope:

- wrong task
- wrong embodiment
- wrong metric
- wrong environment
- no comparable evaluation

## For each paper, capture

- title
- year
- venue or source
- URL
- task
- dataset or benchmark
- metrics
- baseline family
- relevance to the user's project
- reasons it may not be directly comparable

## Search quality checks

- Do not stop after the first few famous papers
- Do not treat citation count as proof of relevance
- Do not rely on one benchmark if the project spans multiple settings
- Do not collapse adjacent tasks into the same comparison bucket without justification

## Default output

When the user asks for prior work, produce:

1. `Search scope`
2. `Candidate paper list`
3. `Direct baselines`
4. `Adjacent but non-baseline work`
5. `Missing areas to search next`
