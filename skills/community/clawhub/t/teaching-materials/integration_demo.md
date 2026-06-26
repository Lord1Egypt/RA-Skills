# teaching-materials + diagram-generator 集成演示

## 概述

本文档演示 teaching-materials 技能（教学文档生成）如何与 diagram-generator 技能（思维导图生成）协同工作,为教师提供完整的课件制作解决方案。

## 功能特点

### 1. 自动识别思维导图需求

当教师要求制作课件时,系统会自动分析课程内容,判断哪些部分适合使用思维导图呈现:

**适合思维导图的情况**:
- 知识复习课
- 概念关系复杂
- 逻辑推理步骤
- 对比总结
- 结构化信息

### 2. 多种导图格式支持

| 格式 | 适用场景 | 生成速度 | 可编辑性 |
|------|----------|----------|----------|
| Mermaid | 课件内嵌、快速预览 | 快 | 中 |
| DrawIO | 需要后续编辑、复杂布局 | 中 | 高 |
| Excalidraw | 创意风格、吸引注意力 | 中 | 高 |

### 3. 无缝集成到课件

生成流程:
```
教师需求 → 分析内容 → 生成导图规范 → 调用 diagram-generator → 插入课件 → 交付文件
```

## 使用示例

### 示例 1: 数学复习课

**教师需求**: "帮我制作五年级《小数乘法》复习课的 PPT"

**系统处理**:
1. 分析《小数乘法》单元知识点
2. 识别出适合用思维导图的内容:知识体系梳理
3. 自动生成思维导图 JSON:
```json
{
  "format": "mermaid",
  "title": "小数乘法知识体系",
  "elements": [
    {"id": "root", "type": "node", "name": "小数乘法"},
    {"id": "n1", "type": "node", "name": "小数乘整数"},
    {"id": "n2", "type": "node", "name": "小数乘小数"},
    {"id": "n3", "type": "node", "name": "积的近似数"},
    {"id": "n4", "type": "node", "name": "混合运算"},
    {"id": "n5", "type": "node", "name": "解决问题"},
    {"id": "e1", "type": "edge", "source": "root", "target": "n1"},
    {"id": "e2", "type": "edge", "source": "root", "target": "n2"},
    {"id": "e3", "type": "edge", "source": "root", "target": "n3"},
    {"id": "e4", "type": "edge", "source": "root", "target": "n4"},
    {"id": "e5", "type": "edge", "source": "root", "target": "n5"}
  ]
}
```
4. 调用 MCP 服务生成导图
5. 将导图插入到课件的第 2-3 页（知识回顾部分）
6. 保存完整的 PPT 文件

**输出文件**:
- PPT: `五上一单元_小数乘法_复习课_课件.pptx`
- 导图: `五上一单元_小数乘法_复习课_导图.md`

### 示例 2: 语文古诗课

**教师需求**: "制作《望天门山》课件,用手绘风格的思维导图"

**系统处理**:
1. 分析古诗内容
2. 识别思维导图需求:意象梳理、情感脉络
3. 使用 Excalidraw 格式生成手绘风格导图
4. 插入到课件的"诗情画意"和"主题总结"页面

**输出文件**:
- PPT: `五年级_望天门山_课件.pptx`
- 导图: `五年级_望天门山_导图.excalidraw`

## 技术实现

### MCP 配置

已在 `~/.workbuddy/mcp.json` 中配置:

```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

### 调用示例

```javascript
// 生成思维导图
const diagramSpec = {
  format: "mermaid",
  title: "小数乘法知识体系",
  elements: [...]
};

const result = await mcp_call_tool(
  "mcp-diagram-generator",
  "generate_diagram",
  {
    diagram_spec: diagramSpec,
    filename: "五上一单元_小数乘法_导图"
  }
);

// 结果保存到 d:/WorkBuddy/MyTeacher/diagrams/
```

## 优势

### 对教师
- ✅ 节省时间：自动生成思维导图,无需手动绘制
- ✅ 专业美观：导图样式统一,视觉效果好
- ✅ 可编辑：保存原始文件,后续可修改
- ✅ 多格式：根据需求选择合适格式

### 对学生
- ✅ 知识清晰：思维导图帮助学生建立知识体系
- ✅ 易于记忆：结构化呈现,便于记忆和复习
- ✅ 逻辑清晰：理解知识点之间的关联关系

## 最佳实践

1. **合理使用**：不是所有内容都需要思维导图,避免滥用
2. **简洁原则**：导图内容要精炼,避免信息过载
3. **层级清晰**：一般不超过 3 层级
4. **配色协调**：使用推荐的配色方案,保证视觉效果
5. **位置恰当**：思维导图放在合适的位置(复习课在前,新授课在后)

## 文档资源

- 思维导图使用指南: `references/mindmap_guide.md`
- 课件制作指南: `references/ppt_guide.md`
- diagram-generator 技能文档: `~/.workbuddy/skills/diagram-generator/SKILL.md`

## 常见问题

**Q: 如何指定导图格式?**
A: 在需求中说明格式,如"使用 drawio 格式的思维导图"或"用手绘风格的思维导图"

**Q: 导图可以修改吗?**
A: 可以,保存的原始文件可以用相应工具打开编辑

**Q: 如果不需要思维导图怎么办?**
A: 系统会自动判断,如果内容不适合使用思维导图则不会生成

**Q: 导图保存位置?**
A: 默认保存到 `d:/WorkBuddy/MyTeacher/diagrams/` 目录

## 总结

通过将 diagram-generator 集成到 teaching-materials 技能中,教师可以更高效地制作课件,特别是知识梳理类的复习课。系统会智能判断何时需要思维导图,并自动生成高质量的导图,大大提升了教学文档的制作效率。
