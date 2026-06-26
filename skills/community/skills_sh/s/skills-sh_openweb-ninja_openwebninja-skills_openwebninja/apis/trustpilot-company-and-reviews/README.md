# trustpilot-company-and-reviews

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/trustpilot_company_and_reviews.yaml

**Host:** `trustpilot-company-and-reviews-data.p.rapidapi.com`
**Notes:** Page-based pagination. Reviews return 20 per page; pages beyond 10 require an authentication cookie. Without a cookie, reviews are capped at ~200 (10 pages x 20 reviews).

## Endpoints

### GET /company-search
Company Search — Search for companies / businesses on Trustpilot. Supports pagination and rating and review count filters.

**Required:**
- `query` (string) — Search query / keyword Example: `bestbuy`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `min_rating` (string, default: any) — values: any, 3, 4, 4.5
- `min_review_count` (string) — values: any, 25, 50, 100, 250, 500
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** page_number (param: `page`)

---

### GET /company-details
Company Details — Get the full details of a specific company by company domain.

**Required:**
- `company_domain` (string) Example: `gossby.com`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none

---

### GET /company-reviews
Company Reviews

**Required:**
- `company_domain` (string) Example: `gossby.com`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `cookie` (string)
- `verified` (boolean) — Only return verified reviews Example: `Do not include in request`
- `with_replies` (boolean) — Only return reviews with owner replies Example: `Do not include in request`
- `sort` (string, default: most_relevant) — values: most_relevant, recency
- `date_posted` (string, default: any) — values: any, last_12_months, last_6_months, last_3_months, last_30_days
- `query` (string) — Return reviews matching a specific query / keyword.
- `rating` (string) — values: 1, 2, 3, 4, 5
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** page_number (param: `page`)
**Response path:** `data` (reviews in `data.reviews[]`)

---

### GET /category-company-list
Companies by Category

**Required:**
- `category_id` (string) Example: `software_company`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `min_rating` (string, default: any) — values: any, 3, 4, 4.5
- `verified` (boolean, default: false) Example: `Do not include in request`
- `claimed` (boolean, default: false) Example: `Do not include in request`
- `sort` (string, default: most_relevant) — values: most_relevant, reviews_count, latest_review
- `country` (string, default: us) Example: `us`
- `city_or_zip_code` (string) — City or zip code from which to return companies / businesses.
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** page_number (param: `page`)

---

### GET /category-recently-reviewed-companies
Recently Reviewed Companies in Category — Get the list of recently reviewed companies is a specific category.

**Required:**
- `category_id` (string) Example: `software_company`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none
**Response path:** `data`
**Key fields:** company_id, name, domain, review_count, trust_score, rating, type, description, example

---

### GET /category-newest-companies
Newest Companies in Category — Get the list of newest companies is a specific category.

**Required:**
- `category_id` (string) Example: `software_company`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none
**Response path:** `data`
**Key fields:** id, name, parent_id, company_count, level, domain, review_count, trust_score, rating, categories, country, city

---

### GET /category-search
Category Search — Search all Trustpilot categories.

**Required:**
- `query` (string) — Search query / keyword Example: `soft`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none
**Response path:** `data`
**Key fields:** id, name

---

### GET /category-details
Category Details — Get the full details of a category, including subcategories, parent categories, sibling categories and more information.

**Required:**
- `category_id` (string) — The ID of the category for which to get full details. Example: `internet_software`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none
**Response path:** `data`
**Key fields:** id, name, parent_id, company_count, level, type, description, example

---

### GET /consumer-details
Consumer Details — Get the full details of a consumer.

**Required:**
- `consumer_id` (string) — The ID of the consumer for which to get full details. Example: `5fafc38b32ed7f0019d27bc5`

**Optional:**
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** none

---

### GET /consumer-reviews
Consumer Reviews — Get all consumer reviews with pagination support.

**Required:**
- `consumer_id` (string) — The ID of the consumer for which to get full details. Example: `5fafc38b32ed7f0019d27bc5`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `locale` (string, default: en-US) — values: da-DK, de-AT, de-CH, de-DE, en-AU, en-CA, en-GB, en-IE, en-NZ, en-US, es-ES, fi-FI, fr-BE, nl-BE, fr-FR, it-IT, ja-JP, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, sv-SE

**Pagination:** page_number (param: `page`)

---
