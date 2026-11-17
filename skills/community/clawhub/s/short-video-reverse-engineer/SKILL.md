---
name: short-video-reverse-engineer
description: 用于对短视频进行反向工程分析：自动提取关键帧、语音转文字、逐帧视觉分析，并生成包含 AI 提示词（仅中文）、台词时间轴、制作建议的 HTML 分析报告。含合规检查（侵权/违规内容排查）和 10 秒适配方案。适用于抖音/快手/视频号等短视频的内容拆解与二次创作。
agent_created: true
---

# 短视频反向工程分析

## Overview

本技能用于将单个短视频自动拆解为：关键帧截图、带时间戳的台词、视觉元素分析，以及可复用的 AI 生成提示词，最终输出为结构化的 HTML 分析报告（含合规检查 + 10 秒适配方案）。适用于短视频二创、AI 复刻、剧本学习等场景。

## 何时使用

- 用户要求“分析这个视频”、“反推这个短视频的提示词”、“把视频转成剧本/分镜”
- 用户提供了视频文件，希望得到画风、角色、场景、台词、AI 提示词等完整报告
- 需要批量或自动化处理视频素材目录下的视频

## 处理流程

### 1. 扫描待处理视频

扫描指定目录（默认 `~/Desktop/视频素材/`，可按需修改）下的 `.mp4/.mov/.avi/.mkv/.webm` 文件，跳过子目录（尤其是 `已处理/`）。

### 2. 一键提取（帧 + 音频 + 转写 + Contact Sheet）

> **积分优化**：将原来的帧提取、音频提取、Whisper转写、逐帧读取（~15次工具调用）合并为 **1次 Bash 调用 + 1次图片读取**。

使用 `scripts/extract_video_one_shot.py` 一步完成：

```bash
python scripts/extract_video_one_shot.py "视频路径" "临时目录"
```

脚本自动完成（**每次先清空旧帧，防止不同视频的帧混在一起**）：
1. 清空 `frames/` 目录中的旧帧
2. ffmpeg 每 2 秒提取关键帧 → `frames/frame_XXXX.jpg`
3. ffmpeg 提取 WAV 音频（16kHz mono）
4. Whisper medium 模型中文转写 → `transcript.json`
5. 将所有帧拼成 **contact sheet** 拼图 → `contact_sheet.jpg`

**脚本输出**（stdout JSON）包含：帧数、时长、台词全文、各文件路径。

### 3. 视觉分析（读 Contact Sheet 1 张图）

读取 `contact_sheet.jpg`（1 张拼图替代原来 9 张单独读取），从以下维度分析：

- 画风（2D 动漫/写实/3D/手绘等）
- 角色外观（发型、服装、表情、姿态）
- 场景设定（室内外、家具、陈设、氛围）
- 色彩风格（主色调、冷暖对比、光影）
- 镜头语言（景别、角度、构图、切换节奏）

> **积分对比**：旧流程读 9 张图 = 9 次图片读取 → 新流程读 1 张拼图 = 1 次图片读取，节省约 **88% 图片读取积分**。

### 4. 合规检查（强制，生成报告前必做）

在生成提示词和报告前，对所有输出内容进行侵权/违规风险排查并修正：

| 风险类型 | 示例 | 处理方式 |
|---------|------|---------|
| 官方标识模仿 | 红色横幅"高考考点"、政府机关名称 | 改为通用标语（如"考试顺利"）或虚构名称 |
| 真实机构/学校名 | "XX市第三高中"、"XX大学" | 改为"学校门口"、"某中学"等通用表述 |
| 真实证件信息 | 准考证号、身份证号、学号 | 改为"个人信息区域"，标注"虚构道具" |
| 风格绑定特定国家 | "日式动漫风格" | 改为"国漫风格"或"二维动漫风格" |
| 品牌/商标 | 可辨识的品牌Logo、产品名 | 模糊处理或替换为虚构品牌 |
| 敏感社会议题 | 涉及政治、宗教、民族敏感内容 | 中性化表述或删除 |

### 5. 生成 HTML 报告

> **只输出 HTML 版本，不再输出 docx。**

报告结构必须包含以下部分（按序号排列，用 h2 标题）：

