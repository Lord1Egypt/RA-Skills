# skill-to-http-flash v1 → v2 迁移指南

> v2.0 不向 v1.x 兼容。已有 v1 project 必须重建。本文给出最少操作的迁移路径。

---

## 为什么不兼容

v1.x 执行链路是 `sessions_spawn → openclaw agent → LLM 解读 message → 调 skill`，
存在问题：
- ⚠️ 30s+ LLM 冷启
- ⚠️ LLM 漂移导致不复现
- ⚠️ 必须依赖 Gateway，跨环境难部署
- ⚠️ 入参出参都是"自由文本"，无 schema 校验，调用方写代码很痛

v2.0 改用 `subprocess.run(["python3", "scripts/main.py", "--foo", "x"])` 直执行 skill 入口：
- ✅ 毫秒级冷启
- ✅ 100% 复现
- ✅ 不依赖 Gateway
- ✅ JSON Schema 校验 + 长 flag CLI 映射，调用契约清晰

由于执行链路完全不同，server.py 模板、入参 schema 形态、响应 envelope 全变了，没有"中间兼容层"可以做。

---

## 最少迁移步骤（3 步）

### 1. 升级 skill-to-http-flash 到 2.0

```bash
# 通过 hub 重装（或 git pull）
openclaw skills install skill-to-http-flash
# 确认 version
grep ^version: ~/.openclaw/workspace/skills/skill-to-http-flash/SKILL.md
# → version: 2.0.0
```

### 2. 给被 flash 的 skill 加 `flash.entry`（推荐）

在 skill 的 `SKILL.md` frontmatter 加：

```yaml
---
name: my-skill
version: 1.0.0
...
flash:
  entry: scripts/main.py        # 相对 skill 目录的 .py 入口
  interpreter: python3          # 可选
---
```

> 没加也可以——v2.0 会启发式扫 `scripts/<name>.py` / `cli.py` / `main.py` / `run.py`。但加上更稳。

### 3. recreate 所有 v1 project

```bash
# 列出现有 project
python3 ~/.openclaw/workspace/skills/skill-to-http-flash/scripts/flash.py list

# 对每个 project：先停服务，再 remove，再 create
cd <output_dir> && python3 server.py stop
python3 flash.py remove --skill <name> --delete-files
python3 flash.py create --skill <name>
```

`recreate` 命令在 v2.0 也支持，但因为模板差异大，**首次从 v1 升级建议走 remove+create**，避免 stale params.json 干扰。

---

## 调用方代码需要改吗？

**几乎肯定要改**。v1 和 v2 的请求 / 响应都变了：

### 请求侧

| v1.x | v2.0 |
|---|---|
| `POST /run -d '{"message": "查一下昨天数据"}'`（LLM 解读）| `POST /run -d '{"date": "2026-05-26", "chart_id": "abc"}'`（CLI flag 映射）|

### 响应侧

| v1.x（自由文本） | v2.0（统一 envelope） |
|---|---|
| `{"output": "查询结果是...\n表格如下..."}` | `{"success":true, "exit_code":0, "elapsed_ms":240, "data":{...}}` 或 `{"output":"..."}` |

**v2.0 客户端通用读法**：
```js
const r = await fetch('/run', {method:'POST', body: JSON.stringify({...})}).then(r => r.json());
if (!r.success) {
  // r.error_type / r.error / r.stderr（业务失败时透出）
  throw new Error(`${r.error_type}: ${r.error || r.stderr}`);
}
const result = r.data ?? r.output;  // data 是结构化，output 是文本
```

---

## skill 脚本改造（让 flash 体验最佳）

- ✅ 用 `argparse` 长 flag（`--foo value`），别用 positional
- ✅ stdout 默认输出 JSON（让客户端走 `data` 字段结构化访问）
- ✅ 错误信息写 `stderr`、`sys.exit(非0)`（v2.0 会自动透出）

最小可用例子：
```python
#!/usr/bin/env python3
import argparse, json, sys
p = argparse.ArgumentParser()
p.add_argument("--name", required=True)
p.add_argument("--limit", type=int, default=10)
args = p.parse_args()
try:
    rows = [{"name": args.name, "i": i} for i in range(args.limit)]
    print(json.dumps({"rows": rows, "total": len(rows)}))
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
```

---

## 常见问题

### Q: server 启动报 entry_not_found 怎么办？
A: 看错误 message 里的 frontmatter patch 建议，给 SKILL.md 加 `flash.entry`。

### Q: 我的 skill 入口是 `.sh`，怎么办？
A: v2.0 不支持 shell entry（shell 难校验参数）。包一层 Python launcher：
```python
import subprocess, sys
subprocess.run(["bash", "scripts/my.sh"] + sys.argv[1:])
```

### Q: 旧 jobs.jsonl 还能查吗？
A: 不行。v1 v2 的 job 记录格式不同，建议升级前先 `flash.py jobs-export-sqlite` 导出做归档。

### Q: skill-to-http 还要装吗？
A: **不要**。v1.x 的"自动安装 skill-to-http"逻辑已经从 flash v2.0 完全删除，自带 `_cert.py` 处理 TLS。

### Q: 我有大量 v1 client 代码，能不能弄个兼容 shim？
A: v2.0 刻意不做 v1 兼容。技术上你可以自己写个 nginx 反代把 v1 风格请求转成 v2 envelope，但不推荐——不如直接改 client。

---

## 升级 checklist

- [ ] `skill-to-http-flash` 已升级到 2.0.0（`grep ^version SKILL.md`）
- [ ] 所有 v1 project 已 `remove`
- [ ] 被 flash 的 skill 已加 `flash.entry`（或确认启发式能找到 `.py`）
- [ ] 所有 project 已 `create`
- [ ] 所有调用方代码已改成读 v2.0 envelope（`data` 或 `output`）
- [ ] 跑通 `/health` 返回 `status:"ok"` + entry/interpreter 都 ok

完事撒花 🎉
