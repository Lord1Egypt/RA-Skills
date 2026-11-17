## Description:

Execute Python code through inference.sh in a sandboxed Python 3.10 environment with pre-installed libraries for data processing, web scraping, media processing, document generation, API calls, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run bounded Python scripts for data analysis, scraping, image, video, and 3D processing, PDF generation, API calls, and automation without managing a local Python environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented quick start pipes a mutable remote installer into a shell.

Mitigation: Download and inspect the CLI installer separately, verify its checksum against the published checksums, and run it only when the inference.sh delivery path is trusted.

Risk: Executed Python code can contact external services or process sensitive data if the submitted script does so.

Mitigation: Review code before execution and avoid passing secrets or private data unless outbound service calls are intended.

Risk: Generated files and captured output may reflect untrusted web, API, or user-provided input.

Mitigation: Review returned files and stdout before using them in downstream workflows.

## Reference(s):

- [Python Executor on ClawHub](https://clawhub.ai/okaris/skills/python-executor)
- [Running Apps](https://inference.sh/docs/apps/running)
- [App Code](https://inference.sh/docs/extend/app-code)
- [Sandboxed Code Execution](https://inference.sh/blog/tools/sandboxed-execution)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with inline bash and JSON examples; executed app responses may include stdout text and generated files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python code supports a 1-300 second timeout, optional output capture, an optional working directory, and automatic return of files saved under outputs/.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
