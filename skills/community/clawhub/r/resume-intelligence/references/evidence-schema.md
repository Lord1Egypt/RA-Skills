# Evidence Schema

Use this reference when a run needs structured evidence that can support resume writing, interview preparation, job scoring, redaction, and run summaries.

The Markdown `evidence.md` file remains the human-readable source. A future `evidence.json` companion may use this schema for deterministic checks.

## Evidence Object

```json
{
  "schema_version": "1.0",
  "candidate_context": {
    "target_roles": ["Staff Platform Engineer"],
    "target_seniority": "staff",
    "years_of_experience": 12,
    "location_preference": "United States remote or hybrid"
  },
  "source_contexts": [
    {
      "id": "local-docs-platform",
      "type": "local-docs",
      "display_name": "Platform project documents",
      "host": "/approved/folder",
      "identity": "user-provided",
      "credential_boundary": "local-filesystem",
      "access_method": "local file",
      "scope": "approved folder and nested files",
      "inventory_reference": "source-inventory.md",
      "tool_usage_reference": "tool-usage-log.md",
      "disclosure_level": "internal-summary-only",
      "quoting_rule": "summarize-only",
      "status": "used"
    }
  ],
  "claims": [
    {
      "id": "claim-001",
      "source_context_id": "local-docs-platform",
      "employer_or_org": "Company Name",
      "role_title": "Staff Platform Engineer",
      "date_range": "2021-2024",
      "project_or_workstream": "Platform Reliability Program",
      "user_ownership": "Led architecture and rollout",
      "responsibilities": ["Designed service health standards", "Improved deployment workflow"],
      "technologies": ["Kubernetes", "Terraform", "Observability"],
      "scale": "Multiple engineering teams",
      "impact": "Improved reliability and developer productivity",
      "metrics": [
        {
          "name": "Incident reduction",
          "value": "needs-user-input",
          "context": "User needs to provide before-and-after incident count"
        }
      ],
      "confidence": "medium",
      "disclosure_level": "internal-summary-only",
      "resume_use": "include-sanitized",
      "missing_user_question": "What measurable reliability, incident, latency, cost, or productivity change came from this work?"
    }
  ]
}
```

## Required Claim Fields

Every claim used in polished outputs should have:

- `id`
- `source_context_id`
- `project_or_workstream`
- `user_ownership`
- `technologies`
- `impact`
- `confidence`
- `disclosure_level`
- `resume_use`

## Confidence Values

- `high`: direct source evidence or user-confirmed detail.
- `medium`: supported by sources but missing a date, metric, ownership boundary, or exact scope.
- `low`: plausible but needs explicit user confirmation before polished wording.

## Resume Use Values

- `include`: safe to use directly.
- `include-sanitized`: use only with internal names, URLs, IDs, customers, or exact metrics removed.
- `needs-confirmation`: ask the user before final output.
- `exclude`: do not use in resume, LinkedIn, cover letter, or interview material.

## Quality Gate Use

Use the schema to check:

- Claims without source context.
- Medium or low confidence claims in polished outputs.
- Internal details that require sanitization.
- Metrics marked `needs-user-input`.
- Missing ownership, date, scale, or impact.
