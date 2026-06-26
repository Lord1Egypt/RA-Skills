## Hotel Search Prompt

When the user expresses an intent to search for hotels, call the `hotel_search` tool.

## Trigger scenarios
- The user wants to find a hotel
- The user mentions a location + accommodation needs
- The user asks for hotel recommendations in a place

## Argument extraction rules

Extract the following structured arguments from the user's message.

## Arguments

| Name            | Type     | Required | Description | Example | Default |
|-----------------|----------|----------|-------------|---------|---------|
| location        | string   | yes      | Coordinates in the format `lat,lon` | 39.9042,116.4074 | - |
| check_in_date   | string   | yes      | Check-in date, `YYYY-MM-DD` | 2024-12-25 | - |
| check_out_date  | string   | yes      | Check-out date, `YYYY-MM-DD` | 2024-12-27 | - |
| query           | string   | no       | Search keyword such as hotel name or area | Hilton | - |
| radius          | number   | no       | Search radius in kilometers | 5.0 | 5 |
| budget          | string   | no       | Price range, `min-max` | 100-500 | - |
| star_rating     | integer  | no       | Star rating, 1-5 | 4 | - |
| rating          | string   | no       | Guest rating range, `min-max` | 8.0-10.0 | - |
| currency        | string   | no       | Currency code, e.g. CNY / USD | CNY | CNY |

## Instructions for the agent

When mapping natural language to arguments, follow these rules:

- **location (required)**
  - Users often describe locations as city names / landmarks / business districts (e.g. “Shanghai Bund”, “Beijing Sanlitun”).
  - You must resolve the place first, then **look up the coordinates**, and fill `location` as `"lat,lon"`, e.g. `"31.2400,121.4900"`.

- **check_in_date / check_out_date (required)**
  - Parse dates mentioned by the user (e.g. “2026-03-20”, “Mar 20th”, “next Friday”, “this weekend”) into concrete calendar dates using `YYYY-MM-DD`.
  - For relative dates like “the 20th”:
    - Use “today is 2026-03-04” as the reference and pick the **nearest future date**.
    - Example: if today is Mar 4 and the user says “the 20th”, use `2026-03-20`. If today is Mar 21 and the user says “the 20th”, use `2026-04-20`.
  - `check_out_date` must be later than `check_in_date`. If the user says “stay 2 nights”, set check-out to check-in + 2 days.

- **budget (optional)**
  - Convert budgets like “300 to 800”, “under 800”, “no more than 500” into `"min-max"`.
  - If there is no upper bound, use a reasonable default upper bound (e.g. “300+” → `"300-100000"`), and prioritize results closer to the intended range.

- **rating (optional)**
  - Map rating constraints like “4.0+”, “4.5 to 5.0” to `"min-max"`, e.g. `"4.0-5.0"`.

- **star_rating (optional)**
  - If the user mentions a star rating (“3+ stars”, “4-5 stars”, “only 5-star”), convert it to a number:
    - For a single rating, set it directly (e.g. “5-star hotel” → `5`).
    - For a range (e.g. “3 to 4 stars”), choose the primary star rating within the range (e.g. `4`) and use `rating` for finer filtering.

- **radius (optional)**
  - Use the default 5 km if not specified. If the user says “within ~10 km” or “within 3 km nearby”, set the numeric value accordingly.

- **query (optional)**
  - Used as a keyword filter, e.g. hotel name, business district, or requirements (“ocean view”, “family-friendly”, “business trip”, “near subway”, etc.).

- **currency (optional)**
  - If the user specifies a currency (“budget 100 USD”), set `currency` to the ISO4217 code (e.g. `"USD"`) and interpret `budget` in that currency.
  - If not specified, use the default `"USD"`.

## `query` requirements

**Important**: `query` is not the user's raw input. It must be a processed hotel-name keyword.

The agent must:
1. Extract the hotel-name keyword from the user input
2. Remove any personally identifiable information (name, phone number, email, ID number, etc.)
3. Keep only the hotel-name keyword, not the city or landmarks

Example:
- User: "My name is Zhang San, I want to book Shanghai Ritz-Carlton Hotel"
- `query` should be: "Ritz-Carlton" (remove the name)

## Example call

User: "Find Rosewood Hotel Hong Kong, check in on Apr 1 for 2 nights"

```json
{
  "location": "22.319304,114.169361",
  "check_in_date": "2026-04-01",
  "check_out_date": "2026-04-03",
  "originQuery": "Rosewood"
}