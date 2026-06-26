# Release v0.2.1 — Security Hardening / 安全加固

**Release date / 发布日期:** 2026-03-16
**Author / 作者:** 圆规

---

## Highlights / 亮点

### Security / 安全
- **Command validation gate** — All test commands now pass through `validate_command()` before execution, enforcing: interpreter whitelist (`python3` only), inline code block (`-c`, `exec(`), absolute path block, path traversal block, and prefix whitelist.
  所有测试命令执行前通过多层安全校验。

- **Safe state probes** — New `scripts/state_probe.py` replaces all inline `python -c` + `exec(open(...).read())` patterns in `config/task-suite.json` with safe, auditable probe functions.
  新增安全状态探针，替代所有内联代码执行。

- **Removed hardcoded paths** — All absolute paths (`/Users/...`) removed from task definitions.
  移除所有硬编码绝对路径。

### Metadata / 元数据
- Author updated to `圆规` across all files.
  作者信息统一更新为"圆规"。

- LLM judge behavior clarified: off by default, explicit opt-in required.
  明确 LLM 裁判功能默认关闭。

---

## Upgrade Notes / 升级说明

- **No breaking changes** to the CLI interface. All existing commands work as before.
  CLI 接口无破坏性变更，所有命令照常使用。

- If you have custom test definitions in `task-suite.json`, ensure they comply with the new command validation rules (no `-c`, no absolute paths, no `..`).
  如果有自定义测试定义，请确保符合新的命令安全规则。

---

## Quick Verify / 快速验证

```bash
# Health check / 健康检查
python3 scripts/check.py

# Quick eval / 快速评估
python3 scripts/eval.py --mode quick --no-probes

# Standard eval + report / 标准评估
python3 scripts/eval.py --mode standard --format markdown
```

---

## Full Changelog / 完整变更日志

See [CHANGELOG.md](./CHANGELOG.md) for detailed changes.
