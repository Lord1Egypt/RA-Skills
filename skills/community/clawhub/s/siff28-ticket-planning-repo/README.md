# SIFF 2026 买票行程规划 Skill

> 第 28 届上海国际电影节（SIFF 2026）专用 Hermes Agent skill

## 功能

- 从任意影片清单（豆瓣/豆列、文本、截图、Excel 等）提取片名
- 自动匹配 SIFF 2026 官方排片表（含 1574 场上海展映 + 36 场长三角展映）
- 评估片长、散场缓冲、跨影院驾车/地铁交通时间
- 输出带优先级的买票顺序、日程安排、转场风险、备选场次
- 支持导出 CSV 和 iCal

## 内置数据

| 文件 | 说明 |
|------|------|
| `references/siff2026/siff2026-official-cndata-20260603-001.json` | 官方排片 JSON（1610 场） |
| `references/siff2026/第28届上海国际电影节排片表-官方.xlsx` | 官方 Excel 原始文件 |
| `references/siff2026/siff2026-cinema-coordinates.csv` | 44 家影院坐标 |
| `references/siff2026/siff2026-cinema-driving-matrix-osrm.csv` | 44×44 驾车距离/时间矩阵（OSRM） |
| `references/siff2026/siff2026-cinema-metro-matrix-estimated.csv` | 44×44 地铁移动时间矩阵 |
| `references/siff2026/siff2026-cinema-nearest-metro-stations.csv` | 每家影院最近地铁站 |

## 安装

### 方式一：Hermes Agent 内直接安装

```bash
hermes skills install --from github fffonion/siff26-ticket-planning
```

### 方式二：手动安装

```bash
# 克隆到 Hermes skills 目录
git clone https://github.com/fffonion/siff26-ticket-planning.git \
  ~/.hermes/skills/leisure/siff26-ticket-planning
```

## 使用方法

在 Hermes Agent 对话中，加载此 skill 后直接发送影片清单即可：

```
/SIFF26 请帮我规划行程：
- 怦然心动
- 原始星球
- 时间之主
- 当哈利遇到莎莉
```

支持的输入格式：
- 豆列 URL（自动抓取）
- 豆瓣/IMDb/Letterboxd 页面 URL
- 任意文本列表
- 截图（OCR 识别）
- 本地文件

## 交通数据说明

- **驾车矩阵**：基于 OSRM 公共接口的自由流耗时，按时段加系数：
  - 早/晚高峰：×2.0 或 +20min
  - 周末商圈高峰：×1.6 或 +15min
  - 平峰：×1.3 或 +10min
- **地铁矩阵**：基于 MetroFlow 2017 站点邻接图最短路 + 步行估算，非实时列车时刻
- 深夜场需额外查末班车或改用驾车

## 数据来源

- 排片数据：SIFF 官网 (siff.com) 抓取
- 影院坐标：OpenStreetMap Overpass API
- 驾车时间：OSRM 公共接口
- 地铁邻接：[MetroFlow](https://figshare.com/collections/ARIZONA_Sun/4209384)

## License

MIT
