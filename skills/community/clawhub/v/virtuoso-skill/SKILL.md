---
name: virtuoso-skill
description: Cadence Virtuoso Skill语言开发辅助工具，包含API查询、代码校验、智能补全功能。使用场景：(1) 编写/调试Virtuoso Skill代码；(2) 检查API调用是否合法；(3) 查询Skill函数的用法和参数；(4) 避免API幻觉和未定义函数调用。
---

# Virtuoso Skill开发辅助工具

本工具提供Virtuoso Skill开发的全流程支持，从根源解决API幻觉问题。

## 功能特性

### 1. 🤖 智能API推荐（新增）
**根据你的自然语言描述，自动推荐最合适的Skill函数！**
- 输入"我想打开单元视图"，直接告诉你应该用 `dbOpenCellView`
- 输入"创建版图矩形"，推荐 `leCreateRect`
- 支持模糊匹配，即使描述不准确也能找到相关函数
- 提供完整的语法、参数说明和示例代码

### 2. 🔍 API校验（核心功能）
自动检查Skill代码中的函数调用是否合法：
- 识别未定义的函数调用
- 检查参数数量是否正确
- 提示参数类型不匹配问题
- 给出错误原因和修复建议

### 3. 📚 API查询
支持按关键词搜索Skill函数：
- 函数功能描述
- 完整语法和参数说明
- 示例代码
- 注意事项和常见问题

## 使用方法

### 智能API推荐（聊天机器人）

#### 交互模式（推荐日常使用）
```bash
skill_chatbot.py
```
进入交互式查询，你可以直接输入自然语言描述：
```
您> 我想要打开一个单元视图
根据您的描述，找到以下最匹配的Skill API：
[显示dbOpenCellView完整信息]
```

#### 直接查询
```bash
skill_chatbot.py --query "打开单元视图"
skill_chatbot.py -q "创建版图矩形"
```

#### 启动Web图形界面
```bash
skill_chatbot.py --web --port 8080
```
然后在浏览器打开 `http://your-server:8080` 即可使用图形化界面查询。

### API代码校验

#### 检查单个Skill文件
```bash
skill_lint.py --file your_code.il
```

#### 检查整个目录下的Skill文件
```bash
skill_lint.py --dir ./your_project/
```

#### 检查代码片段
```bash
skill_lint.py --code "(dbOpenCellView \"mylib\" \"mycell\" \"schematic\" \"r\")"
```

#### 列出所有支持的函数
```bash
skill_lint.py --list-functions
```

## API覆盖范围
当前包含312个常用Skill API，覆盖：
- 基础函数（字符串、列表、文件操作等）
- 数据库操作API（db* 系列函数）
- 版图操作API（le*、ge* 系列函数）
- 原理图操作API（sch* 系列函数）
- 界面操作API（hi* 系列函数）

## 开发规范
1. **必须使用已定义的API**：禁止使用任何不在API数据库中的函数
2. **参数必须匹配**：严格按照文档提供参数数量和类型
3. **提交前必须检查**：所有Skill代码提交前必须通过`skill_lint.py`检查
4. **遇到未定义API**：请反馈到技术团队，不要自行编造

## 错误示例与修复
### ❌ 错误示例：
```skill
; 错误：使用了未定义的函数 dbOpenCell
(dbOpenCell "mylib" "mycell" "r")

; 错误：参数数量不足
(dbOpenCellView "mylib" "mycell" "schematic")
```

### ✅ 正确示例：
```skill
; 正确：使用合法的API并提供完整参数
(dbOpenCellView "mylib" "mycell" "schematic" "r")
```

## 更新说明
API数据库会持续更新，支持更多函数和功能。如有API缺失或错误，请及时反馈。
