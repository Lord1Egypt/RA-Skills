## Description:

Manage your wardrobe, get AI outfit suggestions, and virtually try on clothes before you buy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjc7951](https://clawhub.ai/user/jjc7951)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect an agent to The Style Index, manage wardrobe items, receive outfit suggestions, generate virtual try-on images, save outfits, and review wardrobe gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles user email, clothing photos, and a full-body reference photo for wardrobe and virtual try-on features.

Mitigation: Confirm the user is comfortable sharing those data types with The Style Index before account linking or photo upload, and follow the consent and email-verification flow before processing images.

Risk: The Style Index agent key grants connected-agent access and is sensitive.

Mitigation: Store the agent key securely, do not expose it in user-visible output or logs, and use account settings to revoke access when the connection is no longer wanted.

## Reference(s):

- [The Style Index ClawHub skill page](https://clawhub.ai/jjc7951/skills/style-index)
- [The Style Index agent API](https://thestyleindex.app/api/agent/auth/register)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with API request examples and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated try-on image links, outfit recommendations, wardrobe analysis, account-linking instructions, and status guidance from The Style Index API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
