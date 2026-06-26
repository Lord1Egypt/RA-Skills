# ListUserResources - 查询用户有权限的资源

通过 OpenAPI 查询用户有权限的资源，包括代码库和代码组。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 用户资源 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/users/vision/user_resources`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/users/vision/user_resources
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| user\_ids | string | query | 否 | 用户 ID 列表，多个用逗号分隔。 | 62c795xxxb468af8,62c795xxxb468af9 |
| page | integer | query | 否 | 页码，默认从1开始。 | 1 |
| per\_page | integer | query | 否 | 每页大小，默认10，最大20。 | 10 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/users/vision/user_resources?user_ids=62c795xxxb468af8,62c795xxxb468af9&page=1&per_page=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/users/vision/user_resources?user_ids=62c795xxxb468af8,62c795xxxb468af9&page=1&per_page=10' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| group\_infos | array | 用户所属的代码组列表。 |  |
| \- | object |  |  |
| group\_info | object |  |  |
| avatar | string | 头像地址。 | https://example.com/avatar.png |
| created\_at | string | 创建时间。 | 2025-04-21T10:16:45+08:00 |
| description | string | 代码组描述。 | 代码组描述信息 |
| id | integer | 代码组 ID。 | 2813489 |
| name | string | 代码组名称。 | demo-group |
| path | string | 代码组路径。 | demo-group |
| updated\_at | string | 更新时间。 | 2025-07-14T10:31:41+08:00 |
| visibility\_level | string | 可见性：0-私有，10-内部公开。 | 0 |
| role\_info | object |  |  |
| access\_level | integer | 访问权限：20-浏览者，30-开发者，40-管理员。 | 30 |
| cn\_role\_name | string | 角色名称（中文）。 | 开发者 |
| en\_role\_name | string | 角色名称（英文）。 | Developer |
| source\_id | integer | 资源 ID。 | 2813489 |
| source\_type | string | 资源类型：PROJECT-代码库，NAMESPACE-代码组。 | PROJECT |
| repository\_infos | array | 用户所属的代码库列表。 |  |
| \- | object |  |  |
| repository\_info | object |  |  |
| avatarUrl | string | 头像地址。 | https://example.com/avatar.png |
| created\_at | string | 创建时间。 | 2025-06-25T10:27:09+08:00 |
| description | string | 代码库描述。 | 代码库描述信息 |
| id | integer | 代码库 ID。 | 2813489 |
| last\_activity\_at | string | 最后活跃时间。 | 2025-09-18T10:59:35+08:00 |
| name | string | 代码库名称。 | demo-repo |
| nameWithNamespace | string | 代码库完整名称（含完整组名称）。 | demo-group / demo-repo |
| path | string | 代码库路径。 | demo-repo |
| updated\_at | string | 更新时间。 | 2025-09-18T10:59:35+08:00 |
| visibility\_level | string | 可见性：0-私有，10-内部公开。 | 0 |
| role\_info | object |  |  |
| access\_level | integer | 访问权限：20-浏览者，30-开发者，40-管理员。 | 30 |
| cn\_role\_name | string | 角色名称（中文）。 | 开发者 |
| en\_role\_name | string | 角色名称（英文）。 | Developer |
| source\_id | integer | 资源 ID。 | 2813489 |
| source\_type | string | 资源类型：PROJECT-代码库，NAMESPACE-代码组。 | PROJECT |
| user\_info | object |  |  |
| avatar | string | 头像地址。 | https://example.com/avatar.png |
| email | string | 邮箱。 | zhangsan@example.com |
| id | integer | 用户 ID。 | 2813489 |
| name | string | 用户名称。 | 张三 |
| username | string | 用户名。 | zhangsan |

## **返回示例**

`[ { "group_infos": [ { "group_info": { "avatar": "https://example.com/avatar.png", "created_at": "2025-04-21T10:16:45+08:00", "description": "代码组描述信息", "id": 2813489, "name": "demo-group", "path": "demo-group", "updated_at": "2025-07-14T10:31:41+08:00", "visibility_level": "0" }, "role_info": { "access_level": 30, "cn_role_name": "开发者", "en_role_name": "Developer", "source_id": 2813489, "source_type": "PROJECT" } } ], "repository_infos": [ { "repository_info": { "avatarUrl": "https://example.com/avatar.png", "created_at": "2025-06-25T10:27:09+08:00", "description": "代码库描述信息", "id": 2813489, "last_activity_at": "2025-09-18T10:59:35+08:00", "name": "demo-repo", "nameWithNamespace": "demo-group / demo-repo", "path": "demo-repo", "updated_at": "2025-09-18T10:59:35+08:00", "visibility_level": "0" }, "role_info": { "access_level": 30, "cn_role_name": "开发者", "en_role_name": "Developer", "source_id": 2813489, "source_type": "PROJECT" } } ], "user_info": { "avatar": "https://example.com/avatar.png", "email": "zhangsan@example.com", "id": 2813489, "name": "张三", "username": "zhangsan" } } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 2 |
| x-page | 当前页。 | 1 |
| x-per-page | 每页大小。 | 10 |
| x-prev-page | 上一页。 | 0 |
| x-total | 总条数。 | 100 |
| x-total-pages | 总页数。 | 10 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。