# 新电脑安装指南

两条路线，按需要选：

- **方案 A：只装 Skill**（5 分钟）——纯框架/人格问答，不需要行情数据。
- **方案 B：Skill + 数据工具 `zt`**（推荐）——能看真实行情、跑指标/战法/回测。

> 远端仓库：https://github.com/lululu811/zettaranc-perspective

---

## 0. 前置条件

| 依赖 | 要求 | 说明 |
|---|---|---|
| Python | >= 3.12 | `python3 --version` 确认 |
| git | 任意近期版本 | 拉代码 |
| 磁盘 | 约 1 GB | 代码 + venv + 本地行情库 |
| 网络 | 能访问数据源 | 只装 Skill 时不需要 |

可选：Rust（加速回测）、Node.js（前端看板）、`pypinyin`（拼音搜股）。都不是必需。

---

## 方案 A：只装 Skill

```bash
# 1. 拿到 skill 目录（二选一）
git clone https://github.com/lululu811/zettaranc-perspective.git zettaranc-perspective
# 或：从旧电脑拷贝
# scp -r old-machine:/path/to/zettaranc-perspective ./zettaranc-perspective

# 2. 链接到 Claude Code 的 skills 目录
mkdir -p ~/.claude/skills
ln -s "$(pwd)/zettaranc-perspective" ~/.claude/skills/zettaranc-perspective

# 或者直接复制（不跟随更新）
# cp -R zettaranc-perspective ~/.claude/skills/
```

重启 Claude Code 会话，问一句「什么是少妇战法」验证。

**此时的状态**：没有 `zt`，Skill 自动进入离线模式——能聊框架、战法、职业/人生，但不能看真实行情。首次激活时它会明确告诉你数据工具没接。

---

## 方案 B：Skill + 数据工具

### B1. 安装 `zt`

```bash
git clone https://github.com/lululu811/zettaranc-skill.git
cd zettaranc-skill

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .                   # 注册 zt / zt-web / zt-monitor

zt --help                          # 应看到 16 个子命令
```

> Python < 3.12 会直接装不上；先用 `brew install python@3.12`、`pyenv` 或 python.org 安装包升级。

### B2. 配置数据源

```bash
cp .env.example .env
```

编辑 `.env`，三选一：

**① hithink（当前机器在用，推荐）**

```dotenv
DATA_MODE=jnb
HITHINK_FINANCE_API_KEY=sk-fuyao-xxxx
HITHINK_FINANCE_API_URL=https://fuyao.aicubes.cn
```

Key 获取：https://fuyao.aicubes.cn/admin

**② Tushare Pro**

```dotenv
DATA_MODE=jnb
TUSHARE_TOKEN=你的token
TUSHARE_API_URL=https://api.waditu.com/dataapi
```

注意 `TUSHARE_API_URL` 必须是**路径式中转地址**，官方根地址 `https://api.tushare.pro` 不行。

**③ 零配置免费源（a-stock-data）**

```dotenv
DATA_MODE=jnb
```

不配 Key 时自动走 a-stock-data（mootdx + 腾讯/百度）。能跑，但稳定性和速度不如付费源。

**④ 纯框架模式**

```dotenv
DATA_MODE=websearch
```

不取真实数据；`zt` 的行情类命令会没有数据可分析。

### B3. 初始化 + 首次同步

```bash
zt sync init                          # 建表；不做这步，zt sync status 会抛 no such table
zt sync sync 600519.SH --days 250     # 拉单只日线 + 指标缓存
zt sync status                        # 查看股票数 / K 线数（不支持 --json）
zt analyze 600519.SH --days 120 --json
```

> 只同步单只股票时，「股票」可能仍显示 0（`stock_basic` 未同步），以「K线」数为准。

最后一条应返回合法 JSON，包含 `price`、`indicators`、`strategies` 等字段。

### B4. 让 Claude Code 找到 `zt`

Skill 首次激活只做一件事：`command -v zt`。如果 `zt` 只在 venv 里、没进 PATH，Skill 会误判为离线。二选一：

