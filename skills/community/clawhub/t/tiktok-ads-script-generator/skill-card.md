## Description:

Creates TikTok vertical-ad captions and shot-by-shot scripts for US consumer brands, agencies, and creators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US consumer brands, agencies, and creators use the skill to draft TikTok Spark and non-Spark ad captions, spoken hooks, shot lists, disclosures, and claims to verify. It also creates a length-check report for draft text.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The optional Windows app is a separate download and was not inspected; its publisher-provided hash does not establish that it is safe.

Mitigation: The Python workflow does not require the app. Skip the download unless needed, and do not treat a matching hash as proof of safety.

Risk: Running the length checker can replace an existing length-check.md in the chosen output folder.

Mitigation: Choose an output folder where replacing that file is acceptable.

## Reference(s):

- [TikTok ad fields, format limits and review rules](references/tiktok-ad-specs.md)
- [TikTok Ads Script Generator on ClawHub](https://clawhub.ai/rapidworker1/skills/tiktok-ads-script-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Ad copy and shot-by-shot script, YAML brief, and Markdown length-check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captions and hook overlays are drafted against stated character limits; claims and disclosures are flagged for review.]

## Skill Version(s):

1.0.7 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
