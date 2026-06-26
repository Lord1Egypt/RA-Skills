## Description: <br>
Guides OpenClaw agents in operating a ScrapeFun server through dedicated authenticated OpenClaw-facing APIs, with narrow fallback rules for generic ScrapeFun endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HaoweiLi97](https://clawhub.ai/user/HaoweiLi97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent list ScrapeFun library entries, inspect media state, prepare and submit downloads, confirm landed files, finalize imports, and request scans while reporting endpoint or permission blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide authenticated actions that submit downloads, finalize imports, or trigger scans, which can change media library state. <br>
Mitigation: Use a least-privilege OpenClaw access key and review requests before executing state-changing download, import, or scan workflows. <br>
Risk: The artifact permits admin login as a fallback authentication path. <br>
Mitigation: Prefer the OpenClaw access key path and use admin login only when necessary. <br>
Risk: Endpoint or permission mismatches can cause the agent to use an unintended workflow if fallback behavior is treated too broadly. <br>
Mitigation: Follow the documented OpenClaw endpoint order, stop on missing permissions, and use only the explicitly allowed fallback endpoints. <br>


## Reference(s): <br>
- [ScrapeFun API Reference](references/api.md) <br>
- [ClawHub ScrapeFun Release](https://clawhub.ai/HaoweiLi97/scrapefun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown with endpoint names, auth methods, required permissions, payload shapes, and returned results or blockers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP request details and JSON payload examples for authenticated ScrapeFun operations] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
