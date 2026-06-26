## Description: <br>
Local-only skill for converting horizontal Chinese fonts into high-quality vertical-reading TTF fonts with a preview-first workflow, grouped glyph rules, and local audit/test artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aster-copilot](https://clawhub.ai/user/aster-copilot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert user-provided Chinese fonts into vertical-reading TTFs while preserving readability through preview gates, grouped glyph handling, local audit output, and reader test artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs local Python scripts against user-provided font files. <br>
Mitigation: Run it only on font files you choose, in a normal project or output directory, and review the generated artifacts. <br>
Risk: Converted fonts may be subject to the source font's license or commercial-use restrictions. <br>
Mitigation: Verify that you have the rights to convert and use the source font before using the generated TTF. <br>
Risk: Vertical typography quality can vary by source font and glyph group. <br>
Mitigation: Use the required horizontal and vertical previews, reader test TXT, and optional audit output before relying on the final font. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aster-copilot/ttf-converter) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Glyph rules](artifact/references/rules.md) <br>
- [Implementation notes](artifact/references/implementation-notes.md) <br>
- [Default configuration](artifact/references/default-config.json) <br>
- [Examples](artifact/references/examples.md) <br>
- [Confirmed case: Zihun Songkekaiti](artifact/references/cases-zihun-songkekaiti.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file artifacts such as TTF, PNG, TXT, and optional JSON audit output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only workflow; expects user-provided font files and commonly uses fontTools and Pillow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
