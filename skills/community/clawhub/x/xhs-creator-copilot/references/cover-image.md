# cover-image.md — 笔记封面图生成模块

> **文档类型**:Skill 参考文档(图片生成)
> **适用 Skill**:`xhs-creator-copilot` v1.1+
> **目标路径**:`references/cover-image.md`
> **版本**:1.0.0
> **强制性国标**:GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》

---

## 0. 这个模块的边界

### ✅ 做什么

- 根据笔记内容(标题、关键数字、情绪)生成**符合小红书风格**的封面图
- 三种视觉风格:`finance`(深底金字)/ `finance_light`(浅底深字)/ `warm`(暖色调)
- **强制添加"AI 生成"角标**(符合 GB 45438-2025 国标)
- 输出 PNG(直接用) + SVG(矢量源,可二次编辑)
- 文件元数据写入 AI 生成属性(隐式标识)

### ❌ 不做什么

- ❌ **不生成真人面部**或**仿冒公众人物**(国标 + 平台双红线)
- ❌ **不去除 AI 角标**(违反 GB 45438-2025,平台被识别后封号)
- ❌ **不生成虚假场景**(如假证券交易所截图、假行情图)
- ❌ **不调用外部图床**(纯本地生成,符合 skill"零平台接触"原则)

### 实现路径

skill 用 **SVG 模板 + LLM 文字填充** 的方式生成图片:

1. 定义 3 套 SVG 模板(finance / finance_light / warm)
2. LLM 提取笔记的核心标题(≤8 字)+ 副标题(≤16 字)+ 关键数字(若有)
3. 填入 SVG 占位符 → 生成 SVG 文件
4. (可选)用 `bash_tool` + `cairosvg` / `rsvg-convert` 转 PNG

不依赖 DALL-E / Midjourney / Stable Diffusion 等外部生成模型,**完全本地** + **完全可控**。

---

## 1. 三种视觉风格规范

### 1.1 finance(深底金字)— 播报型 / 复盘型

**适用场景**:数据播报、行情复盘、市场分析

**视觉特征**:
- 背景:深蓝灰 `#1a2332` 或墨黑 `#0d1117`
- 主标题:亮金 `#d4a017` 或亮黄 `#f4d03f`,加粗
- 副标题:浅灰 `#a0aec0`
- 装饰元素:右下角 K 线图占位 / 数字徽章
- 整体气质:**专业、严肃、有冲击力**

**配色码**:
```
背景:#1a2332
主文字:#f4d03f
副文字:#a0aec0
装饰线:#d4a017
角标背景:rgba(255,255,255,0.85)
```

### 1.2 finance_light(浅底深字)— 教学型 / 对比型

**适用场景**:基础知识、概念对比、入门科普

**视觉特征**:
- 背景:米白 `#faf6e9` 或浅蓝灰 `#f0f4f8`
- 主标题:深蓝 `#1e3a5f`
- 副标题:中灰 `#6c757d`
- 装饰元素:左侧色条 + 圆形装饰
- 整体气质:**清爽、易读、不压迫**

**配色码**:
```
背景:#faf6e9
主文字:#1e3a5f
副文字:#6c757d
装饰色条:#3182ce
角标背景:rgba(0,0,0,0.7)
```

### 1.3 warm(暖色调)— 故事型 / 个人分享

**适用场景**:个人复盘、踩坑分享、情感共鸣

**视觉特征**:
- 背景:暖米色 `#fdf6e3` 或浅橘 `#fff5e1`
- 主标题:深棕 `#5c3317`
- 副标题:中棕 `#a0522d`
- 装饰元素:简笔画 emoji / 手写感线条
- 整体气质:**亲切、有温度、不冷冰冰**

**配色码**:
```
背景:#fdf6e3
主文字:#5c3317
副文字:#a0522d
装饰色条:#cd853f
角标背景:rgba(255,255,255,0.85)
```

---

## 2. 标准 SVG 模板

### 2.1 通用尺寸

小红书图文笔记的标准封面尺寸是 **3:4** 竖图:

- 推荐 **1242 × 1656 px**(高清)
- 最低 **864 × 1080 px**(标准)
- 长宽比 **3:4** 严格遵守(否则被裁切)

