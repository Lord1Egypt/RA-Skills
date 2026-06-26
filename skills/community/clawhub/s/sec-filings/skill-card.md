## Description: <br>
Query SEC filings for any public company by name, ticker, or CIK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovelaceai](https://clawhub.ai/user/lovelaceai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to look up SEC filings for public companies by name, ticker, or CIK and summarize filing metadata, company profiles, and extracted financial metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company lookup terms are sent to Lovelace's external SEC API and are subject to Lovelace's terms. <br>
Mitigation: Avoid sending confidential or sensitive company research terms unless that external service use is acceptable for the user's environment. <br>
Risk: SEC filing lookup results and extracted financial metrics may be incomplete, unavailable, or tied to a close-match entity rather than the intended company. <br>
Mitigation: Review the returned company name, CIK, alternatives, filing links, and source SEC filing before relying on the result. <br>


## Reference(s): <br>
- [ClawHub sec-filings skill page](https://clawhub.ai/lovelaceai/sec-filings) <br>
- [Lovelace AI](https://lovelace.ai/) <br>
- [Lovelace AI Terms and Conditions](https://lovelace.ai/terms-and-conditions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples; API responses can be JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends company lookup terms to Lovelace's external SEC API.] <br>

## Skill Version(s): <br>
1.0.0-beta.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
