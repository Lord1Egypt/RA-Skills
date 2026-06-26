## Description: <br>
Act as a professional tarot reader with multiple spreads, card meanings, spread selection by question, energy guidance, interpretation, and follow-up dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Superone77](https://clawhub.ai/user/Superone77) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to conduct tarot-style readings, choose an appropriate spread for a question, generate a spread result, and provide supportive interpretation and follow-up prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and write generated image or cache files. <br>
Mitigation: Run it with normal user permissions and review generated file paths before use. <br>
Risk: The image workflow can make outbound requests for tarot card art. <br>
Mitigation: Provide a local card image directory when possible to reduce network exposure. <br>
Risk: Custom reading JSON is consumed by the image generator. <br>
Mitigation: Use reading JSON produced by the skill and avoid passing untrusted custom reading JSON. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Superone77/vincitarot) <br>
- [Publisher profile](https://clawhub.ai/user/Superone77) <br>
- [README](artifact/README.md) <br>
- [Install guide](artifact/INSTALL.md) <br>
- [The Pictorial Key to the Tarot](https://www.sacred-texts.com/tarot/pkt/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or plain-text tarot interpretation, optional JSON reading data, and optional PNG spread image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The image workflow can write generated spread images and cached card-art files, and can use local card images to avoid outbound image requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
