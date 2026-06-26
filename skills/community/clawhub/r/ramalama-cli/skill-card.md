## Description: <br>
Run and interact with AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ieaves](https://clawhub.ai/user/ieaves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run RamaLama workflows for local or containerized inference, serving, RAG packaging, benchmarking, and model lifecycle tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Serving a model can expose a local OpenAI-compatible endpoint if it is bound beyond localhost or left running. <br>
Mitigation: Bind serve workflows to localhost unless remote access is intentional, avoid sensitive prompts on shared or untrusted networks, and stop the server when finished. <br>


## Reference(s): <br>
- [Model Guide](references/models.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ieaves/ramalama-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ramalama and either Docker or Podman; serving workflows may start a local HTTP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
