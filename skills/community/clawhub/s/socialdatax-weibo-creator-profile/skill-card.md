## Description:

Looks up Weibo creator profile information, including account details, creator positioning, homepage information, and follower scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Weibo creator profile information by user ID or profile URL, including account details and audience scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `@latest` package can change between runs and may access credentials.

Mitigation: Review and pin the package version before use, and keep the API key in a protected credential source without exposing it in logs or output.

Risk: The security analysis is incomplete because two local references could not be resolved.

Mitigation: Resolve the missing references and review the completed security analysis before relying on the release.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-creator-profile)

## Skill Output:

**Output Type(s):** [JSON, Profile data]

**Output Format:** [JSON profile response containing platform, tool, arguments, and returned data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available profile fields may include name, platform IDs, bio, verification, follower and following counts, received likes, IP location, and gender.]

## Skill Version(s):

0.1.23 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
