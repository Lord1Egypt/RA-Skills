---
name: sbkj-bidsearch
category: research
description: 全国招标中标采购信息搜索 - 保标招标 - 支持多条件筛选的招投标数据搜索，返回项目金额、甲方、乙方、代理机构、采集源网址等核心字段。
version: 1.0.1
author: SBKJ
license: MIT-0
homepage: https://www.bog-bid.com
api_endpoint: https://gate.gov-bid.com/outer-gateway/bid/SearchProjectForAI
tags:
  - 招标采购
  - 商机搜索
  - 中标信息
  - 招投标
  - 政府采购
  - 保标招标
credentials:
  - name: BID_API_KEY
    description: API 访问密钥，用于认证招标采购 API 请求
    required: true
    sensitive: true
  - name: BID_SERVER_URL
    description: API 服务器基础地址
    required: false
    default: https://gate.gov-bid.com
    sensitive: false
---

# ⚠️ 安全提示

**本技能会向外部 API 发送 HTTP 请求**

## 关键信息

| 项目 | 说明 |
|------|------|
| **API 端点** | `https://gate.gov-bid.com/outer-gateway/bid/SearchProjectForAI` |
| **请求方式** | POST (JSON) |
| **凭证要求** | `BID_API_KEY` (必需) |
| **数据来源** | 第三方招标采购信息服务 |
| **执行代码** | `scripts/bid_search.py` |

## 安装前必读

**请确认以下事项后再安装：**

1. ✅ 您已从合法渠道获取 API 访问密钥
2. ✅ 您信任 API 服务提供商 (`gate.gov-bid.com`)
3. ✅ 您已审查技能代码（特别是 `scripts/bid_search.py`）
4. ✅ 您了解技能会向外部服务器发送您的 API 密钥
5. ✅ 您已在安全环境中测试或限制 API 密钥权限

## 安全最佳实践

```bash
# 1. 使用环境变量管理密钥（不要硬编码）
export BID_API_KEY="your_api_key_here"

# 2. 限制 API 密钥权限（如服务商支持）
# 3. 定期轮换密钥
# 4. 在生产环境使用前先测试
# 5. 监控 API 使用情况
```

---

# 招标采购信息搜索 API 技能

## 技能描述

封装第三方招标采购信息搜索接口，专为 AI 模型设计，支持多条件筛选的招投标数据搜索。

**数据覆盖：** 招标信息、中标信息、合同信息、采购意向、拍租信息等

**返回核心字段：** 项目金额、甲方信息、乙方信息、代理机构、合同到期时间等

## 安装配置

### 必需凭证

| 凭证名 | 说明 | 是否必需 | 示例 |
|--------|------|----------|------|
| `BID_API_KEY` | API 访问密钥 | ✅ 是 | `AK729447427d63c2320ff44c7a` |
| `BID_SERVER_URL` | API 服务器地址 | ❌ 否 | `https://gate.gov-bid.com` |

### 安装步骤

**方式 1：环境变量**
```bash
export BID_API_KEY="your_api_key_here"
export BID_SERVER_URL="https://gate.gov-bid.com"
```

**方式 2：Hermes 凭证管理（推荐）**
```yaml
# ~/.hermes/config.yaml
credentials:
  BID_API_KEY: "your_api_key_here"
  BID_SERVER_URL: "https://gate.gov-bid.com"
```

**方式 3：技能安装时配置**
```bash
skill_install sbkj-bidsearch
```

### 验证安装

```bash
skill_view sbkj-bidsearch
```

## 使用方法

### 基本搜索

```python
from hermes_tools import terminal

result = terminal('''
python3 << 'EOF'
from skill_view import get_credential
import requests

api_key = get_credential("BID_API_KEY")
url = f"https://gate.gov-bid.com/outer-gateway/bid/SearchProjectForAI?key={api_key}"

payload = {
    "keyword": "工程",
    "className": "招标信息",
    "startDate": "2025-01-10",
    "endDate": "2025-01-17",
    "pageId": 1,
    "pageNumber": 20
}

response = requests.post(url, json=payload)
data = response.json()

if data.get("code") == 200:
    print(f"找到 {data['data']['total']} 条记录")
else:
    print(f"错误：{data.get('msg')}")
EOF
''')
```

### Python 函数封装

```python
def search_bid_projects(
    keyword=None,
    exclude_kw=None,
    include_kw=None,
    class_name=None,
    area_name=None,
    search_field="全部",
    start_date=None,
    end_date=None,
    page_id=1,
    page_number=20
):
    """搜索招标采购项目"""
    from skill_view import get_credential
    import requests
    
    api_key = get_credential("BID_API_KEY")
    server_url = get_credential("BID_SERVER_URL") or "https://gate.gov-bid.com"
    
    url = f"{server_url}/outer-gateway/bid/SearchProjectForAI?key={api_key}"
    
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "pageId": page_id,
        "pageNumber": page_number
    }
    
    if keyword: payload["keyword"] = keyword
    if exclude_kw: payload["excludeKW"] = exclude_kw
    if include_kw: payload["inCludeKW"] = include_kw
    if class_name: payload["className"] = class_name
    if area_name: payload["areaName"] = area_name
    if search_field: payload["searchField"] = search_field
    
    response = requests.post(url, json=payload, timeout=30)
    return response.json()
```

## 请求参数说明

| 参数名 | 必填 | 类型 | 说明 |
|--------|------|------|------|
| keyword | 否 | string | 搜索关键词：空格=同时出现，竖线=或关系 |
| excludeKW | 否 | string | 排除关键词，多个用竖线分隔 |
| inCludeKW | 否 | string | 必须包含关键词，多个用竖线分隔 |
| className | 否 | string | 项目类别：全部信息/招标信息/中标信息/合同信息/采购意向/拍租信息 |
| areaName | 否 | string | 项目归属地区名称（如"武汉"） |
| searchField | 否 | string | 搜索字段：标题、内容、全部（默认"全部"） |
| startDate | ✅ | string | 发布开始日期，格式：yyyy-MM-dd |
| endDate | ✅ | string | 发布结束日期，格式：yyyy-MM-dd |
| pageId | ✅ | int | 当前页码 |
| pageNumber | ✅ | int | 每页记录数（最大 100，设为 0 仅返回总数） |

## 返回参数说明

### 顶层响应

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | int | 接口响应状态码（200=成功） |
| msg | string | 响应信息 |
| subCode | string | 业务侧 code |
| subMsg | string | 业务侧 msg |
| data | object | 业务数据 |

### 项目列表项字段

| 字段 | 说明 |
|------|------|
| id | 项目 ID |
| title | 项目标题 |
| newsTypeName | 信息类型名称 |
| publishTime | 发布时间 |
| areaName | 地区（省/市/区） |
| projectMoney | 项目金额 |
| projectClass | 项目类别 |
| purchaseType | 采购类型 |
| partAInfo | 甲方信息数组（name, contactPhone, email） |
| partBInfo | 乙方信息数组 |
| agencyInfo | 代理机构信息数组 |

## 常见用例

### 1. 获取某地区最新招标公告
```python
result = search_bid_projects(
    class_name="招标信息",
    area_name="上海",
    start_date="2025-01-15",
    end_date="2025-01-17"
)
```

### 2. 搜索特定关键词的中标信息
```python
result = search_bid_projects(
    keyword="智慧城市",
    class_name="中标信息",
    start_date="2025-01-01",
    end_date="2025-01-17"
)
```

### 3. 排除特定关键词
```python
result = search_bid_projects(
    keyword="空调",
    exclude_kw="维修 | 保养",
    class_name="招标信息",
    start_date="2025-01-10",
    end_date="2025-01-17"
)
```

### 4. 仅获取结果总数
```python
result = search_bid_projects(
    keyword="工程",
    start_date="2025-01-01",
    end_date="2025-01-17",
    page_number=0
)
print(f"总数：{result['data']['total']}")
```

## 错误处理

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常处理返回数据 |
| 401 | 认证失败 | 检查 BID_API_KEY 是否正确 |
| 403 | 权限不足 | 联系 API 服务提供商 |
| 500 | 服务器错误 | 稍后重试 |
| 504 | 网关超时 | 检查网络或稍后重试 |

## 注意事项

1. **API Key 安全**：不要将 API Key 硬编码在代码中
2. **请求频率**：建议控制请求频率，避免触发限流
3. **日期格式**：必须使用 `yyyy-MM-dd` 格式
4. **分页限制**：`pageNumber` 最大值为 100
5. **关键词语法**：空格=AND，竖线=OR

## 隐私与数据保护

- **数据传输**：所有请求通过 HTTPS 加密传输
- **凭证存储**：API Key 存储在本地凭证管理系统或环境变量中
- **日志记录**：技能本身不记录请求日志

## 故障排查

### 问题：返回 401 认证失败
**解决**：检查 `BID_API_KEY` 是否正确配置

### 问题：返回数据为空
**解决**：
1. 检查日期范围是否合理
2. 尝试放宽搜索条件
3. 设置 `pageNumber=0` 先查看是否有匹配记录

### 问题：请求超时
**解决**：
1. 检查网络连接
2. 增加请求超时时间
3. 减少 `pageNumber` 值

## 技术细节

### 代码结构
```
sbkj-bidsearch/
├── SKILL.md
└── scripts/
    └── bid_search.py
```

### 网络请求详情
- **协议**: HTTPS
- **方法**: POST
- **Content-Type**: application/json
- **超时**: 30 秒

### 依赖项
- Python 3.7+
- requests 库

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.1 | 2026-04-22 | 更新许可证为 MIT-0，更新 homepage |
| 1.0.0 | 2026-04-21 | 初始版本 |

## 参考链接

- 接口文档：http://faq.zhvac.com/web/#/p/50f55291c248b58163e9ae4aa178eb12
- 官方网站：https://www.bog-bid.com
- API 端点：https://gate.gov-bid.com

---

**最后更新**: 2026-04-22  
**技能版本**: 1.0.1  
**许可证**: MIT-0 (无需署名)
