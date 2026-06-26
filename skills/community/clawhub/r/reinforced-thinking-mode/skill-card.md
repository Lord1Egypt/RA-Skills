## Description: <br>
Guides agents through multi-round independent analysis where each round produces a complete, final-quality solution before synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stofancy](https://clawhub.ai/user/stofancy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analysts use this skill when they need an agent to explore complex designs, decisions, strategies, or risk assessments through several independent rounds before producing a final report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scratch files may contain sensitive or regulated problem details. <br>
Mitigation: Confirm the working directory before use and apply the same data-handling controls as the source material. <br>
Risk: Automatic cleanup can remove intermediate files that may be needed for audit or review. <br>
Mitigation: Ask the agent to retain intermediate files when reviewability or traceability is required. <br>
Risk: Broad trigger phrases could start a multi-round workflow when a lighter response would be enough. <br>
Mitigation: Invoke the skill explicitly for complex analysis and confirm scope before running multiple rounds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stofancy/reinforced-thinking-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a reinforced-thinking working directory, writes problem and round files, synthesizes final_report.md, and normally removes intermediate files after completion.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
