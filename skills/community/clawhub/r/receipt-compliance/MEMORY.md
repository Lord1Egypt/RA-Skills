# MEMORY.md - receipt-compliance 修改记录

## 最近修改

### v4.1.0 (2026-08-05) - 风险预警 + 归档合规

#### 新增内容

**1. 风险预警引擎** (`scripts/risk_detector.py`)
- 连号检测：同一供应商连续开具 N 张连号发票
- 大额整数金额检测：金额达到阈值且为整数
- 频繁开票检测：短时间内同一供应商开具大量发票
- 品名异常检测：品名与供应商经营范围对照
- 进销项匹配分析：Jaccard 相似度计算
- 三级预警分级：提示/关注/严重
- 支持自定义检测配置

**2. 电子档案归档管理器** (`scripts/archive_manager.py`)
- 四性检测：真实性、完整性、可用性、安全性
- 归档包生成：ZIP 格式，含元数据/四性报告/原始文件/说明
- 元数据采集：自动提取 20+ 项元数据字段
- 归档目录索引：文本格式目录
- 批量处理：支持目录批量扫描

**3. 新增参考文档**
- `references\supplier_scope_rules.md`：企业经营范围对照表
- `references\risk_rules_config.yaml`：风险检测规则配置文件

**4. SKILL.md 更新**
- 新增模块 9（风险预警）和模块 10（归档管理）
- 新增「税务风险预警」章节和「电子档案合规归档」章节
- frontmatter version 升至 4.1.0
- 更新日志新增 v4.1.0 条目

---

### v4.0.0 (2026-08-01) - 全电发票 + 多票据 + 智能分类

#### 新增内容

**1. 多类型票据扩展（方向二）**
- `train_parser.py`：火车票 OCR 专用解析器，提取车次、日期、站点、座位等级，自动计算可抵扣进项税 9%
- `flight_parser.py`：飞机行程单解析器，提取航班号、日期、票价、燃油费、民航发展基金，计算可抵扣进项税 9%
- `taxi_parser.py`：出租车票解析器，提取车牌号、上下车时间、里程、金额，计算可抵扣进项税 3%
- `fixed_parser.py`：定额发票解析器，提取发票代码、号码、金额，不可抵扣进项税
- `toll_parser.py`：通行费票据解析器，提取入口/出口、日期、金额，高速按 3%、桥闸按 5% 计算可抵扣进项税
- `fiscal_parser.py`：财政票据解析器，提取缴款人、执收单位、金额，不可抵扣进项税

**2. 智能分类与自动入账（方向三）**
- `smart_classifier.py`：智能分类器，根据发票内容自动匹配会计科目（差旅费/办公费/招待费等），计算进项税额，生成凭证摘要
- `voucher_generator.py`：记账凭证生成器，支持用友 U8、金蝶 KIS、QuickBooks 导入格式
- `references/account_mapping.md`：会计科目对照表（企业会计制度）
- `references\expense_rules.md`：费用分类规则和进项税税率表

**3. 数据结构扩展**
- `unified_invoice.py` 扩展：新增 receipt_type 枚举、票据类型常量、进项税字段、费用归属字段、座位等级、车牌号等
- `invoice_detector.py` 扩展：新增 6 种票据类型的路由和关键词特征匹配

**4. SKILL.md 更新**
- 功能说明表新增模块 5-8
- 更新日志新增 v4.0.0 条目（表格行格式）
- frontmatter version 升至 4.0.0

---

### v3.7.0 (2026-07-22) - 全电发票深度适配

#### 新增内容

**1. 全电发票 XML 解析器** (`scripts/xml_parser.py`)
- 自研全电发票 XML Schema 解析器，使用 Python 标准库 `xml.etree.ElementTree`
- 支持 20 位全电发票号码、校验码、税务数字账户 ID 等特有字段提取
- 兼容多种 XML 命名空间和标签变体（如 `InvoiceNumber`/`Fphm`/`FPHM`）
- 日期格式自动标准化（支持 `YYYY年MM月DD日`、`YYYY-MM-DD`、`YYYYMMDD`）
- 金额字段安全转换（去除货币符号、千位分隔符）

**2. OFD 版式文件解析器** (`scripts/ofd_parser.py`)
- 双方案解析：优先使用 `ofdparser` 库，不可用时自研降级方案
- 降级方案：手动解析 OFD 文件结构（ZIP 格式），提取 XML 内容预览
- 提供转换工具推荐（数科阅读器、福昕 OFD）

**3. 票种自动识别模块** (`scripts/invoice_detector.py`)
- 根据文件扩展名（`.xml`/`.ofd`/`.pdf`/`.png` 等）自动判断票种
- 对 XML 文件读取内容特征进一步判断全电/传统
- 自动路由到对应解析器（传统 OCR / 全电 XML / 全电 OFD）

**4. 统一发票数据结构** (`scripts/unified_invoice.py`)
- 兼容传统发票和全电发票的字段映射
- 提供 `to_dict()`、`to_json()`、`validate()` 等标准接口
- 全电特有字段：`check_code`、`digital_account_id`、`specific_business_info`

**5. SKILL.md 更新**
- 新增「全电发票（数电票）」章节，说明支持的文件类型、特有字段、使用方式
- 新增版本更新提醒机制说明
- 新增联系信息 `njskills@agent.qq.com`
- frontmatter version 升至 `3.7.0`
- 更新日志新增 v3.7.0 条目

#### 对应死规则检查

| 规则 | 状态 |
|------|------|
| #4 禁止自动发布 | ✅ 未自动发布 |
| #5 输出完整目录 | ✅ 见下方 |
| #6 更新日志格式规范 | ✅ 动词开头，无评测字样 |
| #7 发布统一用 tongyifabu.ps1 | ✅ 未发布 |
| #8 更新日志源文件填写规范 | ✅ frontmatter version 不带引号 |
| #9 功能自研优先 | ✅ XML/OFD 解析器自研 |
| #10 性能优化 | ✅ 解析器轻量，无重计算 |
| #11 版本更新提醒 | ✅ SKILL.md 已添加 |
| #12 MD 联系信息 | ✅ njskills@agent.qq.com |
| #13 禁止文件类型 | ✅ 未引入禁止类型 |
| #14 三次自审 | ✅ 完成 |
| #15 沙箱模拟运行 | ✅ 完成 |

---

### v3.4.0 (2026-07-13) - 安全修复（腾讯云鼎实验室安全评估）

#### 修复内容

**1. 供应链风险修复**
- 移除 install_tesseract.ps1 中指向个人 Gitee 仓库的下载源（gitee.com/woaini0919/tesseract-ocr）
- 移除 check_env.py 中 Gitee 镜像推荐
- 替换为 winget/scoop 官方源和 GitHub 官方 Release 下载

**2. 审批链接修复**
- 将 approval_abstract.py 中 `apply_url` 从 `https://open.duxiaoman.com` 改为 `https://open-dev.dingtalk.com`
- 将 approval_abstract.py 中 `reference_url` 从 `https://open.duxiaoman.com/document` 改为 `https://open-dev.dingtalk.com/document`
- 将 api-endpoints.md 中钉钉网址从 `https://open.duxiaoman.com` 改为 `https://open-dev.dingtalk.com`
- 将 setup-guide.md 中钉钉登录地址从 `https://open.duxiaoman.com` 改为 `https://open-dev.dingtalk.com`
- 将 example-approval.md 中 `reference_url` 从 `https://open.duxiaoman.com/document` 改为 `https://open-dev.dingtalk.com/document`

**3. 命令执行风险修复**
- verify_engine.py 中 `subprocess.Popen` 移除 `shell=True`，改为 `['cmd', '/c', 'start', short_url]` 列表形式

#### 对应安全评估问题

| 评估发现问题 | 修复措施 |
|------------|---------|
| 审批接口链接指向无关第三方平台 | 全部替换为钉钉官方 open-dev.dingtalk.com |
| 从个人 Gitee 仓库下载二进制文件 | 移除 Gitee 个人镜像，替换为官方源 |
| 不受限的 shell 执行器 | 移除 shell=True，使用列表参数形式 |

---

### v3.3.0 (2026-07-13) - 更名

- 插件文件夹名从 `tax-receipt-compliance` 改为 `receipt-compliance`
- displayName 从 `财税合规全链路助手` 改为 `会计助手`
- description、标题同步更新为"会计助手"
