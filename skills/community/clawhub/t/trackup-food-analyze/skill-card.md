## Description: <br>
Analyze a food image with AISpark TrackUp production APIs, using AnalyzeWholeFood for full analysis and dedicated endpoints for macros, ingredients, health insight, and keyword-based food search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trackup](https://clawhub.ai/user/trackup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route food image analysis or keyword lookup requests to AISpark TrackUp APIs and return nutrition, ingredient, glycemic index, and health insight data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected food images, image URLs, base64 image data, and food-search keywords are sent to deepeat.ai for processing. <br>
Mitigation: Use only images and keywords appropriate for third-party processing, and avoid private or identifying photos unless that processing is acceptable. <br>
Risk: Local image workflows can create temporary base64 and JSON payload files under /tmp. <br>
Mitigation: Delete temporary payload files after use when the source image or analysis request is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trackup/trackup-food-analyze) <br>
- [AISpark TrackUp API host](https://deepeat.ai) <br>
- [AnalyzeWholeFood endpoint](https://deepeat.ai/step.aispark.api.API/AnalyzeWholeFood) <br>
- [SearchFood endpoint](https://deepeat.ai/step.aispark.api.API/SearchFood) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and optional bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Numeric values should be preserved exactly as returned, and missing fields should not be invented.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
