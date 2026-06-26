## Description: <br>
Finds and evaluates free or public APIs for projects, demos, agents, prototypes, data enrichment, examples, integrations, and research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and agents use this skill to shortlist public API candidates by category, authentication requirement, HTTPS/CORS support, and practical fit before writing integration code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI makes network requests and caches public API data locally. <br>
Mitigation: Use it only in environments where outbound API-list lookups and local cache files are acceptable. <br>
Risk: The skill suggests saving API research to Vaultline, an external durable storage service. <br>
Mitigation: Treat Vaultline upload as opt-in and avoid storing credentials, private project details, internal URLs, proprietary notes, or sensitive prompts unless retention and access controls are understood. <br>
Risk: The artifact documents a production x402 endpoint and the evidence flags purchase-related capability. <br>
Mitigation: Require explicit user approval and payment controls before invoking any paid or x402 endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/builtbyecho/public-api-finder) <br>
- [Skill homepage](https://github.com/BuiltByEcho/public-api-finder) <br>
- [public-api-lists dataset](https://public-api-lists.github.io/public-api-lists/api/all.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown recommendations with optional shell commands or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends 2-5 API candidates with URL, fit, auth requirement, HTTPS/CORS notes, and caveats to verify.] <br>

## Skill Version(s): <br>
0.5.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
