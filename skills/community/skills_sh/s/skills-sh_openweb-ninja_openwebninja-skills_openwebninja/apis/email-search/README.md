# email-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/email_search.yaml

**Host:** `email-search16.p.rapidapi.com`
**Notes:** Single call returns up to 5000 emails. Use 'limit' param to cap results.

## Endpoints

### GET /search-emails
Search Emails — Search the web for emails using a query and email domain and get up to 5,000 email addresses.

**Required:**
- `query` (string) Example: `Car Dealer California USA`
- `email_domain` (string) — Email domain  typically a company domain (e.g. `wsgr.com`) or an email provider domain (e.g. `gmail.com`). Example: `gmail.com`

**Optional:**
- `limit` (number, default: 5000) Example: `100`

**Pagination:** none
**Page size param:** `limit` (default: 5000)

---
