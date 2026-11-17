## Description:

Converts public WeChat articles into offline Markdown, HTML, text, JSON, or Excel files after asking the user which export formats to produce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojiangyong](https://clawhub.ai/user/luojiangyong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save single or multiple public WeChat articles for offline reading, archival, or downstream document processing. The skill is most useful when the user needs a chosen export format before the agent runs the included fetch scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML export can fetch attacker-controlled resource URLs and preserve active HTML content.

Mitigation: Prefer Markdown, text, or JSON for lower-risk exports; review or constrain HTML export behavior before opening or sharing HTML generated from untrusted articles.

Risk: Remote CSS and image assets are downloaded during HTML export.

Mitigation: Run the skill with network and filesystem constraints appropriate for the article source, and add asset URL allowlisting before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luojiangyong/skills/wechat-article-conversion)
- [Publisher profile](https://clawhub.ai/user/luojiangyong)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Agent guidance plus generated Markdown, HTML, plain text, JSON, and Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process one or more WeChat article URLs; selected formats are produced as local files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
