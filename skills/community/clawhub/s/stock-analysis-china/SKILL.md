---
name: stock-analysis-china
description: |
  A股持仓深度技术分析技能。当用户发送持仓截图图片、或提及持仓/股票/投资建议相关意图时，本技能自动激活。

  激活条件（满足任一即触发）：
  - 用户发送了图片（持仓截图、行情截图等）
  - 用户说"分析持仓"、"我的持仓怎么样"、"给投资建议"、"持仓诊断"、"我的股票"、"目前持仓"
  - 用户说"更新持仓"、"录入持仓"
  - 用户说"每日一股"或类似表述
  - 任何涉及持仓查询、投资建议、持仓诊断的技术分析请求

  激活后行为：
  1. 若收到图片 → 优先用 AI 多模态能力直接识别截图内容
  2. 若无图片但有持仓意图 → 读取 positions_portfolio.json
  3. 若无持仓数据 → 告知用户并引导录入
  4. 运行完整技术分析（AKShare 实时行情 + RSI/MACD/KDJ/布林带/均线）
  5. 生成操作建议（持有/减仓/加仓/止盈/止损）
  6. 直接在对话中输出分析结果
---

# A股持仓技术分析 Skill

## ⚠️ AI 行为规则（必须遵守）

当本 skill 被激活时，AI **必须按以下顺序执行**，只有识别图片的结果不是持仓信息时可以退出，否则不得跳过步骤或中途停止：

**第一步：处理图片（如有图片）**
- 微信/飞书截图保存路径：`~/.qclaw/media/inbound/`，或者`~/.openclaw/media/inbound/`（跨平台）
- 优先用 AI **多模态能力直接读取图片内容**，识别其中的持仓信息
- 检查`SKILL_ROOT/data/`目录下是否存在json文件或json文件是否为空，若为空，优先执行"环境依赖与故障排查"章节的环境配置相关操作
- 若多模态失败，使用OCR识别
- 识别成功 → 提取：股票名称、代码、数量、成本价
- 识别失败 → **必须告知用户具体原因**，并引导手动输入，**不得直接说"无法识别"然后停止**

**第二步：读取/更新持仓数据**
- 持仓文件路径：`SKILL_ROOT/data/positions_portfolio.json`
- 若文件不存在或为空 → 引导用户录入持仓
- 若有图片但识别失败 → 询问用户手动输入关键字段

**第三步：运行技术分析**
```bash
python3 <SKILL_ROOT>/scripts/stock_analysis_core.py
```

**第四步：输出分析结果**
- 直接在当前对话输出结构化报告
- 包含：大盘指数、各持仓技术信号、综合建议

**⚠️ 关键禁止行为：**
- 收到图片后，不得在未尝试识别的情况下说"图片无法显示"
- 不得收到图片后要求用户"用文字告诉我持仓"
- 不得跳过识别步骤直接进入"请告诉我你的持仓"
- 识别失败时，必须说明失败原因并提供解决路径


## 核心能力

1. **持仓识别** — 用户发送微信持仓截图，AI 直接识别提取持仓信息
2. **持仓管理** — 自动更新 `data/positions_portfolio.json` 持仓数据
3. **行情拉取** — 通过 AKShare 获取：指数实时行情、个股实时价格、K线历史数据
4. **技术指标** — RSI、MACD、KDJ、布林带、均线多头/空头排列
5. **综合诊断** — 结合大盘趋势 + 技术面，给出每只持仓的具体操作建议
6. **报告推送** — 生成结构化报告，直接在微信对话中展示

## 文件结构

```
stock-analysis-china/
├── SKILL.md                               # 本文件
├── data/
│   └── positions_portfolio.json           # 持仓数据
├── scripts/
│   ├── stock_analysis_core.py            # 技术指标计算引擎
│   └── portfolio_update.py               # 持仓数据管理工具
└── references/
    └── analysis_prompt_template.md       # 报告输出模板
```

## 路径约定（跨平台）

| 资源 | Windows | macOS / Linux |
|------|---------|---------------|
| 用户主目录 | `%USERPROFILE%` | `~` |
| 工作区 | `%USERPROFILE%\.qclaw\workspace` | `~/.qclaw/workspace` |
| 微信截图 | `%USERPROFILE%\.qclaw\media\inbound\` | `~/.qclaw/media/inbound/` |
| Tesseract OCR | `C:\Program Files\Tesseract-OCR\` | `/usr/local/bin/tesseract` (macOS) 或 `/usr/bin/tesseract` (Linux) |
| Python 解释器 | 自动推断（`python` 或 `python3`） | 自动推断（`python3`） |

**所有路径均通过 `Path.home()` 和 `pathlib.Path` 动态推断，无需手动修改。**

---

## 使用流程

### 场景一：发送持仓截图（推荐）

用户在微信中发送持仓截图 → AI 自动识别并更新持仓数据

**识别字段：**
- 股票名称 / 股票代码
- 持仓数量
- 成本价
- 当前价（可选）
- 盈亏比例（可选）

**AI 执行步骤：**

1. **读取截图** — 微信截图自动保存至 `%USERPROFILE%\.qclaw\media\inbound\`，
   查找最新图片文件，读取内容

2. **图像识别** — 优先使用 AI 多模态能力直接识别截图内容；
   备用方案：使用 Tesseract OCR（需安装 tesseract + chi_sim 语言包）
   ```bash
   tesseract <截图路径> stdout --oem 1 --psm 6 -l chi_sim+eng
   ```

3. **提取持仓数据** — 从识别结果中解析出：名称、代码、数量、成本价等

4. **更新持仓 JSON** — 调用 `portfolio_update.py`
   ```bash
   python <SKILL_ROOT>/scripts/portfolio_update.py --json '[{"name":"长电科技","code":"600584","quantity":400,"cost_price":39.53}]'
   ```

5. **确认结果** — 向用户列出识别到的持仓列表，请用户核对校正

**示例对话：**
```
用户：[发送微信持仓截图]
AI：已识别到 5 只持仓：
    1. 长电科技(600584) 400股 成本39.53
    2. 招商银行(600036) 500股 成本39.44
    ...
    ⚠️ 请核对以上数据，如有误请告诉我正确信息。
    数据已更新。需要分析吗？
```

---

### 场景二：手动更新持仓

用户通过对话更新持仓：

```
我今天买了100股宁德时代，成本300
```

```
把招商银行清仓了
```

AI 自动更新持仓 JSON。

---

### 场景三：分析持仓

用户说：
```
分析一下我的持仓
```
```
我的持仓怎么样
```

**AI 执行步骤：**

**Step 1 — 读取持仓数据**
从 `data/positions_portfolio.json` 读取

**Step 2 — 运行分析脚本**
```bash
python <SKILL_ROOT>/scripts/stock_analysis_core.py
```

**Step 3 — AI 综合研判**
结合脚本输出的指标数据，AI 给出：
- 大盘环境判断（强势/震荡/偏弱）
- 每只持仓的技术面评分 + 操作建议
- 整体仓位建议

---

## 持仓数据格式

```json
{
  "last_updated": "2026-03-29",
  "source": "微信截图识别",
  "portfolio": [
    {
      "code": "600584",
      "name": "长电科技",
      "quantity": 400,
      "cost_price": 39.53,
      "current_price": 45.92,
      "market_value": 18368.4,
      "profit_pct": -13.92,
      "asset_type": "stock"
    }
  ]
}
```

---

## 技术指标说明

| 指标 | 计算参数 | 含义 |
|------|---------|------|
| RSI | 14日 | >75超买/<25超卖，>60偏强/<40偏弱 |
| MACD | 12/26/9 | DIF>0多头，红柱扩张更强势 |
| KDJ | 9/3/3 | >80超买/<20超卖，K>D金叉看多 |
| 布林带 | 20日/2σ | 突破上轨注意回调，跌破下轨关注反弹 |
| 均线 | 5/10/20/60日 | 多头排列=强势，空头排列=弱势 |

---

## 分析建议判断逻辑

```
IF 偏空信号 > 2 AND tech_view == '偏空':
    建议: 减仓/止损
ELIF 偏多信号 > 2 AND tech_view == '偏多':
    建议: 持有/关注加仓机会
ELIF RSI超卖 OR 跌破布林下轨:
    建议: 超卖关注，暂持有等反弹
ELIF RSI超买 OR 突破布林上轨:
    建议: 注意止盈
ELSE:
    建议: 持有观望
```

---

## 微信对话中的操作指令

| 用户说 | AI 行为 |
|--------|--------|
| 发送持仓截图 | 识别并更新持仓数据 |
| "分析持仓" / "我的持仓怎么样" | 运行完整技术分析 |
| "更新持仓" + 截图 | 更新持仓并确认 |
| "列出我的持仓" | 显示当前持仓列表 |
| "清空持仓" | 清空所有持仓数据 |

---

## 注意事项

- AKShare 数据为免费实时行情，部分 ETF 可能不在实时行情列表中
- 技术分析仅供参考，不构成投资建议
- 持仓数据存储在 skill 目录，升级 QClaw 时注意备份

---

## 环境依赖与故障排查

### 依赖清单

本 skill 需要以下环境支持：

| 依赖 | 版本 | 用途 | 安装方式 |
|------|------|------|---------|
| Python 3 | 3.10+ | 技术指标计算 | 系统 Python 或 `winget install Python.Python.3.12` |
| pip | 最新 | Python 包管理 | 随 Python 自动安装 |
| AKShare | 最新 | 股票数据源 | `pip install akshare pandas` |
| Node.js | 18+ | 图片处理（sharp） | `winget install OpenJS.NodeJS.LTS` |
| sharp | 0.30+ | 图片读取与处理 | `npm install sharp -g` |
| Tesseract OCR | 5.0+ | 备用 OCR 识别 | `winget install UB-Mannheim.TesseractOCR` |
| chi_sim.traineddata | 最新 | 中文 OCR 语言包 | 随 Tesseract 自动安装或者claw自己安装 |

### 常见问题排查

#### 问题 1：图片无法读取（`Cannot find package 'sharp'`）

**症状**：
```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'sharp' imported from ...
```

**原因**：
- sharp 未安装或安装位置不在 OpenClaw 的 node_modules 搜索路径中
- Node.js 全局安装的 sharp 在 `%APPDATA%\npm\node_modules\` 中，OpenClaw 进程找不到

**解决方案**：

1. **检查 sharp 是否已安装**
   ```bash
   npm list sharp -g
   ```

2. **若未安装，全局安装 sharp**
   ```bash
   npm install sharp -g --prefer-offline
   ```

3. **创建 junction 链接**（Windows）
   ```powershell
   New-Item -ItemType Junction `
     -Target "$env:APPDATA\npm\node_modules\sharp" `
     -Path "C:\Program Files\QClaw\resources\openclaw\node_modules\sharp"
   ```

4. **重启 OpenClaw**
   ```bash
   openclaw gateway restart
   ```

5. **验证**
   ```bash
   node -e "require('sharp'); console.log('ok')"
   ```

#### 问题 2：Tesseract 命令找不到

**症状**：
```
tesseract : 无法将"tesseract"项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

**原因**：
- Tesseract 未安装或未加入 PATH

**解决方案**：

1. **安装 Tesseract**
   ```bash
   winget install UB-Mannheim.TesseractOCR
   ```

2. **验证安装**
   ```bash
   "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```

3. **检查中文语言包**
   ```bash
   Get-ChildItem "C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata"
   ```

4. **若语言包缺失，重新安装 Tesseract**

#### 问题 3：Python 依赖缺失（`ModuleNotFoundError: No module named 'akshare'`）

**症状**：
```
ModuleNotFoundError: No module named 'akshare'
```

**原因**：
- akshare 或 pandas 未安装

**解决方案**：

1. **安装依赖**
   ```bash
   pip install akshare pandas
   ```

2. **验证**
   ```bash
   python -c "import akshare; print('ok')"
   ```

#### 问题 4：图片识别失败（OCR 乱码或无输出）

**症状**：
- Tesseract 输出乱码（如 `锟斤拷`）
- OCR 识别结果为空
- 报错 `Error opening data file .../chi_sim.traineddata`

**原因**：
- 图片质量差或格式不支持
- Tesseract 参数不匹配
- 中文语言包未安装或未正确配置

**解决方案**：

1. **检查图片格式**
   ```bash
   file <image_path>  # 确保是 JPEG/PNG
   ```

2. **安装 Tesseract OCR**
   ```bash
   winget install UB-Mannheim.TesseractOCR
   ```

3. **下载中文语言包**（Windows 需要）
   
   Tesseract 默认安装目录可能没有中文语言包，需要手动下载：
   ```powershell
   # 创建用户 tessdata 目录
   New-Item -ItemType Directory -Path "$env:USERPROFILE\tessdata" -Force
   
   # 下载中文简体语言包
   Invoke-WebRequest -Uri "https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata" -OutFile "$env:USERPROFILE\tessdata\chi_sim.traineddata"
   
   # 复制英文语言包（中英文混合识别需要）
   Copy-Item "C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata" "$env:USERPROFILE\tessdata\eng.traineddata" -Force
   ```

4. **配置 TESSDATA_PREFIX 环境变量**
   
   方法一：临时设置
   ```powershell
   $env:TESSDATA_PREFIX = "$env:USERPROFILE\tessdata\"
   tesseract <image_path> stdout --oem 1 --psm 6 -l chi_sim+eng
   ```
   
   方法二：永久设置（推荐）
   ```powershell
   [System.Environment]::SetEnvironmentVariable("TESSDATA_PREFIX", "$env:USERPROFILE\tessdata\", "User")
   ```

5. **验证语言包安装**
   ```powershell
   $env:TESSDATA_PREFIX = "$env:USERPROFILE\tessdata\"
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
   ```

6. **运行中文 OCR 识别**
   ```powershell
   $env:TESSDATA_PREFIX = "$env:USERPROFILE\tessdata\"
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" <图片路径> stdout --oem 1 --psm 6 -l chi_sim+eng
   ```

7. **若仍失败，使用 AI 多模态识别**（推荐）

#### 问题 5：持仓数据文件不存在

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: '.../positions_portfolio.json'
```

**原因**：
- 首次使用，持仓数据文件未创建

**解决方案**：

1. **手动创建初始文件**
   ```bash
   python <SKILL_ROOT>/scripts/portfolio_update.py --list
   ```

2. **或通过 AI 识别截图自动创建**
   - 发送持仓截图，AI 自动生成 positions_portfolio.json

3. **或手动添加持仓**
   ```bash
   python <SKILL_ROOT>/scripts/portfolio_update.py --add 600584 长电科技 400 39.53
   ```

#### 问题 6：AKShare 数据获取超时

**症状**：
```
[WARN] 指数数据获取失败: ...
```

**原因**：
- 网络连接不稳定
- AKShare 服务器响应慢

**解决方案**：

1. **检查网络连接**
   ```bash
   ping github.com
   ```

2. **重试分析**（AKShare 有内部重试机制）

3. **若持续失败，检查 AKShare 服务状态**
   - 访问 https://github.com/akfamily/akshare/issues

#### 问题 7：跨平台路径错误

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\...\...'
```

**原因**：
- 脚本在 macOS/Linux 上运行，但路径使用了 Windows 格式

**解决方案**：

- 所有脚本已使用 `pathlib.Path` 和 `Path.home()` 动态推断路径
- 无需手动修改路径
- 若仍出现错误，检查 `SKILL_ROOT` 和 `WORKSPACE_DIR` 的推断逻辑

---

## 开发者笔记

### 关键设计决策

1. **路径动态推断**
   - 使用 `Path(__file__).parent.parent` 相对 skill 目录
   - 使用 `Path.home()` 获取用户主目录（跨平台）
   - 避免硬编码路径，确保可移植性

2. **持仓数据优先级**
   - 优先读 skill 内置 `data/positions_portfolio.json`（跟随 skill 更新）
   - 不存在则读 `~/.qclaw/workspace/data/positions_portfolio.json`（升级保护）
   - 确保用户数据不会因 skill 升级而丢失

3. **图片识别优先级**
   - 优先 AI 多模态识别（无需额外工具）
   - 备用 Tesseract OCR（需安装）
   - 若都失败，引导用户手动输入

4. **跨平台支持**
   - Windows / macOS / Linux 全部支持
   - 自动检测系统（`platform.system()`）
   - 自动推断 Python 解释器（`sys.executable`）

### 常见改动陷阱

⚠️ **多文件改动时务必完整检查**

当修改脚本时，必须同步更新：
- SKILL.md 中的路径说明
- analysis_prompt_template.md 中的命令示例
- 所有文档中的硬编码路径

**检查清单**：
- [ ] 脚本改动后，SKILL.md 路径说明是否需要更新？
- [ ] 新增依赖后，是否更新了"依赖清单"表格？
- [ ] 改了路径推断逻辑后，是否更新了"路径约定"？
- [ ] 新增故障排查项后，是否补充了解决方案？

### 测试流程

1. **环境检测**
   ```bash
   python <SKILL_ROOT>/scripts/stock_analysis_core.py
   ```

2. **持仓管理**
   ```bash
   python <SKILL_ROOT>/scripts/portfolio_update.py --list
   ```

3. **图片识别**
   - 发送截图，验证 AI 多模态识别
   - 若失败，手动运行 Tesseract 验证

4. **完整流程**
   - 发送截图 → AI 识别 → 更新持仓 → 运行分析 → 输出报告
