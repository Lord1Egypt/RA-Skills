## Description: <br>
Generates iOS26 liquid glass style multi-page travel websites from travel plans. Invoke when user wants to create a travel website, trip planner page, or provides detailed travel itinerary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dustink66](https://clawhub.ai/user/dustink66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a detailed travel itinerary into a static multi-page trip website with itinerary, preparation, notes, and budget pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trip pages may expose private itinerary details if published publicly. <br>
Mitigation: Review generated pages before publishing and remove private trip details, secrets, or sensitive personal information. <br>
Risk: User-provided itinerary text or inserted SVG/HTML content could create misleading or unsafe page content. <br>
Mitigation: Inspect generated HTML and embedded markup before deployment, especially when source itinerary content comes from an untrusted party. <br>
Risk: Generated content defaults to Chinese unless the user asks otherwise. <br>
Mitigation: Specify the desired language during generation and review the generated copy for the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dustink66/trip-website-generator) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Generated HTML, CSS, and JavaScript files with Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a static website directory with itinerary, preparation checklist, notes, budget, shared styles, and shared JavaScript.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
