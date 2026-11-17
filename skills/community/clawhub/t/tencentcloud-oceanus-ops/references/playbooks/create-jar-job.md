# Playbook: Create JAR Job

Complete workflow for creating, configuring, publishing, and running a JAR job.

## Prerequisites

- Workspace ID (`space-xxx`) and cluster ID (`cluster-xxx`) available
- JAR file built and ready for upload
- Know the main class name (EntrypointClass)

## Workflow Overview

```
upload main jar → create_job → modify_draft → create_job_config → run_jobs
```

Each step is an independent atomic command.

---

### Step 1: Upload Main JAR

```bash
# 1a) Get presigned URL
python scripts/oceanus_ops.py create_presigned_url \
  --file_name my-flink-job.jar --region ap-guangzhou

# 1b) Upload to COS
curl -X PUT -T /path/to/my-flink-job.jar -H "Content-Type: application/java-archive" "<Location>"

# 1c) Register the resource
python scripts/oceanus_ops.py create_resource \
  --name my-flink-job.jar \
  --resource_type 1 \
  --bucket <Bucket> \
  --cos_path <Key> \
  --cos_region ap-guangzhou \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
# → Note ResourceId (e.g. resource-xxx) and Version (e.g. 1)
```

Or use the one-step upload shortcut:

```bash
python scripts/oceanus_ops.py upload_resource \
  --resource_id resource-xxx \
  --file /path/to/my-flink-job.jar \
  --region ap-guangzhou \
  --confirm
```

---

### Step 2: Create JAR Job

```bash
python scripts/oceanus_ops.py create_job \
  --name "my-jar-job" \
  --job_type 2 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --cluster_id cluster-xxx \
  --confirm
```

Note the returned `JobId` (e.g. `cql-xxx`).

---

### Step 3: Modify Draft (Set JAR Config + Resources)

```bash
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 2 \
  --entrypoint_class com.example.job.FlinkTestJob \
  --program_args "-foo 1 -bar 2" \
  --resource_refs '[{"ResourceId":"resource-xxx","Type":1,"Version":1}]' \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

Add auxiliary jars or config files as additional entries in `--resource_refs`:

```bash
--resource_refs '[
  {"ResourceId":"resource-main","Type":1,"Version":1},
  {"ResourceId":"resource-lib","Type":0,"Version":1},
  {"ResourceId":"resource-cfg","Type":2,"Version":1}
]'
```

---

### Step 4: Publish New Version

```bash
python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx \
  --job_type 2 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

Shows draft summary (EntrypointClass, ProgramArgs, ResourceRefs) for confirmation, then publishes. SQL grammar check is **not** performed for JAR jobs.

---

### Step 5: Run the Job

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

---

## ResourceRefs Format (JAR Jobs)

JAR jobs **must have exactly one** `Type=1` (MAIN) entry:

| `ResourceRef.Type` | Meaning | Requirement |
|---|---|---|
| `1` (MAIN) | Main program jar | **Exactly one**, required |
| `0` (DEPENDENCY_JAR) | Auxiliary jars (UDF, connector) | 0 or more |
| `2` (DEPENDENCY) | Non-jar files (.properties, .json) | 0 or more |

```json
[
  { "ResourceId": "resource-main", "Type": 1, "Version": 1 },
  { "ResourceId": "resource-lib",  "Type": 0, "Version": 1 },
  { "ResourceId": "resource-cfg",  "Type": 2, "Version": 1 }
]
```

**Rules:**
- 0 or >1 MAIN entries → CLI rejects with validation error
- If user uploads multiple jars without specifying which is main, ask them to clarify
- `ResourceRefs` is a **top-level field** (not nested inside ProgramArgs)

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `InvalidParameterValue: main ResourceRefs count 0 invalid` | No Type=1 entry | Add exactly one MAIN resource ref |
| `InvalidParameterValue.JobName` | Name format invalid | Use ≤50 chars |
| `DraftNotFound` | No draft prepared | Run `modify_draft` first |
| `ResourceNotFound.ClusterId` | Cluster not found | Check cluster ID |
