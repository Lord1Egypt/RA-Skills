# Output Schema

The script writes one run directory under the `--out` artifact root.

```text
<out>/<issue-identifier-or-manual-timestamp>/
  manifest.json
  summary.md
  urls/001/
    source-url.txt
    target-node.json
    context-tree.json
    design-properties.json
    code-connect.json
    css-hints.css
    screenshots/target.png
    screenshots/parent.png
    screenshots/candidates/001.png
```

Required JSON schema versions:

- `manifest.json`: `figma-context-artifact/v1`
- `target-node.json`: `figma-target-node/v1`
- `context-tree.json`: `figma-context-tree/v1`
- `design-properties.json`: `figma-design-properties/v1`
- `code-connect.json`: `figma-code-connect-context/v1`

Rules:

- `summary.md` is the first file a repair expert reads.
- Every URL, including failed URLs, must have one `summary.md` section.
- `manifest.json` stores portable `artifactRoot` and `runDir` values. When artifacts live inside `--repo`, these paths are relative to `--repo`; otherwise `runDir` is `.` and `artifactRoot` is relative to the run directory.
- CLI JSON output includes `runDirRelative` for repair notes and may include a local absolute `runDir` only for commands that run in the same environment.
- Generated artifacts and temporary issue JSON must not be committed.
- The script writes `.multica/figma-context/` and `.multica/tmp/` to `.git/info/exclude` when `--repo` is a Git repository.
- If that ignore check is not verified, `manifest.json` and `summary.md` include `artifact_ignore_unverified`.
- Artifacts must not contain access tokens, refresh tokens, client secrets, Authorization headers, or temporary signed Figma image URLs.
- `manifest.json` records `targetScreenshot`, `parentScreenshot`, and `candidateScreenshots`; each screenshot path must be local to the artifact run directory.
- `parentScreenshot` is `null` when parent context cannot be located or the parent export fails.
- `candidateScreenshots` is an array of `{ nodeId, name, source, path }`; it may be empty when there are no extra candidates or the screenshot budget is exhausted.
