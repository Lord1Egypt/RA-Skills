---
name: sf-business-data-export
description: Export Salesforce business data into business-readable Excel files from natural-language requests. Use when pull large Salesforce datasets beyond Report limits, map layout-visible fields into readable exports, generate object-level SOQL, handle polymorphic relationship fields, traverse parent-child relationships, run two-step detail queries, export through SOAP with queryMore, or prepare review materials for business users.
---

# SF Business Data Export

Interpret the user's request as a data-export task, not just a query-writing task. Produce files that business users can review directly.

## Checklist Summary

Current status: ready for limited real-world trial use.

Checklist conclusion:
- target definition: passed
- Definition of Done: passed
- input definition: passed
- execution flow: passed
- result verifiability: passed
- failure handling and degradation: passed
- reusable logic extraction into `scripts/` and `references/`: mostly passed
- minimum practical workflow closure: mostly passed

Current strengths:
- the skill now has explicit execution rules, validation rules, fallback rules, and result-reporting rules
- the skill no longer depends on hidden operator knowledge for core workflow decisions
- bundled references, scripts, sample inputs, and SOP documents support repeatable local execution

Known remaining gaps:
- there is not yet a single orchestration command that runs the full export flow from Salesforce retrieval through review package output
- current page field collection still depends on execution-time metadata collection or an explicit field list artifact, which is acceptable but not fully automated

Recommended next step:
- validate the skill with one or two real export requests and use the trial runs to decide whether a full orchestration script is needed

## Normalize the Request

Convert the natural-language request into an export definition before writing SOQL:
- target objects
- business purpose
- time range
- filter conditions
- whether the export is for business review
- whether to use current page-visible fields as the baseline field set
- whether owner, parent-owner, or other relationship context must be included
- desired output format

If the request is ambiguous, prefer a conservative, review-oriented export that includes more context fields rather than fewer.

## Input Definition

Normalize every request into explicit execution inputs before reading metadata or writing SOQL.

Required inputs:
- target object or objects
- business question or review purpose
- field source, choosing either current page-visible fields or an explicit field list
- scope definition from time range, filter conditions, parent-scope conditions, or an explicit full-scope export
- output intent, distinguishing review-ready export from raw extraction

Optional inputs:
- explicit field list
- key fields that must be present in the export
- output format
- language preference for labels
- consolidation preference across objects
- profile name
- record type name for each target object
- owner, parent-owner, or other relationship context

Input fallback rules:
- if current page-visible fields cannot be determined reliably, fall back to an explicit field list instead of assuming success
- if scope is not provided, record the export as full-scope rather than inventing additional filters
- if multiple objects are requested, normalize fields, filters, and record type context per object instead of assuming one shared configuration
- if key fields are not explicitly named, do not invent them; only treat explicitly requested key fields as mandatory

## Page Resolution Rules

When current page-visible fields are used as the field baseline, resolve the page in this order:
1. find the relevant Lightning page first
2. if no Lightning page is available, or the Lightning page does not provide usable field information, fall back to the Page Layout

Profile and record type rules:
- if the user specifies a profile, check whether the target object has multiple record types in that profile context
- if the user specifies a record type for an object but does not specify a profile, resolve the page using the current user's profile
- if the user specifies both a profile and record types for all target objects, resolve pages directly from that combination

Ambiguity handling for page resolution:
- if the user specifies a profile and the target object has multiple record types but the user does not specify which record type to use, ask the user to provide the record type before continuing
- if the user does not specify either profile or record type, default to the current user's profile
- if the user does not specify either profile or record type and an object has multiple record types, tell the user that the workflow will use the current user's profile and may choose a record-type page arbitrarily, then ask whether to proceed
- do not claim that page-visible fields are reliable until the page resolution path is known

## Execution Flow

Execute in this order unless there is a concrete reason to deviate.
Apply steps 3 through 8 per object when the request includes multiple objects.

