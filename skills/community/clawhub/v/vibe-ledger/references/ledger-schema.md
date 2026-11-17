# Ledger fields

`ledger.json` is one JSON object. `evidence` and `promises` are required; `compromises`, `map`, `access` and `paths` may be left out. `vl.py check` lists every format problem at once.

## evidence — `{id: item}`

| kind | fields |
|---|---|
| `transcript` | `session`, `msg_id` (the `[ID]` from a reading pack), `quote` (≥ 4 characters, copied exactly) |
| `code` | `path` (relative to the project), `line` (integer), `snippet` (1–3 lines copied exactly) |
| `probe` | `finding_id` (an `id` from `probes.json`) |

`check` adds `ok` and, when it fails, `reason`. Timestamps always come from the logs.

## promises — list

| field | values |
|---|---|
| `id` | unique, e.g. `P1` |
| `type` | `user_requirement` (the user asked), `ai_claim` (the AI said it did it), `deferred` (put off for later) |
| `question` | `where_data`, `what_costs`, `who_can_see`, `what_breaks`, `open_debts` |
| `plain` | the promise in a short sentence, in the run's language |
| `source` | transcript evidence ids — where it was said |
| `status` | `kept`, `broken`, `partial`, `pending` (only for `deferred`: still not done), `unknown` |
| `verdict_plain` / `verdict_dev` | see SKILL.md rule 4 |
| `evidence` | code/probe evidence ids that support the status |
| `fix_prompt` | optional; an instruction the user can paste to their AI (file, change, how to confirm). Never include a secret. |

## compromises — list

`id`, `error` (transcript id of the error), `change` (transcript ids of the change), `bypassed` (a few words: "RLS", "CORS check"), `still_present` (`true`/`false`), `now` (code/probe ids showing the current state), `breaks` (promise id or `null`).

## map

`lane_labels` (optional): `{browser|server|storage: text}` renames a lane for a project that is not a web app — a CLI or a pipeline names them, e.g. "你运行的脚本" / "本机处理".
`nodes`: `id`, `lane` (`browser`, `server`, `storage`), `kind` (`page`, `route`, `function`, `database`, `storage`, `third_party`, `client`), `label`, `holds` (data names), `paid` (true when it charges per use), `evidence`.
`edges`: `from`, `to`, `carries` (what data), `risk` (short text or `null`), `evidence`.

## access

`resources`: `name` (table, collection, bucket — or `*` for all data), `required_by` (promise id or `null`), `cells` keyed by `anonymous`, `signed_in`, `owner`, each `{read, write, evidence}` with values `allow`, `deny`, `unknown`.

## paths

Each: `action` (what the user does, e.g. "press Save"), `steps`: `[{label, evidence (one id), warning (text or null)}]`.
