---
name: openai-tts
description: "Generate MP3 speech with OpenAI TTS through RunAPI. Use for one-off speech generation or application integration. Prefer the RunAPI CLI for one-off requests and the target-language SDK for production integration."
documentation: https://runapi.ai/models/openai-tts.md
provider_page: https://runapi.ai/providers/openai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/openai-tts
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; agents should prefer environment auth or saved CLI config. Browser login is interactive fallback only.
---

# OpenAI TTS on RunAPI

## Choose route

- For a one-off artifact or result, use the registered `openai-tts` service in the `runapi` CLI. If the installed command catalog does not list it, stop and report the missing service instead of inventing a command.
- For an app, backend, worker, library, webhook pipeline, or production codebase, go directly to **Integrate with SDK**. Never shell out to the CLI as the production runtime.

## Discover contract

Authenticate, then inspect the installed command catalog and the selected operation's current contract:

```shell
runapi auth status > auth.json
jq -e '.authenticated == true' auth.json
runapi openai-tts --help
runapi openai-tts <operation> --help
curl --fail --location https://runapi.ai/docs/api/openai-tts/<operation>.md --output contract.md
```

If authentication is false, stop before submitting. Ask the user to provide a valid `RUNAPI_API_KEY`, or import a user-provided key from stdin with `runapi auth import-token --token -`; use interactive browser login only when the user explicitly requests it. Choose `<operation>` only from service help. Treat command help as authoritative for the installed operation, model, and top-level field roster. Treat its API Reference as authoritative for the complete request schema, nested fields, conditional rules, task behavior, and response variants. If the two surfaces disagree, stop and report the contract mismatch instead of guessing.

## Build request

Create `request.json` as valid JSON using only fields accepted by the discovered operation contract. For the chosen model and values, evaluate every applicable conditional rule as a set: satisfy every required field, omit every forbidden field, and stop on unresolved contradictions.

Traverse nested objects and arrays before execution. Close every relationship stated by the discovered contract, including uniqueness constraints and cross-references between nested values.

For a discovered local media input, including file-typed fields and top-level media URL fields, put an agent-readable local file path directly in `request.json`. The CLI consumes file fields as declared and uploads local paths in top-level media URL fields. Use `runapi files create` only when the user needs a reusable URL, provides Base64, or the discovered contract explicitly requires a separate upload.

Validate the file before sending it:

```shell
jq empty request.json
```

## Execute

Submit exactly once and save the complete synchronous response:

```shell
runapi openai-tts <operation> --input-file request.json > result.out
```

Do not add `--async` or call `runapi wait`. The operation completes in this response; preserve its exact JSON, text, subtitle, or other discovered response format.

## Verify

A success status is not the deliverable. Read and validate the complete response according to the discovered result contract. Preserve the complete non-media result in the exact requested format, including JSON, text, SRT, or VTT.

For every requested media deliverable listed anywhere in the response, download all of them rather than returning only the first URL. Before downloading, derive its expected MIME type or family from response metadata when present, then the selected output format, then an unambiguous result field such as `videos`, `images`, or `audios` in the API Reference. The Catalog-declared fallback families for this skill are `audio/*`. Stop only when no single expected type or family can be established from those sources.

For every downloaded file, require both a non-empty file and the expected MIME type or family:

```shell
curl --fail --location <deliverable-url> --output <downloaded-file>
for file in <downloaded-files>; do
  expected_mime=<expected-MIME-or-family-pattern-for-this-file>
  test -s "$file"
  [[ "$(file --brief --mime-type "$file")" == $expected_mime ]]
done
```

Do not report completion when any requested deliverable is missing, empty, or has an unexpected MIME type. Record `Skill Conformance` separately from `Task Outcome` so a service failure does not hide whether this recipe was followed.

## Recover or stop

- Correct a request shape at most once, and only when the discovered contract or returned validation error identifies the correction.
- Retry a transient transport failure at most once, and only when evidence confirms that no task was created, no billing occurred, and retrying is safe.
- On a terminal RunAPI or service failure, preserve the task/error evidence and stop. Keep the selected model and capability, and do not submit another paid request without user authorization.
- If the contract is missing a fact required to build or verify the request, stop and report the contract gap. Do not turn a product defect into a permanent skill workaround.

## Integrate with SDK

Use this route only for application or production-code integration. Open the current RunAPI SDK reference below, select the package for the target language and `OpenAI TTS`, and confirm its install command, client methods, request types, response types, and error classes before coding. Build the request from the same discovered product contract and apply the same deliverable verification and stop rules. Do not invoke `runapi` as a subprocess from production code.

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/openai-tts.md
- Provider overview: https://runapi.ai/providers/openai.md
- Full model catalog: https://runapi.ai/models.md
- SDK integration: https://github.com/runapi-ai/openai-tts-sdk

## Variants
- `tts-1`: https://runapi.ai/models/openai-tts/tts-1.md
- `tts-1-hd`: https://runapi.ai/models/openai-tts/tts-1-hd.md
