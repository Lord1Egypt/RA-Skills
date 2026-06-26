---
name: wework-financial-daily
description: 每日定时生成金融分析教学课件并推送至企业微信。使用场景：(1) 每天自动生成当日最新金融数据（BTC、AAPL 等）的教学课件，(2) 推送课件到指定企业微信账号，(3) 保存 HTML 课件到本地桌面，(4) 包含价格走势图表和趋势分析。支持通过环境变量配置企业微信 token 和接收人。
---

# 企业微信每日金融分析教学课件

本技能用于每日定时生成金融分析教学课件，并自动推送到企业微信。

## ⚙️ 配置环境变量

在运行脚本前，设置以下环境变量（**必填**）：

```bash
# 企业微信 API Token（必填，从你的企业微信管理后台获取）
export WEWORK_X_TOKEN="eyJhbGciOiJI..."

# 企业微信接收人账号（必填，你的企业微信用户 ID 或手机号）
export WEWORK_TO_USER="18018517752"
```

### 方式一：系统环境变量（推荐）

1. `Win + R` → 输入 `sysdm.cpl` → 回车
2. "高级" → "环境变量"
3. "系统变量" → "新建"：
   - 变量名：`WEWORK_X_TOKEN`，变量值：`你的完整 token`
   - 变量名：`WEWORK_TO_USER`，变量值：`你的企业微信账号`

### 方式二：直接修改脚本

编辑 `scripts/generate_and_send.py`，修改顶部配置：

```python
X_TOKEN = "你的完整 token"
TO_USER = "你的企业微信账号"
```

## 🚀 运行方式

### 手动运行

```powershell
cd C:\Users\wwwir\.openclaw\workspace\skills\wework-financial-daily
python scripts/generate_and_send.py
```

### 双击运行（推荐）

直接双击 `一键运行.bat` 即可手动执行一次。

### 定时任务（每天早上 9 点自动运行）

**方式一：PowerShell 脚本（管理员权限）**

1. 右键点击 `SetupTask.ps1`
2. 选择"以管理员身份运行"
3. 脚本会自动创建每天 9:00 运行的定时任务

**方式二：手动创建**

详见 `README-定时任务配置.md`

## 📊 输出内容

每次运行会生成：

1. **HTML 教学课件** - 保存到桌面，包含：
   - 当日 BTC/USDT 和 AAPL 最新数据（动态生成）
   - 30 天价格走势图表（含 MA5 均线）
   - **五大教学模块**（详见下方）
   - 风险提示与免责声明

2. **企业微信推送** - Markdown 格式教学消息，包含：
   - 标题：【技术分析教学日报】日期
   - 核心数据表格（价格、MA5/MA20、RSI14、趋势）
   - **五大教学模块精讲**（概念 + 今日应用）
   - 完整报告链接

### 📚 五大教学模块

| 模块 | 主题 | 内容 |
|------|------|------|
| 模块一 | MA 均线基础 | 金叉/死叉概念、MA5/MA20 含义、今日应用 |
| 模块二 | RSI 指标解读 | 超买/超卖区判断、4 个区间操作建议 |
| 模块三 | 趋势识别方法 | 多头/空头趋势判断三要素 |
| 模块四 | 支撑阻力位 | 画法技巧、突破确认规则、今日价位 |
| 模块五 | 风险管理 | 仓位控制、止损策略、风险提示 |

## 📦 依赖包

脚本会自动检查并安装以下 Python 包：

- `requests` - HTTP 请求
- `pandas` - 数据处理
- `matplotlib` - 图表绘制
- `numpy` - 数值计算

首次运行会自动安装，后续无需重复。

## 🔧 自定义数据源

当前使用模拟数据（基于日期种子，保证当日数据一致）。如需接入真实 API：

1. 修改 `scripts/generate_and_send.py` 中的 `generate_html_report()` 函数
2. 替换模拟数据为真实 API 调用（如 CoinGecko、Yahoo Finance、Alpha Vantage 等）
3. 添加相应的 API Key 到环境变量

## ❓ 故障排查

| 问题 | 解决方案 |
|------|----------|
| 推送失败 | 检查 `WEWORK_X_TOKEN` 是否正确，确认企业微信 API 地址有效 |
| 图表中文乱码 | 确保系统已安装中文字体（SimHei/Microsoft YaHei） |
| 依赖安装失败 | 手动运行 `pip install requests pandas matplotlib numpy -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| 任务不执行 | 检查任务计划程序中任务状态，确认"不管用户是否登录都要运行"已勾选 |

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/generate_and_send.py` | 主脚本 |
| `一键运行.bat` | 手动运行快捷方式 |
| `SetupTask.ps1` | 定时任务自动配置脚本 |
| `README-定时任务配置.md` | 详细配置指南 |
| `references/cron-setup.md` | OpenClaw Cron 配置 |
