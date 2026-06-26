# jsearch

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/jsearch.yaml

**Host:** `jsearch.p.rapidapi.com`
**Notes:** Fixed 10 results per page. Response includes num_pages (total pages available). Fetching >10 pages costs 3x credits.

## Endpoints

### GET /search
Job Search

**Required:**
- `query` (string) Example: `developer jobs in chicago`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `num_pages` (integer, default: 1) Example: `1`
- `country` (string, default: us) Example: `us`
- `language` (string) Example: `en`
- `date_posted` (string, default: all) — values: all, today, 3days, week, month
- `work_from_home` (boolean, default: false) Example: `false`
- `employment_types` (string) — values: FULLTIME, CONTRACTOR, PARTTIME, INTERN
- `job_requirements` (string) — values: under_3_years_experience, more_than_3_years_experience, no_experience, no_degree
- `radius` (number) Example: `1`
- `exclude_job_publishers` (string) Example: `BeeBe,Dice`
- `fields` (string) Example: `employer_name,job_publisher,job_title,job_country`

**Pagination:** page_number (param: `page`)
**Response path:** `data` (jobs nested as `data[].jobs[]`)

---

### GET /job-details
Job Details

**Required:**
- `job_id` (string) Example: `gcnkkB1_QjIlxbV9AAAAAA==`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string) Example: `en`
- `fields` (string) Example: `employer_name,job_publisher,job_title,job_country`

**Pagination:** none
**Response path:** `data`
**Key fields:** job_id, job_title, employer_name, employer_logo, employer_website, job_publisher, job_employment_type, job_apply_link, job_apply_is_direct, job_description, job_is_remote, job_posted_at, job_posted_at_timestamp, job_posted_at_datetime_utc, job_location, job_city, job_state, job_country, job_latitude, job_longitude, job_benefits, job_google_link, job_salary, job_min_salary, job_max_salary, job_salary_period, job_onet_soc, job_onet_job_zone, job_employment_types, apply_options, job_highlights

---

### GET /estimated-salary
Job Salary

**Required:**
- `job_title` (string) — Job title for which to get salary estimation. Example: `nodejs developer`
- `location` (string) — Location in which to get salary estimation. Example: `new york`

**Optional:**
- `location_type` (string, default: ANY) — values: ANY, CITY, STATE, COUNTRY
- `years_of_experience` (string, default: ALL) — values: ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN
- `fields` (string) Example: `job_title,median_salary,location`

**Pagination:** none
**Response path:** `data`
**Key fields:** location, job_title, min_salary, max_salary, median_salary, min_base_salary, max_base_salary, median_base_salary, min_additional_pay, max_additional_pay, median_additional_pay, salary_period, salary_currency, salary_count, salaries_updated_at, publisher_name, publisher_link, confidence

---

### GET /company-job-salary
Company Job Salary — Get estimated job salaries/pay in a specific company by job title and optionally a location and experience level in years.

**Required:**
- `company` (string) — The company name for which to get salary information (e.g. Amazon). Example: `Amazon`
- `job_title` (string) — Job title for which to get salary estimation. Example: `software developer`

**Optional:**
- `location` (string) — Freetext location/area in which to get salary estimation. Example: `NY`
- `location_type` (string, default: ANY) — values: ANY, CITY, STATE, COUNTRY
- `years_of_experience` (string, default: ALL) — values: ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN

**Pagination:** none
**Response path:** `data`
**Key fields:** location, job_title, company, min_salary, max_salary, median_salary, min_base_salary, max_base_salary, median_base_salary, min_additional_pay, max_additional_pay, median_additional_pay, salary_period, salary_currency, confidence, salary_count

---
