## Description: <br>
Checks Xiaohongshu copy, document text, image-extracted text, or webpage text for prohibited words, highlights matched terms, and provides replacement suggestions plus an optimized draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand operators, advertising teams, and content reviewers use this skill to screen Xiaohongshu publishing copy for prohibited terms before posting. It supports pasted text, supported document files, image text extracted by the agent, and webpage text, then returns marked risks, safer wording suggestions, and an optimized text draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked copy, extracted document text, and fetched webpage text are sent to RedFoxHub for processing. <br>
Mitigation: Use the skill only for content approved for external processing, and avoid submitting confidential, regulated, or private internal material. <br>
Risk: The script can read REDFOX_API_KEY from shell profile files if the environment variable is not set. <br>
Mitigation: Set REDFOX_API_KEY only as a scoped environment variable and avoid storing it in shell profile files alongside other secrets. <br>
Risk: Detection results are guidance and may not reflect the final Xiaohongshu platform review outcome. <br>
Mitigation: Have the publisher or compliance owner review suggested replacements before posting or approving campaign content. <br>


## Reference(s): <br>
- [Core Workflow](references/core_workflow.md) <br>
- [RedFoxHub](https://redfox.hk/) <br>
- [RedFoxHub API Keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [ClawHub Skill Page](https://clawhub.ai/if530770/xhs-prohibited-word) <br>
- [Publisher Profile](https://clawhub.ai/user/if530770) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown response with highlighted prohibited terms, suggestion tables, and a downloadable plain-text optimized draft file when replacements are produced] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends checked content to RedFoxHub for detection; recommended single request size is up to 3000 characters.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
