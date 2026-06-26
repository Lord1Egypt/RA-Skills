# 友盟推送助手 (Umeng Push Helper)

## ⚠️ 安全限制

**重要**：出于安全考虑，本技能**严格禁止**调用以下敏感接口：

| 禁止调用的接口 | 用途 | 风险等级 |
|--------------|------|---------|
| `sendMsg` | 发送推送消息 | 🔴 高危 |
| `updateApp` | 修改应用配置 | 🔴 高危 |
| `updateChannelInfo` | 修改渠道信息 | 🔴 高危 |
| `saveReceipt` | 保存回执配置 | 🟡 中危 |

这些操作需要通过友盟官方后台 ([https://upush.umeng.com](https://upush.umeng.com)) 手动执行。

**本技能仅支持查询类操作（只读）**：
- ✅ 获取应用列表
- ✅ 查询推送数据
- ✅ 查看诊断报告

---

## 安装位置

本技能已安装到：`~/.qoderwork/skills/umeng-push-helper/`

## 目录结构

```
umeng-push-helper/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 使用说明
├── cookie.txt                  # Cookie 存储文件
└── scripts/                    # 辅助脚本
    ├── auto_get_cookie.py      # 自动从浏览器获取 Cookie ⭐
    ├── manage_cookie.py        # Cookie 管理工具
    ├── browser_cookie.py       # Cookie 验证工具
    ├── security_interceptor.py # API 安全拦截器 ⭐🔒
    ├── get_app_list.py         # 获取应用列表
    ├── query_app_data.py       # 查询应用数据
    └── api_request.py          # API 请求封装
```

## 快速开始

### 第一步：登录并保存 Cookie

#### 方法一：自动获取（推荐）⭐

使用浏览器自动化工具获取 Cookie，无需手动操作：

```bash
# 运行自动获取脚本
python scripts/auto_get_cookie.py
```

该脚本会：
1. 自动打开浏览器访问 [https://upush.umeng.com/apps/list](https://upush.umeng.com/apps/list)
2. 检测用户是否已登录
3. 读取浏览器中的 Cookie
4. 验证 Cookie 是否包含必需的 `ctoken` 字段
5. 保存有效的 Cookie 到本地文件

**优点：**
- ✅ 全自动，无需手动操作
- ✅ 自动验证 Cookie 有效性
- ✅ 检查 `ctoken` 字段是否存在

#### 方法二：手动获取（备用）

如果自动获取失败，可手动获取：

1. 访问 [https://upush.umeng.com](https://upush.umeng.com) 并登录

2. 打开 Chrome 开发者工具（F12）
   - 切换到 Network（网络）标签
   - 刷新页面
   - 点击任意请求
   - 在 Request Headers 中找到 `Cookie` 字段
   - 复制完整的 Cookie 值

3. 使用以下命令保存：
   ```bash
   python scripts/manage_cookie.py save "你的 cookie 值"
   ```

   或直接写入文件：
   ```bash
   echo "你的 cookie 值" > ~/.qoderwork/skills/umeng-push-helper/cookie.txt
   ```

### 第二步：使用功能

#### 获取应用列表

告诉助手："获取我的应用列表" 或 "查看友盟应用"

助手会调用 API 并展示所有应用，格式如下：
```
应用列表：

1. 应用名称 A - appkey: 12345678
2. 应用名称 B - appkey: 87654321
...

共找到 X 个应用
```

#### 获取推送周报/应用数据

告诉助手："获取 appkey 为 XXXXX 的推送周报" 或 "查询应用 XXXXX 的数据"

助手会调用三个接口获取完整的应用数据：
- 消息概览 (messageOverview)
- 诊断摘要 (diagnosisSummery)
- 诊断报告 (diagnosisReport)

#### Cookie 管理命令

```bash
# 自动从浏览器获取 Cookie（推荐）
python scripts/auto_get_cookie.py

# 保存 Cookie（会自动验证）
python scripts/manage_cookie.py save "<cookie_value>"

# 加载已保存的 Cookie
python scripts/manage_cookie.py load

# 检查 Cookie 是否存在
python scripts/manage_cookie.py check

# 验证 Cookie 是否有效
python scripts/manage_cookie.py validate "<cookie_value>"

# 从 Cookie 中提取 ctoken
python scripts/manage_cookie.py extract-ctoken "<cookie_value>"
```

## API 详情

### 获取应用列表 API

- **URL**: `https://upush.umeng.com/hsf/home/listAll`
- **方法**: POST
- **参数**:
  ```json
  {
    "appkey": "",
    "platform": "all",
    "page": 1,
    "perPage": 15,
    "hasPush": 0,
    "appName": "",
    "yearQuotaSts": 0
  }
  ```

### 响应解析

从 `data.appList` 数组中提取：
- `appkey`: 应用唯一标识
- `appName`: 应用名称

## 常见问题

### Cookie 过期了怎么办？

如果 API 返回认证错误，说明 Cookie 已过期。可以：

1. **自动重新获取**（推荐）：
   ```bash
   python scripts/auto_get_cookie.py
   ```

2. **手动更新**：
   ```bash
   python scripts/manage_cookie.py save "新的 cookie 值"
   ```

### 如何检查 Cookie 是否有效？

使用以下命令验证 Cookie：
```bash
python scripts/manage_cookie.py validate "<cookie_value>"
```

或直接检查已保存的 Cookie：
```bash
# 加载 Cookie 并手动验证
python scripts/manage_cookie.py load
```

### 为什么需要 ctoken 字段？

`ctoken` 是友盟推送后台的 CSRF 令牌，用于防止跨站请求攻击。所有 API 调用都需要在请求头中包含此值：
```
x-csrf-token: <从 Cookie 中提取的 ctoken 值>
```

自动获取脚本会自动检查并提取此字段。

### 安全提示

- ✅ Cookie 包含敏感认证信息，请妥善保管
- ✅ 不要将 `cookie.txt` 文件分享给他人
- ✅ 建议定期更新 Cookie
- ✅ 使用后及时清理浏览器会话

## 技术支持

如有问题，请访问：
- 友盟官方文档：[https://developer.umeng.com](https://developer.umeng.com)
- QoderWork 论坛：[https://forum.qoder.com](https://forum.qoder.com)
