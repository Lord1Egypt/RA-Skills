# Mode B: On-demand Re-scan

Run when user asks to "scan again", "find more savings", "what else can I optimize", etc.

---

## Steps

1. Run the scanner (same command as Mode A Step 1):
   ```bash
   python3 <skill-install-path>/scripts/scan_workspace.py --workspace .
   ```
   Optionally add `--dry-run` to preview without modifying files.

2. Also do the manual deep scan from Mode A Step 5 above.

3. Compare against what's already been done — don't re-suggest already-moved content.

4. Present new findings and guide through the same move/confirm flow.

5. Support **batch mode**: if user says "just do it all", execute without per-item confirmation, then deliver a unified change report.

6. Report delta:
   ```
   X new issues found, ~Y tokens/session saved if addressed
   （×100 sessions/day = ~Z tokens/day，×22 working days = ~W tokens/month）
   ```

---

## Dry-run Flag

Always offer `--dry-run` first for large batch operations:

```bash
python3 <skill-install-path>/scripts/scan_workspace.py --workspace . --dry-run
```

This shows what would be changed without touching any files — useful before committing to a batch cleanup.
