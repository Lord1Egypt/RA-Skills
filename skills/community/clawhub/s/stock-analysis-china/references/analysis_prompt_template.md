# A股持仓分析报告模板

## OCR 截图识别流程（跨平台）

当用户通过微信发送持仓截图时，按以下步骤处理：

**Step 1 — 获取截图**
微信截图自动保存至 `~/.qclaw/media/inbound/` 目录（跨平台），
文件名为 UUID 格式（如 `2d616508-04d6-44dd-ab45-ed8fe28bd8b9.jpg`）。

AI 读取最新文件：
```bash
# macOS / Linux
ls -t ~/.qclaw/media/inbound/ | head -1

# Windows (PowerShell)
Get-ChildItem "$env:USERPROFILE\.qclaw\media\inbound" -File | Sort-Object LastWriteTime -Descending | Select-Object Name
```

**Step 2 — 图像识别**
方案 A（推荐）：直接用 AI 多模态能力识别截图内容，无需 OCR 工具。
方案 B（备用）：使用 Tesseract OCR。

**Tesseract 安装（跨平台）：**

| 平台 | 安装命令 |
|------|---------|
| Windows | `winget install tesseract-ocr.tesseract` |
| macOS | `brew install tesseract` |
| Linux (Ubuntu/Debian) | `sudo apt-get install tesseract-ocr` |
| Linux (CentOS/RHEL) | `sudo yum install tesseract` |

**中文语言包安装：**

| 平台 | 方法 |
|------|------|
| Windows | 下载 `chi_sim.traineddata` 放入 `C:\Program Files\Tesseract-OCR\tessdata\` |
| macOS | `brew install tesseract-lang` 或手动下载放入 `/usr/local/share/tessdata/` |
| Linux | `sudo apt-get install tesseract-ocr-chi-sim` 或手动下载放入 `/usr/share/tesseract-ocr-4.00/tessdata/` |

**调用命令（跨平台）：**
```bash
tesseract <image_path> stdout --oem 1 --psm 6 -l chi_sim+eng
```

**Step 3 — 提取字段**
从识别结果中提取：
- 股票名称 / 股票代码（6位数字）
- 持仓数量（股数）
- 成本价
- 当前价（可选）
- 盈亏比例（可选）

**Step 4 — 调用持仓更新**
```bash
# 跨平台（自动推断 python3）
python3 <SKILL_ROOT>/scripts/portfolio_update.py --json '[{"name":"长电科技","code":"600584","quantity":400,"cost_price":39.53}]'
```
或通过 Python 直接调用：
```python
import sys; sys.path.insert(0, '<SKILL_ROOT>/scripts')
from portfolio_update import update_from_ai_result
update_from_ai_result([{'name':'长电科技','code':'600584','quantity':400,'cost_price':39.53}])
```

---

## 报告结构

```
📊 A股持仓诊断报告 · {DATE}

> 市场概况：{INDEX_SUMMARY}

---

## 一、持仓健康度总览

| 指标 | 数值 |
|------|------|
| 持仓证券数 | {COUNT} |
| 今日涨跌板块 | {SECTOR_HOT} |
| 整体格局 | {MARKET_VIEW} |

---

## 二、各持仓技术诊断

### {N}. {EMOJI} {NAME}（{CODE}）
成本{COST} | 数量{QTY} | 盈亏{PROFIT_PCT}%

**技术信号：{TECH_VIEW}**
- {SIGNALS_LIST}

> **建议：{ACTION}**
> {REASONING}

---

## 三、综合建议框架

| 操作 | 标的 | 理由 |
|------|------|------|
| {OP_TABLE} | ... | ... |

---

## 四、关注机会

{CUSTOM_STOCKS_VIEW}

---

> ⚠️ 本报告仅供参考，不构成投资建议。
> 数据来源：AKShare 实时行情 | 生成时间：{TIME}
```

## EMOJI 映射

| 信号类型 | EMOJI |
|---------|-------|
| 偏多/上升趋势 | 🟢 |
| 中性/观望 | 🟡 |
| 偏弱/下降趋势 | 🔴 |
| 超卖/反弹机会 | 💡 |
| 超买/注意止盈 | 🎯 |
| 止损/减仓 | ⚠️ |

## 微信推送格式（简化版）

微信消息有字数限制时，使用精简版：

```
📈 持仓诊断 {DATE}
━━━━━━━━━━━━━━
指数：{INDEX_LIST}

【偏多】{STOCK1} {PRICE} {CHANGE}%
【偏弱】{STOCK2} {PRICE} {CHANGE}%

操作建议：
✅ {ACTION1}
⚠️ {ACTION2}

详细分析已发送至控制台
```