一、视频信息 → 文件名/时长/分辨率/台词数
二、合规检查 → 侵权/违规风险排查
三、关键帧分镜图 → contact sheet 拼图（base64 内嵌）
四、视觉元素分析 → 画风/角色/场景/色彩/叙事结构
五、台词时间轴 → 完整对话提取表
六、10秒适配方案 → 压缩策略 + 备用分段方案 + ffmpeg 命令
七、AI生成提示词 → 豆包使用指引 + char_ref.jpg + Prompt（一完整版→二压缩版→三分段版）
八、制作建议 → 工具/工作流/参数

> **关键帧展示格式**：使用 `contact_sheet.jpg`（多宫格拼图）替代逐张展示，节省积分且更直观。如需详细描述，在分镜图下方附描述列表。
> 
> **分镜图风格一致**（v4.9）：全片 contact sheet 和分段分镜图**共用同一套生成参数**（thumb=原帧1/2、gap=4px、bg=#1E1E23、无label），由 gen 脚本统一生成，不依赖 extract_video_one_shot.py 的输出。

**Prompt 输出规则（豆包友好格式，强制）：**
- Prompt 末尾**不要添加** "绝对不要日语，不要英语，只要中国大陆标准普通话" 等语言限制语句
- Prompt 中台词/字幕内容使用视频原始语言即可，不做额外语言约束
- **必须使用自然语言段落格式**，禁止使用以下格式：
  - ❌ `【】` 标记（如 `【场景】` `【角色】` `【台词与动作】`）
  - ❌ `①②③④` 分镜编号
  - ❌ `【镜头】` `【色调】` `【字幕规格】` 等技术参数标签
- ✅ 正确写法：像给人描述视频一样用流畅的中文段落，包含场景、角色外观、对话动作、字幕要求
- ✅ **视频格式统一为 9:16 竖屏**（v4.9）：所有 Prompt 开头必须明确指定"生成一个9:16竖屏短视频"，不再使用 16:9 横屏格式。适用短视频平台（抖音/快手/视频号）
- ✅ 控制每个分段 Prompt 在 **200-300 字**以内
- ✅ 完整版 Prompt 可稍长但不超过 **350 字**
- ✅ **每个 Prompt 板块必须显示对应分镜预览图**（v4.16）：完整版/压缩版显示全部帧横排预览，分段版片段1/片段2各显示对应分段帧预览。`make_seg_preview_sheet()` 统一生成，`max-width:600px`。
- ✅ **Prompt 标题下方显示视频时长说明**（v4.16）：每个 Prompt 板块标题下方必须显示 `<p><strong>视频时长：X.Xs | 台词时长：X.Xs</strong></p>`，压缩版/分段版显示估算值时用 ~ 前缀
- ✅ **每个 Prompt 末尾必须追加字幕提示**（v4.16）：末尾追加醒目提示「**【重要】生成的视频必须在底部添加逐句台词字幕，与角色说话同步显示。**」确保豆包在生成视频时添加字幕
- ✅ **片段间角色/风格一致性（v4.8 → v4.9 强化）**：分段剧本必须保证豆包生成的不同片段人物一致。强制规则：
  - **片段1 Prompt**：末尾追加 `CHAR_DESC` 角色外观设定块
  - **片段2+ Prompt**：开头必须加"接上一段，同一场景同一角色。{角色名}保持和上一段完全一样的外貌、发型、衣着和身体比例。"，末尾追加**与片段1完全相同的** `CHAR_DESC` 块
  - **参考图**：所有片段共用同一张 `char_ref.jpg`（统一角色参考图），**禁止**用分段分镜图（`segN_contact_sheet.jpg`）作为豆包参考图
  - **报告内嵌提示**：在每个分段 Prompt 框上方显示醒目提示"⚠️ 请上传 char_ref.jpg 作为参考图（所有片段共用这一张）"

### 6. 10 秒适配方案输出（强制）

用户使用豆包等工具生成视频，单次上限 10 秒。报告生成后**自动检测台词总时长**，按以下策略输出适配方案：

**判断逻辑：**

