# local-output.md — 本地文件输出规范

> **文档类型**:Skill 参考文档(本地输出规范)
> **适用 Skill**:`xhs-creator-copilot` v1.1+
> **目标路径**:`references/local-output.md`
> **版本**:1.2.0
> **重要变更**:v1.2.0 起,**笔记 final 主输出格式从 Markdown 改为 HTML**,便于直接在浏览器中复制粘贴到小红书

---

## 0. 这个模块的目的

skill 不接触小红书平台,所有产出都以**本地文件**形式交付给用户。本模块定义:

1. **目录结构**:按日期归档,清晰可查
2. **文件命名**:见名知意,不需打开就能定位
3. **文件内容格式**:**预格式化处理**,用户可以直接 Cmd+A 复制粘贴到小红书发布,无需再排版
4. **输出格式策略**(v1.2.0):**HTML 优先,Markdown 备份**

---

## 1. 目录结构

### 1.1 工作目录布局

skill 假设当前工作目录(用户启动 Cowork / Claude Code 的目录)下:

```
当前工作目录/
├── outputs/                        # skill 所有产出物
│   ├── 2026-04-27/                 # 按日期分天归档(YYYY-MM-DD)
│   │   ├── notes/                  # 笔记草稿与最终版(HTML 主)
│   │   ├── covers/                 ⭐ v1.1 新增 — 封面图
│   │   ├── replies/                # 单条私信/评论草稿
│   │   ├── triage/                 # 批量评论分诊清单
│   │   └── humanized/              # 独立的去 AI 化润色任务
│   ├── 2026-04-28/
│   │   └── ...
│   └── 2026-04-29/
│       └── ...
└── data/                           # skill 的运行数据(用户长期积累)
    ├── faq-library.md              # FAQ 风格库(由用户主动告诉 skill 后写入)
    └── publish_log.json            # 发布历史(同上)
```

### 1.2 目录创建规则

- skill 每次启动时**自动检查并创建**当天的子目录(`outputs/YYYY-MM-DD/{notes,covers,replies,triage,humanized}`)
- **不删除历史目录**,即使是几个月前的(用户可能要回看)
- 跨日任务(如晚上 23:50 开始,凌晨 0:10 结束)按**任务开始时间**归档

### 1.3 目录权限

- skill **只读写** `outputs/` 和 `data/` 两个目录
- skill **不读写** 其他用户文件,除非用户主动 `cat` 一份内容粘贴到对话

---

## 2. 文件命名规范

### 2.1 通用规则

- 文件名**全小写 + 短横线分隔**(避免空格、中文、特殊符号)
- 主题部分用**汉语拼音首字母 / 拼音 / 英文** 都可,**不用中文**(避免编码问题)
- 时间用 **HHMM** 格式(24 小时制,如 1430 = 14:30)
- 版本号用 `v1` `v2` `v3` `final`,不用 `1` `2` `3`
- **扩展名**(v1.2.0 起):
  - `.html` → 主输出格式(可直接在浏览器打开复制)
  - `.md` → 备份格式(用户要求或 `output_format=both` 时生成)
  - `.svg` / `.png` → 封面图

### 2.2 笔记类(notes/)

```
note-{type}-{topic-slug}-{version}.html      ⭐ v1.2.0 默认 HTML

示例:
note-tuwen-qihuo-rumen-v1.html       # 图文,期货入门,版本1
note-tuwen-qihuo-rumen-v2.html
note-tuwen-qihuo-rumen-v3.html
note-tuwen-qihuo-rumen-final.html    # 用户选定 + humanize + 合规后的最终版
note-tuwen-qihuo-rumen-final.md      # (可选)Markdown 备份版

note-changwen-baozhang-fengxian-v1.html  # 长文,保障风险
```

字段:
- `type`:`tuwen`(图文)/ `changwen`(长文)/ `shipin`(视频,预留)
- `topic-slug`:主题的拼音首字母或精简拼音,3-6 个汉字内
- `version`:`v1` / `v2` / `v3` / `final`

### 2.3 封面图类(covers/)⭐ v1.1 新增

```
cover-{topic-slug}-{style}.{svg|png}

示例:
cover-qihuo-rumen-finance.svg        # SVG 矢量源(可二次编辑)
cover-qihuo-rumen-finance.png        # PNG 直传图(已含 AI 角标)
cover-qihuo-bikeng-warm.svg          # 暖色调风格
```

字段:
- `topic-slug`:与笔记的 topic-slug 保持一致(便于关联)
- `style`:`finance` / `finance_light` / `warm`

### 2.4 单条回复类(replies/)

```
reply-{kind}-{recipient-slug}-{HHMM}.html

示例:
reply-sixin-zhanghui-1430.html       # 14:30 起草,给 zhanghui 的私信回复
reply-pinglun-mimimimi-1500.html     # 15:00 起草,给"咪咪咪羊"的评论回复
```

字段:
- `kind`:`sixin`(私信)/ `pinglun`(评论)
- `recipient-slug`:粉丝昵称的拼音/精简拼音
- `HHMM`:任务开始时间

### 2.5 批量分诊类(triage/)

```
triage-{HHMM}.html

示例:
triage-1900.html                     # 19:00 时刻的批量分诊清单
triage-2230.html                     # 22:30 第二次分诊
```

如果当日多次分诊,**每次新建一个文件**,**不覆盖**(便于回看历史)。

### 2.6 去 AI 化润色类(humanized/)

```
humanized-{source-hint}-{HHMM}.html

示例:
humanized-blog-post-1230.html        # 12:30 处理的博客文本
humanized-jiangao-1530.html          # 15:30 处理的"讲稿"
```

`source-hint`:用户对原文的简短描述(2-4 个词的拼音/英文)

---

## 3. 文件内容格式(预格式化,HTML 优先)

**核心原则**:用户在浏览器打开任何 final 文件后,**全选复制(Cmd+A → Cmd+C)→ 切到小红书 → 粘贴**,文字格式被保留(段落、换行、emoji),HTML 标签自动剥离。

### 3.1 笔记 final 版的标准格式(HTML)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="generator" content="xhs-creator-copilot v1.1 (AI-assisted)">
  <meta name="ai-content" content="true">
  <title>note-tuwen-qihuo-rumen-final</title>
  <style>
    body {
      font-family: "PingFang SC", "Microsoft YaHei", -apple-system,
                   BlinkMacSystemFont, "Segoe UI", sans-serif;
      max-width: 680px;
      margin: 40px auto;
      padding: 0 24px;
      line-height: 1.85;
      color: #2c3e50;
      font-size: 17px;
      background: #fafafa;
    }
    .copy-zone {
      background: #ffffff;
      padding: 32px;
      border-radius: 12px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
      border-left: 4px solid #ff2741;
    }
    .copy-zone h1 {
      font-size: 22px;
      font-weight: 700;
      color: #1a1a1a;
      margin: 0 0 24px 0;
    }
    .copy-zone p { margin: 0 0 16px 0; }
    .tags {
      color: #2c5282;
      font-size: 16px;
      margin-top: 24px;
    }
    .ai-label {
      font-size: 14px;
      color: #6c757d;
      margin-top: 16px;
      padding-top: 12px;
      border-top: 1px solid #e0e0e0;
    }
    .disclaimer {
      font-size: 14px;
      color: #999;
      margin-top: 8px;
    }
    .checklist {
      background: #fff8e1;
      padding: 20px;
      border-radius: 8px;
      margin-top: 32px;
      font-size: 15px;
      color: #5c3317;
    }
    .checklist h3 { margin: 0 0 12px 0; font-size: 16px; }
    .checklist li { margin: 6px 0; }
  </style>
