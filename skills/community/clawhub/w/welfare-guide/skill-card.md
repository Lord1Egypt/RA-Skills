## Description: <br>
Guides Korean welfare and government-benefit questions by routing nine benefit intents and using Welfare24, Bokjiro central-program, and local welfare API sources to produce tailored eligibility and application guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer Korean welfare, childcare, birth support, basic living, youth, senior, disability, and benefit application questions. It helps collect relevant eligibility details, identify likely central and local support programs, and present application channels with official-source cautions. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: Broad welfare triggers can cause the skill to respond outside its intended benefits domain. <br>
Mitigation: Confirm the conversation is about welfare benefits before collecting details or giving eligibility guidance. <br>
Risk: Benefit eligibility questions may involve personal details such as location, household size, income, disability, pregnancy, or age. <br>
Mitigation: Ask only for details needed for the current benefit search and remind users that final eligibility is decided by the responsible agency. <br>
Risk: The skill may use a data.go.kr API key and future helper scripts for official data access. <br>
Mitigation: Limit the API key to the required public-data services and inspect helper shell scripts before allowing them to run. <br>
Risk: Welfare policies, amounts, and local programs change over time. <br>
Mitigation: State the applicable year, prefer official sources such as Bokjiro, Government24, the Ministry of Health and Welfare, and local offices, and direct users to verify current terms before applying. <br>


## Reference(s): <br>
- [Intent Router](references/intent_router.md) <br>
- [Output Templates](references/output_templates.md) <br>
- [Source Tiers](references/source_tiers.md) <br>
- [Welfare Guide Playbook](playbook.md) <br>
- [Bokjiro Central Programs API](https://www.data.go.kr/data/15090532/openapi.do) <br>
- [Bokjiro Local Welfare API](https://www.data.go.kr/data/15108347/openapi.do) <br>
- [Subsidy24 API](https://www.data.go.kr/data/15113968/openapi.do) <br>
- [Bokjiro](https://www.bokjiro.go.kr) <br>
- [Government24](https://www.gov.kr) <br>
- [Ministry of Health and Welfare](https://www.mohw.go.kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, short question prompts, citations, disclaimers, and occasional bash setup snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flash responses are always produced; deep-dive responses are used when requested or for higher-detail benefit-search and basic-living intents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
