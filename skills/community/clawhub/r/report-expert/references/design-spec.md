# 报告专家 v2.0 设计方案

## 1. 项目概述

将调研内容生成 HTML 报告页面，部署到 Cloudflare Pages 小站。核心设计目标：**产出完整，不遗漏**——图片资源同步、HTML 结构自动检查修复、部署后线上验证闭环。

---

## 2. 概要设计：四模块架构

### 2.1 模块划分

| 模块 | 文件 | 核心职责 | 一句话定位 |
|------|------|----------|-----------|
| 报告生产 | lib/report.py | HTML 提取 → lint修复 → 图片同步 → 页面生成 → 写入dist | 把原始内容变成可部署的产物 |
| 结构修复 | lib/html_lint.py | 可扩展的 lint+fix 管线，12条规则自动检查+修复 | 产出质量守门人 |
| 小站维护 | lib/site.py | 索引管理、资源同步、页面更新、CF部署 | 产物的容器和运输 |
| 验证修复 | lib/verify.py | 从lint管线生成线上验证清单，诊断失败 | 产物的质检员 |

### 2.2 模块依赖关系

<img src="/images/arch-diagram.jpg" alt="四模块架构图">

```
report.py ──→ html_lint.py ──→ page.py ──→ config.py
site.py   ──→ html_lint.py ──→ page.py ──→ config.py ──→ remote_deploy.py
verify.py ──→ html_lint.py ──→ config.py
```

html_lint 是三模块的共享依赖——produce 和 update_pages 都用同一套管线检查+修复。

### 2.3 设计原则

1. **发现问题就修**：lint 规则同时具备 check() 和 fix()，不只报错
2. **修复后必须确认**：管线运行检查→修复→确认（最多3轮），修复后重新检查确认通过
3. **新增规则零改动**：只需定义 LintRule 子类注册到 default_pipeline()，自动生效于所有路径
4. **sys.exit 只在 CLI**：库函数用 raise，CLI 捕获异常后 exit
5. **索引三层保障**：dist → 技能根目录备份 → 线上远程恢复

---

## 3. 详细设计

### 3.1 报告生产（lib/report.py）

produce() 主流程 7 步：

```
1. extract_body()    — 从源HTML提取纯body+style，解包旧模板wrapper
2. lint_body()       — 运行body-stage管线（8条规则）
3. _collect_images() — 扫描<img>标签，复制图片到dist/images/，路径改为绝对
4. generate_page_html() — page.py模板包裹
5. lint_page()       — 运行page-stage管线（3条规则）
6. 写入dist          — 写HTML文件 + 更新index.json
7. _backup_index()   — 备份索引到技能根目录
```

**关键设计点：**

- extract_body() 的清理逻辑（移除header/footer/toc/script等）在 lint 管线的 NoFrameworkChrome 规则中也有，双重保障
- _collect_images() 扫描双引号和单引号的 img src，跳过 http/data 绝对URL，只处理本地相对路径
- 图片文件名空格替换为下划线（URL安全性）
- produce() 中 lint 失败（severity=error）直接 raise ValueError 阻断部署

### 3.2 结构修复（lib/html_lint.py）

#### 3.2.1 管线架构

```
LintRule 基类
  ├── check(html) → LintResult(passed, details, fixable)
  ├── fix(html) → (fixed_html, log)
  └── online_checks() → [str]

LintPipeline
  ├── run(html, stage, label) → (fixed_html, results)
  │     流程: 检查→修复→确认(最多3轮)
  ├── check_only(html, stage) → [LintResult]
  └── get_online_checks() → [{rule, check, severity}]
```

#### 3.2.2 LintResult 语义

- ✅ passed=True — 通过
- 🔧 fixable=True — 有问题但可自动修复
- ❌ fixable=False — 有问题且无法修复（severity=error阻断部署）

#### 3.2.3 规则清单与修复动作

**body-stage（8条规则）**