| 台词总时长 | 策略 | 说明 |
|-----------|------|------|
| ≤10s | 直接可用 | 报告中的提示词可直接提交生成 |
| 10-20s | 方案 B：剧本压缩 | 用 AI 精简台词到 ≤10s，保留核心冲突和反转。**如压缩后仍超 10s，最多分 2 段** |
| >20s | 方案 A：分段拼接 | 按叙事断点拆 2-N 段（各 ≤10s），逐段生成后 ffmpeg 拼接 |

**方案 B 剧本压缩规则（10-20s 视频）：**
1. 优先压缩到 ≤10s：砍掉铺垫台词，只留核心冲突 + 反转
2. 合并两句台词为一句（如"你每次都只顾着自己舒服，从来都不顾及我的感受" → "你只顾自己舒服，从不顾及我感受"）
3. 用动作/表情描述替代部分台词
4. 压缩后台词总时长必须 ≤9.5s（留 0.5s 缓冲）
5. **如压缩后仍超 10s：最多分 2 段，禁止分 3 段**
6. 输出压缩版提示词（仅中文），标注"压缩版"

**方案 A 分段拼接规则（>20s 视频）：**
1. 拆分点选在叙事转折处（场景切换 / 对话者切换 / 情绪转折）
2. 每段包含完整对话几句 + 明确开头结尾
3. 每段独立写 prompt（含场景/角色/对话/镜头）
4. 段间建议 0.3s fade 过渡（ffmpeg 拼接时加 `-vf "fade=in:0:7,fade=out:0:7"` 类似参数）
5. 输出分段方案表（段号 / 内容 / 时长 / prompt）+ ffmpeg 拼接命令模板

**输出格式：**
在报告 HTML 末尾新增"10 秒适配方案"板块，包含：
- 原始台词总时长
- 采用的策略（直接/压缩/分段）
- 适配后的 prompt（仅中文）
- 如分段：分段方案表 + 拼接命令
- 如压缩：压缩前后对比表

### 7. 生成豆包参考图 + 角色一致性保证（v4.8 新增）

> 豆包每次生成是独立的，不同片段间容易出现人物/风格不一致。此步骤解决该问题。

#### 7a. 统一角色参考图（char_ref.jpg）

从全片挑选最能展示所有角色的帧（推荐 4 帧，横排单行排列，每帧 360px 高，9:16 竖屏裁剪），拼成一张**统一角色参考图**。命名为 `char_ref.jpg`，放在参考图目录中。

> **核心原则**：所有片段共用同一张 `char_ref.jpg` 作为豆包参考图。**只生成单帧/角色展示图，不生成多帧拼图（contact sheet），后者会导致豆包输出变成多格模式。**

#### 7b. 角色一致性描述块（CHAR_DESC）

在每个 Prompt 末尾追加统一的角色设定段落，所有片段内容完全一致：

```
角色外观统一设定（所有片段必须严格一致）：
[角色A]：发型、衣着、脸型、身材、表情范围
[角色B]：发型、衣着、脸型、身材、表情范围
场景/画风：统一的背景和风格描述
```

> **强制要求**：每个分段 Prompt（完整版/片段1/片段2/压缩版）末尾必须追加完全相同的 CHAR_DESC 块。
> **Prompt 展示顺序**（v4.10）：一、完整版 → 二、压缩版 → 三、分段版。统一用 h3 标题编号，分段版的子片段用 h4。

#### 7c. 豆包参考图 + 预览分镜图（v4.23 精简：只生成必要图，不再base64内嵌）

> **积分优化**：旧流程每个视频生成 `char_ref.jpg + N张seg_ref单帧 + 4张预览拼图` 并全部base64内嵌到HTML，HTML体积巨大且写入成本高。v4.23 起只保留以下文件，HTML 改为引用本地文件：

输出目录：`~/Desktop/剧本输出/{视频名}_豆包参考图/`

