# Guide 02 — Metadata Schema Standards

## Purpose

Every chunk written to Qdrant must carry a complete, well-structured metadata payload. This guide defines the universal schema, field confidence levels, payload indexing requirements, and source-specific extension namespacing.

The metadata schema is the **contract** between your ingestion pipeline and your retrieval + access control layers. Gaps in metadata cannot be corrected at retrieval time.

---

## Schema Version

Current version: **2.2**

Every chunk must include `schema_version: "2.2"`. When the schema evolves, bump this field and provide a migration guide.

---

## Metadata Confidence Levels

Every field has an implicit confidence level. This determines whether it can be used for filtering and security decisions.

| Level | Meaning | Can Filter On? | Can Use for Security? |
|---|---|---|---|
| `source_asserted` | Value came directly from the source system API | ✅ Yes | ✅ Yes |
| `system_derived` | Value computed deterministically by the pipeline | ✅ Yes | ✅ Yes |
| `model_inferred` | Value produced by an ML classifier or heuristic | ⚠️ Log only | ❌ No (unless separately validated) |

**Rule:** Never use `model_inferred` fields as the sole basis for sensitivity classification, access control, or routing decisions.

---

## Universal Payload Schema

Every chunk in every collection must carry all required fields below. No exceptions.

### Identity and Provenance

| Field | Type | Required | Description |
|---|---|---|---|
| `doc_id` | string | ✅ | Globally unique chunk identifier. Format: `{source}_{entity_id}_{chunk_index}`. Must be deterministic. |
| `source_type` | string | ✅ | Canonical source system name: `slack`, `fireflies`, `clickup`, `email`, `gdrive`, etc. |
| `source_system` | string | ✅ | Specific instance or workspace identifier (e.g., workspace name or URL). |
| `source_record_id` | string | ✅ | Native ID of the source record in the originating system. |
| `integration_id` | string | ✅ | Identifier of the integration pipeline that produced this chunk. |
| `parent_doc_id` | string | ✅ | ID of the parent document or conversation this chunk belongs to. |
| `document_content_hash` | string | ✅ | SHA-256 of the full normalized source document. Used for change detection. |

**Identifier Precedence:**
- Source identity: `source_system` + `source_record_id` uniquely identifies the original record.
- Content equivalence: `document_content_hash` detects whether source content changed.
- Chunk identity & upsert key: `doc_id` is the authoritative key for all Qdrant upsert/delete operations.
- Chunk deduplication: `content_hash` detects duplicate chunks within a source.

### Chunk Hierarchy

| Field | Type | Required | Description |
|---|---|---|---|
| `chunk_index` | integer | ✅ | Zero-based position of this chunk within its parent document. |
| `chunk_total` | integer | ✅ | Total chunks produced from the parent document. |
| `content_hash` | string | ✅ | SHA-256 of the normalized chunk text. Used for within-source deduplication. |

### Timestamps

| Field | Type | Required | Description |
|---|---|---|---|
| `created_at` | ISO 8601 | ✅ | When the original content was created in the source system. |
| `ingested_at` | ISO 8601 | ✅ | When this chunk was written to Qdrant. |
| `modified_at` | ISO 8601 | ✅ | When the original content was last modified in the source system. |
| `source_last_modified` | ISO 8601 | ✅ | Source system's own last-modified timestamp. |

All timestamps must be stored in **UTC** using ISO 8601 format: `2024-11-01T14:30:00Z`.

### Authorship

| Field | Type | Required | Description |
|---|---|---|---|
| `author_id` | string | ✅ | Unique ID of the content author in the source system. |
| `author_name` | string | ✅ | Display name of the content author. |
| `author_email` | string | Conditional | Required when available from the source system. |
| `author_department` | string | Conditional | Required when organizational directory mapping is available. |

### Organizational Context

