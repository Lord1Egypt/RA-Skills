---
name: umeng-api
description: 查询友盟 (UMeng) 应用统计数据分析，支持通过 APPKEY 获取应用的基础指标信息如新增用户数、活跃用户数等。当用户提到"友盟"、"umeng"、"APPKEY"、"新增用户"、"活跃用户"或需要查询应用统计数据时使用此技能。
---

# 友盟 API 技能

## 功能概述
此技能提供友盟开放 API 的完整 Python SDK 封装，用于查询应用的统计数据，包括：
- 新增用户数
- 活跃用户数  
- 异常点检测（异动归因报告）
- 其他友盟 UApp API 支持的指标

## 前置条件
1. **友盟账号**：需要有效的友盟开发者账号
2. **应用 APPKEY**：目标应用的友盟 APPKEY
3. **API 认证**：需要 apiKey 和 apiSecurity（从友盟开发者平台获取）

## 安装依赖
技能已包含完整的友盟 AOP SDK，无需额外安装。

## 使用方法

### 1. 配置认证信息

**认证信息获取优先级**（从高到低）：
1. 代码中直接传入的参数
2. `umeng-config.json` 配置文件（推荐）
3. 环境变量

#### 方式一：使用配置文件（推荐）

创建 `umeng-config.json` 文件，可以放在以下任一位置：
- 当前工作目录
- 用户主目录 (`~/umeng-config.json`)
- 技能目录

```json
{
  "apiKey": "your_api_key",
  "apiSecurity": "your_api_security",
  "note": "友盟 API 配置文件 - 请妥善保管，不要提交到版本控制系统"
}
```

⚠️ **安全提示**：建议将配置文件权限设置为仅所有者可读写（`chmod 600 umeng-config.json`）

#### 方式二：使用环境变量

```bash
export UMENG_API_KEY="your_api_key"
export UMENG_API_SECURITY="your_api_security"
```

#### 方式三：代码中直接设置

```python
import aop
aop.set_default_appinfo(your_api_key, your_api_security)
```

### 2. 查询新增用户数
```python
import aop
import aop.api

# 设置友盟 API 服务器
aop.set_default_server('gateway.open.umeng.com')

# 认证信息会自动从 umeng-config.json 或环境变量加载
# 也可以手动设置：aop.set_default_appinfo(apiKey, apiSecurity)

# 查询新增用户
req = aop.api.UmengUappGetNewUsersRequest()
resp = req.get_response(None, appkey="your_appkey", startDate="2026-03-25", endDate="2026-03-25", periodType="daily")
print(f"新增用户数：{resp['newUserInfo'][0]['value']}")
```

### 3. 查询活跃用户数
```python
# 查询活跃用户
req = aop.api.UmengUappGetActiveUsersRequest()
resp = req.get_response(None, appkey="your_appkey", startDate="2026-03-25", endDate="2026-03-25", periodType="daily")
print(f"活跃用户数：{resp['activeUserInfo'][0]['value']}")
```

## 完整示例

### 1. 查询基础统计数据
```python
import os
import aop
import aop.api

def query_umeng_stats(appkey, date_str=None):
    """查询友盟应用统计数据"""
    if date_str is None:
        from datetime import date
        date_str = date.today().strftime("%Y-%m-%d")
    
    # 设置友盟 API 服务器
    aop.set_default_server('gateway.open.umeng.com')
    
    # 认证信息会自动从 umeng-config.json 或环境变量加载
    # 检查是否成功加载
    appinfo = aop.get_default_appinfo()
    if not appinfo:
        raise ValueError("未找到友盟认证信息，请配置 umeng-config.json 或环境变量")
    
    # 查询新增用户
    new_users_req = aop.api.UmengUappGetNewUsersRequest()
    new_users_resp = new_users_req.get_response(None, appkey=appkey, startDate=date_str, endDate=date_str, periodType="daily")
    new_users = new_users_resp['newUserInfo'][0]['value']
    
    # 查询活跃用户
    active_users_req = aop.api.UmengUappGetActiveUsersRequest()
    active_users_resp = active_users_req.get_response(None, appkey=appkey, startDate=date_str, endDate=date_str, periodType="daily")
    active_users = active_users_resp['activeUserInfo'][0]['value']
    
    return {
        "date": date_str,
        "appkey": appkey,
        "new_users": new_users,
        "active_users": active_users
    }

# 使用示例
if __name__ == "__main__":
    result = query_umeng_stats("64abc640a1a164591b48bb0c")
    print(f"日期：{result['date']}")
    print(f"新增用户：{result['new_users']}")
    print(f"活跃用户：{result['active_users']}")
```

