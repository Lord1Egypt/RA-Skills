# Mermaid 语法速查表

## 流程图 (Flowchart)

### 基本语法

```mermaid
graph TD
    A[开始] --> B{判断}
    B -->|是 | C[执行 A]
    B -->|否 | D[执行 B]
    C --> E[结束]
    D --> E
```

### 节点形状

| 语法 | 形状 | 示例 |
|------|------|------|
| `A[文本]` | 矩形 | `A[开始]` |
| `A(文本)` | 圆角矩形 | `A(处理)` |
| `A(文本)` | 圆形 | `A((结束))` |
| `A>文本]` | 不对称形状 | `A>处理]` |
| `A{文本}` | 菱形（判断） | `A{是否完成？}` |
| `A[[文本]]` | 圆柱体（数据库） | `A[(数据库)]` |
| `A[(文本)]` | 圆柱体 | `A[(数据库)]` |

### 连接方向

- `TD` / `TB` - 从上到下
- `LR` - 从左到右
- `BT` - 从下到上
- `RL` - 从右到左

### 连接样式

```mermaid
graph LR
    A -- 实线 --> B
    A -. 虚线 .-> B
    A ==> 粗线 => B
    A --- 无箭头 --- B
```

---

## 时序图 (Sequence Diagram)

### 基本语法

```mermaid
sequenceDiagram
    participant User as 用户
    participant Bot as 阿香
    participant API as 阿里云 API
    
    User->>Bot: 提问
    Bot->>API: 请求向量
    API-->>Bot: 返回 1024 维向量
    Bot->>User: 回答
```

### 箭头类型

| 语法 | 含义 |
|------|------|
| `->` | 实线箭头（同步） |
| `-->` | 虚线箭头（返回） |
| `-x` | 实线叉头（丢失） |
| `-->>` | 虚线箭头（返回） |
| `->>` | 实线箭头（异步） |

### 备注

```mermaid
sequenceDiagram
    Alice->>Bob: 你好
    Note right of Bob: Bob 思考中
    Bob-->>Alice: 你好
```

---

## 类图 (Class Diagram)

### 基本语法

```mermaid
classDiagram
    class Agent {
        +String name
        #String memory
        -int counter
        +think()
        +reply()
    }
    
    class SubAgent {
        +execute()
        +report()
    }
    
    Agent <|-- SubAgent
```

### 关系符号

| 符号 | 含义 |
|------|------|
| `<|--` | 继承 |
| `*--` | 组合 |
| `o--` | 聚合 |
| `-->` | 关联 |
| `--` | 连接 |
| `..|>` | 实现 |
| `..` | 依赖 |

### 成员可见性

- `+` 公开 (public)
- `#` 保护 (protected)
- `-` 私有 (private)

---

## 状态图 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> 空闲
    空闲 --> 工作中：开始任务
    工作中 --> 空闲：完成任务
    工作中 --> 错误：发生异常
    错误 --> 空闲：恢复
```

---

## 甘特图 (Gantt Chart)

```mermaid
gantt
    title 项目开发计划
    dateFormat  YYYY-MM-DD
    section 设计
    需求分析 :a1, 2026-03-01, 7d
    架构设计 :after a1, 5d
    section 开发
    前端开发 :2026-03-10, 10d
    后端开发 :2026-03-10, 12d
    section 测试
    单元测试 :2026-03-20, 5d
```

---

## 饼图 (Pie Chart)

```mermaid
pie
    title 技能使用统计
    "feishu-doc" : 45
    "web_search" : 30
    "browser" : 15
    "其他" : 10
```

---

## 用户旅程图 (User Journey)

```mermaid
journey
    title 用户使用流程
    section 发现需求
      产生问题：5: 用户
      搜索方案：4: 用户
    section 使用技能
      安装技能：3: 用户
      配置技能：2: 用户
      使用技能：5: 用户
    section 获得结果
      查看结果：5: 用户
      满意：5: 用户
```

---

## 思维导图 (Mindmap)

```mermaid
mindmap
  root((OpenClaw))
    技能系统
      本地技能
      ClawHub
      技能安装
    工具
      文件操作
      网络搜索
      浏览器控制
    记忆系统
      短期记忆
      长期记忆
      自我改进
```

---

## 象限图 (Quadrant Chart)

```mermaid
quadrantChart
    title 技能评估矩阵
    x-axis 低成本 --> 高成本
    y-axis 低价值 --> 高价值
    quadrant-1 高价值高成本
    quadrant-2 高价值低成本
    quadrant-3 低价值低成本
    quadrant-4 低价值高成本
    "feishu-doc": [0.2, 0.8]
    "web_search": [0.3, 0.9]
    "browser": [0.7, 0.6]
```

---

## 实用技巧

### 1. 使用子图

```mermaid
graph TB
    subgraph OpenClaw
        A[阿福] --> B[阿香]
    end
    
    subgraph 外部服务
        C[阿里云 API]
        D[飞书 API]
    end
    
    B --> C
    B --> D
```

### 2. 设置样式

```mermaid
graph LR
    A[普通节点]
    B[红色节点]:::red
    C[蓝色节点]:::blue
    
    classDef red fill:#f96,stroke:#333,stroke-width:4px;
    classDef blue fill:#69f,stroke:#333,stroke-width:4px;
```

### 3. 使用图标

```mermaid
graph LR
    A["📄 文档"] --> B["🔍 搜索"]
    B --> C["📊 分析"]
    C --> D["💬 回复"]
```

### 4. 链接到其他节点

```mermaid
graph LR
    A[点击我] --> B[目标]
    click A "https://example.com" "提示信息"
```

---

## 常用配置

### 主题

```javascript
%%{init: {'theme': 'dark'}}%%
graph LR
    A[暗色主题]
```

可用主题：`default`, `dark`, `forest`, `neutral`, `base`

### 方向

```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
    A --> B
```

### 完整配置示例

```javascript
%%{
  init: {
    'theme': 'dark',
    'flowchart': {
      'curve': 'basis',
      'nodeSpacing': 50,
      'rankSpacing': 50
    }
  }
}%%
graph TD
    A[配置示例] --> B[美观的图表]
```

---

## 快速参考

### 最常用节点

```
A[矩形] - 普通步骤
B{菱形} - 判断/决策
C[(圆柱)] - 数据库
D((圆形)) - 开始/结束
```

### 最常用连接

```
--> 实线箭头（主要流程）
-.-> 虚线箭头（可选/异步）
--- 无箭头连线（关联）
```

### 最佳实践

1. **保持简洁** - 每张图不超过 15 个节点
2. **使用注释** - 复杂连接添加文字说明
3. **统一风格** - 同类节点使用相同形状
4. **测试渲染** - 先在 Mermaid Live Editor 测试

---

## 在线工具

- **Mermaid Live Editor**: https://mermaid.live/
- **Mermaid 官方文档**: https://mermaid.js.org/
- **QuickChart**: https://quickchart.io/ (API 服务)
- **mermaid.ink**: https://mermaid.ink/ (图片生成)

---

**最后更新：** 2026-03-12
