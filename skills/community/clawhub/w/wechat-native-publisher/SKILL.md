---
slug: wechat-native-publisher
displayName: 公众号原生排版推送器
version: 1.2.6
summary: 公众号图文排版+推送一体化工具链。纯文本/md/已排版HTML → 微信原生富文本 → 草稿箱，正文0编辑。含三套主题、排版偏好向导、封面自动生成、发布前自检。v1.2.6安全修复：ClawHub审计3项清零（渲染器HTML转义收敛+消毒器URL scheme白名单+SSRF彻底禁用环境代理）。
license: MIT
description: 把定稿的纯文本/md/已排版HTML，一键渲染成微信原生富文本并推送到公众号草稿箱。支持自动排版和HTML直输两种模式，含主题换肤、排版偏好向导、封面自动生成、发布前自检。
---

# wechat-native-publisher

微信公众号图文「排版 + 推送」一体化工具链。解决公众号领域最头疼的问题：

1. **排版**：公众号不认原生 HTML 粘贴，`<table>`/`<div>` 边框背景会被清洗。必须用「微信原生富文本」结构才能做出白底 + 图标 + 卡片化精品排版，且 **浏览器预览 = 微信端真实渲染**。
2. **流程**：很多工具只能让你「复制粘贴」一段 HTML 再去手动贴。本工链直接把正文推到**草稿箱**，你只需检查排版后点「发布」——**正文 0 编辑**。

## 适用人群
- 泛内容运营者：公众号作者、编辑、代运营、写手，把自己定稿的 `md/txt/word` 一键变成精品图文。
- 不需要写代码：用 `md` 流水线即可；要高度定制再走 `Python 组件` 流水线。

## 第一次使用：确认你的排版风格（第 0 步，2 分钟）

先跑一遍「排版偏好确认」向导，把主题色、署名、渲染规范固定成你的 `wnp_profile.json`，
之后每次推送/预览自动套用，不用重复回答：

```bash
$PY "$SKILL/scripts/init_profile.py"          # 交互式：账号署名 → 主题三选一或自定义配色 → 渲染规范 → 打印确认单 → 保存
```

不想交互可参数直给（脚本化）：
```bash
$PY "$SKILL/scripts/init_profile.py" --name 我的账号 --slogan "清醒，但不冷漠" \
    --theme custom --primary "#2456a6" --accent "#ff6b4a" \
    --concept highlight --numbering on --end-sign on --cover auto
```

生成的 `wnp_profile.json`（放你的工作目录即可，`push_draft`/`make_preview` 自动发现）：
- `theme`：signature / mono / paper / **custom**（自定义主色+强调色，16 色槽自动衍生）
- `sign`：文末品牌签名位（名字 + 签名语）；frontmatter 写了 `sign_name` 时以文章为准
- `rules`：`==高亮==` 用荧光笔还是黑粗 / `##` 是否自动编号 01、02… / 文末签名开关
- `cover`：无封面时是否自动生成同主题几何封面

> 排版规范（wnp_profile.json）与公众号凭据（config.json）**完全分离**：前者管「长什么样」，
> 后者管「推到哪」。凭据依旧只走 `--config`，profile 里永不存 appid/appsecret。

## 一键流程（两种使用方式）

### 方式一：自动排版模式（推荐，0 代码）—— 技能帮你排版

你给纯文本/md，技能用组件库自动排版成微信原生富文本，再推草稿箱。**排版本身是这个技能的硬实力**，不需要你自己写HTML。

```bash
PY=python   # 建议 Python 3.10+（需 requests、Pillow）
SKILL=wechat-native-publisher

# 1) 首次先自检环境（凭据/AppID/IP白名单/连接，有问题会给你指引）
$PY "$SKILL/scripts/push_draft.py" --check-env --config <config.json>

# 2) 把定稿 md 推到草稿箱（自动套用当前目录 wnp_profile.json 的排版规范）
$PY "$SKILL/scripts/push_draft.py" --config <config.json> \
    --md "$SKILL/examples/sample.md"

# 只预览不推送（先自检 + 打印正文）：
#   $PY .../push_draft.py --config <config.json> --md article.md --no-push
# 换主题（覆盖 profile）：--theme mono / --theme paper
# 换排版规范：--profile <其他路径>；跳过自检：--no-validate；BLOCK 仍强推：--force
```