只保留 5 个文件：
1. **统一角色参考图** `char_ref.jpg`（所有片段共用，导出全部已提取帧横排单行排列，9:16竖屏裁剪）→ ✅ 可上传豆包
2. **完整版_分镜预览.jpg**（全部帧横排预览）→ ⚠️ 仅本地预览，不可上传豆包
3. **压缩版_分镜预览.jpg**（隔帧采样横排预览）→ ⚠️ 仅本地预览，不可上传豆包
4. **片段1_分镜预览.jpg**（第一段帧横排预览）→ ⚠️ 仅本地预览，不可上传豆包
5. **片段2_分镜预览.jpg**（第二段帧横排预览，如适用）→ ⚠️ 仅本地预览，不可上传豆包

**删除**：❌ 不再导出 `segN_ref_XX_tXs.jpg` 单帧高清图。这些单帧数量多、占用大、与预览图功能重复，且上传豆包容易触发多格模式。

**HTML 图片策略**：预览图和 char_ref 均使用相对路径引用（如 `<img src="视频名_豆包参考图/char_ref.jpg">`），不再 base64 内嵌。好处：
- HTML 文件体积从数 MB 降到数十 KB
- 写入和读取成本显著降低
- 图片修改后无需重新生成 HTML

> **目录迁移注意**：移动 HTML 时必须同时移动对应的 `{视频名}_豆包参考图/` 目录，否则图片链接失效。

#### 7d. 豆包使用步骤（报告内嵌说明，强制）

报告中必须包含以下指引（放在 Prompt 区域上方，醒目样式）：

> **📋 豆包生成步骤（保证片段间一致性）：**
> 1. 下载 `char_ref.jpg`（统一角色参考图，所有片段共用）
> 2. **生成片段1**：上传 `char_ref.jpg` + 粘贴片段1 Prompt
> 3. **生成片段2**：上传 **同一张** `char_ref.jpg` + 粘贴片段2 Prompt（Prompt 开头已含"接上一段"）
> 4. 生成片段3…同上，始终用同一张 `char_ref.jpg`
>
> ⚠️ **只上传普通单帧图片**。多帧拼图（contact sheet）会导致豆包把视频也生成为多格模式，已不再生成。

> **尺寸说明**：参考图按 9:16 竖屏裁剪（405×720），满足豆包最低尺寸要求。

### 8. 输出与归档

- 报告保存为：`~/Desktop/剧本输出/[视频名]_细化分析报告.html`（仅 HTML，不输出 docx）
- 参考图保存为：`~/Desktop/剧本输出/[视频名]_豆包参考图/`（Step 7 生成）
- 原视频移动到：`~/Desktop/视频素材/已处理/`
- 清理本次临时文件

> **注意**：视频生成交由用户在豆包等工具中手动完成。本工作流终点为 HTML 报告 + 10 秒适配方案输出 + 豆包参考图（含角色一致性保证）。

## 环境依赖

运行脚本前需确保安装：

```bash
python -m pip install openai-whisper imageio-ffmpeg python-docx pillow
```

ffmpeg 由 `imageio-ffmpeg` 自动下载静态构建。Whisper 调用的是命令行 `ffmpeg`，因此需要把 imageio-ffmpeg 的二进制复制一份命名为 `ffmpeg.exe`（Windows）或创建同名软链接（Linux/macOS）：

```bash
# Windows 示例
cp ffmpeg-win-x86_64-v7.1.exe ffmpeg.exe
```

## 脚本使用

本技能包含以下脚本（位于 `scripts/` 目录）：

- `scripts/extract_video_one_shot.py`：**一键提取**（帧+音频+Whisper+contact sheet），积分优化核心脚本。**v4.22 新增 msys 路径自动转换**（`/c/Users/...` → `C:/Users/...`），杜绝 0 帧重试。
- `scripts/gen_report_template.py`：**可复用 HTML 报告模板**（v4.22，积分优化核心）。读取 JSON 配置文件渲染报告，模板只写一次。**v4.23 移除单帧导出、不再 base64 内嵌图片**。
- `scripts/batch_generate_reports.py`：**批量报告生成**（v4.23）。一次处理多个 `config_*.json`，把每个视频单独调用一次 Bash 改成一次批量调用。

> **路径配置**：脚本中的默认路径（如 `~/Desktop/视频素材/`、ffmpeg 位置）需根据实际用户环境调整。首次使用时检查并修改脚本中的路径常量。

### 典型用法（v4.23 积分优化版）

