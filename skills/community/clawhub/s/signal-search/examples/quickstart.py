"""examples/quickstart.py - Signal-Search 最小上手示例（3 行出结果）。

依赖（一次性）：pip install trafilatura curl_cffi requests lxml markdownify
运行：        cd <skill 根目录> && python examples/quickstart.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from orchestrate import retrieve

# 1) 联网检索（默认配置：自动选源 → 抓取 → SBA 打分 → M51 事实锚定）
r = retrieve("TCP 和 UDP 的核心区别", {"max_sources": 3}, 6000)

# 2) 看结果：先答后源，每条结论带来源与加权分
print("档位:", r["tier_used"], "| 置信度:", round(r["confidence"], 2))
print("结论:", r["findings"])
for i, s in enumerate(r["sources"], 1):
    print(f"  [{i}] {s.get('title')}  <-  {s.get('url')}  (加权 {s.get('weighted'):.2f})")

# 3) 返回字段：findings(先答后源) / sources(去重截断后文档) / scores(SBA 明细)
#    confidence(0-1) / token_used / exhausted(预算先到?) / tier_used / trace
#    （单源抓取失败会写入 trace / meta.warnings，不会让检索崩溃）
#
# 想完全离线、不触发任何抓取？把资料直接喂进来即可：
#     r = retrieve("TCP 和 UDP 的核心区别",
#                  docs=[{"url": "https://example.com/a",
#                         "text": "TCP 面向连接、可靠传输；UDP 无连接、低延迟。"}])