### 方式二：HTML 直输模式 —— 你/AI 已排好版，技能直接推送

你或AI已经用HTML排好版了（符合微信白名单规则：section/rgb/span leaf），技能直接验证+上传图片+推草稿箱。不需要重新排版。

```bash
# 把已排好版的 HTML 推到草稿箱
$PY "$SKILL/scripts/push_draft.py" --config <config.json> \
    --html "$SKILL/examples/sample_html.html"

# 只预览不推送：
#   $PY .../push_draft.py --config <config.json> --html article.html --no-push
```

**HTML 文件格式要求：**
- 元数据用 HTML 注释 frontmatter：`<!-- title: 标题 author: 作者 digest: 摘要 cover: 封面路径 -->`
- 正文为 `<body>` 内内容（或全文，技能自动提取）
- 必须符合微信白名单规则（用 `<section>` 不用 `<div>`/`<table>`，颜色用 `rgb()` 不用 hex，文本节点包 `<span leaf="">`）
- 发布前自检会自动拦截不符合规则的内容，告诉你哪里要改
- 图片用 `<img src="本地路径或URL">`，技能自动上传到微信CDN并替换URL

### md 语法约定（确定性映射，一字不改）

| 输入 | 渲染为 |
|---|---|
| `---` 开头的 frontmatter | 标题/摘要/作者/封面（`title/author/digest/cover` + `sign_name/sign_slogan` 文末签名） |
| `# 标题` | 文章标题元信息（若 frontmatter 已给 title 则此文内 `#` 作为正文大标题） |
| `## 标题` | 章节头，自动编号 01/02… |
| `### 标题` | 节内小标题 |
| `> 引用` | 引用卡片（连续行合并） |
| `**加粗**` | 黑色加粗 |
| `==高亮==` | 橙色荧光笔高亮（内容焦点，推荐给自创概念） |
| `*斜体*` / `` `行内码` `` | 斜体 / 等宽灰底 |
| ` ``` lang ` | 代码块（主题浅底等宽圆角） |
| `- 项` / `1. 项` | 圆点列表 / 序号徽章列表 |
| `---` 独立行 | 主题色分隔线 |
| `![图注](路径或URL)` | 正文插图（自动上传换真实图 URL；配图注） |

> 内容原则：**只做结构映射，不增删、不改写文案**。你写的正文长什么样，推出去就长什么样。

## 主题

| id | 名称 | 调性 | 适合 |
|---|---|---|---|
| `signature` | 绿橙旗舰 | 绿主导(结构) + 橙点缀(焦点) | 职场/观点/个人 IP |
| `mono` | 黑白极简 | 石墨黑 + 唯一经典蓝强调 | 通用职场/科技/方法论 |
| `paper` | 暖棕纸感 | 暖棕结构 + 陶土橙强调 | 读书/随笔/文化 |
| `custom` | 自定义配色 | 你给主色+强调色，16 色槽自动衍生 | 品牌色/账号专属调性 |

`--theme` 一键换肤；渲染与封面取色都跟随主题。
`custom` 由 `init_profile.py --theme custom --primary #RRGGBB --accent #RRGGBB` 定义；
主色管结构（徽章/章节方块/列表/竖线），强调色管焦点（荧光笔/概念/结尾卡），
浅底/浅边/深字/投影等其余槽位按同一色族自动算出，不用你配全。

