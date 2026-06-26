# 📧 邮件 IMAP 集成 - 配置完成

## ✅ 配置状态

| 项目 | 状态 | 详情 |
|------|------|------|
| **邮箱账号** | ✅ 已配置 | `sale-9@farreach-electronic.com` |
| **IMAP 服务器** | ✅ 已连接 | `imaphz.qiye.163.com:993` (SSL) |
| **SMTP 服务器** | ✅ 已配置 | `smtphz.qiye.163.com:465` (SSL) |
| **邮件总数** | ✅ 1835 封 | 当前未读：0 |
| **OKKI 集成** | ✅ 已启用 | 向量检索 LanceDB |
| **邮件归档** | ✅ 已启用 | `/Users/wilson/.openclaw/workspace/mail-archive/` |

---

## 📁 目录结构

```
/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/
├── .env                    # 邮箱配置（敏感信息）
├── auto-capture.js         # 自动捕获脚本 ⭐
├── test-read.js            # 测试读取脚本
├── scripts/
│   ├── imap.js             # IMAP CLI 工具
│   └── smtp.js             # SMTP CLI 工具
└── INTEGRATION.md          # 本文档
```

---

## 🚀 使用方法

### 1️⃣ 检查并处理新邮件

```bash
cd /Users/wilson/.openclaw/workspace/skills/imap-smtp-email

# 检查最新 10 封邮件（自动关联 OKKI 客户）
node auto-capture.js check 10

# 只检查未读邮件
node auto-capture.js check --unseen

# 处理所有邮件（谨慎使用！）
node auto-capture.js check --all
```

### 2️⃣ 使用原生 IMAP CLI

```bash
# 查看邮箱目录
node scripts/imap.js list-mailboxes

# 检查最新邮件
node scripts/imap.js check --limit 10

# 搜索邮件
node scripts/imap.js search --from "customer@example.com" --limit 5
node scripts/imap.js search --subject "询价" --limit 10
node scripts/imap.js search --unseen --limit 20

# 获取完整邮件内容
node scripts/imap.js fetch <UID>

# 下载附件
node scripts/imap.js download <UID> --dir ./attachments

# 标记为已读/未读
node scripts/imap.js mark-read <UID1> <UID2>
node scripts/imap.js mark-unread <UID>
```

### 3️⃣ 发送邮件

**⚠️ 重要原则：禁止直接照抄模板！**

**模板仅作为结构参考，每次发送前必须根据收件人信息生成个性化正文内容。**

**错误示例（禁止）：**
- ❌ 直接发送 `development-email.html` 给所有客户（内容写死了 "Paul and QUADNET Team"）
- ❌ 模板里的客户名、地点、行业信息不修改就发送
- ❌ 发送给意大利客户但内容提到 "Queensland, Australia"

**正确做法：**
- ✅ 模板只参考结构（问候 → 寒暄 → 公司介绍 → 附件说明 → 行动号召 → 签名）
- ✅ 根据客户信息（公司名、国家、行业）生成个性化寒暄内容
- ✅ 使用动态生成的 HTML 文件或 `--body` 参数发送定制内容

---

**⭐ 发送前检查清单（必读！）**

在发送开发信/报价单邮件前，**必须**按顺序检查以下内容，确保一次性发送完整邮件：

```markdown
1. [ ] **收集客户信息**（从 OKKI 或其他来源）⭐
   - 公司名称
   - 国家/地区
   - 行业/业务类型
   - 联系人姓名（如有）
   - 邮箱地址

2. [ ] **生成个性化邮件正文** ⭐
   - 根据客户信息定制寒暄内容（提及客户所在地/行业）
   - 调整语气和重点（不同市场关注点不同）
   - 生成 HTML 文件或准备 `--body` 内容
   - **禁止直接照抄模板中的特定客户信息**

3. [ ] 确认产品目录存在
   - 检查：`/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf`
   - 路径包含空格，命令中需要用引号包裹

4. [ ] **生成专属报价单** ⭐⭐⭐（禁止使用示例文件）
   - **原则：** 每次开发信必须生成新的专属报价单，禁止使用示例文件
   - **步骤：**
     ```bash
     # 1. 创建客户专属数据文件
     # 位置：/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/<客户简称>.json
     # 内容：客户公司名、地址、产品列表、价格
     
     # 2. 调用报价单生成 skill
     cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow
     bash scripts/generate-all.sh data/<客户数据>.json QT-<日期>-<客户简称>
     
     # 3. 确认生成的 PDF 文件
     ls data/QT-*.pdf
     ```
   - **重要：** 邮件附件必须使用 HTML 转换的 PDF（`*-HTML.pdf` 或 `*-Final.pdf`）
     - ✅ HTML 转换的 PDF = 邮件附件（现代设计，专业美观）
     - ⚠️ Excel 转换的 PDF = 内部存档（仅用于内部，不发送客户）
   - **禁止：** ❌ 不要使用 `examples/` 目录的示例报价单发送给客户

5. [ ] 确认所有附件路径正确且文件可读
   ```bash
   ls -la "/path/to/catalogue.pdf"
   ls -la "/path/to/quotation.pdf"
   ```

6. [ ] 一次性发送完整邮件（正文 + 目录 + 报价单）
```

**常见错误：**
- ❌ 看到 `output/` 目录不存在就默认"没有报价单"（`examples/` 目录可能有现成的）
- ❌ 没有做完整检查就发送，导致分多次发送碎片邮件
- ❌ 附件路径包含空格未用引号包裹
- ❌ **直接照抄模板内容，不根据客户信息定制（严重错误！）**
- ❌ **使用示例报价单而非生成专属报价单（严重错误！）** - 示例文件仅用于测试，绝对不能发送给客户

```bash
# 简单文本邮件
node scripts/smtp.js send --to "customer@example.com" --subject "回复询价" --body "您好..."

# HTML 格式邮件（推荐⭐，支持格式化）
node scripts/smtp.js send --to "customer@example.com" --subject "产品报价" --html --body "<h1>报价单</h1><p>详见附件...</p>"

# 带附件（单个）
node scripts/smtp.js send --to "customer@example.com" --subject "产品目录" --body "请查收" --attach "/path/to/file.pdf"

# 带附件（多个⭐，逗号分隔，不要重复 --attach）
node scripts/smtp.js send --to "customer@example.com" --subject "报价单" --html --body "..." --attach "/path/to/file1.pdf,/path/to/file2.pdf"

# 从文件读取正文
node scripts/smtp.js send --to "customer@example.com" --subject "报价单" --body-file email.txt --attach "file1.pdf,file2.pdf"
```

---

## ⚠️ 常见错误与正确用法（必读！）

### ❌ 错误 1：多个附件重复使用 `--attach`

```bash
# 错误！只会发送最后一个附件
node scripts/smtp.js send --to "..." --attach "file1.pdf" --attach "file2.pdf"
```

**原因：** 命令行参数解析会覆盖重复参数，只保留最后一个值。

**✅ 正确用法：** 用逗号分隔多个文件路径

```bash
# 正确！两个附件都会发送
node scripts/smtp.js send --to "..." --attach "file1.pdf,file2.pdf"
```

---

### ❌ 错误 2：用 `--body` 发送 Markdown 格式内容

```bash
# 错误！Markdown 不会渲染，收件人会看到原始符号
node scripts/smtp.js send --to "..." --body "**标题**\n- 列表项 1\n- 列表项 2"
```

**原因：** `--body` 发送的是纯文本（text/plain），Markdown 语法不会被渲染。

**✅ 正确用法：** 用 `--html` 发送 HTML 格式邮件

```bash
# 正确！HTML 会正确渲染格式
node scripts/smtp.js send --to "..." --html --body "<h2>标题</h2><ul><li>列表项 1</li><li>列表项 2</li></ul>"
```

---

### 📋 邮件格式对比

| 参数 | 格式 | 适用场景 |
|------|------|----------|
| `--body` | 纯文本 (text/plain) | 简单通知、无格式内容 |
| `--html` | HTML (text/html) | 正式邮件、报价单、开发信（推荐⭐） |
| `--body-file` | 从文件读取 | 长邮件、模板邮件 |

---

### 📧 完整示例（开发信模板）

#### 模板 1：简单 HTML 开发信

```bash
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Professional Cabling Solutions - Product Catalog & Quotation" \
  --html \
  --body "<html><body><p>Dear Customer,</p><p>My name is Wilson from <strong>Farreach Electronic</strong>...</p><h3>Our Core Products:</h3><ul><li>HDMI 2.1 Cables (8K@60Hz, 48Gbps)</li><li>DisplayPort 2.1 Cables (UHBR20, 80Gbps)</li><li>USB-C Cables (USB 4.0, 80Gbps, 240W PD)</li></ul><p>Best regards,<br/>Wilson</p></body></html>" \
  --attach "/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/QT-20260315-001.pdf,/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf"
```

#### 模板 2：从文件读取正文（推荐⭐）

