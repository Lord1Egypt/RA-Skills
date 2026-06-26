# tester-workflow

`tester-workflow` is an OpenClaw skill bundle for running a complete software testing workflow from requirements analysis to test case generation and review.

It packages the full testing flow into one skill so users can install one repository and get all required sub-skills together.

## What It Covers

- requirements analysis from a testing perspective
- design understanding from a testing perspective
- test case generation
- test case review
- one-stop installation with included sub-skills

## Included Sub-skills

This repository includes the following sub-skills under `included-skills/`:

- `analyze-requirements`
- `understand-design`
- `generate-test-cases`
- `review-test-cases`

## Workflow

A typical end-to-end flow looks like this:

```text
Requirements document
  -> analyze-requirements
  -> requirements analysis report
  -> understand-design
  -> design issue list
  -> generate-test-cases
  -> test cases (CSV)
  -> review-test-cases
  -> review report
```

## Repository Structure

```text
included-skills/      Bundled sub-skills
examples/             End-to-end usage examples
reference/            Workflow guidance and reference docs
SKILL.md              Main skill definition
README.md             Repository overview
```

## Usage Notes

- Use this skill when the user wants a full testing workflow instead of a single isolated task
- The sub-skills can also be used independently when needed
- The workflow emphasizes completeness, structured analysis, and quality gates over superficial speed

## Documentation

- Full workflow example: `examples/full-workflow.md`
- Workflow guide: `reference/workflow-guide.md`
- Sub-skill docs: `included-skills/`

## Publishing Notes

Before making this repository public, review:

- whether any included examples contain client-specific information
- whether any bundled templates or CSV examples contain sensitive data
- whether all documentation reflects the final public-facing skill name

## License

This project is released under the MIT License. See `LICENSE` for details.