## 目录结构
```
wechat-native-publisher/
├── SKILL.md
├── scripts/
│   ├── themes.json        # 三套主题的颜色槽（16 个语义槽）
│   ├── theme.py           # 主题加载/换肤/hex 取色 + 自定义配色衍生(apply_custom)
│   ├── renderer.py        # 核心渲染组件库（微信可存活结构：section/rgb/span leaf）
│   ├── md2render.py       # md/txt → 微信组件的确定性解析器（rules：概念高亮/编号）
│   ├── init_profile.py    # ★第 0 步：排版偏好确认向导 → 生成 wnp_profile.json
│   ├── profile.py         # wnp_profile.json 读取/换肤/规则应用（push/preview 共用）
│   ├── validate.py        # 发布前自检（hex/table/text-decoration/script 等 B 级拦截）
│   ├── wx_api.py          # 微信 API（token/封面/正文插图/草稿）—— 不内置凭据
│   ├── make_cover.py      # 封面：插画合成(+裁白边叠字品牌条) / 几何占位(--no-art)
│   └── make_preview.py    # 本地离线预览（微信同结构 + base64 插图；支持 --profile）
├── examples/
│   ├── sample.md          # 通用示例（去品牌，可直接套用）
│   └── sample_html.html   # HTML直输示例（已排好版的微信兼容HTML）
└── references/
    └── wechat-whitelist.md# 微信富文本存活细节
```

> 进阶「Python 组件流水线」请按 `SKILL.md` 下方组件速查，用 `scripts/renderer.py` 的组件
> 自建一个文章模块（导出 `TITLE/AUTHOR/DIGEST/COVER/ILLUSTRATIONS/build_content(images)`）。

## 进阶：Python 组件流水线
需要高度定制（首屏摘要框、part_header 章节头、结尾赞看转卡片等富组件）时，写一个文章模块（导出 `TITLE/AUTHOR/DIGEST/COVER/ILLUSTRATIONS/build_content(images)`），用 `renderer` 组件拼正文：

```bash
$PY .../push_draft.py --config <config.json> --build examples.article
$PY .../make_preview.py --build examples.article --out preview.html
```

组件速查（`scripts/renderer.py`）：`p/key/concept/num_badge/dot/quote_card/summary_box/part_header/chapter_header/section_title/summary_title/img/caption/hr_dashed/signature/end_card`。全部输出 `section`+`rgb()`+`span leaf` 的微信存活结构。

## 配色与安全要点
- 颜色**必须用 rgb()**，不能用 hex（微信富文本会清洗 hex）；下划线用 `border-bottom`（不用 `text-decoration`）；容器统一 `<section>`（不用 `<table>`/`<div>`）。
- **凭据绝不写进 skill**：`config.json` 由 `--config` 指定，或环境变量 `WECHAT_PUSH_CONFIG`。skill 目录不留 config.json。
- **安全**：本 skill 无任何第三方远程渲染，所有处理本地完成；只写入「草稿箱」不群发（群发需管理员扫码）。

### v1.2.6 ClawHub 审计修复（腾讯 A.I.G 扫描 3 项告警 → 清零）

按 ClawHub security-audit 页面（腾讯 A.I.G / AI-Infra-Guard）的 Findings 逐条修复：

**① HTML 注入（未转义标题/签名值）→ 安全边界收敛到 renderer**
- 修复前：md 标题（`#/##/###`）与 frontmatter/profile 的 `sign_name/sign_slogan` 原样插入 HTML，可注入 `<img onerror>` 等。
- 修复后：`renderer.py` 的文本类组件（`h1/chapter_header/section_title/summary_title/signature/caption`）**在组件内部统一 `_esc()` 转义**。所有调用方（md2render、profile 签名、模块流水线）自动安全，且不会与既有转义形成双重转义。

**② 正则消毒器可被编码绕过 → URL scheme 白名单强校验**
- 修复前：`_sanitize_html` 只删字面 `javascript:`，`java&#x73;cript:`/控制字符/`data:text/html` 等编码变体可绕过。
- 修复后（make_preview.py 与 push_draft.py 同步）：
  - URL 属性值先 `html.unescape` + 剥离 C0 控制字符，再解析 scheme
  - 白名单：`http/https`；`data:` 仅 `src` 且必须 `data:image/*;base64`
  - 危险 scheme（javascript/vbscript/data:text/html…）→ 属性清空；相对/协议相对 URL 转义保留
  - `style` 中的 `expression()/behavior/-moz-binding/url(javascript:)` 清空
  - 合法 style/URL 值统一 `html.escape(quote=True)`，防引号逃逸属性注入

