# 云上艾飞 CLI 工具

云上艾飞 OA 系统的纯 API 客户端，零浏览器依赖。支持查询待办、项目、报销、人力成本、线索跟进、创建任务、周报评论等功能。

## ⚠️ 首次使用

### 第一步：安装依赖

```bash
pip install gmssl requests python-dotenv
```

### 第二步：配置账号

复制 `.env.example` 为 `.env`，填入你的云上艾飞账号：

```bash
cp .env.example .env
```

```ini
# 只需填这两项
AIFEI_USERNAME=你的手机号
AIFEI_PASSWORD=你的密码
```

> **验证码识别**：登录时的算术验证码由 AI 模型自动识别。如果你使用 OpenClaw，工具会自动读取配置，**无需额外设置**。如果不使用 OpenClaw，需要在 `.env` 中额外配置 `DASHSCOPE_API_KEY`（阿里云通义千问 API Key，申请地址：https://dashscope.console.aliyun.com/）。

### 第三步：开始使用

```bash
python aifei.py todo    # 查工作待办
```

## 命令一览

```bash
# 正式环境（默认）
python aifei.py todo                          # 查工作待办
python aifei.py user                          # 查当前用户信息
python aifei.py projects                      # 查项目列表
python aifei.py projects --name "项目名"       # 搜索项目
python aifei.py reimbursement                 # 查报销列表
python aifei.py contracts                     # 查合同列表
python aifei.py business                      # 查商机列表

# 测试环境
python aifei.py --env test todo

# 原始 API 调用（高级用法）
python aifei.py raw POST "ef-project/project/info/list" --data '{"pageNum":1,"pageSize":10}'
```

## Python 代码调用

```python
from aifei_api import create_client

client = create_client('prod')  # 或 'test'

todos = client.get_todos()
projects = client.get_projects(name='某项目')
costs = client.get_employee_costs()
clues = client.get_clues()

client.create_task({...})
client.add_weekly_comment(weekly_id, project_id, '评论内容')
```

## 环境说明

| 环境 | 地址 | 说明 |
|------|------|------|
| 正式 (prod) | http://192.168.24.208:20080 | 默认环境 |
| 测试 (test) | http://192.168.24.25 | 开发测试 |

## 文件结构

```
yunshang-aifei-cli/
├── README.md              # 本文件
├── SKILL.md               # 详细接口文档
├── .env.example           # 配置模板（只需填账号密码）
├── aifei.py               # CLI 入口
├── aifei_api.py           # API 客户端
├── requirements.txt       # Python 依赖
└── modules/
    ├── __init__.py
    └── captcha_solver.py  # 验证码自动识别
```

## 注意事项

1. **`.env` 文件包含你的账号密码，不要分享**
2. 登录会踢掉其他在线会话
3. Token 缓存 4 小时，免重复登录
4. 需在内网环境下使用

## 常见问题

**Q: 提示"未找到 API Key"？**
A: 如果不用 OpenClaw，在 `.env` 中加一行 `DASHSCOPE_API_KEY=你的Key`（到 https://dashscope.console.aliyun.com/ 免费申请）。

**Q: 登录失败？**
A: 检查账号密码。验证码偶尔识别错会自动重试。

**Q: 账号被锁定？**
A: 连续失败会锁 20 分钟，等一下再试。
