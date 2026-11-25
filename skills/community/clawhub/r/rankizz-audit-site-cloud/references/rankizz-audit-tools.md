# Rankizz cloud audit tools

## Required sequence

| Step | MCP tool | Purpose |
| --- | --- | --- |
| 1 | `list_projects` | Resolve the project ID without creating duplicates |
| 2 | `create_project` | Create a project only after user confirmation |
| 3 | `run_site_audit` | Start the robots-aware background crawl |
| 4 | `get_audit_status` | Poll crawl and Lighthouse progress |
| 5 | `get_audit_issues` | Read prioritized issues and `how_to_fix` guidance |
| 6 | `get_audit_pages` | Read status, title, description, word count, indexability, depth, and links per page |

Pass the same `projectId` through the workflow. Preserve the returned `auditId` rather than defaulting to the latest audit when concurrent work could exist.

## Scope controls

- `url`: start URL on the project's domain
- `pathScope`: optional section such as `/blog/*`
- `maxPages`: confirmed page budget from 1 to the account maximum
- `runLighthouse`: enable only when performance evidence is useful

## Failure handling

- Low credits: stop and link to Rankizz Billing.
- Capacity reached: tell the user to delete old audits from the dashboard before retrying.
- Blocked crawl: report affected pages and the exact user-agent allowlisting guidance returned by Rankizz.
- Partial Lighthouse failure: keep valid crawl findings and label missing performance measurements.
- Failed audit: report the status once and do not create a replacement run without user direction.

## Optional evidence tools

Use only when required by the question:

- `get_search_console_performance`, `inspect_urls`
- `get_bing_webmaster_performance`, `get_bing_webmaster_crawl_health`, `inspect_bing_urls`
- `get_google_analytics_organic_landing_pages`, `get_google_analytics_page_insights`
- `get_domain_overview`, `get_ranked_keywords`
- `get_backlinks_overview`, `get_backlinks_profile`
- `get_serp_results`, `get_keyword_metrics`