| Rule | Severity | 检查 | 修复 |
|------|----------|------|------|
| DivBalance | error | div开闭平衡（HTMLParser级，排除script/style） | 多余从尾部移除，缺失在尾部补充 |
| NoDuplicateWrapper | error | 无重复report-wrap/page-body/wrap | 剥离多余wrapper（保留第一个） |
| NoFrameworkChrome | warning | 无模板chrome元素 | regex移除header/footer/toc/back-to-top/各脚本 |
| ImgPathAbsolute | error | 图片src为绝对路径 | ../images/ → /images/ |
| ScriptSafety | warning | 无危险script内容 | 移除含cookie/localStorage/eval的script标签 |
| TagBalance | warning | 非div标签闭合平衡 | 尾部补充缺失闭合标签 |
| StyleConflict | warning | 无全局样式覆盖模板 | 冲突选择器加.page-body前缀 |
| BodyNotEmpty | error | 内容不为空 | ❌ 无法修复，阻断部署 |

**page-stage（3条规则）**

| Rule | Severity | 检查 | 修复 |
|------|----------|------|------|
| PageDivBalance | error | 完整页面div平衡 | </body>前补充/移除 |
| PageImgIntegrity | warning | 图片文件存在于dist | 缺失图片→inline SVG占位图 |
| PageStructure | error | html/head/body/report-wrap/footer/css/js | ❌ 无法修复，阻断部署 |

**online-stage（3条规则，不修改HTML）**

