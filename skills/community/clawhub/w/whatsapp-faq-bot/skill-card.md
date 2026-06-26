## Description: <br>
Build and query a searchable FAQ knowledge base from markdown files for WhatsApp business FAQ workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and business operators use this skill to maintain a local FAQ knowledge base, search it for likely answers, and support WhatsApp assistant workflows with reusable responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported FAQ content may be inaccurate, outdated, or inappropriate if the markdown source is untrusted. <br>
Mitigation: Import only trusted FAQ sources and review entries before using the answers in customer-facing workflows. <br>
Risk: FAQ content is stored locally and exports can write files to requested paths. <br>
Mitigation: Use FAQ_BOT_DIR to store data in a dedicated folder and restrict where export outputs are written. <br>
Risk: Letting untrusted chat messages trigger import, export, remove, or file-path commands could alter data or access unintended local files. <br>
Mitigation: Keep file-management commands behind an operator-controlled workflow and use chat automation only for vetted search queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mariusfit/whatsapp-faq-bot) <br>
- [Publisher Profile](https://clawhub.ai/user/mariusfit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text CLI output, JSON search results and statistics, and Markdown or JSON FAQ exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores FAQ content locally under ~/.faq-bot by default; FAQ_BOT_DIR can point storage to a dedicated folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