### 2. 查询异常点检测数据
```python
import os
from umeng_get_outlier_points import get_umeng_outlier_points, format_outlier_report

def query_umeng_outlier(appkey, ds):
    """查询友盟应用异常点数据"""
    # 认证信息会自动从 umeng-config.json 或环境变量加载
    # 也可以直接传入：get_umeng_outlier_points(appkey, ds, api_key, api_security)
    
    # 查询异常点
    outlier_data = get_umeng_outlier_points(appkey, ds)
    return outlier_data

# 使用示例
if __name__ == "__main__":
    try:
        appkey = "59892f08310c9307b60023d0"
        ds = "20260322"  # YYYYMMDD 格式
        
        outlier_data = query_umeng_outlier(appkey, ds)
        print(format_outlier_report(outlier_data))
    except Exception as e:
        print(f"Error: {e}")
```

## 支持的其他 API 接口
SDK 还支持以下接口（位于 `aop/api/biz/` 目录）：
- `UmengUappGetLaunchesRequest` - 启动次数
- `UmengUappGetDurationsRequest` - 使用时长
- `UmengUappGetRetentionsRequest` - 留存率
- `UmengUappGetChannelDataRequest` - 渠道数据
- `UmengUappGetVersionDataRequest` - 版本数据
- 以及更多...

## 错误处理
常见的异常类型：
- `aop.ApiError` - API 网关返回的错误
- `aop.AopError` - 客户端请求前的错误
- `ValueError` - 认证信息未找到（检查 umeng-config.json 或环境变量）
- `Exception` - 其他未知异常

## 安全注意事项
1. **不要硬编码认证信息**：优先使用 `umeng-config.json` 配置文件或环境变量
2. **保护配置文件**：将 `umeng-config.json` 添加到 `.gitignore`，避免提交到版本控制
3. **文件权限**：建议设置 `chmod 600 umeng-config.json` 限制访问
4. **API 调用频率**：友盟 API 有调用频率限制，请合理控制请求频次

## 技能目录结构
```
umeng-api/
├── SKILL.md
├── umeng_config.py          # 配置管理模块（新增）
├── umeng_get_outlier_points.py  # 异常点检测封装
├── aop/                     # 友盟 AOP SDK
│   ├── __init__.py         # 已更新，支持配置文件加载
│   └── api/
│       ├── __init__.py
│       ├── base.py
│       ├── common/
│       └── biz/            # 所有友盟 API 接口
└── scripts/
```

## 使用示例场景
当用户说：
- "查询 APPKEY 为 xxx 的应用今天新增用户数"
- "友盟统计中 xxx 应用的活跃用户是多少"  
- "获取 umeng 应用 xxx 的昨日数据"
- "查询 APPKEY 为 xxx 在 YYYY-MM-DD 的异常点报告"
- "获取友盟异动归因报告链接"

技能会自动：
1. 从 `umeng-config.json` 加载认证信息（如果存在）
2. 否则从环境变量加载
3. 提取 APPKEY，使用当前日期（或指定日期）
4. 调用相应 API 并返回结果

## 配置文件示例

**umeng-config.json**:
```json
{
  "apiKey": "12345678",
  "apiSecurity": "your_api_security_here"
}
```

**位置优先级**：
1. `./umeng-config.json` (当前工作目录)
2. `~/umeng-config.json` (用户主目录)
3. `<skill-dir>/umeng-config.json` (技能目录)
