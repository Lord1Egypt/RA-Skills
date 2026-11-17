## Description:

Check official Srbija Voz notices, station matches, and timetable metadata when verifying live train delays, cancellations, stoppages, or replacement bus service in Serbia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomashevic](https://clawhub.ai/user/atomashevic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to check public Srbija Voz passenger notices, resolve station names, and distinguish live disruptions from recurring timetable information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled lookup script contacts public Srbija Voz websites and may fail or return incomplete information if those public endpoints are unavailable or change.

Mitigation: Treat answers as public transit-status summaries, preserve source notice details where relevant, and state when the official public endpoints were unavailable.

Risk: The skill saves lookup results to a local JSON file when the bundled script is run.

Mitigation: Use the default output only for public transit information and choose an appropriate output path when local files need to be managed.

Risk: A recurring Petrovaradin corridor bus notice can be mistaken for a fresh disruption.

Mitigation: Classify that notice as timetable information unless the source notice explicitly says the bus service changed, stopped, or was canceled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atomashevic/skills/srbijavoz-timetable)
- [Srbija Voz public notices API](https://www.srbvoz.rs/wp-json/wp/v2/info_post?per_page=100)
- [Srbija Voz station autocomplete API](https://w3.srbvoz.rs/redvoznje/api/stanica/)
- [Srbija Voz timetable metadata page](https://w3.srbvoz.rs/redvoznje/info/sr)
- [Srbija Voz timetable page](https://www.srbvoz.rs/redvoznje)
- [Srbija Voz keyword cues](references/keyword-cues.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise Markdown or plain text summaries, with JSON produced by the bundled lookup script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save public notice lookup results to a local JSON file when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
