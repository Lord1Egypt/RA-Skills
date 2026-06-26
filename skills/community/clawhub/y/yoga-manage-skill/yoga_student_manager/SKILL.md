---
name: yoga-student-manager
description: "瑜伽老师专用学员课时管理系统。使用SQLite本地存储学员信息、课程套餐（包年/包课时）和课时扣除日志，每次扣课后自动发送邮件记录。"
---

## 瑜伽学员课时管理系统

这是一个为瑜伽老师设计的轻量级学员管理工具，使用 SQLite 本地数据库存储，支持：

- 学员基本信息管理（姓名、电话、微信、备注）
- 多种课程类型：线上课 / 线下课
- 两种套餐模式：包年 / 包课时
- 包课时课程自动扣除课时并记录日志
- 每次扣除后自动发送邮件记录给自己
- 手动发送完整学员报表

### 首次配置

**安装后必须先配置邮箱**，否则无法发送课时记录邮件。

使用交互式配置：
```python
from config import prompt_email_config
prompt_email_config()
```

或手动配置：
```python
from config import set_email_config
set_email_config(
    smtp_server="smtp.qq.com",
    smtp_port=587,
    email="your_email@qq.com",
    password="your_auth_code",
    use_ssl=True
)
```

常用邮箱SMTP设置参考：
- Gmail: `smtp.gmail.com`, 端口 `587`（需开启应用专用密码）
- QQ邮箱: `smtp.qq.com`, 端口 `587`（需使用授权码而非登录密码）
- 163邮箱: `smtp.163.com`, 端口 `25`
- Outlook: `smtp.office365.com`, 端口 `587`

### 命令行使用

运行主程序：
```bash
python main.py
```

首次运行会提示配置邮箱。之后进入交互式菜单：
1. 添加学员
2. 查看所有学员
3. 查看学员详情
4. 修改学员信息
5. 删除学员
6. 添加课程
7. 扣除课时
8. 增加课时
9. 查看扣除记录
10. 发送完整报表
11. 配置邮箱
0. 退出

### Python API 使用

```python
from manager import YogaManager

manager = YogaManager()

# 添加学员
sid = manager.add_student("张三", phone="13800138000", wechat="zhangsan123")

# 添加包课时课程（线下课，50课时）
cid = manager.add_course(
    student_id=sid,
    course_type="offline",   # 或 "online"
    package_type="hourly",   # 或 "yearly"
    total_hours=50,
    remaining_hours=50,
    price=5000.00
)

# 扣除课时（每次上完课调用）
result = manager.deduct_hours(course_id=cid, hours=1, notes="哈他瑜伽基础课")
# 扣除成功后会自动发送邮件记录

# 添加包年课程
manager.add_course(
    student_id=sid,
    course_type="online",
    package_type="yearly",
    start_date="2026-01-01",
    end_date="2026-12-31",
    price=8000.00
)

# 查看学员详情
manager.show_student(sid)

# 发送完整报表
manager.send_full_report()
```

### 数据库结构

SQLite 数据库文件：`yoga_students.db`

**students 表** - 学员基本信息
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 姓名 |
| phone | TEXT | 电话 |
| wechat | TEXT | 微信 |
| notes | TEXT | 备注 |
| created_at | TEXT | 创建时间 |

**student_courses 表** - 学员课程信息
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学员ID（外键） |
| course_type | TEXT | online/offline |
| package_type | TEXT | yearly/hourly |
| total_hours | INTEGER | 总课时（包课时） |
| remaining_hours | INTEGER | 剩余课时（包课时） |
| start_date | TEXT | 开始日期（包年） |
| end_date | TEXT | 结束日期（包年） |
| price | REAL | 价格 |

**deduction_logs 表** - 课时扣除日志
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学员ID |
| course_id | INTEGER | 课程ID |
| deducted_hours | INTEGER | 扣除课时数 |
| remaining_before | INTEGER | 扣除前剩余 |
| remaining_after | INTEGER | 扣除后剩余 |
| class_date | TEXT | 上课日期 |
| notes | TEXT | 备注 |
| created_at | TEXT | 记录时间 |

### 文件结构

```
yoga_student_manager/
├── SKILL.md              # 本说明文件
├── main.py               # 命令行入口
├── manager.py            # 核心管理类
├── database.py           # 数据库模型
├── email_sender.py       # 邮件发送模块
├── config.py             # 配置管理
├── yoga_students.db      # SQLite数据库（自动创建）
└── config.json           # 邮箱配置（自动创建）
```
