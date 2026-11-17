---
name: visual-interactive-courseware
slug: visual-interactive-courseware
title: 可视化交互课件
displayName: 可视化交互课件
summary: 把教材知识点做成单文件 HTML 可视化交互课件——应用级外壳 + 电影感质感 + 滑块实时仿真，覆盖生物/历史/地理/物理等多学科，含自动审核脚本与教师说明。
description: 可视化交互课件制作技能。当用户需要为课堂教学制作可视化、可交互的课件（HTML 单文件）时使用。触发场景：把教材知识点（如血液循环、四羊方尊、晨昏线、二分二至等）做成 SVG 演示 + 可交互的网页课件、知识卡和教师说明。适用学科：生物、历史、地理、物理、化学、数学等一切含结构、流程、现象的知识点。
version: 1.1.0
tags: ["education", "courseware", "svg", "interactive", "teaching", "physics", "biology"]
license: MIT
metadata: {"clawdbot":{"emoji":"🎓","os":["linux","darwin","win32"]}}
agent_created: true
---

# 可视化交互课件 (Visual Interactive Courseware)

## 概述

将教材知识点转化为**专业软件级**的可视化交互课件——对标三张品质标杆：医学解剖软件级应用外壳与图层化结构（Visible Body 类）、电影感 3D 地形叙事（历史地理动画）、暗色科技风爆炸图+步骤标注流（原理拆解视频）。产出物：

1. **交互课件** `课件.html` — 单文件 HTML：应用级四区外壳（左导航/顶栏模式切换/右知识大纲树/底部控制条）+ 深空主题 + SVG 渐变辉光质感 + 步骤序列器
2. **知识整合文档** `01-知识整合.md` — 权威检索来源 + 配图需求分析
3. **教师说明** `教师说明.md` — 教学目标、分幕操作指引、课堂建议
4. **3D 增强资产（可选）** — Blender 建模 + three.js 内嵌（方案 A）：GLB 交互模型幕、仿真视频、高质量渲染静帧，与 SVG 幕共享同一套外壳与交互引擎，管线详见 `references/3d-blender-pipeline.md`。模型与视频体积宽松（总体几十 MB 内均可），但必须落实大体积离线体验保障（加载遮罩/懒挂载/按需渲染）。

核心理念：**应用级外壳（不是网页幻灯片）、电影感质感（渐变+辉光+运镜，拒绝平面色块卡通风）、结构类解剖（真实形态轮廓，拒绝爱心形）、过程有序列器（①-⑥步骤聚光标注流）**。

**主题路线**：生物/人体/解剖类用**浅色医学插图主题**（淡青底 + 白胶囊标注 + 引线 + 分段时间轴，对标"生命寻动"）；物理/天文/科技类用**深色电影感主题**。两套主题的应用外壳结构一致。

⚠️ **写实度红线——人体/复杂结构必须 AI 底图 + 交互叠加**：
手写 SVG 路径画人体/复杂器官存在天花板，产出必然"示意图感"。正确工作流：
1. **ImageGen 生成写实底图**：提示词对标 Netter/Visible Body 医学插画风格（如"Medical textbook quality anatomical illustration... no text, no labels, no watermark"，1024x1536 high）；可用图生图二次编辑局部（如颅骨换成脑）
2. **PIL 后处理**：AI 生成图右下角水印用**镜像补丁法**去除（同行左侧像素镜像填充 + GaussianBlur 融合接缝）——ImageGen 自身去水印不彻底；缩至 900px 宽 JPEG → base64 内嵌 `<image>`
3. **SVG 三层叠加**：底图（`mix-blend-mode:multiply` + radial-gradient mask 边缘羽化消除矩形色差）→ 血流/流程叠加层（半透明 dash 光带，drop-shadow 辉光）→ 透明热点（ellipse/path 覆盖器官，hover 描边）
4. **图层语义重定义**：MODE_MAP 不再控制器官显隐，改为控制叠加层 `flows[]` + `flowOp`（透明度）+ `focus`（聚焦目标）；聚焦模式底图调暗（0.55-0.68）让光带当主角 + `tweenViewBox` easeInOutQuad 镜头推近
5. **叠加层仿射映射**：底图重定位后，叠加层用 `transform="translate(dx,dy) scale(s)"` 对齐底图血管位置
参照成品：`D:\vibe coding\课件-血液循环示例\课件.html`（写实底图版）。

