## Description: <br>
Use Chanjing AI creation APIs to submit image or video generation tasks across multiple models, inspect task status, poll async results, and explicitly download generated assets when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit Chanjing image or video generation jobs, check asynchronous task status, poll for generated result URLs, and save generated assets only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived Chanjing credentials can be sent to an API host selected through CHANJING_API_BASE. <br>
Mitigation: Keep CHANJING_API_BASE unset for normal use, or set it only to the official Chanjing API or a host you fully control. <br>
Risk: Several documented command scripts are missing from the artifact, so the release may not work as documented or may require unreviewed files. <br>
Mitigation: Review the installed package contents before adding credentials and confirm the expected command scripts are present and reviewable. <br>


## Reference(s): <br>
- [Zyt ai creation on ClawHub](https://clawhub.ai/zuoyuting214/zyt-ai-creation) <br>
- [Reference](artifact/reference.md) <br>
- [Examples](artifact/examples.md) <br>
- [Chanjing Open API Base](https://open-api.chanjing.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, generated result URLs, and optional downloaded asset files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloaded assets are only saved when the user explicitly requests local output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
