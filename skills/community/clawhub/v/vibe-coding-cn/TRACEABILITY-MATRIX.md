# 需求追溯矩阵

**确保每个需求都有代码实现**

---

## 🎯 问题背景

**之前的问题**：
- ❌ Developer 不看 PRD，只看架构
- ❌ 没有验证需求是否全部实现
- ❌ 可能遗漏重要功能

**实际流程**：
```
用户需求 → Analyst → PRD → Architect → 架构 → Developer → 代码
                          ↓
                      (PRD 在这里就断了)
```

---

## ✅ 改进方案

### 1. Developer 看 PRD + 架构

**修改后的提示词**：
```
你是开发工程师。请根据**需求文档和架构设计**实现完整代码。

## 需求文档（必须实现以下功能）
{PRD 内容}

## 架构设计（遵循以下技术规范）
{架构内容}

## 实现要求
1. **必须实现需求文档中的所有功能**
2. **遵循架构设计的技术规范**
3. ...
```

**效果**：
- ✅ Developer 明确知道要实现哪些功能
- ✅ 避免遗漏重要需求
- ✅ 代码更符合用户期望

---

### 2. 需求追溯矩阵

**Phase 5 新增步骤**：
```javascript
// 生成需求 - 代码追溯矩阵
const traceability = await this.generateTraceabilityMatrix(requirements, code);

console.log(`✅ 追溯矩阵完成：${traceability.coverage}% 需求已实现`);
```

**追溯矩阵内容**：
```json
{
  "requirements": [
    {
      "id": "REQ-001",
      "description": "用户输入月收入和五险一金",
      "implemented": true,
      "files": ["index.html", "app.js"],
      "functions": ["calculateTax()", "validateInput()"]
    },
    {
      "id": "REQ-002",
      "description": "计算并显示个税金额",
      "implemented": true,
      "files": ["app.js"],
      "functions": ["calculateTax()", "displayResult()"]
    },
    {
      "id": "REQ-003",
      "description": "导出计算结果为 Excel",
      "implemented": false,
      "files": [],
      "functions": []
    }
  ],
  "coverage": 67,
  "missingRequirements": ["导出计算结果为 Excel"],
  "summary": "2/3 需求已实现，缺少导出功能"
}
```

---

## 📊 追溯矩阵输出

### 完整示例

```
📊 生成需求追溯矩阵...
✅ 追溯矩阵完成：95% 需求已实现

📋 需求实现情况:
  ✅ REQ-001: 用户输入月收入和五险一金
     文件：index.html, app.js
     函数：calculateTax(), validateInput()
  
  ✅ REQ-002: 计算并显示个税金额
     文件：app.js
     函数：calculateTax(), displayResult()
  
  ✅ REQ-003: 支持五险一金自定义比例
     文件：app.js, config.js
     函数：calculateInsurance(), getConfig()
  
  ❌ REQ-004: 导出计算结果为 Excel
     文件：无
     函数：无
  
📊 覆盖率：75% (3/4 需求已实现)
⚠️ 缺失需求：导出计算结果为 Excel
```

---

## 🔧 实现代码

### 生成追溯矩阵函数

```javascript
async generateTraceabilityMatrix(requirements, code) {
  const prompt = `请创建需求 - 代码追溯矩阵，确保每个需求都有对应的代码实现。

## 需求文档
${requirements.output}

## 代码实现
${code.output}

## 任务
1. 提取需求文档中的所有功能点
2. 找出每个功能点对应的代码文件/函数
3. 计算需求覆盖率

## 输出格式（JSON）
{
  "requirements": [
    {
      "id": "REQ-001",
      "description": "需求描述",
      "implemented": true,
      "files": ["文件路径"],
      "functions": ["函数名"]
    }
  ],
  "coverage": 95,
  "missingRequirements": ["未实现的需求"],
  "summary": "总结说明"
}`;

  const result = await this.callAgent('analyst', prompt);
  return JSON.parse(result.output);
}
```