```bash
# 1. 一键提取（帧+音频+转写+contact sheet，1次调用）
#    路径可用 msys 或 Windows 格式，脚本自动转换
python scripts/extract_video_one_shot.py "视频路径" "临时目录"

# 2. 读取 contact_sheet.jpg + transcript stdout 进行视觉分析（1次图片读取）
# 3. 批量写 JSON 配置（每个视频一个 JSON 文件，零语法错误风险）
# 4. 批量运行模板生成报告（v4.23：一次 Bash 处理多个视频）
python scripts/batch_generate_reports.py <configs_dir>
```

> **v4.22 积分优化说明**：旧流程每个视频写 500+ 行 Python 脚本（内嵌分析数据），中文引号频繁触发 SyntaxError，每次需要 5-15 次 Edit 修复。新流程分析数据写 JSON（天然零语法错误），预编译模板一次复用，**节省 50%+ 报告生成积分**。

### 自动化模式

当作为 WorkBuddy 自动化任务运行时，按以下顺序执行：

1. 读取 `.workbuddy/automations/<automation_id>/memory.md` 查看历史
2. **一键提取**：运行 `scripts/extract_video_one_shot.py`（帧+音频+Whisper+contact sheet 合并为 1 次调用）。**路径可用任意格式，脚本自动转换。**
3. 读取 `contact_sheet.jpg`（1 张拼图）进行视觉分析，替代逐帧读取
4. **合规检查**：排查侵权/违规内容并修正（官方标识、真实机构名、证件信息、风格绑定等）
5. **写 JSON 配置**（v4.22）：每个视频生成一个 JSON 配置文件（`write_config_xxx.py`），包含全部分析数据。JSON 格式天然无 Python 语法错误，**彻底消除 Edit 修复循环**。
6. **模板渲染**（v4.23 批量）：运行 `scripts/batch_generate_reports.py <configs_dir>` 一次批量生成所有 HTML 分析报告（仅 HTML，不输出 docx）
7. **检测台词时长，自动输出 10 秒适配方案**（压缩 / 分段 / 直接可用）
8. 更新 automation memory.md
9. 使用 `present_files` 向用户展示报告

> **积分优化**：旧流程约 25-35 次工具调用（含 5-15 次 Edit 修复语法错误）→ 新流程约 10-13 次工具调用（0 次 Edit 修复），节省约 **60-70% 总积分**。

## 注意事项

- 如果某视频处理失败，跳过该视频继续下一个，并在最终汇总中说明失败原因
- 提示词部分只需中文版本
- 报告 HTML 各板块不得省略（含一致性自检表、音频设计总表）
- 视觉分析若无法自动完成，应由模型读取关键帧后人工编写 analysis.json
- 临时目录默认位于 `.workbuddy/temp_video_analysis/`
- **合规检查为强制步骤**：生成报告前必须排查侵权/违规内容并修正，不得跳过
- **只输出 HTML，不输出 docx**
- **Prompt 末尾不添加语言限制语句**（如"绝对不要日语"等），台词使用视频原始语言即可
- **10 秒适配方案为强制步骤**：报告生成后必须检查台词总时长，输出适配方案（直接/压缩/分段），不得省略
- **积分优化**：使用 `extract_video_one_shot.py` 一键提取 + contact sheet 拼图替代逐帧读取，减少约 70% 工具调用
- **可编辑Prompt框**（v4.7→v4.20，2026-06-30）：Prompt 框内文案支持直接在线编辑。HTML模板规范：
  - **Prompt内容结构**：`<div class="prompt-content" contenteditable="true" data-original="{prompt变量}">{prompt变量}</div>`（注意是 `<div>` 不是 `<span>`，必须带 `contenteditable="true"` 和 `data-original` 属性）
  - **CSS 可编辑状态视觉提示**：`contenteditable="true"` 时显示虚线金边 + 深色背景，聚焦时变为实线
  ```css
  .prompt-content[contenteditable="true"] { outline: 2px dashed #f0c75e; background: #1c2030; border-radius: 4px; padding: 10px; cursor: text; }
  .prompt-content[contenteditable="true"]:focus { outline: 2px solid #f0c75e; background: #1e2232; }
  ```
  - **JS**：页面加载时自动保存原始文案到 `data-orig`（`DOMContentLoaded` 事件），复制按钮复制编辑后的 `innerText`，重置按钮通过 `data-orig` 恢复原文
  - 框内右上角"重置"+"复制"双按钮
