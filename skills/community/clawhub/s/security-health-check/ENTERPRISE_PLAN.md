# 企业安全审计 Skill 升级方案

> 规划时间：2026-04-19  
> 基于现有版本：security-health-check v1.x（个人版）  
> 目标版本：Enterprise Security Audit v2.0

---

## 一、现有能力回顾

| 功能 | 技术栈 | 数据源 |
|------|--------|--------|
| 邮箱泄露检查 | HIBP API v3 | haveibeenpwned.com |
| 密码泄露检查 | HIBP k-匿名 API | 本地SHA1前缀查询 |
| 密码强度分析 | zxcvbn-style 本地计算 | 内置弱密码字典 |
| 安全评分报告 | 本地综合计算 | — |

**现有架构**：单文件 Python（~16KB），无状态，无日志，轻量级，适合个人。

---

## 二、功能扩展规格

### 2.1 钓鱼邮件识别（Phishing Detection）

**功能描述**  
通过 URL 安全分析 + 发件人域名信誉查询，判断邮件内容是否属于钓鱼攻击。支持批量导入.eml 文件或直接输入邮件 Header+Body。核心检测逻辑：域名年龄（注册 < 6 个月高风险）、相似域名识别（lookalike，如 g00gle.com）、已知的钓鱼域名黑名单（phishtank.com API）、URL 危险特征（短链接解包、IP 直连 URL、伪装的登录表单 URL）。输出：风险等级（安全/可疑/危险）+ 详细推理依据 + 处置建议。

**技术实现路径**
- `python-evalanche` / `phish tank API`（免费，查询已确认钓鱼域名）
- `whois` 库查询域名注册时间
- `tldextract` 识别根域名 + 注册商信息
- 自建 lookalike 域名相似度引擎（Levenshtein + 视觉混淆检测）
- 短链接解包：`unshorten-api` 或直接 HTTP HEAD 追踪重定向链

**API/库依赖**：phishtank (CSV), python-whois, tldextract, Levenshtein

---

### 2.2 密码策略审计（Password Policy Audit）

**功能描述**  
面向企业场景，审计 Active Directory / LDAP / SaaS 平台（钉钉、企业微信、飞书）的密码策略合规性。同时提供"弱密码模式扫描"——将所有历史泄露密码的规律提取为正则模式（如 `YYYYMMDD` 生日格式、`companyName+123` 命名法），用于检测企业内部是否存在系统性弱密码文化。输入：管理员提供的密码哈希列表（SM3/SHA256，不可逆）或密码策略配置文件。输出：策略合规评分（8 分项）+ 高危模式列表 + 改进建议。

**技术实现路径**
- 密码模式挖掘：基于历史泄露数据（HIBP 免费泄露列表），提取 top 1000 密码的规律正则化（用 `exrex` 生成退化字符串）
- AD 密码策略解析：`python-ldap` 读取组策略（GPO）
- 飞书/钉钉密码策略：通过企业管理员 API 查询（需 OAuth2 授权）
- 弱密码检测正则库：自建 `weak_patterns.json`，含中文互联网常见弱密码模式

**API/库依赖**：python-ldap（可选）、exrex、re（内置）

---

### 2.3 API Key / Token 泄露扫描（Secret Scanning）

**功能描述**  
扫描代码仓库、文档、配置文件中的硬编码凭证（API Key、Access Token、私钥、数据库连接字符串）。支持：GitHub 公开仓库扫描（通过 GitHub API + 正则匹配）、本地文件/目录扫描（支持 `.env`, `.json`, `.yaml`, `.py`, `.js` 等）、GitHub Secret Scanning API 集成（检测推送到仓库的凭证）。输出：泄露凭证清单（类型/位置/严重程度）+ 撤销建议 + 补救步骤。

**技术实现路径**
- 正则模式库：来自 `trufflehog` 项目开源规则（支持 300+ 凭证类型）
- GitHub API：遍历用户仓库 + 使用 Code Search API 搜索高风险路径
- 本地扫描：`python-regex` 批量匹配，支持多文件并行（`concurrent.futures`）
- GitHub Secret Scanning：调用 GitHub API `GET /repos/{owner}/{repo}/secret-scanning/alerts`

**API/库依赖**：trufflehog-regex（规则抽取）、PyGithub、python-regex、concurrent.futures（内置）

---

### 2.4 社会工程学风险评估（Social Engineering Risk Assessment）

**功能描述**  
评估企业员工在社工攻击下的脆弱程度。核心模块：OSINT 个人信息收集（基于输入邮箱，收集该员工在公开社交网络的黑客视角资料：LinkedIn 职位/部门/GitHub 代码提交记录/演讲PPT暴露的组织架构），输出"攻击面报告"——如果攻击者要对这个员工发起钓鱼，成功率有多高。同时提供模拟钓鱼测试工具（生成假钓鱼邮件模板，供安全团队内部演练）。注意：本功能严格限制在用户自己的企业资产范围内，禁止扫描他人。

**技术实现路径**
- LinkedIn/OSINT：`apify.linkedin-scraper` 或直接搜索引擎查询（Google Custom Search API）
- GitHub OSINT：GitHub API 查询用户的代码提交贡献图和组织信息
- 社工攻击面评分算法：基于公开信息量 × 凭证关联度 × 职位敏感度综合打分
- 模拟钓鱼生成：模板引擎（Jinja2），内置 5 种钓鱼场景模板

**API/库依赖**：PyGithub、Google Custom Search API（免费 tier: 100次/天）、apify（可选）、Jinja2

---

