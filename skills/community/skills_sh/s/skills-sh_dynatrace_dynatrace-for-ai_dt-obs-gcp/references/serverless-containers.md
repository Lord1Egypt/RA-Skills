# GCP Serverless Containers (Cloud Run)

Monitor Cloud Run services, revisions, and job executions across GCP projects.

## Table of Contents

- [Serverless Container Entity Types](#serverless-container-entity-types)
- [Service Discovery](#service-discovery)
- [Revision Tracking](#revision-tracking)
- [Execution Monitoring](#execution-monitoring)
- [Service Distribution](#service-distribution)

## Serverless Container Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id, gcp.region`

| Entity type | Description |
|---|---|
| `GCP_RUN_GOOGLEAPIS_COM_SERVICE` | Cloud Run services |
| `GCP_RUN_GOOGLEAPIS_COM_REVISION` | Cloud Run revisions (immutable snapshots of service configuration) |
| `GCP_RUN_GOOGLEAPIS_COM_EXECUTION` | Cloud Run job executions |

## Service Discovery

Cloud Run services exist in two schema versions with different field layouts:
- **v1** (`serving.knative.dev/v1`): Knative-compatible format — runtime state is nested under `status`
- **v2** (`run.googleapis.com/v2`): Native Cloud Run v2 format — fields are top-level

List all Cloud Run services with their API version — use this to identify which schema version applies:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd apiVersion = gcpjson[configuration][resource][apiVersion]
| fields name, gcp.project.id, gcp.region, apiVersion
```

List Cloud Run **v1** services with their public URL and latest serving revision:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd apiVersion = gcpjson[configuration][resource][apiVersion]
| filter apiVersion == "serving.knative.dev/v1"
| fieldsAdd url = gcpjson[configuration][resource][status][url],
            latestReadyRevision = gcpjson[configuration][resource][status][latestReadyRevisionName]
| fields name, gcp.project.id, gcp.region, url, latestReadyRevision
```

List Cloud Run **v2** services with launch stage, URI, and latest revision — field paths follow the Cloud Run v2 API spec:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd apiVersion = gcpjson[configuration][resource][apiVersion]
| filter apiVersion != "serving.knative.dev/v1"
| fieldsAdd launchStage = gcpjson[configuration][resource][launchStage],
            uri = gcpjson[configuration][resource][uri],
            latestReadyRevision = gcpjson[configuration][resource][latestReadyRevision]
| fields name, gcp.project.id, gcp.region, launchStage, uri, latestReadyRevision
```

Find Cloud Run services in a specific project:

```dql-template
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, gcp.region
```

## Revision Tracking

List all Cloud Run revisions to track deployment history:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_REVISION"
| fields name, gcp.project.id, gcp.region
```

Find revisions in a specific project:

```dql-template
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_REVISION"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, gcp.region
```

## Execution Monitoring

List Cloud Run job executions:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_EXECUTION"
| fields name, gcp.project.id, gcp.region
```

## Service Distribution

Count Cloud Run services by project and region:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE"
| summarize count(), by: {gcp.project.id, gcp.region}
```

Count all Cloud Run resources by type:

```dql
smartscapeNodes "GCP_RUN_GOOGLEAPIS_COM_SERVICE", "GCP_RUN_GOOGLEAPIS_COM_REVISION", "GCP_RUN_GOOGLEAPIS_COM_EXECUTION"
| summarize count(), by: {type}
```
