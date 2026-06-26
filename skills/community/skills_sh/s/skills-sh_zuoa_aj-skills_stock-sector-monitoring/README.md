# stock-sector-monitoring

A 股市场监测 skill，支持：
- 概念板块监测（`sector`）
- 龙虎榜（`lhb` / `top_list` / doc_id=106）
- 过滤 ST 类股票（`ST`、`*ST`、`S*ST`、`SST`）
- 结果输出并保存为 Markdown 报告

## 安装 Skill（npx skill add）

### 1) 从本地目录安装

```bash
npx skill add /Users/yujian/Code/py/aj-skills/skills/stock-sector-monitoring
```

### 2) 从 GitHub 安装

```bash
npx skills add https://github.com/zuoa/aj-skills --skill stock-sector-monitoring
```


安装后重启你的 Agent/Codex 会话以加载新 skill。

## 环境准备

```bash
cd /Users/yujian/Code/py/aj-skills/skills/stock-sector-monitoring
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install tushare pandas
```

配置 token：

```bash
export TUSHARE_TOKEN=YOUR_TOKEN
```

## 快速使用

### 龙虎榜（推荐）

```bash
source .venv/bin/activate
python3 scripts/sector-monitoring.py \
  --once \
  --data-source lhb \
  --trade-date 20260213 \
  --top 20 \
  --format json
```

### 指定单只股票

```bash
python3 scripts/sector-monitoring.py \
  --once \
  --data-source lhb \
  --trade-date 20260213 \
  --ts-code 002219.SZ \
  --format json
```

## Markdown 输出约定

建议将报告落到 `reports/`：
- `reports/lhb-YYYYMMDD.md`
- `reports/lhb-YYYYMMDD-TS_CODE.md`
- `reports/sector-YYYYMMDD.md`

报告建议包含：
- 参数区（数据源、日期、TopN、ST 过滤）
- 涨幅榜 Top N
- 综合评分 Top N
- 阈值预警
- 无数据说明（非交易日/无上榜/权限不足）

## 相关文件

- Skill 定义：`SKILL.md`
- 主脚本：`scripts/sector-monitoring.py`
