# Structured image storage

Structured image storage organises images (e.g. photos of sites) in categories per
scope. Images are file objects linked to the parent object.

## Concept

- Every scope has a set of defined **categories** (e.g. "Exterior view" ("Aussenansicht"),
  "Key safe / location" ("Schlüsseltresor / Position")).
- **Important for `upload_file_to_object`:** The `name` parameter (the category filename) must
  correspond **exactly** to the `imagename` of the target category — only then does the image
  land in the right category. Without an exact match the image is not assigned to the category.
- Only one category is marked as thumbnail — its image appears as the preview/title image
  of the object (e.g. in map or list views). Other categories are additional
  documentation but do not appear as a preview image.

## The categories can be read AND set via MCP

There are dedicated tools for this — the categories no longer have to be maintained via the
web interface:

| Tool | Purpose |
|---|---|
| `onto_scope_structuredimage_categories` | **Read** the categories of a scope (`scope_id`) |
| `onto_scope_save_structuredimage_categories` | **Write** categories (`scope_id` + `categories`) |
| `onto_file_structured` | Image list **of an object** (which category is filled, which is empty?) |
| `upload_file_to_object` | Upload image (`type: structuredimage`, `name` = imagename) |

All scope/file tools are visible to the `member` role; writing additionally requires
**`can_manage_scope`** on the scope (403 otherwise).

### Reading categories

```json
{"name":"onto_scope_structuredimage_categories","arguments":{"scope_id":<SCOPE_ID>}}
```

### Setting categories

```json
{"name":"onto_scope_save_structuredimage_categories","arguments":{
  "scope_id":<SCOPE_ID>,
  "categories":[
    {"imagename":"01_<Motiv>.jpg","caption":"<Bezeichnung>","language":"de",
     "info":"<Beschreibung>","thumbnail":true,"versioned":false},
    {"imagename":"01_<Motiv>.jpg","caption":"<Label>","language":"en",
     "info":"<Description>","thumbnail":true,"versioned":false},
    {"imagename":"02_<Motiv>.jpg","caption":"<Bezeichnung>","language":"de",
     "info":"<Beschreibung>","thumbnail":false,"versioned":false}
  ]
}}
```

Field rules per entry:

- **`imagename`** — required. MUST match the filename of the upload (see below).
- **`caption`** — display name in the UI/app.
- **`info`** — photography hint for the human (what should be in the picture?).
- **`language`** — `de` / `en`. **Multiple entries with the same `imagename` are language variants**
  of the same category, not duplicates.
- **`thumbnail`** — `true` = this image is the preview image of the object. Multiple `true`
  are possible (the order or the existing image then decides).
- **`versioned`** — `true` = multiple shots of the same category are kept as
  versions (e.g. recurring inspections); `false` = one image per category.
- **The order of the list determines the display order.**

**The write operation replaces the list completely** — whoever only wants to add one category
reads first, appends and writes the whole list back. Otherwise the remaining categories are gone.

## The name match is the decisive point

The slot match runs via `filename == imagename`. In practice this means:

| File (upload `filename` **and** `name`) | Category `imagename` | Result |
|---|---|---|
| `01_<Motiv>.jpg` | `01_<Motiv>.jpg` | ✅ slot filled |
| `<Motiv>.jpg` | `01_<Motiv>.jpg` | ❌ placeholder only |
| `IMG_4711.jpg` | `01_<Motiv>.jpg` | ❌ placeholder only |

A prefix (`01_`, `02_` …) is **part of the name** and must be included. Before building your own
naming convention, always check this match.

## Example: documenting a site (agent, without write permission on the foreign scope)

```
onto_scope_structuredimage_categories  scope_id=<scope>     → welche Kategorien gibt es?
onto_file_structured  object_id=<udid>                       → welche ist noch leer?
upload_file_to_object type=structuredimage, name=<Kategorie-Dateiname> → hochladen
```

If the target scope is only available read-only, the upload lands in your **own**
write scope via the SSR cascade — the category assignment on the foreign object still works.

## Example: a typical category set

A category set consists of one file per motif and language (fictional example):

```
01_<Motiv>.jpg         de "<Motiv>"          en "<Motive>"        thumbnail=true
02_<Motiv>.jpg         de "<Motiv>"          en "<Motive>"        thumbnail=true
03_<Motiv>.jpg         de "<Motiv>"          en "<Motive>"        thumbnail=true
```
All with `versioned: false`. More extensive motif sets are possible.

## Further settings (scope, not category)

Two scope rights control who may store structured images at all:
`can_upload_structuredimage` and `can_upload_file`.

A user without this right receives a placeholder instead of an error on app upload —
when "my image doesn't appear", check the categories first (match!), then this flag.
