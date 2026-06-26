# API 模板文档

## 限制和要求

这是 API 文档模板。使用此模板创建新的 API 文档时，请严格遵守以下结构和格式。

### 文件命名规范

**API 文件命名和目录结构规则**：

1. **API 路径处理**：
   - 以 `https://open.feishu.cn/open-apis` 开头的接口，文件直接放在 `API/` 目录下
   - 将路径中的 `/` 替换为 `-`，`:` 直接删除
   - 添加 `.md` 后缀

2. **非 standard 路径**：
   - 如果接口路径不是以 `https://open.feishu.cn/open-apis` 开头，**请询问用户**文件名和路径

3. **示例**：
   | API 路径 | 对应文件名 |
   |----------|-------------|
   | `/im/v1/messages` | `im-v1-messages.md` |
   | `/im/v1/messages/:message_id/reply` | `im-v1-messages-message_id-reply.md` |
   | `/auth/v3/tenant_access_token/internal` | `auth-v3-tenant_access_token-internal.md` |
   | `/contact/v3/users` | `contact-v3-users.md` |

### 文档层级结构规范

**API 文档的层级结构必须严格遵循以下格式**：

```
# 接口名称

## 注意事项

## 权限要求

### 必要权限

### 可选权限

## 接口信息

## 接口请求

### 请求头

### 请求参数

### 请求体

### 请求示例

## 接口响应

### 响应头

### 响应体

### 响应示例

## 响应码定义

### 成功码

### 客户端错误码 (4xx)

### 服务端错误码 (5xx)

## 附录

### 按需定义章节标题，例如：相关链接
```

**要求**：
- 一级标题：`#` 接口名称
- 二级标题：`##` 主要章节（注意事项、权限要求、接口信息、接口请求、接口响应、响应码定义、附录）
- 三级标题：`###` 子章节（必要权限、可选权限、请求头、响应头等）
- 禁止使用超出上述级别的标题

### 关于模板说明和模板示例

- **模板说明**：用于说明模板中某些内容的注意事项、强调要点或提供背景信息。这些内容在最终生成文档时，**通常作为提示、说明文字或背景介绍，不会直接作为独立的大节出现**。

- **模板示例**：用于展示实际 API 文档的完整结构和格式。后面根据模板生成文档时，需要按照"模板示例"中的内容和格式来编写实际的文档内容。

### 使用模板生成真实 API 文档的约束

当你根据本模板生成真实的 API 文档时，请严格遵守以下规则：

1. **不要将"关于模板说明和模板示例"的标题及说明文字写入最终文档**。这些内容仅用于指导模板使用者理解如何组织文档。

2. **"关于模板说明和模板示例"的内容**：应作为提示、说明文字嵌入到实际章节的描述中，或作为背景介绍概述，不需要单独作为章节标题。

3. **"关于模板示例"的内容**：直接按示例中的格式和结构编写实际文档内容，使用真实的数据、代码示例和说明。

4. **实际文档_should not_ 包含如下内容**：
   - "关于模板说明和模板示例"的二级标题
   - "参考模板示例中的..."这样的提示语句
   - "请参考..."这类指导性文字

5. **实际文档应该_只有_**：
   - 真实的章节标题（如"注意事项"、"权限要求"、"接口信息"等）
   - 真实的内容（不是模板示例的占位符）
   - 真实的代码示例（不是示例结构）
   - 真实的链接和参考

## 注意事项

### 模板说明

此处说明该接口的使用场景、注意事项等重要信息，特别是：

- 用户身份（user_access_token）调用时的过滤行为
- 应用身份（tenant_access_token）调用时的过滤行为
- 特殊字段的返回条件

### 模板示例