1. Normalize the request into an export definition.
2. Validate minimum executable inputs.
3. Resolve page context for each object.
4. Resolve the field baseline for each object.
5. Generate a business-readable field catalog for each object.
6. Choose the query strategy for each object in a fixed order.
7. Export data for each object through Salesforce SOAP `query` and `queryMore`.
8. Validate per-object outputs against the DoD checks.
9. Assemble the manifest and review package outputs.
10. Mark the export as complete only if all requested objects pass validation.

Flow rules:
- do not move to metadata retrieval or SOQL generation until the minimum executable inputs are known
- if an object cannot resolve current page-visible fields reliably, fall back to an explicit field list before continuing
- if fallback still does not provide a reliable field baseline, stop that object and record the failure instead of inventing fields
- do not reuse unresolved page context, record type assumptions, or field baselines across different objects
- do not treat an object as successfully exported until output validation passes

Query strategy selection order:
1. use a direct query when the object can be filtered and selected without special handling
2. apply polymorphic owner handling when `OwnerId.referenceTo` requires it
3. apply parent traversal when scope is determined from a parent object
4. apply a two-step detail query when one-query filtering is not reliable or supported

Failure and stop conditions:
- if profile and record type ambiguity blocks page resolution, ask the user or follow the documented proceed-confirmation rule before continuing
- if required metadata such as `describe`, Lightning page, `FlexiPage`, or `Layout` cannot be retrieved and no reliable fallback exists, mark the affected object as failed
- if the generated SOQL cannot be made valid for the required scope, do not silently downgrade the export; mark the affected object as failed
- if row count, field coverage, or object completeness validation fails, do not mark the export as complete

## Field Selection

Use retrieved Lightning page metadata as the primary source for current page-visible fields when it provides usable field information.
If Lightning page metadata is unavailable or does not expose enough field information, fall back to `Layout` metadata.
Use `FlexiPage` metadata to identify page-specific field usage before falling back to `Layout`.
Do not assume Report columns are sufficient.

When building export columns:
- include resolved page-visible business fields first
- include key technical identifiers such as `Id`, `OwnerId`, and lookup ids when they are useful for traceability
- include review-assistance fields such as owner name, sales team, sales group, parent opportunity name, or parent owner fields when they affect decision-making
- exclude fields that are not present in `describe` results even if they appear in layout metadata

Prefer Chinese labels for the final Excel header row when labels are available.

## Query Strategy

Choose the query pattern by object shape.

### Direct owner objects

If `OwnerId.referenceTo` is only `User`, query owner fields directly, for example:
- `Owner.Name`
- `Owner.CRM_Sales_Team__c`
- `Owner.CRM_Sales_Group__c`

### Polymorphic owner objects

If `OwnerId.referenceTo` includes both `User` and `Group`, do not rely on `Owner.Custom_Field__c` in `WHERE`.
Use this pattern instead:
- filter with `OwnerId IN (SELECT Id FROM User WHERE ...)`
- expose owner context in `SELECT` with `TYPEOF Owner ...`

This pattern avoids failures like `No such column ... on entity 'Name'`.

### Parent traversal objects

If the current object does not expose owner or scope fields directly, determine scope from the parent object.
Typical pattern:
- current object has `CRM_Opportunity__c`
- scope is determined from `Opportunity.Owner`
- query with parent semi-join where supported

### Detail objects requiring two-step queries

If a detail object cannot be filtered cleanly in one SOQL query, use a staged approach:
1. export parent ids with the full scope filter
2. split parent ids into chunks
3. query child/detail rows with `IN (...)`
4. merge all rows into one export file

Use this approach for objects like order details when SOQL relationship filtering is too limited.

## Export Requirements

Export through Salesforce SOAP API using `query` and `queryMore` when result volume or column flexibility exceeds Report usefulness.
Do not stop at CSV if the user asked for business review output.
Generate `.xlsx` files with:
- Chinese label headers when available
- one file per object unless the user requests consolidation
- a manifest containing object name, file path, row count, and column count