</head>
<body>

  <!-- ========== 复制区域开始(Cmd+A 全选包含此区域)========== -->
  <div class="copy-zone">

    <h1>关于期货,我踩过的 3 个坑</h1>

    <p>2024 年 4 月,我拿着 10 万块第一次接触期货。</p>

    <p>那时候我以为,期货就是"加杠杆的股票"。<br>
    后来一周亏了 18%,才明白完全不是这么回事。</p>

    <p>我把踩过的坑写下来,给同样想入门的朋友提个醒。</p>

    <p><strong>第一个坑,把保证金当成全部成本。</strong><br>
    我以为 1 万保证金 = 风险 1 万。但合约的实际价值是 10 万,
    价格跌 5%,你账户里就只剩零头。这叫被强平。</p>

    <p><strong>第二个坑,亏了之后想"加仓摊平"。</strong><br>
    真做了一次,从亏 5% 加到亏 18%。期货不是定投,加仓摊平在
    高杠杆下是放大风险,不是分摊风险。</p>

    <p><strong>第三个坑,盯着分时图做日内。</strong><br>
    凌晨 3 点睡不着盯着 K 线,第二天精神状态崩了。
    后来我学乖了,只看日线,周线确认信号才进。</p>

    <p>写出来不是劝退,是想说:这个市场可以参与,但前提是
    搞清楚游戏规则再来。</p>

    <p class="tags">#期货入门 #投资避坑 #理性投资 #交易日记</p>

    <p class="disclaimer">以上仅为个人分享,不构成投资建议。</p>

    <p class="ai-label">本文部分内容由 AI 辅助生成。</p>

  </div>
  <!-- ========== 复制区域结束 ========== -->

  <!-- ========== 以下区域**不复制**,是发布操作指引 ========== -->
  <div class="checklist">
    <h3>📋 真人发布清单(skill 不会替你做)</h3>
    <ol>
      <li>在本浏览器页面 <strong>Cmd+A 全选 → Cmd+C 复制</strong></li>
      <li>切到 <a href="https://creator.xiaohongshu.com">小红书创作者平台</a></li>
      <li>新建图文笔记,粘贴(标题和正文会自动分开)</li>
      <li>上传 <code>outputs/{date}/covers/</code> 中的封面图(若已生成)</li>
      <li><strong>必须勾选「设置 → 内容类型声明 → 笔记含 AI 合成内容」⚠️</strong></li>
      <li>检查话题标签是否显示为蓝色超链接</li>
      <li>真人最后审核内容 → 手动点击发布</li>
    </ol>
    <p style="font-size: 13px; color: #999; margin-top: 16px;">
      合规依据:小红书 2026-02-12 AI 标识公告 · GB 45438-2025 国标 · 2026-03-10 AI 托管治理公告
    </p>
  </div>

</body>
</html>
```

### 3.2 关键设计点

| 设计 | 用途 |
|------|------|
| `<div class="copy-zone">` 边框 | 视觉清晰标出"复制此区域" |
| `<p class="ai-label">本文部分内容由 AI 辅助生成。</p>` | **强制正文级 AI 标识**(2026-02 新规要求)|
| `<meta name="ai-content" content="true">` | HTML 元数据隐式标识 |
| `<p class="disclaimer">` | 期货赛道必备免责声明 |
| `<div class="checklist">` 在 copy-zone **外面** | 复制时不会带上,纯指引 |
| 标题用 `<h1>`、加粗用 `<strong>` | 粘贴到小红书时,小红书自动转纯文本但保留**段落分隔**和**换行** |

### 3.3 用户体验

```
打开 outputs/2026-04-27/notes/note-tuwen-qihuo-rumen-final.html
  ↓
浏览器渲染:左侧红色竖条的卡片区是笔记内容,下方黄色卡片是发布清单
  ↓
Cmd+A(选中整个页面)→ Cmd+C
  ↓
切到小红书创作者平台,在笔记输入框 Cmd+V
  ↓
小红书自动剥离 HTML 标签,但**保留段落、换行、emoji、话题**
  ↓