| Field | Type | Required | Description |
|---|---|---|---|
| `project_ids` | string[] | Optional | List of project IDs. Empty array if source doesn't model projects. |
| `team_ids` | string[] | Optional | List of team IDs. Critical for permission scope resolution. Never fabricate. |
| `workspace_id` | string | ✅ | Workspace or tenant identifier. |
| `org_id` | string | ✅ | Top-level organization identifier. All retrieval is scoped to this value. |

### Governance and Classification

| Field | Type | Required | Description |
|---|---|---|---|
| `sensitivity` | enum | ✅ | One of: `public`, `internal`, `restricted`, `confidential`. Determines target collection. |
| `allowed_groups` | string[] | ✅ | Group IDs permitted to retrieve this chunk. Empty array for public content. |
| `owner_user_ids` | string[] | ✅ | User IDs with ownership rights. Empty array when not determinable. |
| `is_pii` | boolean | ✅ | Whether this chunk contains personally identifiable information. |
| `retention_days` | integer | ✅ | Days to retain before scheduled deletion. |
| `data_scope_tags` | string[] | ✅ | Structured labels describing data domain and organizational scope. See Scope Tags section below. |

### Content Descriptors

| Field | Type | Required | Description |
|---|---|---|---|
| `language` | string | ✅ | ISO 639-1 language code: `en`, `es`, `fr`, etc. |
| `content_type` | string | ✅ | Primary category: `message`, `transcript`, `document`, `task`, `email`. |
| `content_subtype` | string | Conditional | Refinement: `thread_reply`, `speaker_segment`, `attachment`. |
| `title` | string | Conditional | Document or conversation title, when available. |
| `summary` | string | Conditional | Natural-language summary. Confidence: `model_inferred`. Do NOT use for filtering. |

### Processing and Lineage

| Field | Type | Required | Description |
|---|---|---|---|
| `token_count` | integer | ✅ | Approximate token count of chunk text (use 4 chars/token heuristic). |
| `chunk_strategy` | string | ✅ | Chunking strategy used (e.g., `sentence_window`, `speaker_turn`, `paragraph`). |
| `embedding_model` | string | ✅ | Dense embedding model identifier. |
| `sparse_model` | string | ✅ | Sparse embedding model identifier. Use `"none"` for dense-only pipelines. |
| `schema_version` | string | ✅ | Metadata schema version. Current: `"2.2"`. |
| `ingestion_run_id` | string | ✅ | Unique identifier for the ingestion job or run. |
| `connector_version` | string | ✅ | Version of the source connector used. |
| `normalizer_version` | string | ✅ | Version of the normalization logic applied. |
| `chunker_version` | string | ✅ | Version of the chunking logic applied. |

---

## Data Scope Tags

`data_scope_tags` is the primary field for semantic-scope filtering. Tags describe **what the data is** — not who may access it.

Use the following controlled taxonomy. Custom tags require explicit definition and documentation before use.

| Namespace | Examples | When to Assign |
|---|---|---|
| Domain (no prefix) | `sales`, `support`, `finance`, `legal`, `hr`, `engineering`, `marketing`, `operations` | Content relates to this business domain. Derived from source metadata, folder, channel name. |
| Team scope (`team:`) | `team:sales_a`, `team:emea_support` | Content scoped to a specific team. Derived from `team_ids`. |
| Data category (`category:`) | `category:pipeline`, `category:forecast`, `category:compensation`, `category:contract` | Content falls into a specific data category with distinct access patterns. |
| Region (`region:`) | `region:emea`, `region:apac`, `region:americas` | Content is regionally scoped. |
| Project (`project:`) | `project:alpha`, `project:crm_migration` | Content associated with a specific named project. Derived from `project_ids`. |

**Tagging Rules:**
- Tags must use **lowercase snake_case**. No free-text values.
- Tags must be **stable**: same source record ingested twice → same tags.
- When organizational context cannot be determined, use an **empty array** (not fabricated tags).
- An empty `data_scope_tags` results in the broadest access (additive model). Do not speculate — when in doubt, omit the tag.
- A chunk may carry multiple tags across multiple namespaces.
- Do not add `model_inferred` tags as sole basis for security-relevant filtering.

