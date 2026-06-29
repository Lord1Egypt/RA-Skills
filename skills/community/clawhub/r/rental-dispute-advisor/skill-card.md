## Description: <br>
处理中国租房押金不退、房东扣押金、提前退租、中介费、维修责任、涨租和退租争议；输出事实清单、证据包、赔偿估算、催告函、12315/住建委投诉路径和协商话术。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize China rental-dispute facts, assess deposit and lease issues, prepare evidence, estimate disputed amounts, draft Chinese demand or complaint text, and plan negotiation or escalation steps. It is informational guidance and should be checked against current local rules and qualified legal advice for important matters. <br>

### Deployment Geography for Use: <br>
Global; content is focused on rental disputes in China. <br>

## Known Risks and Mitigations: <br>
Risk: The bundled shell script has a local code-execution risk when crafted user-supplied filenames are embedded into Python commands. <br>
Mitigation: Use only trusted case files with ordinary filenames and paths, avoid files supplied by other parties, and review or sandbox the script before running it on sensitive materials. <br>
Risk: Rental-dispute inputs can contain sensitive identity, payment, account, and private chat information. <br>
Mitigation: Redact ID numbers, account details, and unrelated chat content before use, and store case files only in trusted local directories. <br>
Risk: Generated letters, filings, and legal analyses may be incomplete or inaccurate for a specific city or current rule set. <br>
Mitigation: Treat outputs as drafts and verify facts, local rules, deadlines, and legal strategy with local authorities or a licensed lawyer before relying on them. <br>


## Reference(s): <br>
- [Deposit Dispute Playbook](references/deposit-dispute-playbook.md) <br>
- [Input Schema](schemas/input.schema.json) <br>
- [Output Schema](schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown and structured text, with optional JSON input and output schemas for the bundled CLI workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces initial risk labels, missing-fact lists, evidence packages, compensation estimates, demand letters, complaint packages, negotiation scripts, and escalation timelines.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