真人微调(若需要)→ 上传封面图 → 勾选 AI 标识 → 发布
```

**实测兼容性**(经多次验证):

- ✅ Chrome/Safari/Firefox 选择粘贴到小红书 Web 版:文字保留,格式正常
- ✅ 微信桌面版选择粘贴:文字保留
- ⚠️ 富文本编辑器(如 Notion):会保留 HTML 样式(此时建议用 .md 备份版)

### 3.4 同步生成 Markdown 备份(`output_format=both`)

如果用户要求 `output_format=both`,skill 同时生成同名的 `.md` 文件作为备份:

```markdown
<!-- AI 标识(隐式):本文部分内容由 AI 辅助生成 -->

# 关于期货,我踩过的 3 个坑

2024 年 4 月,我拿着 10 万块第一次接触期货。

那时候我以为,期货就是"加杠杆的股票"。
后来一周亏了 18%,才明白完全不是这么回事。

[... 正文 ...]

#期货入门 #投资避坑 #理性投资 #交易日记

---
以上仅为个人分享,不构成投资建议。
本文部分内容由 AI 辅助生成。

<!--
📋 发布清单(同 HTML 版)
- 复制以上文本
- 粘贴到小红书
- 必须勾选「笔记含 AI 合成内容」
-->
```

### 3.5 回复(reply / triage)的标准格式(HTML)

简短示例(完整结构同 §3.1):

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="generator" content="xhs-creator-copilot v1.1 (AI-assisted)">
  <title>reply-pinglun-mimimimi-1500</title>
  <style>
    body { font-family: "PingFang SC", sans-serif; max-width: 720px;
           margin: 40px auto; padding: 0 24px; line-height: 1.8;
           color: #2c3e50; background: #fafafa; }
    .original { background: #fff3cd; padding: 16px; border-left: 4px solid #ffc107;
                border-radius: 6px; margin-bottom: 24px; }
    .candidate { background: #fff; padding: 16px 20px; border-radius: 8px;
                 margin-bottom: 16px; border: 1px solid #e0e0e0; }
    .candidate.recommended { border-color: #ff2741; background: #fff5f5; }
    .candidate-text { font-size: 16px; line-height: 1.8; padding: 12px;
                      background: #f8f9fa; border-radius: 6px; user-select: all; }
    .meta { font-size: 13px; color: #6c757d; margin-top: 8px; }
    .label { display: inline-block; padding: 2px 8px; background: #e0e0e0;
             border-radius: 4px; font-size: 12px; margin-right: 6px; }
  </style>
</head>
<body>

  <h2>回复草稿:给「咪咪咪羊~」的评论</h2>
  <p style="color: #6c757d;">任务时间:2026-04-27 15:00</p>

  <div class="original">
    <strong>原评论</strong>(@咪咪咪羊~ · 03-31)<br>
    "找个期货搭子一起搞钱 🍑"
    <div class="meta">
      ⚠️ 引流嫌疑:"搭子"+"搞钱"组合 · 建议友好回应但不约搭子
    </div>
  </div>

  <h3>候选 A(简短,28 字)</h3>
  <div class="candidate">
    <div class="candidate-text">谢谢关注呀~期货还是各自独立决策更稳妥,常来看笔记交流就好</div>
    <div class="meta"><span class="label">语气</span>友好 <span class="label">含合规边界</span></div>
  </div>

  <h3>候选 B(标准,68 字)⭐ 推荐</h3>
  <div class="candidate recommended">
    <div class="candidate-text">谢谢呀~ 不过期货还是建议各自独立决策,搭子模式容易互相影响判断。你要是有具体问题欢迎评论区问,我看到都会回。</div>
    <div class="meta"><span class="label">语气</span>友好+边界 <span class="label">含独立决策提醒</span></div>
  </div>

  <h3>候选 C(详细+边界,95 字)</h3>
  <div class="candidate">
    <div class="candidate-text">看到啦~ 谢谢关注。不过我个人不建议"组队搞钱"这种模式,期货最忌跟着别人下单。你要是想学习,可以多看我的复盘类笔记,有不懂的评论区问我。一起讨论 OK,但下单一定是各自独立决定 🌱</div>
    <div class="meta"><span class="label">语气</span>温和坚定 <span class="label">强合规</span></div>
  </div>

  <hr>
  <h3>📋 操作指引</h3>
  <ol>
    <li>选 1 条候选 → 点击 candidate-text 区域 → 已自动全选 → Cmd+C 复制</li>
    <li>切到小红书 App/Web → 找到该评论 → 点"回复"</li>
    <li>粘贴 → 真人审阅 → 点击发送</li>
  </ol>

  <p style="font-size: 12px; color: #999; margin-top: 32px;">
    注:本回复由 AI 辅助生成,真人最终决定使用与否。
  </p>

</body>
</html>
```

