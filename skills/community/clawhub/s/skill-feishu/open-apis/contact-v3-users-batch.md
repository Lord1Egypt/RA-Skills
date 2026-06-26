# 批量获取用户信息

## 注意事项

该查询接口目前不返回用户的席位（assign_info）和部门路径信息（department_path）。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取通讯录基本信息 (contact:contact.base:readonly) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 查询用户席位信息 (contact:user.assign_info:read) |
| 字段权限（敏感字段） | 获取用户基本信息 (contact:user.base:readonly) |
| 字段权限（敏感字段） | 获取用户组织架构信息 (contact:user.department:readonly) |
| 字段权限（敏感字段） | 获取成员所在部门路径 (contact:user.department_path:readonly) |
| 字段权限（敏感字段） | 查看成员的虚线上级 ID (contact:user.dotted_line_leader_info.read) |
| 字段权限（敏感字段） | 获取用户受雇信息 (contact:user.employee:readonly) |
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |
| 字段权限（敏感字段） | 查看成员工号 (contact:user.employee_number:read) |
| 字段权限（敏感字段） | 获取用户性别 (contact:user.gender:readonly) |
| 字段权限（敏感字段） | 查看成员数据驻留地 (contact:user.user_geo) |
| 字段权限（敏感字段） | 获取用户手机号 (contact:user.phone:readonly) |
| 字段权限（敏感字段） | 分配用户席位 (contact:user.subscription_ids:write) |
| 字段权限（敏感字段） | 获取用户邮箱信息 (contact:user.email:readonly) |
| 字段权限（敏感字段） | 查询用户所属的工作序列 (contact:user.job_family:readonly) |
| 字段权限（敏感字段） | 查询用户职级 (contact:user.job_level:readonly) |
| 字段权限（敏感字段） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 字段权限（敏感字段） | 读取通讯录 (contact:contact:readonly) |
| 字段权限（敏感字段） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/users/batch` |
|----------|----------------------------------------------------------|
| 请求方法 | GET |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/batch_get) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token` 或 `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user_ids` | array | 是 | 用户ID。ID 类型与查询参数 `user_id_type` 保持一致。<br>如需一次查询多个用户ID，可多次传递同一参数名，并且每次传递不同的参数值。例如：`https://{url}?user_ids={user_id1}&user_ids={user_id2}`。<br>单次最大请求可设置的用户 ID 数量上限为 50 |
| `user_id_type` | string | 否 | 用户 ID 类型<br>可选值：<br>- `open_id`：标识一个用户在某个应用中的身份<br>- `union_id`：标识一个用户在某个应用开发商下的身份<br>- `user_id`：标识一个用户在某个租户内的身份<br>默认值：`open_id`<br>**权限要求**：当值为 `user_id` 时，需要获取用户 user ID (contact:user.employee_id:readonly) |
| `department_id_type` | string | 否 | 指定查询结果中的部门 ID 类型<br>可选值：<br>- `open_department_id`：由系统自动生成的部门 ID<br>- `department_id`：支持用户自定义配置的部门 ID<br>默认值：`open_department_id` |

### 请求体

无请求体（GET 请求）

### 请求示例

#### cURL 请求示例