---

## Source-Specific Metadata Namespacing

Source-specific fields must NOT be injected into the top-level payload. All source-specific fields go under a `source_metadata` object keyed by source type:

```json
{
  "source_metadata": {
    "slack": { "channel_id": "C03AB", "thread_ts": "1714500000.000000" },
    "email": null,
    "fireflies": null
  }
}
```

Only populate the namespace relevant to the current chunk's source. See source-specific schemas below.

### Slack Source Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `channel_id` | string | ✅ | Slack channel identifier. |
| `channel_name` | string | ✅ | Human-readable channel name. Used to derive `data_scope_tags`. |
| `channel_type` | enum | ✅ | `public`, `private`, `dm`, `group_dm`. |
| `thread_ts` | string | Conditional | Parent thread timestamp. Null if top-level. |
| `message_ts` | string | ✅ | Message timestamp. |
| `reaction_count` | integer | ✅ | Number of emoji reactions. |
| `reply_count` | integer | Conditional | Number of thread replies (top-level messages only). |
| `is_edited` | boolean | ✅ | Whether this message has been edited. |
| `ordering_index` | integer | ✅ | Zero-based position within thread or channel window. |

### Fireflies (Meeting Transcript) Source Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `meeting_id` | string | ✅ | Fireflies meeting identifier. |
| `meeting_title` | string | ✅ | Meeting title or subject. Used to derive `data_scope_tags`. |
| `meeting_date` | ISO 8601 | ✅ | Date and time the meeting occurred. |
| `attendee_ids` | string[] | ✅ | Identifiers of all meeting attendees. |
| `attendee_names` | string[] | ✅ | Display names of all attendees. |
| `speaker_id` | string | ✅ | Identifier of the speaker for this chunk. |
| `speaker_name` | string | ✅ | Display name of the speaker for this chunk. |
| `meeting_duration_mins` | integer | ✅ | Total meeting duration in minutes. |
| `transcript_segment_start_ms` | integer | ✅ | Millisecond offset of this chunk's start within the transcript. |

### ClickUp Source Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | ✅ | ClickUp task identifier. |
| `task_name` | string | ✅ | Task title. Used to derive `data_scope_tags`. |
| `task_status` | string | ✅ | Current task status: `open`, `in_progress`, `done`. |
| `list_id` | string | ✅ | ClickUp list identifier. |
| `list_name` | string | ✅ | List name. |
| `space_id` | string | ✅ | ClickUp space identifier. |
| `assignee_ids` | string[] | Conditional | Identifiers of assigned users. |
| `due_date` | ISO 8601 | Conditional | Task due date. Null if not set. |
| `priority` | string | Conditional | Task priority level. |
| `custom_fields` | object | Conditional | Key-value map of custom fields. Evaluate for tag derivation. |

### Email Source Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `message_id` | string | ✅ | RFC 5322 Message-ID. |
| `thread_id` | string | ✅ | Email thread/conversation identifier. |
| `subject` | string | ✅ | Email subject line. Used to derive `data_scope_tags`. |
| `from_address` | string | ✅ | Sender email address. |
| `to_addresses` | string[] | ✅ | Recipient email addresses. |
| `cc_addresses` | string[] | Conditional | CC recipients. |
| `has_attachments` | boolean | ✅ | Whether the email includes attachments. |
| `email_folder` | string | Conditional | Folder or label in source mailbox. |
| `is_reply` | boolean | ✅ | Whether this email is a reply in a thread. |

### Google Drive Source Metadata

| Field | Type | Required | Description |
|---|---|---|---|
| `file_id` | string | ✅ | Google Drive file identifier. |
| `file_type` | string | ✅ | Document type: `doc`, `sheet`, `slide`, `pdf`. |
| `mime_type` | string | ✅ | MIME type of the file. |
| `folder_path` | string | ✅ | Full folder path in Drive. Critical for sensitivity classification and tag derivation. |
| `last_editor_id` | string | Conditional | ID of last person to edit the file. |
| `version` | string | Conditional | Document version number or revision ID. |
| `share_scope` | enum | Conditional | `anyone`, `domain`, `specific`. Informs `allowed_groups` population. |

