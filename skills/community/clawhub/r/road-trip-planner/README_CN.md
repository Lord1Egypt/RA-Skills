# Road Trip Planner（自驾游路线规划）

> 仅限中国大陆 — 需高德 API Key  
> 依赖: [@lbs-amap/personal-map](https://clawhub.ai/lbs-amap/personal-map)  
> [English Version](README.md)

基于高德地图 personal-map skill 的多日自驾游路线规划工具。

## 功能

- 设计合理的多日自驾行程，控制每日驾驶时间（建议 4-6 小时）
- 自动调用高德 Web 服务 API 进行地理编码、POI 搜索和驾车路径规划
- 生成可在高德地图 App 中打开的个人地图小程序二维码
- 输出 Markdown 格式的每日行程指南
- 支持闭合环线设计，自动处理跨天里程补全

## 使用场景

当用户提到以下任意话题时，本 skill 会自动触发：
- 规划自驾游路线 / 公路旅行 / 环线
- 设计旅游行程（涉及多地驾驶）
- 生成个人地图 / 旅游地图 / 路线二维码
- 控制每日驾驶时间 / 避免疲劳驾驶
- 查询沿途里程、加油站、医院等补给点

## 安装

```bash
openclaw skills install personal-map
```

## 前置依赖

- [@lbs-amap/personal-map](https://clawhub.ai/lbs-amap/personal-map) skill（[GitHub](https://github.com/amap-demo/amap-sdk-skills) — 高德地图 API 封装）
- 高德开放平台 Web 服务 API Key（需配置环境变量 `AMAP_API_KEY`）

## 核心原则

1. **不疲劳驾驶**：每日实际驾驶时间控制在 6 小时以内，理想状态 4-5 小时
2. **连续路线**：所有天的节点合并为一条连续路线
3. **闭合环线**：如果起点和终点是同一城市，确保终点节点在去重后仍然保留
4. **每日弹性**：行程中保留机动空间，避免把时间排得太满

## 文件结构

```
road-trip-planner/
├── SKILL.md         # 主指导文档
├── references/      # 按需加载的参考资料
├── examples.md      # 示例（蒙东、青甘、川西）
├── README.md        # 英文说明
├── README_CN.md     # 本文件（中文说明）
├── CLAUDE.md        # 开发者参考
├── LICENSE          # MIT 许可证
└── .gitignore
```

## 示例

详见 [examples.md](examples.md)，包含以下案例：
- 蒙东呼伦贝尔 8 日环线
- 青甘大环线 9 日自驾
- 川西小环线 5 日自驾

## License

MIT