⚠️ **品质基准文件**：`D:\vibe coding\课件-血液循环示例\课件.html`（已实测达标杆水准的完整样板，写实底图 + 交互叠加架构）。制作任何新课件前，先读此文件对齐质感与结构；达不到它的水准不得交付。

## 触发条件

用户提出以下任一请求时使用本 skill：
- "把这个知识点做成课件/交互课件/可视化课件"
- "帮我做一节课的演示，要有动画/交互"
- "做 3D 课件 / 虚拟仿真课件 / 用 Blender 配合做课件 / three.js 模型进课件"
- 提及具体知识点：血液循环、四羊方尊、晨昏线、凸透镜成像、有丝分裂、电路……并要求可视化
- "参考图 + 知识拆解 + 课件"的资源整合类教学任务

## 第零步前置：定位学段 × 学科

**必做**：从用户请求中判断（或直接询问）目标学段（小学/初中/高中/中高职/高校）与学科，然后读取 `references/audience-matrix.md` 按矩阵微调五要素：知识深度、视觉写实度、交互复杂度、语言风格、容量时长。质量红线全学段一致。

## 第零·五步：3D 通道决策（必做询问，不得跳过）

知识整合完成后、动手写课件前，**必须向用户提示 3D 增强选项**（用 AskUserQuestion 或等价提问）：

> 本课件是否需要 3D 增强通道（方案 A：Blender 建模 + three.js 内嵌）？
> - **A. three.js 交互 3D 幕**：Blender 从零建模/素材库拉模型 → 导 GLB → base64 内嵌 → 单文件内 OrbitControls 旋转/缩放/点选，与 SVG 幕共用外壳。适合：解剖结构、机械装置、分子构型、地形地貌等"需要绕看"的知识。
> - **B. 仿真视频/渲染静帧**：Blender 动画 → PNG 序列 → ffmpeg 合成 mp4 → base64 内嵌，或高质量渲染静帧内嵌。适合：动态过程（电流流动、天体运动、流体）作为实景素材。
> - **A+B 组合**：既有可交互 3D 模型幕，又有仿真视频/静帧点缀。
> - **D. 纯 SVG**：默认路线，无需 Blender。

**前置安装（三项，用户想用增强 3D 时主动给出以下指引）**——增强 3D 依赖这套环境，三项配合效果最佳：
1. **Blender**：从 https://www.blender.org/download/ 下载安装（3.0+ 均可，5.x 已实测）。这是 3D 建模/动画/渲染的核心引擎，未安装时先请用户装好再继续。
2. **blender MCP 连接**：在 WorkBuddy 连接器中配置 Blender 官方 MCP（源码 https://projects.blender.org/lab/blender_mcp ，Blender 侧桥监听 localhost:9876），用于交互式建模与截图调优；不连 MCP 也能用无头 CLI 跑管线，但调优效率低。
3. **blender-studio 技能**：安装 https://github.com/arjun988/blender-skills （仓库含多个 Blender 技能，整合为单入口后位于 `~/.workbuddy/skills/blender-studio/`），内含建模/动画/渲染/导出全流程知识模块，与 visual-interactive-courseware 搭配使用。

**环境探测**（决策依据，向用户如实报告）：
1. Blender 可执行文件（常见路径 `D:\Program Files\Blender Foundation\Blender <ver>\blender.exe` 等，`--version` 探测）
2. blender MCP（`~/.workbuddy/mcp.json` 含 `"blender"` 键 → 已连接，可交互式建模）
3. blender-studio 技能（`~/.workbuddy/skills/blender-studio/` 存在 → 全流程建模知识库可加载）

判定规则：用户选 A/B/A+B 且三项就绪 → 按 `references/3d-blender-pipeline.md` 执行（无头 CLI 为主，MCP 交互调优为辅，建模知识查 blender-studio）；环境不全 → 列出缺失项与上面的安装指引，回落纯 SVG（D）或等用户装好再继续。**用户未明确选择时默认 D，不擅自启动 Blender。**

