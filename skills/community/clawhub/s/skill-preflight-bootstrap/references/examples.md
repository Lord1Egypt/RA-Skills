# Examples

## 基本初始化

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo
```

预期结果：

- 目标仓库生成 `scripts/skill-preflight.py`
- 生成 `.codex/settings.json` 和 `.claude/settings.json`
- 生成 `.learnings/` 和 `docs/skill-preflight-usage.md`
- `AGENTS.md` 里带上技能预检片段

## 先看计划

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo --dry-run
```

适合：

- 目标仓库已有较多自定义配置
- 想确认会不会覆盖已有文件
- 想在 CI 或自动化流程里先审查输出

## 验收命令

```bash
tmpdir="$(mktemp -d)"
python3 scripts/bootstrap-skill-preflight.py "$tmpdir"
python3 -m json.tool "$tmpdir/.codex/settings.json" >/dev/null
python3 -m json.tool "$tmpdir/.claude/settings.json" >/dev/null
python3 "$tmpdir/scripts/skill-preflight.py" "react performance"
```

## 二次执行

同一个目标目录再次执行时，默认行为应为：

- 已存在模板文件跳过
- hook 配置继续保持合并
- `AGENTS.md` 片段不重复追加

可以用下面命令检查：

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo
rg -c "技能优先与任务前预检（强制）" /path/to/target-repo/AGENTS.md
```
