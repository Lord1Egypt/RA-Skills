# Files — Uploading, Linking and Downloading Documents

**Before a file migration or a re-run of one**, read `loads/<year>.md` and the source-to-document map in `artifacts/` if the `## Boxes` index names one: files have no external id, so that map is the only thing that makes a second run safe.

Files are the one part of the Salesforce API where the record model and the transport are both unusual: three objects for one document, two storage allocations, and no bulk path.

**Contents:** [The Three Objects](#the-three-objects) · [Upload](#upload) · [Multipart vs Base64](#multipart-vs-base64) · [Link to Records](#link-to-records) · [New Versions](#new-versions) · [Download](#download) · [Find a Record's Files](#find-a-records-files) · [Delete](#delete) · [Legacy Attachments](#legacy-attachments) · [Migrating Files](#migrating-files) · [File Traps](#file-traps)

## The Three Objects

| Object | Is | Note |
|---|---|---|
| `ContentVersion` | One version's bytes and metadata | You insert this; the rest is created for you |
| `ContentDocument` | The logical file across its versions | Read-only in practice; deleting it deletes everything |
| `ContentDocumentLink` | The attachment of a document to a record | One document can link to many records |

Insert a `ContentVersion` with no `ContentDocumentId` and Salesforce creates the `ContentDocument` for you and returns the version id. You then read the version's `ContentDocumentId` and link it where it belongs — two steps, always, and skipping the second leaves an uploaded file attached to nothing.

## Upload

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/sobjects/ContentVersion" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"Title":"Signed contract","PathOnClient":"contract.pdf","VersionData":"<base64>"}'
```

- `PathOnClient` carries the file name **and its extension** — that is where the file type comes from. Omit the extension and the file downloads as an unrecognized blob.
- `Title` is what users see; it does not need the extension.
- `FirstPublishLocationId` set to a record id links the file to that record on creation, saving the second call — convenient, but it only works on the first version.

## Multipart vs Base64

Base64 inflates a payload by roughly one third (4 bytes out for every 3 in). A 30 MB file becomes about 40 MB of JSON, so the practical ceiling arrives sooner than the file-size limit suggests.

For anything beyond a few megabytes, use the multipart form:

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/sobjects/ContentVersion" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -F 'entity_content={"Title":"Signed contract","PathOnClient":"contract.pdf"};type=application/json' \
  -F 'VersionData=@contract.pdf'
```

The JSON part must be named `entity_content` and declared as `application/json`; the binary part takes the name of the blob field (`VersionData` for ContentVersion, `Body` for Attachment). Getting either name wrong produces a parser error that says nothing about names.

Size ceilings differ by object and upload path — legacy `Attachment` tops out at a couple of dozen megabytes, Salesforce Files go far higher — and they vary by edition and release. Check the org before designing around a specific number rather than trusting a figure in any document.

## Link to Records

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/sobjects/ContentDocumentLink" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"ContentDocumentId":"069xx0000012345","LinkedEntityId":"001xx0000012345",
       "ShareType":"V","Visibility":"AllUsers"}'
```

- `ShareType`: `V` viewer, `C` collaborator, `I` inferred from the record's sharing. `V` is the safe default for an integration.
- `Visibility`: `AllUsers` for internal plus community where enabled, `InternalUsers` to keep it off portals. Getting this wrong is how an internal document appears in a customer community.
- Linking the same document to a second record is a second link row, not a second upload. That is the entire advantage of Files over Attachments.

## New Versions

Insert another `ContentVersion` carrying the existing `ContentDocumentId`. Salesforce increments the version and keeps the history; `IsLatest` marks the current one. Do **not** delete and re-upload — that breaks every link and loses the history.

## Download

```bash
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/ContentVersion/068xx0000012345/VersionData" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" --output contract.pdf
```

The blob endpoint returns raw bytes, not JSON. Piping it into a JSON parser is the most common first mistake; writing it to a file is the whole API.

## Find a Record's Files

```sql
SELECT ContentDocumentId, ContentDocument.Title, ContentDocument.FileExtension,
       ContentDocument.ContentSize, ContentDocument.LatestPublishedVersionId
FROM ContentDocumentLink WHERE LinkedEntityId = '001xx0000012345'
```

`ContentDocumentLink` **cannot be queried without a filter** on `LinkedEntityId` or `ContentDocumentId` — an unfiltered query is rejected outright. There is no "list every file in the org" query through this object; that is a report or a Bulk export of `ContentDocument`.

## Delete

Deleting the `ContentDocument` deletes every version and every link. Deleting a single `ContentVersion` is not how you remove a file. Deleting a `ContentDocumentLink` unlinks the file from one record while leaving it in place elsewhere — usually what "remove this attachment" actually means.

## Legacy Attachments

`Attachment` (with `ParentId` and a base64 `Body`) and `Document` predate Files and still hold data in older orgs. They attach to exactly one parent, do not version, and are not what new work should create. When both exist in an org, a "find all documents" task means querying both — and a migration to Files is a per-record read-and-rewrite, not a conversion setting.

## Migrating Files

The expensive phase of every migration, and the one most often underestimated:

- **There is no bulk path for binary content.** Bulk 2.0 carries CSV, not blobs, so files move one API call at a time — 50,000 documents is 50,000 calls plus the links, which is an allocation plan of its own (`limits.md`).
- Files consume **file storage**, a separate allocation from data storage. Check `FileStorageMB` in `/limits` before starting; running out fails the writes partway through.
- Load the parent records first; the link needs a `LinkedEntityId` that exists (`migration.md`).
- Keep the source-path-to-`ContentDocumentId` map from the run in `artifacts/<kebab-name>.md`, with its `## Boxes` line. Without it, a re-run duplicates every document, and files have no external id field to make the operation idempotent — the mapping file *is* the idempotency mechanism.
- Rate-limit deliberately and run off hours. A file loop at full speed is the most reliable way to hit the concurrency ceiling.

## File Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Uploading without linking | The file exists and no record shows it | Insert the version, then the link — or use `FirstPublishLocationId` |
| No extension in `PathOnClient` | Salesforce cannot type the file; it downloads as a blob | Always include it |
| Base64 for large files | 33% inflation plus request-size ceilings | Multipart form upload |
| Parsing the download as JSON | The blob endpoint returns bytes | Write to a file |
| Delete-and-reupload to update | Breaks every link and loses version history | New `ContentVersion` with the same `ContentDocumentId` |
| Querying `ContentDocumentLink` unfiltered | Rejected by design | Filter on `LinkedEntityId` or `ContentDocumentId` |
| Planning a file migration like a data migration | No bulk path; calls scale with document count | Budget one call per file, plus links, and run off hours |
| `Visibility: AllUsers` on internal documents | Exposes them in communities | `InternalUsers` unless the file is meant to be external |

**After a file migration or a bulk upload**, append the row to `loads/<year>.md` (count, storage consumed, elapsed) and keep the source-to-`ContentDocumentId` map as `artifacts/<kebab-name>.md` with its `## Boxes` line — it is the only thing that makes a re-run safe.
