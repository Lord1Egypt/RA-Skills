# create-feishu-doc - 飞书文档创建技能

_版本：V1.0 | 创建时间：2026-03-08 | 状态：已上线_

---

## 📋 技能描述

创建飞书文档时，**必须分块写入**（block by block），不能一次性长文本写入。

**原因：**
- 飞书 API 对单次写入长度有限制
- 分块写入更稳定，错误易定位
- 便于后续增量更新（定位到具体 block）

**实战经验（2026-03-08）：**
- 一次性长文本写入会导致文档空白
- 分块写入：5 个项目文档，468 个 blocks，全部成功
- 平均每文档 90-100 个 blocks

---

## 🎯 工作流程

### **Step 1: 创建空文档**
```powershell
# 调用飞书 API 创建空文档
POST /open-apis/docx/v1/documents
{
  "title": "文档标题"
}

# 返回 document_id 和 root_block_id
```

### **Step 2: 拆分内容为 blocks**
```markdown
# 原始内容
# 标题 1
内容 1

# 标题 2
内容 2

# 拆分为 blocks
Block 1: 标题 1
Block 2: 内容 1
Block 3: 标题 2
Block 4: 内容 2
```

### **Step 3: 逐个写入 blocks**
```powershell
# 写入每个 block
POST /open-apis/docx/v1/documents/{document_id}/blocks
{
  "parent_block_id": "root_block_id",
  "block": {
    "block_type": "text",
    "text": {
      "elements": [{
        "text_run": {
          "content": "内容",
          "style": { "bold": true }
        }
      }]
    }
  }
}
```

### **Step 4: 验证写入**
```powershell
# 读取文档确认
GET /open-apis/docx/v1/documents/{document_id}

# 检查 block 数量
```

---

## 📁 Block 类型映射

| Markdown | 飞书 Block 类型 | 说明 |
|----------|----------------|------|
| `# 标题` | `heading1` | 一级标题 |
| `## 标题` | `heading2` | 二级标题 |
| `### 标题` | `heading3` | 三级标题 |
| 普通文本 | `text` | 普通段落 |
| `- 列表` | `bullet` | 无序列表 |
| `1. 列表` | `ordered` | 有序列表 |
| `| 表格 |` | `table` | 表格 |
| `---` | `divider` | 分割线 |
| `> 引用` | `quote` | 引用块 |

---

## ⚙️ 配置项

### **分块策略**
- **最大 block 大小**：5000 字符
- **超时重试**：3 次
- **错误处理**：记录失败 block，继续写入后续

### **性能优化**
- **批量写入**：每 10 个 block 批量提交
- **并发控制**：串行写入（避免顺序错乱）
- **进度跟踪**：实时显示写入进度（30% → 100%）

---

## 🧪 测试用例

### **测试 1：简单文档**
```
输入：标题 + 2 段内容
预期：3 个 blocks，全部写入成功
```

### **测试 2：复杂文档**
```
输入：标题 + 表格 + 列表 + 引用
预期：多种 block 类型，正确渲染
```

### **测试 3：长文档**
```
输入：10000 字符内容
预期：自动拆分为多个 blocks，全部写入
```

---

## 📊 监控指标

- **创建成功率**：目标 100%
- **平均创建时间**：<10 秒/文档
- **Block 写入成功率**：>99%

---

## 🚀 使用示例

### **创建项目立项报告**
```powershell
# 调用示例
New-FeishuDoc -Title "数据治理 - 小米汽车 立项报告" `
  -Content $markdownContent `
  -SplitBlocks $true

# 返回
{
  "document_id": "U9PIdZ5SooMa9TxTXabcv8TGnhb",
  "url": "https://feishu.cn/docx/...",
  "blocks_written": 25
}
```

---

## ⚠️ 注意事项

1. **不要一次性写入长文本**（会失败或空白）
2. **必须拆分 blocks**（按段落、标题、表格）
3. **写入后验证**（确认 block 数量）
4. **错误重试**（网络波动时自动重试）

---

## 🔄 与 project-triple-sync 集成

当 project-triple-sync 需要更新飞书文档时：
1. 读取 MD 内容
2. 对比现有 blocks
3. **增量更新**（只更新变更的 blocks）
4. 维护版本记录

---

