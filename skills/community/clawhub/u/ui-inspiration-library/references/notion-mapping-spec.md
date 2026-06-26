# Notion database creation spec and field mapping

Use this reference to create the Notion database and map the structured analysis object into database properties.

## Recommended database properties

1. `Name` → title
2. `Image` → files
3. `Platform` → select
4. `Page Type` → multi_select
5. `Style Tags` → multi_select
6. `Component Tags` → multi_select
7. `Use Case` → multi_select
8. `Highlights` → rich_text
9. `Summary` → rich_text
10. `Reference Value` → select
11. `Source` → rich_text
12. `Captured At` → date

## Normalization rules before write

Before writing to Notion:
- trim whitespace,
- deduplicate exact repeated tags,
- normalize obvious synonym collisions,
- drop empty strings,
- preserve the chosen normalized tag format consistently.

## Notion implementation notes

If using Notion as the storage backend:
- keep database identifiers configurable,
- separate page/database creation from image upload if the API flow requires it,
- document API-version-specific behavior in implementation notes,
- avoid hardcoding personal workspace values in a public skill.

## Failure handling

If the record is created but one property cannot be written:
- preserve the highest-value fields first,
- report fallback behavior clearly,
- avoid silently dropping image or summary fields.
