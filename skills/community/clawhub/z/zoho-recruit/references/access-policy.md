# Zoho Recruit access policy

An access policy limits which endpoints Zoho Recruit connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-recruit#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Recruit: its 27 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-recruit --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "recruit/v2/{id}/{id}/associate"},
    {"method": "GET", "path": "recruit/v2/{id}/{id}/Attachments"},
    {"method": "GET", "path": "recruit/v2/{id}/{id}/Attachments/{id}"},
    {"method": "GET", "path": "recruit/bulk/v2/read/{id}"},
    {"method": "GET", "path": "recruit/bulk/v2/read/{id}/result"},
    {"method": "GET", "path": "recruit/bulk/v2/write/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/custom_views"},
    {"method": "GET", "path": "recruit/v2/settings/custom_views/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/fields"},
    {"method": "GET", "path": "recruit/v2/settings/layouts"},
    {"method": "GET", "path": "recruit/v2/settings/layouts/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/modules"},
    {"method": "GET", "path": "recruit/v2/settings/modules/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/related_lists"},
    {"method": "GET", "path": "recruit/v2/Notes"},
    {"method": "GET", "path": "recruit/v2/org"},
    {"method": "GET", "path": "recruit/v2/settings/profiles"},
    {"method": "GET", "path": "recruit/v2/settings/profiles/{id}"},
    {"method": "GET", "path": "recruit/v2/{id}"},
    {"method": "GET", "path": "recruit/v2/{id}/deleted"},
    {"method": "GET", "path": "recruit/v2/{id}/search"},
    {"method": "GET", "path": "recruit/v2/{id}/{id}"},
    {"method": "GET", "path": "recruit/v2/{id}/{id}/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/roles"},
    {"method": "GET", "path": "recruit/v2/settings/roles/{id}"},
    {"method": "GET", "path": "recruit/v2/settings/tags"},
    {"method": "GET", "path": "recruit/v2/users"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Recruit endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| PUT | recruit/v2/Candidates/actions/associate | write | associations | Associate candidates with a job opening. |
| GET | recruit/v2/{id}/{id}/associate | read | associations | Get the job openings associated with a candidate, or the candidates associated with a job opening. |
| GET | recruit/v2/{id}/{id}/Attachments | read | attachments | Get the list of attachments of a record. |
| POST | recruit/v2/{id}/{id}/Attachments | write | attachments | Upload an attachment to a record. |
| GET | recruit/v2/{id}/{id}/Attachments/{id} | read | attachments | Download an attachment of a record. |
| DELETE | recruit/v2/{id}/{id}/Attachments/{id} | write | attachments | Delete an attachment of a record. |
| POST | recruit/bulk/v2/read | write | bulk-read | Create a bulk read job to export records. Kept out of read: creates a bulk export job. |
| GET | recruit/bulk/v2/read/{id} | read | bulk-read | Get the details of a bulk read job. |
| GET | recruit/bulk/v2/read/{id}/result | read | bulk-read | Download the result of a bulk read job. |
| POST | recruit/bulk/v2/write | write | bulk-write | Create a bulk write job to insert, update or upsert records. |
| GET | recruit/bulk/v2/write/{id} | read | bulk-write | Get the details of a bulk write job. |
| GET | recruit/v2/settings/custom_views | read | metadata | Get the custom views of a module. |
| GET | recruit/v2/settings/custom_views/{id} | read | metadata | Get a specific custom view of a module. |
| GET | recruit/v2/settings/fields | read | metadata | Get the metadata of the fields in a module. |
| GET | recruit/v2/settings/layouts | read | metadata | Get the layouts of a module. |
| GET | recruit/v2/settings/layouts/{id} | read | metadata | Get a specific layout of a module. |
| GET | recruit/v2/settings/modules | read | metadata | Get the list of modules. |
| GET | recruit/v2/settings/modules/{id} | read | metadata | Get the metadata of a specific module. |
| GET | recruit/v2/settings/related_lists | read | metadata | Get the related lists of a module. |
| GET | recruit/v2/Notes | read | notes | Get the list of notes. |
| POST | recruit/v2/Notes | write | notes | Create notes. |
| PUT | recruit/v2/Notes | write | notes | Update notes. |
| DELETE | recruit/v2/Notes | write | notes | Delete multiple notes. |
| DELETE | recruit/v2/Notes/{id} | write | notes | Delete a note. |
| GET | recruit/v2/org | read | org | Get the organization data. |
| GET | recruit/v2/settings/profiles | read | profiles | Get the list of profiles. |
| GET | recruit/v2/settings/profiles/{id} | read | profiles | Get a specific profile. |
| GET | recruit/v2/{id} | read | records | Get the list of records from a module. |
| POST | recruit/v2/{id} | write | records | Insert records into a module. |
| PUT | recruit/v2/{id} | write | records | Update records in a module. |
| DELETE | recruit/v2/{id} | write | records | Delete records from a module. |
| GET | recruit/v2/{id}/deleted | read | records | Get the list of deleted records of a module. |
| GET | recruit/v2/{id}/search | read | records | Search the records of a module. |
| POST | recruit/v2/{id}/upsert | write | records | Insert or update records by duplicate-check fields. |
| GET | recruit/v2/{id}/{id} | read | records | Get a specific record. |
| PUT | recruit/v2/{id}/{id} | write | records | Update a specific record. |
| DELETE | recruit/v2/{id}/{id} | write | records | Delete a specific record. |
| GET | recruit/v2/{id}/{id}/{id} | read | related-records | Get the records of a related module for a record. |
| GET | recruit/v2/settings/roles | read | roles | Get the list of roles. |
| GET | recruit/v2/settings/roles/{id} | read | roles | Get a specific role. |
| GET | recruit/v2/settings/tags | read | tags | Get the tags of a module. |
| POST | recruit/v2/settings/tags | write | tags | Create tags in a module. |
| PUT | recruit/v2/settings/tags/{id} | write | tags | Update a tag. |
| DELETE | recruit/v2/settings/tags/{id} | write | tags | Delete a tag. |
| POST | recruit/v2/settings/tags/{id}/actions/merge | write | tags | Merge tags. |
| POST | recruit/v2/{id}/actions/add_tags | write | tags | Add tags to multiple records. |
| POST | recruit/v2/{id}/actions/remove_tags | write | tags | Remove tags from multiple records. |
| POST | recruit/v2/{id}/{id}/actions/add_tags | write | tags | Add tags to a specific record. |
| POST | recruit/v2/{id}/{id}/actions/remove_tags | write | tags | Remove tags from a specific record. |
| GET | recruit/v2/users | read | users | Get the list of users. |
