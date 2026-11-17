---
name: vibe-interaction-spec
slug: vibe-interaction-spec
displayName: 动效规格 Vibe Interaction Spec
summary: 把「炫一点」「要高级感」「丝滑一点」这类模糊审美，翻译成带具体数值的动效规格：术语、token、参数、验收标准与 lint 检查。覆盖 CSS / GSAP / three.js / p5.js 四套技术栈与十种艺术方向。
version: 1.2.0
license: MIT
tags: [motion, animation, interaction, css, gsap, threejs, p5js, creative-coding, art-direction, design-system, frontend, ui-components]
description: 把「让页面炫一点」「要高级感」「丝滑一点」这类模糊审美表达，翻译成工业级的动效规格：术语、token、参数、验收标准与实现约束。覆盖三层——静态设计层（视觉层级、栅格、字体阶梯、色彩对比、格式塔、状态矩阵、艺术流派）、动效层（时序编排、缓动、弹簧物理、页面转场范式）、平台层（合成属性、性能预算、无障碍、CSS/WAAPI/View Transitions 选型）。同时覆盖四套实现栈：CSS 与 WAAPI、GSAP（时间线、ScrollTrigger、SplitText、Flip）、three.js（场景、光照、材质、性能预算）、p5.js（生成艺术、噪声流场、粒子、印刷导出）。当用户描述想要某种手感却说不出专业词时使用；当需要写 CSS 动画、Framer Motion、GSAP、滚动特效、hover 微交互、页面转场时使用；当想做 3D 产品展示、创意编程生成艺术、动态海报时使用；当需要选定艺术方向（瑞士、包豪斯、Art Deco、编辑排版、极简、孟菲斯、Y2K）时使用；当页面「不好看 / 廉价 / 乱」需要诊断时使用；当需要评审动效、统一全站动效调性时使用。关键词：动效、交互、动画、过渡、手感、炫、高级感、丝滑、活泼、设计系统、层级、栅格、字阶、token、hover、滚动、转场、three.js、3D、WebGL、p5.js、创意编程、生成艺术、GSAP、ScrollTrigger、SplitText、艺术方向、风格、海报。
agent_created: true
---

# 前端交互与动效规格

把审美诉求翻译成可执行、可验收、可 lint 的规格。本技能的价值不在「列出有哪些效果」，而在**先诊断问题在哪一层**，再给到钉死数值的方案。

## 三层模型

任何「不好看 / 不高级 / 不动」的抱怨，先判断落在哪一层。误判层是最大的浪费。

| 层 | 症状 | 该动什么 | 证据 |
| --- | --- | --- | --- |
| 静态设计层 | 乱、挤、廉价、没重点、像模板 | 层级、留白、字阶、对比、对齐 | 眯眼看不出主次；四边等距；七八种字号 |
| 动效层 | 死板、突兀、跳、卡顿感、没反馈 | 时序、缓动、编排、状态过渡 | 元素瞬间出现；全用 linear；所有动画同时开始 |
| 平台层 | 真卡、掉帧、手机错乱、键盘用不了 | 属性选择、API 选型、降级 | 动 width/height；无 reduced-motion；只做 hover |

**八成「不高级」死在第 1 层。** 这时候加动效只会更廉价。先诊断，再动手。

## 工作流

### 0. 诊断（先做，不要跳）

读用户原话，对照上表归类，给一句诊断结论：

> 诊断：静态层为主——三个卡片区字号相同、间距等值，没有层级；动效只是次要问题。

用户明确说「太素了、想动起来」时，直接进第 1 步。

### 1. 意图 → 效果族

先落到功能意图，再选具体效果。

| 用户说 | 实际想要 | 首选方向 |
| --- | --- | --- |
| 炫、酷、科技感 | 大面积背景在动 + 指针有反馈 | 渐变流动、粒子背景、光标跟随 |
| 高级、贵气、有格调 | 慢、轻、留白多，动效克制 | 视差、毛玻璃、下划线生长、滚动显现 |
| 丝滑、顺、不卡 | 不是加效果，是调参数 | 改缓动与属性，不加新效果 |
| 活泼、有趣、年轻 | 有回弹、有小惊喜 | 点赞弹跳、磁铁按钮、水波纹 |
| 沉浸、讲故事 | 一屏一节、跟着叙事走 | 滚动捕捉、视差、打字机、时间轴 |
| 专业、可信、B 端 | 信息先到位，动效只做引导 | 骨架屏、数字滚动、步骤条、实时校验 |
| 让人想点、有引导 | 明确的悬停/按压暗示 | 悬停上浮、按压回弹、呼吸感 |
| 有质感、精致 | 小反馈叠加，而非一个大特效 | 聚焦高亮、Tooltip、分段控制器、按压回弹 |

反向词同样要接：**别太花 / 低调点** → 只降幅度，时长缓动不动；**极简 / 性冷淡** → 整体降一档；**夸张 / 有冲击力** → 升到强烈档。