_本技能由阿福开发，遵循飞书 API 最佳实践_


---

## 🎯 2026-03-14 重大更新（Thomas 要求）

### Thomas 的完整文档偏好（今日固化）

**1. 拆分 Block 写入（16:10 要求）**
- ✅ 每个章节独立 Block
- ✅ 使用 append 多次调用
- ✅ 禁止一次性写入整个文档
- ✅ 目标：5+ 个 Block

**2. 开通编辑权限（多次强调）**
- ✅ create 时设置 grant_to_requester: true
- ✅ 参数位置正确（顶层）
- ✅ 验证 Thomas 有编辑权限

**3. 表格创建方式（16:58 要求 + 19:00 更新）**

**根据场景选择合适方式：**

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| **简单表格**（≤5 行×5 列） | Markdown 语法 | 飞书自动渲染，快速便捷 |
| **复杂表格**（>5 行或需要样式） | `create_table + write_table_cells` | 分两步，支持公式/样式 |

**简单表格示例（Markdown）：**
```markdown
| 姓名 | 年龄 | 城市 |
|------|------|------|
| Thomas | 30 | 上海 |
```

**复杂表格示例（两步流程）：**
```powershell
# 步骤 1：创建表格框架
feishu_doc --action create_table --doc_token $docId --row_size 5 --column_size 3

# 步骤 2：写入表格数据
feishu_doc --action write_table_cells --doc_token $docId --table_block_id tbl_xxx --values [["姓名","年龄","城市"],["Thomas","30","上海"]]
```

**Thomas 最新要求（19:00）：**
- ✅ 优先使用 `create_table + write_table_cells`
- ✅ 确保表格正常显示（无空白）
- ✅ 验证数据写入成功

**4. 文件编辑用 Out-File（16:16 要求）**
- ✅ 禁止使用 edit 工具
- ✅ 使用 PowerShell Out-File
- ✅ 强制 UTF8 编码
- ✅ 验证写入成功

**5. 强制记忆检索（16:37 要求）**
- ✅ 创建文档前调用 memory_search
- ✅ 查询历史教训
- ✅ 避免重复犯错

---

### 完整检查清单（2026-03-14 版）

**创建前检查：**
- [ ] 调用 memory_search 查询历史教训
- [ ] 规划 Block 结构（5+ 个 Block）
- [ ] 使用 create 动作（不是 write）
- [ ] 设置 grant_to_requester: true
- [ ] 参数位置正确（顶层）
- [ ] folder_token 正确
- [ ] 标题不为空

**创建中检查：**
- [ ] 使用 append 多次调用
- [ ] 每个章节独立 Block
- [ ] 表格创建方式选择：
  - 简单表格 → Markdown 语法
  - 复杂表格 → `create_table + write_table_cells`
- [ ] 图 + 文分离
- [ ] 验证表格数据写入成功

**创建后验证：**
- [ ] 返回 doc_token
- [ ] 确认 grant_to_requester: true
- [ ] Thomas 有编辑权限
- [ ] Block 数量 >= 5
- [ ] 表格正常显示（无空白）
- [ ] 链接可以打开

---

### 历史问题统计（2026-02-20 至 2026-03-14）

| 问题类型 | 次数 | Thomas 提醒次数 |
|---------|------|--------------|
| 未拆分 Block | 27 次 | 14 次 |
| 权限问题 | 24 次 | 13 次 |
| 表格空白 | 多次 | 多次 |

**成功率：**
- 2/20 - 3/13: 42%
- 3/14（应用 Best Practice 后）: 100%

---

### 根本原因分析（2026-03-14 16:45）

**5 大系统缺陷：**
1. SKILL.md 无规范（直到 16:16 才添加）
2. 工具设计缺陷（write 不支持自动拆分）
3. 无验证机制（没有自动化验证 Block 数量）
4. 记忆检索缺失（没有主动调用 memory_search）
5. 错误成本低（重新创建成本由用户承担）

**解决方案：**
- ✅ SKILL.md 规范（已添加）
- ✅ 强制记忆检索（立即执行）
- ✅ 创建后验证（立即执行）
- ⏳ 工具增强（建议开发）
- ⏳ 错误追踪（建议开发）

---

**记住：这是 Thomas 的强制要求！永久生效！**
