# Changelog

## [0.1.0] - 2026-04-23

### 🎉 首发

**核心功能**
- AI 简历改写：按目标 JD 重写工作经历，STAR 结构 + 量化成果 + 关键词命中
- 匹配度评分：4 维度 100 分制（技术栈 / 年限 / 学历 / 亮点）
- JD 解析：支持 Boss 直聘 URL / 拉勾 / 纯文本
- 简历解析：PDF / DOCX / MD / TXT
- DOCX / Markdown 导出
- 面试话术卡生成（付费档）
- Pro 档批量 Boss 自动投递（对接 `boss-zhipin` skill）

**LLM 兼容**
- 阿里百炼（默认 qwen-plus）
- DeepSeek
- 智谱 GLM-4
- OpenAI GPT-4o-mini

**商业化**
- 免费：每天 1 次 match-score
- ¥29 单次
- ¥99 月卡（无限 + 面试卡）
- ¥299 Pro（+ 批量投递）

**首发真人案例**
- 陈虹竹（4 年大数据） vs 字节跳动 JD
- 改写后匹配度 **94/100**
- 详见 `examples/chen-case-report.md`

**合规**
- 不造假原则写入 LLM system prompt
- 免费版含"人工 review 提示"
- 本地数据零上传（简历在本机解析，仅结构化片段发给用户指定 LLM）