## Definition of Done

Treat the export as complete only when all requested objects have review-ready outputs and all validation checks pass.

Minimum required outputs:
- a field catalog for each exported object
- an object-level SOQL file for each exported object
- an `.xlsx` file for each exported object unless the user explicitly requests a different format
- a manifest summarizing all outputs and validation results

Field coverage rules:
- determine the expected field set from either current page-visible fields or fields explicitly requested by the user
- output a field catalog containing at least API name, user-language label when available, source of inclusion, and export status
- count field coverage as `exported expected fields / total expected fields`
- treat the export as passing field coverage when expected field coverage is at least 70 percent
- if the user explicitly requested key fields, do not treat those as optional; if any key field is missing, mark the object as failed unless the field is unavailable in `describe` or inaccessible due to permissions and this is called out in the manifest

Row count validation rules:
- record the row count returned by each SOQL query
- record the final row count written into each Excel file
- if the export uses staged queries, chunking, or merge steps, also record raw row count before deduplication and final row count after deduplication
- treat any mismatch between expected final query row count and final Excel row count as a failure

Object completeness rules:
- the number of requested objects must match the number of output object files
- do not silently skip objects that fail due to permissions, unsupported query patterns, missing metadata, or other blockers
- list failed objects explicitly in the manifest with the reason for failure

Review-readiness rules:
- use user-language labels for headers when available, preferring Chinese labels when available
- include traceability fields such as ids and relevant lookup ids when needed to support review
- call out records that require manual review because they cannot be safely classified by rules alone

## Applicability

Use this skill when the task is to turn a Salesforce business question into review-ready data exports rather than only produce SOQL.

Good fit:
- medium to large exports where Salesforce Reports are insufficient for field coverage, row volume, or relationship handling
- exports that must be readable by business users in Excel
- exports that depend on layout-visible fields, owner context, parent-owner context, or parent-child traversal
- exports that require polymorphic owner handling, two-step detail querying, or manifest-based validation

Not a good fit:
- requests that only need a temporary SOQL statement and no file outputs
- requests that only need raw CSV extraction and do not require business-readable labels or review materials
- ultra-large throughput-first extraction jobs where Bulk API is a better fit than SOAP query/queryMore
- exports whose business classification rules are still undefined and cannot be resolved conservatively

When the request is ambiguous, prefer a conservative review-oriented export with more context fields, but do not claim success if requested objects, required fields, or validation outputs are missing.

## Dependencies

This skill assumes the execution environment can both query Salesforce and produce review-ready files locally.

Required capabilities:
- authenticated Salesforce access through Salesforce CLI
- ability to retrieve object `describe` metadata
- ability to retrieve `Layout` metadata for business-visible field selection
- ability to retrieve `FlexiPage` metadata when page-specific fields must supplement layout fields
- ability to execute Salesforce SOAP `query` and `queryMore`
- ability to generate `.xlsx` files locally

Current page field baseline:
- if the export is defined by current page-visible fields, the workflow must have a reliable source for those fields from metadata or user-provided context
- if current page-visible fields cannot be determined reliably, fall back to explicit user-requested fields or ask for the field list instead of assuming success

Validation outputs are mandatory:
- field catalogs must show what was expected, what was exported, and what was missing
- manifests must show per-object output files, row counts, column counts, and failure reasons when present

## Result Verifiability

Every export result must be independently verifiable by a user reviewing the output package.

The result package must make the following visible for each object:
- what was done
- what was not done
- what evidence was used
- where failures occurred
- what the user should do next when the export is incomplete

Completed work must be visible:
- list every generated file for the object
- show the resolved field baseline and the final exported field set
- show the row counts used for validation
- show whether the object passed or failed validation

Incomplete work must be visible:
- list missing fields, skipped objects, failed objects, and unresolved page-resolution cases explicitly
- do not hide fallback behavior such as switching from current page-visible fields to an explicit field list
- do not report partial object output as complete if validation did not pass

