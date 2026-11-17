# Run and resume

Use Python 3.10 or newer. The standard-library CLI and all required Python modules are bundled. There is no model API dependency for analysis: the host agent reads and interprets the packets.

In the commands below, replace `<skill>` with the folder containing `SKILL.md`. Resolve it from the loaded skill location. The user should not have to find it manually.

## Try an offline example

```sh
python3 <skill>/scripts/v2n.py demo --output NEW_DIRECTORY
```

This creates a new run from invented podcast-production records, prepares packets and renders the supplied demonstration findings. It uses no real accounts or network. Never overwrite the user's existing run to show a demo.

The second invented domain, bicycle-repair, is available beside podcast-production in `assets/demo/`. Both examples contain complete records, config and findings JSON and can be inspected without running anything.

## Real research

Prepare a configuration for the user's decision. Explain which communities or queries will be read, the window and the request/cost cap. Do not search every source merely because an adapter exists.

Read [source configuration](sources.md) for the complete root config, account requirements and concrete job fields for each selected platform. It includes discovery-to-deep-collection steps, per-Actor/per-video caps, and Discord export's separate process budget.

```sh
python3 <skill>/scripts/v2n.py collect --config CONFIG_JSON --run-dir RUN_DIRECTORY
```

Without `--live`, live network requests are disabled. Existing authorized Discord exports can be imported offline. Network collection uses the same command with `--live` only when covered by the user's authorization. Never substitute another provider, payment account, browser session or community silently.

Credentials are checked only when their source is needed: `YOUTUBE_API_KEY`, `X_BEARER_TOKEN`, `APIFY_API_TOKEN`, or `DISCORD_TOKEN` for the appropriate configured adapter. Discord live export additionally requires already-confirmed intended account and specific channel access. Tell the user how to supply a required credential through their environment; never ask them to paste it into the conversation or put it in a public config. A missing source remains a named gap.

Keep the agreed config and use the same run directory to resume. Inspect status after errors or interruption:

```sh
python3 <skill>/scripts/v2n.py status --run-dir RUN_DIRECTORY
python3 <skill>/scripts/v2n.py verify --run-dir RUN_DIRECTORY
```

Status distinguishes collection outcomes. Verification checks stored evidence integrity; neither means the content has been semantically read. Indeterminate paid-actor starts require checking their recorded state before deciding whether any new start is justified.

## Read, analyze and report

For separate completed sources with the same domain and time window, combine them
locally before analysis:

```sh
python3 <skill>/scripts/v2n.py merge --run-dirs FIRST_RUN SECOND_RUN --output NEW_COMBINED_DIRECTORY
```

This copies original raw directories and fixes relative evidence references without
changing the input runs. It retains their retention deadlines. Different domains
or windows are rejected instead of silently pooled. Use the combined directory as
`RUN_DIRECTORY` below. This command needs no account or network.

```sh
python3 <skill>/scripts/v2n.py prepare --run-dir RUN_DIRECTORY --output NEW_PACKETS_JSON
python3 <skill>/scripts/v2n.py report --run-dir RUN_DIRECTORY --findings FINDINGS_JSON --output NEW_REPORT_MD
```

Between those commands, the host reads the packets and writes `FINDINGS_JSON` using [the format](findings-format.md). `report` does not call a model. Resolve missing-context failures or narrow the claim; do not loosen validation just to produce a report.

Write claims and question answers in the user's language. The current deterministic renderer uses English structural headings; the `language` setting guides the host's analysis rather than invoking an automatic translation service.

Packet limits (`analysis.max_packet_records`, `analysis.max_packet_chars`) control subject batches. Full long records and necessary ancestors can exceed a limit and are marked oversized. Adjacent packets and discussion context may still need reading. `analysis.evidence_ids` selects explicit candidate records; keep that selection reason and review other strata for blind spots.

Raw responses and imported originals remain distinct from derived records, packets and reports. Do not edit source text or raw files to make a quote pass. Use the configured retention boundary and the user's deletion policy; a research workflow does not authorize perpetual retention or publication.

Verification checks raw hashes/locations and matches normalized text to the cited
raw object. Broken observation tails remain untouched and are reported as storage
gaps. An explicit change to only the root `limits` can resume a run after budget
approval; changing targets or the research scope requires a new run.

## Completion check

Deliver a decision-focused summary and artifact paths. Include source and reading gaps that affect the conclusion. A passed validator is evidence for identity and arithmetic checks; an independent semantic review is a separate statement with its own basis. Do not claim market coverage or a working paid integration from the offline demo.