- 使用用户身份（user_access_token）调用该接口时，接口将根据该用户的组织架构可见范围进行过滤，仅返回组织架构可见范围内的用户数据。
- 使用应用身份（tenant_access_token）调用该接口时，接口将根据应用的通讯录权限范围进行过滤。如果请求的部门 ID 为 0（即根部门），则接口会校验应用是否具有全员的通讯录权限；如果请求的是非 0 的部门 ID，则会校验应用是否具有该部门的通讯录权限。无权限时，接口会返回无权限的报错信息；有权限则返回对应部门下的直属用户列表。
- 使用应用身份（tenant_access_token）调用本接口时，响应结果中不会返回部门路径字段（department_path）。如需获取部门路径字段值，请为应用申请 **获取成员所在部门路径（contact:user.department_path:readonly）** API 权限，并使用用户身份（user_access_token）调用接口。

关于用户组织架构可见范围和通讯录权限范围的更多信息，可参见[权限范围资源介绍](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority)。

## 权限要求

### 必要权限

#### 模板说明

调用该 API **必须开启**的权限。开启其中任意一项权限即可调用该接口。

权限类型通常为：
- `应用权限（开启任一即可）` - 应用需要配置的权限

#### 模板示例

| 类型 | 名称 |
|----------|----------|
| 应用权限（开启任一即可） | 获取通讯录基本信息 (contact:contact.base:readonly) |
| 应用权限（开启任一即可） | 获取通讯录部门组织架构信息 (contact:department.organize:readonly) |
| 应用权限（开启任一即可） | 以应用身份访问通讯录 (contact:contact:access_as_app) |
| 应用权限（开启任一即可） | 读取通讯录 (contact:contact:readonly) |
| 应用权限（开启任一即可） | 以应用身份读取通讯录 (contact:contact:readonly_as_app) |

### 可选权限

#### 模板说明

敏感字段的权限要求。如果无需获取这些敏感字段，则不需要申请这些权限。

权限类型通常为：
- `字段权限（敏感字段）` - 敏感字段需要的权限

#### 模板示例

| 类型 | 名称 |
|----------|----------|
| 字段权限（敏感字段） | 统一用户标识 (contact:user.base:readonly) |
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |
| 字段权限（敏感字段） | 应用内用户标识 (contact:user.base:readonly) |
| 字段权限（敏感字段） | 获取用户基本信息 (contact:user.base:readonly) |
| 字段权限（敏感字段） | 获取用户邮箱信息 (contact:user.email:readonly) |
| 字段权限（敏感字段） | 获取用户手机号 (contact:user.phone:readonly) |
| 字段权限（敏感字段） | 获取用户性别 (contact:user.gender:readonly) |
| 字段权限（敏感字段） | 获取用户受雇信息 (contact:user.employee:readonly) |
| 字段权限（敏感字段） | 获取用户组织架构信息 (contact:user.department:readonly) |
| 字段权限（敏感字段） | 查看成员工号 (contact:user.employee_number:read) |
| 字段权限（敏感字段） | 查看成员数据驻留地 (contact:user.user_geo) |
| 字段权限（敏感字段） | 查询用户职级 (contact:user.job_level:readonly) |
| 字段权限（敏感字段） | 查询用户所属的工作序列 (contact:user.job_family:readonly) |
| 字段权限（敏感字段） | 获取成员所在部门路径 (contact:user.department_path:readonly) |
| 字段权限（敏感字段） | 查看成员的虚线上级 ID (contact:user.dotted_line_leader_info.read) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

### 模板说明

接口信息表格展示接口的基本信息，包括：

- **API 路径**：接口的完整 URL
- **请求方法**：GET/POST/PUT/DELETE 等
- **调用频率限制**：每分钟/每秒的调用次数限制
- **支持的应用类型**：Custom App 或 Store App
- **文档地址**：飞书开放平台的文档链接

### 模板示例

| API 路径 | `https://open.feishu.cn/open-apis/contact/v3/users/find_by_department` |
|----------|------------------------------------------------------------------------|
| 请求方法 | GET |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/find_by_department) |

## 接口请求

### 请求头

#### 模板说明

HTTP 请求头字段，用于身份认证和内容类型声明。

