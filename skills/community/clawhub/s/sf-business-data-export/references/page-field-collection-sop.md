# Page Field Collection SOP

Use this SOP when the export baseline depends on current page-visible fields instead of an explicit field list.

## Goal

Produce a reliable field list artifact that can be passed into `collect_metadata.py` as `--page-fields-file`.

## When Collection Is Required

Collect page-visible fields when:

- the user asks for the current page fields
- the export should mirror what a business user sees on the page
- no explicit field list was provided

Do not collect page-visible fields when:

- the user already supplied an explicit field list
- the export is intentionally based on a non-page field set

## Required Context

Before collecting page fields, determine:

- target object
- requested profile, if provided
- requested record type, if provided
- whether the user wants current page-visible fields or explicit fields

If profile and record type are both missing, use the current user's profile.
If multiple record types exist in that context, ask the user whether to proceed with an arbitrary record-type page or provide a record type explicitly.

## Collection Order

Resolve page-visible fields in this order:

1. Lightning page
2. `FlexiPage` field usage
3. `Layout`

The purpose of this order is:

- use the actual Lightning experience first
- use `FlexiPage` metadata to identify page-specific field usage
- use `Layout` only when Lightning metadata is unavailable or does not expose enough usable field information

## Minimum Output Artifact

Produce a plain text or JSON field list artifact containing field API names only.

Accepted formats:

- text file with one field API name per line
- JSON array of field API names

Example text artifact:

```text
Id
Name
StageName
Amount
CloseDate
OwnerId
```

## Validation Rules

Before handing the field list to downstream scripts:

- remove empty lines and duplicates
- keep field API names, not labels
- verify fields against `describe` where possible
- record the field source used: Lightning page, `FlexiPage`, `Layout`, or fallback explicit fields

## Failure and Fallback Rules

If collection fails at one step, apply the next documented fallback:

- if Lightning page resolution fails, try `FlexiPage` and then `Layout`
- if Lightning page exists but does not expose usable field information, fall back to `Layout`
- if page resolution is blocked by profile and record type ambiguity, ask the user or follow the proceed-confirmation rule
- if no reliable page-visible field set can be collected, ask for an explicit field list instead of inventing fields

## Handoff to Downstream Scripts

After collection:

1. save the field list artifact
2. pass it to `collect_metadata.py` through `--page-fields-file`
3. keep the chosen field source in the metadata bundle so the review package can explain where the fields came from
