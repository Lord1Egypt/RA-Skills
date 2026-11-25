# Task brief templates

Three templates: one for the reviewer, one for the auditee, one for the return
step. Fill in the blanks; the structure stays as is.

---

## Template A — Reviewer: audit brief

```
Role: reviewer
Goal: complete the audit of <audit topic> without obtaining the auditee's raw data

Scope
- Auditee: <organization>
- Data domain: <ledger / settlement / customer / other>
- Period: <start> to <end>

Deliverables
1. Sealed audit package (.mgc_file)
2. Package sha256 and import instructions
3. Interpretation guide for each rule name

Requirements
- Checking logic runs only on the auditee's machine
- Output keeps conclusions and counts only, never raw rows
- For additional samples, ship a new sealed version — never ask for detail records

Acceptance
- The auditee completes a full run locally
- The returned audit_result.json includes summary.conclusion
```

---

## Template B — Auditee: execution brief

```
Role: auditee
Goal: complete one audit locally and return only the conclusion

Preconditions
- MGC Blackbox >= 1.6.0 is installed and running locally
- The database under review is readable; credentials, if any, are stored in the local MGC

Steps
1. Confirm the package source and sha256
2. Import the sealed package
3. Run the entry script against the local database
4. Check that the output contains conclusions and counts only
5. Return the result file, not the underlying data

Not accepted
- Sending raw data, connection strings, or detail exports together with the result
- Editing the scripts or the rules
- Forwarding the package to a third-party node
```

---

## Template C — Auditee: result return

```
Audit result

Task ID: <task_id>
Package sha256: <sha256>
Run time: <yyyy-mm-dd hh:mm:ss>
Environment: <OS> / Python <version> / MGC <version>

Conclusion: <pass | review_required>
- high: <n>
- medium: <n>
- low: <n>
- total: <n>

Attachment: audit_result.json
Note: only the conclusion is returned; raw data never left this machine.
```
