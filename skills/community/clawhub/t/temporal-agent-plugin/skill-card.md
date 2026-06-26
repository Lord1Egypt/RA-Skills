## Description: <br>
Provides temporal awareness for AI agents, including timing prediction, progress monitoring, and social timing understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmzuo1976](https://clawhub.ai/user/xmzuo1976) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent builders use this skill to add timing prediction, progress monitoring, anomaly detection, social timing analysis, time anchoring, and framework/API integrations to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated archive-unpacking script. <br>
Mitigation: Avoid running process_base64_zip.py unless the archive source is trusted and the unpacking behavior is intentionally needed. <br>
Risk: External location lookup is under-disclosed. <br>
Mitigation: Document or disable location lookup before deployment, especially for workflows with privacy or network restrictions. <br>
Risk: The API server could expose timing and agent workflow functions beyond trusted users. <br>
Mitigation: Run the API only on trusted networks and review access controls before exposing it. <br>
Risk: Installing the release directly may run code and dependencies that have not been locally reviewed. <br>
Mitigation: Review before installing, use an isolated environment, and pin dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xmzuo1976/temporal-agent-plugin) <br>
- [README.md](artifact/README.md) <br>
- [RELEASE_NOTES.md](artifact/RELEASE_NOTES.md) <br>
- [VERSION_LOG.md](artifact/VERSION_LOG.md) <br>
- [Community feedback post 10347](https://clawd.org.cn/forum/post?id=10347) <br>
- [Community feedback post 10455](https://clawd.org.cn/forum/post.html?id=10455) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include library usage patterns, API invocation examples, dependency guidance, and integration steps.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and VERSION_LOG.md, released 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
