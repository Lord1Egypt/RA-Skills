## Description: <br>
Generates QR codes from text, URLs, WiFi credentials, vCards, or other data as PNG, SVG, or ASCII output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and other external users can use this skill to generate scannable QR codes for links, plain text, WiFi network credentials, contact cards, or arbitrary payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script may automatically install Python packages at runtime. <br>
Mitigation: Review the package installation behavior before use, run in a controlled environment, and install dependencies explicitly when policy requires approval. <br>
Risk: WiFi QR codes can encode credentials that may be exposed through shell history, logs, or generated files. <br>
Mitigation: Avoid passing real passwords in commands that may be logged, restrict access to generated QR files, and rotate credentials if exposure is suspected. <br>
Risk: The script writes generated output to filesystem paths chosen by the user. <br>
Mitigation: Use output paths that are intended to be modified and review paths before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudiodrusus/qr-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated QR artifacts may be PNG, SVG, or ASCII text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write QR output files to user-specified paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
