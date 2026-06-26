## Description: <br>
Find things to do in New York City this week. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkirby](https://clawhub.ai/user/zkirby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an agent for timely, interest-aware recommendations for events in and around New York City. The agent checks public event sources, verifies current schedule details, and returns event options with venue, time, cost, transit, description, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Event schedules, prices, sold-out status, accessibility details, and ticket links can change on third-party event websites. <br>
Mitigation: Verify dates, prices, availability, accessibility details, and booking links against the current event page before making plans or purchases. <br>
Risk: The skill expects the agent to visit third-party event and ticketing websites using curl or Puppeteer. <br>
Mitigation: Treat visited sites as external sources and avoid entering private, account, or payment information unless the user independently confirms the site and action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkirby/this-week-in-nyc) <br>
- [Anthology Film Archives calendar](https://www.anthologyfilmarchives.org/film_screenings/calendar) <br>
- [Metrograph](https://metrograph.com/) <br>
- [Alamo Drafthouse Lower Manhattan](https://drafthouse.com/nyc/theater/lower-manhattan) <br>
- [Times Up calendar](https://times-up.org/calendar/) <br>
- [ABC No Rio events](https://www.abcnorio.org/events/events.html) <br>
- [Ars Nova upcoming events](https://arsnovanyc.com/upcoming-events/) <br>
- [Nerd Nite NYC](https://nyc.nerdnite.com/) <br>
- [New York Public Library](https://www.nypl.org/) <br>
- [Meetup NYC events](https://www.meetup.com/find/?location=us--ny--New%20York&source=EVENTS) <br>
- [The Skint](https://www.theskint.com/) <br>
- [Secret NYC things to do](https://secretnyc.co/things-to-do/) <br>
- [NYC.gov events](https://www.nyc.gov/main/events/?) <br>
- [Untapped Cities things to do](https://www.untappedcities.com/tag/things-to-do/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown event recommendations with dates, venues, locations, costs, descriptions, transit notes, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct event, RSVP, or ticketing links from third-party websites.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
