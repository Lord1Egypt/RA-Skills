# Errors — Classify First, Then Fix

**Before debugging**, read `## Gotchas` in `~/Clawic/data/salesforce-api-integration/memory.md` (or `gotchas.md` if the `## Boxes` index points there). This org has produced errors before, and the row that explains this one may already be written.

**Contents:** [The Classification](#the-classification) · [Error Body](#error-body) · [Auth](#auth) · [Permission](#permission) · [Schema and Data](#schema-and-data) · [The Org's Own Code](#the-orgs-own-code) · [Limits and Contention](#limits-and-contention) · [Retry Policy](#retry-policy) · [Getting the Real Message](#getting-the-real-message) · [Debug Logs](#debug-logs)

## The Classification

Branch on `errorCode`, never on the HTTP status — a 403 is either "no permission" or "out of allocation", and the two fixes are opposites.

| Class | Tell | Fix lives in |
|---|---|---|
| Auth | 401, or `invalid_*` from the token endpoint | `auth.md` |
| Permission | `INSUFFICIENT_ACCESS*`, `INVALID_FIELD` on a real field | The integration user's permission set |
| Schema | `INVALID_TYPE`, `INVALID_FIELD`, `MALFORMED_QUERY`, `STRING_TOO_LONG` | Your payload or `metadata.md` |
| Org automation | `FIELD_CUSTOM_VALIDATION_EXCEPTION`, `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY`, `DUPLICATES_DETECTED` | The org's rules — a conversation, not a code change |
| Limits | `REQUEST_LIMIT_EXCEEDED`, `QUERY_TIMEOUT`, concurrency 503 | `limits.md` |
| Contention | `UNABLE_TO_LOCK_ROW` | Batch shape (`bulk.md`) |
| Data | `INVALID_CROSS_REFERENCE_KEY`, `DUPLICATE_VALUE`, `ENTITY_IS_DELETED` | The source data |

## Error Body

Salesforce returns an **array**, even for one error:

```json
[{"errorCode":"INVALID_FIELD","message":"No such column 'Industryy' on entity 'Account'","fields":["Industryy"]}]
```

`fields[]` names the offending field when there is one — an empty `fields` array with a 400 almost always means org automation rather than your payload. In Collections and Composite the same objects appear per record inside a 200 response (`composite.md`); in Bulk they appear in the `sf__Error` column of `failedResults` (`bulk.md`).

## Auth

| Code | HTTP | Cause | Fix |
|---|---|---|---|
| `INVALID_SESSION_ID` | 401 | Token expired, revoked, or sent to the wrong instance | Re-authenticate once, then retry once; use the `instance_url` from the token response |
| `INVALID_AUTH_HEADER` | 401 | Header is not `Bearer <token>` | Check for a stray newline from a shell variable |
| `invalid_grant` | 400 | JWT pre-authorization, `aud`, `sub`, clock skew, or a dead refresh token | `auth.md` — it is one of five specific things |
| `IP_RANGE_ERROR` | 403 | Caller outside the profile's login IP ranges | Relax IP restrictions on the Connected App, or whitelist the range |

## Permission

| Code | HTTP | Cause | Fix |
|---|---|---|---|
| `INSUFFICIENT_ACCESS_OR_READONLY` | 403 | No sharing access to the record, or the record is locked by an approval process | Check sharing and approval state, not object permissions |
| `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY` | 400 | You may edit this record but not the one it points at | Grant access to the *parent* |
| `INVALID_FIELD` on a field that exists | 400 | Field-level security hides it from this user | Add FLS read/edit to the integration user's permission set (`SKILL.md` Rule 7) |
| `ENTITY_IS_LOCKED` | 400 | Approval process or a locked record | Not an API problem; the record is locked in the org |

## Schema and Data

| Code | HTTP | Cause | Fix |
|---|---|---|---|
| `MALFORMED_QUERY` | 400 | SOQL syntax, or a relationship name where a field name goes | `Account.Name` traverses, `AccountId` is the field (`soql.md`) |
| `INVALID_TYPE` | 400 | Object does not exist for this user | Check spelling and the `__c` suffix; then check profile access |
| `REQUIRED_FIELD_MISSING` | 400 | A field required by the schema, not by the layout | Compute the real required list from describe (`metadata.md`) |
| `STRING_TOO_LONG` | 400 | Value longer than the field's `length` | Truncate deliberately at the source, with the truncation rule recorded in `## Gotchas` |
| `INVALID_CROSS_REFERENCE_KEY` | 400 | A lookup id that is wrong, deleted, or points at another object | Check the 3-char prefix first (`records.md`) |
| `DUPLICATE_VALUE` | 400 | Unique field or external id collision | Two source rows carry the same key — dedupe before, not after |
| `ENTITY_IS_DELETED` | 400 | Record is in the recycle bin | `queryAll` to confirm; stop referencing it |
| `JSON_PARSER_ERROR` | 400 | Malformed body, or a read-only field included | Strip `Id`, audit fields and formulas from a record you read back |

## The Org's Own Code

These are not API errors. Something inside the org rejected the write, and the fix is usually a conversation with the admin.

| Code | Meaning | What to do |
|---|---|---|
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | A validation rule fired; the `message` **is** the admin's error text | Satisfy it, or have the rule deactivated for a load, deliberately (`migration.md`) |
| `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` | A trigger, flow or process threw. The message carries the class name and the inner error | Read past the wrapper — the real message is at the end |
| `DUPLICATES_DETECTED` | A duplicate rule blocked the save | Fix the data, or send `Sforce-Duplicate-Rule-Header: allowSave=true`, recording the decision and its reason in `## Gotchas` |
| `FIELD_FILTER_VALIDATION_EXCEPTION` | A lookup filter rejected the related record | The parent does not meet the filter's criteria |
| `CANNOT_EXECUTE_FLOW_TRIGGER` | A record-triggered flow failed | The flow's fault; it needs the admin |
| `UNKNOWN_EXCEPTION` with no field | Frequently an Apex trigger that swallowed its own context | Ask for a debug log (below) |

Before a bulk load, list the target object's active validation rules, triggers and flows — three Tooling queries in `metadata.md` — and you will predict most of this class instead of discovering it at row 12,000.

## Limits and Contention

| Code | HTTP | Retry? | Note |
|---|---|---|---|
| `REQUEST_LIMIT_EXCEEDED` | 403 | **No** | The org's daily allocation, rolling 24 hours. Retrying deepens the outage for every integration |
| `QUERY_TIMEOUT` | 400 | No | The query is unselective; fix the filter (`soql.md`) |
| `OPERATION_TOO_LARGE` | 400 | No | Query returns too much for the resource; narrow it or use Bulk |
| `EXCEEDED_MAX_SEMIJOIN_SUBQUERIES` | 400 | No | Split into two queries |
| `TOO_MANY_APEX_REQUESTS` / concurrency 503 | 503 | Yes, with backoff | More than 25 requests running over 20s at once (`limits.md`) |
| `UNABLE_TO_LOCK_ROW` | 400 | Yes, with backoff | And fix the batch shape, or it recurs forever (`bulk.md`) |
| `STORAGE_LIMIT_EXCEEDED` | 400 | No | The org is full; deleting to the recycle bin does not help until it is emptied |

## Retry Policy

```
retryable  = HTTP 5xx, UNABLE_TO_LOCK_ROW, concurrency 503, network timeout
retry once = 401 INVALID_SESSION_ID, after re-authenticating
never      = any 400 with an errorCode, 403 REQUEST_LIMIT_EXCEEDED, 404
```

- Exponential backoff with jitter: `sleep = min(base × 2^attempt, cap) × (0.5 + random/2)`, base 1s, cap 60s, 3-5 attempts. Without jitter, a batch of parallel workers retries in lockstep and reproduces the contention exactly.
- **Every retryable write must be idempotent first.** A timeout is a missing *response*, not a missing write: the record may exist. Upsert on an external id makes retrying free (`records.md` — `SKILL.md` Rule 4).
- Retrying a 400 unchanged is a loop that consumes allocation and produces the same error. Fix, then resend.
- On `REQUEST_LIMIT_EXCEEDED`, stop everything and report the remaining allocation from `/limits`. This is the one error where the correct behaviour is to give up loudly.

## Getting the Real Message

A wrapped trigger error looks like this:

```
CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY: AccountTrigger: execution of BeforeInsert caused by:
System.DmlException: Insert failed. First exception on row 0; first error:
FIELD_CUSTOM_VALIDATION_EXCEPTION, Region is required for enterprise accounts: [Region__c]
```

Read it back to front: the last error code and message are the actual cause, the field in brackets is the field, and the class name at the front tells you whose code to ask about. Reporting only the outer code sends everyone down the wrong path.

## Debug Logs

When the message is genuinely empty, the org has to be instrumented:

- The admin (or you, with permission) sets a `TraceFlag` on the integration user through the Tooling API or Setup; the resulting `ApexLog` records are queryable and downloadable through the Tooling API (`metadata.md`).
- Logs are capped in size and retained briefly, and a busy user fills the buffer quickly. Set the trace immediately before reproducing, with the smallest reproduction you have — one record, not the load.
- Turn the trace off afterwards. An always-on trace flag on an integration user is a performance problem and an audit finding.

**Every error whose real cause took work to find** goes in `## Gotchas` in `memory.md`: symptom, real cause, fix, and the date. Three columns, one row. This is the highest-return writing this skill does — an org's automation produces the same handful of confusing failures for years, and the row turns each one from an afternoon into a lookup.
