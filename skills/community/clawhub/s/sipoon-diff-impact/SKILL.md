# diff-impact — 变更影响分析

> **借鉴来源**：Understand Anything (Lum1104/Understand-Anything)
>
> 在提交前预测代码改动对整个系统的影响范围，基于知识图谱计算连锁反应。

---

## 触发条件

满足任一场景时激活：
- 用户说"改了这个会不会影响其他地方"、"影响分析"
- 用户说"帮我看看这个 PR 会影响哪些模块"
- 用户即将 commit / merge 前
- 重构前需要确认影响范围

---

## 核心原理

```
git diff → 知识图谱定位 → 连锁影响计算 → 影响报告
```

前置依赖：`codegraph-index` 已完成（知识图谱 `.understand-anything/knowledge-graph.json` 存在）

---

## 工作流程

### Phase 1：获取变更集

```bash
# 获取当前工作区 vs 最新 commit 的 diff
git diff --name-only HEAD

# 或者指定范围
git diff <commit-a> <commit-b> --name-only
```

### Phase 2：定位变更节点

对于每个变更文件，在知识图谱中找到对应节点：

```python
# 伪代码
graph = json.load('.understand-anything/knowledge-graph.json')
changed_files = git_diff_files()  # from Phase 1

affected_nodes = []
for f in changed_files:
    node = find_node_by_path(graph, f)
    if node:
        affected_nodes.append(node)
```

### Phase 3：传播影响（Graph Traversal）

从变更节点出发，沿调用边向外传播：

```python
def propagate(nodes, depth=3):
    """BFS traversal along call edges up to N层深度"""
    visited = set(nodes)
    frontier = list(nodes)
    
    for _ in range(depth):
        next_frontier = []
        for node in frontier:
            for edge in graph.edges(out_node=node.id):
                if edge.target not in visited:
                    visited.add(edge.target)
                    next_frontier.append(edge.target)
        frontier = next_frontier
    
    return visited - set(nodes)  # exclude starting nodes
```

### Phase 4：输出报告

```markdown
## 变更影响报告

**改动文件（3个）：**
- src/auth/login.ts
- src/api/client.ts
- src/utils/crypto.ts

**直接依赖（4个）：**
```
src/auth/login.ts
  ├─ calls → decodeToken() @ src/auth/token.ts:42
  ├─ imports → apiClient @ src/api/client.ts
  └─ field → userId @ src/types/User.ts:12

src/api/client.ts
  ├─ calls → fetchWrapper() @ src/utils/http.ts:8
  └─ calls → Crypto.encrypt() @ src/utils/crypto.ts:31
```

**连锁影响（2层，共7个）：**
```
Layer 1 (直接调用):
- src/auth/token.ts (decodeToken)
- src/utils/http.ts (fetchWrapper)
- src/utils/crypto.ts (encrypt)

Layer 2 (间接调用):
- src/services/AuthService.ts (uses decodeToken)
- src/middleware/auth.ts (uses fetchWrapper)
- src/api/Payment.ts (uses encrypt)
```

**⚠️ 高危区域：** `src/api/Payment.ts` — 支付相关，修改需谨慎

**建议：** 修改后运行 `/understand-diff` 重新验证
```

---

## 增量 diff（针对未 commit 的改动）

对于工作区中未提交的改动，优先用 `codegraph-index` 的增量模式：

```bash
# 知识图谱存在时，codegraph-index 默认增量分析
# 直接调用的命令：
codegraph-index --diff  # 分析当前 diff
codegraph-index --changed-only  # 只分析变更文件
```

---

## 与 refactoring 的区别

| 维度 | refactoring | diff-impact |
|------|-------------|-------------|
| 触发时机 | 修改前 | 修改前 + 提交前 |
| 分析方式 | 影响范围（改什么） | 连锁反应（影响什么） |
| 前置依赖 | 无 | 需要 codegraph-index |
| 深度 | 浅（直接依赖） | 深（多跳传播） |
| 输出 | "改这里会影响那里" | "这个改动会触发N层连锁" |

`diff-impact` 补充 `refactoring`：先用 diff-impact 了解连锁范围，再用 refactoring 做具体重构。

---

## 限制与注意事项

- **依赖知识图谱**：没有 `.understand-anything/knowledge-graph.json` 时，需要先 `codegraph-index` 建立索引
- **动态调用无法追踪**：eval/反射/DI容器动态加载的调用，边在图中不存在
- **循环引用处理**：BFS 时需要记录 visited，防止死循环
- **大型 repo**：超过 10 层深度的传播会截断，显示 "N 个节点未展示"

---

## 下一跳（Skill 链式调用）

```
diff-impact → codegraph-index（知识图谱不存在时）
           → refactoring（确定影响范围后）
           → agent-teams（高危区域需要多人审查）
           → 直接输出报告（知识图谱已存在时）
```

**触发条件：**
- 知识图谱不存在 → `codegraph-index` 先建索引
- 影响报告中有高危模块（如支付、数据写入）→ `agent-teams` 审查
- 用户要开始修改 → `refactoring` 做影响分析