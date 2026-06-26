---
invocation_mode: both
preferred_provider: minimax
name: skill_cad_generator
alias: CAD生成器技能
description: |
  豆豆CAD/3D能力提升方案的核心技能。
  接收用户描述，生成JSON参数定义文件，通过FRP隧道发送到M4 Pro执行重计算和渲染。
  支持郁金香花瓣等参数化模型生成。
metadata:
  author: 豆豆
  version: "1.0"
  tags: cad, 3d, threejs, blender, parametric, m4pro
  updated: 2026-04-01
---
invocation_mode: both
preferred_provider: minimax

# CAD生成器技能 v1.0

## 功能概述
豆豆作为参数定义引擎，M4 Pro作为图形工作站的协同架构：
- **豆豆职责**：理解用户需求 → 生成JSON参数定义 → 推送到M4 Pro
- **M4 Pro职责**：接收参数 → Three.js渲染 → 生成OBJ/CAD文件 + 预览图

## 通信协议
### JSON参数格式
```json
{
  "model_type": "tulip_petal",
  "params": {
    "radius": 45,
    "curvature": 0.75,
    "twist": 35,
    "length": 120,
    "segments": 32,
    "material": "acrylic",
    "color": "#FF69B4"
  },
  "output": {
    "format": "obj",
    "preview": "png"
  }
}
```

### M4 Pro服务端点
- **地址**: http://localhost:3006/generate (通过FRP隧道6003端口访问)
- **方法**: POST
- **认证**: 无（内网安全）

## 使用方法
### 生成郁金香花瓣
```javascript
// 输入：用户描述文本
// 输出：3D模型文件 + 预览图
const result = await skill_cad_generator.generateTulipPetal(userDescription);
```

### 参数提取
```javascript
// 输入：自然语言描述
// 输出：结构化参数对象
const params = await skill_cad_generator.extractParams(description);
```

## 依赖项
- FRP隧道 (6003端口 → M4 Pro:3006)
- M4 Pro Three.js引擎 (~/DouCAD/engine/)
- HTTP客户端库

## 安全性说明
- **参数验证**：所有数值参数都有合理范围限制
- **模型类型白名单**：只允许预定义的模型类型
- **输出格式限制**：仅支持obj/png格式
- **网络隔离**：仅通过FRP隧道与M4 Pro通信

## HTML页面集成
- 集成在设计部工作台 (design.html)
- 灯光/音响/视频部门的CAD生成功能
- AI助手对话中可直接调用