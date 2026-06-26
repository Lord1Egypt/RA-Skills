# UpdateReleaseStageFlow - 更新发布阶段 YAML 配置

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 研发流程 | 读写 |

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}/yaml`

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
| \- | object | body | 否 | 更新发布阶段流程配置请求。 |  |
| flow | string | body | 是 | 流程配置,只支持更新 yaml 形式 的流程配置。 | `stages: stage_0: name: 执行命令 jobs: job_0: name: 执行命令 runsOn: group: public/cn-beijing labels: linux,amd64 container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest steps: step_0: name: 执行命令 step: Command with: ifGivenShell: false run: \| # input your command here echo hello,world! driven: auto plugins: []` |

## **请求示例**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/appstack/organizations/ec766e63xxxxx334d6exe671/apps/my-app/releaseWorkflows/3f472a1xxxxxx6227bb85f787c/releaseStages/6b4c53eexxxxxxxxxx35b29d002a81/yaml' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "flow": "stages:
  command_stage:
    name: "执行命令"
    jobs:
      command_job:
        name: "执行命令"
        runsOn:
          group: public/cn-beijing
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
        steps:
          command_step:
            name: "执行命令"
            step: "Command"
            with:
              run: "echo hello world\n"
"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean |  | true |

## **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。