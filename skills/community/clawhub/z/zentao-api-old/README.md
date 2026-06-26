# ZenTao API Client

禅道(ZenTao)项目管理系统的 Python API 客户端，支持产品、项目、任务、Bug、需求、测试、版本、发布全生命周期管理。

## 目录

- [特性](#特性)
- [支持的禅道版本](#支持的禅道版本)
- [安装](#安装)
- [接入方式](#接入方式)
  - [方式一：OpenClaw 接入（推荐）](#方式一openclaw-接入推荐)
  - [方式二：直接使用客户端](#方式二直接使用客户端)
- [功能概览](#功能概览)
- [状态流转](#状态流转)
- [注意事项](#注意事项)
- [常见问题](#常见问题)
- [项目结构](#项目结构)
- [许可证](#许可证)

---

## 特性

- 禅道老 API (Legacy API v1.0) 封装
- Session 认证方式
- **137+ 个 API 方法**，覆盖完整开发流程
- 返回格式统一处理（兼容 text/html 返回 JSON 的情况）
- 丰富的类型提示和文档注释
- 支持需求、任务、Bug、项目、测试、版本、发布、计划全流程管理

---

## 支持的禅道版本

本客户端基于禅道 **老 API (Legacy API v1.0)** 开发，兼容范围广泛。

### 兼容版本

| 版本类型   | 兼容版本    | 说明                  |
| ---------- | ----------- | --------------------- |
| **开源版** | 12.x - 20.x | 12.x 起全面支持老 API |
| **旗舰版** | 4.x - 7.x   | 全系列支持            |
| **企业版** | 13.x 及以上 | 企业版全系列支持      |
| **IPD版**  | 1.x - 5.x   | IPD 系列全支持        |

> **实测反馈**：禅道 12.3.3 版本测试通过。

### 关于新 API (v2.0)

禅道 **21.7+** 版本引入了全新的 **API v2.0**，采用 RESTful 风格和 Token 认证方式：

- **新 API (v2.0)**：禅道 21.7+ 推荐使用
- **老 API (v1.0)**：本客户端使用，21.7 仍可使用但逐步废弃

---

## 安装

### 环境要求

- Python 3.8+
- requests 库

### 安装依赖

```bash
pip install -r requirements.txt
```

或直接安装：

```bash
pip install requests>=2.28.0
```

---

## 接入方式

提供两种接入方式，推荐使用 **OpenClaw 接入**。

### 方式一：OpenClaw 接入（推荐）

OpenClaw 是一个智能开发助手，可以自动化执行禅道工作流。

#### 1. 配置凭证

在项目根目录创建 `TOOLS.md` 文件：

```markdown
## 禅道 API

- **API 地址：** http://your-zentao-host/
- **用户名：** your-username
- **密码：** your-password
```

#### 2. 使用示例

直接告诉 OpenClaw 你的需求，它会自动调用禅道 API：

```
用户：帮我创建一个用户登录功能的需求，包括前端和后端开发

OpenClaw：
✓ 已创建需求：用户登录功能开发 (ID: 123)
✓ 已创建任务：
  - 前端登录页面开发 (ID: 456)
  - 后端登录接口开发 (ID: 457)
  - 前后端联调 (ID: 458)
```

```
用户：记录一下今天做了什么

OpenClaw：
✓ 已记录工时：
  - 前端登录页面开发：3小时（剩余：0小时）
  - 任务状态已更新为：done
```

```
用户：有个bug，登录页面输入特殊字符报错

OpenClaw：
✓ 已创建Bug：登录页面输入特殊字符报错 (ID: 789)
  - 严重程度：3
  - 类型：代码错误
  - 指派给：admin
```

#### 3. 支持的工作流

OpenClaw 自动化支持完整的开发工作流：

```
需求管理 → 任务分解 → 任务执行 → 工时记录 → Bug管理 → 版本发布
    ↓          ↓          ↓          ↓          ↓          ↓
  创建需求   创建任务   开始/完成  记录工时   创建/解决  创建发布
  评审需求   分配任务   暂停/继续  验证工时   指派Bug    关联需求
  变更需求   移动任务   激活任务              关闭Bug    关联Bug
```

#### 4. 优势

- ✅ **自然语言交互**：无需编写代码，直接描述需求
- ✅ **自动化工作流**：自动创建需求、分解任务、记录工时
- ✅ **智能推荐**：根据上下文推荐最佳实践
- ✅ **完整流程追踪**：从需求到发布全程可追溯

#### 5. 常用命令示例

| 用户说 | OpenClaw 执行 |
|--------|--------------|
| "创建需求：xxx" | 创建需求 + 关联项目 |
| "分解任务" | 自动分解需求为多个任务 |
| "开始做xxx" | 查找任务 → 开始任务 |
| "记录今天的工时" | 记录工时 + 更新剩余时间 |
| "完成这个任务" | 记录最终工时 → 完成任务 |
| "有个bug：xxx" | 创建Bug → 关联需求/任务 |
| "bug已修复" | 解决Bug → 关闭Bug |
| "发布版本1.0" | 创建版本 → 关联需求/Bug → 创建发布 |

---

### 方式二：直接使用客户端

如果需要在代码中直接使用 API，可以使用 Python 客户端。

#### 1. 导入客户端

```python
from pathlib import Path
import sys

# 导入禅道客户端
lib_path = Path(__file__).parent / 'lib'
sys.path.insert(0, str(lib_path))
from zentao_client import ZenTaoClient, read_credentials

# 读取凭证
credentials = read_credentials()

# 创建客户端
client = ZenTaoClient(
    credentials['endpoint'],
    credentials['username'],
    credentials['password']
)

# 获取会话（首次登录，后续自动加载持久化的 Session）
sid = client.get_session()
print(f"登录成功，Session ID: {sid}")
```

#### 2. Session 持久化

客户端支持 Session 持久化，无需每次都登录：

```python
client = ZenTaoClient('http://127.0.0.1:8080', 'admin', 'password')

# 首次调用自动登录并保存 Session
sid = client.get_session()  # 登录 + 保存

# 新实例自动加载已有 Session
client2 = ZenTaoClient('http://127.0.0.1:8080', 'admin', 'password')
sid2 = client2.get_session()  # 直接加载，无需登录

# 强制刷新 Session
sid3 = client.get_session(force_refresh=True)  # 重新登录

# 清除保存的 Session
client.clear_session()
```

**存储位置**：项目根目录 `.zentao/sessions/` 目录下

```
项目目录/
├── .zentao/
│   └── sessions/
│       └── {hash}.json  # Session 文件
└── ...
```

#### 3. 快速示例

```python
# 创建需求
client.create_story(
    product_id="1",
    title="用户登录功能",
    execution_id="1",
    pri="3"
)

# 批量创建任务
client.create_tasks(
    project="1",
    tasks=[
        {"name": "前端开发", "type": "devel", "assignedTo": "admin", "estimate": "8"},
        {"name": "后端开发", "type": "devel", "assignedTo": "admin", "estimate": "16"},
        {"name": "测试", "type": "test", "assignedTo": "qa", "estimate": "4"}
    ]
)

# 开始任务
client.start_task(task_id, "开始开发")

# 记录工时
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
client.record_estimate(task_id, [
    {"date": today, "consumed": "8", "left": "0", "work": "完成开发"}
])

# 完成任务
client.finish_task(task_id, "开发完成")

# 创建Bug
client.create_bug(
    product_id="1",
    title="登录页面报错",
    severity="3",
    pri="3",
    assignedTo="admin"
)

# 解决Bug
client.resolve_bug(bug_id, "fixed", "trunk", "已修复")

# 关闭Bug
client.close_bug(bug_id, "验证通过")
```

---

## 功能概览

ZenTaoClient 提供 **137+ 个 API 方法**，覆盖完整的开发工作流：

### 核心模块

| 模块 | 方法数 | 主要功能 |
|-----|-------|---------|
| **任务管理** | 26个 | 创建、编辑、状态流转、工时记录、移动、复制、关联 |
| **Bug管理** | 18个 | 创建、编辑、状态流转、关联需求/任务、统计、评论 |
| **需求管理** | 13个 | 创建、编辑、变更、评审、关联项目/任务/Bug/用例 |
| **项目管理** | 13个 | 创建、编辑、成员管理、需求关联、团队、动态查询 |
| **测试管理** | 23个 | 测试用例、测试套件、测试任务、测试报告的CRUD操作 |
| **发布管理** | 9个 | 创建、编辑、关联需求/Bug |
| **版本管理** | 8个 | 创建、编辑、关联需求/Bug |
| **计划管理** | 7个 | 创建、编辑、关联需求 |
| **产品管理** | 7个 | 创建、编辑、查询 |

### 完整生命周期管理

✅ **需求管理**
- 创建、编辑、变更、评审需求
- 需求关联项目、任务、Bug、测试用例
- 需求状态查询和统计

✅ **任务管理**
- 创建任务、批量创建、创建子任务
- 任务状态流转：wait → doing → done → closed
- 任务移动、复制、指派
- 工时记录和管理

✅ **Bug管理**
- 创建Bug、从测试用例创建Bug
- Bug状态流转：active → resolved → closed
- Bug关联需求、任务
- Bug统计和评论

✅ **项目协作**
- 项目创建、编辑、启动、关闭
- 项目成员管理
- 项目需求关联
- 项目团队和动态查询

✅ **测试管理**
- 测试用例创建、编辑、批量创建
- 测试套件管理
- 测试任务创建和状态管理
- 测试报告

✅ **版本发布**
- 版本创建和管理
- 发布创建和管理
- 需求和Bug关联

详细 API 文档请参考：
- **新增接口清单**：`new_apis_added.md`
- **缺失接口清单**：`missing_apis.md`

---

## 状态流转

### 任务状态流转

```
wait ──开始──→ doing ──完成──→ done ──关闭──→ closed
  │              │    ↑
  │              │    │
  │              ↓    │
  │            pause ─┘
  │              ↑    
  │              └── 继续
  └──取消──→ cancel

done/closed ──激活──→ doing
```

### Bug 状态流转

```
active ──解决──→ resolved ──关闭──→ closed
  ↑                │
  │                │
  └──激活──────────┘
```

### 需求状态流转

```
draft ──评审──→ active ──开发──→ developed ──测试──→ testing ──发布──→ released
  │              │                │               │              │
  └──关闭────────┴────────────────┴───────────────┴──────────────┘
```

---

## 注意事项

### 1. 工时记录是批量接口

```python
# ✅ 正确：一次提交多条记录
client.record_estimate(task_id, [
    {"date": "2026-03-27", "consumed": "2", "left": "6", "work": "开发"},
    {"date": "2026-03-28", "consumed": "3", "left": "3", "work": "测试"}
])

# ❌ 错误：多次调用会覆盖之前记录
```

### 2. 完成任务前先记录工时

```python
# ✅ 正确流程
client.record_estimate(task_id, [
    {"date": today, "consumed": "8", "left": "0", "work": "完成"}
])
client.finish_task(task_id, "开发完成")
```

### 3. 验证操作结果

很多 API 返回 HTML 而非 JSON，建议用查询接口验证：

```python
success, result = client.start_task(task_id)
ok, task = client.get_task_detail(task_id)
print(task['status'])  # 验证是否为 'doing'
```

### 4. 统一的返回格式

所有 API 方法都返回 `(success, result)` 元组：

```python
success, result = client.create_task(...)

if success:
    print(f"操作成功: {result}")
else:
    print(f"操作失败: {result}")
```

---

## 常见问题

### Q: 认证失败怎么办？

```python
credentials = read_credentials()
print(credentials)  # 检查凭证是否正确

sid = client.get_session()
if not sid:
    print("认证失败，请检查用户名密码")
```

### Q: API 返回 success=False 但操作成功？

禅道老 API 有时返回 HTML 而非 JSON。解决方案：

1. 使用查询接口验证操作结果
2. 检查 `get_task_detail` 或 `get_bug` 的状态

### Q: 工时记录不生效？

确保参数格式正确：
- `date` 必须是 `YYYY-MM-DD` 格式
- `consumed` 和 `left` 必须是字符串

```python
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
```

### Q: 如何查看所有支持的 API？

```python
# 查看客户端所有方法
import inspect
for name, method in inspect.getmembers(client, predicate=inspect.ismethod):
    if not name.startswith('_'):
        print(name)
```

或参考以下文档：
- `new_apis_added.md` - 新增接口清单
- `missing_apis.md` - 缺失接口清单
- `SKILL.md` - OpenClaw 使用指南

---

## 项目结构

```
zentao-api/
├── lib/
│   └── zentao_client.py       # 核心客户端（137+ API方法）
├── docs/
│   └── *.md                    # 禅道 API 文档
├── scripts/                    # 辅助脚本
├── new_apis_added.md           # 新增接口清单
├── missing_apis.md             # 缺失接口清单
├── SKILL_UPDATE_SUMMARY.md     # SKILL 更新总结
├── SKILL.md                    # OpenClaw 使用指南
├── README.md                   # 本文件
├── package.json                # npm包配置
└── requirements.txt            # Python依赖
```

---

## 参考资料

- [禅道官网](https://www.zentao.net/)
- [禅道 API 文档 v1](https://zentao.net/book/apidoc-v1/apidoc-v1.html)
- [禅道二次开发手册](https://zentao.net/book/api/c634.html)
- [禅道 21.7 新 API v2.0](https://www.zentao.net/download/pms21.7.8-85834.html)

---

## 许可证

MIT License
