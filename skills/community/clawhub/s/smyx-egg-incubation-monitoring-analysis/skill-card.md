## Description: <br>
Analyzes fixed-camera or candling images of turtle and snake eggs to classify visual development signals, estimate incubation stage, and produce incubation progress reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Reptile breeders, hatchery operators, and hobbyists use this skill to review turtle or snake egg images, track fertilization and embryo-development signals, and receive non-invasive monitoring guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected media or URLs to a remote service and uses a user identifier for cloud report history. <br>
Mitigation: Install only when the publisher and remote service are trusted, avoid personal media or phone-number-style identifiers unless account linkage is intentional, and disclose the remote processing path to users. <br>
Risk: Security evidence reports under-disclosed account, token persistence, broad backend API, and device-deletion capabilities beyond simple image analysis. <br>
Mitigation: Review the skill before deployment, inspect configuration and local persistence behavior, and run it only in environments where those account and API capabilities are acceptable. <br>
Risk: Incorrect visual incubation classifications could lead to poor handling decisions for eggs. <br>
Mitigation: Treat outputs as monitoring support only, confirm important decisions against species incubation guidance and expert review, and avoid invasive actions or autonomous incubator changes. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report or JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include egg identifiers, incubation dates, visual signal classifications, alert level, recommended non-invasive actions, and disclaimers.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
