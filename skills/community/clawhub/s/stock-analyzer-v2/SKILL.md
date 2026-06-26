---
name: stock-analyzer
description: A股/港股实时行情查询、基本面分析、深度报告生成与邮件发送一体化工具。触发场景：(1) 用户询问股票价格、市值、PE/PB等数据；(2) 用户要求分析某只或多只股票；(3) 用户要求生成股票分析报告；(4) 用户要求通过邮件发送股票报告。支持AkShare实时行情、聚宽基本面数据、QQ邮箱/Gmail发送。
---

# Stock Analyzer - 股票深度分析工具

> ⚠️ **安全提示**：本 skill 不在任何文件中硬编码密码、授权码或私人账号信息。所有凭证均通过环境变量或运行时配置传入，绝不写入代码或文档。

## 快速开始

### 1. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 2. 配置聚宽账号（可选，用于基本面数据）

**通过环境变量配置**（推荐，安全）：
```bash
export JQDATA_PHONE="你的手机号"
export JQDATA_PASSWORD="你的密码"
```

或使用 `jq_login.py` 交互式配置：
```bash
python scripts/jq_login.py
```

### 3. 查询实时行情

```python
python scripts/stock_query.py --codes 03690.HK,300413.SZ,300251.SZ
```

返回：股价、涨跌幅、成交量、成交额

### 4. 获取基本面数据（需配置聚宽）

```python
python scripts/stock_fundamentals.py --codes 300413.SZ,300251.SZ
```

返回：PE、PB、市值、ROE、营收增长率等

### 5. 生成分析报告

```python
python scripts/generate_report.py --codes 03690.HK,300413.SZ --output report.md
```

### 6. 发送邮件（需配置邮箱授权码）

**通过环境变量配置**：
```bash
export QQ_EMAIL_AUTH_CODE="your_auth_code"
export GMAIL_APP_PASSWORD="your_app_password"
```

发送：
```python
python scripts/send_email.py --to 收件人邮箱 --file report.md --auth-code "$QQ_EMAIL_AUTH_CODE"
```

## 工作流程

```
用户请求 → 解析股票代码 → 获取实时行情 → 获取基本面 → 深度分析 → 生成报告 → 发送邮件
```

## 凭证管理规范

| 凭证 | 推荐配置方式 | 说明 |
|------|------------|------|
| 聚宽账号 | `JQDATA_PHONE` + `JQDATA_PASSWORD` 环境变量 | 免费注册 joinquant.com |
| QQ邮箱授权码 | `QQ_EMAIL_AUTH_CODE` 环境变量 | QQ邮箱设置 → 账户 → POP3/IMAP → 生成授权码 |
| Gmail应用密码 | `GMAIL_APP_PASSWORD` 环境变量 | Google账户 → 安全 → 应用密码 |

> ⚠️ **禁止**：将任何真实密码、授权码、手机号写入代码、文档或示例中。

## 股票代码格式

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| 港股 | `XXXXX.HK` | `03690.HK`（美团） |
| A股深交所 | `XXXXXX.SZ` | `300413.SZ`（芒果超媒） |
| A股上交所 | `XXXXXX.SH` | `600519.SH`（贵州茅台） |

> 💡 常见股票代码见 `references/stock_codes.md`

## 依赖说明

### AkShare（实时行情，无需账号）
- A股实时：`ak.stock_zh_a_spot_em()`
- 港股实时：`ak.stock_hk_spot_em()`
- 完全免费，但需注意并发限制

### 聚宽 JQData（基本面数据，需注册）
- 注册地址：https://www.joinquant.com
- 免费版有数据范围和日期权限限制
- 使用前请先阅读聚宽积分说明

## 文件说明

### scripts/
- `stock_query.py` - 实时行情查询（AkShare，无需账号）
- `stock_fundamentals.py` - 基本面数据获取（聚宽，需配置）
- `generate_report.py` - 报告生成
- `send_email.py` - 邮件发送
- `jq_login.py` - 聚宽账号配置（交互式，安全存储）
- `requirements.txt` - 依赖清单

### references/
- `report_template.md` - 报告模板
- `stock_codes.md` - 常用股票代码对照表

## 使用示例

**示例1：查询美团股价**
```
用户：帮我查一下美团的股价
→ python scripts/stock_query.py --codes 03690.HK
→ 返回：美团(03690.HK) HK$80.70 (-1.41%)
```

**示例2：分析多只股票**
```
用户：分析一下美团、芒果超媒、光线传媒
→ python scripts/stock_query.py 获取行情
→ python scripts/stock_fundamentals.py 获取基本面
→ python scripts/generate_report.py 生成报告
```

**示例3：发送报告到邮箱**
```
用户：把报告发到我邮箱
→ python scripts/send_email.py --to 收件人邮箱 --file report.md --auth-code "$QQ_EMAIL_AUTH_CODE"
```

## 常见问题

### Q: AkShare 获取数据失败？
- 网络问题：检查代理设置
- 并发限制：逐个查询而非批量
- 数据源维护：稍后重试

### Q: 聚宽登录失败？
- 检查手机号/密码是否正确
- 账号是否过期（免费版1年有效期）
- 是否有港股数据权限

### Q: 邮件发送失败？
- `Login denied`：授权码错误，请重新生成
- `Connection closed`：尝试 465 SSL 端口
- `SMTPAuthenticationError`：确认已开启 SMTP 服务
