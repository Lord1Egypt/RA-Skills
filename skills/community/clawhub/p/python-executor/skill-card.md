## Description: <br>
Execute Python code in a sandboxed inference.sh environment with common data, scraping, visualization, media, document, and automation libraries pre-installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to run Python scripts for data processing, web scraping, visualization, image and video generation, 3D processing, PDF creation, API calls, and file-producing automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes remote Python code and may send code, data, network requests, and generated files through the provider. <br>
Mitigation: Install only when the provider is trusted, review code before execution, and avoid submitting secrets, private datasets, or sensitive outputs unless that transfer is intended. <br>
Risk: The quick-start install command pipes a remote installer into a shell. <br>
Mitigation: Prefer the documented manual install and SHA-256 checksum verification path before running the CLI. <br>
Risk: User-provided Python can make network requests and interact with external services. <br>
Mitigation: Review scripts for outbound requests and API usage before execution, especially when handling credentials or confidential data. <br>


## Reference(s): <br>
- [Python Executor ClawHub Page](https://clawhub.ai/okaris/python-executor) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [App Code](https://inference.sh/docs/extend/app-code) <br>
- [Sandboxed Code Execution](https://inference.sh/blog/tools/sandboxed-execution) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Code, Shell commands, Configuration] <br>
**Output Format:** [Command output, generated files, and Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Python 3.10 in a CPU-only environment with configurable timeout and 8GB or 16GB RAM variants.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