**即使请求头无额外字段，也要保留该章节结构**。

**如果某个字段有权限要求，要在"描述"字段中注明权限要求**。权限名称的格式为：`获取用户 user ID (contact:user.employee_id:readonly)`。参考请求参数下模板示例中的 `user_id_type` 权限要求写法。

#### 模板示例

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token` 或 `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

#### 模板说明

URL 查询参数或路径参数，用于传递请求所需的数据。

**参数根据接口提供内容动态生成，不固定在模板里**。

**如果某个参数有权限要求，要在"描述"字段中注明权限要求**。权限名称的格式为：`获取用户 user ID (contact:user.employee_id:readonly)`。参考请求参数下模板示例中的 `user_id_type` 权限要求写法。

#### 模板示例

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user_id_type` | string | 否 | 用户 ID 类型<br>可选值：<br>- `open_id`：标识一个用户在某个应用中的身份<br>- `union_id`：标识一个用户在某个应用开发商下的身份<br>- `user_id`：标识一个用户在某个租户内的身份<br>默认值：`open_id`<br>**权限要求**：当值为 `user_id` 时，需要获取用户 user ID (contact:user.employee_id:readonly) |
| `department_id_type` | string | 否 | 部门 ID 类型<br>可选值：<br>- `department_id`：支持用户自定义配置的部门 ID<br>- `open_department_id`：由系统自动生成的部门 ID<br>默认值：`open_department_id` |
| `department_id` | string | 是 | 部门 ID，ID 类型与 `department_id_type` 的取值保持一致。<br>说明：<br>- 根部门的部门 ID 为 0<br>- 可调用搜索部门接口获取对应的部门 ID |
| `page_size` | int | 否 | 分页大小<br>默认值：`10`<br>数据校验规则：<br>- 最大值：`50` |
| `page_token` | string | 否 | 分页标记，第一次请求不填，表示从头开始遍历 |

### 请求体

#### 模板说明

POST/PUT 请求的 JSON body，GET 请求通常无请求体。

**如果请求体中有字段有权限要求，要在"描述"字段中注明权限要求**。权限名称的格式为：`获取用户 user ID (contact:user.employee_id:readonly)`。参考请求参数下模板示例中的 `user_id_type` 权限要求写法。

#### 模板示例

无请求体（GET 请求）

### 请求示例

#### 模板说明

代码示例展示如何调用该接口，支持多种编程语言和工具。根据实际需要选择示例：

- **Go 和 Java 示例**：使用飞书 SDK（推荐）
- **cURL 示例**：适用于快速测试，基于 HTTP 原生请求
- **Python 示例**：适用于自动化脚本
- **Node.js 示例**：适用于 Node.js 环境

如果官方文档提供了其他语言的示例（如 PHP、C# 等），请参考文档格式添加相应代码。

#### 模板示例

##### cURL 请求示例

cURL 是最简单的 HTTP 请求方式，适合快速测试：

```bash
curl -X GET 'https://open.feishu.cn/open-apis/contact/v3/users?department_id=od_xxx&page_size=10&page_token=AQD9/...' \
  -H 'Authorization: Bearer tenant_access_token' \
  -H 'Content-Type: application/json; charset=utf-8'
```

##### Go 请求示例

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
	req := larkcontact.NewFindByDepartmentUserReqBuilder().
		UserIdType(`open_id`).
		DepartmentIdType(`open_department_id`).
		DepartmentId(`od-xxxxxxxxxxxxx`).
		PageSize(10).
		Build()

	// 发起请求
	resp, err := client.Contact.User.FindByDepartment(context.Background(), req)
}
```

##### Java 请求示例

