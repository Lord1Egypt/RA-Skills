# 批量获取脱敏的用户登录信息

## 注意事项

该接口用于查询用户的登录信息。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取用户登录信息（mask）(passport:session_mask:readonly) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/passport/v1/sessions/query` |
|----------|---------------------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | 10 次/分钟 |
| 支持的应用类型 | Custom App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/ukTMukTMukTM/reference/passport-v1/session/query) |

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
| `user_ids` | array | 否 | 用户 ID<br>最大长度：`100` |

### 请求示例

#### cURL 请求示例

```bash
curl -X POST 'https://open.feishu.cn/open-apis/passport/v1/sessions/query?user_id_type=open_id' \
  -H 'Authorization: Bearer tenant_access_token' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "user_ids": ["7aeddb6a1", "7aeddb6a2", "7aeddb6a3"]
  }'
```

#### Go 请求示例

```go
import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	url := "https://open.feishu.cn/open-apis/passport/v1/sessions/query?user_id_type=open_id"
	
	data := map[string]interface{}{
		"user_ids": []string{"7aeddb6a1", "7aeddb6a2", "7aeddb6a3"},
	}
	
	jsonData, _ := json.Marshal(data)
	
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer tenant_access_token")
	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()
	
	fmt.Println("Response status:", resp.Status)
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/passport/v1/sessions/query"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "user_id_type": "open_id"
    }
    data = {
        "user_ids": ["7aeddb6a1", "7aeddb6a2", "7aeddb6a3"]
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

#### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.core.request.RequestOptions;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 注意：该接口路径为 passport/v1/sessions/query
        // 飞书 SDK 可能不包含此接口，建议直接使用 HTTP 请求
    }
}
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
| `mask_sessions` | array | 用户登录信息列表 |

#### mask_sessions 对象

| 字段 | 类型 | 描述 |
|------|------|------|
| `create_time` | string | 创建时间 |
| `terminal_type` | int | 客户端类型<br>可选值：<br>- `0`：未知<br>- `1`：个人电脑<br>- `2`：浏览器<br>- `3`：安卓手机<br>- `4`：Apple手机<br>- `5`：服务端<br>- `6`：旧版小程序端<br>- `8`：其他移动端 |
| `user_id` | string | 用户ID |
| `sid` | string | 需要登出的 session 标识符 |

### 响应示例

```json
{
    "code": 0,
    "data": {
        "mask_sessions": [
            {
                "create_time": "1644980493",
                "terminal_type": 2,
                "user_id": "47f183f1f1",
                "sid": "ABBAAAAAAANll6nQoIAAFA=="
            },
            {
                "create_time": "1644983127",
                "terminal_type": 2,
                "user_id": "47f183ff1",
                "sid": "ACCAAAAAAANll6nQoIAAFA=="
            },
            {
                "create_time": "1644983127",
                "terminal_type": 2,
                "user_id": "47f183ff2",
                "sid": "BBBAAAAAAANll6nQoIAAFA=="
            }
        ]
    },
    "msg": ""
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
| 400 | 1080001 | param is invalis |

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
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |