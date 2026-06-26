## Description: <br>
Contribute to Simmer's hackathon entry by completing platform tasks, earning 0.01 USDC on Base per approved task and a possible prize share while using an existing Simmer API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adlai88](https://clawhub.ai/user/adlai88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with Simmer, browse and claim platform tasks, complete them, and submit deliverables for review and USDC payment eligibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Simmer API key and uses it against listed HTTPS task endpoints. <br>
Mitigation: Keep SIMMER_API_KEY out of chat logs and shell history, and send it only to the listed Simmer and task-bridge HTTPS endpoints. <br>
Risk: Task submission can include a Base wallet address for USDC rewards. <br>
Mitigation: Confirm with the user before sharing a wallet address and review the task submission payload before sending it. <br>
Risk: The hackathon deadline in the artifact has passed, so reward expectations may be stale. <br>
Mitigation: Verify that the Simmer contribution program is still active before claiming tasks or expecting payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adlai88/simmer-contributor) <br>
- [Simmer platform](https://simmer.markets) <br>
- [Simmer agent-readable docs](https://docs.simmer.markets/llms-full.txt) <br>
- [Simmer onboarding skill](https://simmer.markets/skill.md) <br>
- [Simmer SDK](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown instructions with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY for task APIs and may include a Base wallet address in task submissions.] <br>

## Skill Version(s): <br>
0.3.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
