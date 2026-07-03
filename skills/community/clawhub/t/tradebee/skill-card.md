## Description: <br>
小蜜蜂数字营销 maps explicit Tradebee Website Builder requests to API actions for content, product, inquiry, visitor, keyword ranking, language, and HTML-rule operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxiaming](https://clawhub.ai/user/mouxiaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Tradebee site operators and their agents use this skill to manage Tradebee Website Builder data, including blogs, FAQs, custom pages, products, groups, inquiries, recent visitors, keyword rankings, enabled languages, and tenant HTML rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Tradebee website content and product data. <br>
Mitigation: Review each create, update, and delete confirmation carefully, and require an explicit Tradebee object type plus record ID or confirmed ID list for update and delete actions. <br>
Risk: The skill sends site and business data to the external Tradebee Website Builder API using BEE_API_KEY. <br>
Mitigation: Install only from a trusted publisher, configure BEE_API_KEY as an environment variable, and send only the minimum data needed for the stated Tradebee task. <br>
Risk: Update actions write local backup JSON files that may contain business content or personal data. <br>
Mitigation: Secure or delete backup files after they are no longer needed, and avoid retaining more visitor telemetry than the user task requires. <br>
Risk: Generated HTML fragments can drift from tenant requirements if rules are guessed. <br>
Mitigation: Call rule-get with the exact language and scene first, then follow the returned rule payload instead of generating fragments from assumptions. <br>


## Reference(s): <br>
- [Tradebee Open API homepage](https://open.tradew.com) <br>
- [ClawHub skill page](https://clawhub.ai/mouxiaming/skills/tradebee) <br>
- [Publisher profile](https://clawhub.ai/user/mouxiaming) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown summaries and JSON API responses, with local JSON backup files for update actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BEE_API_KEY. Update actions read the current record and write a backup under backups/<action>/ before sending the update request.] <br>

## Skill Version(s): <br>
26.6.26 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