**③ SSRF 环境代理旁路 → Session.trust_env=False**
- 修复前：`proxies={"http": None, "https": None}` 挡不住 `ALL_PROXY` 等环境代理（requests `trust_env=True`）。
- 修复后：独立 `requests.Session()` + `sess.trust_env = False`，配合 `_PinnedDNS` 只走校验过的公共 IP 直连。

---

### v1.2.5 安全防护（SSRF + 路径遍历 + DNS重绑定 + HTML消毒 + 临时文件安全 + 防代理绕过）

**远程图片URL防护（SSRF）**：
- 下载远程图片前解析主机名，拒绝所有私有/回环/链路本地/多播/保留IP（IPv4+IPv6）
- 禁用HTTP重定向（防止公开URL重定向到内部地址）
- 仅允许80/443端口
- 流式下载，单张图片最大20MB
- 验证Content-Type为图片类型
- 用Pillow解码验证下载内容确实是有效图片
- **彻底禁用代理**：`requests.Session()` + `session.trust_env = False`，不读取任何环境代理（HTTP_PROXY/HTTPS_PROXY/ALL_PROXY），连接只走校验过的公共 IP 直连

**DNS重绑定防护**：
- DNS只解析一次，验证所有IP后用 `_PinnedDNS` 上下文管理器锁定socket.getaddrinfo
- requests连接时强制使用验证过的IP，不二次解析DNS，防止"验证时公共IP、连接时私有IP"的DNS重绑定攻击
- 连接完成后自动恢复原始DNS解析

**本地图片路径防护（路径遍历）**：
- 所有本地图片路径用 `os.path.realpath()` 解析后，验证仍在授权目录（文章所在目录）之下
- 拒绝 `../` 路径遍历和绝对路径逃逸
- 验证是常规文件（非目录/设备/FIFO）
- 仅允许 `.jpg/.jpeg/.png/.gif/.webp/.bmp` 格式
- 单张图片最大20MB

**HTML消毒（预览+发布双流水线）**：
- 预览流水线（make_preview.py）和发布流水线（push_draft.py）使用同一 `_sanitize_html` 消毒器
- 移除script/iframe/object/embed/form/svg等危险标签及其内容
- 移除on*事件处理器属性（onerror/onload/onclick等）
- **URL scheme 白名单**（v1.2.6）：href/src/action/formaction/xlink:href/poster/background 属性值先 `html.unescape`+剥离控制字符，再按 scheme 判定——仅 http/https 放行；data: 仅限 img 的 `data:image/*;base64`；javascript/vbscript/data:text/html 等一律清空
- 移除style属性中的expression()/behavior/url(javascript:)等危险CSS；合法 style/URL 值转义防属性逃逸
- 所有模式下的TITLE均进行HTML转义，防止标题注入
- 保留微信兼容的安全标签（section/p/span/img/a等）和内联样式

**临时文件安全（防符号链接攻击）**：
- 封面自动生成使用 `tempfile.NamedTemporaryFile()` 生成不可预测的临时文件名
- `--no-push` 预览输出使用 `tempfile.NamedTemporaryFile()` 生成不可预测的临时文件名
- 不使用基于标题hash的可预测文件名，防止攻击者预先创建符号链接覆盖重要文件

**--no-push预览模式无网络请求**：
- `--no-push` 检查在凭据检查、获取access_token、执行pipeline之前
- 预览模式直接调用make_preview生成本地HTML，不获取access_token、不上传图片到微信CDN
- 不需要config.json凭据文件也能使用预览模式
- 预览输出到本地临时文件，用浏览器打开即可查看，无任何网络请求

- 需 `requests` + `Pillow`（封面/插图本地处理）。桌面/服务器均可。

## 参考
- 微信富文本「可存活」结构细节 → `references/wechat-whitelist.md`
- 新手环境指引/errcode 对照 → `push_draft.py --check-env`
