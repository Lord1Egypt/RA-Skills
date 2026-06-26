# Field Guide: Sunrise Link Maid Search

This document describes every search parameter accepted by the search tool and every field returned in the results. Load this reference when you need to understand what a field means or which values are valid.

## Search Parameters

All parameters are optional. Pass them as a JSON object to `search_maids.mjs`.

### Basic Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `nationality` | string | Filter by nationality. Single value. |
| `religion` | string | Filter by religion. Single value. |
| `languages` | string[] | Filter by languages spoken. Candidates matching any of the listed languages are returned (overlaps logic). |
| `minAge` | number | Minimum age (inclusive). |
| `maxAge` | number | Maximum age (inclusive). |
| `minSalary` | number | Minimum monthly salary in SGD (inclusive). |
| `maxSalary` | number | Maximum monthly salary in SGD (inclusive). |
| `hasSgExperience` | boolean | If `true`, only candidates with prior Singapore work experience. |

### Skill Filters

Skill filters use AND logic — all specified skill conditions must be met.

Each skill has two filter levels:
- **`needs*`** (e.g. `needsCooking`) — matches candidates who are **willing** OR **experienced**
- **`needsExperienced*`** (e.g. `needsExperiencedCooking`) — matches only candidates who are **experienced**

| Parameter | Matches |
|-----------|---------|
| `needsInfantCare` | Willing or experienced in infant/child care |
| `needsExperiencedInfantCare` | Experienced in infant/child care only |
| `needsElderlyCare` | Willing or experienced in elderly care |
| `needsExperiencedElderlyCare` | Experienced in elderly care only |
| `needsDisabledCare` | Willing or experienced in disabled care |
| `needsCooking` | Willing or experienced in cooking |
| `needsExperiencedCooking` | Experienced in cooking only |
| `needsHousework` | Willing or experienced in housework |

## Valid Enum Values

### Nationality

`Myanmar` · `India` · `Indonesia` · `Philippines` · `Bangladesh` · `Cambodia` · `Laos` · `Nepal`

### Religion

`Buddhism` · `Christianity` · `Islam` · `Hinduism` · `None`

### Education Level (response only)

`Primary school` · `Secondary school` · `High school` · `University` · `Graduate`

### Marital Status (response only)

`Single` · `Married` · `Divorced` · `Widowed`

### Interview Availability (response only)

`notAvailable` · `byPhone` · `byVideo` · `inPerson`

## Response Fields

### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `totalFound` | number | Total candidates matching the filters in the database. |
| `returned` | number | Number of candidates in this response (max 5 by default). |
| `candidates` | array | List of matching candidates. |

### Candidate Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Internal candidate ID. |
| `uuid` | string | Public identifier used in profile URLs. |
| `age` | number \| null | Candidate's age. |
| `nationality` | string \| null | Country of origin. |
| `religion` | string \| null | Religious affiliation. |
| `salary` | number \| null | Expected monthly salary in SGD. |
| `loan` | number \| null | Agency service fee loan amount in SGD. This is owed by the maid to the agency, not paid by the employer. |
| `loanPeriodMonths` | number \| null | Number of months to repay the loan. |
| `educationLevel` | string \| null | Highest education completed. |
| `maritalStatus` | string \| null | Current marital status. |
| `monthlyRestDays` | number \| null | Number of rest days per month. |
| `hasSgExperience` | boolean \| null | Whether the candidate has worked in Singapore before. |
| `languages` | string[] | Languages the candidate speaks. |
| `interviewAvailability` | string \| null | How the candidate is available for interviews. |
| `skills` | object \| null | Skill evaluations (see below). |
| `workExperience` | array | Past work history (see below). |
| `profileUrl` | string | Link to the candidate's profile page on Sunrise Link (includes UTM tracking). |

### Skills Object

`skills` contains two evaluations with identical structure:

- `sgEvaluated` — assessed by the Singapore agency
- `overseasEvaluated` — assessed by the overseas training centre

Each evaluation has these skill categories:

| Category | Fields | Notes |
|----------|--------|-------|
| `infantsChildren` | `willingness`, `experienced`, `ageRange` | `ageRange` is a string like `"0-6"` describing the age group the candidate has experience with. |
| `elderly` | `willingness`, `experienced` | |
| `disabled` | `willingness`, `experienced` | |
| `housework` | `willingness`, `experienced` | |
| `cooking` | `willingness`, `experienced`, `cuisines` | `cuisines` is an array of strings, e.g. `["Chinese", "Western"]`. |

- `willingness` (boolean): The candidate is willing to do this type of work.
- `experienced` (boolean): The candidate has been formally evaluated and confirmed to have hands-on experience in this area. This carries more weight than willingness alone.

### Work Experience Array

Each entry represents one overseas work placement (maximum 2 entries):

| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country where the candidate worked. |
| `workDuties` | string | Description of job responsibilities. |
| `dateFrom` | string | Start date (e.g. `"2021-01"`). |
| `dateTo` | string | End date (e.g. `"2023-06"`). |

## Privacy Notice

The API intentionally excludes all personally identifiable information (PII). The following are **never** returned: candidate name, photo, date of birth, place of birth, home address, phone number, employer feedback, health records, or government documents. Use the `profileUrl` to direct users to the full profile on the Sunrise Link website.
