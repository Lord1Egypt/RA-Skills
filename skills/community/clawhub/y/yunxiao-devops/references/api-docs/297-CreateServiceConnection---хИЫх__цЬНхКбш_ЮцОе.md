# CreateServiceConnection - 创建服务连接

通过 OpenAPI 创建服务连接。

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 服务连接 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/flow/organizations/{organizationId}/createServiceConnection`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| authId | integer | body | 否 | 服务授权 id。 | 111 |
| authType | string | body | 否 | 服务授权类型。 | CREDENTIAL （服务证书）; AUTHENTICATION （服务授权） |
| connectionName | string | body | 否 | 服务连接名称。 | ecs 连接 |
| connectionType | string | body | 否 | 服务连接类型。 | ecs 云服务器(ECS); ack 容器服务 Kubernetes(ACK); oss 对象存储(OSS); edas 企业级分布式应用(EDAS); sae Serverless 应用引擎(SAE); ros 资源编排服务(ROS); fc 阿里云函数计算(FC); emas 移动研发平台(EMAS); customGitlab 自建 Gitlab; git 通用 Git; gitlab Gitlab; bitbucket Bitbucket; docker\_register\_aliyun 容器镜像服务(ACR); ess 弹性伸缩(ESS); Codeup |
| scope | string | body | 否 | 可见范围：如 PERSON，GLOBAL，CUSTOM。 | PERSON （私有）; GLOBAL （公开）; CUSTOM （自定义） |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/createServiceConnection' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "authId": 111, "authType": "CREDENTIAL （服务证书）; AUTHENTICATION （服务授权）", "connectionName": "ecs连接", "connectionType": "ecs 云服务器(ECS); ack 容器服务Kubernetes(ACK); oss 对象存储(OSS); edas 企业级分布式应用(EDAS); sae Serverless应用引擎(SAE); ros 资源编排服务(ROS); fc 阿里云函数计算(FC); emas 移动研发平台(EMAS); customGitlab 自建Gitlab; git 通用Git; gitlab Gitlab; bitbucket Bitbucket; docker_register_aliyun 容器镜像服务(ACR); ess 弹性伸缩(ESS); Codeup", "scope": "PERSON （私有）; GLOBAL （公开）; CUSTOM （自定义）" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | integer | 服务连接 id。 | 19224 |

## **返回示例**

`19224`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。