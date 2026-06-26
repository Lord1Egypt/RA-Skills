## Description: <br>
Fetches WeChat Work developer documentation pages and converts their authenticated SPA content into clean Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouzhi](https://clawhub.ai/user/mouzhi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical writers use this skill to save authorized WeChat Work API documentation pages as local Markdown, including pages whose content is loaded by a client-side application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session cookies can grant access to authenticated WeChat Work documentation and should be treated as secrets. <br>
Mitigation: Use only authorized documents, keep cookies out of commits, screenshots, shared logs, and shell history, and prefer an isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mouzhi/wecom-doc-fetcher) <br>
- [WeChat Work developer documentation](https://developer.work.weixin.qq.com/document/path/*) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated agent outputs may include Markdown files converted from documentation pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a URL, optional output file path, optional doc_id, and optional session cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
