# Output format

You author one file, `scorecard.json`. `scripts/score.py` validates it and renders everything else from it, so the report, the website entry, and the score table can never disagree.

```
scorecard.json  ──score.py──▶  entry.json   the website record for this agent (schema/entry.schema.json)
  (you write)                   report.md    the human-readable report
                                table        printed to stdout
score.py --catalog        ──▶  data/criteria.json (criteria names, questions, OWASP labels, bands, enums)
```

Start from `python3 scripts/score.py --example`. Never write computed fields (`score`, `band`, `points`, `url`, …); the script rejects them.

## Top-level fields

| Field | Type | How to fill it |
|---|---|---|
| `id` | slug | Lowercase `[a-z0-9-]`, stable across rescoring: the website URL. Use the project's common name (`smolagents`, `mcp-server-filesystem`). |
| `name` | string | Display name. |
| `repo_url` | `https://…` | Repository root, no trailing path. |
| `subpath` | string \| null | Directory scored inside a monorepo (`src/filesystem`), else `null`. |
| `description` | string | One line: what the project is, not how safe it is. |
| `category` | enum | See below. |
| `pinned_commit` | 40-hex | Full `git rev-parse HEAD`. |
| `version` | string \| null | Release tag at that commit, if any. |
| `scored_date` | `YYYY-MM-DD` | Today. |
| `scored_configuration` | string | One sentence: the default configuration you scored. |
| `capability_profile` | object | Shown in the report as "Agent surface". Each of `code_execution`, `filesystem_write`, `network_egress`, `external_credentials`, `persistent_memory`, `untrusted_input`, `third_party_extensions`, `sub_agents`, `external_communication` is `yes`, `no`, or `opt_in`, describing the scored default. |
| `headline` | string | 2–4 sentences for someone deploying this as shipped. Lead with what matters most; name the dominant risk. Plain language — the website shows it at the top of the agent page. |
| `safe_setup` | object | Shown in the report as "Safest setup", right after the headline. How to run the agent most safely, written from this review's findings (SKILL.md step 6, and below). Never changes a score. Optional in the schema so older entries still validate; write it for every new scorecard. |
| `criteria` | array | Exactly C1–C10 (below). |
| `critical_findings` | array | See the rule below. |
| `rule_of_two` | object | `untrusted_input`, `sensitive_data`, `state_change_or_egress` (short strings with `path:line`), `same_session` (bool). |
| `fixes` | array ≤ 5 | Shown in the report as "Highest-impact improvements". Ordered by score gained per unit of effort. Each: `summary`, `criterion`, `parameter`, `from_level`, `to_level`, optional `playbook` (OWASP playbook step). The script computes `estimated_gain`. |
| `reaudit_log` | array | Every level changed during the adversarial re-audit: `criterion`, `parameter`, `from_level`, `to_level`, `reason`. Empty if none. |
| `limitations` | array of strings | Always include the static-review statement; add unexamined areas, INFERRED-heavy criteria, reviewer-injection attempts found. |

### Category
Category is the **domain the agent acts on**, judged from its primary documented use. Agents in one category hold similar access and fail in similar ways, which is what makes ranking them against each other fair. Architecture is not category: MCP servers are spread across categories by domain.

| id | Label | What belongs |
|---|---|---|
| `coding` | Coding | Coding CLIs, IDE agents, autonomous software engineers, code-review bots, git/GitHub tool servers |
| `cybersecurity` | Cybersecurity | Pentest agents, SOC and alert triage, threat investigation, cloud configuration auditing |
| `infrastructure_ops` | Infrastructure & Ops | SRE, incident response, Kubernetes, cloud ops, infrastructure-as-code, observability |
| `ai_assistants` | AI Assistants | General and personal assistants, browser and computer-use, research, email/calendar/docs |
| `data_analytics` | Data & Analytics | SQL and BI agents, data-science agents, database and warehouse tool servers |
| `agent_frameworks` | Agent Frameworks | Libraries and platforms for building agents, including low-code builders |

Boundary rules:
- Security beats infrastructure when the agent's job is finding or stopping threats (a Kubernetes vulnerability scanner is `cybersecurity`).
- Domain beats generality for tool servers (GitHub server → `coding`; Postgres server → `data_analytics`).
- Libraries and platforms for building agents are `agent_frameworks`, even if they ship example agents.
- Truly general-purpose agents and general tool servers (filesystem, browser) are `ai_assistants`.

## Each criterion

```json
{"id": "C4",
 "summary": "One plain-language paragraph: what was found in the source and why it scored as it did.",
 "parameters": {"S": {...}, "C": {...}, "D": {...}, "B": {...}},
 "caps": [{"id": "G1", "reason": "Why the cap applies, one sentence."}],
 "alt": {"label": "opt-in E2B sandbox", "parameters": {...}, "caps": []},
 "notes": "Optional: caveats, partial controls."}
```

- `summary` is what the website shows under each criterion. 3–5 sentences, no jargon a deployer wouldn't know, no level codes. Say what exists, what's missing, and the consequence.
- `alt` only when a stronger opt-in mechanism exists (SKILL.md, "One criterion, several mechanisms"). The script adds G1 to it.
- Structural absence replaces `parameters` with `"structural_absence": true` and `"absence_evidence": [search items]`.

### Each parameter

```json
{"level": 2, "status": "verified",
 "finding": "One sentence: what the code shows at this level.",
 "gap": "One sentence: what the next level requires that the code doesn't do.",
 "evidence": [ {"file": "src/agent/tools.py", "lines": "40-58", "contains": "def validate_path"},
               {"search": "rg -n -S 'approv|confirm'", "scope": "src/", "hits": 3,
                "note": "hits are CLI prompts for config, not tool gating"} ]}
```

