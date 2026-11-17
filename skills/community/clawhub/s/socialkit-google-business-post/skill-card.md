## Description:

Publishes an update, event or offer to the user's Google Business Profile through the official Business Profile APIs after the user approves it. Use when the user wants to post to their Google Business Profile or Google Maps listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External business owners and their agents use this skill to prepare and publish an approved update, event, or offer on a Google Business Profile or Google Maps listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested business.manage permission is broad.

Mitigation: Use your own Google Cloud OAuth client and review the requested permission before signing in.

Risk: The stored refresh token can grant continued access to the Google account.

Mitigation: Protect the stored refresh token and keep its credentials private.

Risk: A post can publish incorrect details or public photos to the wrong business location.

Mitigation: Check the location, post text, and public photo URLs, then review the post and approve it before publishing.

Risk: The required socialkit-social-core dependency was not supplied for review.

Mitigation: Review socialkit-social-core separately, including its initialization and approval behavior, before use.

## Reference(s):

- [Google Business Profile setup](references/setup.md)
- [Business Profile API prerequisites](https://developers.google.com/my-business/content/prereqs)
- [Business Profile posts](https://developers.google.com/my-business/content/posts-data)
- [ClawHub skill page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-google-business-post)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Google Business Profile post with a JSON publication result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes a user-approved update, event, or offer.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
