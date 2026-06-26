# 工作流程说明

本文档详细说明 weekly-report skill 的完整工作流程。

## 概述

周报生成系统执行以下步骤：

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   登录认证   │ -> │  获取数据   │ -> │  AI 总结   │ -> │  生成文档   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 详细流程

### Step 1: 登录认证

**目的**: 获取访问周报系统所需的认证 token

**流程**:
1. 检查本地是否有缓存的 token (`.token_cache` 文件)
2. 如果有缓存且未强制刷新，直接使用缓存
3. 否则启动浏览器自动化：
   - 打开登录页面
   - 等待用户手动登录（或自动填充凭据）
   - 监听网络请求，捕获 authorization header
   - 保存 token 和 cookies 到缓存

**输出**: `LoginResult` 对象，包含 token 和 cookies

**相关文件**:
- `lib/login.py` - 登录逻辑
- `.token_cache` - token 缓存文件

### Step 2: 获取数据

**目的**: 从周报系统获取指定时间范围的周报数据

**流程**:
1. 优先使用浏览器自动化方式：
   - 恢复登录时的 cookies
   - 导航到工作表页面
   - 拦截 API 响应获取数据
2. 如果浏览器方式失败，回退到直接 API 调用：
   - 构建请求体（包含分页、过滤条件）
   - 添加认证 header
   - 发送 POST 请求获取数据
3. 解析响应，转换为 `WeeklyReportItem` 列表
4. 根据 `team_members` 配置过滤非团队成员数据

**输出**: `WeeklyReportData` 对象，包含所有周报条目

**相关文件**:
- `lib/fetcher.py` - 数据获取逻辑
- `.data_cache` - 数据缓存文件

### Step 3: AI 总结

**目的**: 使用 LLM 将原始周报数据提炼为结构化总结

**流程**:
1. 格式化原始数据为 prompt
   - 过滤非团队成员
   - 提取关键字段
2. 构建 system prompt（定义工作分类和输出格式）
3. 调用 LLM API 进行总结
4. 解析 LLM 返回的 JSON 结果
5. 构建 `WorkCategories` 对象

**工作分类**:
- 人才转型: AI培训、技能学习、人才培养
- 自主开发: 自主开发的应用、工具、系统
- 科创支撑: 专利申报、创新项目、科创制度
- AI架构及网运安全自智规划: AI架构、监控智能化、态势感知
- 系统需求规划建设: 系统需求分析、平台建设
- 综合工作: 日常运维、综合事务、其他

**输出**: `SummarizedReport` 对象，包含结构化的周报总结

**相关文件**:
- `lib/summarizer.py` - AI 总结逻辑
- `lib/llm_client.py` - LLM 客户端

### Step 4: 生成文档

**目的**: 生成格式化的 Word 文档

**流程**:
1. 创建新文档或加载模板
2. 设置默认字体（仿宋_GB2312）
3. 添加标题（监控调度室周工作总结计划）
4. 添加"本周主要工作总结"章节
5. 添加"下周主要工作计划"章节
6. 每个章节按分类列出工作内容
7. 保存文档到输出目录

**输出**: `.docx` 文件

**相关文件**:
- `lib/generator.py` - 文档生成逻辑
- `assets/template.docx` - 可选模板文件

## 数据模型

### WeeklyReportItem

原始周报条目：

```python
class WeeklyReportItem:
    row_id: str          # 行 ID
    create_time: str     # 创建时间
    owner_id: str        # 提交者 ID (JSON 格式)
    owner_name: str      # 提交者姓名
    # ... 其他动态字段
```

### DateRange

日期范围：

```python
class DateRange:
    start_date: date     # 开始日期（周一）
    end_date: date       # 结束日期（周日）
```

### CategoryItem

分类条目：

```python
class CategoryItem:
    content: str         # 工作内容
    person: str          # 人员姓名
```

### WorkCategories

工作分类集合：

```python
class WorkCategories:
    人才转型: List[CategoryItem]
    自主开发: List[CategoryItem]
    科创支撑: List[CategoryItem]
    AI架构及网运安全自智规划: List[CategoryItem]
    系统需求规划建设: List[CategoryItem]
    综合工作: List[CategoryItem]
```

### SummarizedReport

最终报告：

```python
class SummarizedReport:
    week_range: DateRange      # 日期范围
    team_name: str             # 团队名称
    this_week: WorkCategories  # 本周工作
    next_week: WorkCategories  # 下周计划
    overview: str              # 工作概述
    issues: str                # 遇到的问题
    raw_items_count: int       # 原始条目数量
```

## 错误处理

### 登录失败

- **超时**: 用户未在指定时间内完成登录
- **Token 捕获失败**: 未能在网络请求中找到认证 token
- **解决**: 使用 `--force-login` 重新登录

### 数据获取失败

- **API 错误**: 认证失效或网络问题
- **空数据**: 指定时间范围无周报提交
- **解决**: 检查网络连接，确认登录状态

### AI 总结失败

- **API Key 无效**: 检查 `DEEPSEEK_API_KEY` 环境变量
- **JSON 解析失败**: LLM 返回格式不正确
- **解决**: 重试或检查 API 配置

### 文档生成失败

- **模板不存在**: 检查 `template.docx` 文件
- **权限问题**: 检查输出目录写权限
- **解决**: 确认文件路径和权限

## 输出格式

### JSON 输出（标准输出）

```json
{
  "success": true,
  "output_file": "output/周报_科创研发组_2026-03-02-2026-03-08.docx",
  "items_count": 25,
  "filtered_count": 25,
  "week_range": "2026.03.02-2026.03.08",
  "error": null
}
```

### 文档输出

生成的 Word 文档包含：

1. **标题**: 监控调度室周工作总结计划（日期范围）
2. **一、本周主要工作总结**
   - 科创团队
   - 1、人才转型
     - （1）工作内容--人员
   - 2、自主开发
   - ...
3. **二、下周主要工作计划**
   - 结构同上

## 缓存机制

### Token 缓存

- **文件**: `.token_cache`
- **内容**: JSON 格式的 token 和 cookies
- **用途**: 避免每次都需要重新登录
- **清除**: `python login.py --logout` 或删除文件

### 数据缓存

- **文件**: `.data_cache`
- **内容**: JSON 格式的原始周报数据
- **用途**: 调试和数据分析
- **注意**: 每次运行会覆盖

## 性能优化

1. **Token 复用**: 使用缓存避免重复登录
2. **浏览器复用**: 单次运行中复用浏览器实例
3. **并行请求**: API 分页请求可并行处理（未来优化）
4. **增量更新**: 支持增量获取新数据（未来优化）
