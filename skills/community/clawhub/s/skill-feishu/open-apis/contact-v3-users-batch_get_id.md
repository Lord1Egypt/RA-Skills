# 通过手机号或邮箱获取用户 ID

## 注意事项

请求后不返回用户 ID 的可能原因：

- 请求头 Authorization 传入的 tenant_access_token 有误。例如，tenant_access_token 对应的应用与实际所需应用不一致。
- 输入的手机号或者邮箱不存在。
- 应用未开通 **获取用户 user ID** API 权限。
- 应用无权限查看用户信息。你需要在应用详情页为应用配置数据权限，具体说明参见[配置应用数据权限](https://open.feishu.cn/document/home/introduction-to-scope-and-authorization/configure-app-data-permissions)。
- 使用企业邮箱查询将无法返回用户 ID，必须使用用户的邮箱地址。
- 所查询的用户已离职，如果请求参数 include_resigned 取值为 false，则不会返回离职用户 ID。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 通过手机号或邮箱获取用户 ID (contact:user.id:readonly) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取用户受雇信息 (contact:user.employee:readonly) |
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |
| 字段权限（敏感字段） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 字段权限（敏感字段） | 读取通讯录 (contact:contact:readonly) |
| 字段权限（敏感字段） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id` |
|----------|-------------------------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/batch_get_id) |

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

### 请求体

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `emails` | array | 否 | 要查询的用户邮箱，最多可传入 50 条。<br>注意：<br>- 不支持企业邮箱<br>- emails 与 mobiles 两个参数相互独立<br>- 本接口返回的用户 ID 数量为 emails 数量与 mobiles 数量之和<br>最大长度：`50` |
| `mobiles` | array | 否 | 要查询的用户手机号，最多可传入 50 条。<br>注意：<br>- 非中国大陆地区的手机号需要添加以 "+" 开头的国家或地区代码<br>- emails 与 mobiles 两个参数相互独立<br>- 本接口返回的用户 ID 数量为 emails 数量与 mobiles 数量之和<br>最大长度：`50` |
| `include_resigned` | boolean | 否 | 查询结果是否包含离职员工的用户信息<br>可选值：<br>- `true`：包含<br>- `false`：不包含<br>默认值：`false` |

### 请求示例

#### cURL 请求示例

```bash
curl -X POST 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id' \
  -H 'Authorization: Bearer tenant_access_token' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "emails": ["zhangsan@z.com", "lisi@a.com"],
    "mobiles": ["13011111111", "13022222222"],
    "include_resigned": true
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
	req := larkcontact.NewBatchGetIdUserReqBuilder().
		UserIdType(`open_id`).
		Body(larkcontact.NewBatchGetIdUserReqBodyBuilder().
			Emails([]string{`zhangsan@z.com`, `lisi@a.com`}.
			Mobiles([]string{`13812345678`, `13812345679`}.
			Build()).
		Build()

	// 发起请求
	resp, err := client.Contact.User.BatchGetId(context.Background(), req)
}
```

#### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.core.request.RequestOptions;
import com.lark.oapi.service.contact.v3.model.BatchGetIdUserReq;
import com.lark.oapi.service.contact.v3.model.BatchGetIdUserReqBody;
import com.lark.oapi.service.contact.v3.model.BatchGetIdUserResp;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 创建请求对象
        BatchGetIdUserReq req = BatchGetIdUserReq.newBuilder()
                .userIdType("open_id")
                .batchGetIdUserReqBody(BatchGetIdUserReqBody.newBuilder()
                        .emails(new String[]{"zhangsan@z.com", "lisi@a.com"})
                        .mobiles(new String[]{"13812345678", "13812345679"})
                        .build())
                .build();

        // 发起请求
        BatchGetIdUserResp resp = client.contact().user().batchGetId(req, RequestOptions.newBuilder().build());
    }
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "user_id_type": "open_id"
    }
    data = {
        "emails": ["zhangsan@z.com", "lisi@a.com"],
        "mobiles": ["13011111111", "13022222222"],
        "include_resigned": True
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
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
| `user_list` | array | 手机号或者邮箱对应的用户 ID 信息列表 |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "user_list": [
            {
                "user_id": "ou_979112345678741d29069abcdef01234",
                "email": "zhanxxxxx@a.com",
                "status": {
                    "is_frozen": false,
                    "is_resigned": false,
                    "is_activated": true,
                    "is_exited": false,
                    "is_unjoin": false
                }
            },
            {
                "user_id": "ou_919112245678741d29069abcdef02345",
                "email": "lisixxxx@a.com",
                "status": {
                    "is_frozen": false,
                    "is_resigned": false,
                    "is_activated": true,
                    "is_exited": false,
                    "is_unjoin": false
                }
            },
            {
                "user_id": "ou_46a087654321a1dc920ffab8fedc3456",
                "mobile": "130xxxx1111",
                "status": {
                    "is_frozen": false,
                    "is_resigned": false,
                    "is_activated": true,
                    "is_exited": false,
                    "is_unjoin": false
                }
            },
            {
                "user_id": "ou_01b081675121a1dc920ffab97cdc4567",
                "mobile": "130xxxx2222",
                "status": {
                    "is_frozen": false,
                    "is_resigned": false,
                    "is_activated": true,
                    "is_exited": false,
                    "is_unjoin": false
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
| - | - | 暂无（具体错误码请参考[通用错误码](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN)） |

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
| 配置应用数据权限 | [https://open.feishu.cn/document/home/introduction-to-scope-and-authorization/configure-app-data-permissions](https://open.feishu.cn/document/home/introduction-to-scope-and-authorization/configure-app-data-permissions) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |