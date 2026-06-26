## Description: <br>
Interact with SOLID Pods - read data, write RDF data, create containers, manage access control, and provision new SOLID Pods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pettifordo](https://clawhub.ai/user/pettifordo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate on Solid Pods from an agent, including reading pod resources, writing RDF data, creating containers, managing access rules, and provisioning Community Solid Server pods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, delete, and change access controls on Solid Pod resources. <br>
Mitigation: Use least-privilege Solid client credentials and verify target URLs and WebIDs before write, delete, or ACL commands. <br>
Risk: Dependency versions may change behavior or security posture in high-assurance environments. <br>
Mitigation: Consider pinning dependencies and reviewing installed packages before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pettifordo/solidpod-data) <br>
- [Solid Project](https://solidproject.org/) <br>
- [Inrupt Solid Client](https://github.com/inrupt/solid-client-js) <br>
- [Inrupt Solid Client Authn Node](https://github.com/inrupt/solid-client-authn-js) <br>
- [Inrupt Common RDF Vocabularies](https://github.com/inrupt/solid-common-vocab-rdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples and operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Solid environment variables for identity provider, client credentials, pod URL, and optional OIDC issuer.] <br>

## Skill Version(s): <br>
1.2.6 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
