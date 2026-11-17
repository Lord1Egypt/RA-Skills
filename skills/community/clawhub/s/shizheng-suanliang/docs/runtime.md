# 市政算量运行时

## 环境与运行时（自动解析，无需手工配置）

- 所有 `scripts/*.sh` 入口都 `source scripts/runtime_env.sh`，由它统一解析三件事：
  1. **解释器**：`CAD_SKILL_PYTHON` / `CODEX_PYTHON` → Codex 运行时 → PATH 上的 `python3.12/3.11` → `python3`（要求 ≥3.10）；
  2. **识图底座**：`CAD_SKILL_DIR` → 同级 `../cad-file-reader` → `~/.workbuddy/skills/*/cad-file-reader` → `~/.claude` → `$HOME/.codex`；
  3. **依赖路径**：把「本技能 scripts + 底座 scripts + 底座 vendor」拼进 `PYTHONPATH`。
- 推荐用 `bash scripts/municipal_qty.sh ...`；直接 `python3 scripts/municipal_qty.py ...` 需要全局已装齐依赖（本技能只用 stdlib，通常没问题）。
- 本技能 `requirements.txt` 不声明任何第三方依赖：识图能力在 `cad-file-reader`，算量主入口纯 stdlib。

## 排障速查

| 症状 | 退出码 | 处置 |
|---|---|---|
| `--check-deps` 报缺 reader | 20 | `skillhub install cad-file-reader --namespace user_43faedd6` |
| `--check-deps` 报缺 bus | 21 | `bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply` |
| 契约 schema/单位/哈希不符 | 22 | 回 `cad-file-reader` 重新生成 `*.municipal.json` |
| 直接给了 DWG/DXF/DWT | 23 | 先走识图：`cad_scan.sh` → `cad_municipal_geometry.sh` |
| 文件入口缺 `--allow-manual` | 3 | 加 `--allow-manual`（结果 manual 降级）或改走 `--from-contract` |
| 契约证据为空 | 5 | 回识图层确认识图范围，勿硬算 |
| m 单位缺 `unit_scale` | GuardError(4) | 契约顶层补 `unit_scale: 1000` |

## 真图全链路（本机，数据不出本机）

```bash
# 1) 扫描（cad-file-reader）
bash ~/.codex/skills/cad-file-reader/scripts/cad_scan.sh 市政图.dwg \
    --with-mtext --with-insert --with-geom --with-geom-layer \
    --detail-json 市政详情.json --format json -o 市政扫描

# 2) 市政识图包
bash ~/.codex/skills/cad-file-reader/scripts/cad_municipal_geometry.sh \
    市政详情.json --out-dir 市政识图

# 3) 算量（文件降级入口）
bash scripts/municipal_qty.sh --municipal 市政识图/市政图.municipal.json \
    --allow-manual --out-prefix 市政算量
```

## Windows

入口 `.sh` 用 Git Bash/WSL 运行；或直接 `python scripts\municipal_qty.py`。UTF-8 由 `pyboot.ensure_utf8_io()` 兜底。
