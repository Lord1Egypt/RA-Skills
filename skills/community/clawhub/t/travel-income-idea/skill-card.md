## Description: <br>
Helps users discover travel income ideas by matching travel goals, skills, budget, timing, estimated earnings, risks, and execution steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuxin-wenxiang](https://clawhub.ai/user/chuxin-wenxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to explore ways to offset travel costs through event-related work, skills-based services, content creation, proxy purchasing, resource sharing, or seasonal work. It produces advisory opportunity recommendations, earnings estimates, risk notes, and step-by-step execution plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel-income recommendations can involve legal, tax, customs, venue, platform, work-authorization, or privacy obligations. <br>
Mitigation: Treat outputs as advisory and verify applicable laws, venue rules, platform policies, work authorization, tax/customs obligations, and privacy consent before acting. <br>
Risk: The artifact includes guidance for database writes, source-code edits, booking features, and third-party search or redirect behavior outside the core idea-generation scope. <br>
Mitigation: Require explicit operator approval before database writes, source-code edits, third-party searches, or booking-link generation; review generated changes and destination URLs before deployment. <br>
Risk: Estimated earnings, costs, availability, and success rates may be inaccurate or outdated. <br>
Mitigation: Validate prices, demand, event details, competition, costs, and expected income against current sources before relying on a plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuxin-wenxiang/travel-income-idea) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code, configuration] <br>
**Output Format:** [Markdown responses with structured recommendations, earnings estimates, task lists, risk notes, and occasional code or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory outputs may include projected income, budgets, booking links, database-update guidance, and implementation notes that require human review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
