# TravelMaster V8 - 多MCP集成智能旅行规划系统

## 项目简介

TravelMaster V8 是一个集成多个MCP服务的智能旅行规划系统，支持：

- **FlyAI MCP** - 真实航班/火车票价查询（飞猪实时数据）
- **高德MCP** - 地图导航、POI搜索
- **腾讯MCP** - POI验证、路径对比
- **美团MCP** - 美食优惠套餐推荐
- **麦当劳MCP** - 快餐兜底方案

## 功能特性

| 功能 | 说明 |
|------|------|
| 真实票价查询 | FlyAI API调用飞猪实时数据 |
| POI验证 | 高德vs腾讯双源验证 |
| 路径规划对比 | 验证准确度 |
| 美食推荐 | 美团优先，麦当劳兜底 |
| 截图生成 | 地图+美食截图 |
| HTML攻略 | 可下载的完整攻略 |

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
npm install @fly-ai/flyai-cli
```

### 配置API密钥

创建 `.env` 文件：

```env
GAODE_API_KEY=your_gaode_key
TENCENT_MAP_KEY=your_tencent_key
FLYAI_API_KEY=your_flyai_key
MEITUAN_API_KEY=your_meituan_key
```

### 启动服务

```bash
python main_v8.py
```

访问：http://localhost:7860

## API接口

### 健康检查

```
GET /health
```

### 旅行规划

```
POST /api/travel
Body: {"message": "五一去香港，北京出发"}
```

### 方案选择

```
POST /api/select_plan
Body: {"plan": "A"}
```

## 项目结构

```
travel-swarm-v8/
├── README.md                  # 项目说明
├── LICENSE                    # MIT许可证
├── requirements.txt           # Python依赖
├── main_v8.py                 # 启动入口
├── backend/
│   ├── agents/
│   │   └── travel_swarm_engine_v8.py
│   └── utils/
│       ├── flyai_client.py
│       └── multi_mcp_client.py
├── frontend/
│   └── index_v7_fusion.html
├── docs/
│   └── TUTORIAL.md
└── tests/
    └── test_api.py
```

## 使用示例

```python
from backend.agents.travel_swarm_engine_v8 import TravelSwarmEngineV8

engine = TravelSwarmEngineV8()
plan = engine.plan_travel(
    destination='香港',
    departure='北京',
    date='2026-05-01',
    people={'adult': 2, 'child': 1},
    budget=15000,
    days=5
)

html = engine.generate_html(plan)
```

## 技术栈

- **Python 3.8+**
- **Flask** - Web框架
- **FlyAI CLI** - 票价查询
- **高德地图API**
- **腾讯地图API**

## 版本历史

| 版本 | 功能 |
|------|------|
| V7 | FlyAI真实票价集成 |
| V8 | 多MCP集成（高德+腾讯+美团+麦当劳） |

## 许可证

MIT License

## 作者

海狸 🦫 | 靠得住、能干事、在状态

## 贡献

欢迎提交Issue和Pull Request！

## 致谢

- FlyAI MCP
- 高德地图
- 腾讯地图
- 飞猪平台