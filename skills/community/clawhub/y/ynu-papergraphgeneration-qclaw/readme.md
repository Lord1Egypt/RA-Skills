# 论文架构图生成器 (Paper Diagram Generator)

## 📌 简介
本技能专为科研人员设计。它通过 OpenClaw 解析学术论文的核心框架或摘要文本，自动提取逻辑结构与视觉实体，并将其转化为高质量的绘图提示词，最终调用图像大模型（如 Banana Pro / Zimage）生成符合顶会审美（CVPR/NeurIPS）的架构示意图。

## ⚙️ 工作流
1. **输入层**：接收用户自定义要求和论文文本。
2. **中控层**：OpenClaw 总结提取结构化逻辑，生成纯英文 Prompt。
3. **执行层**：调用文生图 API 渲染图片并返回。

## 🚀 使用方法
在 OpenClaw 中触发该技能，提供论文的摘要或核心 Methodology 段落，并指定想要的图片风格（如 Flat Design）。