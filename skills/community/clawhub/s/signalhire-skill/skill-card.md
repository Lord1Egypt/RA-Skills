## Description: <br>
Prospect and enrich contacts via the SignalHire API for search, person enrichment, and credits checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ms-youssef](https://clawhub.ai/user/ms-youssef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent check SignalHire credits, search for prospects, and enrich contact details through SignalHire workflows. The companion connector receives asynchronous Person API callbacks and writes enrichment results to CSV for downstream CRM or analysis use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public callback endpoint accepts unauthenticated inbound data. <br>
Mitigation: Use a hard-to-guess callback path or proxy-level authentication where feasible, and expose only the callback route required for SignalHire. <br>
Risk: Enriched contact details are stored in local CSV files. <br>
Mitigation: Restrict the output directory, apply a retention schedule, and review privacy and compliance obligations before importing the data into downstream systems. <br>
Risk: The SignalHire API key can be misused if exposed or left unmonitored. <br>
Mitigation: Provide the key only through SIGNALHIRE_API_KEY, rotate it regularly, and monitor usage and remaining credits. <br>


## Reference(s): <br>
- [SignalHire API documentation](https://www.signalhire.com/api/person) <br>
- [ClawHub skill listing](https://clawhub.ai/ms-youssef/signalhire-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text, CSV files] <br>
**Output Format:** [Markdown guidance with inline shell commands, API workflow descriptions, JSON status responses, and CSV output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIGNALHIRE_API_KEY and SIGNALHIRE_CALLBACK_URL; connector output defaults to local CSV files under SIGNALHIRE_OUTPUT_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
