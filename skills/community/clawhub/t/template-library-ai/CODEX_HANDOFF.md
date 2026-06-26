# TemplateBased-Writing — Codex 交接文档

> 用途：让 Codex 完全了解这个技能的代码、架构、服务器、支付、待修复问题，可以直接上手改。

---

## 一、项目定位

**templatebased-writing** 是一个 OpenClaw Skill，卖给最终用户 ¥0.99 终身买断。用户通过 AI（当前对话模型）按 5 步流程生成论文/PPT/简历等文档。依赖一个自建的后端 API 服务器 + 503 个内置模板。

**核心卖点**：自然语言直接出文档，无需安装软件。

---

## 二、本地文件结构

根目录：`C:\Users\90961\.openclaw\workspace\skills\templatebased-writing\`

```
templatebased-writing/
├── SKILL.md                  ← OpenClaw Skill 主流程文件（483 行）
├── _meta.json                ← 技能元数据（version: 2.0.0）
├── readme.md                 ← 对外 readme
├── .clawhub/
│   └── origin.json           ← ClawHub 发布记录（installedVersion: 1.0.0，需同步）
├── references/
│   ├── api.md                ← API 端点文档（106 行）
│   ├── pricing.md            ← 定价规则文档（190 行）
│   └── templates.md          ← 模板选择/流程话术指南（362 行）
└── scripts/
    ├── check_payment.py      ← 查付费状态脚本（193 行）
    ├── create_template.py    ← 本地创建 .docx 模板（963 行）
    ├── upload_template.py    ← 上传自有模板脚本（345 行）
    └── __pycache__/          ← Python 缓存（忽略）
```

### 各文件职责速览

| 文件 | 干什么 |
|------|--------|
| `SKILL.md` | AI 的执行流程手册，定义 Step 0→5 的每个操作步骤 |
| `references/api.md` | API 端点清单 + content 数据结构的 JSON 格式规范 |
| `references/pricing.md` | ¥0.99 买断定价、3 次免费额度、付费检查流程 |
| `references/templates.md` | 需求分析清单、模板推荐话术、场景流程指南 |
| `scripts/create_template.py` | 用户描述需求后，本地用 python-docx 生成 .docx（含{{}}占位符） |
| `scripts/upload_template.py` | 用户上传自有模板后，调后端 API 分析结构并返回占位符 |
| `scripts/check_payment.py` | 调后端 API 查 paid / free_uses_remaining |

---

## 三、后端服务器

### 基本信息

| 项目 | 值 |
|------|-----|
| 服务器 IP | `124.221.10.61` |
| Web Server | `nginx/1.18.0 (Ubuntu)` |
| 后端框架 | Flask / FastAPI（待确认，返回 JSON 格式为 `{"ok":true/false, "data":{...}}`） |
| API Base | `http://124.221.10.61/api/v1/` |
| 服务端语言 | Python |

### 已确认的 API 端点

| 方法 | 路径 | 认证 | 状态 | 说明 |
|------|------|:----:|:----:|------|
| GET | `/api/v1/templates` | 不需要 | ✅ 正常工作 | 返回全部 503 个模板 |
| GET | `/api/v1/templates/categories` | 可能需要Key | ✅ 存在 | 返回分类列表 |
| POST | `/api/v1/user/upload` | 需要API Key | ✅ 端点存在 | 上传自有模板 |
| GET | `/api/v1/key/balance` | 需要API Key | ✅ 端点存在 | 查付费状态 |
| POST | `/api/v1/key/create_api_key` | — | 未测试 | 创建 API Key |
| GET | `/api/v1/preview/<id>` | 不需要 | ⚠️ 地址是 127.0.0.1:3000 | 模板预览图 |
| GET | `/api/v1/check_environment` | — | ❌ 不存在 | SKILL.md Step 0 需要 |
| GET | `/api/v1/health` | — | ❌ 不存在 | |

### 模板数据示例

总模板数：**503 个**

分类分布（从 API 响应中解析的类别前缀）：

| 类别 | 数量级 |
|------|:------:|
| 简历（RES-G/RES-E/RES-4P/RES-A） | ~80 |
| PPT | ~200+ |
| 论文（THE-/BTH-） | ~50 |
| 实验报告（EXP-） | ~10 |
| 其他 | ~150 |

每个模板的数据结构：
```json
{
  "id": "THE-TSK-001",
  "name": "毕业论文任务书1",
  "category": "论文>任务书",
  "description": "毕业设计（论文）任务书模板，含课题名称、研究内容、进度安排",
  "price": 0.99,
  "is_premium": false,
  "is_preferred": false,
  "formats": ["image"],
  "preview": "http://127.0.0.1:3000/api/v1/preview/THE-TSK-001",
  "preview_text": "毕业设计（论文）任务书模板..."
}
```

### 需要新增的 API 端点

按 SKILL.md 和 api.md 定义，后端还需要实现以下端点：

1. **`/api/v1/check_environment`** 或 **`/api/v1/health`** — SKILL.md Step 0 的健康检查
2. **`/api/v1/user/upload`** (POST) — 已有框架，需确认完整实现
3. **`/api/v1/user/fill`** (POST) — **尚未测试**，填充内容到模板
4. **`/api/v1/templates/:id`** (GET) — 单模板详情
5. **`/api/v1/preview/:id`** (GET) — 预览图
6. **`/api/v1/templates/recommend`** (POST) — AI 智能推荐
7. **`/api/v1/templates/search`** (GET) — 搜索模板
8. **`/api/v1/pay/create`** (POST) — 支付订单创建
9. **`/api/v1/pay/test`** (POST) — 模拟支付（本地测试用）

---

## 四、支付接入（a2apay）

### 当前代码中的支付逻辑（在 api.md + pricing.md 中）

```
付费流程：
1. 用户免费额度用完 → 提醒付费
2. 用户同意 → 调 pay_for_download(template_id) 创建订单
3. 返回支付二维码/链接
4. 用户付款 → 调 test_pay_order(order_id) 模拟（本地测试）
5. 付费后 → key_balance() 返回 paid=true
```

### 实际支付接入（需要你补充细节）

你说接的是 **a2apay（a2a pay）**，这块当前代码里没有实现具体调用的细节。需要 Codex 改后端代码：

1. 创建订单时调 a2apay API 生成支付二维码
2. 用户扫码付款后 a2apay 回调通知
3. 支付成功 → 更新用户状态 → 后续所有操作免费

**当前缺失**：
- `pay_for_download()` 的实际后端实现
- `test_pay_order()` 的测试实现
- a2apay 回调 webhook
- 支付成功后的状态持久化

---

## 五、已知问题清单（需要 Codex 修复）

### 🔴 严重级别

| # | 问题 | 影响 |
|---|------|------|
| 1 | **`/api/v1/check_environment` 不存在** | SKILL.md Step 0 无法执行，AI 流程卡住 |
| 2 | **预览图 URL 指向 127.0.0.1:3000** | 用户看到的模板预览图打不开 |
| 3 | **后端缺用户管理** | 免费次数无法持久化，无法区分不同用户 |
| 4 | **缺少 API Key 生成/管理** | upload_template.py 和 check_payment.py 无法调用需要认证的接口 |

### 🟡 中等级别

| # | 问题 | 影响 |
|---|------|------|
| 5 | `check_payment.py` 中 `⚠️` 字符 → GBK 编码 crash | 中文 Windows 用户运行脚本报错 |
| 6 | `TEMPLATE_API_KEY` 环境变量未配置 | 本地无法测试认证链路 |
| 7 | `_meta.json` 版本 2.0.0 与 `origin.json` 的 1.0.0 不一致 | 发布混乱 |

### 🟢 低级别

| # | 问题 |
|---|------|
| 8 | PowerShell 中 `~` 路径展开问题（脚本调用示例需改为 `$env:USERPROFILE`） |
| 9 | 没有 CI/CD 或自动化测试 |
| 10 | SKILL.md 中的 "MCP 工具" 与实际 REST API 命名不统一 |

---

## 六、部署测试记录

### 已通过测试

- ✅ Python 3.13.13 环境就绪
- ✅ `python-docx` 1.2.0 已安装
- ✅ `create_template.py` 本地生成 .docx 正常（A4, 页边距, 封面, {{}}占位符 均正确）
- ✅ 后端 `124.221.10.61` 网络可达
- ✅ `/api/v1/templates` 返回 503 个模板数据完整

### 待测试（需要 API Key 或后端补充实现后）

- [ ] `check_payment.py` → 查付费状态
- [ ] `upload_template.py` → 上传自有模板
- [ ] `POST /api/v1/user/fill` → 填充内容
- [ ] 支付流程（a2apay 创建订单 → 支付 → 回调 → 状态更新）
- [ ] 预览图 URL 修正后是否能正常加载
- [ ] AI 走完整 5 步流程（Step 0→5）是否畅通

---

## 七、云服务器连接方式

```
服务器: 124.221.10.61 (Ubuntu)
Web: nginx/1.18.0 (反向代理到后端应用)
后端: Python 应用（端口推测为 3000，与 preview URL 一致）
```

目前没有 SSH 密钥信息。如果要部署修改后的代码，需要提供：
- SSH 用户名/密钥
- 后端代码的仓库地址或服务器上的源码路径
- nginx 配置文件位置（`/etc/nginx/sites-enabled/`）
- 后端应用启动方式（systemd? supervisor? pm2?）

---

## 八、代码核心数据流总结

```
用户说"帮我写论文"
    │
    ▼
AI 走 SKILL.md 流程
    │
    ├── Step 0: check_environment() → GET /api/v1/templates（替代方案）
    │
    ├── Step 1: 需求分析 → 列出信息清单
    │
    ├── Step 2: 选模板来源
    │   ├── A. 自有模板 → upload_template.py → POST /api/v1/user/upload
    │   │                    → 解析 analysis.structure → 提取 {{}} 占位符
    │   ├── B. 描述创建 → create_template.py → 本地生成 .docx
    │   └── C. 内置模板 → GET /api/v1/templates → 推荐→选模板→付费检查
    │
    ├── Step 3: 收集用户内容 → 覆盖所有 {{}} 占位符
    │
    ├── Step 4: 执行生成
    │   ├── A/B场景 → user_fill_document(session_id, content) → POST /api/v1/user/fill
    │   └── C场景   → generate_document(template_id, content)
    │
    └── Step 5: 交付文件路径给用户
```

---

## 九、给 Codex 的操作建议

1. **先修后端** —— 补全缺失的 API 端点（health, fill, pay, 用户状态）
2. **修正预览图 URL** —— 把 127.0.0.1:3000 改成 124.221.10.61
3. **接入 a2apay** —— 实现真实的支付流程
4. **实现用户管理** —— session_id / API Key / 免费次数持久化
5. **本地联调** —— 生成 API Key 配到环境变量，跑通所有 3 个 Python 脚本
6. **修复 GBK 编码问题** —— 替换脚本中的特殊 Unicode 字符
7. **统一版本号** —— `_meta.json` 和 `origin.json` 保持一致
8. **重新发布到 ClawHub** —— `openclaw skill publish`
