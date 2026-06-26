## Description: <br>
ToB销售提案生成器。输入客户信息/行业/痛点/产品，基于知识库真实案例输出带品牌色CSS的4模块HTML分页提案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william202404](https://clawhub.ai/user/william202404) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales and presales teams use this skill to turn customer, industry, pain point, product, budget, and timeline inputs into a four-section HTML sales proposal. The generated proposal aligns pains, solution value, implementation plan, and ROI with examples from the bundled case library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated proposals can include customer names, budgets, and pain points that may be sensitive if copied into external AI or presentation services. <br>
Mitigation: Review and redact sensitive customer information before sharing or pasting the generated proposal outside the trusted environment. <br>
Risk: The tool writes an HTML proposal to the selected output path and could overwrite an existing file. <br>
Mitigation: Choose a fresh output path, such as a new proposal.html, before generation. <br>
Risk: Sales proposal content may contain incorrect or misleading business claims if accepted without review. <br>
Mitigation: Review the generated proposal, case references, ROI assumptions, and customer-specific claims before using it with customers. <br>
Risk: Dependency changes can alter runtime behavior. <br>
Mitigation: Install from the reviewed package and prefer deterministic installs using the included lockfile. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william202404/tob-sales-proposal) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [HTML file with embedded CSS and proposal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a proposal HTML file, defaulting to ./proposal.html unless an output path is provided.] <br>

## Skill Version(s): <br>
1.2.0 (source: package.json and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
