# TEST.md template

> Copy this file into your target skill directory, rename it to `TEST.md`, and fill in real cases.

## Meta

```yaml
skill_name: your-skill-name
version: "1.0"
maintainer: your-name
```

## Test Cases

### Case 1: [normal-flow description]

```yaml
id: case_001
name: Basic functionality
type: normal  # normal | error | edge
trigger: "user trigger phrase, e.g., upload this image /tmp/test.jpg"
script_cmd: "bash scripts/upload.sh /tmp/test.jpg"  # optional; empty = AI-layer only
expected_output: "https://"  # keyword or regex
expected_output_mode: contains  # contains | regex | exact
expected_agent_response: "Returned a CDN URL, confirmed upload"
```

### Case 2: [error-handling description]

```yaml
id: case_002
name: File not found error
type: error
trigger: "Upload this image /tmp/does_not_exist.jpg"
script_cmd: "bash scripts/upload.sh /tmp/does_not_exist.jpg"
expected_output: "error|not found|missing"
expected_output_mode: regex
expected_agent_response: "Tells the user the file is missing and suggests a fix"
```

### Case 3: [edge-case description]

```yaml
id: case_003
name: Oversized file handling
type: edge
trigger: "Upload this huge file /tmp/large.jpg"
script_cmd: ""  # No script; AI-layer only
expected_output: ""
expected_output_mode: contains
expected_agent_response: "Includes appropriate guidance or size warning"
```

## Notes

- `type`: `normal` (happy path), `error` (failure handling), `edge` (boundary)
- `script_cmd`: empty = skip script layer, AI layer only
- `expected_output_mode`:
  - `contains`: actual output contains the substring
  - `regex`: regex match against actual output
  - `exact`: actual output equals expected exactly
- `expected_agent_response`: natural-language description; used by the LLM-as-judge for scoring
- `skip_agent: true`: optional; if set, this case bypasses the AI layer entirely

## Path placeholders (usable in script_cmd)

| Placeholder | Resolves to |
|---|---|
| `{SKILL_DIR}` | Target skill directory (absolute path) |
| `{TESTRES_DIR}` | `~/.skill-regression-space/testres/<skill-name>` (fixtures, helpers) |
| `{WORK_DIR}` | `~/.skill-regression-space/output/<skill-name>/<timestamp>` (this run) |
