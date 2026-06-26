# job-salary-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/job_salary_data.yaml

**Host:** `job-salary-data.p.rapidapi.com`
**Notes:** No pagination — each call returns salary estimates for a given job title and location. Use `location_type` to control geographic scope (city, state, country, or any).

## Endpoints

### GET /job-salary
Retrieve estimated salary ranges for a job title in a specific location, sourced from Glassdoor.

**Required:**
- `job_title` (string) Example: `software engineer`
- `location` (string) Example: `New York, NY`

**Optional:**
- `location_type` (string) — values: `CITY`, `STATE`, `COUNTRY`, `ANY` (default: `ANY`) Example: `CITY`
- `years_of_experience` (string) — values: `0-1`, `1-3`, `3-5`, `5-10`, `10-15`, `15+` (default: ALL) Example: `3-5`

**Pagination:** none
**Response path:** `data`
**Key fields:** job_title, location, min_salary, max_salary, median_salary, salary_period, currency, confidence, publisher_name

---

### GET /company-job-salary
Retrieve compensation data for a specific role at a specific company, broken down by base salary and additional compensation (bonuses, etc.).

**Required:**
- `job_title` (string) Example: `software engineer`
- `company_name` (string) Example: `Google`

**Optional:**
- `location` (string) Example: `San Francisco, CA`
- `location_type` (string) — values: `CITY`, `STATE`, `COUNTRY`, `ANY` (default: `ANY`) Example: `CITY`
- `years_of_experience` (string) — values: `0-1`, `1-3`, `3-5`, `5-10`, `10-15`, `15+` Example: `5-10`

**Pagination:** none
**Response path:** `data`
**Key fields:** job_title, company_name, location, min_salary, max_salary, median_salary, additional_pay_min, additional_pay_max, salary_count, salary_period, currency, confidence, publisher_name
