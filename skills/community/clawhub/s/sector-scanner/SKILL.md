---
name: sector-scanner
description: "A股板块资金流向扫描器。当用户询问板块资金热点、板块排名、资金流向、哪些板块在涨、热点扫描、板块强弱对比时触发。通过TDX通达信实时行情，对25个主题板块（半导体、AI算力、机器人、创新药、新能源车等）的个股进行量化评分，输出板块热度排名、个股详情和资金流向分类。支持扫描全部板块或指定板块，结果可导出为CSV。触发词：板块扫描、资金流向、热点板块、板块排名、资金热点、板块强弱。"
agent_created: true
---

# A股板块资金流向扫描器

## Overview

扫描A股主题板块的资金流向和热度排名。通过TDX通达信行情协议获取实时数据，对每只个股计算量化评分（均线趋势、MACD动量、量能、涨跌幅、价格位置），汇总为板块级别的热度标签和资金流向分类。

## 依赖安装

首次使用时，需在 managed Python venv 中安装 pytdx：

```bash
C:\Users\xfb\.workbuddy\binaries\python\versions\3.13.12\python.exe -m venv C:\Users\xfb\.workbuddy\binaries\python\envs\default
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\pip install pytdx
```

若 venv 已存在则跳过创建，直接执行 pip install。

## 扫描工作流

### 1. 扫描全部板块

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan.py --all --output json
```

进度信息输出到 stderr，JSON 结果输出到 stdout。

### 2. 扫描指定板块

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan.py --sectors semiconductor,ai_compute,robotics --output json
```

板块 ID 用逗号分隔。可用 `--list-sectors` 查看全部板块ID：

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan.py --list-sectors
```

### 3. 导出 CSV

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan.py --all --output csv --file <output_path>/scan_result.csv
```

生成两个文件：`scan_result.csv`（板块排名）和 `scan_result.detail.csv`（个股明细）。

### 4. 快速自检

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan.py --self-test
```

## JSON 输出结构

```json
{
  "scan_time": "2026-07-07T10:30:00",
  "source": "server_1",
  "total_sectors": 25,
  "total_stocks": 280,
  "sectors": [
    {
      "id": "semiconductor",
      "name": "半导体",
      "average_score": 63.8,
      "heat_label": "强势",
      "flow_label": "主力流入",
      "flow_level": 2,
      "red_count": 8,
      "total_count": 12,
      "up_ratio": 0.6667,
      "avg_pct_chg": 2.16,
      "stocks": [
        {
          "code": "688981",
          "name": "中芯国际",
          "price": 88.62,
          "pct_chg": 4.82,
          "score": 71.0,
          "flow_label": "主力流入",
          "flow_level": 2,
          "volume_ratio": 1.85,
          "details": ["MA多头排列+22", "MACD金叉+15", "放量上涨1.9x+14", "强势涨幅+14"]
        }
      ],
      "scanned_at": "2026-07-07T10:30:00",
      "source": "server_1",
      "errors": []
    }
  ]
}
```

## 结果呈现方式

扫描完成后，按以下方式向用户呈现结果：

### 板块排名表

用 Markdown 表格展示 TOP 10 板块排名：

| 排名 | 板块 | 均分 | 热度 | 红盘 | 均涨跌 | 资金流向 |
|------|------|------|------|------|--------|----------|
| 1 | 半导体 | 63.8 | 强势 | 8/12 | +2.16% | 主力流入 |
| 2 | AI算力 | 58.4 | 回暖 | 7/12 | +1.42% | 微流入 |
| ... | ... | ... | ... | ... | ... | ... |

### 资金流向汇总

- 主力流入板块：列出 flow_label 为"主力流入"的板块
- 微流入板块：列出 flow_label 为"微流入"的板块
- 主力流出板块：列出 flow_label 为"主力流出"的板块

### 个股精选

展示 TOP 3 板块中评分最高的个股：

| 板块 | 代码 | 名称 | 价格 | 涨跌幅 | 评分 | 资金流向 | 评分明细 |
|------|------|------|------|--------|------|----------|----------|
| 半导体 | 688981 | 中芯国际 | 88.62 | +4.82% | 71 | 主力流入 | MA多头排列+22, MACD金叉+15, ... |

### 可视化（可选）

当用户要求图表展示时，使用 show_widget 渲染：
- 板块排名柱状图（均分从高到低）
- 资金流向分布图（流入/流出板块数量）
- 板块红盘率对比图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --all | 扫描全部板块 | 是 |
| --sectors ID1,ID2 | 指定板块ID | - |
| --output json/csv | 输出格式 | json |
| --file PATH | CSV文件路径 | stdout |
| --self-test | 自检模式 | - |
| --list-sectors | 列出可用板块 | - |

## 板块列表

当前内置 25 个主题板块（config/sectors.json）：

创新药、人形机器人、AI算力、半导体、新能源车、医药、光伏储能、金融、消费、低空经济、商业航天、固态电池、AI应用、AI眼镜/消费电子、CPO光模块、PCB、液冷数据中心、稀土永磁、有色金属、军工、核电/可控核聚变、智能电网、影视传媒/Sora、券商

## 评分算法

详见 references/scoring_rules.md。核心维度：
- 均线趋势（MA5/10/20/60 多头排列）权重 35%
- MACD 动量（金叉/死叉）权重 25%
- 量能分析（量比放量/缩量）权重 20%
- 价格位置（20日高低位）权重 20%

## 错误处理

- TDX 连接失败：4 台服务器自动 failover，每台重试 3 次。全部失败时报错并提示用户稍后重试。
- 个股行情缺失：跳过该股，继续扫描，errors 字段记录失败信息。
- K线获取失败：仍用行情数据评分（精度降低），errors 字段记录。
- 非交易时间：TDX 返回上一交易日收盘数据，可正常扫描。

## 注意事项

- A股涨跌颜色：涨为红色，跌为绿色（中国市场惯例）。
- 评分仅供行情整理与复盘参考，不构成投资建议。
- config/sectors.json 可编辑：增减板块或调整个股列表。
- config/settings.json 可编辑：调整 TDX 服务器、超时时间、重试次数。
