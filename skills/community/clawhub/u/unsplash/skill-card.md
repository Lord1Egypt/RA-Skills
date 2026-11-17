## Description:

Search, browse, and download high-quality free photos from Unsplash with filtering, random selection, and detailed photo metadata access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brokenwatch24](https://clawhub.ai/user/brokenwatch24)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill as an Unsplash API reference for finding photos, retrieving metadata, preparing download-tracking calls, and configuring authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Unsplash developer access key and may cause agents to send user search terms to Unsplash API endpoints.

Mitigation: Install only when this external API use is acceptable; prefer the environment variable credential path for temporary use or keep the config file permission-restricted.

Risk: Photo downloads may fail to meet Unsplash API requirements if download tracking is skipped.

Mitigation: Call the documented download endpoint before allowing downloaded photo use, and preserve attribution guidance where photos are surfaced.

## Reference(s):

- [ClawHub Unsplash Skill](https://clawhub.ai/brokenwatch24/skills/unsplash)
- [BrokenWatchCEO ClawHub Profile](https://clawhub.ai/user/brokenwatch24)
- [Unsplash Developers](https://unsplash.com/developers)
- [Unsplash API Base URL](https://api.unsplash.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides API endpoint patterns, authentication setup, request parameters, response structures, and operational notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
