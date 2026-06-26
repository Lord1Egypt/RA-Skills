## Description: <br>
Book restaurant tables on OpenTable via the browser tool, including hidden time slots and terms checkboxes, using a logged-in session with a saved card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eeshita-Pande](https://clawhub.ai/user/Eeshita-Pande) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-assistant agents use this skill to reserve restaurant tables on OpenTable through a logged-in browser session. It guides the agent through finding a restaurant, selecting date, time, party size, booking type, and completing the reservation when required account details are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can confirm real OpenTable reservations through a logged-in account with a saved card and no clear final approval step. <br>
Mitigation: Require the agent to show the exact restaurant, date, time, party size, cancellation or no-show terms, fees, and saved-card indicator before it clicks Confirm. <br>
Risk: The skill operates inside an authenticated browser session that may expose account state or saved payment availability. <br>
Mitigation: Use a dedicated browser profile for booking tasks, and log out or remove saved card access when the skill is not in use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Eeshita-Pande/restaurant-booking-opentable) <br>
- [Browser Booking JS Snippet Reference](artifact/browser-snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with browser action steps and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser.enabled and an authenticated OpenTable browser session with a saved card when completing reservations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
