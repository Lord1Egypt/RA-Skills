# CI Output Schema — Skills-Summarize-Audit v9.2.2

发布版本元数据：{"version": "9.2.2"}。运行格式以脚本真实 JSON 为准，不依赖 LLM 模拟 --ci。

- installed/visible/all：schema_version=1、mode=read_only、scope、summary、issues、profile、skill_scores、relationships、recommendations、items、scan、baseline、actions。
- ecosystem：schema_version=2、mode=read_only、ecosystem_assessment、signals_source、signals_status、data_contract、scan/baseline（Skill 层可读时）、actions。
- optimization.summary：total_tools、keep、watch、hide、uninstall_candidates、pending_evidence、evidence_coverage、data_gaps。
- 扫描 baseline 可随显式 JSON 导出提供下次 --baseline；默认只 stdout，不隐式写入。
- 默认输出 Markdown 文本；--json 为结构化报告；--detail 展开行动明细。

退出码：0=完成请求的扫描（仍可能含问题/未知）；1=--fail-on 严重度门禁命中；2=参数/导出/证据输入错误。
CI 使用 --fail-on critical 或 warning，不根据模型生成的总体分数决定成功。
