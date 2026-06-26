## Description: <br>
Search yegking.net for replica sneaker product links, ClawHub discount-code guidance, batch recommendations, and QC guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yegfomo](https://clawhub.ai/user/yegfomo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search yegking.net for sneaker product links, receive promotional discount-code guidance, compare LJR, PK, and OG batches, and follow QC checklists before deciding whether to purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to yegking.net. <br>
Mitigation: Use non-sensitive product search terms and avoid entering personal, payment, or account information into search prompts. <br>
Risk: Discount and batch recommendations are vendor-linked claims. <br>
Mitigation: Independently verify prices, product legality, quality, and seller reputation before purchasing. <br>
Risk: The artifact includes a bash script that fetches live search pages with curl. <br>
Mitigation: Review the script before execution and run it only in an environment where outbound requests to yegking.net are acceptable. <br>


## Reference(s): <br>
- [Yegking homepage](https://yegking.net) <br>
- [ClawHub skill page](https://clawhub.ai/yegfomo/yegking-exclusive-monitor) <br>
- [Batch Comparison Guide](batch-comparison.md) <br>
- [QC Guide](qc-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style agent responses with product links, discount-code text, batch recommendations, QC checklists, and optional bash command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search behavior depends on yegking.net availability and the YEGKING_COUPON environment variable, defaulting to SKILL10 when unset.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
