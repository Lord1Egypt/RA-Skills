# -*- coding: utf-8 -*-
"""extraction 包：散文 → EventNode 的上游抽取层。

两种实现：
  rule_extractor  零依赖规则抽取（实测天花板约 2.4% 完整坐标率，仅作降级兜底
                   与白盒验收基线；坐标口径见 coverage_stats）
  llm_extractor   LLM 抽取（需 OpenAI 兼容端点，精度高，需 audit_postprocess 清洗）

契约在 schema.py；编排入口在仓库根目录 detect_logic_gaps.py。
"""