### 2. 落位：触发时机 × 微交互四段

先定触发点，再看这个交互的四段是否完整（Dan Saffer 模型）：

| 段 | 要回答的问题 | 缺了会怎样 |
| --- | --- | --- |
| 触发器 Trigger | 悬停 / 点击 / 滚动 / 定时 / 系统事件 | 用户不知道能不能点 |
| 规则 Rules | 点了发生什么、能不能撤销、有没有中间态 | 点完像没反应 |
| 反馈 Feedback | 视觉、动效、文案、声音，至少两样 | 用户不确定成功 |
| 循环与模式 Loops & Modes | 重复操作会不会退化、有没有例外态 | 第二次用就出错 |

触发时机分类：入场 / 滚动 / 悬停 / 点击 / 弹层 / 展开 / 导航 / 手势 / 表单 / 数据 / 装饰 / 转场。

### 3. 定栈：先选实现方式，再谈效果

同一个效果，用错技术栈会白付十倍代价。**默认从最轻的开始，只有当它做不到时才升级。**

| 需求 | 用什么 | 代价 |
| --- | --- | --- |
| 状态切换（hover / focus / active）、简单入场 | CSS `transition` + `@keyframes` | 0 依赖，自动可打断 |
| 需要读当前值、动态目标、播放控制 | Web Animations API | 0 依赖，命令式 |
| 时间线编排、滚动绑定、文字拆分、SVG 形变、布局动画 | **GSAP** | ~70KB，换到确定性与控制力 |
| 真实三维空间、材质反射、产品可转看 | **three.js** | 数百 KB + GPU 开销 + 低端机风险 |
| 生成图案、噪点纹理、粒子场、数据艺术、印刷海报 | **p5.js** | 只在「生成」场景划算 |

判断口径：

- **能在 CSS 里写出来的，不要上 GSAP**（单次 hover 变色不需要 70KB）
- **能拍成照片/渲染成图的，不要上 three.js**（3D 只在空间关系本身是信息时才划算）
- **能用设计稿交付的，不要上 p5.js**（生成艺术的价值在于「可无限变化且可复现」）
- 三套混用时**只允许一套主导**：GSAP 编排，three.js 渲染场景，p5.js 生成底纹——不要让两套同时驱动同一个元素

细节分别见 `references/gsap-motion.md`、`references/threejs-3d.md`、`references/p5js-creative-coding.md`。

### 4. 选型：查词库，不要凭记忆

用脚本检索，别整份读文件：

```bash
# S 指本技能所在目录，按实际安装位置填写
S="<skill-dir>"
python3 "$S/scripts/search_terms.py" "悬停"          # 跨全部参考文件模糊搜
python3 "$S/scripts/search_terms.py" "stagger" --limit 5
python3 "$S/scripts/search_terms.py" --list          # 看有哪些章节
```

脚本按自身位置定位 `references/`，与当前工作目录无关，所以在哪个目录下调用都能跑。

一次选 **1–3 个**。一个位置堆三个以上效果，观感立刻掉档。

术语必须给**中文名 + 英文名**（「悬停上浮 Hover Lift」）。英文名是让 AI 一次写对的关键。

### 5. 锁参：三旋钮 + token

任何调性由三个旋钮决定。**先拧旋钮，再挑术语**——反过来做，就会得到「什么效果都有，但完全不统一」。

| 旋钮 | 克制 | 标准（默认） | 强烈 |
| --- | --- | --- | --- |
| 幅度 | 位移 2–4px、缩放 1.02 | 位移 8–16px、缩放 1.05 | 位移 24–40px、缩放 1.1 |
| 时长 | 0.15–0.25s | 0.3–0.4s | 0.5–0.8s |
| 缓动 | linear（机械） | ease-out（自然收敛） | spring（有回弹） |

落具体数值时读 `references/motion-tokens.md`，那是可直接抄的 duration / easing / spring 表，与 Material 3 token 对齐。**同一个动作全站必须用同一个 token**，这是「看起来专业」最便宜的来源。

### 6. 出卡：规格卡

每套方案输出卡片。它是「锁定」的载体——后续写码改码都以卡为准。

模板见 `assets/spec-card.md`，最小形态：

```
【效果规格】悬停上浮 / Hover Lift
触发   .card 上 hover
变化   translateY 0 → -4px；box-shadow 0 0 0 rgba → 0 12px 24px rgba(27,58,46,.10)
参数   duration.200 / ease.standard；延迟 0
收尾   hover 结束同参数回到原位
降级   触屏无 hover → 改为 active 时 scale .98；reduced-motion → 只留阴影变化
约束   只动 transform / opacity / box-shadow；不改 width、height、top、left
验收   移入 200ms 内到位；移出无残留中间态；相邻卡片不位移；60fps 掉帧为零
```

一次最多 3 张，超过先问「哪两个是重点」。

### 7. 自检：跑 lint，不要靠自觉