### 2.5 勒索软件 Preparedness 检查（Ransomware Readiness Assessment）

**功能描述**  
评估企业在遭受勒索软件攻击时的恢复能力。5 大检查维度：备份覆盖率（是否至少 3-2-1 备份：3份副本、2种介质、1份离线）、备份完整性（定期演练验证）、网络分段（关键资产是否与互联网隔离）、终端防护（EDR 安装率 + 病毒库更新率）、 Incident Response 计划（是否有成文的 IR 流程 + 联系人清单）。输出：Ransomware Readiness Score（RRS 0-100）+ 分维度雷达图 + Top 5 紧急修复项。

**技术实现路径**
- 问卷驱动评估：自动化问卷收集 20+ 关键安全控制项状态
- 云存储备份检查：调用 AWS S3 / 阿里云 OSS API 检查版本控制设置
- 网络分段检查：Nmap 扫描（需内网授权）或用户提供网络拓扑图
- EDR 覆盖率：SentinelOne/CrowdStrike API 查询（需企业授权）
- 报告生成：matplotlib 雷达图 + MarkDown 报告

**API/库依赖**：boto3（AWS）、aliyun-openapi-python-sdk（阿里云）、python-nmap（需安装nmap）、matplotlib

---

## 三、技术实现路径汇总

```
┌─────────────────────────────────────────────────────┐
│                  Enterprise Skill v2.0              │
├──────────┬──────────┬──────────┬──────────┬────────┤
│ Phase 1  │ Phase 2  │ Phase 2  │ Phase 3  │ Phase3 │
│ 钓鱼检测 │ 密码审计 │ API泄露  │ 社工评估 │ 勒索防御│
├──────────┴──────────┴──────────┴──────────┴────────┤
│                    共用基础设施                      │
│  • HIBP API（已有）  • 正则凭证库  • 报告生成器     │
│  • 企业上下文管理（多用户Session）                   │
│  • 飞书/企微 Webhook 通知                           │
└─────────────────────────────────────────────────────┘
```

---

## 四、定价建议

### 4.1 套餐设计

| 套餐 | 价格 | 目标用户 | 功能范围 |
|------|------|----------|----------|
| **Free** | ¥0 | 个人用户 | 邮箱泄露检查 + 密码强度分析（现有功能） |
| **Starter** | ¥999/年 | 小微企业（≤50人） | Free + 钓鱼邮件识别（每月50次）+ 密码策略基础审计 |
| **Professional** | ¥2,999/年 | 成长期企业（50-500人） | Starter + API Key泄露扫描（GitHub公开仓库）+ 社工风险评估（5人份）+ 勒索 Preparedness 基础版 |
| **Enterprise** | ¥4,999/年 | 大型企业（500人+） | Professional + 无限次扫描 + 多账号管理 + 全员社工评估 + 备份覆盖率API集成 + 专属报告 + Slack/企微告警推送 |

### 4.2 定价逻辑

- **Free 层**：留住用户，形成漏斗入口
- **¥999 Starter**：解决"我的员工会不会点钓鱼邮件"这个老板最痛的点
- **¥2,999 Professional**：安全合规需求（等保/ISO 27001 配套工具）
- **¥4,999 Enterprise**：CISO 采购清单，B2B 销售主力SKU

---

## 五、开发优先级（Phase 1/2/3）

### Phase 1（1-2个月，快速上线）
**目标**：在现有架构上最小化扩展，快速产生商业价值

| 功能 | 优先级 | 理由 |
|------|--------|------|
| 钓鱼邮件识别 | P0 | 用户感知最强，解决"这封邮件安不安全"的直接需求 |
| 密码策略审计 | P0 | 企业刚需，可直接用于现有员工密码整改 |

### Phase 2（3-4个月，能力深化）
**目标**：构建差异化竞争壁垒

| 功能 | 优先级 | 理由 |
|------|--------|------|
| API Key泄露扫描 | P1 | 开发者安全意识崛起，GitHub泄露事件频发 |
| 社会工程学风险评估 | P2 | 依赖OSINT，数据质量不稳定，推迟至Phase 2完善 |

### Phase 3（5-6个月，企业级完善）
**目标**：完整的企业安全运营体系

| 功能 | 优先级 | 理由 |
|------|--------|------|
| 勒索软件 Preparedness | P1 | 监管合规（等保2.0）驱动需求明确 |
| 完整社工评估 | P1 | Phase 2数据积累成熟后，评分模型更准确 |
| 企业级管理后台 | P0 | 多租户、报告导出、SSO集成 |

---

## 六、关键里程碑

```
Month 1: Phase 1 MVP
  - 钓鱼邮件识别（URL分析 + 黑名单）上线
  - 基础密码策略问卷审计上线

Month 3: Phase 2 扩展
  - API Key泄露扫描上线（GitHub集成）
  - 飞书文档 + 定价页上线

Month 6: Phase 3 企业版
  - 勒索 Preparedness 检查上线
  - 企业管理后台 + 多租户
  - 完整报告 + Webhook告警
```

---

## 七、风险与依赖

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| HIBP API 速率限制 | 免费版限制严格 | 提供 HIBP API Key 配置入口（用户自备） |
| OSINT 数据合规性 | 社工评估可能触碰隐私法规 | 明确仅扫描用户授权的自身资产，增加同意书 |
| GitHub API 配额 | 公开仓库扫描受限 | 企业GitHub Token可提升配额至5000次/小时 |
| 钓鱼检测误报 | 影响用户体验 | 提供"加入白名单"功能，允许人工复核 |
