# -*- coding: utf-8 -*-
"""
rag-optimization scripts 包
===========================
将 scripts/ 目录封装为 Python 包。

导入约定（与 SKILL.md 一致）：推荐平铺导入——先将 scripts/ 加入 sys.path，
再 `from llm_client import ...`。

包式导入（`from scripts.xxx import ...`）默认不可用：子模块内部使用平铺导入
（如 bm25_retriever 内部 `from retriever_base import BaseRetriever`），
未将 scripts/ 加入 sys.path 时会触发 ModuleNotFoundError。
仅当 scripts/ 已在 sys.path 中（例如同进程先运行过
`scripts/generate-api-docs.py`，它会把 scripts/ 注入 sys.path）时，
包式导入才生效。
"""
