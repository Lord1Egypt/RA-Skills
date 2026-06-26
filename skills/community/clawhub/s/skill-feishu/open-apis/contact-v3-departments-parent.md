# 获取父部门信息

## 注意事项

- 使用应用身份（tenant_access_token）调用本接口时，该接口只返回应用通讯录可见范围内的父部门信息。例如有 A > B > C > D 四层级部门关系，当前应用的通讯录权限内只包含了 B 部门，那么查询 D 部门的父部门信息时，只会返回 B、C 部门信息，不会返回 A 部门信息。了解权限范围参见[权限范围资源介绍](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority)。

- 使用用户身份（user_access_token）调用本接口时，只返回对当前用户有可见性的部门信息。用户的组织架构可见范围需要由企业管理员在[管理后台](https://feishu.cn/admin/index) > **安全** > **成员权限** > **组织架构可见范围** 内调整。

- 所能查询到的父部门不包括根部门。

- 当返回列表内包含多个部门信息时，会按照由子部门到父部门的顺序进行展示。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取通讯录基本信息 (contact:contact.base:readonly) |
| 应用权限（开启任一即可） | 获取通讯录部门组织架构信息 (contact:department.organize:readonly) |
| 应用权限（开启任一即可） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 应用权限（开启任一即可） | 读取通讯录 (contact:contact:readonly) |
| 应用权限（开启任一即可） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

### 可选权限

| 类型 | 名称 |
|------|------|
| 字段权限（敏感字段） | 获取通讯录部门组织架构信息 (contact:department.organize:readonly) |
| 字段权限（敏感字段） | 获取部门基础信息 (contact:department.base:readonly) |
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |
| 字段权限（敏感字段） | 查询部门 HRBP 信息 (contact:department.hrbp:readonly) |
| 字段权限（敏感字段） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 字段权限（敏感字段） | 读取通讯录 (contact:contact:readonly) |
| 字段权限（敏感字段） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/departments/parent` |
|----------|-------------------------------------------------------------------|
| 请求方法 | GET |
| 调用频率限制 | 特殊频控 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/parent) |

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
| `department_id_type` | string | 否 | 此次调用中的部门 ID 类型<br>可选值：<br>- `department_id`：支持用户自定义配置的部门 ID<br>- `open_department_id`：由系统自动生成的部门 ID<br>默认值：`open_department_id` |
| `department_id` | string | 是 | 部门 ID。ID 类型需要与查询参数 `department_id_type` 的取值保持一致。<br>当你在创建部门时，可从返回结果中获取到部门 ID 信息，你也可以调用搜索部门接口，获取所需的部门 ID |
| `page_token` | string | 否 | 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果 |
| `page_size` | int | 否 | 分页大小，用于限制一次请求所返回的数据条目数<br>默认值：`20`<br>最大值：`50` |

### 请求体

无请求体（GET 请求）

### 请求示例

#### cURL 请求示例

```bash
curl -X GET 'https://open.feishu.cn/open-apis/contact/v3/departments/parent?department_id=od-4e6ac4d14bcd5071a37a39de902c7141&department_id_type=open_department_id&user_id_type=open_id&page_size=20' \
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
	req := larkcontact.NewParentDepartmentReqBuilder().
		DepartmentId(`od-4e6ac4d14bcd5071a37a39de902c7141`).
		PageSize(20).
		Build()

	// 发起请求
	resp, err := client.Contact.Department.Parent(context.Background(), req)
}
```

#### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.core.request.RequestOptions;
import com.lark.oapi.service.contact.v3.model.ParentDepartmentReq;
import com.lark.oapi.service.contact.v3.model.ParentDepartmentResp;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 创建请求对象
        ParentDepartmentReq req = ParentDepartmentReq.newBuilder()
                .departmentId("od-4e6ac4d14bcd5071a37a39de902c7141")
                .pageSize(20)
                .build();

        // 发起请求
        ParentDepartmentResp resp = client.contact().department().parent(req, RequestOptions.newBuilder().build());
    }
}
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/departments/parent"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "department_id": "od-4e6ac4d14bcd5071a37a39de902c7141",
        "department_id_type": "open_department_id",
        "user_id_type": "open_id",
        "page_size": 20
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
| `has_more` | boolean | 是否还有更多项 |
| `page_token` | string | 分页标记，当 `has_more` 为 true 时，会同时返回新的 `page_token` |
| `items` | array | 部门列表 |

#### department 对象

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 部门名称 |
| `i18n_name` | object | 部门名称的国际化配置 |
| `parent_department_id` | string | 父部门的部门 ID |
| `department_id` | string | 自定义部门 ID |
| `open_department_id` | string | 部门的 open_department_id |
| `leader_user_id` | string | 部门主管的用户 ID |
| `chat_id` | string | 部门群的群 ID |
| `order` | string | 部门的排序 |
| `unit_ids` | array | 部门绑定的单位自定义 ID 列表 |
| `member_count` | int | 当前部门及其下属部门的用户（包含部门负责人）个数 |
| `status` | object | 部门状态 |
| `leaders` | array | 部门负责人信息列表 |
| `group_chat_employee_types` | array | 部门群的人员类型限制 |
| `department_hrbps` | array | 部门 HRBP 的用户 ID 列表 |
| `primary_member_count` | int | 当前部门及其下属部门的主属成员数量 |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "has_more": true,
        "page_token": "AQD9/Rn9eij9Pm39ED40/RD/cIFmu77WxpxPB/2oHfQLZ%2BG8JG6tK7%2BZnHiT7COhD2hMSICh/eBl7cpzU6JEC3J7COKNe4jrQ8ExwBCR",
        "items": [
            {
                "name": "DemoName",
                "i18n_name": {
                    "zh_cn": "Demo名称",
                    "ja_jp": "デモ名",
                    "en_us": "Demo Name"
                },
                "parent_department_id": "D067",
                "department_id": "D096",
                "open_department_id": "od-4e6ac4d14bcd5071a37a39de902c7141",
                "leader_user_id": "ou_7dab8a3d3cdcc9da365777c7ad535d62",
                "chat_id": "oc_5ad11d72b830411d72b836c20",
                "order": "100",
                "unit_ids": [
                    "custom_unit_id"
                ],
                "member_count": 100,
                "status": {
                    "is_deleted": false
                },
                "leaders": [
                    {
                        "leaderType": 1,
                        "leaderID": "ou_7dab8a3d3cdcc9da365777c7ad535d62"
                    }
                ],
                "group_chat_employee_types": [
                    1
                ],
                "department_hrbps": [
                    "ou_7dab8a3d3cdcc9da365777c7ad535d62"
                ],
                "primary_member_count": 100
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
| 400 | 40001 | param error |
| 400 | 40002 | process root dept error |
| 400 | 40003 | internal error |
| 400 | 40008 | dept Info is null error |
| 400 | 40010 | chat id is invalid error |
| 400 | 40011 | page size is invalid |
| 400 | 40012 | page token is invalid error |
| 400 | 43001 | dept unit repeat error |
| 400 | 43002 | dept unit is still using error |
| 400 | 43003 | multi dept unit error |
| 400 | 43004 | illegal unit error |
| 400 | 43005 | duplicate order error |
| 400 | 43007 | duplicated department custom id error |
| 400 | 43008 | custom dept id invalid error |
| 400 | 43009 | exceed update custom dept limit error |
| 400 | 43010 | big dept forbid recursion error |
| 400 | 43011 | delete has member dept error |
| 400 | 43012 | delete has sub dept department error |
| 400 | 43013 | dept too many children error |
| 400 | 44102 | miss department_id error |
| 401 | 42008 | tenant id is invalid error |
| 403 | 40004 | no dept authority error |
| 403 | 40014 | no parent dept authority error |

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