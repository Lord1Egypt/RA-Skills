## Description: <br>
Session retrospective that analyzes conversation history to produce structured feedback for both user and LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review project conversation history, identify user prompting patterns, and critique LLM performance after one or more sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad local AI assistant session logs and include sensitive conversation content in generated feedback files. <br>
Mitigation: Before running it, confirm which session files will be included, restrict analysis to the intended project or session, and redact secrets or private data. <br>
Risk: The skill writes retrospective files in the project root that may persist sensitive feedback longer than intended. <br>
Mitigation: Review access to FEEDBACK_TO_HUMAN.md and FEEDBACK_TO_LLM.md and delete the temporary transcript and feedback files when they are no longer needed. <br>


## Reference(s): <br>
- [Retrospect on ClawHub](https://clawhub.ai/zbc0315/retrospect) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Shell commands] <br>
**Output Format:** [Markdown feedback files with structured retrospective analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; creates a temporary transcript and writes FEEDBACK_TO_HUMAN.md and FEEDBACK_TO_LLM.md in the project root.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
