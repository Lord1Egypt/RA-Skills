## Description: <br>
ZFONT-CLI searches ZFONT.CN for free commercial-use fonts, retrieves download links, downloads font archives, and can extract or send font files with installation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LANMIN-X](https://clawhub.ai/user/LANMIN-X) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users find, download, extract, and receive free commercial-use font files from ZFONT.CN. It is intended for users who need practical font acquisition and installation guidance in a conversational workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact ZFONT.CN, run local wget and unzip commands, write temporary files, and send generated local paths. <br>
Mitigation: Review the workflow before installation and require operational controls that confirm downloads, restrict sendable paths to created font files, validate archive size and contents, safely escape shell inputs, and clean up temporary files. <br>


## Reference(s): <br>
- [ZFONT.CN](https://zfont.cn/) <br>
- [ClawHub ZFONT-CLI release page](https://clawhub.ai/LANMIN-X/zfont-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with generated file paths and downloadable font archive or font file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HTTP requests to ZFONT.CN and local shell commands for download and extraction.] <br>

## Skill Version(s): <br>
1.5.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
