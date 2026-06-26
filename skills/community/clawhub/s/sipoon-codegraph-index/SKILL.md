# codegraph-index

> **借鉴来源**：CodeGraph (colbymchenry/codegraph)
>
> 预索引代码知识图谱，用 tree-sitter 建立符号关系、调用图、代码结构，通过 MCP Server 供 Agent 查询。
>
> **Benchmark**：平均减少 57% token，71% 更少 tool calls，大型仓库效果更明显。

---

## 触发条件

满足以下任一场景时激活：
- 用户要求分析项目结构、架构、技术栈
- 用户要求查找某个函数/类的调用关系
- 用户要求了解代码库规模（文件数、语言分布）
- 工作区代码量超过 200 个源文件
- 进入大型代码库（>5000 行）需要快速定位

---

## 工作流程

### Phase A：初始化索引（首次使用）

```bash
# 检查 tree-sitter CLI 是否存在
tree-sitter --version

# 如果不存在，用 npm 安装（CodeGraph 兼容 Windows）
npm install -g tree-sitter-cli

# 初始化项目索引
cd <项目目录>
tree-sitter graph
```

### Phase B：索引构建（核心）

对工作区执行 tree-sitter 解析，输出四类信息：

**1. 符号表（Symbols）**
```bash
tree-sitter query --scope source.ts "<项目>" "(function_declaration name: (identifier) @func-name)"
```

**2. 调用图（Call Graph）**
```bash
tree-sitter query --scope source.ts "<项目>" "(call_expression function: (identifier) @caller)"
```

**3. 导入关系（Imports）**
```bash
tree-sitter query --scope source.ts "<项目>" "(import_statement)"
```

**4. 文件结构摘要**
```bash
# 按语言统计文件数
Get-ChildItem -Recurse -Include *.ts,*.tsx,*.js,*.py,*.go,*.rs | Group-Object Extension | Select-Object Name, Count
```

### Phase C：MCP Server 封装（可选，看 OpenClaw MCP 支持情况）

将索引结果封装为 MCP Tool，供 Agent 调用：

```
Available Tools:
- symbol_search(query) → 返回符号定义位置
- callgraph(function_name) → 返回调用链
- file_structure(lang) → 返回文件树
- import_graph(file) → 返回导入/被导入关系
```

### Phase D：Agent 查询模式

收到代码探索请求时：
1. **先查索引**（symbol_search / callgraph）
2. **再读文件**（只读相关文件，不是全文扫描）
3. **避免 spawn Explore 子 agent 全文扫描**

---

## 输出格式

```markdown
## 代码结构摘要

| 指标 | 值 |
|------|-----|
| 总文件数 | N |
| 总代码行数 | N |
| 主语言 | TypeScript |
| 框架 | Next.js 16 |

## 核心模块

| 模块 | 路径 | 导出符号 |
|------|------|---------|
| auth | src/auth/ | login, logout, refresh |
| api | src/api/ | fetch, post, put |

## 调用关系（简化）

auth/login → api/fetch → /auth/token
```

---

## 与直接 grep/glob 的对比

| 操作 | 无索引 | 有索引 |
|------|--------|--------|
| 找函数定义 | grep 全文 → 扫描所有文件 | symbol_search → 直接返回 |
| 找调用链 | 手动追踪 | callgraph → 一步返回 |
| 大仓库探索 | 消耗大量 token | 减少 57% token |

---

## 限制与注意事项

- tree-sitter CLI 不支持 C#（需要 .NET 分析器）
- Windows 下 `tree-sitter graph` 输出路径可能用反斜杠
- 索引只对解析过的语言有效，先确认项目语言是否被支持
- 索引文件（.tree-sitter/）应该加入 `.gitignore`

---

## 死代码检测（扩展）

利用调用图识别孤立节点（叶子节点无入边 = 潜在死代码）：

```bash
# 通过 tree-sitter 调用图，找出从未被调用的函数
# 步骤：
# 1. 用 tree-sitter graph 导出调用图（JSON 格式）
# 2. 解析 JSON，找出所有函数定义节点
# 3. 过滤出没有任何调用者的节点

python3 -c "
import json, sys
graph = json.load(open('.tree-sitter/call_graph.json'))
calls = set()
for edge in graph.get('calls', []):
    calls.add(edge['caller'])
    
for node in graph.get('definitions', []):
    if node['name'] not in calls:
        print(f'POTENTIAL DEAD: {node[\"name\]} @ {node[\"file\"]}:{node[\"line\"]}')
"
```

**注意**：调用图只能检测静态调用，动态调用（eval、反射）需人工确认。

---

## 触发命令

当用户说"分析这个项目"、"找某个函数在哪"、"了解代码结构"时使用。
## 下一跳（Skill 链式调用）

codegraph-index 是**代码探索前置技能**，索引完成后按以下路径调用：

`
codegraph-index → refactoring（发现死代码/结构问题时）
              → agent-teams（需要多角度代码审查时）
              → 直接读文件（索引结果足够时，不需要下一步）
`

**下一跳触发条件**：
- 索引完成后发现大量死代码 → 调用 efactoring 做影响分析和重构
- 索引完成后需要多角度审查 → 调用 gent-teams
- 索引结果已足够回答用户问题 → 直接输出结果，不需要下一步
