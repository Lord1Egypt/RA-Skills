# 企业接入指南

本文档说明如何将财税合规全链路Skill接入您的企业系统。

---

## 一、接入前准备

### 1.1 环境要求

| 要求项 | 说明 |
|--------|------|
| 操作系统 | Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+) |
| Python | 3.8 或更高版本 |
| Tesseract | 5.x 版本，需安装中文语言包 |
| 磁盘空间 | 至少 500MB（含Tesseract语言数据） |
| 内存 | 建议 4GB 以上 |

### 1.2 安装步骤

详见 `scripts/install_tesseract.sh`（Linux/macOS）或 `scripts/install_tesseract.ps1`（Windows）。

---

## 二、企业自主配置

### 2.1 配置文件结构

 Skill不提供任何默认密钥，所有配置由企业自主填写：

```yaml
# config.yaml

# ==================== 查验引擎配置 ====================
verify_engine: "tax_bureau"
# 可选值:
# - "tax_bureau": 国税总局查验平台（免费，无需API Key）
# - "bairong": 百望云API（需企业自行申请）
# - "nuonuo": 诺诺发票API（需企业自行申请）
# - "custom": 企业自建接口（需提供接口地址）
# - "none": 不启用查验功能

# ==================== 审批平台配置 ====================
approval:
  platform: "none"
  # 可选值:
  # - "dingtalk": 钉钉审批
  # - "wecom": 企业微信审批
  # - "feishu": 飞书审批
  # - "custom": 企业自建审批系统
  # - "none": 不启用审批对接
```

### 2.2 引擎配置详解

#### 国税总局查验平台（推荐免费方案）

```yaml
verify_engine: "tax_bureau"
```

优点：
- 完全免费
- 官方权威数据
- 无需申请API Key

缺点：
- 需要手动访问网站查验
- Skill提供链接跳转，企业自行操作

#### 百望云API

```yaml
verify_engine: "bairong"

bairong:
  api_key: "在此填写您的百望云API Key"
  api_secret: "在此填写您的百望云Secret"
```

申请步骤：
1. 访问 https://www.bairong.com
2. 注册企业账号
3. 申请API接入权限
4. 获取API Key和Secret

#### 钉钉审批

```yaml
approval:
  platform: "dingtalk"
  
  dingtalk:
    app_key: "应用的AppKey"
    app_secret: "应用的AppSecret"
    process_code: "审批流程编码"
```

申请步骤：
1. 登录 https://open.duxiaoman.com
2. 创建企业内部应用
3. 开通审批权限
4. 获取AppKey和AppSecret
5. 创建审批流程并获取编码

---

## 三、报销单模板配置

### 3.1 模板要求

- 格式：Excel (.xlsx)
- 第一行为表头（字段名）
- 使用中文字段名
- 支持多Sheet，但仅识别第一个

### 3.2 字段映射

首次使用时，Skill自动识别字段映射关系：

```yaml
template:
  path: "您的报销单模板.xlsx"
  field_mapping:
    invoice_date: "开票日期"      # 发票字段 → 模板列名
    seller_name: "销方名称"
    amount: "金额（不含税）"
    tax_amount: "税额"
    total: "价税合计"
    remark: "费用说明"
```

企业可手动调整映射关系，后续自动学习保存。

---

## 四、安全配置

### 4.1 API密钥管理

| 密钥类型 | 存储方式 | 安全等级 |
|----------|----------|----------|
| 配置文件 | config.yaml | ⚠️ 中等（建议设置文件权限） |
| 环境变量 | INVOICE_API_KEY 等 | ✅ 推荐 |
| 密钥管理系统 | AWS KMS / Azure Key Vault | ✅✅ 高安全 |

**推荐做法**：

```bash
# macOS/Linux（在 ~/.bashrc 或 ~/.zshrc 中）
export INVOICE_OCR_KEY="your-key-here"

# Windows（PowerShell）
$env:INVOICE_OCR_KEY="your-key-here"
```

### 4.2 数据安全策略

建议企业配置：

| 策略项 | 建议值 |
|--------|--------|
| 临时文件清理 | 每次操作后自动清理 |
| 日志保留期限 | 30天 |
| API密钥轮换 | 每90天 |
| 访问控制 | 仅财务人员可执行 |
| 数据备份 | 仅备份映射配置，不备份发票图片 |

---

## 五、运维与监控

### 5.1 日常操作

```bash
# 日常识别
python scripts/ocr_engine.py --input /path/to/invoice.png --output /tmp/receipt.json

# 批量处理
python scripts/ocr_engine.py --input /path/to/invoices_dir/ --output /tmp/batch_results.json

# 模板填充
python scripts/template_matcher.py fill --config config.yaml --receipt /tmp/receipt.json --template templates/报销单.xlsx
```

### 5.2 监控要点

| 监控项 | 方法 |
|--------|------|
| Tesseract版本 | `tesseract --version` |
| API调用频率 | 查看日志文件 |
| 识别准确率 | 抽样对比人工结果 |
| 错误率 | 监控error.log |
| 磁盘空间 | 监控临时文件目录 |

---

## 六、常见问题

### Q1: Tesseract安装失败？
- 确认操作系统版本符合要求
- 确认下载了正确的语言包（chi_sim）
- Windows用户需将Tesseract路径加入系统PATH

### Q2: 识别准确率不高？
- 确保发票图片清晰（300DPI以上）
- 确保光线均匀、无反光
- 可尝试调整预处理参数
- 考虑升级Tesseract版本

### Q3: 查验接口返回失败？
- 检查API Key是否正确
- 检查网络是否可访问
- 检查是否超出调用频率限制

### Q4: 模板匹配不准确？
- 确认模板第一行为表头
- 确认使用中文字段名
- 手动匹配后Skill会学习并记住

---

## 七、合规建议

1. **法规遵从**：确保发票管理符合《中华人民共和国发票管理办法》
2. **内部控制**：建立适当的审批流程，防止滥用
3. **审计追踪**：保留操作日志，便于内部审计
4. **定期审查**：定期检查API权限和使用情况
5. **员工培训**：确保操作人员了解财务合规要求

---

## 八、获取帮助

- GitHub Issues: 提交问题和建议
- SkillHub文档: https://skillhub.cn/docs
- 邮箱: 联系Skill开发者