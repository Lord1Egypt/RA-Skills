## Description:

Drive the browser the user is already signed into, instead of a cold automation profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to work with pages that require an existing signed-in browser session, including dashboards, admin consoles, internal tools, ticket queues, webmail, billing pages, and rendered application inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected clients can control the user's signed-in browser and act inside real accounts.

Mitigation: Use only when a signed-in session is necessary, read page state before acting, confirm irreversible actions, and keep the approval gate enabled.

Risk: The setup path can use npx or a global npm install for the bridge package.

Mitigation: Verify or pin the bridge package before installation and before registering the native messaging host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t3ratech/skills/t3rnel-signed-in-browser)
- [T3rnel Browser documentation](https://t3ratech.github.io/t3rnel-browser-plugin/)
- [T3rnel Browser tools documentation](https://t3ratech.github.io/t3rnel-browser-plugin/tools.html)
- [Chrome Web Store extension](https://chromewebstore.google.com/detail/egpckhdpkoeimoekciejbmbbcackhdmd)
- [Microsoft Edge Add-ons extension](https://microsoftedge.microsoft.com/addons/detail/t3rnel-browser/dnplmolfblplbeclnglmjamppekpbcjo)
- [Firefox Add-ons extension](https://addons.mozilla.org/en-US/firefox/addon/t3rnel-browser/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs use of local session tools and browser-extension setup; no fixed token or artifact post-processing constraints.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
