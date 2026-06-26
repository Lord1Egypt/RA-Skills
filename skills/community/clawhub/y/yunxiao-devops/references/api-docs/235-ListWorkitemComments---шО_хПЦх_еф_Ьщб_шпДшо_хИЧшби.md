# ListWorkitemComments - 获取工作项评论列表

通过 OpenAPI 获取工作项评论列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项评论 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/comments`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 工作项唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/comments' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| content | string | 评论内容。 | test |
| contentFormat | string | 内容格式，RICHTEXT 或是 MARKDOWN。 | RICHTEXT |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | id。 | id-xxx |
| parentId | string | 父评论 id。 | 1222333 |
| top | boolean | 是否置顶。 | false |
| topTime | string | 置顶时间。 |  |
| user | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |

## **返回示例**

`[ { "content": "test", "contentFormat": "RICHTEXT", "gmtCreate": "", "gmtModified": "", "id": "id-xxx", "parentId": "1222333", "top": false, "topTime": "", "user": { "id": "674d96abd497cd558d68****", "name": "name-xxx" } } ]`

### **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。