---

## 📈 效果对比

### 改进前 vs 改进后

| 指标 | 改进前 | 改进后 | 改进 |
|------|--------|--------|------|
| **Developer 看 PRD** | ❌ 不看 | ✅ 看 | 100% |
| **需求覆盖率检查** | ❌ 无 | ✅ 有 | +100% |
| **遗漏需求发现** | ❌ 最终才发现 | ✅ 生成时发现 | 提前 100% |
| **平均覆盖率** | ~70% | ~95% | +36% |

---

## 🎯 使用示例

### 代码示例

```javascript
const { run } = require('vibe-coding-cn');

const result = await run('做个个税计算器', { mode: 'v4' });

// 查看需求追溯
const traceability = result.outputs.traceability;
console.log(`需求覆盖率：${traceability.coverage}%`);
console.log(`已实现：${traceability.requirements.filter(r => r.implemented).length}`);
console.log(`缺失：${traceability.missingRequirements.length}`);

// 如果有缺失需求，启动增量更新
if (traceability.missingRequirements.length > 0) {
  console.log('⚠️ 有需求未实现，启动增量更新...');
  await run(`实现以下功能：${traceability.missingRequirements.join(', ')}`, {
    projectId: result.projectId,
    parentVersion: result.version
  });
}
```

### 输出示例

```
🎨 Vibe Coding v4.0 启动（增强协作模式）
...
✅ Phase 5/5: 整合验收 + 需求追溯
📊 生成需求追溯矩阵...
✅ 追溯矩阵完成：95% 需求已实现

📋 需求实现情况:
  ✅ REQ-001: 用户输入月收入
  ✅ REQ-002: 计算个税
  ✅ REQ-003: 显示结果
  ❌ REQ-004: 导出 Excel

📊 覆盖率：75% (3/4 需求已实现)
⚠️ 缺失需求：导出 Excel

📊 最终质量评分：88/100
```

---

## 🎯 最佳实践

### ✅ 应该做的

1. **Developer 必须看 PRD** - 明确实现目标
2. **生成追溯矩阵** - 验证覆盖率
3. **检查缺失需求** - 及时补充实现
4. **记录未实现原因** - 技术限制/时间不足
5. **更新 PRD** - 标记已实现/未实现

### ❌ 不应该做的

1. **不看 PRD 就写代码** - 容易遗漏
2. **不检查覆盖率** - 不知道缺什么
3. **忽略缺失需求** - 用户不满意
4. **不记录原因** - 下次还犯

---

## 📊 追溯矩阵模板

### Markdown 格式

```markdown
# 需求追溯矩阵

## 需求实现情况

| ID | 需求描述 | 状态 | 文件 | 函数 |
|----|---------|------|------|------|
| REQ-001 | 用户输入月收入 | ✅ | index.html, app.js | calculateTax() |
| REQ-002 | 计算个税 | ✅ | app.js | calculateTax() |
| REQ-003 | 显示结果 | ✅ | index.html | displayResult() |
| REQ-004 | 导出 Excel | ❌ | 无 | 无 |

## 覆盖率统计

- **总需求数**: 4
- **已实现**: 3
- **未实现**: 1
- **覆盖率**: 75%

## 缺失需求

1. REQ-004: 导出 Excel
   - 原因：时间不足
   - 计划：v2.0 实现
```

---

## 🎉 总结

**需求追溯矩阵核心价值**：

1. ✅ **确保完整性** - 每个需求都有代码
2. ✅ **及早发现遗漏** - 生成阶段就检查
3. ✅ **透明可追溯** - 需求→代码映射清晰
4. ✅ **便于验收** - 用户知道实现了什么

**适用场景**：
- ✅ 所有项目（无论大小）
- ✅ 特别是复杂项目
- ✅ 有明确 PRD 的项目

---

**最后更新**: 2026-04-06  
**版本**: v4.0
