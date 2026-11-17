## Description:

Read a SimplePractice Client Portal from a shell using curl, with passwordless sign-in or an optional browser session cookie, to retrieve appointments, billing documents, paperwork, announcements, and practice information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People with SimplePractice Client Portal access can use this skill to review appointments, billing documents, paperwork, announcements, and practice details through shell requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The portal session cookie grants access to sensitive health and billing information.

Mitigation: Use the intended practice hostname and confirm the selected client; keep the cookie jar permission-restricted, remove it when finished, and avoid shared machines. Review browser-pairing permissions if using the optional fpx route.

## Reference(s):

- [SimplePractice Client Portal request reference](artifact/references/requests.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown instructions with inline shell examples; JSON:API data retrieved through curl]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only portal data; responses depend on the signed-in client's access and practice permissions.]

## Skill Version(s):

1.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
