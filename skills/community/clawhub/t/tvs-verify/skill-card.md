## Description: <br>
Verifies whether recent AI-made changes actually satisfy the user's original request by turning the request into acceptance criteria, gathering evidence, and reporting a clear pass, partial pass, fail, or unverifiable result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after an AI agent changes code, configuration, UI, documentation, or agent rules to verify that the original user request was actually satisfied. It focuses on narrow evidence collection rather than broad code review or silent fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification can require reading local project files or running targeted checks that expose sensitive project data to the agent. <br>
Mitigation: Review the planned evidence-gathering steps and limit checks to the files, commands, and observations needed to prove the user's acceptance criteria. <br>
Risk: Targeted commands may trigger slow builds, external services, or environment-specific side effects. <br>
Mitigation: Prefer narrow static checks and existing focused tests; review commands before execution when they could be slow, networked, or dependent on sensitive local services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inksnowhailong/tvs-verify) <br>
- [Publisher profile](https://clawhub.ai/user/inksnowhailong) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown validation report with acceptance criteria, evidence, risks, and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise command result summaries, file path evidence, UI observations, or manual verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