Evidence must be visible:
- keep the field catalog, object-level SOQL, and manifest as user-reviewable artifacts
- record the field source used for the export, such as Lightning page, `FlexiPage`, `Layout`, or explicit user-provided fields
- record the validation evidence used to determine success or failure, including field coverage and row-count comparisons

Failure location must be visible:
- identify the failed stage for each failed object, such as page resolution, metadata retrieval, field resolution, SOQL generation, SOAP export, Excel generation, or validation
- record a short reason that explains the blocker without forcing the user to inspect logs first

Next actions must be visible:
- when the export is incomplete, tell the user the next action needed to proceed, such as providing a record type, providing an explicit field list, confirming profile-based page selection, fixing permissions, or retrying after metadata access is available
- if no safe automatic continuation exists, say that clearly instead of implying that the export can continue unchanged

## Failure Handling and Degradation

Handle failures by using explicit fallback rules first, then recording object-level failure when no safe fallback remains.
Do not convert unresolved failures into silent partial success.

Failure categories:
- input ambiguity
- page resolution failure
- metadata failure
- field resolution failure
- query generation failure
- export execution failure
- validation failure

Default handling by failure category:
- input ambiguity: ask the user when the ambiguity changes page resolution, scope, key fields, or requested objects; otherwise follow the documented fallback or proceed-confirmation rule
- page resolution failure: fall back through the documented page resolution order; if no reliable page source remains, fail the affected object
- metadata failure: retry only through documented metadata fallbacks such as Lightning page to `Layout`; if required metadata still cannot be retrieved, fail the affected object
- field resolution failure: fall back from current page-visible fields to an explicit field list when available; if no reliable field baseline can be established, fail the affected object
- query generation failure: try the next allowed query strategy only when it preserves the requested scope and review intent; if no valid strategy remains, fail the affected object
- export execution failure: fail the affected object and preserve generated evidence such as SOQL, field catalogs, partial counts, or error messages
- validation failure: keep the generated artifacts for inspection, but mark the affected object as failed

Allowed degradation paths:
- Lightning page field resolution to `Layout` field resolution
- current page-visible field baseline to explicit user-provided field list
- direct query strategy to polymorphic owner handling when required by object shape
- direct or polymorphic query strategy to parent traversal when scope must be resolved from a parent object
- one-query detail extraction to a two-step detail query when one-query filtering is not reliable or supported

Disallowed degradation paths:
- do not narrow the requested scope only to make the query succeed
- do not remove explicitly requested key fields without recording object failure
- do not replace failed validation with a warning while still marking the object as successful
- do not silently skip objects, fields, or relationship context to produce a cleaner-looking output package

Object-level and job-level rules:
- evaluate success and failure per object first
- allow successful objects to keep their generated outputs even if another object fails
- if any requested object fails, do not mark the overall export as complete
- when the overall export is not complete, state which objects succeeded, which failed, and what action is required to continue

## Review Package Output

When the export is for review, follow the Definition of Done output and validation requirements.
Use the review package step to assemble the required field catalogs, object-level SOQL files, Excel files, and manifest into a business-readable handoff.

## Bundled Resources

Use scripts in `scripts/` for deterministic tasks instead of rewriting logic in the prompt.
Add references in `references/` for:
- `polymorphic-owner-patterns.md`
- `parent-traversal-patterns.md`
- `review-package-format.md`
- `end-to-end-usage.md`
- `page-field-collection-sop.md`
- sample inputs under `references/examples/`

Provide deterministic scripts in `scripts/` for:
- `preflight_check.py`
- `collect_metadata.py`
- `build_field_catalog.py`
- `validate_export_results.py`
- `write_review_manifest.py`

Keep `SKILL.md` focused on decision-making and workflow. Move object-specific mappings and reusable implementation details into scripts or references.
