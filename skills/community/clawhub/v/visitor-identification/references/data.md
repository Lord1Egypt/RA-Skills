# What the rows mean

## The two models

- **`website_visiting_companies`**: one row per organisation Snitcher resolved from a visit's IP
  address. Website, industry, and first and last seen. A row is a company, not a person: a visit
  from a shared office network, a VPN or a coworking space resolves to whoever owns the address.
- **`website_visitor_sessions`**: one row per visit by an identified company. The organisation's
  UUID, when the session started, the referrer and the pages viewed. Join it to the companies
  model on `organisation_uuid = uuid`.

Both fetch incrementally on Cargo's own interval and refuse a cron. The first rows can take a sync
interval after the first accepted visit.

## Reading a count

- **Zero is a valid answer.** Visitors who reject tracking send nothing, and many IP addresses do
  not resolve to an organisation (home broadband, mobile networks). Report a zero as a zero; never
  insert rows to show the pipeline works.
- **Only accepted visits count.** The models undercount real traffic by every visitor who rejects
  or sends Global Privacy Control. Say so next to any number.
- **A company is not a buyer.** A visit says someone on that network read those pages. Anything
  that acts on it, a score, an alert, an email, has to say it is about the company.

## Query it

```sql
SELECT c.website, c.industry, COUNT(s.uuid) AS sessions, MAX(s.started_at) AS last_visit
FROM snitcher.website_visiting_companies c
JOIN snitcher.website_visitor_sessions s ON s.organisation_uuid = c.uuid
GROUP BY c.website, c.industry
ORDER BY last_visit DESC
```

Check the real column names with `cargo-ai storage column list` against the live models before
relying on this; the extractor owns them.

## Stopping it

- **Stop browser collection:** remove the env token from the app (or set the site back to
  `draft`) and deploy. The export then carries no profile ID.
- **Stop billing:** remove the companies model through a reviewed plan. Removing it can deactivate
  the provisioned Snitcher workspace; export what you need first.
