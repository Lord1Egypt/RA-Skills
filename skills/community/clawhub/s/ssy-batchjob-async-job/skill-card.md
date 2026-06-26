## Description: <br>
Use BatchJob HTTP APIs for strict upload validation, precheck, submit, polling, and cancellation with automatic file source resolution and fallback interaction only when a source is not readable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cocovs](https://clawhub.ai/user/cocovs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run and manage BatchJob service workloads, including file upload validation, precheck, job submission, status polling, cancellation, and result summary reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected files or attachments to a configured BatchJob service. <br>
Mitigation: Use it only with services authorized to process the selected data, and avoid confidential files unless that service is approved for them. <br>
Risk: Misconfigured service URLs or broad bearer tokens could send data or job requests to the wrong endpoint or with excessive access. <br>
Mitigation: Verify BATCHJOB_BASE_URL before use and provide a scoped BATCHJOB_BEARER_TOKEN. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, CSV, and JSONL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BatchJob IDs, status, progress, output summary URLs, and copyable input templates.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
