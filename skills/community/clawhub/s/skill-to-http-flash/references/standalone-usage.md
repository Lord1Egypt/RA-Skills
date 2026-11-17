# skill-to-http-flash v2.0 — Standalone 使用指南

> 在**非 OpenClaw 环境**（公网 / 私有云 / 同事的笔记本 / CI runner）跑 flash 的完整指南。

---

## 设计前提

v2.0 把 standalone 当作**一等公民**，三处软依赖全部清理：

| 软依赖 | v2.0 处理 |
|---|---|
| Skill 路径 `~/.openclaw/workspace/skills/` | `--skill-dir` flag + `FLASH_SKILL_DIR` env |
| Flash 数据目录 `<workspace>/.skill-to-http-flash/` | `--data-dir` flag + `FLASH_DATA_DIR` env |
| `skill-to-http` 复用（tls_auth / gen_cert）| **删除**自动安装链路，自带精简版 `_cert.py` |

---

## 5 分钟跑通

```bash
# 1. 安装 Python 依赖（任何 Linux/macOS 都行）
pip install fastapi 'uvicorn[standard]' pydantic cryptography jsonschema

# 2. 准备 skill 目录
mkdir -p ~/my-skills/hello-world/scripts

cat > ~/my-skills/hello-world/SKILL.md <<'EOF'
---
name: hello-world
version: 1.0.0
description: standalone demo
flash:
  entry: scripts/main.py
---
EOF

cat > ~/my-skills/hello-world/scripts/main.py <<'EOF'
#!/usr/bin/env python3
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("--name", default="world")
a = p.parse_args()
print(json.dumps({"hello": a.name, "from": "standalone"}))
EOF

# 3. 把 skill-to-http-flash 仓库 clone 到任意位置
git clone <skill-to-http-flash repo> ~/flash-tools

# 4. 创建项目（CLI flag 模式）
python3 ~/flash-tools/scripts/flash.py \
  --skill-dir ~/my-skills \
  --data-dir ~/flash-data \
  create --skill hello-world

# 5. 启动 & 调
cd ~/flash-data/services/hello-world-api
pip install -r requirements.txt
python3 server.py start &
curl -X POST http://127.0.0.1:7780/run \
  -H 'content-type: application/json' \
  -d '{"name":"Anthropic"}'
# {"success":true,"exit_code":0,"elapsed_ms":18,
#  "data":{"hello":"Anthropic","from":"standalone"},"output":null}
```

---

## 路径覆盖：CLI flag 与 env 两套都行

### 方式 A — Env 变量（推荐：脚本化 / Dockerfile / 长期使用）

```bash
export FLASH_SKILL_DIR=/data/skills
export FLASH_DATA_DIR=/data/flash
export OPENCLAW_HTTP_ROOT=/data/http     # 证书 / API Key 存这里

python3 flash.py create --skill my-skill   # 自动读 env
python3 flash.py list                       # 同样自动读
```

### 方式 B — CLI Flag（一次性测试 / 多 skill 仓库快切）

```bash
python3 flash.py \
  --skill-dir /path/to/skills \
  --data-dir /path/to/flash \
  create --skill my-skill
```

CLI flag 优先级 > env 变量 > 默认值。

### 探测顺序

| 资源 | 优先级 |
|---|---|
| **skill 搜索目录** | `--skill-dir` → `FLASH_SKILL_DIR` env → 多 agent 默认（`~/.openclaw/workspace/skills` → `~/.claude/skills` → `~/.cursor/skills` → `~/.config/skills` → `./skills` → `/app/skills`）→ `openclaw.json:extraDirs` |
| **flash 数据目录** | `--data-dir` → `FLASH_DATA_DIR` env → `OPENCLAW_FLASH_DATA_DIR` env → `<workspace>/.skill-to-http-flash/` → `~/.skill-to-http-flash/` |
| **证书/API Key 根目录** | `OPENCLAW_HTTP_ROOT` env → `<workspace>/.http/` → `~/.http/` |

---

## 运行时（server.py）的 standalone 行为

