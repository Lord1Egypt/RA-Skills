---
name: teletalk-alljobs-govjob-search
description: Search Bangladesh government jobs from the Teletalk AllJobs API, filter out excluded keywords, present matching jobs, and track applied job IDs. Use when the user wants gov job search results from alljobs.teletalk.com.bd, wants to exclude roles by keyword, or wants to save applied government job IDs after confirmation.
---

# Teletalk AllJobs Gov Job Search

Use this skill to search and shortlist government jobs from the Teletalk AllJobs API.

## Core flow

1. Ask the user for:
   - a search keyword, such as `electrical`, `civil`, `mechanical`, `computer`, or `engineer`
   - excluded keywords, such as `Sub Assistant`, `Diploma`
2. Save the preferences in `data/preference.json`.
3. Run the search script with the keyword.
4. Show the remaining jobs with only these fields:
   - `job_title`
   - `job_title_bn`
   - `org_name`
   - `org_name_bn`
   - `vacancy`
   - `deadline_date` (show date and BST, Bangladesh Standard Time when possible)
   - `application_site_url`
   Skip any jobs whose deadline has already passed.
5. If the user confirms they applied, save the `job_primary_id` in `data/appliedJobIds.json`.

## Data files

Store skill data inside this skill folder in:
- `data/preference.json`
- `data/appliedJobIds.json`

Use this preference shape:

```json
{
  "keyboard": "",
  "excluded": ["", ""]
}
```

Note: keep the field name as `keyboard` to match the skill data format, even though it represents the search keyword.

## Confirmation behavior

When the user says they applied:
- append the `job_primary_id` to `data/appliedJobIds.json`
- avoid duplicates

## Script entry point

Use the script inside this skill folder:
- `scripts/teletalk-alljobs-search.js`

The script should:
- read `data/preference.json`
- call the Teletalk API
- filter excluded keywords
- skip jobs whose deadline has already passed
- print the compact job list as JSON

## Notes

- Keep the skill focused on Teletalk government jobs only.
- Do not mix this workflow with BDJobs skill data.
- Favor deterministic filtering over model guesses.
