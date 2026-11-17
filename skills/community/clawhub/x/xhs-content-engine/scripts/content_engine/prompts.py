"""Prompt 模板集合 — 5 类文本 + 图片 prompt 构造。

每个函数接收"上下文 dict"（拆解卡 + graph + 我方输入）返回完整 prompt 字符串。
不在这里调 LLM；只构造 prompt。LLM 调用在 generate.py 编排。

设计原则：
- prompt 模板放在 Python 字符串里（方便 import / unit test）
- 每个模板都明示"你是谁 / 输出格式 / 硬约束"三段
- 输出格式偏向"少修饰多结构"，方便后续解析
"""

from __future__ import annotations


# ─────────────────────────────────────────────────
# 通用 system prompt 构造
# ─────────────────────────────────────────────────

def system_for_brand(
    brand_voice: str = "",
    brand_story: str = "",
    audience: str = "",
    taboo: str = "",
) -> str:
    """构造品牌侧 system message — 所有生成都需要这一段。

    任意字段空字符串 → 跳过那段（容错：graph 没填也能跑）。
    """
    parts = [
        "你是一个专业的小红书内容策划，正在为「我方」品牌生成对标参考视频/图文的同主题创作。",
        "你的任务是：基于参考拆解卡 + 我方品牌信息 → 生成符合我方 brand-voice 的内容。",
        "",
        "硬性原则：",
        "1. 严守我方 brand-voice 的语气和用词偏好",
        "2. 严守禁忌词清单（包括平台合规 + 品牌调性双约束）",
        "3. 不生成对标视频/图文里的具体专有名词（避免抄袭）",
        "4. 输出格式严格按 user message 要求，不加多余寒暄",
    ]
    if brand_voice:
        parts.extend(["", "── 我方 Brand Voice ──", brand_voice])
    if brand_story:
        parts.extend(["", "── 我方 Brand Story ──", brand_story])
    if audience:
        parts.extend(["", "── 目标客群 ──", audience])
    if taboo:
        parts.extend(["", "── 禁忌词 / 合规要求 ──", taboo])
    return "\n".join(parts)


# ─────────────────────────────────────────────────
# 1) 脚本（核心，先出）
# ─────────────────────────────────────────────────

def prompt_script(
    deconstruction: str,
    product_usp: str = "",
    product_imgs_desc: str = "",
    output_type: str = "video",  # video / image / script
    output_count: int = 1,
) -> str:
    """生成脚本 prompt。

    Args:
        deconstruction: v1 拆解卡完整 markdown
        product_usp: 我方产品卖点（材质 / 工艺 / 价格带）
        product_imgs_desc: 我方产品图描述（如「8 张多角度图，米白色羊绒大衣」）
        output_type: 决定脚本结构（video=分镜 / image=图组规划 / script=拍摄指引）
        output_count: 视频时长档/图片张数
    """
    type_guide = {
        "video": (
            f"输出形式：视频脚本（推断目标时长 15-45s 之间，{output_count} 条同主题视频）。\n"
            "结构：分镜 N 个 × 每个镜头含 [景别 / 画面内容 / 旁白或字幕 / 服化道]。\n"
            "结尾必须有 1 个 5 秒以内的「升华句」或「画面收束」，对应拆解卡里观察到的钩子模式。"
        ),
        "image": (
            f"输出形式：图组规划（{output_count} 张图）。\n"
            "结构：图 1 (封面 / 主推) → 图 2-N (细节 / 搭配 / 场景)。\n"
            "每张图需明示：[构图 / 主体 / 风格 / 在整组里的角色]。"
        ),
        "script": (
            f"输出形式：拍摄指引（{output_count} 套，给摄影师/团队看的 mood 文档）。\n"
            "结构：核心理念 → 镜头清单 → 服化道清单 → 道具清单 → 灯光建议。\n"
            "不必出旁白；侧重可执行的拍摄方案。"
        ),
    }.get(output_type, "")

    # 图片类型有特殊约束：每张图必须是 single isolated subject，否则下游生图会拼图
    image_isolation_constraint = ""
    if output_type == "image":
        image_isolation_constraint = """
## 图片描述硬约束（must follow，下游生图模型会按此严格执行）
- **每张图的"构图/主体"描述必须是 ONE SINGLE isolated subject in ONE frame**
- 禁止用"并排" / "并列" / "两件一起" / "三件同框" / "对比展示" / "目录" / "全部" / "整组" 等集合性词汇
- 一张图只展示一个主体 / 一个 angle / 一个工艺细节
- 即使对标视频是"沉浸式陈列多件并排"，我方图组也要拆成单图序列（图 1 单品 A 全身 → 图 2 单品 A 工艺 → 图 3 单品 B 全身 → ...）
- "在整组里的角色"段落只描述本图叙事位置，不要用画面语言描述其他图
"""

    return f"""## 任务
基于下面的对标拆解卡，给我方品牌生成一条同主题的【{output_type}】内容。

## 参考拆解卡（v1 产出）
{deconstruction}

## 我方产品卖点
{product_usp or "（未提供，agent 自己从拆解卡推断同品类的我方产品类型）"}

## 我方产品图
{product_imgs_desc or "（未提供视觉参考，文案侧自由发挥但不可虚构具体颜色/材质细节）"}

## 输出要求
{type_guide}
{image_isolation_constraint}
## 关键约束
- 复用拆解卡里学到的"情绪钩子"和"旁白逻辑分层"，但**用我方品牌的语气重写**
- 不能出现对标内容里的具体专有名词（品牌 / 主理人 / 地点 / 产品款型）
- 输出纯 markdown，不加 ``` 包裹

直接输出脚本内容。"""


# ─────────────────────────────────────────────────
# 2) 视频内字幕 (caption)
# ─────────────────────────────────────────────────

