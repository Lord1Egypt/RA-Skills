## Description:

Interact with SOLID Pods -- read data, write RDF data, create containers, manage access control, and provision new SOLID Pods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pettifordo](https://clawhub.ai/user/pettifordo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate on SOLID Pods from an agent workflow, including authenticated reads, RDF writes, container and area management, access-control changes, and pod provisioning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated credentials can be used against arbitrary SOLID Pod, IDP, or resource URLs supplied through environment variables or command arguments.

Mitigation: Use only trusted Pod and IDP URLs, verify each target URL before reads or writes, and avoid running the skill with credentials for Pods containing sensitive data unless the release has been reviewed.

Risk: Write, delete, acl grant, and acl revoke operations can replace data, remove resources, or change sharing permissions.

Mitigation: Require explicit confirmation for destructive or permission-changing actions and show the exact URL, WebID, modes, and data changes before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pettifordo/skills/solidpod-data)
- [SOLID Project](https://solidproject.org/)
- [Inrupt solid-client](https://github.com/inrupt/solid-client-js)
- [Inrupt solid-client-authn-node](https://github.com/inrupt/solid-client-authn-js)
- [Inrupt common RDF vocabularies](https://github.com/inrupt/solid-common-vocab-rdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with command examples and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display SOLID Pod resource contents, RDF properties, URLs, access-control entries, and generated registration instructions.]

## Skill Version(s):

1.2.6 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
