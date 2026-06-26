# ListServiceConnections - 获取服务连接列表

通过 OpenAPI 获取服务连接列表。

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 服务连接 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/serviceConnections`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| sericeConnectionType | string | query | 是 | 服务连接类型: aliyun\_code 阿里云代码; Codeup Codeup; Gitee 码云; github Github; ack 容器服务 Kubernetes（ACK）; docker\_register\_aliyun 容器镜像服务（ACR）; ecs ecs 主机; edas 企业级分布式应用（EDAS）; emas 移动研发平台（EMAS）; fc 阿里云函数计算（FC）; kubernetes 自建 k8s 集群; oss 对象存储（OSS）; PACKAGES 制品仓库; ros 资源编排服务（ROS）; sae Serverless 应用引擎（SAE）。 | codeup |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/serviceConnections?sericeConnectionType=codeup' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| createTime | integer | 创建时间。 | 1586863220000 |
| id | integer | 服务连接 Id。 | 123 |
| name | string | 服务连接名称。 | 张三的 oss 服务连接 |
| ownerAccountId | integer | 拥有者阿里云账号 id。 | 1212123212121212 |
| type | string | 服务连接类型。 | oss |
| uuid | string | uuid。 |  |

## **返回示例**

`[ { "createTime": 1586863220000, "id": 123, "name": "张三的oss服务连接", "ownerAccountId": 1212123212121212, "type": "oss", "uuid": "" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。