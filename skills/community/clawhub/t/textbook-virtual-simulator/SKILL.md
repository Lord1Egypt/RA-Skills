---
name: textbook-virtual-simulator
description: >
  教材虚拟仿真系统生成器，支持多种教材格式（文本/PDF/JSON）转换为交互式教育仿真 Web 应用。
  能够生成3D场景、交互式组件、数据分析功能，适用于教育实验、操作培训、知识图谱等多种仿真类型。
  当用户提出以下意图时触发：创建教材仿真、生成虚拟实验、构建教学模拟、制作教育3D场景、
  教材可视化、交互式教学应用、仿真教学系统等。
version: 1.0.0
agent_created: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🎓"
    homepage: https://github.com/your-username/textbook-virtual-simulator
---

# 教材虚拟仿真系统生成器

本技能提供完整的教材到虚拟仿真 Web 应用的转换能力。通过解析多种格式的教材内容，生成包含3D场景、交互式组件和数据分析功能的完整 Web 应用。

## 核心能力

| 能力 | 说明 |
|------|------|
| 多格式解析 | 支持文本、PDF、JSON 等教材格式 |
| 仿真类型 | 教育实验、操作培训、知识图谱等多种类型 |
| 3D 场景生成 | 基于教材内容自动生成 3D 交互场景 |
| 交互组件 | 创建测验、进度追踪、控制面板等组件 |
| 数据分析 | 支持学习进度、操作数据分析 |
| Web 应用输出 | 生成完整的可部署 Web 应用 |

## 工作流程

### 第一阶段：教材解析与需求确认

1. **识别教材格式** - 检测用户提供的教材文件类型
2. **解析教材内容** - 使用 `scripts/parse_materials.py` 提取关键信息
3. **确认仿真类型** - 根据内容特征推荐合适的仿真类型
4. **收集需求细节** - 确认具体的功能要求和交互设计

### 第二阶段：场景与组件设计

1. **选择仿真类型** - 参考 `@references/simulation_types.md` 选择最合适的类型
2. **设计3D场景** - 基于教材内容设计场景布局和交互逻辑
3. **选择3D技术栈** - 参考 `@references/3d_technologies.md` 选择合适的技术
4. **规划交互组件** - 确定需要的交互组件类型和数量

### 第三阶段：代码生成与构建

1. **生成3D场景代码** - 使用 `scripts/scene_generator.py` 生成场景代码
2. **创建交互组件** - 使用 `scripts/interactive_builder.py` 构建组件
3. **实现数据分析** - 使用 `scripts/data_analyzer.py` 添加数据功能
4. **组装Web应用** - 使用 `scripts/generate_webapp.py` 生成完整应用

### 第四阶段：测试与交付

1. **验证应用功能** - 检查所有功能是否正常工作
2. **优化用户体验** - 调整交互细节和视觉效果
3. **打包部署文件** - 生成可直接部署的应用包
4. **提供使用文档** - 生成使用说明和部署指南

## 仿真类型指南

参考 `@references/simulation_types.md` 获取详细的仿真类型说明和实现指南。

### 支持的仿真类型

| 类型 | 适用场景 | 3D需求 | 交互复杂度 |
|------|---------|--------|-----------|
| 教育实验 | 化学实验、物理模拟 | 高 | 中等 |
| 操作培训 | 设备操作、流程演练 | 中等 | 高 |
| 知识图谱 | 概念关系、知识可视化 | 低 | 低 |
| 历史重现 | 历史场景、事件模拟 | 高 | 中等 |
| 地理探索 | 地形展示、地理教学 | 高 | 中等 |

## 3D 技术选型

参考 `@references/3d_technologies.md` 了解不同3D技术的优缺点和适用场景。

### 推荐技术栈

- **默认选择**: Three.js + 3D Loader
- **轻量级场景**: Babylon.js
- **移动端优化**: Cannon.js + Three.js
- **数据可视化**: Three.js + D3.js

## 关键规则

1. **格式检测优先** - 自动检测教材格式，优先使用专用解析器
2. **渐进式增强** - 基础功能优先，高级功能可选
3. **响应式设计** - 生成的应用必须支持多设备访问
4. **无外部依赖** - 生成的应用应尽量减少外部依赖
5. **性能优化** - 3D场景必须进行性能优化和LOD处理
6. **教育适用性** - 所有交互设计必须考虑教育场景特点

## 脚本使用说明

### parse_materials.py

解析不同格式的教材文件，提取结构化内容。

```bash
python3 scripts/parse_materials.py input_file --format auto|text|pdf|json --output content.json
```

### scene_generator.py

根据教材内容生成 3D 场景代码。

```bash
python3 scripts/scene_generator.py content.json --scene-type lab|classroom|outdoor --output scene.js
```

### interactive_builder.py

创建交互式组件。

```bash
python3 scripts/interactive_builder.py content.json --components quiz|progress|control --output components/
```

### data_analyzer.py

添加数据分析功能。

```bash
python3 scripts/data_analyzer.py content.json --metrics progress|accuracy|time --output analytics.js
```

### generate_webapp.py

生成完整的 Web 应用。

```bash
python3 scripts/generate_webapp.py content.json --template default --output dist/
```

## 参考资料

- `@references/simulation_types.md` - 仿真类型详细指南
- `@references/3d_technologies.md` - 3D技术选型和对比
- `@references/web_templates.md` - Web应用模板设计
- `@references/best_practices.md` - 教育仿真最佳实践

## 资产模板

技能包含多个预构建的模板，可直接使用或作为基础修改：

- `assets/web-template/` - Web应用基础模板
- `assets/3d-templates/` - 3D场景模板
- `assets/interactive-components/` - 交互组件模板

## 使用示例

### 示例1：化学实验仿真

用户需求：基于化学教材创建虚拟实验

1. 解析化学教材PDF
2. 选择"教育实验"仿真类型
3. 生成实验室3D场景
4. 添加交互式实验组件
5. 生成完整Web应用

### 示例2：设备操作培训

用户需求：为设备手册创建培训仿真

1. 解析设备操作手册
2. 选择"操作培训"仿真类型
3. 生成设备3D模型和场景
4. 添加步骤指导和错误检测
5. 生成培训Web应用

## 依赖

- Python 3.7+
- PyPDF2 (PDF解析)
- jsonschema (JSON验证)
- 可选：ImageMagick (图片处理)