```bash
S="<skill-dir>"   # 同第 3 步，指本技能所在目录
python3 "$S/scripts/lint_motion.py" src/components/Card.tsx
python3 "$S/scripts/lint_motion.py" src/styles/ --format json
```

会查出：动画宽高/位置属性、`transition: all`、超长时长、缺 `prefers-reduced-motion`、hover 未做触屏降级、`will-change` 滥用。有 `error` 必须改完再交付。

交付前对照 `references/review-rubric.md` 打一次分，低于 3 分的维度要么补、要么说明为什么不做。

## 参考文件地图

按需读，不要预读全部。

| 文件 | 内容 | 什么时候读 |
| --- | --- | --- |
| `references/effect-catalog.md` | 68 条具体效果，每条带可复制话术 | 要给「看得见的效果」找名字时 |
| `references/motion-vocabulary.md` | 动效职能、编排、缓动、弹簧物理、页面转场范式 | 解释「为什么这么动」、多元素编排、转场 |
| `references/design-vocabulary.md` | 层级、栅格、字体阶梯、色彩、格式塔、状态矩阵 | 用户说「不好看 / 廉价 / 乱」而非「不够动」时 |
| `references/motion-tokens.md` | 可直接抄的 duration / easing / spring 数值与 CSS 变量 | 落参数、对齐设计系统 |
| `references/platform-and-perf.md` | 属性成本、API 选型、性能预算、无障碍、移动端 | 写代码前、排查卡顿、适配触屏 |
| `references/review-rubric.md` | 6 维打分表与扣分项 | 评审既有页面、交付前自检 |
| `references/art-direction.md` | 十种艺术方向（瑞士 / 包豪斯 / 构成主义 / Art Deco / 编辑 / 粗野 / 极简 / 孟菲斯 / Y2K / 印刷质感）的栅格、字体、色彩、动效规格，构图与配色法则，流派→动效映射 | 用户说「要有点风格 / 艺术感 / 杂志感」、需要定调时 |
| `references/gsap-motion.md` | 授权现状、timeline 位置参数、ScrollTrigger、SplitText、Flip、React 集成、性能与反模式 | 需要时间线编排、滚动绑定、文字拆分、布局动画时 |
| `references/threejs-3d.md` | 该不该上 3D、最小骨架、相机构图、光照材质、性能预算、滚动运镜、降级 | 做 3D 产品展示、空间叙事、WebGL 特效时 |
| `references/p5js-creative-coding.md` | 2.0 变更、噪声流场、粒子、递归细分、字体轮廓、OKLCH 色带、印刷导出、嵌入方式 | 做生成艺术、动态海报、底纹纹理、数据艺术时 |
| `references/premium-components.md` | 40 个高级交互组件的完整规格（静止态 / 状态机 / 参数 / 降级 / 验收 / 常见做错），含「怎么补新组件」的六格法 | 做具体组件、提升产品质感、需要可直接落地的交互细节时 |

## 硬门槛（不可协商）

1. **只动合成属性**：`transform` / `opacity` / `filter`。动 width、height、top、left、margin 触发重排，必掉帧。手风琴这类必须改高度的场景，用 `grid-template-rows: 0fr → 1fr` 或 `clip-path`，并说明理由。
2. **`prefers-reduced-motion` 要降级，不能直接 `animation: none` 了事**。位移与缩放关掉，但保留透明度或颜色变化，否则反馈信息一起消失。
3. **`hover` 必须配 `focus-visible`**。键盘用户看不到 hover，触屏也没有。hover 样式包在 `@media (hover: hover) and (pointer: fine)` 里。
4. **一页最多两个主效果**。其余用 0.15–0.25s 的微交互填充。全是动效等于没有重点。
5. **不让动效阻塞交互**：不要用 animationend / setTimeout 锁按钮，改用乐观更新，或即时可点、失败回滚。

## 反模式

- 用动效掩盖排版问题（层级没做，加动效只会更乱）
- 全站 `transition: all`（性能不可控，误伤布局属性）
- hover 是唯一反馈（触屏与键盘直接失能）
- 同类动作不同时长（各组件自己写 0.3 / 0.25 / 0.4，立刻显廉价）
- 弹簧参数随手写（表单、列表这类高频操作用 overshoot 会让人晕）
- 无限循环 + 大幅位移的装饰动画（晕动症风险，验收必挂）

## 工作方式

- 信息缺失不要连环追问。按默认值出卡，一行内标注假设：「按桌面优先、卡片列表假设」。
- 用户改主意，先更新规格卡，再改代码。不要出现「卡上 0.25s、代码里 0.6s」。
- 用户拿不准时给 2 个方向对比（克制版 / 强烈版各一张卡），不要一次给五个。
- 用户给参考网站或截图：先判断「这个效果叫什么」，再照卡打参数。说不清术语就别凭手感复刻，复刻必走样。
- 用户问「为什么不好看」，先按三层模型诊断，别直接推荐动效。