```bash
# 方式 A：软链到已在 PATH 的目录（macOS/Linux）
ln -s /path/to/zettaranc-skill/.venv/bin/zt ~/.local/bin/zt

# 方式 B：把 venv/bin 加进 shell 配置
echo 'export PATH="/path/to/zettaranc-skill/.venv/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

验证：

```bash
command -v zt
zt sync status
```

### B5. 安装 Skill

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/zettaranc-perspective ~/.claude/skills/zettaranc-perspective
```

重启 Claude Code。现在问「帮我看看 600519.SH」应走真实数据；问「什么是四块砖」应走知识库。

---

## Windows 补充

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
zt --help
```

- `zt` 实际路径：`.venv\Scripts\zt.exe`；把 `.venv\Scripts` 加进用户 PATH。
- Skill 目录：`%USERPROFILE%\.claude\skills\zettaranc-perspective`。
- 用目录联接（不需要管理员）：

```cmd
mklink /J "%USERPROFILE%\.claude\skills\zettaranc-perspective" "C:\path\to\zettaranc-perspective"
```

- Claude Code 的 Bash 工具在 Windows 上通常走 Git Bash，`command -v zt` 可用；确保 Git Bash 的 PATH 能看到 `zt.exe`。

---

## 可选组件

| 组件 | 安装 | 用途 |
|---|---|---|
| Rust 加速核 | 安装 Rust 1.78+ + `pip install maturin`，在 `rust/crates/bindings` 下 `maturin develop --release` | 回测热路径加速；失败会自动回落 Python |
| 强制 Python 回测 | `export ZETTARANC_BACKTEST_IMPL=python` | 排查 Rust 相关问题 |
| API 服务 | `pip install fastapi uvicorn pydantic-settings`，然后 `zt-web` | http://localhost:8000 |
| 前端看板 | `cd frontend && npm install && npm run dev` | http://localhost:5173 |
| 拼音搜股 | `pip install pypinyin` | 股票搜索支持拼音首字母/全拼 |

---

## 验收清单

```bash
python3 --version                 # >= 3.12
command -v zt                     # 有输出
zt --help                         # 16 个子命令
zt sync status                    # 能看到数据库路径和 K 线数
zt analyze 600519.SH --days 120 --json   # 返回合法 JSON
```

Skill 侧：

```bash
ls -l ~/.claude/skills/zettaranc-perspective/SKILL.md
```

然后在 Claude Code 里问「什么是少妇战法」和「帮我看看 600519」各一次：前者应引用知识库，后者应调用 `zt analyze`。

---

## 常见问题

| 症状 | 原因 | 处理 |
|---|---|---|
| `python: command not found` | 系统只有 `python3` | 用 `python3` 替代 |
| `pip install -e .` 报 Python 版本不满足 | 低于 3.12 | 升级 Python |
| `zt: command not found` | venv 未激活 / PATH 没有 | `source .venv/bin/activate` 或按 B4 软链 |
| `no such table: stock_basic` | 数据库未初始化 | `zt sync init` |
| `zt sync status --json` 报参数错误 | `sync` 子命令不支持 `--json` | 去掉 `--json` |
| 同步成功但分析没数据 | 数据源/Key 没配好，或没同步该股票 | 看 `zt sync status`，再 `zt sync sync <code>` |
| Rust 构建失败 | 工具链不匹配 | 忽略；默认 `auto` 会回落 Python |
| `zt-web` 报缺 fastapi | API 依赖不在 requirements.txt | `pip install fastapi uvicorn pydantic-settings` |
| Skill 不触发 | 目录不在 `~/.claude/skills` 或没重启 | 检查软链，重启会话 |
| Skill 判定离线但终端能跑 `zt` | Claude Code 没继承 venv PATH | 按 B4 软链到全局 PATH |

---

## 安全

- `.env` 与 `data/` 都不入库；Key 只留本机。
- 不要把 `TUSHARE_TOKEN`、`HITHINK_FINANCE_API_KEY` 写进脚本或提交记录。
- Skill 的输出是分析框架，不是投资建议。
