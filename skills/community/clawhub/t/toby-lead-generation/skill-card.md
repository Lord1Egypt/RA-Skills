## Description: <br>
Lead Generation finds high-intent buyers in live Twitter, Instagram, and Reddit conversations, researches a product, generates targeted search queries, and discovers people actively looking for relevant solutions through SkillBoss API Hub search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, marketing, and customer-discovery users use this skill to find and prioritize prospects who show buyer intent, competitor frustration, or solution-seeking behavior in public social conversations. The workflow produces scored leads and draft outreach for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated product profiles and prospecting queries may reveal sensitive product, customer, or roadmap details to SkillBoss. <br>
Mitigation: Review the product profile before searches run and avoid including sensitive customer, roadmap, or confidential business details. <br>
Risk: Lead-generation files may contain personal identifiers or social-post data. <br>
Mitigation: Protect or periodically delete files under data/lead-generation when they contain personal identifiers or prospecting data. <br>
Risk: Draft outreach may be inaccurate or may omit appropriate affiliation disclosure if sent without review. <br>
Mitigation: Have the user review and send outreach manually, and keep the affiliation disclosure included in the draft workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/toby-lead-generation) <br>
- [Publisher profile](https://clawhub.ai/user/kirkraman) <br>
- [SkillBoss](https://skillbossai.com) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API Calls, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON lead/profile files, Python API-call examples, scored lead records, and outreach drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and network access to api.skillbossai.com; stores product profiles, search queries, and deduplication data under data/lead-generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
