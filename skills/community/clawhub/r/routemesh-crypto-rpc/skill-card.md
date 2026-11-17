## Description:

Call RouteMesh's unified JSON-RPC endpoint (lb.routeme.sh) for any EVM chainId using a helper script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kermankohli](https://clawhub.ai/user/kermankohli)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to call RouteMesh's unified JSON-RPC endpoint for EVM chain data, RPC response debugging, and RouteMesh routing demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a RouteMesh API key for RPC calls.

Mitigation: Use a limited-scope or low-quota key, provide it through ROUTEMESH_API_KEY, and avoid sharing logs that contain request URLs.

Risk: The artifact references a helper script that is not included.

Mitigation: Confirm the helper script is present or provide an equivalent reviewed RPC caller before relying on the examples.

## Reference(s):

- [RouteMesh homepage](https://routeme.sh)
- [RouteMesh unified RPC endpoint](https://lb.routeme.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RouteMesh API key via ROUTEMESH_API_KEY and a Python runtime; the referenced helper script is not bundled in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
