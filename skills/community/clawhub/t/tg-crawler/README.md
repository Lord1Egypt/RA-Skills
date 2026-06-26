# TG-Crawler — Telegram 舆情采集工具

基于 Telethon 的 Telegram 频道/群组消息采集与舆情监控 OpenClaw Skill。

## 功能概览

| 模式 | 说明 |
|------|------|
| **hybrid** | 发现 + 回溯（推荐），先搜频道再爬消息 |
| **discover** | 仅发现频道，搜索并保存频道列表 |
| **backfill** | 仅回溯消息，对已有频道爬取历史消息 |
| **monitor** | 7×24 实时监听新消息 |
| **export** | 导出采集数据（CSV / JSON / Markdown） |

## 运行环境

- **Python** ≥ 3.10
- **Telegram 账号**（至少 1 个，用于调用 TG API）
- **代理（推荐）**：SOCKS5 代理以规避 GFW 封锁

## 快速开始

### 第一步：获取 TG API 凭证

1. 打开浏览器访问 **https://my.telegram.org/apps**
2. 用你的 TG 账号登录（需要已绑定手机号，会收到验证码）
3. 登录后点击 **「Create application」** 或选择一个已有应用
4. 记录以下信息：
   - `api_id` — 一串数字（如 `12345678`）
   - `api_hash` — 一串字母数字（如 `a1b2c3d4e5f6...`）

> ⚠️ **api_id 和 api_hash 是敏感凭证，不要分享给他人！**

### 第二步：配置 .env 文件

```bash
cd tg-crawler/config
cp .env.example .env
```

编辑 `.env` 文件，填入你的凭证：

```ini
# 必填：至少配置账号 1
TG1_API_ID=你的api_id
TG1_API_HASH=你的api_hash
TG1_PHONE=+8613800138000
```

如果你在中国大陆，还需配置 SOCKS5 代理：

```ini
# 在你自己的代理服务器上运行：
# ssh -D 1080 -N -f user@your-vps.com
# 然后配置全局代理：
PROXY_HOST=127.0.0.1
PROXY_PORT=1080
```

> 💡 详见 `references/proxy-pool-setup.md` 了解多 IP 隔离代理池方案。

### 第三步：安装 Python 依赖

```bash
cd tg-crawler/scripts
pip install -r requirements.txt
```

### 第四步：验证账号连接

使用 `--dry-run` 试运行，验证配置是否正确：

```bash
cd tg-crawler/scripts
python3 main.py --mode discover --keywords "测试" --dry-run
```

如果输出显示「Dry-run mode」执行计划且无报错，说明参数配置正确。

### 第五步：首次登录验证

首次运行时，TG 会要求验证码验证：

```bash
# 交互式输入验证码（终端可用时）
python3 main.py --mode discover --keywords "游戏外挂"

# 非交互环境：将验证码写入文件
echo "12345" > /tmp/tg_code.txt
python3 main.py --mode discover --keywords "游戏外挂" --code-file /tmp/tg_code.txt
```

验证成功后，会在 `scripts/` 和 `config/` 目录下生成 `.session` 文件。之后运行无需再次验证。

> ⚠️ 如果账号开启了**二次验证（2FA）**，需要传 `--password 你的2FA密码`。

---

## 使用指南

### 场景一：首次扫描某个行业（推荐 hybrid）

**两步法：先用生态词发现频道 → 再用精准词回溯消息。**

```bash
# 以「游戏外挂」为例
python3 main.py --mode hybrid \
  --keywords "外挂,辅助,破解,脚本" \
  --backfill-keywords "和平精英,王者荣耀,原神" \
  --targets ../config/targets.yaml \
  --backfill-limit 500
```

参数说明：

| 参数 | 作用 |
|------|------|
| `--keywords` | **discover 阶段**：用于搜索发现频道的生态关键词（范围大） |
| `--backfill-keywords` | **backfill 阶段**：在频道内搜索匹配的精准关键词（范围小） |
| `--targets` | 频道配置文件路径 |
| `--backfill-limit` | 每个频道最多回溯多少条消息 |

### 场景二：对已有频道回溯消息

```bash
python3 main.py --mode backfill \
  --backfill-keywords "关键词1,关键词2" \
  --targets ../config/targets_gaming.yaml \
  --backfill-limit 300
```

### 场景三：仅发现新频道

```bash
python3 main.py --mode discover \
  --keywords "外挂,辅助,破解" \
  --targets ../config/targets.yaml
```

新发现的频道会自动追加到 targets 配置文件中。

### 场景四：持续监控

```bash
# 后台运行，持续监听
python3 main.py --mode monitor --targets ../config/targets.yaml &
```