```bash
curl -X GET 'https://open.feishu.cn/open-apis/contact/v3/users/batch?user_ids=ou_xxx&user_ids=ou_yyy&user_id_type=open_id&department_id_type=open_department_id' \
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
	req := larkcontact.NewBatchGetUserReqBuilder().
		UserIdList([]string{
			"7be5fg",
		}).
		UserIdType(`open_id`).
		DepartmentIdType(`open_department_id`).
		Build()

	// 发起请求
	resp, err := client.Contact.User.BatchGet(context.Background(), req)
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
        BatchGetUserReq req = BatchGetUserReq.newBuilder()
                .userIdList(java.util.Arrays.asList("7be5fg"))
                .userIdType("open_id")
                .departmentIdType("open_department_id")
                .build();

        // 发起请求
        BatchGetUserResp resp = client.contact().user().batchGet(req, RequestOptions.newBuilder().build());
    }
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "user_ids": ["ou_xxx", "ou_yyy"],
        "user_id_type": "open_id",
        "department_id_type": "open_department_id"
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
| `items` | array | 查询到的用户信息列表 |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "union_id": "on_94a1ee5551019f18cd73d9f111898cf2",
                "user_id": "3e3cf96b",
                "open_id": "ou_7dab8a3d3cdcc9da365777c7ad535d62",
                "name": "张三",
                "en_name": "San Zhang",
                "nickname": "Alex Zhang",
                "email": "zhangsan@gmail.com",
                "mobile": "13011111111",
                "mobile_visible": false,
                "gender": 1,
                "avatar_key": "2500c7a9-5fff-4d9a-a2de-3d59614ae28g",
                "avatar": {
                    "avatar_72": "https://foo.icon.com/xxxx",
                    "avatar_240": "https://foo.icon.com/xxxx",
                    "avatar_640": "https://foo.icon.com/xxxx",
                    "avatar_origin": "https://foo.icon.com/xxxx"
                },
                "status": {
                    "is_frozen": false,
                    "is_resigned": false,
                    "is_activated": true,
                    "is_exited": false,
                    "is_unjoin": false
                },
                "department_ids": [
                    "od-4e6ac4d14bcd5071a37a39de902c7141"
                ],
                "leader_user_id": "ou_7dab8a3d3cdcc9da365777c7ad535d62",
                "city": "杭州",
                "country": "CN",
                "work_station": "北楼-H34",
                "join_time": 2147483647,
                "is_tenant_manager": false,
                "employee_no": "1",
                "employee_type": 1,
                "orders": [
                    {
                        "department_id": "od-4e6ac4d14bcd5071a37a39de902c7141",
                        "user_order": 100,
                        "department_order": 100,
                        "is_primary_dept": true
                    }
                ],
                "custom_attrs": [
                    {
                        "type": "TEXT",
                        "id": "DemoId",
                        "value": {
                            "text": "DemoText",
                            "url": "http://www.fs.cn",
                            "pc_url": "http://www.fs.cn",
                            "option_id": "option",
                            "option_value": "option",
                            "name": "name",
                            "picture_url": "https://xxxxxxxxxxxxxxxxxx",
                            "generic_user": {
                                "id": "9b2fabg5",
                                "type": 1
                            }
                        }
                    }
                ],
                "enterprise_email": "demo@mail.com",
                "job_title": "xxxxx",
                "is_frozen": false,
                "geo": "cn",
                "job_level_id": "mga5oa8ayjlp9rb",
                "job_family_id": "mga5oa8ayjlp9rb",
                "subscription_ids": [
                    "23213213213123123"
                ],
                "assign_info": [
                    {
                        "subscription_id": "7079609167680782300",
                        "license_plan_key": "suite_enterprise_e5",
                        "product_name": "旗舰版 E5",
                        "i18n_name": {
                            "zh_cn": "zh_cn_name",
                            "ja_jp": "ja_jp_name",
                            "en_us": "en_name"
                        },
                        "start_time": "1674981000",
                        "end_time": "1674991000"
                    }
                ],
                "department_path": [
                    {
                        "department_id": "od-4e6ac4d14bcd5071a37a39de902c7141",
                        "department_name": {
                            "name": "测试部门名1",
                            "i18n_name": {
                                "zh_cn": "测试部门名1",
                                "ja_jp": "試験部署名 1",
                                "en_us": "Testing department name 1"
                            }
                        },
                        "department_path": {
                            "department_ids": [
                                "od-4e6ac4d14bcd5071a37a39de902c7141"
                            ],
                            "department_path_name": {
                                "name": "测试部门名1",
                                "i18n_name": {
                                    "zh_cn": "测试部门名1",
                                    "ja_jp": "試験部署名 1",
                                    "en_us": "Testing department name 1"
                                }
                            }
                        }
                    }
                ],
                "dotted_line_leader_user_ids": [
                    "ou_7dab8a3d3cdcc9da365777c7ad535d62"
                ]
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
| 400 | 40001 | invalid parameter |
| 400 | 41050 | no user authority |
| 403 | 40004 | no dept. authority |

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
| 部门 ID 说明 | [https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview) |
| 权限范围校验 | [https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |