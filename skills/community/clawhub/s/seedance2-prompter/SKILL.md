---
name: seedance2-prompter
description: "Seedance 2.0（即梦）视频生成提示词工程。当用户提到 Seedance、即梦、视频提示词、视频生成、AI视频、prompt、镜头语言、分镜、电商视频、产品展示视频 等关键词时激活。"
read_when:
  - Seedance 提示词
  - 即梦提示词
  - 视频生成提示词
  - AI视频 prompt
  - video generation prompt
  - 分镜设计
  - 镜头语言
  - 电商视频
  - 产品展示视频
---

# Seedance 2.0 即梦技能（OpenClaw / ClawHub）

## 用途
使用多模态参考素材（图片/视频/音频/文本）为 **Seedance 2.0** 和 **Seedance 2.0 Fast** 创建高控制力的英文提示词。

本技能适用于：
- 从粗略想法到可用提示词的完整设计
- 模式选择：**纯文本** vs **首帧/尾帧** vs **全素材引用**
- `@asset` 素材映射（每个图片/视频/音频控制什么）
- 4-15 秒时长规划与时间轴节拍
- 超过 15 秒的多段拼接
- 视频延长 / 续接提示词
- 角色替换与定向编辑提示词
- 从参考视频复制镜头语言
- 场景策略（产品广告、短剧、奇幻、MV 等）

---

## 核心规则

1. 默认使用**全能参考模式**（即梦界面选"全能参考"）。
2. 始终包含明确的 **Assets Mapping** 部分：
   - `@image1`：人物参考图（锁定角色外观，每段上传同一张）
   - `@image2`：首帧参考图（第 1 段可不上传，第 2 段起用上一段尾帧截图）
   - 第 1 段若剧情开场不适合用角色特写作为首帧（如城市远景开场），则只上传 `@image1`，不上传 `@image2`
3. 使用带时间码的节拍，每段一个主要动作。
4. 保持提示词简洁可控（≤ 2000 字符硬限制；避免纯诗意模糊描述；画面每段 2-3 句；Sound 只写关键词；删除无用修饰词如 subtle、faintly、slightly）。
5. 用户需要干净输出时添加负面约束。
6. **具体而视觉化** — "a woman in a red trench coat walks through rain-soaked neon streets" >> "a woman walking"。
7. **对话/音效与画面分层且嵌入时间段** — 对话带角色名+情绪标签，音效作为独立层描述。Narration 和 Sound 必须紧跟在对应时间段的画面描述之后，不得堆在 prompt 末尾。
8. **参考图风格匹配视频主题** — 如水墨风格图片配古风主题，霓虹渲染配赛博朋克。

---

## 平台限制（Seedance 2.0）

- 混合输入总数（图片+视频+音频）：**最多 12 个文件**
- 图片：jpeg/png/webp/bmp/tiff/gif，**最多 9 张**，每张 < 30MB
- 视频：mp4/mov，**最多 3 个**，总时长 2-15s，总大小 < 50MB
- 音频：mp3/wav，**最多 3 个**，总时长 ≤ 15s，总大小 < 15MB
- 生成时长：**4-15 秒**
- 提示词长度：**≤ 2000 字符**（含空格和换行，超出会被截断）
- 真实人脸参考图可能被平台审核拦截

---

## 输出格式（默认使用）

1. **Mode（模式）**
2. **Assets Mapping（素材映射）**
3. **Final Prompt（正文提示词）**
4. **Negative Constraints（负面约束）**
5. **Generation Settings（生成设置）**

示例骨架：

```text
Mode: All-Reference
Assets Mapping:
- @image1: character identity anchor (same image for all segments)
- @image2: first frame reference (optional for segment 1, required from segment 2 using previous tail frame)

Final Prompt:
[画幅], [时长], [风格].
Preserve character appearance from @image1. Use @image2 as opening composition.
0-3s: [动作 + 镜头].
Narration (emotion): "旁白内容"
Sound: [音效关键词]
3-7s: [动作 + 转场].
Narration (emotion): "旁白内容"
Sound: [音效关键词]
7-10s: [揭示/高潮 + 结束帧].
Narration (emotion): "旁白内容"
Sound: [音效关键词]

Negative Constraints:
no watermark, no logo, no subtitles, no on-screen text.

Generation Settings:
Duration: 10s
Aspect Ratio: 9:16
```

---

## IP / 版权规避（审核安全提示词）

Seedance 2.0 有平台内容审核。引用可识别的品牌、角色或品牌美学的提示词会被**拒绝**，即使没有使用名称也可能被拦。遵循以下规则：

### 核心原则

