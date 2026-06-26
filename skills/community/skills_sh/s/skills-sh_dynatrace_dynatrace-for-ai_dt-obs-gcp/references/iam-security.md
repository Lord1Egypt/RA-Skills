# GCP IAM & Security

Monitor IAM service accounts, roles, and Secret Manager secrets for security auditing across GCP projects.

## Table of Contents

- [IAM & Security Entity Types](#iam--security-entity-types)
- [Service Account Inventory](#service-account-inventory)
- [Service Account Security Audit](#service-account-security-audit)
- [IAM Role Analysis](#iam-role-analysis)
- [Secret Management](#secret-management)

## IAM & Security Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id`

| Entity type | Description |
|---|---|
| `GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT` | IAM service accounts |
| `GCP_IAM_GOOGLEAPIS_COM_ROLE` | IAM roles |
| `GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION` | Secret Manager secret versions |

## Service Account Inventory

List all service accounts with email and status:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd email = gcpjson[configuration][resource][email],
            disabled = gcpjson[configuration][resource][disabled]
| fields name, gcp.project.id, email, disabled
```

Count service accounts by project:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT"
| summarize count(), by: {gcp.project.id}
```

Find service accounts in a specific project:

```dql-template
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd email = gcpjson[configuration][resource][email],
            disabled = gcpjson[configuration][resource][disabled]
| fields name, email, disabled
```

## Service Account Security Audit

Find disabled service accounts — useful for identifying decommissioned accounts that may still have role bindings:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd email = gcpjson[configuration][resource][email],
            disabled = gcpjson[configuration][resource][disabled]
| filter disabled == true
| fields name, gcp.project.id, email
```

Find active (enabled) service accounts:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd email = gcpjson[configuration][resource][email],
            disabled = gcpjson[configuration][resource][disabled]
| filter isNull(disabled) or disabled != true
| fields name, gcp.project.id, email
```

## IAM Role Analysis

List all IAM roles:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_ROLE"
| fields name, gcp.project.id
```

Count IAM roles by project:

```dql
smartscapeNodes "GCP_IAM_GOOGLEAPIS_COM_ROLE"
| summarize count(), by: {gcp.project.id}
```

## Secret Management

List Secret Manager secret versions with their state:

```dql
smartscapeNodes "GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd state = gcpjson[configuration][resource][state]
| fields name, gcp.project.id, state
```

Find enabled (active) secret versions:

```dql
smartscapeNodes "GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd state = gcpjson[configuration][resource][state]
| filter state == "ENABLED"
| fields name, gcp.project.id
```

Find destroyed or disabled secret versions — useful for lifecycle auditing:

```dql
smartscapeNodes "GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd state = gcpjson[configuration][resource][state]
| filter state != "ENABLED"
| fields name, gcp.project.id, state
```

Summarize secret versions by state:

```dql
smartscapeNodes "GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd state = gcpjson[configuration][resource][state]
| summarize count(), by: {state}
```
