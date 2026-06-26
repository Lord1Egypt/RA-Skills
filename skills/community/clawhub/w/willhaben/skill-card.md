## Description: <br>
Create and manage Willhaben.at listings for the Austrian marketplace by helping draft titles, descriptions, prices, photo uploads, and supervised browser posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benjaminorthner](https://clawhub.ai/user/benjaminorthner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and marketplace sellers use this skill to draft German Willhaben listings, research comparable prices, prepare listing details, upload photos, and publish through a supervised signed-in browser session. <br>

### Deployment Geography for Use: <br>
Austria <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a signed-in Willhaben browser session and publish marketplace listings. <br>
Mitigation: Review the listing text, price, photos, location, contact details, package size, and shipping choices before allowing publication. <br>
Risk: Paid promotion options may appear during the Willhaben posting flow. <br>
Mitigation: Confirm paid promotion options remain unselected and the total remains zero before publishing. <br>
Risk: Local preference files may store location, shipping, pricing, and selling preferences for reuse. <br>
Mitigation: Review or delete config/user-preferences.json when those local preferences should not be retained. <br>


## Reference(s): <br>
- [Willhaben Setup](references/SETUP.md) <br>
- [Willhaben Categories](references/categories.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/benjaminorthner/willhaben) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown listing drafts, browser-action guidance, and JSON preference configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces German listing copy, price recommendations, shipping/package-size suggestions, and supervised publishing steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
