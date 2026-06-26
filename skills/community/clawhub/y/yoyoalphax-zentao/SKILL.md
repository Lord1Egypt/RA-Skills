---
name: zentao
description: ZenTao Project Management API Integration | 禅道-ZenTao 项目管理 API 集成。Query products, projects, executions, stories, tasks, bugs / 查询产品、项目、执行、需求、任务、缺陷等。Triggers: 禅道，zentao, project management
license: MIT
version: 1.0.4
author: yoyoalphax
config:
  required_files:
    - path: TOOLS.md
      description: ZenTao API credentials configuration file | 禅道 API 凭证配置文件
      required_sections:
        - "## 禅道 API"
        - "## ZenTao API"
  dependencies:
    - python3
    - requests
    - beautifulsoup4
---

# ZenTao Project Management Skill (禅道-ZenTao 项目管理技能)

> 首先，感谢禅道团队多年的深耕与付出。没有你们孜孜不倦的耕耘和维护，就没有这款优秀的项目管理工具。禅道作为国内领先的开源项目管理解决方案，帮助无数团队提升了协作效率，这份贡献值得我们致以最诚挚的敬意。🙏

> **English Version** | 英文版 (Primary)  
> **Chinese Version** | 中文版 (Below)

---

## 🇬🇧 English Version

### Quick Start

This skill integrates both legacy ZenTao API and REST API, providing unified project management query interfaces.

#### Installation

**Prerequisites:**
- Python 3.8+
- pip (Python package manager)

**Install Dependencies:**
```bash
# Option 1: Using requirements.txt (recommended)
pip3 install -r requirements.txt

# Option 2: Manual install
pip3 install requests beautifulsoup4
```

#### Credentials Configuration

ZenTao API credentials are stored in the `TOOLS.md` file:

```markdown
## 禅道 API (ZenTao API)

- **API URL:** http://<your-zentao-host>/
- **Username:** <your-username>
- **Password:** <your-password>
```

**⚠️ Security Notice:** Do not commit API credentials to version control or share them publicly.

#### Usage Examples

**Query Product List**
```
ZenTao product list
Query all products in ZenTao
zentao products
```

**Query Project List**
```
ZenTao project list
Query active projects
zentao projects status=doing
```

**Query Stories List**
```
ZenTao stories project=<project-name>
Query stories for product=<your-product-name>
```

**Query Tasks List**
```
ZenTao tasks execution=<execution-id>
Query tasks for project=<your-project-name>
```

**Query Bugs List**
```
ZenTao bugs product=<product-name>
Query bugs for product=<your-product-name>
```

**Create Story (Requires Confirmation)**
```
ZenTao create story product=<product-name> execution=<execution-id> title=[New Feature] Test story plan=<date>
```

**Create Task (Requires Confirmation)**
```
ZenTao create task execution=<execution-id> story=<story-id> title=Development task assign=<username>
```

### Features

#### Query Operations (No Confirmation Required)

**User**
- Get user list
- Get user info
- Get my personal info

**Program**
- Get program list
- Get program info

**Product**
- Get product list
- Get product info
- Get product teams
- Get product plans
- Get stories list
- Get bugs list
- Get releases list
- Get test cases list
- Get test tasks list
- Get feedbacks list
- Get tickets list

**Project**
- Get projects list
- Get project info
- Get project stories
- Get executions list
- Get builds list

**Execution**
- Get executions list
- Get execution info
- Get tasks list
- Get bugs list
- Get builds list

**Task**
- Get tasks list
- Get task

**Bug**
- Get bug

**Build**
- Get build

**Test Case**
- Get test case

**Test Task**
- Get test task

**Feedback**
- Get feedback

**Ticket**
- Get ticket

#### Action Operations (Confirmation Required)

**User Management**
- Create user
- Update user info
- Delete user

**Program Management**
- Create program
- Update program
- Delete program

**Product Management**
- Create product
- Update product
- Delete product
- Create product plan
- Update product plan
- Delete product plan
- Create story
- Update story
- Delete story
- Activate story
- Close story

