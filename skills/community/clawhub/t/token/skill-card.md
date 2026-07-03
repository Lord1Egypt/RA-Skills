## Description: <br>
This skill helps agents reduce LLM token usage by guiding installation and use of the headroom token-compression wrapper, proxy, SDK, and MCP integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to set up prompt and context compression before requests reach Claude, OpenAI, Gemini, LiteLLM, LangChain, or MCP-compatible workflows. It is aimed at reducing API cost for long-context, coding-agent, RAG, log, and tool-output scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says this skill can route prompts, code, and tool output through headroom wrappers or a local proxy. <br>
Mitigation: Review the routing mode before use, avoid sending secrets or regulated data, and only enable wrappers or proxy settings in environments where that traffic path is acceptable. <br>
Risk: The security scan says original prompt content may be stored locally by compression and retrieval features. <br>
Mitigation: Confirm retention, purge, and access controls before production use, and configure or disable local content storage where sensitive data is involved. <br>
Risk: The security scan flags the curl-to-bash installer and mandatory promotional footer behavior. <br>
Mitigation: Prefer reviewing and pinning package installation steps instead of running remote shell installers, and remove or ignore promotional output requirements in governed deployments. <br>


## Reference(s): <br>
- [Headroom project repository](https://github.com/chopratejas/headroom) <br>
- [headroom-ai on PyPI](https://pypi.org/project/headroom-ai/) <br>
- [headroom-ai on npm](https://www.npmjs.com/package/headroom-ai) <br>
- [Headroom API reference](references/headroom_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, wrapper, proxy, SDK, MCP, environment variable, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
