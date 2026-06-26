## Description: <br>
Search hashes through 25 billion leaked passwords using the Weakpass API (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibnaleem](https://clawhub.ai/user/ibnaleem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security practitioners use Weakpass to query leaked-password hash lookups, hash-prefix ranges, generated wordlists, and available wordlist data during authorized password and security analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected hashes, prefixes, seed words, or wordlist names to weakpass.com and may return plaintext passwords or wordlists. <br>
Mitigation: Use only with authorization; do not submit production credential material, regulated data, proprietary hashes, or sensitive investigation targets unless approved, and avoid storing or logging returned plaintext passwords. <br>
Risk: Leaked-password results and generated wordlists are sensitive dual-use outputs. <br>
Mitigation: Restrict use to approved defensive password auditing, incident response, or security research workflows and review outputs before acting on them. <br>


## Reference(s): <br>
- [ClawHub Weakpass Release](https://clawhub.ai/ibnaleem/weakpass) <br>
- [Weakpass](https://weakpass.com/) <br>
- [Weakpass API](https://weakpass.com/api) <br>
- [Weakpass OpenAPI JSON](https://weakpass.com/openapi.json) <br>
- [Weakpass OpenAPI YAML](https://weakpass.com/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON or text API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses can include plaintext passwords, hash-password pairs, generated wordlists, and wordlist content from Weakpass.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
