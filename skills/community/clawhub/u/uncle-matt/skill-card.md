## Description: <br>
Uncle Matt lets OpenClaw agents call approved API actions through a hardened local Broker without exposing secrets, calling arbitrary URLs, or becoming an open proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to constrain agent-initiated external API calls to preapproved local Broker actions while keeping secrets out of the agent context. It is intended for OpenClaw workflows that need strict outbound API boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The separate Broker installation could be misconfigured before use. <br>
Mitigation: Review the Broker configuration and installer scripts before running them, then validate the configured actions before restart. <br>
Risk: Secrets could be exposed if operators store them in JSON configuration files. <br>
Mitigation: Keep secrets out of JSON configs and let the local Broker inject secrets at runtime. <br>
Risk: A Broker exposed beyond localhost could expand the attack surface. <br>
Mitigation: Keep the Broker bound to localhost unless a reviewer approves a more restrictive deployment design. <br>
Risk: Overbroad action definitions could permit unintended outbound access. <br>
Mitigation: Add only API actions with tightly pinned hosts, paths, methods, request limits, response limits, budgets, and rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/uncle-matt) <br>
- [Publisher profile](https://clawhub.ai/user/uncmatteth) <br>
- [Project homepage](https://bobsturtletank.fun) <br>
- [Full project repository referenced by artifact](https://github.com/uncmatteth/UNCLEMATTCLAWBOT) <br>
- [Artifact operator quick guide](artifact/README.md) <br>
- [Artifact generated actions list](artifact/ACTIONS.generated.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown guidance with inline tool-call and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional voice packs are limited to refusals and warnings; the Broker and installer are not packaged in this skill artifact.] <br>

## Skill Version(s): <br>
5.420.70 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
