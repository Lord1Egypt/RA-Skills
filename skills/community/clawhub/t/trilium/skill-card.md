## Description:

Manage Trilium Notes by reading, searching, and creating notes via the ETAPI with a provided server URL and ETAPI token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtbf999](https://clawhub.ai/user/mtbf999)

### License/Terms of Use:


## Use Case:

Developers and Trilium users use this skill to search, read, and create notebook content in a Trilium database through the External Trilium API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a Trilium database through an ETAPI token.

Mitigation: Use only a Trilium server and token you control, keep the token out of chat, and store it in the environment or a local configuration file.

Risk: Agent actions could create, update, or delete Trilium notes when ETAPI access is available.

Mitigation: Review requested note changes or deletions before allowing them, especially for important notebooks.

## Reference(s):

- [Trilium ETAPI Reference](references/api.md)
- [Trilium ETAPI Wiki](https://github.com/zadam/trilium/wiki/Etapi)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Markdown]

**Output Format:** [Markdown with Trilium note content, search results, configuration guidance, and ETAPI request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-controlled Trilium server URL and ETAPI token.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
