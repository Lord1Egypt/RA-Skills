# Data Hydration Policy

Decide this with the user before enabling preview database hydration.

## Questions To Ask

```text
What initializes persistent develop?
What hydrates feature/agent preview databases?
Should previews copy auth users?
Should previews copy public table data?
Should previews copy storage objects?
Should previews use scrubbed/synthetic seed data instead?
Are there privacy or compliance limits on copying production data?
```

## Recommended Default

```text
production/default schema -> persistent develop
persistent develop data   -> feature/agent previews
local Docker Supabase     -> migrations + seed only
```

Do not copy production data into preview databases unless the user explicitly approves it and confirms privacy/compliance requirements.

## Branch Creation vs Data Hydration

Supabase branch creation and data hydration are separate concepts, and the split is forced by the platform: Supabase cannot create a preview branch from another branch project (the API returns `Cannot create preview branch from another branch project`). Preview branches must be created under the production/default project.

So a Supabase preview branch is created under the production/default project (schema only), while its usable app data is hydrated separately from persistent develop or seed scripts. Do not try to "simplify" this by creating previews from the develop branch — it will fail.

Document both:

```text
Branch creation source:
Data hydration source:
Auth copy policy:
Public data copy policy:
Storage copy policy:
Seed/scrub policy:
```

## Config Fields

Use or adapt these fields in `branching-config.json`:

```json
{
  "supabase": {
    "schemaBranchCreateSource": "production-default",
    "developHydrationSource": "production-default",
    "previewHydrationSource": "develop"
  },
  "preview": {
    "hydrateFromDevelop": true,
    "syncAuthConfig": false,
    "copyAuthUsers": false,
    "copyPublicData": false,
    "includePublicTables": [],
    "excludePublicTables": [],
    "storageBuckets": [],
    "copyStorageBuckets": []
  }
}
```

Defaults should be conservative: create isolated previews, apply migrations, and avoid copying real production data unless approved.

## Implementation Notes

- `storageBuckets` creates buckets in the preview project.
- `copyStorageBuckets` copies objects from the hydration source to the preview.
- `copyAuthUsers` requires `PREVIEW_USER_PASSWORD`; copied users cannot keep their original password hashes.
- `copyPublicData` truncates and refills selected public tables in the preview database.
- `includePublicTables` limits copying to specific public tables.
- `excludePublicTables` prevents copying specific public tables.
- `syncAuthConfig` copies selected Supabase Auth configuration to the preview branch.

If the user wants scrubbed data, add a project-specific scrub step before enabling public table copying.

