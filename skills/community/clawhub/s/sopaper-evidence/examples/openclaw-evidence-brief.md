# OpenClaw Evidence Brief Example

## Scope

This brief supports early paper planning for OpenClaw, an embodied AI / robotics project. The objective is not to prove final performance claims, but to establish a reviewer-safe evidence base for related work framing, experiment design, and later draft support.

## Working assumptions

- OpenClaw is a manipulation-focused system rather than a pure simulator paper
- The final paper may need to compare planning, policy, and perception design choices
- Internal experimental evidence may exist but is not treated as paper-ready unless traceable to artifacts

## Evidence categories to collect

### Related work

- manipulation systems papers
- long-horizon embodied task papers
- policy-plus-planning hybrid methods
- sim-to-real or real-world robotics evaluations

### Benchmarks and datasets

- task suites relevant to manipulation and long-horizon behavior
- official dataset definitions
- evaluation protocols and metrics definitions

### Baselines

- strong recent methods that target similar tasks
- official implementations when available
- standard baseline families used in robotics and embodied AI papers

### Project-native evidence

- internal result tables
- run logs
- configuration files
- ablation records
- videos or artifact notes with provenance

## Claim style guidance

Until project-native evidence is verified, preferred claim forms are:

- `OpenClaw targets`
- `OpenClaw is designed to`
- `OpenClaw is intended to evaluate`

Avoid:

- `OpenClaw outperforms`
- `OpenClaw achieves state of the art`
- `OpenClaw solves`

## Key gaps to resolve before drafting

- identify benchmark-fit evidence
- identify baseline comparison coverage
- verify which internal results are reproducible and citable
- determine whether real-world validation exists or whether the paper is simulation-only
- determine whether contribution claims are method, system, benchmark, or integration claims

## Safe writing notes

- Related work can be drafted early if all citations are verified
- Abstract wording should remain conservative until quantitative evidence is validated
- Contribution bullets should be narrowed to supported scope
- Experiment sections should list missing ablations explicitly if they are not yet run
