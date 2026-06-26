# 获取通讯录授权范围

## 注意事项

- 当应用通讯录权限范围为全部成员时，该接口将返回根部门下的一级部门列表和直属用户列表，以及租户下所有用户组列表。

- 当应用通讯录权限范围不为全部成员时，则只返回在通讯录权限范围内的部门列表（不包含部门内的子部门以及用户）、用户列表或用户组列表。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取通讯录基本信息 (contact:contact.base:readonly) |
| 应用权限（开启任一即可） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 应用权限（开启任一即可） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/scopes` |
|----------|-----------------------------------------------------|
| 请求方法 | GET |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/scope/list) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer t-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user_id_type` | string | 否 | 用户 ID 类型<br>可选值：<br>- `open_id`：标识一个用户在某个应用中的身份<br>- `union_id`：标识一个用户在某个应用开发商下的身份<br>- `user_id`：标识一个用户在某个租户内的身份<br>默认值：`open_id`<br>**权限要求**：当值为 `user_id` 时，需要获取用户 user ID (contact:user.employee_id:readonly) |
| `department_id_type` | string | 否 | 指定查询结果中的部门 ID 类型<br>可选值：<br>- `department_id`：支持用户自定义配置的部门 ID<br>- `open_department_id`：由系统自动生成的部门 ID<br>默认值：`open_department_id` |
| `page_token` | string | 否 | 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果 |
| `page_size` | int | 否 | 分页大小，用于设置一次调用的返回值列表长度。<br>取值范围：`1` ～ `100`<br>默认值：`50` |

### 请求体

无请求体（GET 请求）

### 请求示例

#### cURL 请求示例

```bash
curl -X GET 'https://open.feishu.cn/open-apis/contact/v3/scopes?page_size=50&page_token=AQD9/...' \
  -H 'Authorization: Bearer tenant_access_token' \
  -H 'Content-Type: application/json; charset=utf-8'
```

#### Go 请求示例

```go
import (
	"context"

	"github.com/larksuite/oapi-sdk-go/v3"
	"github.com/larksuite/oapi-sdk-go/v3/service/contact/v3"
)

func main() {
	// 创建 Client
	client := lark.NewClient("appID", "appSecret")

	// 创建请求对象
	req := larkcontact.NewListScopeReqBuilder().
		UserIdType(`open_id`).
		DepartmentIdType(`open_department_id`).
		PageSize(50).
		PageToken(`AQD9/...`).
		Build()

	// 发起请求
	resp, err := client.Contact.Scope.List(context.Background(), req)
}
```

#### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.service.contact.v3.model.*;
import com.lark.oapi.core.request.RequestOptions;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 创建请求对象
        ListScopeReq req = ListScopeReq.newBuilder()
                .userIdType("open_id")
                .departmentIdType("open_department_id")
                .pageSize(50)
                .pageToken("AQD9/...")
                .build();

        // 发起请求
        ListScopeResp resp = client.contact().scope().list(req, RequestOptions.newBuilder().build());
    }
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/scopes"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "page_size": 50,
        "page_token": "AQD9/..."
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

## 接口响应

### 响应头

| 名称 | 类型 | 描述 |
|------|------|------|
| - | - | 无额外响应头字段 |

### 响应体

| 字段 | 类型 | 描述 |
|------|------|------|
| `code` | int | 错误码，非 0 表示失败 |
| `msg` | string | 错误描述 |
| `data` | object | 响应数据 |
| `department_ids` | array | 已授权的部门列表。列表内的部门 ID 类型与查询参数 `department_id_type` 的取值一致 |
| `user_ids` | array | 已授权的用户列表。列表内的用户 ID 类型与查询参数 `user_id_type` 的取值一致 |
| `group_ids` | array | 已授权的用户组 |
| `has_more` | boolean | 是否还有更多项 |
| `page_token` | string | 分页标记，当 `has_more` 为 true 时，会同时返回新的 `page_token` |

### 响应示例

```json
{
    "code": 0,
    "data": {
        "department_ids": [
            "75217143312g9842"
        ],
        "group_ids": [
            "4bgga762"
        ],
        "has_more": true,
        "page_token": "AQD9/Rn9eij9Pm39ED40/e4EuQbBea/ybCE7/PQ1yzQXAVoq7bxTVC%2BI1oJqeoRY",
        "user_ids": [
            "9b2fabg6"
        ]
    },
    "msg": "success"
}
```

## 响应码定义

### 成功码

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 200 | 0 | 请求成功 |

### 客户端错误码 (4xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 400 | 40011 | page size is invalid |
| 400 | 40012 | page token is invalid error |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无 |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 应用权限配置 | [https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 部门 ID 说明 | [https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview) |
| 权限范围校验 | [https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |