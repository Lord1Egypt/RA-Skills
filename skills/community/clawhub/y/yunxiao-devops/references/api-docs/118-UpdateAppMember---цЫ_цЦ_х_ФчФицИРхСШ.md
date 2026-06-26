# UpdateAppMember - 更新应用成员

通过OpenAPI更新应用成员。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用 | 读写 |

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/members`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-demo-app |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |
| \- | object | body | 否 |  |  |
| player | object | body | 是 | 更新的成员。 |  |
| id | string | body | 否 | 成员 ID。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| type | string | body | 否 | 成员类型，可能的值：\[ User Team Group\]。 | User |
| roleNames | array\[string\] | body | 是 | 更新成员的角色列表：admin 负责人, developer 开发, tester 测试, operator 运维。 | \["admin"\] |

## **请求示例**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-demo-app/members' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "player": { "id": "1c83bd48e254405fb27297ee1fb8xxxx", "type": "User" }, "roleNames": [ "admin" ] }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | string | 调用是否成功。 | true |

## **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。