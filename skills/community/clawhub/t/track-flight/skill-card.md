## Description: <br>
Track flights in real time with detailed status, gate information, delays, and live position using AviationStack flight data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafaforesightai](https://clawhub.ai/user/rafaforesightai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up flight status by IATA flight number, including schedule, gate, delay, aircraft, and live position details when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free AviationStack setup sends the API key and flight lookup over HTTP, which can expose sensitive travel lookups or credentials on untrusted networks. <br>
Mitigation: Use a dedicated, revocable AviationStack key; avoid sensitive lookups on untrusted networks; prefer an HTTPS-capable plan, proxy, or alternative provider when confidentiality matters. <br>
Risk: The skill depends on a third-party flight-data service and local Python dependencies, so availability, rate limits, and environment setup can affect results. <br>
Mitigation: Install dependencies in a virtual environment, monitor API quota, and verify critical flight details with an authoritative airline or airport source. <br>


## Reference(s): <br>
- [AviationStack API Setup](references/api-setup.md) <br>
- [AviationStack free API signup](https://aviationstack.com/signup/free) <br>
- [ClawHub Track Flight release page](https://clawhub.ai/rafaforesightai/track-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Formatted terminal text or raw JSON, with setup guidance and command examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AVIATIONSTACK_API_KEY environment variable and the Python requests package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
