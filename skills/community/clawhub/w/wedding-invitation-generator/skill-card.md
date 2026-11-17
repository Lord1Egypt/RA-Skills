## Description:

Design elegant AI wedding invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, wedding planners, stationery designers, and marketplace sellers use this skill to generate wedding invitation suite artwork and related event stationery from short style prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta API token is passed through command-line arguments and may be exposed in shell history, shared process listings, or CI logs.

Mitigation: Use a low-privilege or short-lived token, avoid literal tokens on shared systems, prefer shell-session variables where appropriate, and rotate any token that may have been recorded.

Risk: The install commands shown in the artifact are mutable and may resolve to a different release later.

Mitigation: Install only from a pinned, trusted release when available and review the release before execution.

Risk: Prompts, optional reference UUIDs, and the API token are sent to api.talesofai.com.

Mitigation: Avoid submitting confidential event details, private reference identifiers, or credentials beyond the required Neta token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/wedding-invitation-generator)
- [Neta AI token and service page](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token, accepts prompt text plus optional size and reference image UUID, and can poll for up to about three minutes.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
