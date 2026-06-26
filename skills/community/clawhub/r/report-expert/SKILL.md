---
name: report-expert
description: "生成 HTML 报告页面并部署到 Cloudflare Pages 站点。五模块架构：输入适配、报告生产、结构检查修复、小站维护、验证修复。触发词：写报告、发布报告、部署报告、生成报告页面、出报告、做报告、写页面、发布到CF、部署到CF、上线报告、report publisher、报告专家、deploy report、publish report。不触发：纯文档下载/上传、非 HTML 内容生成、本地文件管理、其他平台部署。"
---

# 报告专家 v2.0

将调研内容生成 HTML 报告，部署到 Cloudflare Pages 小站，自动检查修复 HTML 结构问题，验证线上正确性。支持多种输入格式（HTML/Markdown/URL/纯文本）自动适配，CF双向同步保证本地与线上一致。

---

## 前置配置

TOOLS.md 中添加：

```
### Report Expert 技能配置
- `CLOUDFLARE_API_TOKEN=cfat_xxxx`    # 必需
- `REPORT_CF_PROJECT=xuedi`           # 必需，CF Pages 项目名
- `REPORT_SITE_NAME=雪地`              # 必需，小站显示名
- `REPORT_CUSTOM_DOMAIN=xue.mei.pub`  # 可选，不填用 *.pages.dev
```

---

## 五模块架构

| 模块 | 文件 | 职责 |
|------|------|------|
| **输入适配** | `lib/adapter.py` | 自动检测输入类型（HTML/Markdown/URL/纯文本），转换为规范 HTML |
| **报告生产** | `lib/report.py` | 提取 body → lint 修复 → 图片同步 → 生成页面 → 写入 dist |
| **结构修复** | `lib/html_lint.py` | 可扩展的 lint+fix 管线，12 条规则自动检查+修复 |
| **小站维护** | `lib/site.py` | 索引管理、资源同步、CF双向同步、页面更新、CF 部署 |
| **验证修复** | `lib/verify.py` | 从 lint 管线生成线上验证清单，诊断失败原因 |

依赖：`adapter → report → html_lint → page → config`，`site → html_lint → page → config → remote_deploy`，`verify → html_lint → config`

html_lint 是 report/site 的共享守门人——produce 和 update_pages 都用同一套管线。

---

## 输入适配

支持四种输入类型，自动检测转换：
- **HTML** — 直接使用，无需转换
- **Markdown** — markdown 库渲染（表格、代码块、目录）
- **URL** — curl 抓取网页，提取 body 清洗（移除 script/nav/sidebar）
- **纯文本** — 按段落包裹 `<p>` 标签

检测逻辑：看扩展名 → 看 URL 前缀 → 读前 2000 字符判断内容特征。标题从 Markdown 首行标题、HTML `<title>` 标签、URL 页面标题自动提取。

---

## HTML 结构检查修复（核心能力）

lint+fix 管线保证产出 HTML 结构完整。每条规则同时具备 check+fix，发现问题就修。流程：检查 → 修复 → 确认（最多 3 轮）。

### 规则清单

| Rule | Stage | 修复动作 |
|------|-------|---------|
| DivBalance | body | 多余/缺失 `</div>` 从尾部处理 |
| NoDuplicateWrapper | body | 多余 wrapper 剥离 |
| NoFrameworkChrome | body | 移除 header/footer/toc 等模板 chrome |
| ImgPathAbsolute | body | `../images/` → `/images/` |
| ScriptSafety | body | 移除危险 `<script>`（只检查 `<script>` 标签内） |
| TagBalance | body | 非语义标签闭合补充 |
| StyleConflict | body | 全局样式加 `.page-body` 前缀 |
| BodyNotEmpty | body | ❌ 无法修复，阻断部署 |
| PageDivBalance | page | `</body>` 前补充/移除 `</div>` |
| PageImgIntegrity | page | 缺失图片 → SVG 占位图 |
| PageStructure | page | ❌ 无法修复，阻断部署 |

**新增规则只需定义 LintRule 子类，注册到 default_pipeline()。**

---

## 工作流程

### 一键部署（自动适配输入类型）

```bash
uv run deploy.py deploy <category> <source> --title "标题" --desc "描述"
# source 支持: .html / .md / URL / 纯文本文件
```

### 分步操作

```bash
uv run deploy.py produce <category> <source> --title "标题"  # 适配+生产到 dist
uv run deploy.py publish                                    # 部署到 CF
uv run deploy.py sync                                       # 从 CF 线上同步缺失文件到 dist
uv run deploy.py verify                                     # 验证线上结果
```

### 维护命令

```bash
uv run deploy.py add <filename> --title T --desc D --category C [--url U]
uv run deploy.py remove <category/filename>
uv run deploy.py rebuild_index
uv run deploy.py update              # 用最新模板+lint 重新包裹所有页面
uv run deploy.py check               # 检查配置
```

---

## CF双向同步

`sync_from_cf()` 从线上站点拉取缺失文件到 dist，保证本地与线上一致：
1. 拉取线上 index.json 获取页面列表
2. 对比 dist 中缺失的文件逐个下载
3. 合并线上索引到本地索引

应用场景：dist 被意外清理后恢复、新环境初始化、多人协作同步。

---

## 索引安全

三层保障防止 dist 被清理时丢失：
1. **dist/index.json** — 正常路径
2. **技能根目录 index.json** — 每次写索引时同步备份
3. **线上 index.json** — 终极恢复源

`load_index_safe()` 按优先级依次恢复。

---

## 验证流程

部署后 agent 用 web_fetch 逐项验证。验证清单从 lint 管线 online stage 规则自动生成。失败 → diagnose → 修复 → publish → 再验证，最多 3 次。

---

## 文件清单

```
deploy.py              — CLI 入口
lib/adapter.py         — 输入适配（HTML/Markdown/URL/纯文本 → HTML）
lib/config.py          — 配置加载 + 索引读写 + 分类常量
lib/html_lint.py       — lint+fix 管线（LintRule + LintPipeline + 12 规则）
lib/page.py            — 页面 HTML 生成（纯模板渲染）
lib/report.py          — 报告生产（提取 → lint → 图片 → 生成 → 写入）
lib/site.py            — 小站维护（索引 + 资源 + CF双向同步 + 更新 + 部署）
lib/remote_deploy.py   — CF Pages wrangler 调用
lib/verify.py          — 验证修复（URL 清单 + 诊断）
references/            — 详细规范
templates/base.css     — 设计系统
templates/index.html   — 首页模板
scripts/main.js        — 交互系统
```