**Project Management**
- Create project
- Update project
- Delete project
- Create build
- Update build
- Delete build

**Execution Management**
- Create execution
- Update execution
- Delete execution
- Create task
- Update task
- Delete task

**Bug Management**
- Create bug
- Update bug
- Delete bug

**Test Management**
- Create test case
- Update test case
- Delete test case
- Create test task
- Run test case

**Feedback & Ticket**
- Create feedback
- Update feedback
- Delete feedback
- Create ticket
- Update ticket
- Delete ticket

### Workflow

1. **Read Credentials** - Get ZenTao API credentials from TOOLS.md
2. **Parse Command** - Parse user command and parameters
3. **Authenticate** - Get Token via REST API or Session via legacy API
4. **Execute** - Call corresponding API endpoints
5. **Output** - Return formatted results

### API Documentation

**REST API (Preferred)**
- **Authentication:** Token
- **Endpoint:** `/api.php/v1/`
- **Use Cases:** Users, products, projects, executions, builds queries

**Legacy API (Compatibility)**
- **Authentication:** Session/Cookie
- **Endpoint:** `/api-*.json`
- **Use Cases:** Stories, tasks, bugs, releases queries

### Output Format

**Product List**
```
✅ ZenTao product query completed
Found N products:
| ID | Product Name |
|----|--------------|
| 21 | <Your Product Name> |
| ... | ... |
```

**Project List**
```
✅ ZenTao project query completed
Found N projects:
| ID | Project Name | Status |
|----|--------------|--------|
| 176 | <Your Project Name> | doing |
| ... | ... | ... |
```

### Error Handling

- **Missing Credentials:** Prompt user to configure ZenTao API credentials in TOOLS.md
- **Authentication Failed:** Check username and password
- **API Connection Failed:** Check network and API URL
- **No Data:** May be permission issue or no data in time range

### Notes

1. Configure ZenTao API credentials in TOOLS.md before first use
2. All create/update/delete operations require user confirmation
3. REST API is preferred, legacy API for compatibility
4. Query time range recommended not to exceed 1 year (large data volume)

---

## 🇨🇳 中文版

### 快速开始

本技能整合禅道老 API 和 REST API，提供统一的项目管理查询接口。

#### 安装步骤

**前置要求：**
- Python 3.8+
- pip (Python 包管理器)

**安装依赖：**
```bash
# 方式 1：使用 requirements.txt（推荐）
pip3 install -r requirements.txt

# 方式 2：手动安装
pip3 install requests beautifulsoup4
```

#### 凭证配置

禅道 API 凭证存储在 `TOOLS.md` 文件中：

```markdown
## 禅道 API

- **API 地址：** http://<your-zentao-host>/
- **用户名：** <your-username>
- **密码：** <your-password>
```

**⚠️ 安全提醒：** 不要将 API 凭证提交到版本控制或公开分享。

#### 使用示例

**查询产品列表**
```
禅道产品列表
查询禅道所有产品
zentao products
```

**查询项目列表**
```
禅道项目列表
查询进行中的项目
zentao projects status=doing
```

**查询需求列表**
```
禅道需求列表 项目=<项目名称>
查询禅道需求 产品=<你的产品名称>
```

**查询任务列表**
```
禅道任务列表 执行=<执行 ID>
查询禅道任务 项目=<你的项目名称>
```

**查询缺陷列表**
```
禅道缺陷列表 产品=<产品名称>
查询禅道 bug 产品=<你的产品名称>
```

**新建需求（需要确认）**
```
禅道新建需求 产品=<产品名称> 执行=<执行 ID> 标题=【新功能】测试需求 计划=<日期> 版本
```

**新建任务（需要确认）**
```
禅道新建任务 执行=<执行 ID> 需求=<需求 ID> 标题=开发任务 指派=<用户名>
```

> **注意：** 参数中的数字 ID（如产品 ID、执行 ID、需求 ID 等）可以直接使用对应的名称替代，系统会自动识别。
> 例如：`产品=21` 可以写成 `产品=IDS_投资决策支持系统`

