## Description: <br>
Rewrites user-provided WeChat public-account articles in the style of a selected author using bundled style profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers and content editors use this skill to transform source articles into WeChat-style Markdown drafts that follow a selected bundled author profile while preserving the article's core information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill imitates named authors' writing styles and could be used to publish output as if it came from the imitated author. <br>
Mitigation: Use only content the user owns or is authorized to rewrite, remove author-specific identifiers, and do not represent generated drafts as work by the imitated author. <br>
Risk: The artifact includes instructions to make AI-written text appear human-written by adding deliberate mistakes. <br>
Mitigation: Remove or ignore deliberate-error instructions before publication and review outputs for accuracy, transparency, and editorial standards. <br>
Risk: The security guidance flags under-scoped risky examples, including scraping and workplace-monitoring scenarios. <br>
Mitigation: Do not apply those examples without clear permission and appropriate legal, privacy, and data-handling safeguards. <br>
Risk: The security guidance warns against exposing secrets in prompts or files. <br>
Mitigation: Do not paste real API keys, credentials, or other sensitive secrets into source articles, style profiles, prompts, or generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harven-droid/wechat-style-writer) <br>
- [Style profile template](references/styles/README.md) <br>
- [Banfo style profile](references/styles/banfo.md) <br>
- [Dayu style profile](references/styles/dayu.md) <br>
- [Kazike style profile](references/styles/kazike.md) <br>
- [Laoxu style profile](references/styles/laoxu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown article draft with title candidates and rewritten body; optional .md file after user confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source article facts and key points while applying the selected style profile.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
