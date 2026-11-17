## Description:

Deploy and manage a SONiC sonic-mgmt KVM virtual testbed with cEOS neighbors for running pytest-based network tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxieca](https://clawhub.ai/user/yxieca)

### License/Terms of Use:


## Use Case:

Network developers and test engineers use this skill to set up, troubleshoot, redeploy, and run pytest-based SONiC tests against a local KVM sonic-vs testbed with cEOS neighbors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends weak default credentials for lab users and network devices.

Mitigation: Replace default passwords with unique secrets before use and avoid embedding passwords in reusable commands or files.

Risk: The skill includes root-equivalent Docker access patterns, including unrestricted Docker socket permissions and broad sudo rights.

Mitigation: Use an isolated disposable lab host, avoid chmod 666 on /var/run/docker.sock, and restrict sudo privileges where possible.

Risk: The skill relies on moving external branches and container images for SONiC, cEOS, and sonic-mgmt components.

Mitigation: Pin reviewed git commits and container image digests, and limit management network reachability to the lab environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxieca/skills/sonic-kvm-testbed)
- [Credentials Configuration](artifact/references/credentials.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, and inventory snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended for an isolated disposable lab host and includes setup, credential, deployment, teardown, and troubleshooting procedures.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
