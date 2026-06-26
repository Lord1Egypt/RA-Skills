# ExecuteChangeRequestReleaseStage - 执行研发阶段流水线

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 研发阶段 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}:execute`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| releaseWorkflowSn | string | path | 是 | 发布流程唯一序列号。 | xxxxxxxx |
| releaseStageSn | string | path | 是 | 发布流程阶段唯一序列号。 | xxxxxxxxxxxx |
| organizationId | string | path | 是 | 组织 ID。 | xxxxxxxxxxxxx |
| \- | object | body | 否 | 执行流水线请求。 |  |
| params | object | body | 否 | 运行流水线参数（支持使用代码库指定分支触发运行，格式： "sourceId": "分支" ）。支持使用变更运行研发阶段,参考示例值中的releaseBranchRepoInfo。 | { "params": { "FLOW\_INST\_RUNNING\_COMMENT": "运行备注1",# 运行备注 "k1": "v1", # 运行参数 "${sourceId}":"branch", # 运行分支，非使用变更时生效 "releaseBranchRepoInfo": { # 运行的变更信息，可调用ListAppChangeRequests 获取具体的数据 "featureBranchs": \[ { "branchName": "feature/20251216\_1", # 变更的分支名称 "changeRequestSn": "25500xxxxxxaaf9855" # 变更的sn } \], "repo": "[https://codeup.aliyun.com/xxxxxx/codeDemo.git](https://codeup.aliyun.com/xxxxxx/codeDemo.git)", # 代码库地址 "baseBranch": { # 基础分支，会基于此分支生成release分支 "branchName": "master" }, "needCreateBranch": false, # 是否需要生成release分支，为false 时，使用 releaseBranch 对应的值作为release 分支 "releaseBranch": { "branchName": "release/xxxxx\_release\_4468686\_2" # release分支 } } }} |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/releaseWorkflows/xxxxxxxxxxxxxx/releaseStages/xxxxxxxxxxxxxxx:execute' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "params": { "FLOW_INST_RUNNING_COMMENT": "运行备注1", "k1": "v1", "${sourceId}":"branch", "releaseBranchRepoInfo": { "featureBranchs": [ { "branchName": "feature/20251216_1", "changeRequestSn": "25500xxxxxxaaf9855" } ], "repo": "https://codeup.aliyun.com/xxxxxx/codeDemo.git", "baseBranch": { "branchName": "master" }, "needCreateBranch": false, "releaseBranch": { "branchName": "release/xxxxx_release_4468686_2" } } } }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 执行流水线阶段结果。 |  |
| object | number | 流水线对象。 | 1 |

## **返回示例**

`{ "object": 1 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。