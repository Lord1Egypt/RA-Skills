# Twenty CRM access policy

An access policy limits which endpoints Twenty CRM connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/twenty#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Twenty CRM: its 29 read-only endpoints, plus deny rules for the 3 write endpoints a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create twenty --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "rest/ai-front-components/drafts/{id}"},
    {"method": "GET", "path": "rest/metadata/fields"},
    {"method": "GET", "path": "rest/metadata/fields/{id}"},
    {"method": "GET", "path": "rest/metadata/objects"},
    {"method": "GET", "path": "rest/metadata/objects/{id}"},
    {"method": "GET", "path": "rest/metadata/pageLayoutTabs"},
    {"method": "GET", "path": "rest/metadata/pageLayoutTabs/{id}"},
    {"method": "GET", "path": "rest/metadata/pageLayoutWidgets"},
    {"method": "GET", "path": "rest/metadata/pageLayoutWidgets/{id}"},
    {"method": "GET", "path": "rest/metadata/pageLayouts"},
    {"method": "GET", "path": "rest/metadata/pageLayouts/{id}"},
    {"method": "GET", "path": "rest/metadata/viewFields"},
    {"method": "GET", "path": "rest/metadata/viewFields/{id}"},
    {"method": "GET", "path": "rest/metadata/viewFilterGroups"},
    {"method": "GET", "path": "rest/metadata/viewFilterGroups/{id}"},
    {"method": "GET", "path": "rest/metadata/viewFilters"},
    {"method": "GET", "path": "rest/metadata/viewFilters/{id}"},
    {"method": "GET", "path": "rest/metadata/viewGroups"},
    {"method": "GET", "path": "rest/metadata/viewGroups/{id}"},
    {"method": "GET", "path": "rest/metadata/viewSorts"},
    {"method": "GET", "path": "rest/metadata/viewSorts/{id}"},
    {"method": "GET", "path": "rest/metadata/views"},
    {"method": "GET", "path": "rest/metadata/views/{id}"},
    {"method": "GET", "path": "rest/open-api/core"},
    {"method": "GET", "path": "rest/open-api/metadata"},
    {"method": "GET", "path": "rest/{id}"},
    {"method": "POST", "path": "rest/{id}/duplicates"},
    {"method": "GET", "path": "rest/{id}/groupBy"},
    {"method": "GET", "path": "rest/{id}/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "rest/metadata/webhooks"},
    {"method": "GET", "path": "rest/webhooks"},
    {"method": "GET", "path": "rest/webhooks/{id}"}
  ]
}
```

## Endpoints

The Twenty CRM endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | rest/ai-front-components/drafts/{id} | read | ai | Returns an AI front component draft. |
| POST | rest/ai/generate-text | write | ai | Generates text with AI. |
| GET | rest/metadata/fields | read | metadata | Lists fields. |
| POST | rest/metadata/fields | write | metadata | Creates one of the fields. |
| GET | rest/metadata/fields/{id} | read | metadata | Returns one of the fields by ID. |
| PUT | rest/metadata/fields/{id} | write | metadata | Updates one of the fields (legacy alias of PATCH). |
| PATCH | rest/metadata/fields/{id} | write | metadata | Updates one of the fields. |
| DELETE | rest/metadata/fields/{id} | write | metadata | Deletes one of the fields. |
| GET | rest/metadata/objects | read | metadata | Lists objects. |
| POST | rest/metadata/objects | write | metadata | Creates one of the objects. |
| GET | rest/metadata/objects/{id} | read | metadata | Returns one of the objects by ID. |
| PUT | rest/metadata/objects/{id} | write | metadata | Updates one of the objects (legacy alias of PATCH). |
| PATCH | rest/metadata/objects/{id} | write | metadata | Updates one of the objects. |
| DELETE | rest/metadata/objects/{id} | write | metadata | Deletes one of the objects. |
| GET | rest/metadata/pageLayoutTabs | read | metadata | Lists page layout tabs. |
| POST | rest/metadata/pageLayoutTabs | write | metadata | Creates one of the page layout tabs. |
| GET | rest/metadata/pageLayoutTabs/{id} | read | metadata | Returns one of the page layout tabs by ID. |
| PATCH | rest/metadata/pageLayoutTabs/{id} | write | metadata | Updates one of the page layout tabs. |
| DELETE | rest/metadata/pageLayoutTabs/{id} | write | metadata | Deletes one of the page layout tabs. |
| GET | rest/metadata/pageLayoutWidgets | read | metadata | Lists page layout widgets. |
| POST | rest/metadata/pageLayoutWidgets | write | metadata | Creates one of the page layout widgets. |
| GET | rest/metadata/pageLayoutWidgets/{id} | read | metadata | Returns one of the page layout widgets by ID. |
| PATCH | rest/metadata/pageLayoutWidgets/{id} | write | metadata | Updates one of the page layout widgets. |
| DELETE | rest/metadata/pageLayoutWidgets/{id} | write | metadata | Deletes one of the page layout widgets. |
| GET | rest/metadata/pageLayouts | read | metadata | Lists page layouts. |
| POST | rest/metadata/pageLayouts | write | metadata | Creates one of the page layouts. |
| GET | rest/metadata/pageLayouts/{id} | read | metadata | Returns one of the page layouts by ID. |
| PATCH | rest/metadata/pageLayouts/{id} | write | metadata | Updates one of the page layouts. |
| DELETE | rest/metadata/pageLayouts/{id} | write | metadata | Deletes one of the page layouts. |
| GET | rest/metadata/viewFields | read | metadata | Lists view fields. |
| POST | rest/metadata/viewFields | write | metadata | Creates one of the view fields. |
| GET | rest/metadata/viewFields/{id} | read | metadata | Returns one of the view fields by ID. |
| PATCH | rest/metadata/viewFields/{id} | write | metadata | Updates one of the view fields. |
| DELETE | rest/metadata/viewFields/{id} | write | metadata | Deletes one of the view fields. |
| GET | rest/metadata/viewFilterGroups | read | metadata | Lists view filter groups. |
| POST | rest/metadata/viewFilterGroups | write | metadata | Creates one of the view filter groups. |
| GET | rest/metadata/viewFilterGroups/{id} | read | metadata | Returns one of the view filter groups by ID. |
| PATCH | rest/metadata/viewFilterGroups/{id} | write | metadata | Updates one of the view filter groups. |
| DELETE | rest/metadata/viewFilterGroups/{id} | write | metadata | Deletes one of the view filter groups. |
| GET | rest/metadata/viewFilters | read | metadata | Lists view filters. |
| POST | rest/metadata/viewFilters | write | metadata | Creates one of the view filters. |
| GET | rest/metadata/viewFilters/{id} | read | metadata | Returns one of the view filters by ID. |
| PATCH | rest/metadata/viewFilters/{id} | write | metadata | Updates one of the view filters. |
| DELETE | rest/metadata/viewFilters/{id} | write | metadata | Deletes one of the view filters. |
| GET | rest/metadata/viewGroups | read | metadata | Lists view groups. |
| POST | rest/metadata/viewGroups | write | metadata | Creates one of the view groups. |
| GET | rest/metadata/viewGroups/{id} | read | metadata | Returns one of the view groups by ID. |
| PATCH | rest/metadata/viewGroups/{id} | write | metadata | Updates one of the view groups. |
| DELETE | rest/metadata/viewGroups/{id} | write | metadata | Deletes one of the view groups. |
| GET | rest/metadata/viewSorts | read | metadata | Lists view sorts. |
| POST | rest/metadata/viewSorts | write | metadata | Creates one of the view sorts. |
| GET | rest/metadata/viewSorts/{id} | read | metadata | Returns one of the view sorts by ID. |
| PATCH | rest/metadata/viewSorts/{id} | write | metadata | Updates one of the view sorts. |
| DELETE | rest/metadata/viewSorts/{id} | write | metadata | Deletes one of the view sorts. |
| GET | rest/metadata/views | read | metadata | Lists views. |
| POST | rest/metadata/views | write | metadata | Creates one of the views. |
| GET | rest/metadata/views/{id} | read | metadata | Returns one of the views by ID. |
| PATCH | rest/metadata/views/{id} | write | metadata | Updates one of the views. |
| DELETE | rest/metadata/views/{id} | write | metadata | Deletes one of the views. |
| GET | rest/open-api/core | read | metadata | Returns the OpenAPI schema of the workspace core API. |
| GET | rest/open-api/metadata | read | metadata | Returns the OpenAPI schema of the metadata API. |
| POST | rest/batch/{id} | write | records | Creates up to 60 records. |
| GET | rest/{id} | read | records | Lists records of an object (standard or custom). |
| POST | rest/{id} | write | records | Creates a record. |
| DELETE | rest/{id} | write | records | Deletes records matching a filter. |
| POST | rest/{id}/duplicates | read | records | Finds potential duplicates for given record data; does not write. |
| GET | rest/{id}/groupBy | read | records | Groups records of an object by a field. |
| PATCH | rest/{id}/merge | write | records | Merges records. |
| GET | rest/{id}/{id} | read | records | Returns one record of an object by ID. |
| PUT | rest/{id}/{id} | write | records | Updates a record (legacy alias of PATCH). |
| PATCH | rest/{id}/{id} | write | records | Updates a record. |
| DELETE | rest/{id}/{id} | write | records | Deletes a record. |
| PATCH | rest/{id}/{id}/restore | write | records | Restores a soft-deleted record. |
| GET | rest/metadata/webhooks | write | webhooks | Lists webhooks. Kept out of read: webhook records include the signing secret. |
| POST | rest/metadata/webhooks | write | webhooks | Creates a webhook. |
| GET | rest/metadata/webhooks/{id} | write | webhooks | Returns a webhook. Kept out of read: webhook records include the signing secret. |
| PATCH | rest/metadata/webhooks/{id} | write | webhooks | Updates a webhook. |
| DELETE | rest/metadata/webhooks/{id} | write | webhooks | Deletes a webhook. |
| GET | rest/webhooks | write | webhooks | Lists webhooks. Kept out of read: webhook records include the signing secret. |
| POST | rest/webhooks | write | webhooks | Creates a webhook. |
| GET | rest/webhooks/{id} | write | webhooks | Returns a webhook. Kept out of read: webhook records include the signing secret. |
| PATCH | rest/webhooks/{id} | write | webhooks | Updates a webhook. |
| DELETE | rest/webhooks/{id} | write | webhooks | Deletes a webhook. |
