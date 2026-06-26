# CreatePipeline - 创建流水线

通过 OpenAPI 创建流水线。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines`

### **Region版**

```
POST https://{domain}/oapi/v1/flow/pipelines
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| content | string | body | 是 | 流水线 yaml 描述，可参考 YAML 流水线的帮助文档编写。 | stages:   command\_stage:   name: "执行命令"   jobs:   command\_job:   name: "执行命令"   runsOn:   group: public/cn-beijing   container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest   steps:   command\_step:   name: "执行命令"   step: "Command"   with:   run: "echo hello world" |
| name | string | body | 是 | 流水线名称,最大支持60个字符。 | 测试流水线 |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "content": "stages: command_stage: name: "执行命令" jobs: command_job: name: "执行命令" runsOn: group: public/cn-beijing container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest steps: command_step: name: "执行命令" step: "Command" with: run: "echo hello world"", "name": "测试流水线" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/flow/pipelines' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "content": "stages:
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
              run: "echo hello world"",
        "name": "测试流水线"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | integer | 流水线 id。 | 1 |

## **返回示例**

`1`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。