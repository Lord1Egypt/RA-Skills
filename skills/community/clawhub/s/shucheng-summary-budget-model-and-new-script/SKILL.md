---
name: summary-budget-model-and-new-script
description: "用于总结和更新预算数据模型及脚本技能。当用户发出【总结对话内容】指令时，从对话历史中提取新的脚本写法、数据模型和字段信息，更新到 platform-script 和 budget-data-model 技能中。"
metadata: { "openclaw": { "emoji": "🔄", "requires": { "bins": [] } } }
---

# 预算模型与脚本总结技能

用于持续更新和迭代预算系统相关的两个核心技能。

## 何时使用

✅ **使用此技能的情况：**

- 用户发出【总结对话内容】指令
- 对话中出现了新的脚本写法或技巧
- 发现了新的数据表或字段
- 需要更新现有技能的参考内容
- 用户提供了新的业务逻辑或规则

## 工作流程

### 1. 触发条件

当用户发出以下指令时触发：
- 【总结对话内容】
- 【更新技能】
- 【记录新的脚本写法】
- 【保存这个数据模型】

### 2. 信息收集

从对话历史中提取以下信息：

#### 脚本操作类
- 新的 API 调用方式
- 特殊的数据处理逻辑
- 新的函数或工具类使用
- 脚本模板或最佳实践
- 错误处理和边界情况

#### 数据模型类
- 新的表名和表描述
- 新的字段名和字段类型
- 字段间的关联关系
- 数据验证规则
- 默认值和约束条件

### 3. 信息分类

将收集到的信息分类到：

**Platform Script Skills 更新内容：**
- 基础脚本操作新方法
- 表单脚本新技巧
- SQL 查询新写法
- 附件处理新函数
- 工作流程新脚本

**Budget Data Model Skills 更新内容：**
- 新数据表定义
- 新字段定义
- 表间关系说明
- 业务规则说明

### 4. 更新技能

#### 更新 Platform Script Skills

1. 读取 `skills/platform-script-skills/references/platform-script-templates.txt`
2. 在对应分类下追加新的脚本示例
3. 添加必要的注释和说明
4. 保存文件

#### 更新 Budget Data Model Skills

1. 读取 `skills/BudgetDataModelSkills/references/data_models.json`
2. 添加新的数据表定义（如适用）
3. 在现有表中添加新字段（如适用）
4. 保存 JSON 文件
5. 更新 SKILL.md 中的表说明

### 5. 记录更新日志

在 `references/update_log.md` 中记录：
- 更新日期
- 更新内容摘要
- 来源对话主题
- 更新人（AI 或用户）

## 更新规范

### 脚本更新格式

```groovy
// [新增] 功能描述
// 日期：YYYY-MM-DD
// 来源：对话主题

def 示例代码 = "实际代码示例"
```

### 数据模型更新格式

```json
{
  "table_id": "新表名",
  "table_name": "新表显示名",
  "description": "表描述",
  "fields": [
    {
      "field_id": "新字段名",
      "field_name": "新字段显示名",
      "data_type": "数据类型",
      "description": "字段描述"
    }
  ],
  "added_date": "YYYY-MM-DD",
  "source": "来源说明"
}
```

## 质量保证

### 验证检查

在更新前验证：

1. **脚本语法**：确保 Groovy/JavaScript 语法正确
2. **API 存在性**：确认使用的 API 函数确实存在
3. **字段命名**：遵循平台的命名规范
4. **数据类型**：确保数据类型定义准确
5. **无重复**：检查是否已存在相同内容

### 备份策略

更新前自动备份：
- 原文件备份到 `references/backup/` 目录
- 备份文件名包含时间戳
- 保留最近 10 个备份版本

## 使用示例

### 示例 1：总结对话内容

**用户：** 【总结对话内容】

**AI 响应：**
```
正在总结对话内容...

📝 发现新的脚本写法：
- 查询预算数据时使用 SQL 分页的新方法
- 处理空值的新的工具函数

📊 发现新的数据模型：
- 新增表：预算执行跟踪表
- 新增字段：预算调整原因（预算主表）

✅ 已更新：
- platform-script-skills/references/platform-script-templates.txt
- BudgetDataModelSkills/references/data_models.json
- references/update_log.md

下次查询时可使用这些新内容！
```

### 示例 2：手动添加脚本

**用户：** 记录这个脚本写法：[脚本内容]

**AI 响应：**
```
已记录新的脚本写法到 Platform Script Skills。

分类：数据查询
描述：使用 SQL 查询预算执行数据
日期：2026-03-28

下次查询预算执行数据时会自动使用此脚本模板。
```

## 相关文件

- `skills/platform-script-skills/` - 平台脚本技能目录
- `skills/BudgetDataModelSkills/` - 预算数据模型技能目录
- `references/update_log.md` - 更新日志
- `references/backup/` - 备份文件目录

## 注意事项

1. **不要删除旧内容**：只追加新内容，保留历史记录
2. **保持格式一致**：遵循现有文件的格式规范
3. **添加注释**：新内容要包含必要的注释说明
4. **验证后再更新**：确保新内容的正确性
5. **记录来源**：注明新内容的来源和背景

## 回滚机制

如果更新后发现问题：
1. 从 `references/backup/` 恢复最近的备份
2. 在 update_log.md 中记录回滚原因
3. 通知用户回滚操作
