# SIFS Command Recipes

## Discovery

```bash
sifs agent-context --json
sifs capabilities --json
sifs status --source <project> --json
```

## Search

```bash
sifs search "query text" --source <project>
sifs search "exact_symbol" --source <project> --mode bm25 --json
sifs search "conceptual behavior" --source <project> --mode hybrid --limit 10
sifs search "parser error handling" --source <project> --filter-path src/parser.rs
```

## Inspect Results

```bash
sifs list-files --source <project> --limit 200 --json
sifs get <file_path> <line> --source <project>
sifs find-related <file_path> <line> --source <project> --limit 10 --json
```

## Profiles

```bash
sifs profile save current --source <project> --mode bm25 --offline --json
sifs search "startup handshake" --profile current --json
```

## Agent Integration

```bash
sifs agent print --target codex --artifact snippet
sifs agent install --target codex --artifact snippet --file AGENTS.md --dry-run --json
sifs agent doctor --target codex --json
```