**体积基调**：3D 模型（GLB）与仿真视频**不必苛刻压缩——总体积几十 MB 以内均可接受**；但必须坚持单文件零外链，并落实大体积 HTML 的离线打开体验保障（loading 遮罩、视频 faststart、GLB 贴图适压、canvas 占位防白屏），具体清单见管线文档第六节。

**从零建模铁律**（用户指令，优先级最高）：当需要完整从零创建模型时，必须"**先设计 →（必要时搜图/AI 生成参考图）→ 高质量 .py 脚本（零件逐个建函数 → 组装）→ 交给 Blender 执行 → 渲染验证**"，逐环节确保质量，严禁跳过设计直接堆代码。详见管线文档第二节。

## 自动审核（交付前强制执行）

课件完成后运行：
```bash
python scripts/audit_courseware.py <课件.html> --report 审核报告.md
```
- 10 项静态审核（单文件/内嵌图/ID唯一/键盘/暂停/字号/无障碍…），P0 项一票否决
- **≥90 分才可交付**；不达标先按报告修复再交付
- 审核之外还须：浏览器逐幕截图（1600×900/1366×768/1024×768）+ 功能回归 **14 项**（暂停/速度/时间轴跳转/键盘翻页/点选联动/引线数/模式循环，**外加画布漫游 7 项**：滚轮缩放/拖动平移/双击复位/缩放边界/拖后不误触/知识点→镜头/环节→镜头；完整清单见 `references/design-guide.md`）
- **内容精准自检**：知识点逐条与教材核对（学段对应版本）；AI 生成图需检查解剖学/科学性错误（如心尖朝向、血管连接），有误则重新生成或换图

## 标准工作流（两步法）

> 详细执行规范见 `references/workflow.md`，视觉与交互规范见 `references/design-guide.md`，
> 学段×学科适配见 `references/audience-matrix.md`，
> 各学科拆解模式见 `references/subject-examples.md`，HTML 骨架见 `assets/template.html`。

### 第零步：项目初始化

在当前工作区创建项目文件夹，命名格式 `课件-<知识点名称>/`：

```
课件-血液循环/
├── 01-知识整合.md      ← 第一步产物
├── 参考图/             ← SVG/参考素材存放处
│   ├── 血液循环总览.svg
│   ├── 肺循环.svg
│   └── 体循环.svg
├── 课件.html           ← 第二步产物（核心交付）
└── 教师说明.md         ← 第二步产物
```

### 第一步：知识整合（有据可查，拒绝胡编）

1. **检索知识点**：通过 WebSearch/WebFetch 从教材官方来源（人教版电子教材、教育部课程资源、学科专业网站如中国植物志、国家地理、博物馆官网）总结归纳教材内容。**禁止凭空编造教材数据**——数值、名称、结论必须有检索来源。
2. **写入 `01-知识整合.md`**，结构固定为：
   - 教材定位（学段/年级/册/章节）
   - 知识点清单（每条注明来源）
   - 核心关系/过程（这是 SVG 化的对象，用文字+箭头先描述清楚）
   - 易错点与常见考点
   - **配图需求分析**：每个知识点需要什么图？静态结构图 / 动态过程图 / 对比图 / 数据图表？
3. **生成 SVG 参考图**：按配图需求逐一绘制 SVG，存入 `参考图/`。SVG 必须是自包含的、可独立打开验证的文件。

### 第二步：课件生成（拆解 + SVG 化 + 交互 + 可选 3D 增强）

1. **拆解知识模块**：把知识点拆为 4–8 个模块，每模块对应课件的一个"幕"（一屏一焦点）。拆解原则见 `references/workflow.md` 的模块拆解表。
2. **核心关系 SVG 化**：把知识整合文档中的"核心关系/过程"转为可交互 SVG：
   - 流程类（血液循环、水循环）→ 循环路径动画，可分层切换（如肺循环/体循环分看）
   - 结构类（四羊方尊、细胞结构）→ 分层展开/剖切视图，部件可点选高亮
   - 现象类（晨昏线、二分二至）→ 参数滑块驱动（拖动日期看太阳直射点）
   - 几何类（凸透镜成像）→ 拖动物体观察像的变化
