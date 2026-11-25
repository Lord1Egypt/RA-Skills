# Safe Local-Only Mode Checklist

## Mode Declaration

- External connectors disabled:
- Approved local roots:
- Pasted or exported LinkedIn content:
- Local Git or project notes:
- Local job postings:
- Third-party uploads disabled:

## Allowed Sources

| Source | Approved Scope | Status | Notes |
| --- | --- | --- | --- |
| Local documents |  |  |  |
| Pasted LinkedIn export |  |  |  |
| Local Git exports |  |  |  |
| Local job posting text |  |  |  |

## Disabled Or Unavailable Sources

| Tool Or Source | Reason | Fallback |
| --- | --- | --- |
| GitHub connector |  | Public links, local exports, or pasted summaries |
| GitHub Enterprise |  | Local export or manual summary |
| Jira |  | Exported issues or manual summary |
| Confluence |  | Exported pages or manual summary |
| LinkedIn web access | Not used by default | Export, pasted profile, or notes |
| Canva/Figma upload | Approval required | HTML/PDF and handoff notes |

## Safety Checks

- Generated outputs stay under `resume-runs/`:
- Credentials were not requested or stored:
- Private names are sanitized by default:
- Tool limitations recorded in `tool-usage-log.md`:
- Missing evidence recorded in `missing-information-loop.md`:
