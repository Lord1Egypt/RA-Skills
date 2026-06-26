# 获取用户姓名

## 注意事项

本接口不校验[通讯录授权范围](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority)，将直接根据传入的用户 ID 返回对应基础信息（姓名），不受数据权限范围限制。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取用户的基本信息 (contact:user.basic_profile:readonly) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/users/basic_batch` |
|----------|----------------------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | 5 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/batch_get_name) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token` 或 `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user_id_type` | string | 否 | 用户 ID 类型<br>可选值：<br>- `open_id`：标识一个用户在某个应用中的身份<br>- `union_id`：标识一个用户在某个应用开发商下的身份<br>- `user_id`：标识一个用户在某个租户内的身份<br>默认值：`open_id`<br>**权限要求**：当值为 `user_id` 时，需要获取用户 user ID (contact:user.employee_id:readonly) |

### 请求体

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `user_ids` | array | 是 | 用户 ID。ID 类型与查询参数 `user_id_type` 保持一致。<br>长度范围：`1` ～ `10` |

### 请求示例

#### cURL 请求示例

```bash
curl -X POST 'https://open.feishu.cn/open-apis/contact/v3/users/basic_batch' \
  -H 'Authorization: Bearer tenant_access_token' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "user_ids": ["ou_b3b46653c99f1f6177a478974bdabb72"]
  }'
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
	req := larkcontact.NewBatchGetNameUserReqBuilder().
		UserIdType(`open_id`).
		UserIdList([]string{
			"ou_b3b46653c99f1f6177a478974bdabb72",
		}).
		Build()

	// 发起请求
	resp, err := client.Contact.User.BatchGetName(context.Background(), req)
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
        BatchGetNameUserReq req = BatchGetNameUserReq.newBuilder()
                .userIdType("open_id")
                .userIdList(java.util.Arrays.asList("ou_b3b46653c99f1f6177a478974bdabb72"))
                .build();

        // 发起请求
        BatchGetNameUserResp resp = client.contact().user().batchGetName(req, RequestOptions.newBuilder().build());
    }
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/users/basic_batch"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "user_ids": ["ou_b3b46653c99f1f6177a478974bdabb72"]
    }
    
    response = requests.post(url, headers=headers, json=data)
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
| `users` | array | 用户信息列表 |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "users": [
            {
                "user_id": "ou_b3b46653c99f1f6177a478974bdabb72",
                "name": "张三",
                "i18n_name": {
                    "zh_cn": "张三",
                    "ja_jp": "佐藤はるか",
                    "en_us": "Jason Zhang"
                }
            }
        ]
    }
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
| 400 | 40001 | param is invalid |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无 |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 应用权限配置 | [https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 用户相关的 ID 概念 | [https://open.feishu.cn/document/home/user-identity-introduction/introduction](https://open.feishu.cn/document/home/user-identity-introduction/introduction) |
| 权限范围校验 | [https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |