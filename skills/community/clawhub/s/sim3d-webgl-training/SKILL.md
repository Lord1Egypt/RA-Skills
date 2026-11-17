---
name: sim3d-webgl-training
slug: sim3d-webgl-training
title: 3D虚拟仿真实训系统
displayName: 3D虚拟仿真实训系统生成器
summary: 零依赖单文件 WebGL2 + 原生 JS 的 3D 虚拟仿真实训系统生成技能——双画布架构、法线矩阵重归一化 PBR 着色器、6 类程序化 CAD 曲面、四维教学闭环（结构拆解/原理仿真/SOP 工卡/故障排故考核），零外部依赖离线可用，弱模型可复制的低自由度工程骨架。
description: 3D虚拟仿真实训系统制作技能。当用户需要为职业教育/职业培训制作 3D 虚拟仿真实训页面（单文件 HTML）时使用。触发场景：内燃机/无人机/新能源汽车/民航机务/安检/客舱乘务/空港管理等设备或岗位的"3D 结构拆解、原理仿真、实操培训、考核系统"。产出对标已验证的 9 个高逼真样本（特斯拉 Model Y、四冲程内燃机、A320/B747 客舱、大疆无人机、民航安检/机务/空港）。
version: 2.0.0
tags: ["webgl", "3d", "virtual-simulation", "training", "education", "pbr", "vocational"]
license: MIT
metadata: {"clawdbot":{"emoji":"🏭","os":["linux","darwin","win32"]}}
agent_created: true
---

# 3D 虚拟仿真实训系统 (Sim3D WebGL Training)

## 概述

生成**零外部依赖、单文件 HTML**的 3D 高仿真虚拟仿真实训系统。底层 `<canvas id="gl-canvas">` 跑原生 WebGL2 硬件加速 PBR 渲染，顶层透明 `<canvas id="hud-canvas">`（或 overlay-canvas）画 2D 矢量引线标注与虚拟仪器，配合 Web Audio API 合成音效。**严禁引用 three.js / OrbitControls 等任何外部 CDN**——离线教室必须可用。

核心能力全部来自 `references/` 内**可直接复制粘贴**的工程骨架（零推导），专治弱模型三大死穴：
1. 引 CDN 断网白屏 → 本 skill 全程序化，零依赖
2. 只会拼"积木方盒 Minecraft 感" → 6 类程序化 CAD 曲面 + 3D 关节技师人物
3. 做成"只能旋转看的 3D 玩具" → 四维教学闭环状态机（强制 SOP 工卡校验 + 防呆报警 + 虚拟仪表 + 评分）

## 触发条件

- "做一个 XX 设备/工种的 3D 虚拟仿真实训系统/实训平台/培训系统"
- "把 XX（内燃机、无人机、安检流程、新能源车维修…）做成可交互 3D 教学页面"
- "WebGL 3D 结构拆解 / 原理仿真 / SOP 实操 / 排故考核"

## 交付品质基准

以下 9 个已验证的高逼真成品样本即为交付底线（内燃机/新能源车/民航客舱/无人机/安检/机务/空港等领域的单文件 HTML 实训系统，含双画布架构、PBR 渲染、四维教学闭环），新项目达不到其水准不得交付：
- 内燃机 ICE-3D（粒子燃烧 + P-V 图 + 配气相位盘）
- 特斯拉 Model Y（3D 技师 + 万用表 + 评分 + 故障注入）
- 空客 A320 / 波音 747（客舱漫游 + 热点知识库 + 应急演练）
- 大疆无人机 ×2、民航安检、机务维修、空港管理

## 标准工作流（七步法）

### 第 0 步：需求定义（必须先明确，缺则追问）

| 必须确定项 | 说明 |
|---|---|
| **实训对象** | 设备（内燃机/无人机…）或 场景工种（安检/空港…） |
| **教学闭环形态** | 原理仿真型（内燃机式：参数+图表驱动）或 SOP 实操型（Model Y 式：模块+工卡+考核）或 混合型 |
| **核心部件清单** | 8–15 个主要部件/工位，每个需名称+材质+功能描述 |
| **动态过程** | 什么在动？（曲轴旋转/皮带输送/人物走动/粒子流动） |
| **SOP 步骤** | 实操型必须有：标准作业流程步骤 + 每步完成判据 |
| **考核规则** | 扣分点、一票否决项（安全红线） |

### 第 0.5 步：领域数据准备（内容密度之源，缺资料必做）

**这是"惊艳度"的决定性步骤**——用户感知的"精致/完善"90% 来自领域数据密度，而非渲染技术。当用户未提供设备资料时，**必须先用 WebSearch 检索真实工程参数**，再动笔写代码。

| 数据项 | 数量基线 | 来源 |
|---|---|---|
| 设备真实型号谱系 | 1 个基准变体（如 IRB 6700-235/2.85） | WebSearch |
| 每部件工程规格表 | ≥4 行真实数值（转矩/速比/精度/电压/行程…） | WebSearch + 推理 |
| 每部件**可测数值** testPoints | 8 值：vNorm/vFault/ohmNorm/ohmFault/mohmNorm/mohmFault/ampNorm/ampFault | 按电气量级推理 |
| 引用标准 | ≥2 个（GB/T、ISO、IEC 真实标准号） | WebSearch |
| 典型工况 | 3–4 种（如机械臂：焊接/码垛/零点/过载 STO） | 领域常识 |
| 关节/运动限位 | 真实行程范围 | WebSearch |

**数据契约模板与范例见 `references/domain-data.md`**（含 IRB 6700 全量范例，可直接照抄结构换内容）。

### 第 1 步：场景数据建模（数据驱动架构，内容与代码分离）

**采用 SIM_CONFIG 声明式单源数据架构**（对标 irb_6700 高分结构）：全部领域数据集中在一个配置对象，渲染/教学/仪器全部由数据驱动，改内容不动代码。

1. 建立 `SIM_CONFIG.components[]`：每项含 `id / code / shortName / name / category / color / pos / explodeVec / leaderOffset / principle(原理段) / specs(≥4行) / testPoints(8值)`（契约见 domain-data.md §1）。
2. 场景型（安检/空港）改用工位数据库：`pos / camTarget / camPos / sopSteps[] / warning / actionBtn`（参照 A320 HOTSPOTS_DATA）。
3. 建立 `SIM_CONFIG.sopSteps[]`：每步含 `title / desc / actionLabel / reqPpe / reqPowerOff / score / targetComp / techPos`。
4. 建立 `SIM_CONFIG.faults[]`：每故障含 `code / name / symptom / targetComp / hint(表笔+档位引导) / quizQuestion / options(3) / answerIdx`。
5. 相机预设 `SIM_CONFIG.cameraPresets[]`：≥4 个机位（全景/局部特写×2/俯视），含 `yaw/pitch/dist/look`。
6. 关节/运动限位表（机械臂类）：`limits = [[min,max,label]×6]`。

### 第 2 步：引擎搭建（直接复制 references 代码）

按顺序组装单文件 HTML，各段代码从对应参考文档**原样复制后只改业务参数**：

| 段 | 内容 | 代码来源 |
|---|---|---|
| HTML+CSS | 双画布 + 三栏式工作台 UI | `references/core-engine.md` §1 |
| 数学库 | Mat4（multiply/perspective/lookAt/TRS/projectPoint） | `references/core-engine.md` §2 |
| 着色器 | PBR_VS / PBR_FS（**含法线矩阵重归一化**）/ 粒子着色器 | `references/core-engine.md` §3 |
| MeshBuilder | addCylinder/addTubeSection/addBox/addHelicalSpring/addExtrudedPolygon/appendBuilder/compile | `references/cad-library.md` §1 |
| 独立网格函数 | buildCylinderMesh(X/Y/Z轴)/buildSphereMesh/buildTubeMesh/buildChamferBox | `references/cad-library.md` §2 |
| 部件建模 | buildAllMeshes()——用 CAD 库拼装第 1 步的部件清单 | 业务代码，参照样本写法 |
| 3D 技师 | render3DTechnician()（关节人物+PPE 装备） | `references/cad-library.md` §3 |
| 场景组装 | 相机/地面/车间设备（举升机/传送带/值机岛） | `references/rendering-rules.md` §1 |
| 双通道渲染 | Pass1 不透明 → Pass2 半透明（depthMask 开关） | `references/rendering-rules.md` §2 |
| 2D 叠加 | 引线标注布局算法 + 热点拾取 | `references/rendering-rules.md` §3 |
| 交互 | 拖拽/平移/缩放/点击拾取（5px 位移阈值） | `references/rendering-rules.md` §4 |
| 教学闭环 | SimState 状态机 + SOP 校验 + 评分 + 日志 | `references/teaching-modes.md` |
| **领域数据** | **SIM_CONFIG 全量数据（部件/specs/testPoints/SOP/故障/工况/相机）** | **`references/domain-data.md`** |
| **虚拟仪器** | **万用表4模式(V/Ω/MΩ/A)+表笔选择 / 双通道示波器 / 五维能力雷达** | **`references/teaching-modes.md` §仪器矩阵（P1必需）** |
| **遥测条** | **底部 4–6 项实时指标（坐标/电流/电压/误差…），随故障变色** | **`references/teaching-modes.md` §遥测条** |
| **工况控制台** | 3–4 种典型工况切换 + 关节点动滑块（真实限位） | `references/domain-data.md` §工况库 |
| 主循环 | DOMContentLoaded 初始化 + requestAnimationFrame | `references/core-engine.md` §4 |

**生成方式（防截断铁律）**：总代码量预计超 1500 行时，**必须用 Python 脚本分模块拼接生成**（每段为独立字符串变量，最后 write 单文件），禁止一次性直接输出全文——弱模型单次输出 3000+ 行必然截断残缺。

### 第 3 步：无头验证（交付前强制）

1. 浏览器打开，Console 必须 **0 个 SEVERE/ERROR**（着色器编译失败、undefined 变量都不允许）。
2. 多视角截图确认：默认视角 + 至少 2 个相机预设位 + 爆炸视图（如有）。
3. 交互回归：拖拽旋转不误触选件、滚轮缩放、点击部件弹出详情、SOP 步骤可完成、评分联动。
4. 静态审核：`python scripts/audit_sim3d.py <成品.html>` 三档判定——**≥85 优（直接交付）/ 80-84 良（补齐失败 P1 项后交付）/ <80 不可交付**。

### 第 4 步：迭代补丁

交付后用户反馈"逼真度不够"时，按此优先级打补丁（每补丁独立可回滚）：
1. **几何细节**：给大块面部件加倒角/分缝线/散热孔阵列（addExtrudedPolygon + 循环 addBox）
2. **材质微调**：metallic/roughness 分层（金属亮面 0.9/0.15、喷塑哑光 0.5/0.5、橡胶 0.1/0.85）
3. **动态增强**：加粒子流（烟/气流/冷却液）、状态灯闪烁、人物走动
4. **音效**：Web Audio 合成（参照 core-engine.md §5）

## 内容密度红线（一票否决，audit 自动检测）

技术引擎达标≠可交付。以下内容基线全部满足才允许交付（不足则回第 0.5 步补数据）：

| 基线项 | 最低值 | audit 检测项 |
|---|---|---|
| 部件总数 | ≥8 | `SIM_CONFIG.components` 或等效 |
| 每部件规格表 | ≥4 行真实数值 | `specs:` 数组 |
| 可测数值体系 | ≥1 组 `testPoints`（含 Norm+Fault 双值） | `vNorm.*vFault` 或 `ohmNorm.*ohmFault` |
| SOP 工卡 | ≥5 步，含联锁要求与分值 | `sopSteps`/`reqPpe`/`score` |
| 故障库 | ≥4 个，含选择题（≥2 选项） | `quizQuestion`/`answerIdx` |
| 虚拟万用表 | ≥3 档位 + 表笔选择 | `data-dmm`/`sel-probe` |
| 遥测条 | ≥3 项实时指标 | `tele-` id |
| 工况模式 | ≥2 种可切换 | 工况按钮组 |
| 标准引用 | ≥1 个真实标准号 | `GB/T`/`ISO`/`IEC` |
| 关节限位（机械臂） | 6 轴真实行程 | `limits` 表 |

## 架构红线（一票否决）

- **零外部依赖**：无任何 `<script src>`/`<link href>` 指向网络；WebGL2 不可用时降级 WebGL1 兜底或给出友好提示
- **双画布**：3D 渲染与 2D 标注/仪表分层，overlay 层 `pointer-events:none`（拾取穿透到 gl 层统一处理）
- **双通道渲染**：不透明件 Pass1（depthMask(true)）→ 半透明外壳/粒子 Pass2（depthMask(false) + blend）；流线型外壳必须是**中空侧板/剖面结构**，严禁实心壳挡死内部
- **视口变量命名 `viewW`/`viewH`**：严禁用 `h`/`w` 等易遮蔽名（防 `for (const h of hotspots)` 覆盖）
- **拖拽与点击解耦**：mouseup 时位移 `< 5px` 才触发拾取
- **人物防穿模**：技师朝向 `Math.atan2(dx, dz)`；工位坐标一律设在设备包围盒**外侧**
- **中文学术语言**：术语用行业标准表述（对标国标/民航 CAAC/特斯拉 SOP 等真实规范）

## Resources

### references/（按需加载，均含可直接复制的完整代码）
- `domain-data.md` — **领域数据建模规范**：SIM_CONFIG 数据契约全量模板 + IRB 6700 真实数据范例 + testPoints 测量体系设计 + 工况库 + 标准引用规范（**写代码前先读这篇**）
- `core-engine.md` — 双画布 HTML 骨架、Mat4 数学库、法线矩阵重归一化 PBR 着色器、主循环、Web Audio 音效
- `cad-library.md` — MeshBuilder 类 + 6 类程序化曲面生成器 + 3D 关节技师人物（含 PPE 装备）
- `rendering-rules.md` — 双通道渲染、粒子系统、2D 引线标注、爆炸视图、相机预设、拾取交互、质感细节清单
- `teaching-modes.md` — 四维教学闭环状态机、SOP 工卡、考核评分、故障注入、**虚拟仪器矩阵（万用表4模式/示波器/能力雷达）与遥测条（P1 必需）**
- `gotchas.md` — 弱模型防呆机制完整清单（写代码前通读一遍）

### scripts/
- `audit_sim3d.py` — 静态审核脚本（引擎必需项/防呆项/交互项 + 内容密度基线项，P0 一票否决；≥85 优 / 80-84 良 / <80 不可交付；已用 9 个基准样本校准）

## 输出约定

- 项目目录：`实训-<对象名称>/成品.html`（或用户指定路径）
- 文件命名含业务关键词，如 `特斯拉 Model Y 3D高仿真虚拟实训与考核系统.html`
- 交付时 present_files + 简述四大模块与亮点
