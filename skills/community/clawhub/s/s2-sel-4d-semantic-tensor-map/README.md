# 🌍 S2 空间要素多维图层与语义张量图集 (S2-SEL)

> **让机器人的每一步移动，都有物理因果支撑。**
> 本项目是桃花源世界模型（S2-SWM）的核心组件，将室内平面图升格为具备“物理张量”与“时空记忆”的 4D 导航底座。

## 🚀 核心突破
* **人机双读架构**：基于标准 GeoJSON 扩展，设计师可渲染图形，机器人可读取张量。
* **L3 语义图谱**：内置 20 种高频材质（玻璃、地毯、大理石等）的物理权重，自动接管传感器决策流。
* **4D Chronos 融合**：引入 `chronos_stamp`，支持 60 秒逆向持存法则，让空间状态具备历史因果性。

## 📁 目录结构
* `docs/`: 包含 4D 时空切片核心白皮书。
* `data/`: 20 种室内物理材质张量库。
* `core/`: 机器人导航张量解析引擎。
* `examples/`: L0-L4 结构化 GeoJSON 示例。

## 🛠️ 快速集成
具身机器人可通过 `S2GeoJSONParser` 直接从地图中提取物理干预指令：
```python
from core.s2_geojson_parser import S2GeoJSONParser
parser = S2GeoJSONParser('data/s2_material_tensor_library.json')
directives = parser.parse_layer_to_costmap('examples/sample_room_layers.json', '2026-04-07T15:02:18Z')

⚖️ 法律声明

本软件受 S2-CLA (S2-SWM 空间操作系统定制开源许可协议) 保护。严禁软件平台商进行二次打包倒卖或捆绑牟利。