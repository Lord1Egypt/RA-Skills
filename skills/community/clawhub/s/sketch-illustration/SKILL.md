---
name: sketch-illustration
description: 插画图片生成技能，支持多种手绘风格。适合流程图、功能说明、PPT配图、教程配图、知识图和手绘信息图等场景。支持五种风格：A) Sketch 极简手绘风（Notion/Linear 风格，简笔人物，冷淡低饱和）；B) Watercolor 奶油彩铅水彩风（暖色调，纸纹彩铅，适合PPT讲义）；C) Flat Vector Retro 扁平矢量复古风（黑色轮廓线，几何简化，复古配色，适合NotebookLM PPT/课程封面）；D) Doodle Infographic 白纸手绘知识图风（白纸背景、拟人角色、高信息密度、手账/课堂板书感，适合概念对比、方法论、拖延机制、知识卡片）；E) NotebookLM Tech 技术图解风（低饱和莫兰迪色系、扁平2.5D插画、模块化布局、中等信息密度，适合产品功能介绍、流程说明、概念图解）。生成后自动上传发送到飞书。当用户要求生成插画、配图、手绘风格图、流程示意图、产品插图、PPT配图、知识图、信息图、手绘知识海报时触发此技能。
---

# 插画生成 Skill

支持多种手绘插画 / 知识图风格,按需选择,使用任意可用图像模型生成并发送到飞书。

## 风格选择

查看 `references/styles.md` 了解五种风格的详细说明和使用场景：
- **风格 A：Sketch 极简手绘风**（默认）— Notion/Linear 风，极简冷淡，适合技术流程图
- **风格 B：Watercolor 奶油彩铅水彩风** — 暖色调纸纹，适合 PPT 配图、课程讲义
- **风格 C：Flat Vector Retro 扁平矢量复古风** — 黑色轮廓线+几何简化，适合 NotebookLM PPT、课程封面、复古感内容
- **风格 D：Doodle Infographic 白纸手绘知识图风** — 白纸背景、拟人角色、高信息密度、手账/课堂板书感，适合概念对比、方法论、知识海报、拖延机制图
- **风格 E：NotebookLM Tech 技术图解风** — 低饱和莫兰迪色系、扁平2.5D插画、模块化布局、中等信息密度，适合产品功能介绍、流程说明、概念图解

用户未指定时默认用风格 A;如果用户明确喜欢"白纸手绘知识图 / 蜗牛 / 拟人大脑 / 手账板书感 / 信息很多但不乱"这类效果,优先用风格 D。

如果使用风格 D,再按图类型去读对应模板:
- **机制图**:`references/doodle-template-mechanism.md`
- **对比图**:`references/doodle-template-compare.md`
- **步骤流程图**:`references/doodle-template-flow.md`

## 执行流程

### 1. 确认内容与风格
- 明确要画什么内容、用什么风格
- 从 `references/styles.md` 取对应风格块
- 风格 B 的布局模板在 `references/image-assistant-templates/`
- 风格 D(手绘知识图)优先确认:
  - 是**单张知识海报**还是**对比图 / 流程图 / 多模块信息图**
  - 是否需要**拟人角色**(如蜗牛、脑子、小龙虾)
  - 是否需要**高信息密度但少长段文字**

### 2. 构建 Prompt

基础结构:
```
[风格块(从 styles.md 复制)]

顶部居中标题:'[中文标题]'

[内容描述:人物、场景、元素、布局]

[负面约束]
```

详细提示词模板见 `references/prompt-guide.md`。

如果是风格 D,不要只写"画个XX知识图",要先明确图类型:
- **机制图**:读 `references/doodle-template-mechanism.md`
- **对比图**:读 `references/doodle-template-compare.md`
- **步骤流程图**:读 `references/doodle-template-flow.md`

优先直接复用对应模板里的 prompt 骨架,再替换成当前主题。

### 3. 生成图片

使用系统配置的图像生成模型生成图片。

```bash
# 通过系统工具或配置的图像生成服务生成
# 输出到 /root/myfiles/<filename>.png
```

### 4. 上传并发送到飞书

```bash
bash scripts/send_to_feishu.sh /root/myfiles/<filename>.png <open_id>
```

该脚本现在走**稳定发图链路**(飞书 `im/v1/images` -> `image_key` -> `msg_type=image`),不再依赖容易把本地路径发成文本的旧链路。

猫南北的 open_id:`ou_22f2eefd5abe63e0cd67f4882cec06d4`

## 注意事项

- 图片输出到 `/root/myfiles/`
- 所有文字标注默认中文
- 风格 B 的多张成套配图工作流见 `references/image-assistant-workflow.md`
- 风格 D 不要写成长段密集小字，优先用：标题、短句、箭头、卡片、小标签、拟人角色来承载信息
- 风格 D 的核心不是"神奇咒语"，而是：**主体 + 情绪/主题 + 隐喻物 + 白纸手绘版式 + 高信息密度 + 可爱角色** 的组合
- 风格 E（NotebookLM Tech）适合中等信息密度的技术说明，不要做成高密度信息图
