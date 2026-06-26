# QuickBooks Online Query Language & Error Handling Reference

## Intuit Data Services (IDS) Query Language

### Syntax & Pagination
To retrieve lists of entities, use the SQL-like IDS Query Language.
```sql
SELECT * FROM Customer WHERE Active = true STARTPOSITION 1 MAXRESULTS 500
```
*   **Pagination:** Use `STARTPOSITION` (1-indexed) and `MAXRESULTS` (maximum limit of **1000** records per request) to paginate through large datasets.
*   **Unsupported Operators:** `OR` operations are **not** supported by the IDS query engine. Split complex `OR` conditions into separate API queries or use `IN` clauses.

### IDS-QL Injection Prevention
The QuickBooks API does not sanitize query inputs. Always escape single quotes (`'`) by replacing them with backslash-escaped single quotes (`\'`) or stripping them completely before interpolating variables into query strings:
```python
def sanitize_input(user_input: str) -> str:
    return user_input.replace("'", "\\'")
```

---

## Change Data Capture (CDC)
Query all entities of specified types that have changed since a given timestamp.
*   **Endpoint:** `/v3/company/<realmId>/cdc?entities=<EntityList>&changedSince=<Timestamp>`
*   **Example Call:** `/v3/company/12345/cdc?entities=Customer,Invoice&changedSince=2026-05-31T00:00:00Z`

---

## Error Handling & Resilience

### Common Error Codes

| Error Code | HTTP Status | Common Cause | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **`2030`** | `400 Bad Request` | Stale `SyncToken` during update. | Fetch the latest version of the entity, merge changes, and retry. |
| **`3100`** | `400 Bad Request` | Duplicate `DocNumber`. | Enable `allowduplicatedocnum` query parameter or let system auto-generate. |
| **`3200`** | `400 Bad Request` | Transaction is locked / reconciled. | Do not allow edits via API; prompt user to unlock inside QuickBooks UI. |
| **`100`** | `401 Unauthorized` | Invalid or expired Access Token. | Execute OAuth token refresh flow and retry the request. |
| **`429`** | `429 Too Many Requests`| API rate limit exceeded (100 req/min). | Implement exponential backoff with jitter. |

### Exponential Backoff Implementation (Python)
```python
import time
import random
import requests

def execute_with_retry(api_call_func, max_retries=5):
    base_delay = 1.0  # start with 1 second
    
    for attempt in range(max_retries):
        try:
            response = api_call_func()
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                # Rate limited - backoff and retry
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(delay)
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay)
```
