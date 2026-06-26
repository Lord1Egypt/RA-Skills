## Description: <br>
Generate travel capsule-wardrobe plans with outfit formulas, packing lists, layering strategy, and visual lookbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan practical travel outfits across destinations, weather, scenes, and travelers. It produces a capsule wardrobe, daily outfit calendar, packing checklist, luggage strategy, travel reminders, and an optional visual lookbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a local HTML lookbook that may include trip details and outfit planning information. <br>
Mitigation: Review the generated HTML before sharing it and avoid including sensitive travel or identity details in lookbook content. <br>
Risk: The optional lookbook workflow can use third-party image or search services. <br>
Mitigation: Use the Pexels API key only when comfortable sending search terms to that service, and review external search links before following or sharing them. <br>


## Reference(s): <br>
- [Lookbook Guide](artifact/references/lookbook-guide.md) <br>
- [Outfit Examples](artifact/references/outfit-examples.md) <br>
- [Pexels API](https://www.pexels.com/api/) <br>
- [ClawHub Release Page](https://clawhub.ai/tinayunyunyun/travel-outfit-planner) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Chinese Markdown travel outfit plan plus generated HTML lookbook file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for lookbook generation; can use an optional Pexels API key and falls back to CSS placeholders and Xiaohongshu search links when no key is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
