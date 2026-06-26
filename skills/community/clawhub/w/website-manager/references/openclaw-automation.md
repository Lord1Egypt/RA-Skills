# OpenClaw Automation Patterns

Use this file when recurring website upkeep should run in OpenClaw.

Cron is the built-in OpenClaw scheduler. Prefer it when available.

## Weekly SEO audit

```bash
openclaw cron add \
  --name "Weekly website SEO audit" \
  --cron "0 9 * * 1" \
  --tz "America/Toronto" \
  --session isolated \
  --message "Review the website for broken links, missing metadata, weak internal links, stale schema, and pages that need content refresh. Summarize findings with priorities and recommended fixes." \
  --announce
```

## Daily publish queue

```bash
openclaw cron add \
  --name "Daily website publish queue" \
  --cron "0 8 * * *" \
  --tz "America/Toronto" \
  --session isolated \
  --message "Check the Notion website CMS for records marked Ready or Needs Update, identify what should be rebuilt, and prepare a concise publish plan." \
  --announce
```

## Monthly content health review

```bash
openclaw cron add \
  --name "Monthly content health review" \
  --cron "0 10 1 * *" \
  --tz "America/Toronto" \
  --session isolated \
  --message "Review the website's pages, collections, blog categories, filters, and search experiences for stale content, thin SEO coverage, missing internal links, and poor empty-state behavior. Recommend the highest-impact updates." \
  --announce
```

If OpenClaw is not available, use an equivalent scheduler such as GitHub Actions, provider cron, or system cron.
