# Sant'Anna Pisa Monitor

OpenClaw skill for monitoring job postings, admissions, PhD programs, and courses from the **Scuola Superiore Sant'Anna** in Pisa, Italy.

## What It Does

Automatically tracks and extracts information from the university website:

- **Job postings** — Research contracts, postdoc positions, teaching roles, technical/administrative staff
- **PhD admissions** — Open positions (fully funded, no tuition), application deadlines, special deadlines
- **Degree program admissions** — Bachelor (I livello) and Master (II livello) entrance exam deadlines
- **Seasonal Schools** — Short intensive courses (~36 per academic year) with dates and application deadlines
- **University Master programs** — 1st and 2nd level Master degree programs

## Features

- Zero API keys required — uses the university's public website
- Parses 8 key pages for complete coverage
- Filters job postings by 11 categories (staff type, role, etc.)
- Tracks ~36 Seasonal School courses per year
- Standardized report output format
- Ready for scheduled monitoring via cronjob or agent loop

## Install

```
clawhub install FabioBaroni/santanna-pisa-monitor-skill
```

## Usage

### One-shot check

Load the skill, then ask your agent to check the Sant'Anna website for whatever you care about:

```
Check Sant'Anna Pisa for new job postings in AI
What are the upcoming PhD application deadlines?
Which Seasonal Schools are coming up in the next month?
```

### Scheduled monitoring

Set up a recurring check that summarizes any new opportunities:

```
Every day at 9am, load the santanna-pisa skill, navigate all 8 key pages described in the workflow, extract any new postings or upcoming deadlines, and report only what's changed since last check.
```

## Pages Monitored

| Category | Pages | Content |
|----------|-------|---------|
| Jobs | 4 pages | Active postings, expiring deadlines, 11 role categories |
| PhD Admissions | 2 pages | Open positions, general + special deadlines |
| Degree Programs | 3 pages | Bachelor/Master entrance exam deadlines |
| Seasonal School | 2 pages | ~36 short courses with dates per academic year |

## Notes

- The Sant'Anna website is Drupal-based with server-side rendering
- URLs for PDFs and specific pages change annually — the skill uses stable hub pages
- Seasonal School pages have a multi-column layout that requires scrolling to capture all courses
- No official RSS feeds exist — monitoring is done via browser automation

## License

MIT-0

## Author

Baroni Fabio
