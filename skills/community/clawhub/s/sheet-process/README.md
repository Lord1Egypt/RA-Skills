# sheet-process

腾讯文档智能表格通用筛选处理 Skill — 将表格筛选功能抽象为可编排的工作流节点。

## 模式

| 模式 | 触发词 | 说明 |
|------|--------|------|
| **工作流模式** | `sheet-process` | 一键输出 JSON，适合作为下游 AI 节点输入 |
| **原子模式** | `表格筛选`、`表格处理`、`表格过滤` | 引导式问答，可自定义输出格式（JSON/HTML 等） |

## 工作流程

1. 确认腾讯文档连接状态
2. 选定要筛选的工作表（多 sheet 时交互选择）
3. 填写参数模板（筛选列、关键词、取并集/交集、输出列）
4. 执行筛选并输出结果

## 输出格式

- **工作流模式**：结构化 JSON（含 meta 元数据 + records 数组 + 匹配详情）
- **原子模式**：用户自定义（JSON / HTML / 等）

## 依赖

- WorkBuddy「腾讯文档」连接器
- 依赖 `tencentdocs.py`（随 WorkBuddy 内置）

## 安装

```bash
# 克隆到 WorkBuddy skills 目录
git clone https://github.com/liuyi-arch/sheet-process.git ~/.workbuddy/skills/sheet-process
```

## 使用示例

```
# 工作流模式
@tdoc#xxx sheet-process

# 原子模式
@tdoc#xxx 帮我筛选表格中岗位含"前端"的企业
```
