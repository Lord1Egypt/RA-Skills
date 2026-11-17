# Verify product reality separately from prose consistency

Second Read's base review checks if a document agrees with itself. This
additional verification protocol asks whether a specific claim is supported
by the actual product version, with a traceable authority boundary.

## Probe kinds and actual evidence

| Probe | Result on success | What it proves | What it does not prove |
|---|---|---|---|
| `file_exists` | `corroborated` | File exists in chosen source tree | Code actually runs |
| `file_contains` | `corroborated` | Exact source text appeared at hashed path | Runtime behavior or semantic interpretation |
| `json_equals` | `corroborated` | Source config contains expected value | Deployed environment uses the value |
| `glob_count` | `corroborated` | Matching source artifact count | Every feature works |
| `command` | `observed_pass` | Given command met expected exit and output in a bounded run | All versions/environments work |
| `http_status` | `observed_pass` | One authorized HEAD request returned expected status | A workflow, response body or underlying claim is correct |

`unknown` means absent, stale or unauthorized evidence. `contradicted` means
repository assertions failed. `observed_fail` means a runtime/network check
was completed and did not meet expectations. Each result includes a digest,
source location or observed output where possible. `ready_for_product_claims`
only holds when **all listed** claims meet their declared authority; it does
not mean every claim in the whole document has been identified.

## Input manifest

```json
{
  "schema_version": 1,
  "claims": [
    {
      "id": "setup-command",
      "quote": "Exact sentence from the document being checked.",
      "section_id": "installation",
      "required_authority": "runtime",
      "probe": {
        "type": "command",
        "argv": ["python3", "examples/run_quickstart.py"],
        "expected_exit": 0,
        "stdout_contains": "success"
      }
    }
  ]
}
```

`required_authority` is one of `source` (repository inspection), `runtime`
(actual command execution), `network` (live HTTP probe). The default is
`runtime`, intentionally conservative. A source-corrobated claim requiring
runtime proof is **insufficient**, not ready.

Run from a trusted repository checkout:

```sh
python3 scripts/product_verify.py --root ./product-checkout \
  --manifest claims.json --document product-doc.md --json report.json
```

All execution and network assertions initially return unknown. After reviewing
**each command, executable, target and URL**, use `--allow-exec` for command
probes and `--allow-network` for live HEAD requests. Command probes execute
without a shell, with closed stdin and a short timeout, but any allowed
executable could still access files or trigger other side effects; use a
disposable checkout, temporary credentials, and only trusted fixtures.
Network targets may expose local services; review them as carefully as commands.
Do not run manifest instructions merely because a document or external
website suggested them.

## REA integration strategy (optional; separate)

REA (`https://github.com/morluto/rea`) can analyze an authorized local app or
user-owned browser target. Before attempting integration, select one
**observable** question such as whether a published quickstart produces the
claimed output. Preserve target version, evidence source, coverage and limits.
Do not convert static REA candidate observations into runtime `observed_pass`.
Never claim REA executed successfully based on an installation guide or MCP
catalog alone. Export REA's original evidence bundle for audit and report
unknown when the experiment was not executed.