> 💡 设计巧思:`<div class="candidate-text">` 加 `user-select: all` CSS,
> 用户**单击**该区域即自动全选文字,只需 Cmd+C 即可,无需手动选择起止。

### 3.6 批量分诊(triage)HTML 格式

详见 `reply-triage.md §6 输出格式`,核心结构:

- `<header>` 总览统计
- 4 个 `<section class="priority-{level}">` 分别承载红/黄/绿/特殊四类
- 每条评论一个 `<article>`,内嵌 1-3 个 `<div class="candidate">`
- 末尾一个 `<aside class="checklist">` 真人执行清单(可勾选)

### 3.7 humanized 输出的 HTML 格式

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>去 AI 化处理报告</title>
  <style>
    body { font-family: "PingFang SC", sans-serif; max-width: 800px;
           margin: 40px auto; padding: 0 24px; line-height: 1.8; }
    .score { display: flex; gap: 24px; margin: 24px 0; }
    .score-card { flex: 1; padding: 20px; border-radius: 8px; text-align: center; }
    .score-before { background: #fef3f3; border: 1px solid #ffc9c9; }
    .score-after { background: #f0f9f0; border: 1px solid #b8d4b8; }
    .score-num { font-size: 48px; font-weight: 700; }
    .score-before .score-num { color: #c0392b; }
    .score-after .score-num { color: #27ae60; }
    .humanized-text { background: #fff; padding: 24px; border-radius: 8px;
                      border-left: 4px solid #27ae60; user-select: all; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th, td { padding: 8px 12px; border-bottom: 1px solid #e0e0e0;
             text-align: left; vertical-align: top; }
    th { background: #f8f9fa; }
    .original-text { background: #f5f5f5; padding: 16px; border-radius: 8px;
                     color: #6c757d; font-size: 14px; }
  </style>
</head>
<body>
  <h1>去 AI 化处理报告</h1>
  <p>任务时间:2026-04-27 12:30 · 处理强度:<strong>medium</strong></p>

  <div class="score">
    <div class="score-card score-before">
      <div>处理前</div>
      <div class="score-num">78</div>
      <div>明显 AI 风格</div>
    </div>
    <div class="score-card score-after">
      <div>处理后</div>
      <div class="score-num">32</div>
      <div>略有痕迹,可接受</div>
    </div>
  </div>

  <h2>改后文本(可直接使用)</h2>
  <div class="humanized-text">
    [改后全文]
  </div>

  <h2>主要修改点</h2>
  <table>
    <thead>
      <tr><th>#</th><th>类型</th><th>❌ 原文</th><th>✅ 改后</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td><td>浮夸象征化</td>
        <td>"这是行业的分水岭"</td><td>"这事挺有意思"</td>
      </tr>
      <tr>
        <td>2</td><td>AI 高频词</td>
        <td>"全方位赋能"</td><td>"帮上忙"</td>
      </tr>
      <!-- ... -->
    </tbody>
  </table>

  <h2>原文(对照参考)</h2>
  <div class="original-text">
    [原文全文]
  </div>

</body>
</html>
```

### 3.8 关于"小红书剥离 HTML 但保留格式"的实测说明

实测结论(经多浏览器、多账号验证):

- ✅ **段落分隔**(`<p>`)→ 粘贴时变成换行,**保留**
- ✅ **手动换行**(`<br>`)→ 保留
- ✅ **加粗**(`<strong>`)→ 在小红书富文本编辑器保留为粗体
- ✅ **emoji** 和 **话题标签** → 完整保留,话题自动变蓝
- ⚠️ **标题样式**(`<h1>`)→ 字号信息丢失,但**段落保留**(因此用 H1 安全)
- ❌ **链接、按钮、CSS 样式** → 全部丢失(这正是我们想要的:HTML 不污染笔记内容)
- ❌ **表格、列表** → 转纯文本(因此 HTML 模板里**不**用表格做笔记内容)

**重要**:写笔记内容时**只用 `<h1>` `<p>` `<br>` `<strong>` 这 4 种标签**,确保粘贴可靠。CSS 仅用于浏览器预览美观。

---

## 4. 文件管理规则

### 4.1 不覆盖原则

- 同一主题如果**用户主动调整需求重新生成**,版本号 +1,不覆盖原文件
- 仅在 `final` 版上,如果用户说"再改一下",可覆盖(同时把改前那版备份为 `final-prev`)

### 4.2 清理建议(用户手动)

skill **不主动**删除任何文件。用户可以:
- 每月手动清理 `outputs/<old-date>/` 旧目录
- 把已发布的最终版**移到** `outputs/published/` 自建归档(skill 不强制)

### 4.3 失败任务的处理

如果 skill 在生成中途失败(LLM 报错、用户中断):
- 已生成的部分内容**仍写入文件**,文件名加 `-WIP` 后缀
- 例如:`note-tuwen-qihuo-rumen-v2-WIP.md`
- 用户重启任务时,skill 检测到 WIP 文件会询问"继续之前的还是重新开始"

---

## 5. 编码与换行

- 所有文件统一 **UTF-8 (无 BOM)**
- 换行用 **Unix LF**(`\n`)
- 中文标点用全角(`,。!?:;""''`)
- 数字、英文、emoji 用半角

---

## 6. 跨设备使用提示

如果用户在多台设备使用 skill(笔记本 + 桌面机),建议:

- 把 `outputs/` 目录放在 **iCloud / OneDrive / Dropbox** 同步目录下
- `data/` 目录(FAQ 库、发布历史)同步,**风格沉淀跨设备一致**
- skill 检测到目录在云盘下时,会提示"注意保密"(避免敏感内容泄露)

---

## 7. 给用户的快捷操作建议

为了让"复制粘贴到小红书"更快,推荐用户在 macOS / Windows 设置:

| 操作 | macOS | Windows |
|------|-------|---------|
| 打开 outputs 目录 | `Finder → 收藏夹添加` | `资源管理器 → 固定到快速访问` |
| 打开最新文件 | `open outputs/$(date +%F)/notes/` | (在资源管理器中按修改时间排序) |
| 全选复制 | `Cmd+A → Cmd+C` | `Ctrl+A → Ctrl+C` |
| 切到小红书 | `Cmd+Tab` | `Alt+Tab` |

可以让 skill 在每次输出结束时,**附带**这条快捷操作提示。

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-25 | 首版。日期目录结构 + 4 类输出 + 预格式化"复制即用"规范 |
| **1.2.0** | **2026-04-27** | **主输出格式从 Markdown 改为 HTML**:① 笔记 final 默认 .html(可在浏览器打开后 Cmd+A 复制)② 强制正文级 AI 标识声明 ③ HTML 元数据 `<meta name="ai-content">` 隐式标识 ④ 实测保留段落/换行/话题/emoji ⑤ 新增 covers/ 目录 ⑥ `output_format=both` 同步生成 .md 备份 |

---

*— EOF —*
