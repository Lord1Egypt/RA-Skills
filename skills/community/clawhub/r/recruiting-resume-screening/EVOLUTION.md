# Evolution Log — recruiting-resume-screening

## 2026-05-12 — PDF 脚本补 stderr 警告

- CEO review 发现：三个后端 wrapper 静默吞错（`except Exception: return None`），批量跑挂时无法 debug 是哪个后端在哪个文件上失败。
- 修正：新增 `_warn()` 辅助，在 fitz / pdfplumber / pdfminer 三处 wrapper 里输出 `warn: {backend} failed on {file}: {ErrType}: {msg}`。
- 接口不变；评分与最佳后端选择逻辑不变。

## 2026-05-12 — 重构为 Superpowers 风格 + 开源 PDF 脚本

- 把原 `05-resume-screening.md` 拆分：SKILL.md 只留触发、工作流、评级、反模式、自检；
  - 五维评估细节独立为 `five-dimension-rubric.md`。
  - 疑点清单独立为 `red-flags-catalog.md`。
  - 个人评估卡 / 排序表 / 复核报告模板独立为 `output-templates.md`。
  - 批量筛选纪律独立为 `batch-screening.md`。
  - PDF 提取与多后端 triage 独立为 `pdf-extraction.md`。
- 补一份开源版 `scripts/resume_pdf_extract.py`：多后端（fitz / pdfplumber / pdfminer.six）+ Unicode 归一化 + 跟踪串 / 碎片行清洗 + 评分 + 质量分层 + JSON / Markdown 输出。
- 描述字段改为 "Use when ..." 触发条件。

## 2026-05-11 — 校招 AI 平台工程师筛选校准

- 在反模式中明确"凭记忆输出""复用旧会话结论""3 行总结当完整执行""把内部过程混入正式报告"。
- 强化文本质量分层：`high / medium / low`，low 候选人单独列待补核，不阻塞整批交付。
- 强化 PDF 提取纪律：不再默认单跑 `pdfplumber`，必须先做多后端 triage。

## 2025-02-14 — 多后端 PDF 提取 triage 沉淀

- 触发：多简历筛选暴露 `pdfplumber` 在中文简历 PDF 上的严重噪声（页边跟踪串、隐藏文本层、装饰碎片）。
- 验证集：11 份 AI 平台工程师简历。
- 发现：
  - 单一后端时 11 份都被判为 `low`。
  - 多后端 + 清洗后，每份 PDF 的"最佳后端"会变化（`pdfplumber` / `pdfminer` / `fitz` 各有胜出）。
  - 跟踪串 / 短 ASCII 碎片清洗显著提升可读性和关键词召回。
- 输出：
  - 新增 `scripts/resume_pdf_extract.py`。
  - 强制要求"先 triage 再排序"，废弃旧固定阈值，改为评分驱动的 `high / medium / low` 分层。
- 经验：
  - 不要相信第一次提取结果。
  - 始终 triage、选最佳清洗文本、把 `low` 单独留人工复核。