| Rule | 验证项 |
|------|--------|
| OnlineReportChecks | HTTP可达、结构完整、路径正确、无chrome遗留 |
| OnlineAssetChecks | CSS/JS可达、index.json可解析、图片真实 |
| OnlineImageChecks | 图片返回image/*、非HTML fallback |

#### 3.2.4 管线运行流程

<img src="/images/lint-flow-diagram.jpg" alt="Lint管线检查修复闭环流程图">

```
for round in [0, 1, 2, 3]:
    results = check_only(html, stage)
    if round == 0: 打印所有失败项
    
    fixable = [r for r in results if not r.passed and r.fixable]
    if 无fixable失败 or round >= 3:
        return (html, results)  # 最终结果
    
    for each fixable result:
        html = rule.fix(html)  # 应用修复
```

#### 3.2.5 新增规则方式

```python
class MyNewRule(LintRule):
    name = "my_new_rule"
    stage = "body"
    severity = "warning"
    
    def check(self, html):
        if problem_found:
            return LintResult(self, False, "description", fixable=True)
        return LintResult(self, True)
    
    def fix(self, html):
        fixed_html = ...  # 修复逻辑
        return fixed_html, "修复日志"

# 注册到管线
def default_pipeline():
    return LintPipeline([
        ..., MyNewRule(), ...
    ])
```

### 3.3 小站维护（lib/site.py）

#### 3.3.1 核心函数

| 函数 | 职责 |
|------|------|
| copy_assets() | templates/base.css + scripts/main.js → dist/ |
| add_to_index() | 外部页面加入索引 |
| remove_from_index() | 删除页面（索引+dist文件+空目录清理） |
| rebuild_index() | 扫描dist恢复遗漏页面 + 重建首页 |
| update_pages() | extract_body → lint_body → lint_page → 重写所有页面 |
| publish() | copy_assets + deploy_to_cf |
| full_deploy() | produce → copy_assets → deploy_to_cf → verify |

#### 3.3.2 索引安全机制

三层保障防止 dist 被清理时丢失：

```
1. dist/index.json         ← 正常路径
2. 技能根/index.json       ← 每次save_index同步备份
3. 线上/index.json         ← curl拉取终极恢复

load_index_safe() 按优先级: dist → 备份 → 线上
```

- save_index() 使用原子写入（tmp → rename）
- produce() 每次写索引后调用 _backup_index()
- _restore_index_from_remote() 先尝试 curl，再 urllib 兜底

#### 3.3.3 update_pages 流程

```
for each HTML in dist/:
    1. extract_body()          — 提取内容（与produce相同逻辑）
    2. lint_body()             — 管线检查+修复
    3. skip if body empty      — 无法自动修复
    4. 提取title/desc/date     — 从HTML提取元信息
    5. generate_page_html()    — 模板包裹
    6. lint_page()             — 页面级检查+修复
    7. 写回dist
```

### 3.4 验证修复（lib/verify.py）

#### 3.4.1 验证清单生成

从 lint 管线的 online-stage 规则自动收集验证项，合并到 URL 清单：

```
get_verify_urls():
    1. 小站首页 → 基础检查
    2. 报告页面 → OnlineReportChecks 规则产生的8项
    3. 静态资源 → OnlineAssetChecks 规则产生的3项
    4. 图片资源 → OnlineImageChecks 规则产生的3项
```

#### 3.4.2 修复循环

```
验证失败 → diagnose_failure(url, status) → 诊断建议
→ 修复问题 → publish → 再验证
→ 连续3次失败 → 通知用户手动排查
```

### 3.5 配置与部署（lib/config.py + lib/remote_deploy.py）

#### 3.5.1 配置加载

从 TOOLS.md 读取配置，支持格式：
- `KEY=value`
- `KEY=value  # comment`
- `KEY="quoted value"`
- `KEY=`value``（backtick包裹）

必填：CLOUDFLARE_API_TOKEN、REPORT_CF_PROJECT、REPORT_SITE_NAME
可选：REPORT_CUSTOM_DOMAIN

派生：SITE_URL = https://{CUSTOM_DOMAIN} 或 https://{CF_PROJECT}.pages.dev

#### 3.5.2 Cloudflare 部署

remote_deploy.py 调用 wrangler：
- 3次重试 + 30s超时
- --commit-message 传入部署描述
- 部署成功后输出 preview URL

### 3.6 图片资源管理

这是 v2.0 新增的关键能力（v1 完全缺失）。

#### 3.6.1 _collect_images() 流程

```
扫描body中所有<img src="...">标签
  ├── 跳过 http/https/data 绝对URL
  ├── 解析相对路径（相对于源文件目录）
  ├── 检查文件存在性和图片扩展名
  ├── 复制到 dist/images/{safe_name}
  │     safe_name = 原名.replace(' ', '_')
  └── 替换body中 src="../images/xxx" → src="/images/xxx"
```

#### 3.6.2 为什么绝对路径

部署后页面在 /research/xxx.html，../images/ 解析到 /images/。
但如果未来有多层目录（/analysis/sub/），../images/ 不一致。
统一用 /images/ 绝对路径，任何目录层级都能正确引用。

---

## 4. CLI 入口（deploy.py）

| 命令 | 对应函数 | 说明 |
|------|----------|------|
| deploy | full_deploy() | 一键：produce → lint → 部署 → 验证 |
| produce | produce() | 生成到 dist（含 lint） |
| publish | publish() | 部署到 CF |
| add | add_to_index() | 外部页面入索引 |
| remove | remove_from_index() + rebuild + publish | 删除+重建+部署 |
| rebuild_index | rebuild_index() | 重建索引+首页 |
| update | update_pages() | 重新包裹所有页面 |
| verify | verify_deployment() | 输出验证清单 |
| check | check_config() | 配置完整性检查 |

---

## 5. 数据结构

### 5.1 index.json

```json
{
  "site": { "name": "雪地", "baseUrl": "https://xue.mei.pub" },
  "pages": [
    {
      "filename": "2026-06-04-jinniu-ai-report.html",
      "title": "金牛自运营服务商AI提效建设思路",
      "desc": "描述文本",
      "date": "2026-06-04",
      "category": "research",
      "url": "/research/2026-06-04-jinniu-ai-report.html",
      "external": true  // 可选，外部页面标记
    }
  ]
}
```

### 5.2 page_info（produce/update_pages 传递给 page.py）

```json
{
  "title": "标题",
  "desc": "描述",
  "date": "2026-06-17",
  "category": "research",
  "body": "<div>...</div>",  // lint修复后的HTML
  "style": "CSS内容"         // 提取的<style>内容
}
```

---

## 6. 分类体系

| key | 名称 | 说明 |
|-----|------|------|
| research | 深度研究 | 系统性调研 |
| analysis | 数据分析 | 数据驱动洞察 |
| summary | 内容摘要 | 信息提炼 |
| comparison | 对比评测 | 横向对比 |
| tutorial | 教程指南 | 操作指南 |
| project | 项目作品 | 互动作品 |
| other | 其他 | 游戏/工具/测试 |

新分类：英文标识 + 中文名称，在 config.py CATEGORIES dict 注册。

---

## 7. 安全说明

- CLOUDFLARE_API_TOKEN 通过 TOOLS.md 配置，建议最小权限（仅 Pages 编辑）
- 外部工具：uv（Python执行）+ npx/wrangler（CF部署）
- ScriptSafety 规则自动移除 document.cookie/localStorage/eval 等危险内容
- 索引原子写入（tmp → rename）防止部分写入
- Path traversal 检查：category 不允许含 / \ .