- `level`: 0–4, or `"SA"` for a parameter whose surface is absent (needs a search item).
- `status`: `verified` (read in source) or `inferred` (reasoned; cannot exceed L2).
- `gap`: required below L4 (except SA). The specific element of the next level up that the code doesn't meet, one sentence, e.g. "No session wall-clock limit; the token budget is off by default." The website shows it as "what would raise this".

### Evidence items
Two kinds. Every parameter needs at least one.

**Code citation** — `file` is repo-relative from the repository root (include the subpath: `src/filesystem/index.ts`, not `index.ts`). `lines` is `"N"` or `"N-M"`. `contains` is a short literal copied from inside those lines; `score.py --repo` checks it. The website turns citations into permalinks at the pinned commit.

`contains` is **required** on evidence for critical gaps (`critical_findings`), for any parameter at L3 or L4, and for every parameter of a criterion with a cap other than G1 (for G1, on D). Use it everywhere you can: it is the only thing that proves a citation points at the code you meant. Take line numbers from `rg -n` or `grep -n` run on the file itself — numbering from `sed -n X,Yp file | grep -n` is relative to the excerpt and will be wrong.

**Search** — `search` is the exact command, `scope` the space-separated paths it ran over, `hits` the **exact number of matching lines** that command prints. Not "relevant" hits: all of them. If hits aren't controls (comments, unrelated words), say so in `note`. `score.py --repo` re-runs plain `rg` searches and errors on a mismatch, so write the search as a command that reproduces: `rg` flags and pattern in `search`, paths only in `scope`.

## Safest setup (`safe_setup`)

```json
"safe_setup": {
  "intro": "Cynative ships with a read-only permission gate on every cloud request, per-call approval and an audit log of every tool call. The safest setup keeps those on and adds a few layers around them.",
  "steps": [
    {"setup": "A read-only identity", "how": "Run it from a read-only cloud identity, such as an AWS role with SecurityAudit",
     "gives_you": "The cloud provider itself blocks writes, so safety no longer depends on the tool's own gate",
     "criterion": "C1", "source": "operator"},
    {"setup": "A token ceiling", "how": "`max_total_tokens: <n>` in the config file",
     "gives_you": "A hard cap on spend for the whole run, sub-agents included", "criterion": "C10", "source": "opt_in",
     "evidence": [{"file": "internal/config/config.go", "lines": "88", "contains": "max_total_tokens"}]}
  ],
  "approving": ["Read each prompt and approve calls one at a time; a script approval covers every request the script makes."],
  "handling": ["The audit log keeps the raw arguments of approved calls; store it like other sensitive logs."]
}
```

| Field | How to fill it |
|---|---|
| `intro` | 1–3 sentences on what already ships protected, in plain, positive language. If the defaults are weak and there is nothing to turn on, say so plainly here. |
| `steps` | 2–8 items, ordered by protection: the step that holds even if the tool's own controls fail comes first (usually least privilege the provider enforces), then the tool's own gates, then containment and logging. |
| `steps[].setup` | Short name: "A read-only identity", "Per-call approval". |
| `steps[].how` | The exact flag, config key, env var or deployment action. Put names in backticks, use `<n>` style placeholders for values. |
| `steps[].gives_you` | What it protects, in positive terms. |
| `steps[].criterion` | The criterion (C1–C10) whose finding the step comes from. |
| `steps[].source` | `default` (keep a protection that ships on), `opt_in` (turn on a mechanism the review found) or `operator` (something outside the tool, such as a read-only cloud role or a container). |
| `steps[].evidence` | Code citations (`file`, `lines`, `contains`) of where each flag, key or env var named in `how` is defined at the pinned commit. Required for `default` and `opt_in`; optional for `operator`. `score.py --repo` checks them like any other citation and warns when a backticked name in `how` is not in the cited lines. |
| `approving` | Optional: short notes on reviewing approval prompts safely ("read each prompt and approve calls one at a time", never "approve everything"). |
| `handling` | Optional: short notes on handling logs or data the tool writes. |

Rules: every step traces to a finding already in the scorecard (a level, its gap, an `alt` mechanism, a limitation); no defect details (SKILL.md step 8), so evidence cites the setting, never a defective line; no estimated score for the safe setup. The report renders `intro`, a table (Setup | How | What it gives you), then "Approving with confidence" and "Handling data" when present; the entry carries the whole object, with a `url` permalink on each citation.

## Critical gaps rule (`critical_findings`)
The report shows these under "Critical gaps". List every one of these that applies, regardless of the total — the script warns if one is missing; when none applies the section says so:
- any criterion-specific cap that was applied (C1-SELFESC, C2-SELFAPPROVE, C4-HOSTROOT, C5-WORSTCASE, C6-REPOCONFIG, C7-RCELOAD, …), or G2;
- B at L0 in C1, C4, C5, or C7 (for criteria with an alt, check the default mechanism — that's what ships).

Each: `summary` (one sentence), `criterion`, `owasp` (labels from `owasp-mapping.md`), `evidence` (with `contains`).

## Bands and website colours

| Total | Band id | Label | Colour |
|---|---|---|---|
| 8.5–10.0 | `hardened` | Hardened | green |
| 7.0–8.4 | `strong` | Strong | green |
| 5.0–6.9 | `moderate` | Moderate | amber |
| 0.0–4.9 | `weak` | Minimal | red |

The entry also carries `applicable` (score over criteria that weren't structurally absent). Read the band together with it and the capability profile: a 9.0 earned mostly through absent surfaces and a 9.0 earned through strong controls on a large surface mean different things.
