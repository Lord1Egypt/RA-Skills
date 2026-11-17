## Description:

Create and verify no-thinking variants of local Qwen/Qwen3-series Ollama models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patmenciu](https://clawhub.ai/user/patmenciu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create reversible no-thinking Ollama tags for local Qwen models, verify that thinking markers are absent, and avoid changing the source model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow persistently modifies local Ollama model metadata for the derived target tag.

Mitigation: Run with --dry-run first, back up relevant Ollama manifests and blobs, and verify the target tag is distinct from the source model before execution.

Risk: Accidental use of an existing valuable target tag could overwrite or require repair of local model metadata.

Mitigation: Prefer a new derived target name and avoid running against an existing important tag unless prepared to recreate or repair it.

Risk: Untrusted custom system text may affect the generated Modelfile behavior.

Mitigation: Avoid untrusted --system text and review the generated Modelfile before creating the derived tag.

## Reference(s):

- [Manifest Patch Reference](references/manifest-patch.md)
- [ClawHub Skill Page](https://clawhub.ai/patmenciu/skills/qwen-nothink)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Modelfile snippets, and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a bundled Python script that creates a derived Ollama model tag, patches local target metadata, and verifies output through the local Ollama API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
