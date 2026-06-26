## Description: <br>
Create and verify no-thinking variants of local Qwen/Qwen3-series Ollama models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patmenciu](https://clawhub.ai/user/patmenciu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a reversible local Ollama tag for Qwen models that defaults to direct answers without requiring --think=false on every run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled workflow can modify the local Ollama model store for the selected target tag. <br>
Mitigation: Use a new derived target tag, keep the target different from the source model, and review --models-dir before running. <br>
Risk: Verification contacts the configured Ollama server and depends on the selected --host value. <br>
Mitigation: Review --host or OLLAMA_HOST before execution and prefer the intended local Ollama endpoint. <br>
Risk: Changing renderer/parser metadata for a derived tag can affect tool-calling or advanced renderer behavior. <br>
Mitigation: Keep the original source model unchanged and verify vision or tool workflows separately if they are needed. <br>


## Reference(s): <br>
- [Manifest Patch Reference](artifact/references/manifest-patch.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/patmenciu/qwen-nothink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local configuration/script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a derived local Ollama model tag and patch that target tag's local manifest/config when the bundled script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
