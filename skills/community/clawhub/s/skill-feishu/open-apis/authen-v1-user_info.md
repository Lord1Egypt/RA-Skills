# 获取用户信息

## 注意事项

手机号和邮箱信息为管理员导入的用户联系方式，未经过用户本人实时验证，不建议开发者直接将其作为业务系统的登录凭证。如使用，务必自行认证。

## 权限要求

### 必要权限

无需权限

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取用户受雇信息 (contact:user.employee:readonly) |
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |
| 字段权限（敏感字段） | 获取用户手机号 (contact:user.phone:readonly) |
| 字段权限（敏感字段） | 获取用户邮箱信息 (contact:user.email:readonly) |
| 字段权限（敏感字段） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 字段权限（敏感字段） | 读取通讯录 (contact:contact:readonly) |
| 字段权限（敏感字段） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/authen/v1/user_info` |
|----------|--------------------------------------------------------|
| 请求方法 | GET |
| 调用频率限制 | 特殊频控 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/ukTMukTMukTM/ugjNz4SO2UjL5jDN/authen-v1/user_info) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

无查询参数

### 请求体

无请求体（GET 请求）

### 请求示例

#### cURL 请求示例

```bash
curl -X GET 'https://open.feishu.cn/open-apis/authen/v1/user_info' \
  -H 'Authorization: Bearer user_access_token' \
  -H 'Content-Type: application/json; charset=utf-8'
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/authen/v1/user_info"
    headers = {
        "Authorization": "Bearer user_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

#### Go 请求示例

```go
import (
	"context"
	"fmt"
	"net/http"
)

func main() {
	url := "https://open.feishu.cn/open-apis/authen/v1/user_info"
	
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("Authorization", "Bearer user_access_token")
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

#### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.core.request.RequestOptions;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 发起请求
        // 注意：该接口使用 user_access_token，无需应用凭证
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
| `data` | object | 用户信息对象 |
| `name` | string | 用户姓名 |
| `en_name` | string | 用户英文名称 |
| `avatar_url` | string | 用户头像 |
| `avatar_thumb` | string | 用户头像 72x72 |
| `avatar_middle` | string | 用户头像 240x240 |
| `avatar_big` | string | 用户头像 640x640 |
| `open_id` | string | 用户在应用内的唯一标识 |
| `union_id` | string | 用户对ISV的唯一标识，对于同一个ISV，用户在其名下所有应用的union_id相同 |
| `email` | string | 用户邮箱。邮箱信息为管理员导入的用户联系方式，未经过用户本人实时验证，不建议开发者直接将其作为业务系统的登录凭证。如使用，务必自行认证。 |
| `enterprise_email` | string | 企业邮箱，请先确保已在管理后台启用飞书邮箱服务 |
| `user_id` | string | 用户 user_id |
| `mobile` | string | 用户手机号。手机号信息为管理员导入的用户联系方式，未经过用户本人实时验证，不建议开发者直接将其作为业务系统的登录凭证。如使用，务必自行认证。 |
| `tenant_key` | string | 当前企业标识 |
| `employee_no` | string | 用户工号 |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "name": "zhangsan",
        "en_name": "zhangsan",
        "avatar_url": "www.feishu.cn/avatar/icon",
        "avatar_thumb": "www.feishu.cn/avatar/icon_thumb",
        "avatar_middle": "www.feishu.cn/avatar/icon_middle",
        "avatar_big": "www.feishu.cn/avatar/icon_big",
        "open_id": "ou-caecc734c2e3328a62489fe0648c4b98779515d3",
        "union_id": "on-d89jhsdhjsajkda7828enjdj328ydhhw3u43yjhdj",
        "email": "zhangsan@feishu.cn",
        "enterprise_email": "demo@mail.com",
        "user_id": "5d9bdxxx",
        "mobile": "+86130002883xx",
        "tenant_key": "736588c92lxf175d",
        "employee_no": "111222333"
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
| 200 | 20001 | Invalid request. Please check request param |
| 200 | 20005 | The user access token passed is invalid. Please check the value |
| 200 | 20008 | User not exist |
| 200 | 20021 | User resigned |
| 200 | 20022 | User frozen |
| 200 | 20023 | User not registered |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 500 | 20050 | System error |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 获取 user_access_token | [获取用户访问凭证](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/authentication-management/access-token/get-user-access-token) |
| 应用权限配置 | [https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 用户相关的 ID 概念 | [https://open.feishu.cn/document/home/user-identity-introduction/introduction](https://open.feishu.cn/document/home/user-identity-introduction/introduction) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |