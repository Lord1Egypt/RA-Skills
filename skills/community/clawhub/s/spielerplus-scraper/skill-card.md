## Description: <br>
Scraper for SpielerPlus/TeamPlus team management platform. Extracts events, members, absences, finances, participation stats, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firstsanny](https://clawhub.ai/user/firstsanny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and authorized team administrators use this skill to collect SpielerPlus/TeamPlus team information such as events, members, absences, finances, participation, roles, and full reports through CLI or programmatic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-provided SpielerPlus credentials and can access team data. <br>
Mitigation: Install only for authorized teams, use a dedicated or least-privilege account where possible, and keep SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD out of commits, screenshots, CI logs, and shell history. <br>
Risk: Exported or console-printed member, absence, participation, role, and finance data may be sensitive. <br>
Mitigation: Treat generated outputs as sensitive data and limit storage, sharing, and logging to authorized users and systems. <br>
Risk: Browser automation depends on Playwright and Chromium runtime components. <br>
Mitigation: Prefer updating or locking Playwright to a patched release before running browser installs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/firstsanny/spielerplus-scraper) <br>
- [SpielerPlus/TeamPlus platform](https://www.spielerplus.de) <br>
- [npm package listing](https://www.npmjs.com/package/spielerplus-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text or JSON data, with JavaScript API usage guidance and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD for authentication; outputs may include sensitive team member, absence, participation, role, and finance data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
