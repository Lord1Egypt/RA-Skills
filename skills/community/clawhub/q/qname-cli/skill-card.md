## Description: <br>
Use QName.AI domain lookup from the terminal. Call this when an Agent needs WHOIS/domain availability evidence for one domain at a time through the approved QName API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibevibing](https://clawhub.ai/user/vibevibing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run one-domain QName.AI WHOIS and domain availability lookups from the terminal, with JSON output available for downstream parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an approved QName API key for CLI use. <br>
Mitigation: Use environment variables for temporary sessions and avoid printing stored secrets unless intentionally inspecting local configuration. <br>
Risk: Using the CLI outside its documented scope may produce unsupported or incomplete workflows. <br>
Mitigation: Limit use to single-domain WHOIS or availability lookups and avoid batch lookup, realtime stream checks, traffic analysis, domain rating, or registrar purchase actions. <br>


## Reference(s): <br>
- [QName.AI](https://qname.ai) <br>
- [ClawHub release page](https://clawhub.ai/vibevibing/qname-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides one-domain lookups and credential setup; QName CLI responses may be JSON or text depending on command flags.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
