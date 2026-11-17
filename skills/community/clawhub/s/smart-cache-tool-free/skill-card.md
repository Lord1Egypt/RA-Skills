## Description: <br>
智能缓存工具-免费版 helps developers manage local caches with LRU/LFU eviction, TTL expiry, hit-rate statistics, manual cache clearing, and optional disk persistence for API responses, computed results, and file contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small project teams use this skill to add or tune local cache behavior for API responses, expensive computations, and frequently read files. It is intended for local cache-management tasks such as choosing an eviction strategy, setting TTLs, reviewing hit-rate statistics, and clearing or persisting cache entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read, exec, glob, and grep tool access may affect files or commands outside an intended cache-management task. <br>
Mitigation: Use the skill only for explicit cache-management requests and review proposed commands or file access before execution. <br>
Risk: Disk persistence can store private API responses, file contents, or computed data in cache files. <br>
Mitigation: Choose safe cache paths and permissions, and avoid persisting secrets or private content unless retention is intentional. <br>
Risk: Manual cache deletion or clear operations can remove data that a project expects to reuse. <br>
Mitigation: Confirm the target cache key, path, or scope before delete and clear operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/smart-cache-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON-style result structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes json, text, and csv output preferences through an output_format option.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
