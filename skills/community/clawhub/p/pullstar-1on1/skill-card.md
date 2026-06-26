## Description: <br>
Generate a ready-to-use 1-on-1 brief for any engineer on your team from their GitHub activity, including patterns such as high output with low review participation, large PR sizes, and cross-repo collaboration signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacksync](https://clawhub.ai/user/jacksync) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineering managers use this skill to prepare for 1-on-1 meetings by turning a direct report's GitHub activity into a concise, scan-ready brief. The workflow gathers scoped GitHub activity, scores contribution patterns locally, prepares an LLM input, and finalizes a markdown brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub token and may access private repository activity depending on token scope. <br>
Mitigation: Use the narrowest GitHub token scope that still works and set GITHUB_ORG where possible to limit ingestion scope. <br>
Risk: Generated .pullstar artifacts may contain private repository activity and PR discussion excerpts. <br>
Mitigation: Treat .pullstar artifacts as sensitive local files and review llm_input before sending it to an AI provider, especially when PR insights are enabled. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/jacksync/pullstar-1on1) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown brief and JSON artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local .pullstar artifacts, including LLM input, LLM output, and final brief JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
