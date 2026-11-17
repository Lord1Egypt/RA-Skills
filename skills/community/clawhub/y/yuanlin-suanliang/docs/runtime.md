# 园林算量运行时

## 环境与运行时（自动解析，无需手工配置）

- 所有 `scripts/*.sh` 入口都 `source scripts/runtime_env.sh`，由它统一解析三件事：
  1. **解释器**：`CAD_SKILL_PYTHON` / `CODEX_PYTHON` → Codex 运行时 → PATH 上的 `python3.12/3.11` → `python3`（要求 ≥3.10）；
  2. **识图底座**：`CAD_SKILL_DIR` → 同级 `../cad-file-reader` → `~/.workbuddy/skills/*/cad-file-reader` → `~/.claude` → `$HOME/.codex`；
  3. **依赖路径**：把「本技能 scripts + 底座 scripts + 底座 vendor」拼进 `PYTHONPATH`，`ezdxf / ezdwg / openpyxl` 等**无需全局 pip 安装**。
- 推荐用对应的 `bash scripts/<入口>.sh`；直接 `python3 <入口>.py` 只在全局已装齐依赖时可用。
- 依赖缺失时按 `requirements.txt` 安装：`python3 -m pip install -r requirements.txt`。
