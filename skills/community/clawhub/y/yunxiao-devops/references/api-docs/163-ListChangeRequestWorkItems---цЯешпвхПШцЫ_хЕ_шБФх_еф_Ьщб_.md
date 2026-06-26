# ListChangeRequestWorkItems - 查询变更关联工作项

通过 OpenAPI 查询变更关联工作项。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 变更 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeRequests/{sn}/workItems`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| sn | string | path | 是 | 变更标识符。 | f1e78f22428e4e2496a0169181xxxxx |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exxxxx/apps/my-web-service/changeRequests/f1e78f22428e4e2496a0169181xxxxx/workItems' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| description | string | 变更工作项描述。 | 项目 A 下的 bug 工作项 |
| name | string | 变更工作项名称。 | 修复 bug |
| sn | string | 变更工作项唯一标识。 | 3344b6fdd94f43628f63b126209xxxxx |
| type | string | 变更工作项类型：PROJEX-Projex工作项，COMMON-其他事项。 | PROJEX |
| value | string | 变更工作项内容。 | 修复 bug，修改文件 A 和文件 B |

## **返回示例**

`[ { "description": "项目A下的bug工作项", "name": "修复bug", "sn": "3344b6fdd94f43628f63b126209xxxxx", "type": "PROJEX", "value": "修复bug，修改文件A和文件B" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。