### 2.2 finance 模板(完整 SVG 示例)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1242 1656"
     width="1242" height="1656">
  <!-- 背景 -->
  <rect width="1242" height="1656" fill="#1a2332"/>

  <!-- 装饰金条 -->
  <rect x="120" y="280" width="80" height="8" fill="#d4a017"/>

  <!-- 副标题 -->
  <text x="120" y="380" font-family="PingFang SC, Microsoft YaHei, sans-serif"
        font-size="42" fill="#a0aec0" font-weight="500">
    {SUBTITLE}
  </text>

  <!-- 主标题(可换行) -->
  <text x="120" y="520" font-family="PingFang SC, Microsoft YaHei, sans-serif"
        font-size="120" fill="#f4d03f" font-weight="700">
    <tspan x="120" dy="0">{TITLE_LINE_1}</tspan>
    <tspan x="120" dy="140">{TITLE_LINE_2}</tspan>
  </text>

  <!-- 关键数字徽章(若有)-->
  <g transform="translate(120, 1100)">
    <rect width="500" height="120" rx="20" fill="rgba(212,160,23,0.15)"
          stroke="#d4a017" stroke-width="2"/>
    <text x="40" y="80" font-family="sans-serif" font-size="80"
          fill="#f4d03f" font-weight="700">
      {KEY_NUMBER}
    </text>
  </g>

  <!-- 账号水印 -->
  <text x="120" y="1580" font-family="sans-serif" font-size="32"
        fill="#a0aec0" opacity="0.6">
    @{ACCOUNT_NAME}
  </text>

  <!-- ⭐ 强制 AI 角标(GB 45438-2025 要求高度 ≥ 5% 最短边)-->
  <!-- 短边 = 1242 px,5% = 62 px,这里用 70 px 高度更安全 -->
  <g transform="translate(950, 1530)">
    <rect width="220" height="70" rx="35" fill="rgba(255,255,255,0.85)"/>
    <text x="110" y="48" font-family="sans-serif" font-size="36"
          fill="#1a2332" text-anchor="middle" font-weight="600">
      AI 生成
    </text>
  </g>
</svg>
```

### 2.3 占位符替换规则

| 占位符 | 来源 | 上限 | 示例 |
|-------|------|------|------|
| `{TITLE_LINE_1}` | LLM 提取自笔记标题,第一行 | ≤6 字 | "期货的" |
| `{TITLE_LINE_2}` | 同上,第二行 | ≤6 字 | "3 个真相" |
| `{SUBTITLE}` | LLM 生成的副标题 | ≤16 字 | "新手避坑指南" |
| `{KEY_NUMBER}` | 笔记中提取的核心数字(可选) | ≤10 字符 | "亏 18%" / "1847 字" |
| `{ACCOUNT_NAME}` | 用户提供的账号名 | ≤12 字 | "不期而遇" |

**LLM 提取规则**:

```python
def extract_cover_text(note_title: str, note_body: str) -> dict:
    """
    从已起草的笔记中,提取适合封面的关键文字。
    """
    return llm_call(f"""
你是小红书封面文案专家。基于以下笔记,提取封面文字:

笔记标题:{note_title}
笔记正文(前 200 字):{note_body[:200]}

请输出 JSON:
{{
  "title_line_1": "第一行标题(≤6 字,有冲击力)",
  "title_line_2": "第二行标题(≤6 字,可省略)",
  "subtitle": "副标题(≤16 字,简短描述笔记主题)",
  "key_number": "笔记中的关键数字(若无填空字符串)"
}}

要求:
- 不使用"稳赚/必涨/翻倍"等敏感词
- 不使用"震惊/速看/紧急"等标题党
- 突出笔记最核心的价值点
- 标题要够"短",别试图把所有信息塞进去
""")
```

---

## 3. AI 标识规范(GB 45438-2025 强制)

### 3.1 显式标识(必须)

**位置要求**:图片**角落**,文字**高度 ≥ 画面最短边的 5%**

| 图片尺寸 | 最短边 | 角标最低高度 | skill 实际使用 |
|---------|-------|------------|--------------|
| 1242×1656 | 1242 | 62 px | **70 px**(留余量)|
| 864×1080 | 864 | 43 px | **50 px** |

**文字内容**:必须包含"人工智能"或"AI"以及"生成"或"合成"等要素。

skill 默认用 **"AI 生成"** 4 个字,符合最简标识要求。

**位置选择**(三种风格统一):
- 默认右下角(避免遮挡主文字)
- 角标背景:半透明白底 `rgba(255,255,255,0.85)`(深底图)或半透明黑底 `rgba(0,0,0,0.7)`(浅底图)
- 角标内文字:与背景对比鲜明的深色 / 白色

### 3.2 隐式标识(推荐,自动添加)

按 GB 45438-2025 要求,文件元数据中应含 AI 生成属性。

**PNG 元数据**:

```bash
# skill 在生成 PNG 后,用 ImageMagick / exiftool 写入
exiftool -overwrite_original \
  -Comment="AI-generated by xhs-creator-copilot v1.1; \
            tool: Claude SVG template; \
            timestamp: 2026-04-27T10:00:00; \
            standard: GB 45438-2025" \
  cover.png
