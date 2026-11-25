# Role and task-card template library

> This file is the **task-card template library** for chain-mode collaboration. The orchestrator agent copies the matching template per scenario, replaces `<>` placeholders, and distributes to each agent.
> Roles are not fixed — scale by **data domain**: one execution agent per domain, exactly one orchestrator agent.
> Template list: Template 1 Orchestrator task card / Template 2 Dispatch instructions / Template 3 Executor task card / Template 4 Result return / Template 5 Orchestrator return receipt.

## Role overview

| Role | Count | Holds data / credentials | Primary responsibility | Output |
|------|------|:---:|------------------------|--------|
| Orchestrator agent | 1 | ❌ none | Split task, generate spec, dispatch, aggregate | Task card, targets spec, aggregate report |
| Internal execution agent | 1 per internal data domain | ✅ local only | Execute scripts inside local data domain | Result summary |
| External execution agent | 1 per external data domain | ✅ local only | Execute scripts inside external data domain | Result summary |

> Internal / external is a **data boundary**, not a device type. A single-domain scenario can run with just "1 orchestrator + 1 internal executor" — drop the external row.

---

## Template 1: orchestrator agent task card

```text
[Role] You are the orchestrator for this multi-agent encrypted collaboration.

[Task goal]
Use MGC chain mode to split task <task name> into <N> independent sealed sub-packages, and dispatch them to the following data domains:
- <data domain 1> (internal): <analysis / processing handled by this domain>
- <data domain 2> (external): <analysis / processing handled by this domain>

[Hard constraints]
1. You do not touch any business data or credentials. They live only on each executor's local machine and are prepared by the executor itself.
2. You handle script files (.py) only. Do not ship data files such as CSV / JSON / config.
3. The workflow directory must be flat (no sub-directories). Cross-script imports must be written as `from helper import ...`.
4. Files inside a sub-package are defined by the grant list. Ungranted files will not appear on the other side.
5. Verify each sub-package against sha256 before delivery — use the value from distribution_index.json.

[Deliverables]
1. Flat workflow script directory
2. Targets spec JSON (each entry contains node_pub + files; files contain .py only)
3. N sealed sub-packages + distribution_index.json
4. Dispatch notes (transport method, recipients, verification method)
```

---

## Template 2: orchestrator agent dispatch instructions

```text
[Task] Generate chain-mode sub-packages for the workflow already stored in MGC and dispatch them.

[Stored in MGC]
info_owner = <owner>
diff_2      = <folder>

[Data domains and granted files]
- <data domain 1>: files = ["<script_a.py>", "<shared_helper.py>"]
- <data domain 2>: files = ["<script_b.py>", "<shared_helper.py>"]

[Procedure]
1. Collect node_pub from each executor (they run mgc_get on their own machine; use the multi-line PEM as-is).
2. Build targets, write to a local JSON file, pass via ext04="@<absolute path>".
3. Call mgc_seal_package to produce sub-packages.
4. Read distribution_index.json. Match node_pub_fingerprint one by one against the node fingerprint ledger (each executor's email + node_pub + fingerprint) to verify recipients.
5. Default dispatch is email: package each task_package_NN/ directory independently and attach with the sha256 verification value.
   - Subject always uses `chain:<task_id>` so executors can poll and filter by keyword.
   - Write each attachment's sha256 in the email body (not only in the file name) so the receiver can verify before import.
6. After dispatching, wait for each executor's result return, then aggregate.

[Forbidden]
- Do not add data files to files.
- Do not merge multiple sub-packages into one and send.
- Do not paste .mgc_file base64 into the email body (must be an attachment).
```

---

## Template 3: executor agent task card

```text
[Role] You are the executor for the <data domain name> portion of this task.

[Your environment]
- MGC is running locally (≥1.6.0).
- This domain's data / credentials are already stored in your local MGC (info_owner=<local owner>). They never travel outward.

[Task]
1. Receive the <task_package_NN>.mgc_file from the orchestrator (email attachment, Subject contains `chain:<task_id>`).
2. Verify: the attachment's actual sha256 matches the value in the email body, then import.
3. Import: mgc_save_file(path="<local path>", info_owner="<owner inside package>", diff_2="<diff_2 inside package>").
4. Verify grant list: use mgc_find to confirm the actual files received are exactly what the task card lists. If they differ, stop and report an exception.
5. Smoke test: note that "import success ≠ unsealable" — unsealing happens at run time. After verifying the grant list, smoke-test the entry script with small parameters. If UNSEAL_FAILED (Double-layer unseal failed) surfaces, the sub-package's node_pub does not match this machine; stop and report an exception.
6. Full run: mgc_run(info_type="script", info_owner=..., diff_2=..., diff_3="<script.py>").
   - Inside the script, read data / credentials via local MGC REST API. Do not write them to disk, do not print them.
   - If passing --output through ext02, create the parent directory first (sealed scripts do not auto-mkdir).
7. Keep only a summary of results: fields, metrics, conclusions — no raw data rows.

[Hard constraints]
- Do not read unauthorized MGC records.
- Do not write data / credentials into results or logs.
- Do not modify sealed script contents.
- On execution failure, return an error summary (error type + key stack line), not environment variables.

[Deliverable]
A single result summary (JSON or short text). Return it per Template 4.
```

---

## Template 4: result return

```text
[Task] Return the execution result for <data domain name>.

[Return content]
- Task identifier: <task name>
- Execution status: success / failed
- Result summary: <structured summary, no raw data>
- Artifact verification: sha256 = <value>
- Exception notes (failed only): <error type + key information>

[Return method]
- Option A (recommended, encrypted): wrap the result in <report.py> (results as string constants), seal with the orchestrator's node_pub in p2p mode, then return.
- Option B (simple, plaintext): write the summary directly in the email body — use only when the result contains no sensitive information.

[Forbidden]
- Do not return raw data rows, credentials, or full logs.
- Do not mix results and scripts into the same sub-package for return.
```

---

## Template 5: orchestrator agent return receipt

```text
[Role] You are the orchestrator for this multi-agent encrypted collaboration, responsible for receiving each executor's returned results.

[Receiving flow]
1. Match incoming return mail against the node fingerprint ledger: sender email ↔ ledger fingerprint. Confirm the source is trustworthy.
2. Verify: the attachment's actual sha256 matches the value in the email body.
3. Import: mgc_save_file(path="<return package path>", info_owner="<owner inside return package>", diff_2="<diff_2 inside package>").
   Return packages are p2p-sealed with the orchestrator's node_pub, so only the orchestrator's machine can unseal them.
4. Run: mgc_run(info_type="script", info_owner="<owner inside return package>", diff_3="<report.py>").
   The report.py script writes the summary out (via --output or local file).
5. Aggregate: once all data-domain results are in, produce the final deliverable.

[Exception handling]
- sha256 mismatch / source fingerprint mismatch → reject, ask executor to resend.
- Return package import failure → check that the .mgc_file suffix was preserved.
- UNSEAL_FAILED at run time → return package was not sealed with the orchestrator's node_pub; send back for resealing.

[Forbidden]
- Do not ask executors to attach raw data or credentials in the return path.
- Do not import multiple executors' return packages together.
```

---

## Usage notes

1. **Copy only the templates you need** — do not forward the entire file to an agent.
2. The number of executor agents follows the number of data domains; if there is only one domain, drop "external" references from Template 3.
3. The "forbidden" clauses in each template are the guardrails against privilege escalation and secondary leakage — do not remove them.
4. The grant list in each task card must match the `files` field of targets item-by-item.
