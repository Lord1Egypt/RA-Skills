## Description: <br>
Audit tool and command results before acting on them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to review command or tool output before continuing multi-step workflows. It helps classify results as success, failure, partial, or ambiguous so packaging, publishing, deployment, API, process, and file-generation workflows do not proceed on assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper uses heuristic pattern matching, so a classification can be incomplete or wrong. <br>
Mitigation: Treat the verdict as a review aid and manually inspect decisive lines before taking the next action. <br>
Risk: Captured command output can contain tokens, API keys, or other secrets, and matching lines may be printed back to the console. <br>
Mitigation: Avoid passing sensitive logs to the helper, or redact secrets before auditing output. <br>


## Reference(s): <br>
- [Tool Output Audit Checklist](references/checklist.md) <br>
- [Real Output Patterns](references/examples.md) <br>
- [Real Mistakes This Skill Is Designed To Catch](references/real-mistakes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/daowuu/tool-output-auditor) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance and plain-text command-output classifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper classifies captured output heuristically and highlights decisive lines when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
