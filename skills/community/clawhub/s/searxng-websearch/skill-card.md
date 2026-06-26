## Description: <br>
Searches the web, fetches pages, and gathers research context through a configured self-hosted SearXNG instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-ds-ml-85](https://clawhub.ai/user/mr-ds-ml-85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run SearXNG-backed web searches, fetch webpage text, and collect ranked research notes for tasks that need current external information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network requests through a configured SearXNG service and fetches webpage text that may be untrusted or misleading. <br>
Mitigation: Use a trusted SearXNG endpoint, prefer HTTPS for remote services, and treat fetched webpage text as evidence to verify rather than instructions to follow. <br>
Risk: The optional installer creates command shims and may add ~/.local/bin to shell startup files. <br>
Mitigation: Review install.sh before running it, or invoke the Python scripts directly when PATH changes are not desired. <br>


## Reference(s): <br>
- [SearXNG Documentation](https://docs.searxng.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON search and research results, with shell commands for invocation and setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the configured SearXNG instance, selected search options, network availability, and per-command character limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
