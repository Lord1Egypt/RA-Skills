# 搜广推 ScalingUp 日报 Skill 安装指引 v2.0

## 概述

`scalingup-daily` 是一个 WorkBuddy Skill，定期自动检索 6 类优先级信息源，生成搜广推领域模型 Scaling Up 日报，并**双平台同步**至 IMA 知识库和腾讯文档。

## 文件结构

```
scalingup-daily/
├── SKILL.md                          # Skill 主描述文件（核心配置）v2.0
├── INSTALL.md                        # 本安装指引
├── _meta.json                        # 版本元信息
├── package.json                      # npm 依赖声明（cheerio）
├── scripts/
│   ├── search_wechat.js              # 微信公众号文章搜索脚本
│   └── ima_upload.py                 # IMA 知识库上传脚本
├── references/
│   └── known_papers.md               # 已知核心论文列表 + 机构归属表
└── templates/
    └── daily_report_template.md      # 日报 Markdown 模板
```

## 安装步骤

### 第 1 步：安装前置 Skill

在 WorkBuddy 中需先安装 **3** 个前置 Skill/MCP：

1. **wechat-article-search** — 微信公众号文章搜索
   - 在 WorkBuddy 中搜索并安装该 Skill
2. **ima-skills**（或"腾讯ima"）— IMA 知识库操作
   - 在 WorkBuddy 中搜索并安装该 Skill
   - 配置 IMA API 凭证（见下方）
3. **tencent-docs** — 腾讯文档 MCP
   - 通过 mcporter 注册（见第 5 步）

### 第 2 步：安装 Skill

**方式一：从 ClawHub 安装（推荐）**
```
在 WorkBuddy 中搜索 scalingup-daily 并安装
```

**方式二：手动复制**
```bash
cp -r scalingup-daily ~/.workbuddy/skills/
```

### 第 3 步：安装 Node.js 依赖

```bash
cd ~/.workbuddy/skills/scalingup-daily
npm install
```

如果使用 WorkBuddy 管理的 Node.js：
```bash
cd ~/.workbuddy/skills/scalingup-daily
PATH="~/.workbuddy/binaries/node/versions/22.12.0/bin:$PATH" npm install
```

### 第 4 步：配置 IMA API 凭证

```bash
mkdir -p ~/.config/ima
echo "你的_client_id" > ~/.config/ima/client_id
echo "你的_api_key" > ~/.config/ima/api_key
```

获取方式：IMA 应用 → 设置 → 开放平台 → 创建应用

### 第 5 步：配置腾讯文档 MCP

```bash
export PATH="~/.workbuddy/binaries/node/versions/22.12.0/bin:$PATH"
# 生成授权码
CODE=$(openssl rand -hex 8)
echo "请在浏览器中打开以下链接完成授权："
echo "https://docs.qq.com/scenario/open-claw.html?nlc=1&authType=1&code=$CODE&mcp_source=desktop"
# 授权完成后获取 token 并注册
TOKEN=$(curl -s "https://docs.qq.com/oauth/v2/mcp/token/get?code=$CODE" | jq -r '.data.token')
mcporter config add tencent-docs https://docs.qq.com/openapi/mcp \
  --header "Authorization=$TOKEN" --transport http --scope home
```

### 第 6 步：创建 IMA 知识库

1. 打开 IMA 应用
2. 创建知识库，命名为「龙虾-模型ScalingUp」
3. 记录知识库 ID（KB ID）

### 第 7 步：配置自动化任务

在 WorkBuddy 对话中输入：
```
帮我创建一个每周一早上 8 点执行的自动化任务，名称为"搜广推ScalingUp日报生成"，
使用 scalingup-daily skill 生成日报，并同步至 IMA 知识库和腾讯文档。
```

### 第 8 步：验证安装

执行一次测试运行，检查：
- [ ] ArXiv 论文检索正常
- [ ] 微信公众号搜索正常（wechat-article-search 返回真实 mp.weixin.qq.com 链接）
- [ ] 知乎/技术博客/GitHub/会议论文检索正常
- [ ] 所有引用链接均为真实可访问的 URL（无占位符）
- [ ] 报告开头已注明驱动大模型名称
- [ ] 日报文件正确生成
- [ ] IMA 知识库写入成功
- [ ] **腾讯文档创建成功**

---

## 常见问题

### Q: 微信搜索返回空结果？
A: 搜狗微信搜索有反爬机制，可尝试更换关键词或稍后重试。

### Q: IMA 上传返回 code=220030？
A: 这是限流（非权限问题），sleep 15 秒后重试即可成功。

### Q: 腾讯文档创建报 400006 鉴权失效？
A: token 已过期，需重新走第 5 步的授权流程更新 token。

### Q: 腾讯文档标题报 business 400001？
A: 标题超过 36 字符限制（按字符数计算），适当缩短标题。

### Q: 如何更新已知论文列表？
A: 编辑 `references/known_papers.md`，注意**机构归属必须基于作者 affiliation**。

---

## 技术架构 v2.0

```
┌──────────────────────────────────────────────┐
│        WorkBuddy 自动化任务调度               │
│        (每周一 08:00 触发)                    │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│       scalingup-daily Skill v2.0             │
│       (SKILL.md 定义工作流程)                 │
└──────────────────┬───────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌───────────┐  ┌──────────┐
│ web_   │  │ wechat-   │  │ 引用链接 │
│ search │  │ article-  │  │ 验证     │
│ (6类   │  │ search    │  │ (P0强制) │
│ 信息源)│  │ (微信搜索)│  │          │
└───┬────┘  └─────┬─────┘  └────┬─────┘
    │             │              │
    └──────┬──────┘              │
           ▼                     │
    ┌──────────────────┐         │
    │ 日报 Markdown    │◄────────┘
    │ (本地文件)       │
    └────────┬─────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────┐  ┌──────────────┐
│ IMA      │  │ 腾讯文档     │
│ 知识库   │  │ (Markdown)   │
│ (平台1)  │  │ (平台2)      │
└──────────┘  └──────────────┘
```

## 更新日志

### v2.0（2026-04-26）
- **双平台发布**：新增腾讯文档同步，日报同时上传至 IMA 知识库和腾讯文档
- **引用链接 P0 规范**：所有引用必须为真实可访问链接，严禁占位符
- **大模型声明**：报告开头必须注明驱动大模型名称
- **机构归属表**：`references/known_papers.md` 升级为含完整机构归属的参考表
- **结构化排版**：强制使用多级标题、列表、加粗等 Markdown 元素
- **效率优化**：IMA + 腾讯文档上传链并行启动

### v1.0（2026-04-19）
- 初始版本，支持 6 类信息源检索和 IMA 知识库写入
