## Description: <br>
Helps an agent plan trips by gathering Chinese social-platform travel signals, scoring attractions, prioritizing activities, surfacing pitfalls, and preparing travel-guide PPT content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongji921](https://clawhub.ai/user/yongji921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to research a destination, compare attraction recommendations, organize warnings and priorities, and draft a travel-guide presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip recommendations may be inaccurate, incomplete, or stale if the agent does not show current sources or if helper scripts are used without live search results. <br>
Mitigation: Review cited sources and verify opening hours, prices, crowd levels, and safety details before relying on the itinerary. <br>
Risk: The helper scripts can create local output files and may use example or mock data when no verified attraction data is supplied. <br>
Mitigation: Inspect generated JSON or PPT content before sharing and label draft content until it is backed by current travel sources. <br>


## Reference(s): <br>
- [Scoring criteria](artifact/references/scoring-criteria.md) <br>
- [ClawHub release page](https://clawhub.ai/yongji921/travel-planner-case) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and structured JSON or PPT content files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a generated PPT file path, itinerary highlights, attraction scores, activity priorities, and travel warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