```bash
node scripts/smtp.js send \
  --to "paul@quadnet.com.au" \
  --cc "syed@quadnet.com.au,sales@quadnet.com.au" \
  --subject "🔌 Great to Reconnect - Farreach Electronic Cable Solutions" \
  --html \
  --body-file "/Users/wilson/.openclaw/workspace/mail-attachments/quadnet_development_email.html" \
  --attach "/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf,/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/QT-20260314-009-Farreach-Final.pdf"
```

#### 模板 3：久未联系客户开发信（结构参考）

**邮件结构：**
1. **问候 + 寒暄** - "Hope this email finds you well! It's been a while..."
2. **提及客户所在地/业务** - 显示你了解他们
3. **介绍公司新动态** - 产能扩张、新认证、新产品
4. **说明附件内容** - Catalogue + Quotation
5. **行动号召** - "If you have any upcoming projects..."
6. **签名** - 公司名称 + 联系方式 + 核心优势

**关键信息（Farreach 卖点）：**
- 🏭 18 年经验 | HDMI 认证会员 | ISO9001
- 🌏 中越双基地（珠海 2006 + 越南 2019, 10,000㎡, 420 人）
- 📦 月产能 80 万件 +
- ⚡ 标准品 7-15 天交期
- 💰 MOQ 500 pcs（可协商）

**产品亮点：**
- HDMI 2.1: 8K@60Hz, 48Gbps
- DP 2.1: UHBR20, 80Gbps, 16K@60Hz
- USB-C: USB 4.0, 80Gbps, 240W PD
- LAN: CAT6A 10Gbps, CAT8 40Gbps, PoE++

**附件规范：**
- ✅ Catalogue: `/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf`
- ✅ Quotation: `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/QT-*.pdf`

---

### 📝 开发信 HTML 模板文件

**位置：** `/Users/wilson/.openclaw/workspace/mail-templates/development-email.html`

**使用方法：**
```bash
# 1. 复制模板
cp /Users/wilson/.openclaw/workspace/mail-templates/development-email.html \
   /Users/wilson/.openclaw/workspace/mail-attachments/customer_email.html

# 2. 编辑客户信息（公司名称、联系人、所在地等）

# 3. 发送
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "🔌 Great to Reconnect - Farreach Electronic" \
  --html \
  --body-file "/Users/wilson/.openclaw/workspace/mail-attachments/customer_email.html" \
  --attach "/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf,/Users/wilson/.openclaw/workspace/skills/quotation-workflow/output/QT-xxx.pdf"
```

---

### 🔧 调试技巧

```bash
# 先测试 SMTP 连接
node scripts/smtp.js test

# 发送测试邮件到自己邮箱
node scripts/smtp.js send --to "sale-9@farreach-electronic.com" --subject "Test" --html --body "<h1>Test Email</h1><p>Format check.</p>"

# 检查附件路径是否正确
ls -lh /path/to/attachment.pdf

# 如果 DNS 解析超时，稍后重试（网络波动）
```

---

## 📂 邮件归档

邮件自动保存到：
```
/Users/wilson/.openclaw/workspace/mail-archive/
├── 2026-03-09/
│   ├── 2026-03-09_13-57-25_邮件主题.md
│   └── ...
└── 2026-03-10/
    └── ...
```

每封邮件包含：
- ✅ 发件人、收件人、日期、主题
- ✅ 邮件正文（纯文本）
- ✅ OKKI 客户匹配信息（如有）
- ✅ 附件列表
- ✅ Obsidian 兼容的 Markdown 格式

---

## 🎯 OKKI 客户关联

自动捕获系统会：

1. **提取发件人信息**
   - 邮箱地址
   - 公司名称
   - 邮箱域名

2. **向量检索匹配**
   - 使用 LanceDB 向量搜索
   - 支持域名匹配
   - 支持公司名匹配

3. **归档时附加客户信息**
   - 匹配成功 → 附加 OKKI 客户档案
   - 匹配失败 → 标记为新客户线索

---

## ⚙️ 高级配置

### 环境变量（.env）

```bash
# IMAP 配置
IMAP_HOST=imaphz.qiye.163.com
IMAP_PORT=993
IMAP_USER=sale-9@farreach-electronic.com
IMAP_PASS=<授权码>
IMAP_TLS=true

# SMTP 配置
SMTP_HOST=smtphz.qiye.163.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=sale-9@farreach-electronic.com
SMTP_PASS=<授权码>

# 输出目录
MAIL_OUTPUT_DIR=/Users/wilson/.openclaw/workspace/mail-archive

# OKKI 工具路径
OKKI_CLI_PATH=/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_cli.py
VECTOR_SEARCH_PATH=/Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py
```

### 定时任务（Cron）

```bash
# 每 30 分钟检查一次新邮件
*/30 * * * * cd /Users/wilson/.openclaw/workspace/skills/imap-smtp-email && node auto-capture.js check --unseen >> /tmp/mail-capture.log 2>&1
```

