# UpdateProtectedBranch - 更新保护分支

通过 OpenAPI 更新保护分支。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 保护分支 | 读写 |

## **请求语法**

### **中心版**

`PUT https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches/{id}`

### **Region版**

```
PUT https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/protectedBranches/{id}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| repositoryId | string | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| id | integer | path | 是 | 保护分支规则主键 ID。 | 1 |
| \- | object | body | 否 |  |  |
| allowMergeRoles | array\[integer\] | body | 否 | 允许合并的角色列表：40-管理员，30-开发者。 | \[40, 30\] |
| allowMergeUserIds | array\[string\] | body | 否 | 允许合并的用户 ID 列表。 | \["62c795xxxb468af8"\] |
| allowPushRoles | array\[integer\] | body | 否 | 允许推送的角色列表：40-管理员，30-开发者。 | \[40, 30\] |
| allowPushUserIds | array\[string\] | body | 否 | 允许推送用户 ID 列表。 | \["62c795xxxb468af8"\] |
| branch | string | body | 是 | 被保护分支名称。 | master |
| mergeRequestSetting | object | body | 否 | 要求合并前通过代码评审。 |  |
| allowMergeRequestRoles | array\[integer\] | body | 否 | 允许合并请求的角色列表。 | \[40, 30\] |
| defaultAssignees | array\[string\] | body | 否 | 默认评审人 ID 列表。 | \["62c795xxxb468af8"\] |
| isAllowSelfApproval | boolean | body | 否 | 是否允许创建者通过代码评审。 | false |
| isAllowSourceBranchPushUserApproval | boolean | body | 否 | 是否允许源分支的提交者通过合并请求。 | false |
| isRequireDiscussionProcessed | boolean | body | 否 | 是否要求评审全部已解决。 | true |
| isRequired | boolean | body | 否 | 是否开启【要求合并前通过代码评审】。 | true |
| isResetApprovalWhenNewPush | boolean | body | 否 | 是否在有推送时重置评审状态。 | true |
| minimumApproval | integer | body | 否 | 评审通过的最少人数，仅普通模式生效。 | 1 |
| mrMode | string | body | 否 | 评审模式：general - 普通模式, codeowner - CodeOwner 模式。 | general |
| whiteList | string | body | 否 | 评审文件白名单；输入文件路径，多行以换行符隔开，通配符请使用英文格式。 | \*.java |
| testSetting | object | body | 否 | 要求合并前通过自动化状态检查。 |  |
| checkCheckRunConfig | object | body | 否 | 运行检查。 |  |
| checkRunCheckItems | array | body | 否 | 配置项列表。 |  |
| \- | object | body | 否 |  |  |
| id | string | body | 否 | 写入人的 ID。 | 62c795xxxb468af8 |
| name | string | body | 否 | check run 的名称。 | default-test-check-run-name |
| required | boolean | body | 否 | 是否作为卡点。 | true |
| type | string | body | 否 | 写入人类型：User。 | User |
| checkCommitStatusConfig | object | body | 否 | 提交状态。 |  |
| commitStatusCheckItems | array | body | 否 | 配置项列表。 |  |
| \- | object | body | 否 |  |  |
| context | string | body | 否 | 三方提交状态的名称（以名称作为卡点的匹配项）。 | default-context |
| required | boolean | body | 否 | 是否作为卡点。 | true |
| checkConfig | object | body | 否 | 流水线检查。 |  |
| checkItems | array | body | 否 | 配置项列表。 |  |
| \- | object | body | 否 |  |  |
| isRequired | boolean | body | 否 | 是否是卡点项。 | true |
| pipelineId | integer | body | 否 | 流水线 ID。 | 1880578 |
| pipelineName | string | body | 否 | 流水线名称。 | 测试代码检测 |
| checkTaskQualityConfig | object | body | 否 | 代码检测任务。 |  |
| bizNo | string | body | 否 | 检测任务流水线号。 | 202207270957450000110900090430096 |
| enabled | boolean | body | 否 | 是否开启代码检测。 | true |
| message | string | body | 否 | 描述信息。 | codeup-demo 测试代码检测任务 |
| taskName | string | body | 否 | 检测任务名称。 | codeup-demo 测试检测 |
| isRequired | boolean | body | 否 | 是否开启【要求合并前通过自动化状态检查】。 | true |

## **请求示例**

### **中心版**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/protectedBranches/1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "allowMergeRoles": [40, 30], "allowMergeUserIds": ["62c795xxxb468af8"], "allowPushRoles": [40, 30], "allowPushUserIds": ["62c795xxxb468af8"], "branch": "master", "mergeRequestSetting": { "allowMergeRequestRoles": [40, 30], "defaultAssignees": ["62c795xxxb468af8"], "isAllowSelfApproval": false, "isAllowSourceBranchPushUserApproval": false, "isRequireDiscussionProcessed": true, "isRequired": true, "isResetApprovalWhenNewPush": true, "minimumApproval": 1, "mrMode": "general", "whiteList": "*.java" }, "testSetting": { "checkCheckRunConfig": { "checkRunCheckItems": [ { "id": "62c795xxxb468af8", "name": "default-test-check-run-name", "required": true, "type": "User" } ] }, "checkCommitStatusConfig": { "commitStatusCheckItems": [ { "context": "default-context", "required": true } ] }, "checkConfig": { "checkItems": [ { "isRequired": true, "pipelineId": 1880578, "pipelineName": "测试代码检测" } ] }, "checkTaskQualityConfig": { "bizNo": "202207270957450000110900090430096", "enabled": true, "message": "codeup-demo测试代码检测任务", "taskName": "codeup-demo测试检测" }, "isRequired": true } }'`

### **Region版**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/protectedBranches/1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "allowMergeRoles": [40, 30],
        "allowMergeUserIds": ["62c795xxxb468af8"],
        "allowPushRoles": [40, 30],
        "allowPushUserIds": ["62c795xxxb468af8"],
        "branch": "master",
        "mergeRequestSetting": {
            "allowMergeRequestRoles": [40, 30],
            "defaultAssignees": ["62c795xxxb468af8"],
            "isAllowSelfApproval": false,
            "isAllowSourceBranchPushUserApproval": false,
            "isRequireDiscussionProcessed": true,
            "isRequired": true,
            "isResetApprovalWhenNewPush": true,
            "minimumApproval": 1,
            "mrMode": "general",
            "whiteList": "*.java"
        },
        "testSetting": {
            "checkCheckRunConfig": {
                "checkRunCheckItems": [
                    {
                        "id": "62c795xxxb468af8",
                        "name": "default-test-check-run-name",
                        "required": true,
                        "type": "User"
                    }
                ]
            },
            "checkCommitStatusConfig": {
                "commitStatusCheckItems": [
                    {
                        "context": "default-context",
                        "required": true
                    }
                ]
            },
            "checkConfig": {
                "checkItems": [
                    {
                        "isRequired": true,
                        "pipelineId": 1880578,
                        "pipelineName": "测试代码检测"
                    }
                ]
            },
            "checkTaskQualityConfig": {
                "bizNo": "202207270957450000110900090430096",
                "enabled": true,
                "message": "codeup-demo测试代码检测任务",
                "taskName": "codeup-demo测试检测"
            },
            "isRequired": true
        }
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| allowMergeRoles | array\[integer\] | 允许合并的角色列表：40-管理员，30-开发者。 | \[40, 30\] |
| allowMergeUserIds | array\[string\] | 允许合并的用户 ID 列表。 | \["62c795xxxb468af8"\] |
| allowMergeUsers | array | 允许合并的用户列表。 |  |
| \- | object |  |  |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-demo |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| allowPushRoles | array\[integer\] | 允许推送的角色列表：40-管理员，30-开发者。 | \[40, 30\] |
| allowPushUserIds | array\[string\] | 允许推送用户 ID 列表。 | \["62c795xxxb468af8"\] |
| allowPushUsers | array | 允许推送的用户列表。 |  |
| \- | object |  |  |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-demo |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| branch | string | 分支名称。 | master |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| id | integer | 保护分支规则 ID。 | 1 |
| matches | array\[string\] | 匹配的分支列表。 | \["master"\] |
| mergeRequestSetting | object |  |  |
| allowMergeRequestRoles | array\[integer\] | 允许合并请求的角色列表。 | \[40, 30\] |
| defaultAssignees | array | 默认评审人列表。 |  |
| \- | object |  |  |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-demo |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| isAllowSelfApproval | boolean | 是否允许创建者通过代码评审。 | false |
| isAllowSourceBranchPushUserApproval | boolean | 是否允许源分支的提交者通过合并请求。 | false |
| isRequireDiscussionProcessed | boolean | 是否要求评审全部已解决。 | true |
| isRequired | boolean | 是否开启。 | true |
| isResetApprovalWhenNewPush | boolean | 是否在有推送时重置评审状态。 | true |
| minimumApproval | integer | 评审通过的最少人数，仅普通模式生效。 | 1 |
| mrMode | string | 评审模式：general - 普通模式, codeowner - CodeOwner 模式。 | general |
| whiteList | string | 评审文件白名单；输入文件路径，多行以换行符隔开，通配符请使用英文格式。 | \*.java |
| testSetting | object |  |  |
| checkCheckRunConfig | object | 运行检查。 |  |
| checkRunCheckItems | array | 配置项列表。 |  |
| \- | object |  |  |
| id | string | 写入人的 ID。 | 62c795xxxb468af8 |
| name | string | check run 的名称。 | default-test-check-run-name |
| required | boolean | 是否作为卡点。 | true |
| type | string | 写入人类型：User。 | User |
| checkCommitStatusConfig | object | 提交状态。 |  |
| commitStatusCheckItems | array | 配置项列表。 |  |
| \- | object |  |  |
| context | string | 三方提交状态的名称（以名称作为卡点的匹配项）。 | default-context |
| required | boolean | 是否作为卡点。 | true |
| checkConfig | object | 流水线检查。 |  |
| checkItems | array | 配置项列表。 |  |
| \- | object |  |  |
| isRequired | boolean | 是否是卡点项。 | true |
| pipelineId | integer | 流水线 ID。 | 1880578 |
| pipelineName | string | 流水线名称。 | codeup-demo 测试代码检测 |
| checkTaskQualityConfig | object | 代码检测任务。 |  |
| bizNo | string | 检测任务流水线号。 | 202207192301340000110700070550024 |
| enabled | boolean | 是否开启。 | true |
| message | string | 描述信息。 | 测试代码检测 |
| taskName | string | 检测任务名称。 | codeup-demo 代码检测 |
| isRequired | boolean | 是否开启。 | true |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |

