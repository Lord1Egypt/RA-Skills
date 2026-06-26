# TeslaMate Grafana Skills

通过 Grafana API 查询特斯拉车辆数据和行程的 OpenClaw 技能。

## 功能特性

- 🚗 **车辆状态** - 实时查看电池电量、续航里程、车辆状态
- 🛣️ **行程记录** - 查询历史行程，包含出发/到达地址（反向地理编码）
- 🗺️ **路线规划** - 计算两点之间的距离、时间和能耗预估
- 📊 **数据可视化** - 支持 Grafana Dashboard 数据查询
- 📈 **能耗趋势** - 30天能耗走势分析
- 🏆 **里程里程碑** - 总里程成就系统
- 🏎️ **驾驶评分** - 根据驾驶行为打分
- 🔋 **电池健康度** - 电池容量估算
- 💰 **充电费用** - 充电成本统计
- 📍 **常去地点** - 频繁访问位置统计
- 🦇 **驻车消耗** - 哨兵模式/空调消耗分析
- 📊 **状态统计** - 车辆在线/离线/驾驶时长统计

## 环境要求

- TeslaMate 已部署并配置 Grafana
- Grafana 运行在可访问的服务器上
- Python 3.7+

## 配置

在 `memory/teslamate-grafana-config.json` 中配置：

```json
{
  "grafana_url": "http://192.168.1.100:3000",
  "datasource_id": 1
}
```

## 使用方法

### 快速命令

```bash
# 车辆状态
python3 scripts/query_teslamate.py --status
# 输出: Battery: 85% | Range: 420 km | State: online | Today: 45 km

# 最近行程
python3 scripts/query_teslamate.py --drives 5

# 路线规划
python3 scripts/query_teslamate.py --route "广州珠江新城"
```

### 实用功能

```bash
# 周报
python3 scripts/query_teslamate.py --report

# 月度统计
python3 scripts/query_teslamate.py --monthly

# 能耗趋势 (30天)
python3 scripts/query_teslamate.py --trend

# 驾驶评分
python3 scripts/query_teslamate.py --score

# 里程里程碑
python3 scripts/query_teslamate.py --milestones

# 充电费用 (默认1.5元/度)
python3 scripts/query_teslamate.py --cost

# 里程预测
python3 scripts/query_teslamate.py --range

# 电池健康度
python3 scripts/query_teslamate.py --health
```

### 趣味功能

```bash
# 常去地点 TOP10
python3 scripts/query_teslamate.py --places

# 驻车消耗分析
python3 scripts/query_teslamate.py --drain

# 车辆状态统计
python3 scripts/query_teslamate.py --states

# 充电统计
python3 scripts/query_teslamate.py --charging

# 能耗统计
python3 scripts/query_teslamate.py --efficiency
```

### 其他命令

```bash
# 异常检查
python3 scripts/query_teslamate.py --alerts

# 温度监控
python3 scripts/query_teslamate.py --temp

# 车辆位置
python3 scripts/query_teslamate.py --location

# 完整仪表盘
python3 scripts/query_teslamate.py --full
```

## 命令列表

| 命令 | 功能 |
|------|------|
| `--status` | 快速状态：电量、续航、状态、今日里程 |
| `--drives [N]` | 最近N条行程（含地址） |
| `--route <地址>` | 路线规划（距离、时间、能耗预估） |
| `--report` | 周报（本周行驶、充电、能耗） |
| `--monthly` | 月度统计（本月+预计全月） |
| `--trend` | 能耗趋势（30天每日能耗） |
| `--score` | 驾驶评分（基于速度行为） |
| `--milestones` | 里程里程碑（成就系统） |
| `--charging` | 充电统计（30天） |
| `--efficiency` | 能耗统计（平均Wh/km） |
| `--cost` | 充电费用（默认1.5元/度） |
| `--range` | 里程预测（剩余续航估算） |
| `--health` | 电池健康度（容量估算） |
| `--places` | 常去地点 TOP10 |
| `--drain` | 驻车消耗分析 |
| `--states` | 车辆状态统计 |
| `--alerts` | 异常检查（低电量、离线等） |
| `--temp` | 温度监控 |
| `--location` | 当前位置 |
| `--full` | 完整仪表盘 |

## 在 OpenClaw 中使用

将技能添加到你的 OpenClaw 工作空间：

```bash
cp -r TeslaMateSkills ~/.openclaw/workspace/skills/teslamate-grafana
```

然后在对话中直接使用：
- "查询特斯拉状态"
- "今天的行程有哪些"
- "我的驾驶评分多少"
- "本月跑了多少公里"

## 技术原理

- **数据源**: 通过 Grafana 的 PostgreSQL 数据源查询 TeslaMate 数据库
- **地理编码**: 使用 Nominatim (OpenStreetMap) 进行反向地理编码
- **路线计算**: 使用 OSRM (Open Source Routing Machine) 计算路线和能耗

## 数据字段说明

### 车辆状态
| 字段 | 说明 |
|------|------|
| battery | 电池电量百分比 |
| range_km | 预估续航里程(km) |
| state | 车辆状态 (online/sleeping/offline) |
| today_km | 今日行驶里程 |

### 行程记录
| 字段 | 说明 |
|------|------|
| id | 行程唯一ID |
| start_date | 开始时间(毫秒时间戳) |
| end_date | 结束时间(毫秒时间戳) |
| distance | 行驶距离(km) |
| duration_min | 行驶时长(分钟) |
| start_ideal_range_km | 出发时预估续航 |
| end_ideal_range_km | 到达时预估续航 |

## 许可证

MIT License

## 作者

OpenClaw（小龙虾）
