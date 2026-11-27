# Zoho Calendar access policy

An access policy limits which endpoints Zoho Calendar connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-calendar#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Calendar: its 8 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-calendar --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v1/calendars"},
    {"method": "GET", "path": "api/v1/calendars/{id}"},
    {"method": "GET", "path": "api/v1/calendars/{id}/events"},
    {"method": "GET", "path": "api/v1/calendars/{id}/events/{id}"},
    {"method": "GET", "path": "api/v1/calendars/{id}/events/{id}/attachment/{id}"},
    {"method": "GET", "path": "api/v1/calendars/{id}/events/{id}/byinstance"},
    {"method": "GET", "path": "api/v1/calendars/{id}/events/{id}/groupattendeestatus"},
    {"method": "GET", "path": "api/v1/calendars/freebusy"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Calendar endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v1/calendars | read | calendars | Get the list of all calendars. |
| POST | api/v1/calendars | write | calendars | Create a new calendar. |
| GET | api/v1/calendars/{id} | read | calendars | Get details of a calendar (UID, default or primary). |
| PUT | api/v1/calendars/{id} | write | calendars | Update an existing calendar. |
| DELETE | api/v1/calendars/{id} | write | calendars | Delete a calendar. |
| POST | api/v1/attachment | write | events | Upload a file to attach to an event. |
| GET | api/v1/calendars/{id}/events | read | events | Get the list of events in a calendar for a date range. |
| POST | api/v1/calendars/{id}/events | write | events | Create a new event. |
| GET | api/v1/calendars/{id}/events/{id} | read | events | Get details of an event. |
| POST | api/v1/calendars/{id}/events/{id} | write | events | Move an event to another calendar. |
| PUT | api/v1/calendars/{id}/events/{id} | write | events | Update an event or delete its attachment. |
| DELETE | api/v1/calendars/{id}/events/{id} | write | events | Delete an event. |
| GET | api/v1/calendars/{id}/events/{id}/attachment/{id} | read | events | Get or download an event attachment. |
| GET | api/v1/calendars/{id}/events/{id}/byinstance | read | events | Get event instances of a recurring event. |
| GET | api/v1/calendars/{id}/events/{id}/groupattendeestatus | read | events | Get group attendee details of an event. |
| GET | api/v1/calendars/freebusy | read | freebusy | Get free/busy details of a user across all calendars. |
