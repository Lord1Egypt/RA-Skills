## Description: <br>
scellrun guides an agent through report-first single-cell and limited multi-omics analysis with the scellrun CLI for .h5ad, 10x mtx, cellranger, loom, and tabular expression inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drstrangerujn](https://clawhub.ai/user/drstrangerujn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents supporting clinicians or bench scientists use this skill to run scellrun analyses, inspect generated reports, and explain quality control, integration, marker, and annotation decisions in plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run commands on remote research systems where biomedical data lives. <br>
Mitigation: Before execution, confirm the remote host, account, dataset path, working directory, package version, files to be written, and whether tmux or a scheduler may be used. <br>
Risk: The skill may use AI helpers on sensitive or regulated biomedical datasets. <br>
Mitigation: Use least-privilege access and prefer --no-ai unless third-party processing has been explicitly approved. <br>
Risk: The skill may require sensitive credentials such as ANTHROPIC_API_KEY. <br>
Mitigation: Only pass credentials when approved for the dataset and environment, and avoid persisting secrets in shared shells, logs, or reusable command snippets. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/drstrangerujn/scellrun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, and report interpretation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct an agent to run scellrun locally or over SSH and to summarize generated HTML reports and decision logs.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
