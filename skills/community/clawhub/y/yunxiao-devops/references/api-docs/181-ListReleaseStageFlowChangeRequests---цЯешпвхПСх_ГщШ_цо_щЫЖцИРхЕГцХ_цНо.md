# ListReleaseStageFlowChangeRequests - 查询发布阶段集成元数据

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 研发阶段 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}:find_release_integrated_metadata`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63xxxxx334d6exe671 |
| appName | string | path | 是 | 应用名。 | my-app |
| releaseWorkflowSn | string | path | 是 | 发布流程唯一序列号。 | 3f472a1xxxxxx6227bb85f787c |
| releaseStageSn | string | path | 是 | 发布流程阶段唯一序列号。 | 6b4c53eexxxxxxxxxx35b29d002a81 |
| buildNum | integer | query | 否 | 运行次数，可为空，为空则查询最新的一次。 | 5 |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63xxxxx334d6exe671/apps/my-app/releaseWorkflows/3f472a1xxxxxx6227bb85f787c/releaseStages/6b4c53eexxxxxxxxxx35b29d002a81:find_release_integrated_metadata?buildNum=5' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 发布阶段集成元数据。 |  |
| crDetailList | array | 变更详情列表。 |  |
| \- | object | 变更详情。 |  |
| branchName | string | 分支名称。 | feature/20251107\_saassa |
| branchState | string | 分支状态，可能的值：\[DELETED NEW\_COMMIT UNKNOWN LATEST\]。 | LATEST |
| commitId | string | 对应的 commitId。 | xxxxxxxxxxxx |
| name | string | 变更的名称。 | aaa |
| ownerId | string | 变更负责人。 | xxxxxxxxxx |
| sn | string | 变更的 sn。 | xxxxxxxxxxxxxx |
| state | string | 集成状态，可能的值：\[INTEGRATING RELEASED CLOSED DEVELOPING\]。 | INTEGRATING |
| releaseBranch | string | 发布分支。 | release/20251204-xxxxxxxxxxx\_release\_4566642\_5 |
| releaseRevision | string | 发布的 Revision。 | xxxxxxxxxxxx |
| releaseStageSn | string | 研发流程阶段 sn。 | xxxxxxxxxxxxxxx |
| repoType | string | 代码库类型。 | CODEUP |
| repoUrl | string | 代码库 url。 | https://codeup.aliyun.com/xxxxxxxxxxxxxxx/Codeup-Demo.git |
| runNumber | integer | 运行次数。 | 5 |

## **返回示例**

`{ "crDetailList": [ { "branchName": "feature/20251107_saassa", "branchState": "LATEST", "commitId": "64cb648xxxxxxxxx5c54934e148ef", "name": "aaa", "ownerId": "5e9exxxxx8c7c8906", "sn": "9dfe68c8xxxxxxxx863c4f16872fe", "state": "INTEGRATING" } ], "releaseBranch": "release/20251204-094700635356876_release_4566642_5", "releaseRevision": "a124d55cxxxxxxxxxx1646ab142e08d", "releaseStageSn": "f469b665xxxxxxxxxxcff2d12887", "repoType": "CODEUP", "repoUrl": "https://codeup.aliyun.com/xxxxxxxxc/Codeup-Demo.git", "runNumber": 5 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。