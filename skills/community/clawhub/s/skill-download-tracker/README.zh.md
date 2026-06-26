# ClawHub 下载量追踪

定时监控你在 ClawHub 上发布的技能下载量，自动记录变化趋势并推送异动提醒。支持日/周/月报告。

## 文件结构

```
~/.openclaw/workspace/skills/clawhub-download-tracker/
├── SKILL.md                  # 本文件（英文版）
├── README.zh.md              # 中文说明
├── clawhub_tracker.py        # 主脚本：采集 + 报告 + 飞书推送
├── clawhub_tracker.sh        # launchd 入口包装（设置 PATH）
└── test_clawhub_tracker.py   # 测试脚本（mock 数据，19 个用例）

~/.openclaw/workspace/data/clawhub-tracker/
├── skills.csv                # 监控列表：slug,note
├── checklog.csv              # 历史记录：timestamp,slug,downloads,delta
└── reports/                  # 报告存档（按月 .md 文件）
```

## 前置依赖

- `clawhub` CLI 已安装（脚本通过 `shutil.which` + fallback 自动定位）
- Python 3（macOS 自带）
- 飞书 APP_ID / APP_SECRET / USER_OPEN_ID，通过环境变量配置：
  - `CLAWHUB_FEISHU_APP_ID`
  - `CLAWHUB_FEISHU_APP_SECRET`
  - `CLAWHUB_FEISHU_USER_OPEN_ID`
  - （环境变量未设置时，可创建 `~/.openclaw/workspace/data/clawhub-tracker/.env` 配置文件）

## 操作

### 1. 采集当前下载量（即时快照 + 飞书推送）

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py
```

遍历 `skills.csv` 中的所有 slug，获取最新下载量，计算 delta，写入 `checklog.csv`，存档到 `reports/`，推送飞书通知。

### 2. 报告

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report daily   # 今日报告
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report weekly  # 最近 7 天
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report monthly # 当月
```

根据 `checklog.csv` 历史数据生成报告，内容包括：
- 各 slug 周期起始 → 结束下载量，累计 delta
- 采样次数与峰值时段
- 总计新增与当前总量

报告同时打印到 stdout、存档到 `reports/YYYY-MM.md`、推送飞书。

### 3. 添加 / 删除监控技能

直接编辑 `~/.openclaw/workspace/data/clawhub-tracker/skills.csv`，格式：`slug,note`

## 数据源

通过 `clawhub inspect <slug> --json` 获取官方 `stats.downloads` 字段，数据来自 ClawHub 注册中心，**不涉及第三方 API**。

当前监控列表以 `~/.openclaw/workspace/data/clawhub-tracker/skills.csv` 为准（动态维护）。