```

**SVG 元数据**(直接写在文件内):

```xml
<svg xmlns="http://www.w3.org/2000/svg" ...>
  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <rdf:Description>
        <dc:creator>xhs-creator-copilot v1.1 (AI-assisted)</dc:creator>
        <dc:type>AI-generated</dc:type>
        <dc:date>2026-04-27</dc:date>
        <dc:source>GB 45438-2025</dc:source>
      </rdf:Description>
    </rdf:RDF>
  </metadata>
  <!-- ... 图形内容 ... -->
</svg>
```

### 3.3 用户**不得**做的事

skill 在交付时**强制提示**:

```
⚠️ 重要 — 关于 AI 角标的合规要求

1. 角标位于右下角的"AI 生成"文字
   - 这是国标 GB 45438-2025 的强制要求
   - 高度符合"≥画面最短边 5%"标准
   - 不得手动 P 掉、裁切掉、或用其他元素遮挡

2. 文件元数据中含 AI 生成属性
   - 请使用原文件直接上传到小红书
   - 不要先用 PS 等工具重新导出(会丢失元数据)

3. 在小红书发布时,仍需勾选"笔记含 AI 合成内容"
   - 这是双重保险:图片标识 + 后台标识

擅自去除 AI 角标会:
- 违反国标 GB 45438-2025
- 违反平台规则
- 被识别后限流甚至封号
```

---

## 4. 处理流程(skill 内部)

```python
async def generate_cover_image(
    topic: str,
    note_title: str = None,
    note_body: str = None,
    cover_style: str = "finance",  # finance / finance_light / warm
    account_name: str = "我的账号",
    output_dir: str = "outputs/{date}/covers/"
) -> dict:
    """生成封面图。"""

    # 1. 提取封面文字
    if note_title and note_body:
        text = await extract_cover_text(note_title, note_body)
    else:
        text = await extract_cover_text_from_topic(topic)

    # 2. 选模板
    template = load_svg_template(cover_style)

    # 3. 填充占位符
    svg = template.format(
        TITLE_LINE_1=text["title_line_1"],
        TITLE_LINE_2=text["title_line_2"],
        SUBTITLE=text["subtitle"],
        KEY_NUMBER=text["key_number"],
        ACCOUNT_NAME=account_name,
    )

    # 4. 写 SVG 文件(包含 metadata 隐式标识)
    svg_path = f"{output_dir}/cover-{slug(topic)}-{cover_style}.svg"
    write_svg_with_metadata(svg_path, svg, ai_generated=True)

    # 5. 转 PNG(可选,需 cairosvg / rsvg-convert)
    png_path = svg_path.replace(".svg", ".png")
    if has_tool("rsvg-convert"):
        run_bash(f"rsvg-convert -w 1242 -h 1656 {svg_path} -o {png_path}")
        # 写元数据
        if has_tool("exiftool"):
            run_bash(f"""exiftool -overwrite_original \\
                -Comment="AI-generated by xhs-creator-copilot v1.1; \\
                          standard: GB 45438-2025" {png_path}""")
    else:
        png_path = None
        warn_user("无 rsvg-convert,只输出 SVG。可用浏览器打开后截图保存为 PNG。")

    # 6. 输出交付报告
    return {
        "svg_path": svg_path,
        "png_path": png_path,
        "ai_label_visible": True,
        "ai_label_size_pct": 5.6,  # 70/1242
        "metadata_embedded": True,
        "warnings": []
    }
```

---

## 5. 用户交互流程

### 5.1 触发方式 1:笔记起草后追问

笔记起草流程(`task_type=起草笔记`)在 Step 7 自动询问:

```
笔记 final 已生成。需要我顺便给你生成一张封面图吗?

