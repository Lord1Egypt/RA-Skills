# GetChangeRequestAuditItems - 查找变更关联的审批项列表

通过OpenAPI查找变更关联的审批项列表。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeRequests/{sn}/auditItems`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| sn | string | path | 是 | 变更标识符。 | eb4aee827214408e8d2dda49f0c0xxxx |
| refType | string | query | 是 | 关联类型：CR。 | CR |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exxxxx/apps/my-web-service/changeRequests/eb4aee827214408e8d2dda49f0c0xxxx/auditItems?refType=CR' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array\[\] |  |  |
| \- OneOf | object | 代码审核审批项。 |  |
| auditOrderSn | string | 审批单编号。 | c695782863c3479db8909d696c24xxxx |
| commitId | string | 代码提交 ID。 | c229f22024535638af41838daa43af1e6d46xxxx |
| crId | string | 变更 ID。 | cr-123 |
| operatorId | string | 代码提交人 ID。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| refSn | string | 审批关联对象标识符。 |  |
| refType | string | 审批关联类型：CR。 | CR |
| sourceVersion | string | 代码来源分支版本。 | c229f22024535638af41838daa43af1e6d46xxxx |
| state | string | 审批状态：INIT 初始化, WAIT 等待中, AUDITING 审核中, PASS 审核通过, FAILED 审核不通过, CANCELED 已取消, NO\_NEED 无需审核。 | PASS |
| targetVersion | string | 代码目标分支版本。 | c229f22024535638af41838daa43af1e6d46xxxx |
| type | string | 审批类型：CODE\_REVIEW 代码审核， CODE\_SPLC 代码扫描。 | CODE\_REVIEW |
| url | string | 代码提交 URL。 | http://xxxxxxx |
| \- OneOf | object | 代码扫描审批项。 |  |
| auditOrderSn | string | 审批单编号。 | c695782863c3479db8909d696c24xxxx |
| commitDate | string | 提交时间。 | 2024-09-01 00:00:00 |
| commitEmployeeId | string | 提交人。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| commitMsg | string | 提交信息。 | message-xxx |
| crId | string | 变更 ID。 | cr-123 |
| refSn | string | 审批关联对象标识符。 |  |
| refType | string | 审批关联类型：CR。 | CR |
| state | string | 审批状态：INIT 初始化, WAIT 等待中, AUDITING 审核中, PASS 审核通过, FAILED 审核不通过, CANCELED 已取消, NO\_NEED 无需审核。 | PASS |
| trunkVersion | string | 主干版本。 | trunk-version-xxx |
| type | string | 审批类型：CODE\_REVIEW 代码审核，CODE\_SPLC 代码扫描。 | CODE\_SPLC |
| url | string | 提交地址。 | http://xxxxxxx |
| version | string | 变更版本。 | version-xxx |

## **返回示例**

`[ "- OneOf": { "auditOrderSn": "c695782863c3479db8909d696c24xxxx", "commitId": "c229f22024535638af41838daa43af1e6d46xxxx", "crId": "cr-123", "operatorId": "1c83bd48e254405fb27297ee1fb8xxxx", "refSn": "", "refType": "CR", "sourceVersion": "c229f22024535638af41838daa43af1e6d46xxxx", "state": "PASS", "targetVersion": "c229f22024535638af41838daa43af1e6d46xxxx", "type": "CODE_REVIEW", "url": "http://xxxxxxx" }, "- OneOf": { "auditOrderSn": "c695782863c3479db8909d696c24xxxx", "commitDate": "2024-09-01 00:00:00", "commitEmployeeId": "1c83bd48e254405fb27297ee1fb8xxxx", "commitMsg": "message-xxx", "crId": "cr-123", "refSn": "", "refType": "CR", "state": "PASS", "trunkVersion": "trunk-version-xxx", "type": "CODE_SPLC", "url": "http://xxxxxxx", "version": "version-xxx" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。