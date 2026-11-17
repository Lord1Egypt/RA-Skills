# 小微企业财税套装 使用说明书

套装包含：**小微企业财税专家 Agent** + **发票归集自动台账 Skill**

核心优势：全本地离线运行，发票、收支数据全程不出本机，杜绝财务信息泄露。
发票识别采用「本地 OCR 取字为主 + 本地多模态大模型(VLM)辅助字段定位」的混合路线，
兼顾长数字串的识别准确率与各种版式的适应能力。

---

## 一、安装导入步骤

1. 关闭 WorkBuddy，将整个 `tax-invoice-skill` 文件夹放入技能目录：
   - Windows：`C:\Users\你的用户名\.workbuddy\skills\`
   - Mac：`~/.workbuddy/skills/`
2. 重启 WorkBuddy，左侧技能栏会自动加载本套工具。
3. 导入 `tax-expert.agent`：快捷键 `Ctrl+Shift+P` 打开代理面板 → 创建代理 → 粘贴文件全部内容保存。
4. 按第二节「手动安装步骤」装好本机运行环境（Python 依赖 + Ollama 模型）。

---

## 二、本地运行依赖（离线必需）

本技能自带 Python 实现（`scripts/` 目录），运行时不依赖任何云端接口，但本机需具备以下环境：

1. **Python >= 3.10**
2. **OCR 引擎（本地）**：`PaddleOCR`，用于逐字识别发票号码、税号、价税合计等长数字串（数字来源基准）。
3. **本地多模态模型（VLM，辅助）**：通过 **Ollama** 提供，仅用于补 OCR 规则未能定位的字段。
   必须使用支持图像输入的本地模型，例如 `qwen2.5vl:7b`（默认）/ `minicpm-v` / `llava` 等。
   > 注意：必须是**本地多模态模型**，不能偷接任何云端 VLM（如 GPT-4V），否则「数据不上传」的承诺即被打破。
4. **Excel 导出**：`openpyxl`

> 运行前脚本会自动检测上述环境；若 PaddleOCR 未装、Ollama 未启动或模型未拉取，会**打印明确的安装命令提示后退出**，不会静默联网安装。因此请务必先按下方步骤手动装好。

### 手动安装步骤

**第 1 步：安装 Python 依赖（OCR 引擎 + Excel 导出）**
```bash
# 建议在项目内建虚拟环境（可选但推荐）
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 安装全部 Python 依赖（含 paddleocr / paddlepaddle / PyMuPDF / opencv-python / openpyxl / requests）
pip install -r scripts/requirements.txt
# 注：requests 已包含在 requirements.txt 中，无需单独安装；仅当环境异常缺失时才需 pip install requests
```
> 首次运行 `PaddleOCR` 会自动下载中文识别模型（约几百 MB），需联网一次；模型落本地后后续断网可用。

**第 2 步：安装并启动 Ollama（本地 VLM 运行时）**
```bash
# 1) 下载安装 Ollama：https://ollama.com  （按系统指引安装，Windows/Mac 均为图形安装包）
# 2) 启动 Ollama 服务（安装后通常开机自启；也可手动启动）
ollama serve          # 终端常驻，监听 http://localhost:11434
```

**第 3 步：拉取本地多模态模型**
```bash
# 拉取默认模型（约 4~6 GB，需联网一次，落本地后断网可用）
ollama pull qwen2.5vl:7b
```
> 验证模型已就位：`ollama list` 应能看到 `qwen2.5vl:7b`。

**第 4 步（可选）：自定义模型或地址**
```bash
# 若使用其他本地多模态模型，或 Ollama 不在默认地址，用环境变量覆盖：
export VLM_MODEL=minicpm-v          # 模型名，需先 ollama pull 对应模型
export OLLAMA_API=http://localhost:11434/api/chat   # 默认地址，一般无需改
```

**完成上述 4 步后**，即可在 WorkBuddy 中触发技能整理发票（见第三节）。若某步缺失，运行时会立即得到对应的安装提示。

---

## 三、使用方法

### 1. 自动批量整理发票（生成台账）
聊天输入：`整理发票`，按提示选择存放票据的文件夹（仅读取该目录，PDF/JPG/JPEG/PNG）。
技能会通过终端执行本地脚本完成全流程：
```bash
python scripts/run_pipeline.py "<票据文件夹路径>"
# 可选参数：
#   --out "<输出xlsx路径>"   指定台账保存位置（默认在票据目录生成「月度财税台账.xlsx」）
#   --limit N                单批处理上限（默认 100）
```
执行后在该目录生成 `月度财税台账.xlsx`，含两个工作表：
- **月度财税台账**：固定 10 列表头（开票日期、发票类型、销售方、不含税金额、税额、价税合计、发票号码、票据状态、所属月份、风险备注）+ 合计行。
- **异常票据清单**：勾稽不符、字段缺失、格式异常或类型无法识别的票据，供人工复核。

### 2. 财税风险 & 报税测算
聊天输入：`财税咨询`，读取上一步生成的台账文件，专家自动做成本核算、季度算税、风险排查。

---

## 四、容错与安全

- 损坏、模糊无法识别的发票单独列入「异常票据清单」，不丢弃源文件。
- 全程禁止将发票原图、金额、企业信息上传任何云端接口；VLM 必须走本地 Ollama。
- 不修改、删除客户原始发票文件，仅读取解析。
- VLM 调用失败（本地模型未就绪等）时自动降级为「OCR + 正则」，缺失字段进入异常清单，整体流程不中断。

---

## 五、售后与更新

购买享 1 年免费更新：财税新政更新、台账模板优化、新增票据识别兼容格式。
如需企业定制：定制公司专属报表、对接内部进销存表格可单独付费开发。
