## Description: <br>
Racing Quant AI helps agents query an A-share quantitative strategy database, retrieve strategy holdings, and produce structured stock analysis reports with data-source notes and investment-risk disclaimers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for investment research workflows that match user preferences to quantitative A-share strategies, retrieve holdings, and generate multi-factor stock analysis reports. Outputs should be treated as research material, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact publishes reusable credentials for a remote MySQL strategy database. <br>
Mitigation: Install only after trusting the publisher, treat the password as exposed, and verify the database account is read-only and intended for public access. <br>
Risk: The skill can contact a remote database and external search services during analysis. <br>
Mitigation: Review network access before use and avoid sending confidential prompts, strategy names, or portfolio details through this workflow. <br>
Risk: A bundled helper can present simulated holdings or fallback research as analysis. <br>
Mitigation: Require reports to label data sources clearly and independently verify holdings, prices, financial metrics, and research claims before relying on the output. <br>
Risk: Financial analysis output may be mistaken for investment advice. <br>
Mitigation: Keep the skill's disclaimer in final reports and route outputs through appropriate financial review before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenxyzcyxpp/racing-quant-ai) <br>
- [Publisher profile](https://clawhub.ai/user/chenxyzcyxpp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, source notes, disclaimers, and optional shell commands for bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include strategy metadata, holdings tables, stock analysis, source annotations, and explicit non-advice disclaimers.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence and artifact listing) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
