## Description: <br>
Plan Switzerland trips with Alpine rail and mountain logistics, verified entry rules, scenic routing, and practical local execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan Switzerland trips with practical routing, entry, transport, seasonal, budget, accessibility, and safety guidance. It is intended for travel-planning conversations that need operational decisions rather than general destination inspiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep local trip notes in ~/switzerland/ for continuity. <br>
Mitigation: Use local memory only for ongoing Switzerland planning, avoid storing passport numbers, payment details, or other highly sensitive information, and review or delete ~/switzerland/memory.md when the trip is over. <br>
Risk: Travel, entry, weather, mountain, and transport information can change after the source material was checked. <br>
Mitigation: Verify time-sensitive entry rules, EES or ETIAS status, rail schedules, lift operations, weather, avalanche conditions, and road or pass closures against current official sources before booking or departure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/switzerland) <br>
- [Skill homepage](https://clawic.com/skills/switzerland) <br>
- [Swiss State Secretariat for Migration entry overview](https://www.sem.admin.ch/sem/en/home/themen/einreise.html) <br>
- [Swiss Federal Railways](https://www.sbb.ch/en) <br>
- [MeteoSwiss](https://www.meteoswiss.admin.ch/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown travel-planning guidance with structured recommendations and optional local trip notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain lightweight local trip context in ~/switzerland/ when continuity is useful and the user wants ongoing planning.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
