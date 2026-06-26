# GetTask - 查看批量任务

通过 OpenAPI 查看批量任务。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 制品仓库 | 批量任务 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/packages/organizations/{organizationId}/tasks/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | xxxxxxxx |
| id | integer | path | 是 | 任务 ID，参见来源:DeleteArtifact - 删除单个制品 API 的返回值。 | 123456 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/packages/organizations/xxxxxxxx/tasks/123456' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 批量任务。 |  |
| action | string | 行为, REPO\_DEL:删除仓库,REPO\_RES:恢复仓库,MODULE\_DEL:删除制品,MODULE\_RES:恢复制品。 | MODULE\_DEL |
| data | string | 操作的对象信息。 | module id |
| description | string | 描述信息。 | 删除 abc 等制品 |
| gmtCreate | integer | 任务创建时间。 | 1728557118000 |
| id | integer | 任务id。 | 123456 |
| repoId | string | 仓库 Id。 | flow\_generic\_repo |
| repoType | string | 仓库类型。 | GENERIC |
| status | string | 任务状态,INIT:初始化,RUNNING:运行中，SUCCESS:运行成功,FAILED:运行失败。 | RUNNING |

## **返回示例**

`{ "action": "MODULE_DEL", "data": "module id", "description": "删除abc等制品", "gmtCreate": 1728557118000, "id": 123456, "repoId": "flow_generic_repo", "repoType": "GENERIC", "status": "RUNNING" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。