`server.py` 模板把 `SKILL_DIR` / `ENTRY_REL` 编译到代码常量。运行时：

- `FLASH_SKILL_DIR` env **覆盖** `SKILL_DIR`（搬迁 skill 目录后无需重 generate）
- `FLASH_DATA_DIR` env **覆盖**持久化目录（PID / JSONL / log）
- `FLASH_API_KEY` env **直接配** API Key（不读文件）
- `FLASH_TLS_ENABLED=1` env **运行时**强制开/关 HTTPS（不重生代码）

最少 standalone 启动：
```bash
FLASH_DATA_DIR=/data/flash \
  python3 server.py start
```

---

## TLS 证书（standalone）

自带 `_cert.py`，**优先用 openssl CLI**（依赖少）、**回退 cryptography 库**：

```bash
# 仅生成证书（不依赖 OpenClaw skill-to-http）
python3 ~/flash-tools/scripts/_cert.py
# → /tmp/flash-cert-test/server.{crt,key}

# flash project 切到 HTTPS
python3 flash.py recreate --skill my-skill --tls-enabled

# 查看 / 续期 / 导入
python3 flash.py cert --skill my-skill --cert-action info
python3 flash.py cert --skill my-skill --cert-action renew
python3 flash.py cert --skill my-skill --cert-action import \
  --cert-src /path/to/wildcard.crt --key-src /path/to/wildcard.key
```

证书自动 SAN 嗅探本机所有 IP，有效期 825 天（Chrome 上限），key 自动 `chmod 0o600`。

---

## Docker / K8s 部署示例

### Dockerfile

```dockerfile
FROM python:3.11-slim
RUN pip install fastapi 'uvicorn[standard]' pydantic cryptography jsonschema
COPY ./skills /skills
COPY ./skill-to-http-flash /flash-tools

ENV FLASH_SKILL_DIR=/skills
ENV FLASH_DATA_DIR=/data/flash
ENV OPENCLAW_HTTP_ROOT=/data/http

WORKDIR /flash-tools
RUN python3 scripts/flash.py create --skill my-skill <<<"y
7780
60
n"

WORKDIR /data/flash/services/my-skill-api
EXPOSE 7780
CMD ["python3", "server.py", "start"]
```

### K8s

挂 PVC 到 `/data/flash`、`/data/http`，重启不丢 PID / cert / API key。

---

## 常见坑

### Q: server.py 启动报 `entry_not_found`，但本地能跑？
A: 上一轮 P3 修过的 bug — 必须用绝对路径。检查 server.py 里 `SKILL_DIR = '...'` 是不是绝对路径。v2.0 已强制 `.resolve()`。

### Q: 我的 skill 装在 git repo 里，没法挂 PVC，怎么搬？
A: 整个 `<output_dir>` 是自包含的（`server.py` 内嵌代码）。直接 `tar` / `scp` 到目标机器，挂 env 跑即可。

### Q: 不想用 jsonschema 行不行？
A: 行，flash 入参校验对 jsonschema **降级处理**（找不到 jsonschema 时只做字段名白名单 + required 检查）。但生成项目的 `requirements.txt` 默认列了 jsonschema。

### Q: 多个 flash project 共享同一个 data-dir 冲突吗？
A: 不会。每个 skill 独立的 `<skill>.pid` / `<skill>.jsonl` / `services/<skill>-api/`。共享反而方便统一管理。

### Q: standalone 模式下 LLM 提 schema 失败了？
A: standalone 通常没有 LLM config，flash **自动 fallback** 到最小 schema（`{type:object, properties:{}, additionalProperties:true, required:[]}`）。可以正常跑，只是没有 schema 校验。建议手动补 params.json 后 recreate。

---

## 最小依赖清单（standalone）

```
python>=3.10
fastapi
uvicorn[standard]
pydantic>=2
cryptography
jsonschema           # optional but recommended
```

`bins`: `python3`，`openssl`（可选，没有就走 cryptography 回退）

无 OpenClaw，无 Gateway，无 LLM API。
