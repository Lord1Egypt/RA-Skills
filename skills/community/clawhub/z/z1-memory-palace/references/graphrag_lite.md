# GraphRAG Lite Protocol V1
# 日期：2026-04-08
# 状态：ACTIVE

## 目标
让 Watchdog 在向量命中核心节点后，额外返回 1-hop 的 1-2 个邻居节点。

## 硬限制
- 只允许 1-hop
- 最多返回 1-2 个邻居
- 仍受上下文预算限制
- 不允许因图谱扩散重新制造 context bloat

## 流程
1. BGE-m3 命中核心节点
2. 解析该节点中的 [[Links]]
3. 取最多 1-2 个相邻节点
4. 将核心节点 + 邻居节点一起交给前台 Agent
