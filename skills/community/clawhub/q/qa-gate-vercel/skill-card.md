## Description: <br>
Pre-production validation gate for Vercel/Supabase/Firebase stacks that generates test plans, executes validation suites, checks APIs, UI flows, toast behavior, LLM output quality, and produces go/no-go reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill as a pre-production validation gate for web applications on Vercel with Supabase or Firebase integrations. It helps them discover validation surfaces, generate and run QA checks, and summarize release readiness in a go/no-go report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated validations can access provider APIs and network services using supplied tokens. <br>
Mitigation: Use staging systems, test accounts, and least-privilege credentials; review the generated test plan before execution. <br>
Risk: Reports or generated tests could expose sensitive operational details if production data or privileged credentials are supplied. <br>
Mitigation: Avoid production data and service-role credentials unless the operator intentionally accepts that risk; redact secrets from reports. <br>
Risk: LLM-as-judge checks consume OpenRouter credentials and may send test prompts or outputs to an external API. <br>
Mitigation: Run rule-based checks first and provide only non-sensitive evaluation content to LLM-as-judge workflows. <br>


## Reference(s): <br>
- [Qa Gate Vercel on ClawHub](https://clawhub.ai/guifav/qa-gate-vercel) <br>
- [OpenClaw Skills Repository](https://github.com/guifav/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and Markdown reports, generated test files, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes QA artifacts under qa-reports/ and qa-tests/ when executed by an agent] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
