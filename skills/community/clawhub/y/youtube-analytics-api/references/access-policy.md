# YouTube Analytics access policy

An access policy limits which endpoints YouTube Analytics connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/youtube-analytics#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for YouTube Analytics: its 3 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create youtube-analytics --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/groupItems"},
    {"method": "GET", "path": "v2/groups"},
    {"method": "GET", "path": "v2/reports"}
  ],
  "deny": []
}
```

## Endpoints

The YouTube Analytics endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v2/groupItems | read | groupItems | Returns a collection of group items that match the API request parameters. |
| POST | v2/groupItems | write | groupItems | Creates a group item. |
| DELETE | v2/groupItems | write | groupItems | Removes an item from a group. |
| GET | v2/groups | read | groups | Returns a collection of groups that match the API request parameters. |
| POST | v2/groups | write | groups | Creates a group. |
| PUT | v2/groups | write | groups | Modifies a group. |
| DELETE | v2/groups | write | groups | Deletes a group. |
| GET | v2/reports | read | reports | Retrieve your YouTube Analytics reports. |
