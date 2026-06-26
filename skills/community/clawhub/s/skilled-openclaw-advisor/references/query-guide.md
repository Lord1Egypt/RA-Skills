# Query Guide — openclaw-docs skill

For use by all agents (Ada, K2, Cora, Winston, Synergy).

## One-liner (agent mode)

```bash
python3 $SKILL_DIR/scripts/query_index.py --query "QUESTION" --mode agent
```

Returns 1-3 compact lines. Sufficient for most routing/config decisions.

## Need more context?

```bash
python3 $SKILL_DIR/scripts/query_index.py --query "QUESTION" --mode agent --verbosity standard
```

## Human-readable answer

```bash
python3 $SKILL_DIR/scripts/query_index.py --query "QUESTION"
```

## Check what changed in latest update

```bash
python3 $SKILL_DIR/scripts/query_index.py --diff
```

## Index status

```bash
python3 $SKILL_DIR/scripts/query_index.py --status
```