def prompt_caption(script_md: str) -> str:
    """从脚本里提取"屏幕字幕层"——比旁白更精炼，用于无声播放时也能看懂。"""
    return f"""## 任务
从下面的视频脚本里提取"屏幕字幕"——观众静音播放时也能完整理解内容。

## 输入脚本
{script_md}

## 输出要求
- 一行一条字幕，对应脚本里的一个分镜或时间段
- 每条字幕 ≤ 18 字（屏幕显示舒适度上限）
- 字幕之间空一行，方便人工二次编辑
- 不带时间戳（剪辑时再加）
- 纯文本，不加 markdown 标记

直接输出字幕，从第一条开始。"""


# ─────────────────────────────────────────────────
# 3) 封面文案 (cover.txt)
# ─────────────────────────────────────────────────

def prompt_cover_text(
    script_md: str,
    deconstruction: str,
    title_hint: str = "",
) -> str:
    """生成封面大字 — 钩子句 + 1 个 emoji 点缀。"""
    return f"""## 任务
为下面这条脚本设计封面大字（XHS 视频封面 1 行字 + 1 个 emoji）。

## 脚本
{script_md}

## 对标参考的封面文案（拆解卡里学到的钩子模式）
{title_hint or "（参见拆解卡情绪钩子部分）"}

## 输出要求
- 1 行字，≤ 15 字
- 加 1 个 emoji（💚✨📍 这种偏审美感的；不要 💰🔥🎁）
- 用我方 brand-voice 语气
- 不能照搬对标的封面文案

直接输出 1 行，不解释。"""


# ─────────────────────────────────────────────────
# 4) 发布正文 (desc.txt)
# ─────────────────────────────────────────────────

def prompt_desc(
    script_md: str,
    deconstruction: str,
    cta_hint: str = "",
) -> str:
    """生成 XHS 发布正文 — 长文 + emoji + 段落空行 + 地址 / CTA。"""
    return f"""## 任务
为下面这条脚本生成 XHS 发布正文（desc）。

## 脚本
{script_md}

## 对标参考（拆解卡里 §13 参考发布文案）的 vibe
{deconstruction[:2000]}

## CTA 提示
{cta_hint or "（默认：📍 地址 + 一句温和邀请）"}

## 输出要求
- 200-400 字
- 第一段是钩子句 + emoji 点缀（学拆解卡的 vibe 但用我方语气）
- 段落短，空行多（XHS 视觉留白）
- emoji 用 1-2 个，不堆
- 末尾段：📍地址 + 一句温和邀请（不用"快冲""必入"）
- 纯文本，不加 markdown 标记

直接输出正文。"""


# ─────────────────────────────────────────────────
# 5) 发布标签 (tags.txt)
# ─────────────────────────────────────────────────

def prompt_tags(
    desc: str,
    deconstruction: str,
    location: str = "",
    category: str = "",
) -> str:
    """生成 XHS 发布标签 — 地点 + 品类 + 季节 + 单品 4 类，10-15 个。"""
    return f"""## 任务
为下面这条 XHS 发布正文生成 hashtag 标签。

## 正文
{desc}

## 对标参考标签（拆解卡里 §14）
{deconstruction[:1500]}

## 我方信息
- 地点（本地服务必填）：{location or "（未指定）"}
- 品类：{category or "（从正文推断）"}

## 输出要求
- 10-15 个标签，覆盖 4 类：地点（{2 if location else 0}-4）+ 品类（3-5）+ 季节/场景（1-2）+ 单品（1-3）
- 格式：`#标签1 #标签2 #标签3 ...`（一行，空格分隔）
- 每个标签自带 `#`
- 大词 + 中长尾混合（避免全大词导致竞争激烈，也避免全长尾没流量）
- 不照搬对标，但可参考其结构

直接输出一行 hashtag。"""


# ─────────────────────────────────────────────────
# 6) Seedance prompt（v2.0 仅生成，v2.1 才执行）
# ─────────────────────────────────────────────────

def prompt_seedance_video(
    script_md: str,
    deconstruction: str,
) -> str:
    """从脚本生成 Seedance 2.0 cinema-style prompt。

    **v2.0 设计**：用户要视频时，v2.0 输出此 prompt 取代真视频生成。
    v2.1 接 Seedance API 后会用此 prompt 直接生视频。
    """
    return f"""## 任务
把下面的脚本翻译成 Seedance 2.0 视频生成模型的 cinema-style prompt。

## 用途说明（必须放在输出最顶部）
请在 markdown 最开头加一段：

> ⚠️ **此文件是 v2.0 对"视频生成"请求的产出物——用 Seedance 2.0 prompt
> 取代真实视频。当 v2.1 接入 Seedance API 后，此 prompt 会被直接执行。
> 现阶段你可以：(a) 等待 v2.1 自动跑；(b) 手动复制此 prompt 到 Seedance
> 控制台 / 火山引擎执行；(c) 拿给摄影师作为分镜参考拍摄真实视频。**

## 脚本
{script_md}

## 输出格式（Seedance 2.0 prompt 规范）
为脚本里每个分镜各写一段 prompt，每段含：
- **Shot type**: close-up / medium / wide
- **Subject + action**: 主体 + 动作（具体名词，避免形容词）
- **Setting**: 环境 / 灯光 / 时间
- **Camera movement**: static / push / pull / pan / dolly
- **Mood / aesthetic**: 借拆解卡的风格关键词
- **Duration**: 该镜头时长（秒）

## 输出 markdown 结构
```markdown
> ⚠️ [上方"用途说明"那段引用块]

## Shot 1 (0-3s)
- Shot type: ...
- Subject + action: ...
...

## Shot 2 (3-8s)
...
```

直接输出 markdown，不加额外解释。"""
