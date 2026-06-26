# 云上艾飞 CLI 技能

云上艾飞 OA 系统的纯 API 客户端，零浏览器依赖，支持查询和写入操作。

## 快速使用

```bash
cd C:\Users\EF\.openclaw\workspace\skills\yunshang-aifei-cli

# 正式环境（默认）
python aifei.py todo                          # 查工作待办
python aifei.py user                          # 查当前用户
python aifei.py projects                      # 查项目列表
python aifei.py projects --name "万鑫测试"     # 搜索项目

# 测试环境
python aifei.py --env test todo
python aifei.py --env test projects
```

## Python API 调用

```python
from aifei_api import create_client, sm4_encrypt, parse_response

c = create_client('prod')  # 或 'test'
base = c.base_url
h = {'Authorization': 'Bearer ' + c.token, 'Content-Type': 'application/json;charset=UTF-8'}
```

## 已验证的 API 接口

### 微服务路由前缀

所有接口通过 nginx 代理，URL 格式：`{base_url}/dev-api/{服务名}/{Controller路径}`

| 微服务 | 服务名 | 说明 |
|--------|--------|------|
| 认证 | (无前缀) | `/dev-api/auth/login`, `/dev-api/code` |
| 系统 | (无前缀) | `/dev-api/system/user/getInfo` |
| 项目 | ef-project | 项目管理、项目计划、项目周报 |
| 市场 | ef-market | 线索、商机、线索跟进 |
| 财务 | ef-finance | 报销 |
| 人力 | ef-human | 员工、薪资、人力成本 |
| 公共 | ef-public | 任务、待办 |

### 查询接口（已验证 ✅）

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 验证码 | GET | `/dev-api/code` | 返回 uuid + base64 图片 |
| 登录 | POST | `/dev-api/auth/login` | forceLogin='1' 必须 |
| 用户信息 | GET | `/dev-api/system/user/getInfo` | |
| **待办** | POST | `/prod-api/public/pendingTask/processingList` | 正式用 prod-api |
| **项目列表** | POST | `/dev-api/ef-project/project/info/list` | data 包裹在 result.data |
| **项目周报列表** | POST | `/dev-api/ef-project/project/weekly/list` | 按 projectId 查 |
| **项目周报详情** | POST | `/dev-api/ef-project/project/weekly/getInfo/{weeklyId}` | |
| **报销列表** | POST | `/dev-api/ef-finance/expense/list` | applyStatus: 03=待会计审核, 05=已通过, 07=已发放 |
| **员工列表** | POST | `/dev-api/ef-human/employee/listAll` | 名字字段: employeeName |
| **人力成本** | POST | `/dev-api/ef-human/employeeCost/listPage` | 名字字段: userByName, 含税前工资/日单价 |
| **岗位薪资** | POST | `/dev-api/ef-human/salary/list2` | 岗位+职级的薪资配置 |
| **日单价** | POST | `/dev-api/ef-human/salary/getUserDayCost` | 返回所有人 |
| **线索列表** | POST | `/dev-api/ef-market/clue/selectList` | 返回全部线索（482条） |
| **线索跟进** | POST | `/dev-api/ef-market/clueFollow/list` | 用 clueId 过滤，注意返回所有线索的跟进 |

### 写入接口（已验证 ✅）

| 功能 | 方法 | 路径 | 关键字段 |
|------|------|------|----------|
| **周报评论** | POST | `/dev-api/ef-project/project/weekly/insertComment` | weeklyId, projectId, description |
| **创建任务** | POST | `/dev-api/ef-public/public/task/add` | 需 businessId 关联项目 |

## 技术架构

### 加解密（SM4/ECB/PKCS5Padding）
- **密钥**: `1097659710ff550f7da111309f64386b`（前后端统一）
- **请求**: `JSON → sm4_encrypt → hex 字符串`
- **响应**: `hex 字符串 → sm4_decrypt → JSON`（部分接口直接返回 JSON）
- **密码**: 明文 → sm4_encrypt → hex，放入 login 请求体的 password 字段
- **gmssl 库**：内部已处理 PKCS5 padding，**不要手动 pad**

### 认证
- **登录**: `POST /dev-api/auth/login`，**必须 `forceLogin: '1'`**（否则已有在线会话时返回 loginStatus:100）
- **Token**: 登录返回 `data.access_token`
- **传递**: Cookie `Admin-Token=<token>` + Header `Authorization: Bearer <token>` **双传**
- **缓存**: `.token-{env}.json`，4 小时有效，自动验证

### 环境差异

| | 测试环境 | 正式环境 |
|---|---------|---------|
| 地址 | http://192.168.24.25 | http://192.168.24.208:20080 |
| 登录方式 | 纯 API ✅ | 纯 API ✅ |
| API 前缀 | /dev-api | /dev-api（系统） + /prod-api（业务待办） |
| 账号 | 18602920976 | 18602920976 |

### 响应格式差异

| 接口 | 格式 |
|------|------|
| 大多数接口 | `{code, msg, total, rows}` |
| 项目列表 | `{code, msg, data: {total, rows}}` — data 多包一层 |
| 员工列表 | `{code, msg, data: [...]}` — data 是数组 |
| 岗位薪资 | `{code, msg, data: {posts: [...]}}` — 嵌套结构 |

### 关键字段名映射

| 业务 | 名字字段 | 注意 |
|------|----------|------|
| 员工 | employeeName | 不是 nickName |
| 人力成本 | userByName | 不是 employeeName |
| 线索 | clueTitle | 不是 clueName |
| 跟进内容 | followRecords | 不是 followContent |
| 报销状态 | applyStatus | 03=待审核, 05=已通过, 07=已发放 |

### 任务创建必要字段

```python
{
    'taskContent': '任务内容',
    'taskType': '01',       # 01=技术交流 02=现场勘察 03=需求调研 04=原型制作 05=可研及评审 06=商务招投标 07=其它
    'taskHeadBy': 'userId', 
    'taskHeadByName': '姓名',
    'taskHeadDeptId': 'deptId',
    'taskHeadDeptName': '部门名',
    'taskStartTime': 'YYYY-MM-DD',
    'taskEndTime': 'YYYY-MM-DD',
    'expectManDay': 2,
    'taskSource': '02',     # 02=项目关联
    'businessId': '项目ID', # 必须关联项目，否则 500
    'businessName': '项目名',
    'taskStatus': '01',     # 01=执行中
    'isPlan': 'N',
    'projectPhase': '04',
}
```

### 钉钉机器人推送

```python
import requests
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=daf5fd...'
requests.post(webhook, json={
    'msgtype': 'markdown',
    'markdown': {'title': '标题', 'text': '@康楠 内容...'},
    'at': {'atMobiles': ['手机号'], 'isAtAll': False}
})
```

## 常用人员 ID

| 姓名 | userId | deptId | 部门 |
|------|--------|--------|------|
| 万鑫 | 10 | 105 | 总经办/研发中心 |
| 康楠 | 12 | 130 | 开发组 |

## 常用项目 ID

| 项目 | projectId |
|------|-----------|
| 艾飞-AI全栈赋能项目（2026） | 9a7192dc-4f4a-4423-bff5-c46575944785 |

## 文件结构

```
skills/yunshang-aifei-cli/
├── SKILL.md              # 本文件
├── aifei.py              # CLI 入口
├── aifei_api.py          # API 客户端核心（SM4 + 认证）
├── login.py              # Playwright 登录（备用）
├── modules/
│   └── captcha_solver.py # 验证码识别（阿里云通义千问 VL）
├── .token-test.json      # 测试环境 token 缓存
├── .token-prod.json      # 正式环境 token 缓存
└── results/              # 调试输出
```

## 依赖
- Python 3.10+
- gmssl（SM4 加解密）
- requests
- playwright（仅备用登录需要）

## 踩坑记录

1. **forceLogin 必须为 '1'**：否则已有在线会话时返回 loginStatus:100 没有 token
2. **Token 双传**：Cookie `Admin-Token` + Header `Authorization: Bearer` 缺一不可
3. **gmssl 不要手动 pad**：`crypt_ecb()` 内部已处理 PKCS5，手动加 pad 会变成双倍长度
4. **正式环境待办用 /prod-api**：其他接口用 /dev-api，待办走 /prod-api
5. **clueFollow/list 返回所有线索的跟进**：需要用 clueId 在结果中过滤
6. **创建任务必须关联 businessId**：否则后端调用商机/项目服务失败（500）
7. **项目列表返回格式多包一层 data**：`result.data.rows` 而非 `result.rows`