1. **绝不使用品牌名、角色名或品牌词** — 甚至不能用 "style of" 引用。
2. **发明完全原创的名字**。使用描述性昵称（如 "Alloy Sentinel"、"Storm-Rabbit"）。
3. **用通用描述替换标志性特征**：
   - ❌ "arc reactor" → ✅ "hex-light energy core"
   - ❌ "yellow lightning mouse" → ✅ "tiny storm-rabbit with glowing cyan antlers"
   - ❌ "red-gold armored suit" → ✅ "custom exo-suit with smooth ceramic panels"
4. **在负面约束中明确列出所有可推断的品牌名、角色名和品牌词**。
5. **使用 family-friendly / PG-13 标记** — 有助通过审核。

### 渐进规避策略

如果提示词被拒绝，逐级增加与原始 IP 的距离：

1. **L1**：替换所有名字为原创昵称，保留大致美学。
2. **L2**：替换标志性视觉特征（颜色、轮廓、标志道具）为完全原创设计。
3. **L3**：彻底改变角色类型（如人形英雄 → 自主机甲+无人机；生物对战 → 抽象元素精灵）。

### 玩具/手办动画

当从图片制作玩具或手办动画时：
- 从提示词中去除所有品牌标识。
- 使用 "original vinyl-style toy figure" 或 "collectible art figure" 替代任何品牌名。
- `@image1` 只绑定比例、颜色、服装轮廓 — 绝不保留 logo 或商标。

---

## 特殊场景

### A) 视频延长
明确写：`Extend @video1 by Xs`。
生成时长填**新增段**的时长，不是最终总时长。

### B) 角色替换
将基础动作/镜头绑定到 `@video1`，替换角色身份绑定到 `@image1`，要求严格保留编舞/时间节奏。

### C) 节拍同步
使用 `@video`/`@audio` 节奏参考，按时间段锁定节拍切换点。

### D) 纯文本生成
无参考素材时使用。提示词必须包含所有视觉指导：风格、色彩、角色描述、镜头和时间轴节拍。特别适合原创角色/生物概念和 IP 安全场景。

### E) 多段拼接（视频 > 15 秒）
Seedance 2.0 单段最长 **15 秒**。更长视频需拆分为链式段落：

1. **第 1 段**：正常生成（最长 15 秒）。结尾留**干净交接帧**（稳定姿态、清晰构图）。
2. **第 2 段起**：上传前段输出为 `@video1`，写 `Extend @video1 by Xs`。包含**连续性说明**，描述最后一帧的画面内容。
3. 重复直到达到目标时长。

始终包含：
- 顶部声明**总时长**和**分段数**。
- 每段末尾的**交接帧描述**（最后一帧画面内容）。
- 明确的连续性指令：preserve identity, outfit, lighting, camera direction。

### F) 对话短剧
有角色台词的剧本场景：
- 画面动作和对话作为**独立层**按时间段分写。
- 对话标签：`Dialogue (角色名, 情绪): "台词"`
- 音效标签：`Sound: [描述]`
- 每 3-5 秒最多一句对话效果最佳。

### G) 产品展示 / 电商广告
产品演示和广告：
- 产品图片绑定到 `@image1` 作为身份锚点。
- 常用技巧：**360° 旋转**、**3D 爆炸视图**、**重组动画**、**英雄光**。
- 背景保持干净（纯色渐变、中性台面或场景化）。
- 指定材质渲染：glass reflections, metallic sheen, matte texture 等。

### H) 一镜到底（多图路标）
无剪辑的连续跟拍镜头：
- 每个 `@image` 分配为**场景路标**（镜头经过的地点、角色或道具）。
- 提示词写成连续镜头路径，按顺序经过每个路标。
- 明确写：`no cuts, single continuous shot` 或 `one-take`。
- `@image1` 作为首帧，后续图片作为沿途环境/角色的参考。

---

## 场景策略速查表

| 场景 | 关键技巧 | 典型模式 |
|------|----------|----------|
| **电商/产品广告** | 360° 旋转、3D 爆炸视图、英雄光、干净背景 | All-Reference |
| **对话短剧** | 对话标签+情绪、音效层、演员走位 | All-Reference 或 First Frame |
| **奇幻/仙侠动画** | 法术粒子、武术编排、能量光环 | Text-only 或 All-Reference |
| **科普/教育** | 4K CGI、透明解剖、标注缩放 | Text-only |
| **MV/节拍同步** | 节拍锁定剪辑、16:9 宽屏、多图蒙太奇 | All-Reference + @audio |
| **一镜到底** | 多图路标、连续镜头、无剪辑 | All-Reference |
| **IP 安全原创角色** | 原创名字、独特特征、明确负面约束 | Text-only |

---

## 技能文件

- `SKILL.md` — 主技能行为定义
- `SKILL.sh` — 本地快速测试脚本
- `scripts/setup_seedance_prompt_workspace.sh` — 工作区脚手架脚本
- `references/recipes.md` — 现成提示词模板
- `references/modes-and-recipes.md` — 模式与控制说明
- `references/camera-and-styles.md` — 镜头语言与视觉风格词汇表
