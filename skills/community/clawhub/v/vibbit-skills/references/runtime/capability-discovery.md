# Capabilities and execution conditions

`capabilities` lists client operations, not account permissions. `describe` returns fields, examples, and requirements. Actual availability depends on the account, assets, and response.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" capabilities --all
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" describe --command seedance
~~~

| Status | Action |
| --- | --- |
| documented | Use the API reference; listing does not certify account access, every mode, or output quality |
| legacy | Compatibility operation; avatar listing works directly without extra opt-in or a webpage workflow |
| known_issue | Read the limitation; use `--allow-known-issue` only for an explicit investigation |
| Not provided | Do not invent commands/parameters; identify available results and remaining steps |

`requires_opt_in` describes a command option, not repeated approval. Retain existing authorization. Use [API references](../catalog.md) for encoding, and [task lifecycle](task-lifecycle.md) for recovery; do not change encoding and resubmit after uncertainty.

Platform methods guide planning, APIs perform operations, and FFmpeg/HyperFrames/Remotion run locally. Upload credentials do not prove upload; project links do not prove video; finding an engine does not prove rendering. See [dependencies](external-render-dependencies.md) and [media inputs](media-inputs.md). Vibbit's accepted fields govern when a general model guide differs.
