---
name: swimlane-arch
description: |
  业务流程图×系统架构图，一句话出图。支持横向泳道、竖向泳道和分层架构图，输出Draw.io XML格式直接可编辑。
  触发关键词：泳道图、架构图、流程图、swimlane、一句话出图、画个图、业务流程、系统架构
version: 1.1.5
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: ""
    emoji: "🗺️"
---

# 泳道图架构图一句话生成

> 业务流程图 × 系统架构图，一句话出图

**版本**: 1.1.4

---

## ⚡ 30秒体验

对你的Agent说：
> "画个政务审批泳道图"

一句话生成Draw.io XML — 横向/竖向泳道、分层架构，直接打开就能编辑，配色专业美观。

## 技能定位

泳道图架构图一句话生成 是一款智能图表生成器，一句话就能生成专业的 Draw.io XML 图表。

### 核心能力

- **泳道图（Swimlane）**：支持横向泳道和竖向泳道两种方向，多角色/多部门清晰展示跨角色业务流转，政务场景友好
- **架构图（Architecture）**：分层架构（用户层→应用层→服务层→数据层→基础设施层），支持微服务/API/数据库等组件
- **双格式输出**：
  - **Draw.io XML**（`.drawio`）：默认格式，直接在 [diagrams.net](https://app.diagrams.net) 打开编辑
  - **ProcessOn**（需配置 API Key）：如检测到 `PROCESSON_API_KEY`，自动调用 ProcessOn API 生成更精美的云端图表
- **自然语言交互**：无需了解图表语法，用日常语言描述即可

---

## 泳道图（Swimlane Diagram）规范

### 结构规范

#### 方向选择

| 方向 | 适用场景 | 触发关键词 |
|------|---------|-----------|
| **横向泳道**（默认） | 角色少、流程步骤多、强调时序推进 | 默认，或"横向""水平" |
| **竖向泳道** | 角色多、流程步骤少、强调角色分工对比 | "竖向""纵向""竖版""垂直" |

#### 横向泳道

1. **泳道方向**：横向泳道，每个泳道代表一个角色/部门/系统
2. **排列顺序**：泳道从上到下排列，角色名在左侧标签区
3. **流程节点**：节点在对应泳道内，用箭头连接
4. **起止标识**：
   - 起始节点：实心圆（绿色，#82b366）
   - 结束节点：圆环+实心圆（红色，#d9574a）

#### 竖向泳道

1. **泳道方向**：竖向泳道，每个泳道代表一个角色/部门/系统
2. **排列顺序**：泳道从左到右排列，角色名在顶部标签区
3. **流程节点**：节点在对应泳道内，从上到下流转
4. **起止标识**：
   - 起始节点：实心圆（绿色，#82b366）
   - 结束节点：圆环+实心圆（红色，#d9574a）
5. **适用场景**：
   - 多角色并行对比（如多个部门各自流程并排展示）
   - 角色分工明确但流程不长的场景（如政务审批多部门会签）
   - 需要强调角色间横向交互的场景

### 竖向泳道 XML 生成规范

竖向泳道的 Draw.io XML 关键差异：

```xml
<!-- 竖向泳道：使用 horizontal=0 或在 style 中指定方向 -->
<mxCell id="swimlane1" value="角色名称" 
  style="swimlane;horizontal=0;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;startSize=40;" 
  vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="300" height="800" as="geometry" />
</mxCell>
```

关键参数：
- `horizontal=0`：泳道竖向排列（角色标签在顶部）
- `startSize=40`：顶部标签区高度
- 泳道宽度固定（约300px），高度随流程步骤增加
- 节点在泳道内从上到下排列，y坐标递增
- 跨泳道箭头为水平方向连接

### 节点类型与样式

| 节点类型 | 形状 | 填充色 | 边框色 |
|---------|------|-------|--------|
| 开始/结束 | 圆形 | #82b366 / #d9574a | #333333 |
| 活动节点 | 圆角矩形 | #dae8fc | #6c8ebf |
| 判断节点 | 菱形 | #fff2cc | #d6b656 |
| 子流程 | 双边框矩形 | #f8cecc | #b85450 |
| 数据/文档 | 波浪底矩形 | #f5f5f5 | #666666 |

### 箭头规范

| 路径类型 | 线型 | 颜色 | 标注 |
|---------|------|------|------|
| 主流程 | 实线箭头 | 黑色 #333333 | 无 |
| 判断"是" | 实线箭头 | 绿色 #82b366 | 是 |
| 判断"否" | 虚线箭头 | 红色 #d9574a | 否 |
| 跨泳道连接（横向泳道） | 垂直箭头 | 黑色 #333333 | 交互说明 |
| 跨泳道连接（竖向泳道） | 水平箭头 | 黑色 #333333 | 交互说明 |

### 样式参数

- **泳道标题区**：深色背景（#f5f5f5），加粗文字，14px
- **泳道内容区**：白色背景
- **整体尺寸**：宽度自适应，最小 1200px
- **泳道高度**：每条至少 200px
- **字体**：微软雅黑，节点内 12px
- **节点内边距**：上下 8px，左右 12px

### 政务场景常见角色

- 申请人/群众
- 窗口受理人员
- 部门审批人员
- 领导决策
- 系统自动处理
- 第三方机构

---

## 架构图（Architecture Diagram）规范

### 分层架构规范

从下到上依次为：

1. **基础设施层**（最底层）
2. **数据层**
3. **服务层**
4. **应用层**
5. **用户层**（最顶层）

### 节点样式

| 层级 | 形状 | 填充色 | 边框色 |
|------|------|-------|--------|
| 用户层 | 圆角矩形 | #d5e8d4 | #82b366 |
| 应用层 | 圆角矩形 | #dae8fc | #6c8ebf |
| 服务层 | 圆角矩形 | #fff2cc | #d6b656 |
| 数据层 | 圆柱体形状 | #e1d5e7 | #9673a6 |
| 基础设施层 | 矩形 | #f5f5f5 | #666666 |

### 特殊节点

- **数据库**：圆柱体形状（style 包含 `shape=cylinder3`）
- **外部系统**：虚线边框矩形（dashed=1）
- **API/网关**：六边形（hexagon）
- **微服务**：带云图标边框

### 连接线规范

| 关系类型 | 线型 | 说明 |
|---------|------|------|
| 同步调用 | 实线箭头 | 标准服务调用 |
| 异步消息 | 虚线箭头 | 消息队列场景 |
| 数据流 | 实线+标注 | 带数据说明 |
| 依赖关系 | 箭头 | A→B 表示 A 依赖 B |

---

## 输出格式说明

### Draw.io XML（默认）

生成 `.drawio` 文件，可在 [diagrams.net](https://app.diagrams.net) 直接打开编辑，无需任何账号。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxGraphModel dx="900" dy="900" grid="1" gridSize="10" guides="1" ...>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- 泳道和节点定义 -->
  </root>
</mxGraphModel>
```

### ProcessOn（需配置 API Key）

如用户配置了 ProcessOn API Key（环境变量 `PROCESSON_API_KEY`），则优先调用 ProcessOn API：

1. 将图表转换为 ProcessOn 支持的格式
2. 调用 `POST https://open.pingcode.com/v1/graph` 上传并生成图片
3. 返回 ProcessOn 在线链接，支持更多人协作

若未配置 ProcessOn API Key，默认输出 Draw.io XML 格式。

---

## 生成流程

### Step 1: 理解需求

从用户描述中提取：

- **泳道图**：角色列表、流程步骤、所属角色、判断分支、跨角色交互
- **架构图**：架构层次、各层组件、组件调用关系、数据流向

### Step 2: 结构化解析

**泳道图解析逻辑**：

```
输入描述 → 识别角色 → 梳理流程 → 标记判断 → 确定交互
```

**架构图解析逻辑**：

```
输入描述 → 识别层次 → 梳理组件 → 确定关系 → 标注流向
```

### Step 3: 生成 Draw.io XML

必须遵循的 XML 规范：

1. 使用 mxGraphModel 作为根元素
2. 每个元素使用 mxCell 定义，id 必须唯一
3. 泳道使用 `swimlane` 关键字标识
4. 箭头使用 edge 类型，source/target 指向节点 id
5. 合理计算坐标位置，避免重叠

### Step 4: 保存文件

- 文件路径：`{工作目录}/{用户指定名称或自动生成名称}.drawio`
- 编码：UTF-8

---

## XML 生成关键规范

### 节点定义示例

```xml
<mxCell id="node1" value="开始" style="ellipse;fillColor=#82b366;strokeColor=#333333;fontColor=#000000;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>
```

### 泳道定义示例

**横向泳道**（默认）：
```xml
<mxCell id="swimlane1" value="角色名称" style="swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="400" height="300" as="geometry" />
</mxCell>
```

**竖向泳道**：
```xml
<mxCell id="swimlane1" value="角色名称" style="swimlane;horizontal=0;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;startSize=40;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="300" height="800" as="geometry" />
</mxCell>
```

### 箭头定义示例

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;arrowColor=#333333;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

---

## 交互规范

### 用户交互方式

用户只需用自然语言描述流程或架构，例如：

- "画一个用户注册登录的泳道图"
- "生成政务服务事项办理流程图"
- "做一个微服务架构图"

### 自动识别逻辑

1. **图类型判断**：
   - 提到"角色"、"流程"、"办理" → 泳道图
   - 提到"架构"、"层"、"服务"、"系统" → 架构图
   - 混合描述时，优先泳道图（更常用）

2. **泳道方向判断**：
   - 用户提到"竖向""纵向""竖版""垂直" → 竖向泳道
   - 角色数量≥4且流程步骤≤6 → 自动推荐竖向泳道
   - 其他情况 → 横向泳道（默认）

2. **信息补全**：
   - 如果用户描述的信息不足以生成完整图，列出需要补充的点
   - 但不要逐个追问，一次性列出所有缺失信息

### 输出提示

生成完成后告知：

1. 文件保存路径
2. 提醒可在 diagrams.net 打开编辑
3. 如有自定义需求可继续调整

---

## 文件路径

- 主文件：`泳道图架构图一句话生成/SKILL.md`
- 参考模板：
  - `泳道图架构图一句话生成/references/swimlane-template.xml`
  - `泳道图架构图一句话生成/references/arch-template.xml`
---

## 完整生成示例

### 示例：电商订单处理泳道图

**用户输入**：
> 画一个电商订单处理流程图，包含用户、订单系统、库存系统、支付系统4个角色，从下单到发货的完整流程

**生成步骤**：

1. **识别角色**：用户、订单系统、库存系统、支付系统
2. **识别流程**：
   - 用户 → 提交订单 → 订单系统
   - 订单系统 → 扣减库存 → 库存系统
   - 订单系统 → 请求支付 → 支付系统
   - 支付成功 → 发货 → 用户
3. **判断分支**：支付成功/失败
4. **泳道方向**：横向（4个角色，流程步骤适中）

**生成输出**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tools="ext">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- 泳道1：用户 -->
    <mxCell id="swimlane1" value="用户" style="swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="0" y="0" width="300" height="600" as="geometry" />
    </mxCell>
    <!-- 开始节点 -->
    <mxCell id="node1" value="开始下单" style="ellipse;fillColor=#82b366;strokeColor=#333333;fontColor=#000000;" vertex="1" parent="swimlane1">
      <mxGeometry x="100" y="50" width="100" height="60" as="geometry" />
    </mxCell>
    <!-- 订单系统泳道 -->
    <mxCell id="swimlane2" value="订单系统" style="swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="300" y="0" width="300" height="600" as="geometry" />
    </mxCell>
    <!-- 库存系统泳道 -->
    <mxCell id="swimlane3" value="库存系统" style="swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="600" y="0" width="300" height="600" as="geometry" />
    </mxCell>
    <!-- 支付系统泳道 -->
    <mxCell id="swimlane4" value="支付系统" style="swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="900" y="0" width="300" height="600" as="geometry" />
    </mxCell>
    <!-- 结束节点 -->
    <mxCell id="node8" value="收到货物" style="ellipse;fillColor=#d9574a;strokeColor=#333333;fontColor=#000000;" vertex="1" parent="swimlane1">
      <mxGeometry x="100" y="500" width="100" height="60" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

**保存路径**：`电商订单处理流程.drawio`

**用户提示**：
> 泳道图已生成！保存在 `电商订单处理流程.drawio`，可在 [diagrams.net](https://app.diagrams.net) 打开编辑。如需调整角色、流程步骤或添加判断分支，请告诉我。
