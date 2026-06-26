## Description: <br>
Cheap first-pass web discovery without launching Chrome; fetch SSR pages, run bounded JavaScript, find routes, forms, and API endpoints, extract structured data, and detect bot-wall or browser-only escalation points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[protostatis](https://clawhub.ai/user/protostatis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Unbrowser for low-cost first-pass discovery and extraction on public or explicitly authorized web pages before escalating to a managed browser. It helps inspect routes, forms, API-like endpoints, structured data, and challenge signals while keeping authenticated actions user-confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive session cookies during authenticated browsing. <br>
Mitigation: Use only cookies explicitly provided by the user for the authorized host, confirm state-changing authenticated actions, clear cookies after use, and close the session before unrelated work. <br>
Risk: Cookie-solving services can expose browser cookies if bound or routed too broadly. <br>
Mitigation: Keep solver services on loopback, use explicit host allowlists for private or internal targets, and avoid remote cookie services unless the user intentionally trusts them. <br>
Risk: The security review flagged a helper that can grant a nested reviewer full local access. <br>
Mitigation: Install only in a trusted ClawHub maintenance environment and prefer the documented opt-out or non-yolo mode unless full local access is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/protostatis/unbrowser) <br>
- [Project homepage](https://github.com/protostatis/unbrowser) <br>
- [RPC methods reference](https://github.com/protostatis/unbrowser#rpc-methods) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-RPC request examples and escalation guidance; the skill itself does not directly produce persistent files.] <br>

## Skill Version(s): <br>
0.0.15 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