我可以根据笔记内容,生成 3 种风格之一:
A. finance(深底金字)— 适合播报/复盘类
B. finance_light(浅底深字)— 适合教学/对比类
C. warm(暖色调)— 适合故事/分享类(本笔记是版本 B 故事型,默认推荐 C)

回 A/B/C 即可生成,回"不用"跳过。
```

### 5.2 触发方式 2:独立调用

用户也可单独调用:

```
用户:帮我做张封面图,主题"期货新手避坑",风格 finance,加个"亏 18%"的角标
skill:[直接进入生成流程]
```

### 5.3 输出展示

```markdown
## 🎨 封面图已生成

**风格**:finance(深底金字)
**主题**:期货新手避坑
**尺寸**:1242×1656 px(3:4 标准)

📁 文件位置:
- SVG 矢量源:outputs/2026-04-27/covers/cover-qihuo-bikeng-finance.svg
- PNG 直传图:outputs/2026-04-27/covers/cover-qihuo-bikeng-finance.png

🔍 预览:
[显示一个 SVG 内联预览(若环境支持)]

⚠️ 合规提示:
- 图片右下角的"AI 生成"角标符合 GB 45438-2025 国标(高度 5.6%,标准 ≥5%)
- 文件元数据已写入 AI 生成属性
- **不要手动 P 掉角标**,被识别后会限流封号
- 上传到小红书时,仍需勾选"笔记含 AI 合成内容"

💡 不满意可以:
- 让我换风格(回"换 finance_light")
- 让我改文字(回"标题改成 XX")
- 让我重新提取关键词(回"重新提取")
```

---

## 6. 多张封面策略

如果用户想要"多张图组成一组封面"(小红书图文最多 18 张),建议:

```
首图:cover-{topic}-finance.png(主标题,有冲击力)
2-N 图:由真人手绘 / 拍摄 / 配图,**不全部用 AI 生成**

理由:
- 一篇笔记**全部图片都是 AI 生成**会显著提升被识别为"AI 托管"的风险
- 平台 2026-02 公告明确:"全程 AI 托管账号会直接封禁"
- 推荐策略:首图用 AI 生成(标识清楚),内页图真人提供
```

skill **拒绝**为单条笔记一次生成 ≥3 张配图,引导用户混合使用真人素材。

---

## 7. 安全边界(再次强调)

### 7.1 严禁生成的内容

| 类别 | 例 | 后果 |
|------|-----|------|
| 真人面孔 | 任何人脸,无论真人或虚构 | 违反平台 + 国标 |
| 仿冒公众人物 | 像马云 / 李大霄等 | 严重违法 |
| 伪造金融数据图 | 假 K 线 / 假交易截图 | 涉嫌伪造证券信息 |
| 仿冒平台 UI | 假交易所界面、假券商 App 截图 | 涉嫌欺诈 |
| 性暗示 / 暴力 / 违禁 | 无需解释 | 平台 + 法律双红线 |
| 政治敏感 | 无需解释 | 法律红线 |

### 7.2 SVG 模板的安全设计

- 模板**不含**任何真人头像占位符
- **不含**任何模拟 K 线 / 行情数据的图形(防止用户用作假行情图)
- **不含**任何"开户"、"加群"、"扫码"类引导元素

---

## 8. 与其他模块协作

| 上游 | 触发 cover-image |
|------|------------------|
| `content.md` Step 7 | 笔记起草完成后,询问是否生成封面 |
| 用户直接调用 | `task_type=生成封面图` |

| cover-image 下游 | 调用谁 |
|-----------------|-------|
| 生成完毕后 | → `local-output.md` 写文件 + 元数据 |
| 角标合规检查 | → `compliance-guide.md §10.5` |

---

## 9. 已知限制

- 当前版本只用 **SVG 模板** 生成,不调用真正的图像生成模型(DALL-E / SD)
- 这是**有意的设计**:模板确定 → 输出可控 → 不会"画错"或"违规"
- 未来若引入图像生成模型,**必须**同时满足:① AI 角标自动添加 ② 元数据写入 ③ 拒绝违规题材
- 目前不支持背景插画、不支持手绘风格、不支持照片合成

---

## 10. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-27 | 首版。3 种 SVG 模板 + 国标 GB 45438-2025 角标合规 + 元数据写入 |

---

*— EOF —*