## **返回示例**

`{ "allowMergeRoles": [40, 30], "allowMergeUserIds": ["62c795xxxb468af8"], "allowMergeUsers": [ { "avatarUrl": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-demo", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "allowPushRoles": [40, 30], "allowPushUserIds": ["62c795xxxb468af8"], "allowPushUsers": [ { "avatarUrl": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-demo", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "branch": "master", "createdAt": "2024-10-05T15:30:45Z", "id": 1, "matches": ["master"], "mergeRequestSetting": { "allowMergeRequestRoles": [40, 30], "defaultAssignees": [ { "avatarUrl": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-demo", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "isAllowSelfApproval": false, "isAllowSourceBranchPushUserApproval": false, "isRequireDiscussionProcessed": true, "isRequired": true, "isResetApprovalWhenNewPush": true, "minimumApproval": 1, "mrMode": "general", "whiteList": "*.java" }, "testSetting": { "checkCheckRunConfig": { "checkRunCheckItems": [ { "id": "62c795xxxb468af8", "name": "default-test-check-run-name", "required": true, "type": "User" } ] }, "checkCommitStatusConfig": { "commitStatusCheckItems": [ { "context": "default-context", "required": true } ] }, "checkConfig": { "checkItems": [ { "isRequired": true, "pipelineId": 1880578, "pipelineName": "codeup-demo测试代码检测" } ] }, "checkTaskQualityConfig": { "bizNo": "202207192301340000110700070550024", "enabled": true, "message": "测试代码检测", "taskName": "codeup-demo代码检测" }, "isRequired": true }, "updatedAt": "2024-10-05T15:30:45Z" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。