- **按钮遮罩修复**（v4.11，2026-06-29）：`.prompt-content` 必须设置 `padding-top: 30px`，否则绝对定位的"复制""重置"按钮会遮住 Prompt 第一行文本。两种方案可选：① `.prompt-box { padding: 40px 20px 20px }`（按钮悬停在 box padding 区）；② `.prompt-content { padding-top: 30px }`（文本下推 30px）。推荐方案①（box padding 预留按钮空间），gen_npy_v410.py 和 gen_sy_v410.py 已修复。

## 已知踩坑 (msys + Windows + docx)

### 1. ffmpeg.exe 路径问题
- `imageio_ffmpeg` 自带的 ffmpeg 不在 PATH 中
- 解决方案：把 `imageio_ffmpeg/binaries/ffmpeg.exe` 复制到 `Python/Scripts/ffmpeg.exe`
- ffmpeg 不接受 msys 风格路径 (`/tmp/xxx`)，必须用 `cygpath -w` 转 Windows 风格
- **关键：调用 `scripts/extract_video_one_shot.py` 时，视频路径和 temp_dir 都必须使用 Windows 风格路径（如 `C:/Users/.../视频素材/xxx.mp4`），不能使用 msys 风格（如 `/c/Users/.../Desktop/...`），否则 ffmpeg 会提取 0 帧并报音频文件不存在**
- ffmpeg 不认符号链接，要先 `cp` 实体文件
- whisper 内部 subprocess 调 ffmpeg，因此 whisper 同样需要 PATH 中有 ffmpeg.exe
- **ffmpeg 路径修复**（2026-06-29）：`extract_video_one_shot.py` 的 `find_ffmpeg()` 和 Whisper PATH 设置均指向 `versions/3.13.12/Scripts/ffmpeg.exe`（而非已废弃的 `envs/default/Scripts/`）

### 2. python-docx 拒收 ffmpeg 抽出的 jpg
- 现象：`UnrecognizedImageError`（baseline 8 mjpeg 探针问题）
- 解决：用 Pillow 重新保存
  ```python
  from PIL import Image
  img = Image.open(raw_path)
  img.save(out_path, "JPEG", quality=92, optimize=True)
  ```

### 3. docx 报告脚本中字符串内嵌中文双引号 → SyntaxError
- 现象：形如 `"他说：\"你好\""` 的写法极易触发字符串提前闭合
- 解决：直接用单引号外层 + 中文「」/『』内层，或写成单引号外层 + 中文内嵌双引号（前提是内层是"而非"）

### 4. docx 报告脚本中 Unicode escape 错误（最隐蔽）
- 现象：`(unicode error) 'unicodeescape' codec can't decode bytes in position X-Y: truncated \uXXXX escape`
- 根因：用 `\u7ad6` 这种转义写中文 prompt 时，手抖写成 `\u7豎` (把"竖"字误填进 hex 位) 或 `\u飩车` (开头就不是 4 位 hex)
- 解决：用 `fix_unicode_robust.py` 一次性修复：
  ```python
  import re
  HEX4_RE = re.compile(r'\\u([0-9a-fA-F]{4})')   # 必须 raw string，避免正则本身被解析为 \u
  BARE_U_RE = re.compile(r'\\u(?![0-9a-fA-F]{4})')
  text = BARE_U_RE.sub('', text)                 # 删掉非法的 \u
  text = HEX4_RE.sub(lambda m: chr(int(m.group(1), 16)), text)  # 合法 \uXXXX 还原为字面字符
  ```
- 经验：**写 docx 报告脚本时直接用中文字符串，不要用 `\uXXXX` 转义**。如必须使用，提交前先跑这个 fix 脚本过一遍

### 5. 自动化场景下需把"已扫描但需确认"的视频告知用户
- 不要把桌面所有视频默默处理掉
- 扫描时若发现新视频，先列在 memory.md 备注里等用户确认是否纳入下一轮
