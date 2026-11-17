---
name: 发票归集自动台账工具
version: 2.0.0
description: 本地离线OCR识别图片/PDF发票，自动分类专票/普票/电子普票，生成月度报销台账，断网可用，财务数据不向外传输。采用「本地OCR取字为主 + 本地多模态大模型(VLM)辅助字段定位」的混合路线，兼顾数字准确率与版式适应性。
agent_created: true
bind_agent: 小微企业财税专家
triggers: ["整理发票", "票据汇总", "生成报销台账", "统计进项票据"]
tools: [read_file, write_file, terminal]
working_mode: Craft
only_local_data: true
allow_network_upload: false
file_limit: 100
depends:
  python: ">=3.10"
  ocr_engine: "PaddleOCR (本地)"
  vlm: "本地多模态模型，通过 Ollama 提供 (如 qwen2.5vl:7b / minicpm-v / llava)"
  excel: "openpyxl"
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ollama
    envVars:
      - name: OLLAMA_API
        required: false
        description: 本地 Ollama 多模态模型服务地址，默认 http://localhost:11434/api/chat
      - name: VLM_MODEL
        required: false
        description: 本地多模态模型名，默认 qwen2.5vl:7b
    emoji: "🧾"
---

# 一、设计路线（混合架构）

**核心原则：本地 OCR 为主，本地 VLM 辅助。**

| 环节 | 负责方 | 说明 |
|------|--------|------|
| 取字（字符级） | **本地 OCR（PaddleOCR）** | 逐字识别发票号码、税号、价税合计等长数字串，确定性强、不幻觉 |
| 字段定位/归类 | OCR规则优先；**本地 VLM 辅助兜底** | 标准票用关键词+正则直接定位；版式异常/缺字段时调本地多模态模型从图定位字段 |
| 校验 | 脚本（validate） | 价税合计≈不含税+税额、发票号码正则、必填项、分类 |
| 出表 | 脚本（ledger_builder） | openpyxl 生成「月度财税台账.xlsx」+「异常票据清单」 |

> ⚠️ VLM 仅作为**辅助**：只负责"这段OCR文字归到哪个字段"，不负责从零读数字；数字以 OCR 结果为基准。
> ⚠️ 所有模型必须**本地运行**（Ollama 加载多模态模型），严禁把发票图片/金额发往任何云端接口。

# 二、技能执行流程

1. 仅当用户明确提供了票据存放文件夹路径时才继续；**若用户未提供目录，直接退出，不追问、不扫描电脑任何目录**。
2. 用 `python scripts/run_pipeline.py "<文件夹路径>"` 在本地执行整套流程：
   a. 遍历目录内 PDF / JPG / JPEG / PNG（上限 `file_limit` 个，超出提示分批）。
   b. **本地 OCR** 逐张取字（PDF 先渲染首页为图像）。
   c. **字段抽取**：先用关键词+正则从 OCR 文本定位字段；若关键数字字段缺失或置信度低，调**本地 VLM** 辅助定位（仍以南向 OCR 数字为准）。
   d. **校验**：勾稽关系 + 格式校验 + 分类，生成「风险备注」，不可读/对不上的标记为「异常」。
   e. **按月分组**统计总收入、总税额、各类票据数量。
   f. 在票据目录生成「月度财税台账.xlsx」（固定表头）+ 独立「异常票据清单」页。
3. （可选 · 仅 WorkBuddy 环境）输出完成后，自动唤醒【小微企业财税专家】Agent，同步台账数据做税务测算与风险分析。若运行环境不支持 Agent 绑定（如 OpenClaw 等非 WorkBuddy 平台），跳过此步即可——台账与异常清单已完整生成，不影响主流程。

运行脚本前确认依赖已装：`pip install -r scripts/requirements.txt`，且 Ollama 已加载本地多模态模型（默认 `qwen2.5vl:7b`，可用环境变量 `VLM_MODEL` / `OLLAMA_API` 覆盖）。

# 三、容错&安全规则

1. 损坏、模糊无法识别的发票单独列入「异常票据清单」写入 Excel，不丢弃源文件。
2. 全程禁止将发票原图、金额、企业信息上传任何云端接口；VLM 必须走本地 Ollama。
3. 不修改、删除客户原始发票文件，仅读取解析。
4. 含个人身份证、隐私抬头的票据信息仅本地缓存，任务结束自动清空内存数据。
5. 中文路径、带空格文件夹自动兼容，无乱码。
6. VLM 调用失败（本地模型未就绪等）时降级为「OCR+正则」，缺失字段进入异常清单，不中断整体流程。
7. 运行前自动检测本地环境（PaddleOCR 是否安装、Ollama 服务是否运行且已拉取所需模型）；任一缺失则打印明确的安装命令提示后退出，**绝不静默联网安装或拉取模型**（坚持全本地离线）。

# 四、Excel台账固定表头

开票日期 | 发票类型 | 销售方 | 不含税金额 | 税额 | 价税合计 | 发票号码 | 票据状态 | 所属月份 | 风险备注
