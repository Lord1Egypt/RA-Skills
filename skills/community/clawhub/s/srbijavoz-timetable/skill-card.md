## Description: <br>
Check official Srbija Voz notices, station matches, and timetable metadata for live train delays, cancellations, stoppages, operational changes, and replacement bus service in Serbia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomashevic](https://clawhub.ai/user/atomashevic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check public Srbija Voz passenger notices, resolve station names, and distinguish live disruptions from recurring timetable information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts official Srbija Voz public websites, so lookup results depend on those services being reachable and current. <br>
Mitigation: Report endpoint failures clearly, use the documented fallback only for passive timetable metadata, and include notice dates or source links when relevant. <br>
Risk: The bundled lookup script saves results to a JSON file in the current working directory by default. <br>
Mitigation: Run it in an appropriate working directory or provide an explicit output path with --out. <br>
Risk: Transit notices can be incomplete, delayed, or represent recurring timetable information rather than a fresh disruption. <br>
Mitigation: Separate live notices from recurring timetable notices and avoid claiming a current disruption unless the official notice supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atomashevic/srbijavoz-timetable) <br>
- [Srbija Voz public notices API](https://www.srbvoz.rs/wp-json/wp/v2/info_post?per_page=100) <br>
- [Srbija Voz station autocomplete API](https://w3.srbvoz.rs/redvoznje/api/stanica/) <br>
- [Srbija Voz timetable metadata page](https://w3.srbvoz.rs/redvoznje/info/sr) <br>
- [Srbija Voz timetable page](https://www.srbvoz.rs/redvoznje) <br>
- [Srbija Voz keyword cues](references/keyword-cues.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown passenger summaries with optional shell commands and JSON lookup output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes srbvoz_notices.json by default unless a different output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