---

## Reference Payload Example

```json
{
  "doc_id": "slack_C03AB_1714500000_0",
  "source_type": "slack",
  "source_system": "workspace-name",
  "source_record_id": "1714500000.000000",
  "integration_id": "slack-ingester-v3",
  "parent_doc_id": "slack_C03AB_thread_1714499900",
  "document_content_hash": "a3f1c29e...",
  "chunk_index": 0,
  "chunk_total": 1,
  "content_hash": "b7d2e44f...",
  "created_at": "2024-04-30T18:00:00Z",
  "ingested_at": "2024-04-30T18:05:00Z",
  "modified_at": "2024-04-30T18:00:00Z",
  "source_last_modified": "2024-04-30T18:00:00Z",
  "author_id": "U012AB3CD",
  "author_name": "Jane Smith",
  "author_email": "jane@company.com",
  "author_department": "Sales",
  "project_ids": [],
  "team_ids": ["team_sales_a", "team_sales_b"],
  "workspace_id": "workspace-123",
  "org_id": "org-456",
  "sensitivity": "internal",
  "allowed_groups": ["g_all_staff"],
  "owner_user_ids": [],
  "is_pii": false,
  "retention_days": 1095,
  "data_scope_tags": ["sales", "team:sales_a", "team:sales_b", "category:pipeline", "region:emea"],
  "language": "en",
  "content_type": "message",
  "content_subtype": "thread_reply",
  "title": null,
  "summary": null,
  "token_count": 187,
  "chunk_strategy": "sentence_window",
  "embedding_model": "BAAI/bge-m3",
  "sparse_model": "BAAI/bge-m3-splade",
  "schema_version": "2.2",
  "ingestion_run_id": "run_2024043001",
  "connector_version": "1.4.2",
  "normalizer_version": "2.1.0",
  "chunker_version": "3.0.1",
  "source_metadata": {
    "slack": {
      "channel_id": "C03AB",
      "channel_name": "sales-emea-pipeline",
      "channel_type": "public",
      "thread_ts": "1714499900.000000",
      "message_ts": "1714500000.000000",
      "reaction_count": 2,
      "is_edited": false,
      "ordering_index": 3
    }
  }
}
```

---

## Payload Indexing Requirements

**Every field used as a filter in Qdrant queries MUST have a payload index created.** Filtering on unindexed fields causes full collection scans and degrades performance.

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="...")

# Index sensitivity (most important — used in every query)
client.create_payload_index(
    collection_name="company_memory",
    field_name="sensitivity",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

# Index org_id for tenant isolation (use is_tenant=True for multi-tenant)
client.create_payload_index(
    collection_name="company_memory",
    field_name="org_id",
    field_schema=models.KeywordIndexParams(type="keyword", is_tenant=True),
)

# Index allowed_groups for group-based access
client.create_payload_index(
    collection_name="company_memory",
    field_name="allowed_groups",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

# Index data_scope_tags for scope-based filtering
client.create_payload_index(
    collection_name="company_memory",
    field_name="data_scope_tags",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

# Index team_ids for team-scoped queries
client.create_payload_index(
    collection_name="company_memory",
    field_name="team_ids",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

# Index timestamps for recency filtering
client.create_payload_index(
    collection_name="company_memory",
    field_name="created_at",
    field_schema=models.PayloadSchemaType.DATETIME,
)

# Index source_type for source-specific queries
client.create_payload_index(
    collection_name="company_memory",
    field_name="source_type",
    field_schema=models.PayloadSchemaType.KEYWORD,
)
```

**Fields to always index:** `sensitivity`, `org_id`, `workspace_id`, `allowed_groups`, `data_scope_tags`, `team_ids`, `source_type`, `is_pii`, `created_at`, `content_type`.
