# CreatePipelineRun - 运行流水线

通过 OpenAPI 运行流水线。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线运行实例 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/runs`

### **Region版**

```
POST https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/runs
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | path | 是 | 流水线 Id。 | 123 |
| \- | object | body | 否 |  |  |
| params | string | body | 否 | 运行流水线参数,json 格式的字符串,流水线运行参数 branchModeBranchs:分支模式运行分支, envs 运行变量, runningBranchs 运行分支 key 为仓库地址, runningTags 运行 tag key 为仓库地址。 | { "branchModeBranchs": \["branch1", "branch2"\], "envs": { "k1": "v1", "k2": "v2", "k3": "v3" }, "runningBranchs": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "master1" }, "runningTags": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "1.0" }, "runningPipelineArtifacts": { "3184679": "12" }, "runningAcrArtifacts": { "yunxiao-registry.cn-beijing.cr.aliyuncs.com/build-steps/tool-registry": "89b20155-2024-05-14-21-52-44" }, "runningPackagesArtifacts": { "generic/flow\_generic\_repo/Artifacts\_3183732": "2024-06-04-17-58-34" }, "comment":"222" } |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/runs' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "params": "{ "branchModeBranchs": ["branch1", "branch2"], "envs": { "k1": "v1", "k2": "v2", "k3": "v3" }, "runningBranchs": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "master1" }, "runningTags": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "1.0" }, "runningPipelineArtifacts": { "3184679": "12" }, "runningAcrArtifacts": { "yunxiao-registry.cn-beijing.cr.aliyuncs.com/build-steps/tool-registry": "89b20155-2024-05-14-21-52-44" }, "runningPackagesArtifacts": { "generic/flow_generic_repo/Artifacts_3183732": "2024-06-04-17-58-34" }, "comment":"222" }" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/flow/pipelines/123/runs' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "params": "{ "branchModeBranchs": ["branch1", "branch2"], "envs": { "k1": "v1", "k2": "v2", "k3": "v3" }, "runningBranchs": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "master1" }, "runningTags": { "https://codeup.aliyun.com/60c1abb32c5969c370c5fcd0/Codeup-Demo.git": "1.0" }, "runningPipelineArtifacts": { "3184679": "12" }, "runningAcrArtifacts": { "yunxiao-registry.cn-beijing.cr.aliyuncs.com/build-steps/tool-registry": "89b20155-2024-05-14-21-52-44" }, "runningPackagesArtifacts": { "generic/flow_generic_repo/Artifacts_3183732": "2024-06-04-17-58-34" }, "comment":"222" }"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | integer | 流水线运行 id，也既流水线的运行次数。 | 1 |

## **返回示例**

`1`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。