---

## 🔐 安全提示

1. **授权码** 已保存在 `.env` 文件中，请勿提交到 Git
2. `.env` 已添加到 `.gitignore`
3. 建议定期更换授权码
4. 邮件归档目录建议设置适当的访问权限

---

## 📊 网易企业邮服务器信息

| 服务 | 服务器地址 | 端口 | SSL |
|------|-----------|------|-----|
| **IMAP** | `imaphz.qiye.163.com` | 993 | ✅ |
| **SMTP** | `smtphz.qiye.163.com` | 465 | ✅ |
| **POP3** | `pop3hz.qiye.163.com` | 995 | ✅ |

> 💡 如果连接失败，可尝试不带区域前缀的服务器：
> - `imap.qiye.163.com`
> - `smtp.qiye.163.com`

---

## 🧪 测试命令

```bash
# 测试 IMAP 连接
node auto-capture.js test

# 测试 OKKI 向量搜索
python3 /Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py search "客户名称"

# 测试 SMTP 发送
node scripts/smtp.js test
```

---

## 📝 待办事项

- [ ] 设置定时任务（Cron）自动检查邮件
- [ ] 配置邮件过滤规则（特定发件人/关键词）
- [ ] 附件自动下载和保存
- [ ] 邮件自动分类标签
- [ ] 与 Obsidian 深度集成（双向链接）

---

## 🆘 故障排除

### 连接失败
```bash
# 检查网络
ping imaphz.qiye.163.com

# 检查端口
telnet imaphz.qiye.163.com 993

# 查看错误日志
node auto-capture.js check 2>&1 | tee /tmp/mail-error.log
```

### 登录失败
- 确认授权码是否正确
- 确认邮箱已开启 IMAP/SMTP 服务
- 联系邮箱管理员检查账户状态

### OKKI 搜索失败
```bash
# 测试向量搜索
python3 /Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py search "测试"

# 检查索引
python3 /Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py import
```

---

---

## 📝 教训与反思

### 教训 1：报价单遗漏 (2026-03-15)
**事件：** 发送开发信时只附了产品目录，没有附报价单。  
**原因：** 没有检查 `examples/` 目录已有现成报价单。  
**改进：** 发送前检查清单明确要求检查 `output/` **和** `examples/` 两个目录。

### 教训 2：直接照抄模板内容 (2026-03-15) ⭐
**事件：** 模板内容包含其他客户信息（"Paul and QUADNET Team", "Queensland"）直接发送给意大利客户。  
**原因：** 把模板当成成品，没有根据客户信息定制内容。  
**改进：** 明确"模板只参考结构，内容必须定制"原则，添加个性化内容生成指南。

### 教训 3：碎片化发送 (2026-03-15)
**事件：** 先发只有目录的邮件，后补发带报价单的邮件。  
**原因：** 没有做完整检查就发送。  
**改进：** 强调"一次性发送完整邮件"原则。

### 教训 4：使用示例报价单而非生成专属报价单 (2026-03-15) ⭐⭐⭐
**事件：** 给美国客户 SPECIALIZED COMPUTER PRODUCTS USA 发送开发信时，直接使用了 `examples/QT-TEST-001-Final.pdf` 示例文件，而不是为客户生成专属报价单。

**问题严重性：**
- 报价单上没有客户公司名称和地址
- 产品列表不是针对客户需求定制的
- 显得不专业，像群发垃圾邮件
- 客户无法用这份报价单做内部采购申请

**正确流程（必须遵守）：**
```markdown
1. 收集客户信息（公司名、地址、行业、联系人）
2. 创建报价单数据文件（JSON 格式）
   位置：/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/<客户简称>.json
3. 调用报价单生成 skill
   bash scripts/generate-all.sh data/<客户数据>.json QT-<日期>-<客户简称>
4. 确认生成的 PDF 文件（*-Final.pdf 或 *-HTML.pdf）
5. 发送邮件时附上这份专属报价单
```

**原则：**
> **每次开发信必须生成新的专属报价单，禁止使用示例文件。**  
> 示例文件仅用于测试和演示，绝对不能发送给真实客户。

**记忆口诀：**
```
开发信三件套：个性化正文 + 产品目录 + 专属报价单 ⭐
示例文件 = 测试用，禁止发给客户 ❌
```

---

**配置完成时间：** 2026-03-09 13:57  
**配置者：** Wilson (AI Assistant)  
**邮箱服务商：** 网易企业邮 (qiye.163.com)  
**最后更新：** 2026-03-15 02:50（添加教训 4）