```java
import com.lark.oapi.Client;
import com.lark.oapi.service.contact.v3.model.*;
import com.lark.oapi.core.request.RequestOptions;

public class Main {
    public static void main(String arg[]) throws Exception {
        // 构建client
        Client client = Client.newBuilder("appId", "appSecret").build();

        // 创建请求对象
        FindByDepartmentUserReq req = FindByDepartmentUserReq.newBuilder()
                .userIdType("open_id")
                .departmentIdType("open_department_id")
                .departmentId("od-xxxxxxxxxxxxx")
                .pageSize(10)
                .build();

        // 发起请求
        FindByDepartmentUserResp resp = client.contact().user().findByDepartment(req, RequestOptions.newBuilder().build());
    }
}
```

##### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department"
    headers = {
        "Authorization": "Bearer tenant_access_token",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "department_id": "od-xxxxxxxxxxxxx",
        "department_id_type": "open_department_id",
        "user_id_type": "open_id",
        "page_size": 10
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

## 接口响应

### 响应头

#### 模板说明

HTTP 响应头字段。

**即使响应头无额外字段，也要保留该章节结构**。

**如果某个字段有权限要求，要在"描述"字段中注明权限要求**。权限名称的格式为：`获取用户 user ID (contact:user.employee_id:readonly)`。参考请求参数下模板示例中的 `user_id_type` 权限要求写法。

#### 模板示例

| 名称 | 类型 | 描述 |
|------|------|------|
| - | - | 无额外响应头字段 |

### 响应体

#### 模板说明

JSON 响应体结构，包含 code、msg 和 data 字段。**响应体具体字段根据接口返回内容动态生成，不固定**。

**如果某个字段有权限要求，要在"描述"字段中注明权限要求**。权限名称的格式为：`获取用户 user ID (contact:user.employee_id:readonly)`。参考请求参数下模板示例中的 `user_id_type` 权限要求写法。

#### 模板示例

| 字段 | 类型 | 描述 |
|------|------|------|
| `code` | int | 错误码，非 0 表示失败 |
| `msg` | string | 错误描述 |
| `data` | object | 响应数据，根据接口类型动态变化 |

### 响应示例

#### 模板说明

完整的响应 JSON 示例。

#### 模板示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "has_more": true,
        "page_token": "AQD9/Rn9eij9Pm39ED40/RD/cIFmu77WxpxPB/2oHfQLZ%2BG8JG6tK7%2BZnHiT7COhD2hMSICh/eBl7cpzU6JEC3J7COKNe4jrQ8ExwBCR",
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
                            "option_id": "edcvfrtg",
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
                "department_path": [
                    {
                        "department_id": "od-4e6ac4d14bcd5071a37a39de902c7141",
                        "department_name": {
                            "name": "测试部门名1",
                            "i18n_name": {
                                "zh_cn": "测试部门名1",
                                "ja_jp": "試験部署名 1",
                                "en_us": "Test department name 1"
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
                                    "en_us": "Test department name 1"
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

### 模板说明

响应码表格列出该接口可能返回的 HTTP 状态码、错误码或成功码。

**请按以下顺序组织响应码**：

1. **成功码**（2xx）放在最上边，表示请求成功处理
2. **客户端错误码**（4xx）在中间，表示客户端请求问题
3. **服务端错误码**（5xx）在最后，表示服务端错误

这样可以快速区分成功和错误情况。

### 模板示例

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 200 | 0 | 请求成功 |
| 400 | 41050 | no user authority error |
| 400 | 40011 | page size is invalid |
| 400 | 40012 | page token is invalid error |
| 403 | 40004 | no dept authority error |

## 附录

### 模板说明

附录是一个总括性的章节，用于存放接口文档的补充信息。

通过模板在生成接口文档时，会根据接口实际情况自动判断是否需要添加额外的补充信息章节，补充信息章节必须用二级分类章节的形式。请参考"模板示例"下的"相关链接"

### 模板示例

#### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 应用权限配置 | [https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 用户相关的 ID 概念 | [https://open.feishu.cn/document/home/user-identity-introduction/introduction](https://open.feishu.cn/document/home/user-identity-introduction/introduction) |
| 部门 ID 说明 | [https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview) |
| 权限范围校验 | [https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |