## Description: <br>
Turns science or technical explainer text into a single-page HTML presentation or flowchart-style animation using bundled PPT and Animation templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, educators, and developers use this skill to transform science or technical explainer text into browser-based slide animations for videos, classroom lessons, demos, and technical sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled templates and generated HTML may contact third-party CDNs for fonts or icon libraries. <br>
Mitigation: Review generated HTML before publishing or deploying, and replace CDN dependencies with approved local assets when offline or controlled execution is required. <br>
Risk: Some bundled templates contain unrelated OpenClaw-specific warning content or a restriction-removal example that may be unsuitable for neutral presentations. <br>
Mitigation: Inspect selected templates before use and remove or replace unrelated warning content before relying on the output. <br>
Risk: The workflow can overwrite an existing AI_Animation.html file when the output path is not explicit. <br>
Mitigation: Specify the output path for each run and confirm whether an existing file may be overwritten. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unclecheng-li/unclecheng-ai-animation) <br>
- [README](artifact/README.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [PPT template selection guide](artifact/assets/templates/PPT Template-level2/SUMMARY.md) <br>
- [Animation template selection guide](artifact/assets/templates/Animation/SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated single-file HTML/CSS/JavaScript presentation code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may use bundled HTML templates and can write or rewrite an AI_Animation.html file at a user-selected path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