3. **3D 增强（若第零·五步选定 A/B）**：按 `references/3d-blender-pipeline.md` 在恰当模块插入 three.js 交互 3D 幕 / 内嵌仿真视频 / 渲染静帧——3D 幕与 SVG 幕共用四区外壳、幕切换引擎、知识大纲联动与底部控制条，做到"无缝一体"。
4. **生成交互课件**：复制 `assets/template.html` 为骨架，填充模块内容。单文件自包含（无外部依赖），可在教室浏览器直接打开。
5. **生成知识卡**：每模块 3–5 条要点，作为课件的"要点速览"面板。
6. **生成教师说明.md**：教学目标、每幕操作指引、课堂互动建议、预设提问。

### 交付验收

- 用浏览器打开 `课件.html` 验证：每个交互控件都可用、SVG 无错位、无控制台报错
- 调用 present_files 展示课件 HTML 给用户
- 询问是否需要调整交互粒度、视觉风格或补充模块

## 交互设计红线

- 单文件、零外部依赖（离线教室可用）
- **每个 `<svg>` 自带 `<defs>`，渐变/滤镜 ID 全文档唯一**（加幕号后缀）。Chromium/Edge 下跨 SVG 引用 `display:none` 内的 `url(#id)` 会渲染失败、路径凭空消失；重复 ID 只认第一个同样会炸——已实测踩坑，验收时必须跨幕切换检查
- **白胶囊标注必须配引线**：JS 动态生成 SVG 折线（胶囊边缘 → 水平拐点 → 器官点 + 端点圆），随标注显隐同步重绘，resize 重算（实现见基准文件 `drawAnnoLines()`）
- 每个动画必须可暂停/可重放；播放暂停需同时作用于 dash 流动、beat 脉动、步骤序列器
- 步骤序列器：自动步进 + 点击跳步 + SVG 路径聚光联动（当前步加粗辉光、其余暗化）
- 所有文字 ≥ 13px（1200 viewBox），SVG 关键标注加强调色
- 中文界面，术语与教材表述一致
- 不使用需联网的 CDN 字体/图标库
- **交付前必须用浏览器自动化逐幕截图验收**（1600×900 / 1366×768 / 1024×768 三种视口），肉眼确认渲染无误；功能测试至少覆盖：暂停、速度切换、时间轴跳转、键盘翻页、点选联动、标注引线数量、**画布漫游（滚轮缩放/拖动平移/双击复位/镜头联动）**

## Resources

### references/
- `workflow.md` — 两步工作流详细执行规范、模块拆解表、SVG 类型决策树
- `design-guide.md` — 配色、字号、布局、交互控件规范
- `audience-matrix.md` — 学段×学科适配矩阵（小学→高校）与 AI 提示词模板
- `subject-examples.md` — 生物/历史/地理/物理等学科的拆解模式库
- `3d-blender-pipeline.md` — **3D 增强通道（方案 A）完整管线**：Blender 无头建模/动画/渲染 → GLB/mp4/JPEG base64 内嵌 → three.js 静态打包单文件方案（v1.2.2 起废弃 Blob URL 动态 import）；含从零建模铁律、Blender 5.2 兼容坑、质量红线与回归清单

### scripts/
- `audit_courseware.py` — 自动审核脚本（10 项检查，P0 一票否决，≥90 分可交付）
- `bundle_3d.py` — three.js 静态打包脚本：把 three.module.min.js + OrbitControls + BufferGeometryUtils + GLTFLoader 打成单 IIFE（`window.ThreeBundle`），运行时零 fetch——沙箱 iframe/file:// 会拦截 Blob URL 动态 import（报 Failed to fetch），3D 幕一律用本脚本构建期内联。用法 `python bundle_3d.py [工作目录]`，详见 `references/3d-blender-pipeline.md` §3.2

### assets/
- `template.html` — 单文件交互课件 HTML 骨架（含导航、SVG 容器、知识卡面板）