### 功能列表

#### 查询类（无需确认）

**用户 User**
- 获取用户列表
- 获取用户信息
- 获取我的个人信息

**项目集 Program**
- 获取项目集列表
- 获取项目集信息

**产品 Product**
- 获取产品列表
- 获取产品信息
- 获取产品团队
- 获取产品计划列表
- 获取需求列表
- 获取 Bug 列表
- 获取发布列表
- 获取用例列表
- 获取测试单列表
- 获取反馈列表
- 获取工单列表

**项目 Project**
- 获取项目列表
- 获取项目信息
- 获取项目需求列表
- 获取项目执行列表
- 获取项目版本列表

**执行 Execution**
- 获取执行列表
- 获取执行信息
- 获取执行任务列表
- 获取执行 Bug 列表
- 获取执行版本列表

**任务 Task**
- 获取任务列表
- 获取任务

**缺陷 Bug**
- 获取 Bug

**版本 Build**
- 获取版本

**用例 TestCase**
- 获取用例

**测试单 TestTask**
- 获取测试单

**反馈 Feedback**
- 获取反馈

**工单 Ticket**
- 获取工单

#### 操作类（需要确认）

**用户管理**
- 创建用户
- 修改用户信息
- 删除用户

**项目集管理**
- 创建项目集
- 修改项目集
- 删除项目集

**产品管理**
- 创建产品
- 修改产品
- 删除产品
- 创建产品计划
- 修改产品计划
- 删除产品计划
- 创建需求
- 修改需求
- 删除需求
- 激活需求
- 关闭需求

**项目管理**
- 创建项目
- 修改项目
- 删除项目
- 创建版本
- 修改版本
- 删除版本

**执行管理**
- 创建执行
- 修改执行
- 删除执行
- 创建任务
- 修改任务
- 删除任务

**缺陷管理**
- 创建 Bug
- 修改 Bug
- 删除 Bug

**测试管理**
- 创建用例
- 修改用例
- 删除用例
- 创建测试单
- 执行用例

**反馈与工单**
- 创建反馈
- 修改反馈
- 删除反馈
- 创建工单
- 修改工单
- 删除工单

### 工作流程

1. **读取凭证** - 从 TOOLS.md 获取禅道 API 凭证
2. **解析命令** - 解析用户命令和参数
3. **认证登录** - 使用 REST API 获取 Token 或老 API 获取 Session
4. **执行操作** - 调用对应 API 接口
5. **输出结果** - 返回格式化的结果

### API 说明

**REST API (优先使用)**
- **认证方式：** Token
- **接口路径：** `/api.php/v1/`
- **适用场景：** 用户、产品、项目、执行、版本等查询

**老 API (兼容模式)**
- **认证方式：** Session/Cookie
- **接口路径：** `/api-*.json`
- **适用场景：** 需求、任务、缺陷、发布计划等

### 输出格式

**产品列表**
```
✅ 禅道产品查询完成
共查询到 N 个产品：
| ID | 产品名称 |
|----|---------|
| 21 | <你的产品名称> |
| ... | ... |
```

**项目列表**
```
✅ 禅道项目查询完成
共查询到 N 个项目：
| ID | 项目名称 | 状态 |
|----|---------|------|
| 176 | <你的项目名称> | doing |
| ... | ... | ... |
```

### 错误处理

- **凭证缺失：** 提示用户在 TOOLS.md 中配置禅道 API 凭证
- **认证失败：** 检查用户名密码是否正确
- **API 连接失败：** 检查网络连接和 API 地址
- **无数据返回：** 可能是权限问题或时间范围内无数据

### 注意事项

1. 首次使用需在 TOOLS.md 中配置禅道 API 凭证
2. 所有新增、新建、删除操作都需要用户确认
3. 建议优先使用 REST API，老 API 作为兼容
4. 查询时间范围建议不超过 1 年（数据量较大）

---

## License | 许可证

MIT-0 · MIT No Attribution

Free to use, modify, and redistribute. No attribution required.

免费使用、修改和重新分发。无需署名。
