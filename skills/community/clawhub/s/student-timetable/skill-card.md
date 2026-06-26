## Description: <br>
Student timetable manager for self or parent-managed child profiles, including an init flow and a profile registry under schedules/profiles/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users such as students and parents or guardians use this skill to initialize local profile-based timetable data and query today, tomorrow, this week, or next week schedules for a selected profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student or child timetable details are stored locally under schedules/profiles. <br>
Mitigation: Use the skill only in workspaces where local storage of student schedule details is acceptable, and review profile files before sharing or publishing the workspace. <br>
Risk: Academic calendar import can share school and location search terms with a search or fetch provider. <br>
Mitigation: Use academic calendar import only when that sharing is acceptable, and verify imported dates against official school notices before relying on them. <br>
Risk: Wake keywords persist in the profile registry and can affect future timetable routing. <br>
Mitigation: Review configured wake keywords during setup and remove or revise terms that are too broad or sensitive. <br>


## Reference(s): <br>
- [Student Timetable ClawHub listing](https://clawhub.ai/extraterrest/student-timetable) <br>
- [README](artifact/README.md) <br>
- [StudentTimetable Schema v2](artifact/schema_v2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text schedule summaries, JSON migration reports, CLI command guidance, and local schedule/profile configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists timetable profiles locally under schedules/profiles and may use web search/fetch for supported academic calendar imports.] <br>

## Skill Version(s): <br>
0.1.0-alpha.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
