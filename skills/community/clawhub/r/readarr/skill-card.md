## Description: <br>
Interact with Readarr via its REST API to search books, monitor authors, check wanted or missing items, trigger downloads, and manage an ebook or audiobook library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minerva-care](https://clawhub.ai/user/minerva-care) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to produce Readarr API calls, shell commands, and configuration guidance for managing ebook and audiobook acquisition, author monitoring, wanted or missing lists, download queues, and Calibre handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Readarr API key that can expose library access if copied into prompts, logs, or shared files. <br>
Mitigation: Keep the API key private, store it in a restricted-permission file, and avoid including it in prompts or logs. <br>
Risk: Generated Readarr API calls can change the library, remove queue items, or trigger broad searches and downloads. <br>
Mitigation: Review commands before execution and explicitly confirm deletions, queue removals, and broad search operations. <br>


## Reference(s): <br>
- [Readarr API Reference](references/api.md) <br>
- [Readarr Setup](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl, JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls that view or change a Readarr library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
