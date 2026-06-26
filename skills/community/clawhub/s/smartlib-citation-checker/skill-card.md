## Description: <br>
Checks academic references from manuscripts or AI-generated citation lists against SmartLib services and produces an HTML report with authenticity results, corrections, verification links, and citation analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, editors, reviewers, and students use this skill to verify whether cited papers exist, catch AI-hallucinated references, compare citation fields against database records, and export corrected citations before submission or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference lists or manuscript-derived citation text may be sent to SmartLib/Gateway services. <br>
Mitigation: Use the skill only for content appropriate for those services, avoid unpublished sensitive manuscripts unless necessary, and prefer a dedicated SmartLib email/account. <br>
Risk: The skill links citation checking to a shared SmartLib email and quota account. <br>
Mitigation: Confirm the account to be used before running checks and monitor quota consumption for each batch of references. <br>
Risk: Payment flows may create orders, and the artifact contains inconsistent consent and paywall instructions. <br>
Mitigation: Require explicit user confirmation before starting any recharge or purchase flow and review displayed plan, amount, quota, and order details. <br>
Risk: Corrected citations and authenticity results may still be wrong or incomplete. <br>
Mitigation: Verify important corrected citations manually against source databases or publisher records before using them in submitted work. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/j-levee/smartlib-citation-checker) <br>
- [SmartLib homepage](https://www.vipslib.com) <br>
- [Paper draft verification sample report](examples/citation_check_paper_draft_sample.html) <br>
- [AI hallucination citation sample report](examples/citation_check_ai_hallucination_sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, files, guidance] <br>
**Output Format:** [HTML report with textual summaries, citation corrections, verification links, statistics, and quota or payment guidance when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SmartLib/Gateway connectivity and configured gateway credentials; citation results should be manually reviewed before relying on corrected references.] <br>

## Skill Version(s): <br>
3.6.0 (source: server release evidence; artifact frontmatter reports 3.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