### 场景五：导出数据

```bash
# 导出为 CSV
python3 main.py --export results.csv --since 2026-01-01

# 导出为 Markdown 报告
python3 main.py --export report.md --export-format markdown --since 2026-01-01
```

---

## 不同行业的搜索关键词

TG 上不同行业的黑灰产分布在完全不同的频道生态中，搜索关键词必须根据行业调整：

| 行业 | 搜索关键词 | 禁止用 |
|------|-----------|--------|
| 🎮 游戏 | 游戏名、外挂、辅助、破解 | 优惠券、漏洞单 |
| 🥛 快消/零售 | 优惠券、薅羊毛、漏洞、线报、Bug价 | 外挂、破解 |
| 💰 金融 | 套利、路子、代刷、水钱 | 优惠券、外挂 |
| 📱 App | 破解版、Mod、去广告、解锁 | 优惠券 |
| 💬 社交 | 交友、引流、号商、脚本、代聊 | 外挂 |

> 📖 更多行业两步法完整命令 → `references/industry-playbook.md`

---

## 常用参数速查

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | hybrid / discover / backfill / monitor | — |
| `--keywords` | discover 搜索关键词，逗号分隔 | — |
| `--backfill-keywords` | backfill 精准关键词 | 回退用 `--keywords` |
| `--targets` | 频道配置文件路径 | `../config/targets.yaml` |
| `--backfill-limit` | 单频道回溯消息数 | 500 |
| `--account` | 使用哪个 TG 账号（1/2/3） | 1 |
| `--failover` | 失败后尝试后续 N 个备用账号 | 0 |
| `--fetch-sender` | 获取消息发送者信息 | false |
| `--retention-days` | 数据自动清理天数 | 90 |
| `--dry-run` | 试运行，不连接 TG | false |
| `--export` | 导出文件路径 | — |
| `--export-format` | csv / json / markdown | csv |
| `--since` / `--until` | 导出时间范围 YYYY-MM-DD | — |
| `--log-level` | DEBUG / INFO / WARNING / ERROR | INFO |

---

## 文件结构

```
tg-crawler/
├── SKILL.md              # OpenClaw Skill 定义
├── README.md             # 本文件
├── config/
│   ├── .env              # 你的凭证（不提交）
│   ├── .env.example      # 凭证模板
│   └── targets*.yaml     # 频道配置文件
├── scripts/
│   ├── main.py           # 入口
│   ├── database.py       # 数据库管理
│   ├── channel_discoverer.py  # 频道发现
│   ├── monitor.py        # 实时监控
│   ├── keyword_filter.py # 关键词过滤
│   ├── deduplicator.py   # 去重
│   ├── sender_cache.py   # 发送者缓存
│   └── config_loader.py  # 配置加载
├── data/
│   └── crawler.db        # SQLite 数据库（自动生成）
├── references/
│   ├── industry-playbook.md    # 各行业完整命令
│   ├── proxy-pool-setup.md     # 代理池自建方案
│   ├── targets-format.md       # targets 配置格式说明
│   └── tg-crawler-architecture.md  # 架构设计文档
```

---

## 常见问题

### Q: 运行时报 `FloodWaitError` 怎么办？

TG API 有严格的频率限制。应对方案：
1. 等待提示的冷却时间
2. 使用 `--failover 2` 自动切换到备用账号
3. 减小 `--backfill-limit` 值

### Q: 收到 `The phone number is banned`？

该 TG 账号被 TG 官方封禁，需要换一个账号。

### Q: 在中国大陆无法连接 TG API？

需要配置 SOCKS5 代理。最简单的方式：
```bash
# 在你自己的海外 VPS 上运行：
ssh -D 1080 -N -f user@your-vps.com
```
然后在 `.env` 中配置 `PROXY_HOST=127.0.0.1` 和 `PROXY_PORT=1080`。

详见 `references/proxy-pool-setup.md`。

### Q: 如何清空已采集的数据重新开始？

```bash
# 方法一：清空数据库
sqlite3 data/crawler.db "DELETE FROM messages; DELETE FROM channel_progress; VACUUM;"

# 方法二：导出后清空
python3 main.py --export backup.csv --purge-after-export
```

### Q: discover 阶段没有发现频道？

可能原因：
1. 关键词太精准——尝试更宽泛的生态词
2. 代理未生效——检查 SOCKS5 连接
3. 目标行业在 TG 上生态薄弱——考虑切换到 `web_search`（微博/知乎/黑猫投诉）

---

## 技术支持

- 详细架构说明：`references/tg-crawler-architecture.md`
- 各行业实战手册：`references/industry-playbook.md`
- OpenClaw Skill 定义：`SKILL.md`
