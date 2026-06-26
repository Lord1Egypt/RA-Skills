---
templateId: items.fileUpload.common
componentType: item
version: 2.0
canonicalDslType: fileUpload
nativeType: NATIVE_FILE
description: Canonical contract for file-upload item templates.
---

# Purpose

Define the canonical contract, conditional rules, and output skeleton for `file-upload` items.

---

# Generation Rules (MANDATORY)

1. Load `templates/items/items._common.md` first.
2. Load `references/policies/memory-bank/40-components/apex.items.md` before drafting final item DSL.
3. Use this family only for `fileUpload` semantics and remove attributes that belong to other item families.
4. Keep scenario overlays in the family templates and keep reusable contract details in this common file.

---

# Variable Contract

| Name | Required | Type | Notes |
|---|---|---|---|
| itemName | yes | string | Page item static name such as `P10_STATUS`. |
| type | yes | enum | Must be `fileUpload`. |
| label.label | yes | string | Visible label text. |
| label.alignment | optional | enum | Label alignment when the label is shown. |
| layout.region | yes | alias | Host region static ID reference. |
| layout.sequence | yes | number | Rendering sequence within the region. |
| layout.slot | optional | enum | Region slot, typically `regionBody` for items rendered inside a host region. |
| layout.alignment | optional | enum | Item alignment inside the slot. |
| appearance.template | yes | alias | Family-appropriate template alias. |
| appearance.templateOptions | optional | array/string | Template modifiers such as `#DEFAULT#` or compact options. |
| settings.* | optional | variant | Normalized family settings such as `storageType`, `displayAs`, `allowMultipleFiles`, `fileTypes`, `maxFileSize`, `displayDownloadLink`, `downloadLinkText`, `contentDisposition`, `purgeFileAt`, `dropzoneTitle`, `dropzoneDescription`, and `captureUsing`. |
| validation.valueRequired | optional | boolean | Set when the item value is mandatory. |
| source.formRegion | conditional | alias | Required for form-bound upload items. |
| source.column | conditional | string | Primary file payload column. |
| source.dataType | conditional | enum | Data type for the stored payload, typically BLOB. |
| source.mimeTypeColumn | optional | string | Column storing the MIME type. |
| source.filenameColumn | optional | string | Column storing the uploaded file name. |
| source.characterSetColumn | optional | string | Column storing the character set when applicable. |
| source.blobLastUpdatedColumn | optional | string | Column storing the last-updated timestamp. |
| help.helpText | required by default | string | Builder help text or assistive guidance for visible user-facing file-upload items; omit only for hidden items or a documented exemption. |
| security.sessionStateProtection | optional | enum | Session state protection policy. |
| security.authorizationScheme | optional | alias | Authorization scheme alias when the item is conditionally visible. |

---

# Output Skeleton Template

```apexlang
pageItem {{itemName}} (
    type: fileUpload
    label {
        label: {{label.label}}
        alignment: {{label.alignment}}
    }
    layout {
        sequence: {{layout.sequence}}
        region: @{{layout.region}}
        slot: {{layout.slot}}
        alignment: {{layout.alignment}}
    }
    appearance {
        template: {{appearance.template}}
        templateOptions: {{appearance.templateOptions}}
    }
    settings {
        storageType: {{settings.storageType}}
        displayAs: {{settings.displayAs}}
        allowMultipleFiles: {{settings.allowMultipleFiles}}
        fileTypes: {{settings.fileTypes}}
        maxFileSize: {{settings.maxFileSize}}
        displayDownloadLink: {{settings.displayDownloadLink}}
        downloadLinkText: {{settings.downloadLinkText}}
        contentDisposition: {{settings.contentDisposition}}
        purgeFileAt: {{settings.purgeFileAt}}
        dropzoneTitle: {{settings.dropzoneTitle}}
        dropzoneDescription: {{settings.dropzoneDescription}}
        captureUsing: {{settings.captureUsing}}
    }
    validation {
        valueRequired: {{validation.valueRequired}}
    }
    source {
        formRegion: @{{source.formRegion}}
        column: {{source.column}}
        dataType: {{source.dataType}}
        mimeTypeColumn: {{source.mimeTypeColumn}}
        filenameColumn: {{source.filenameColumn}}
        characterSetColumn: {{source.characterSetColumn}}
        blobLastUpdatedColumn: {{source.blobLastUpdatedColumn}}
    }
    help {
        helpText: {{help.helpText}}
    }
    security {
        sessionStateProtection: {{security.sessionStateProtection}}
        authorizationScheme: @{{security.authorizationScheme}}
    }
)
```

---

# Conditional Rendering Rules

- Remove unsupported or unused blocks before finalizing the DSL.
- Omit `source {}` when the item is not bound to persisted data or a form region.
- Emit `validation {}` only when the scenario requires declarative checks.
- Keep the settings block lean and emit only the family-specific properties that are actually needed.

---

# Guardrails

- Follow guardrails in `references/policies/memory-bank/00-guard/ai.guard.md`.
- Do not invent unsupported attributes or UT classes.
- Keep placeholder names aligned with `templates/items/items._common.md`.
- Validate the storage strategy and metadata column mappings before finalizing upload items.
