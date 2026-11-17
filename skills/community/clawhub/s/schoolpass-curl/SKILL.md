---
name: schoolpass-curl
description: Read a SchoolPass parent account directly with curl against the regional SchoolPass REST API (a busapi shard on school-pass.net), without running the MCP server. Use for a one-off shell read of your students, arrival/dismissal calendar, pending pickup changes, drivers, dismissal locations, or school info — "check SchoolPass from the terminal", "list my kids in SchoolPass", "any dismissal changes today". Requires SCHOOLPASS_EMAIL / SCHOOLPASS_PASSWORD / SCHOOLPASS_SCHOOL_CODE.
---

# SchoolPass API via curl

The SchoolPass JSON API is reachable server-side — no browser, no bridge, no
extension. This skill talks to it directly with `curl`.

Prefer the `schoolpass-mcp` server for anything conversational or repeated; use
this for one-off shell work, scripts, or when the server isn't running.

**Ready-to-run request bodies and `jq` recipes: `references/requests.md`.**
Full shape reference: `../../docs/SCHOOLPASS-API.md`.

## Setup

```bash
export SCHOOLPASS_EMAIL='you@example.com'
export SCHOOLPASS_PASSWORD='…'
export SCHOOLPASS_SCHOOL_CODE=1183          # your school id (the AppCode)
export SCHOOLPASS_API_HOST=busapi-east16-ss.school-pass.net   # your region's shard
```

Find your school id and region host by signing into your school's
`<school>.school-pass.net` portal, opening the new SchoolPass app, and reading
`appCode` (the id) and `apiUrl` (the host) from its `localStorage`.

## Two rules

1. **Every request needs an `AppCode: <schoolCode>` header.** It selects your
   school. Omit it (or send the wrong one) and you get `401`. It is not a
   secret. `references/requests.md`'s `sp_curl` helper adds it for you.
2. **HTTP status codes are real.** `401` = the token or AppCode was rejected,
   `403` = a parent account cannot reach that route (it is admin-only), `2xx` =
   success. Branch on the HTTP code.

## Auth: email/password → bearer

1. `POST Auth/users` with `{schoolCode,email,password,authType:"Credentials"}`
   → the identities your email owns. Take the one whose `userType` is `3`
   (Parent).
2. `POST Auth/token` with `{schoolCode,userId,userType,password,authType:"Credentials"}`
   → `{ access_token, refresh_token, … }`. Send `access_token` as
   `Authorization: Bearer …` on every subsequent call.

`references/requests.md`'s `sp_login` does both and caches the token.

> **Never retry a rejected login.** SchoolPass fronts its login with reCAPTCHA;
> repeated wrong passwords can get the account challenged and break shell login.
> Fix the credential and try once.

## Reads

All are `GET` with the `AppCode` header + `Authorization: Bearer`. Most parent
endpoints take an optional `memberId` (your own parent id, from `Auth/users`).

| Want | Endpoint |
| --- | --- |
| your students | `GET parent/getstudents` |
| parent profile | `GET parent/profile` |
| authorized drivers | `GET parent/parentdrivers?includeCarpool=true` |
| student calendar | `GET Student/StudentCalendar?schoolCode=&studentId=&startDate=&endDate=` |
| pickup changes | `GET PickupChange/GetChanges?studentId=&date=` |
| dismissal locations | `GET dismissal/getDismissalLocations` |
| school info | `GET SchoolInfo/GetBasicSchoolInfo?schoolCode=` |
| reachability (no auth) | `GET version?schoolCode=` |

## Scope

Parent tokens are parent-scoped: the admin surface (visitor management, carline
operations, reports, bus routing) returns `403`. This is expected, not a bug.

Never echo the password or the bearer token into a shared transcript.
