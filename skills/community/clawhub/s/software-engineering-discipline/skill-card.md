## Description: <br>
Engineering discipline for coding agents on large, complex codebases, applying architecture boundaries, cohesion, contracts, concurrency, migrations, security, and bounded blast radius when writing, refactoring, or reviewing non-trivial code in real systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering-focused agents use this skill during non-trivial coding, refactoring, and review work to keep changes aligned with existing architecture, contracts, tests, observability, security, and migration constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add review and design overhead that is disproportionate for small, single-file, prototype, or glue-code changes. <br>
Mitigation: Apply the documented skip conditions for very small or throwaway work, and reserve the full operating loop for non-trivial changes in real systems. <br>
Risk: Architecture guidance may prompt larger design changes than the immediate task requires. <br>
Mitigation: Keep the diff bounded to the request, state the impact surface before wide changes, and confirm before moving contracts, boundaries, or migrations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown or plain text with optional code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
