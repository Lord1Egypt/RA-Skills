## Description: <br>
Checks email breach exposure and password strength, then generates security score reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, developers, and security teams use this skill to check whether an email or password appears in known breach data, review password strength, scan for exposed secrets, and generate concise security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles email addresses and passwords during security checks. <br>
Mitigation: Use interactive prompts or test passwords, avoid passing real passwords on the command line, and install only when sending email addresses to HIBP is acceptable. <br>
Risk: Enterprise OSINT, phishing-simulation, and secret-scanning workflows may expose or process sensitive organizational findings. <br>
Mitigation: Run those workflows only with explicit organizational authorization and handle generated findings as sensitive security data. <br>
Risk: Privacy expectations may be unclear for breach and password checks. <br>
Mitigation: Review the skill's HIBP data flows and local password-check behavior before using it with real accounts or credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freedompixels/security-health-check) <br>
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3) <br>
- [Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Plain text and JSON reports with command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security scores, breach summaries, password-strength assessments, masked secret findings, and remediation guidance.] <br>

## Skill Version(s): <br>
2.1.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
