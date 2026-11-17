---
name: style-card
version: 0.6.5
description: 图生风格卡——从参考图反推结构化风格卡并入库，再用风格卡为任意文本生成同风格图片。触发场景：用户给一张图说"总结这个画风/反推prompt/做成风格卡"，或用户给文本要求"用我的风格库/风格卡出图"。Use when the user wants to reverse-engineer an image's visual style into a reusable, slot-based style card, or to generate images from text using the accumulated style card library.
---

# Style Card · 图生风格卡

把「这张图真好看」变成可复用资产：**参考图 → 结构化风格卡 → 填槽生成同风格新图**。
核心信仰（借鉴 frontend-slides）：风格说不出口，就 show, don't tell；每次验证踩的坑，都回写成卡的一部分。

## 目录结构（渐进加载，不要一次读全部）

```
style-card/
├── SKILL.md                        # 本文件：工作流地图（每次必读，其余按需）
├── library/
│   ├── INDEX.json                  # 所有风格卡的紧凑元数据（每次必读）
│   └── cards/*.md                  # 风格卡正文（含完整生成prompt，用到哪张读哪张）
├── references/
│   ├── reverse-meta-prompt.md      # 反推模板（仅 Phase A 反推时读）
│   ├── html-base.css               # HTML 引擎强制底座样式（仅 HTML 引擎时读）
│   └── html-template.md            # HTML 引擎结构规范（仅 HTML 引擎时读）
├── scripts/
│   └── export-png.sh               # HTML → PNG 截图导出（仅 HTML 引擎时用）
├── gotchas.md                      # 实战坑清单（生成前必读，发现新坑回写）
└── assets/                         # 各卡的参考原图（卡内引用）
```

**铁律**：`library/cards/` 是唯一事实源。INDEX.json 是派生索引，改卡必须同步改索引。

---

## 引擎选择（先于一切生成动作）

每张卡的元数据带 `engine` 字段；用户没有指定卡、需要新选引擎时按此规则：

| 判断 | 引擎 | 理由 |
|---|---|---|
| 文字密集：知识点 ≥5 个 / 正文文字多 / 中文排版要求高 | **HTML** | agent 手写 HTML 再截图，文字准确率 100% |
| 插画感强：手绘/像素/照片质感、构图复杂图形多 | **ImageGen** | 生图模型的视觉质感代码写不出 |
| 要动起来：原理动画、流程演示、GIF/视频素材 | **html-anim** | CSS 动画手写，节奏可控；ImageGen 只能出静帧 |
| 卡上标了 `engine` 字段 | 按卡执行 | 卡是验证过的事实 |

- HTML 引擎：单文件 HTML、内联 CSS/JS、必带 `html-base.css` 全文、只用 Google Fonts（中文用 Noto Sans SC / ZCOOL 系列）。产出后用 `scripts/export-png.sh` 截图出 PNG
- **html-anim 引擎**：在 HTML 引擎基础上按卡的「动画语言」段写 `@keyframes`，
  统一时间轴保证元素同步；交付自循环 HTML，GIF 用录屏或逐帧截图合成
- ImageGen 引擎：按卡的生成 Prompt 填槽投喂。**先告知用户约 5-10 积分/张**
- 双轨卡（如复古印刷信息图）：默认 HTML 引擎出正式稿，ImageGen 出快速草稿

---

## Phase A · 反推（图 → 风格卡）

输入：用户提供的参考图（本地路径或剪贴板图）。

1. 读 `references/reverse-meta-prompt.md`，严格按其结构分析图片
2. 产出风格卡草稿，必须包含 9 个标准段：
   一句话风格描述 / 基础参数 / 配色系统(带hex) / 构图布局(ASCII线框) /
   字体排印 / 图形元素 / 内容槽位 / 生成Prompt / 禁止出现(负面清单)
3. 展示卡片给用户确认，允许调整后再进入 Phase B

## Phase B · 验证（闭环，不可跳过）

目的：证明这张卡能复现风格，而不是"碰巧像"。

1. 换一批**与原图无关的测试内容**，按卡的 engine 字段选引擎生成
2. ImageGen 引擎：**先告知用户约 5-10 积分/张**，比例按卡的画幅参数；
   HTML 引擎：零积分，写 HTML 后用 `scripts/export-png.sh` 截图
3. 并排对比参考图与生成图，从四个维度评估：配色还原 / 构图还原 / 元素还原 / 文字准确率
4. 差异点做两件事：
   - 回写卡的「禁止出现」段（如：字母混入噪点纹理 → 加"纯色块、无噪点"）
   - 通用性坑（跨卡都会犯的）回写 `gotchas.md`
5. 必要时修改后重生成一次，达到用户满意为止

## Phase C · 入库

1. 卡片存为 `library/cards/风格卡_{风格名}.md`
2. 参考原图存入 `assets/原图_{风格名}.jpg`，卡内更新引用路径
3. 更新 `library/INDEX.json`：name / file / vibe / ratio / use_cases / verified
4. 向用户报一句：库里有几张卡、分别管什么场景

## Phase D · 复用（文本 → 同风格图）

输入：用户的文本内容 + 可选的风格偏好。

1. 读 `library/INDEX.json`，按画幅和场景筛出 1-3 张候选卡
2. **Show, don't tell**：不逼用户用语言挑风格，二选一——
   - 快路径：报候选卡的一句话风格让用户点名
   - 效果路径：用用户文本给每张候选卡出小样，让眼睛选
3. 用户选定后读该卡全文，按「引擎选择」定引擎：
   - HTML 引擎：读 `references/html-base.css` + `references/html-template.md`，
     按卡的配色/构图/槽位段手写单文件 HTML → `scripts/export-png.sh` 出 PNG
   - ImageGen 引擎：文本填槽（遵守槽位字数限制）→ 投喂生成
4. 生成前过一遍该卡「禁止出现」段 + `gotchas.md`，把规避指令写进 prompt
5. 生成 → 自检（HTML：浏览器渲染检查 / ImageGen：文字拼写、幻觉区块）→ 交付
6. 复用中发现新坑 → 回写卡和 gotchas（卡越用越准）

---

## 维护规则

- 每张卡必须经过 Phase B 验证才能标记 `verified: true`
- 未验证的卡可以入库，但复用时要提示用户"这张还没跑过闭环"
- gotchas 只收跨卡通用的坑；卡特有的进该卡的「禁止出现」段
- SKILL.md 保持 < 300 行；细节全部下沉到 references/ 和卡内

## 发布

打包即 GitHub repo / ClawHub skill：目录自包含、零依赖（读图 + ImageGen + 文件系统，无需外部 API）。

## 相关 skill / Related skills

- 风格卡反推出的画风，可直接交给 `text-to-comic` 出漫画/绘本：本 skill 解决「画风从哪来」，它解决「画风怎么落到分镜」。
