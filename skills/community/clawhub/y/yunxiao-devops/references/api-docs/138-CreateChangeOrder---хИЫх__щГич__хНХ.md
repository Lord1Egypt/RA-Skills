# CreateChangeOrder - 创建部署单

通过 OpenAPI 创建部署单。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 部署单 | 读写 |
    

### 请求语法

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeOrders`

### 请求头

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

### 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |
| \- | object | body | 否 | 创建部署单请求。 |  |
| changeOrderName | string | body | 是 | 部署单名称。 | 20240201161127-部署 |
| deploymentChangedCheck | boolean | body | 否 | 当本次发布会增加或者删除 Deployment 时，是否阻断本次发布，默认值为 true。 | true |
| description | string | body | 否 | 描述。 | 这是一段描述信息 |
| envs | map | body | 是 | 环境信息：用于指定要部署的环境，以及该环境的相关配置，Map的key为环境名，Map的value为相关配置（可参考示例）。（当前仅支持单环境部署） | 示例1（部署）：部署test环境，并且使用指定的自定义参数部署 { "test": { "values": { "image.backend": "nginx", "namespace": "default", "cpuLimit": "1", "memoryLimit": "1024Mi", "cpuRequest": "0.01", "memoryRequest": "32Mi" } } } 字段含义： values - 部署单类型为Deploy时使用，用于指定部署使用的变量信息，例如镜像image.backend，namespace等，使用kv方式传入 示例2（滚动扩缩容）：扩缩容test环境，并针对 myapp-dev/default/apps/v1/Deployment资源通过滚动升级的方式调整到3副本； { "test": { "deploymentScaleStrategies": \[{ "locator": "myapp-dev/default/apps/v1/Deployment", "deployType": "Rolling", "targetReplicas": 3, "timeOutMS": 600000 }\] } } 字段含义： deploymentScaleStrategies - 工作负载扩缩策略 locator（必填） - k8s资源定位器，用于指定要扩缩的资源，格式：{metadata.name}/{metadata.namespace}/{group}/{version}/{kind} deployType（必填） - 部署类型：Rolling-滚动升级，Batch-分批发布 targetReplicas（必填） - 目标副本数 timeOutMS（可选） - 每批Pod最长发布时间，单位为毫秒，默认600000ms，即10分钟 示例3（分批扩缩容）：扩缩容test环境，并针对 myapp-dev/default/apps/v1/Deployment资源通过分批发布的方式调整到3副本； { "test": { "deploymentScaleStrategies": \[{ "locator": "myapp-dev/default/apps/v1/Deployment", "deployType": "Batch", "targetReplicas": 3, "timeOutMS": 600000, "batches": 2, "batchSteps": \[1,2\], "batchMode": "Auto" }\] } } 字段含义： deploymentScaleStrategies - 工作负载扩缩策略 locator（必填） - k8s资源定位器，用于指定要扩缩的资源，格式：{metadata.name}/{metadata.namespace}/{group}/{version}/{kind} deployType（必填） - 部署类型：Rolling-滚动升级，Batch-分批发布 targetReplicas（必填） - 目标副本数 timeOutMS（可选） - 每批Pod最长发布时间，单位为毫秒，默认600000ms，即10分钟 batches（必填） - 分批发布时，指定分批数量，默认1 batchSteps（必填） - 分批发布时，指定每批数量，\[1,2\] 表示第一批1个，第二批2个； batchMode（必填） - 分批发布时，指定暂停策略：ConfirmFirstBatch-首批暂停，Auto-不暂停，Manual-每批暂停，默认Auto 示例4（清理环境资源）：清理test环境资源，并删除环境 { "test": { "deleteEnvAfterDeleteResource": true } } 字段含义： deleteEnvAfterDeleteResource（必填） - 部署单类型为Destroy时选填，用于指定删除资源后是否删除环境，默认删除环境 |
| orchestrationRevisionSha | string | body | 否 | 编排版本 sha 值，部署单类型为 Deploy 时必填。 | 94c50c64ccf2e966f1b37ef422db8136772039bc |
| rollbackChangeOrderVersion | string | body | 否 | 部署单类型为 Rollback 时必填，指定回滚时使用的部署版本号。 | 20241120175852-177 |
| type | string | body | 是 | 部署单类型：Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-删除资源。 | Deploy |

### 请求示例

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/changeOrders' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "changeOrderName": "20240201161127-部署", "deploymentChangedCheck": true, "description": "这是一段描述信息", "envs": {"test":{} }, "orchestrationRevisionSha": "94c50c64ccf2e966f1b37ef422db8136772039bc", "rollbackChangeOrderVersion": "20241120175852-177", "type": "Deploy" }'`

### 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| creator | string | 创建人。 | 10df6011-2837-4fdb-ad92-356a679a60ca |
| description | string | 描述。 | 正常发布日常需求 |
| endedAt | string | 部署单结束时间。 | 2024-10-08T09:11:38Z |
| gmtCreate | string | 部署单最后修改时间。 | 2024-10-08T09:11:38Z |
| jobs | array | 环境部署单列表。 |  |
| \- | object | 部署单任务列表。 |  |
| appOrchestration | object | 应用内置编排。 |  |
| app | object | 应用。 |  |
| creatorId | string | 应用创建者。 | 10df6011-2837-4fdb-ad92-356a679a60ca |
| description | string | 应用描述。 | for java |
| favoured | boolean | 是否收藏。 | false |
| gmtCreate | string | 应用创建时间。 | 2024-09-01 00:00:00 |
| labelList | array | 应用标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| name | string | 应用名称。 | my-web-app |
| type | string | 类型，可能的值：\[APP SYSTEM\]。 | APP |
| componentList | array | 组件列表。 |  |
| \- | object | 编排组件模型。 |  |
| content | string | 组件内容，以 go 标准库 text/template 的形式呈现。 | —\\napiVersion: v1\\nkind: Service\\nmetadata:\\n name: prod-sidecar-test-{{ .AppStack.envName }}\\n # 命名空间配置：\\n # 建议每个环境使用不同的 Kubernetes 集群命名空间，以便达到环境隔离效果\\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\\n namespace: {{ .Values.namespace }}\\nspec:\\n selector:\\n run: prod-sidecar-test-{{ .AppStack.envName }}\\n ports:\\n - protocol: TCP\\n port: 80\\n targetPort: 8080 |
| description | string | 组件描述。 | 示例描述 |
| kind | string | 组件类型（在 kubernetes 场景下，需要沿用 kubernetes 对象的 kind）。 | Service |
| name | string | 组件名。 | demo-service |
| priority | integer | 组件优先级，从 1 开始；环境部署时，会按优先级数值从低到高的顺序下发部署。 | 1 |
| type | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| creatorId | string | 创建人。 | app-builtin-creator-id |
| description | string | 描述。 | app-builtin-orchestration-description |
| format | string | 格式。 | MANIFEST |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| gmtModified | string | 修改时间。 | 2024-09-01 00:00:00 |
| groupNameMap | object |  |  |
| labelList | array | 标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| labelPolicy | string | 标签策略。 | NONE |
| modifierId | string | 修改人。 | app-builtin-modifier-id |
| name | string | 名称。 | app-builtin-orchestration-name |
| placeholderList | array | 占位符列表。 |  |
| \- | object | 占位符模型。 |  |
| description | string | 占位符描述。 | 内存限制 |
| name | string | 占位符名。 | memoryLimit |
| overridable | boolean | 占位符是否部署时可修改。 | true |
| predefined | boolean | 是否预置占位符。 | false |
| rsType | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| rule | string | 占位符取值的可选校验规则。 |  |
| type | string | 占位符类型，可能的值：\[string number boolean float object\]。 | string |
| value | string | 占位符取值。 | 1024Mi |
| valueSource | string | 占位符取值的数据源类型（如常量、变量等），可能的值：\[CONSTANT VARIABLE NULL\]。 | CONSTANT |
| revision | object | 编排版本信息。 |  |
| author | string | 编排版本提交人。 | 10df6011-2837-4fdb-ad92-356a679a60ca |
| commitTime | string | 编排版本提交时间。 | 2024-09-01 00:00:00 |
| message | string | 编排版本信息 commit 信息。 | 3t7cb880d20614038740e00e819dcdb13a37ce31 |
| sha | string | 编排版本信息 commit sha 值。 | c229f22024535638af41838daa43af1e6d468116 |
| sn | string | 唯一序列号。 | app-builtin-orchestration-1 |
| storageType | string | 存储类型。 | BUILTIN |
| suitableResourceTypes | array\[string\] | 使用资源类型。 |  |
| syncSourceTemplate | object | 编排同步源模板。 |  |
| appTemplateName | string | 应用模板名称。 | app-template-name |
| orchestrationSha | string | 应用模板版本 commit sha 值。 | app-template-version-sha |
| type | string | 类型。 | AppBuiltInOrchestration |
| endedAt | string | 部署单结束时间。 | 2024-10-08T09:11:38Z |
| envName | string | 环境名称。 | test |
| sn | string | 环境部署单编号。 | 40bfa492838047ce91870f52f6017ca6 |
| stages | array | 阶段列表。 |  |
| \- | object | 阶段列表。 |  |
| endedAt | string | 部署单阶段结束时间。 | 2024-10-08T09:11:38Z |
| sn | string | 部署单阶段唯一标识。 | 37bfa492838047ce91870f52f6017cb8 |
| startedAt | string | 部署单阶段开始时间。 | 2024-10-08T09:11:38Z |
| state | string | 部署单阶段状态，可能的值：\[INIT PREPARING RUNNING STOPPING SUSPENDING SUSPENDED SUCCESS FAILED CANCELED\]。 | 状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功 |
| tasks | array | 部署单节点任务列表。 |  |
| \- | object | 部署单节点任务列表。 |  |
| behavior | string | 任务行为:Upsert-会对该对象进行更新，Delete-会对该对象进行删除。 | Upsert |
| endedAt | string | 节点任务结束时间。 | 2024-10-08T09:11:38Z |
| errorMessage | string | 错误信息。 | error-message |
| sn | string | 节点任务唯一标识。 | 27bfa492838047ce91870f52f6017dj3 |
| spec | string | 部署任务编排 yaml。 | —\\napiVersion: “v1”\\nkind: “Service”\\nmetadata:\\n name: “app-test”\\n namespace: “ns-aaa”\\n labels:\\n devops.aliyun.com/app-name: “app-test”\\n devops.aliyun.com/version: “20241202120555-308”\\n devops.aliyun.com/org-id: “aaa-bbb-ccc”\\n devops.aliyun.com/env-name: “test”\\nspec:\\n selector:\\n run: “app-test”\\n ports:\\n - name: “http-8080”\\n protocol: “TCP”\\n port: 8080\\n targetPort: 8080 |
| startedAt | string | 节点任务开始时间。 | 2024-10-08T09:11:38Z |
| state | string | 节点任务状态。 | 状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功 |
| startedAt | string | 部署单开始时间。 | 2024-10-08T09:11:38Z |
| state | string | 部署单状态，可能的值：\[INIT PREPARING RUNNING STOPPING SUSPENDING SUSPENDED SUCCESS FAILED CANCELED\]。 | 状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功 |
| type | string | 部署单类型。 | 操作类型:Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-销毁,Revert-回退 |
| variableGroups | array | 变量组。 |  |
| \- | object | 变量组。 |  |
| name | string | 变量组名称。 | test |
| revisionSha | string | 变量组版本。 | my-revision-sha |
| type | string | 变量组类型，可能的值：\[GLOBAL TEMPLATE APP\]。 | 类型：GLOBAL-全局,TEMPLATE-模板，APP-应用 |
| name | string | 部署单名称。 | 20241008171130-部署 |
| sn | string | 部署单唯一标识。 | bc62b3e953714aa8be431f47b9c9b72a |
| startedAt | string | 部署单开始时间。 | 2024-10-08T09:11:38Z |
| state | string | 部署单状态，可能的值：\[INIT PREPARING RUNNING SUSPENDED CANCELED SUCCESS FAILED\]。 | 操作类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功 |
| type | string | 部署单类型，可能的值：\[Deploy Scale Rollback Destroy\]。 | 操作类型:Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-销毁 |
| version | string | 使用版本。 | 20241008171130-762 |

### 返回示例

`{ "creator": "10df6011-2837-4fdb-ad92-356a679a60ca", "description": "正常发布日常需求", "endedAt": "2024-10-08T09:11:38Z", "gmtCreate": "2024-10-08T09:11:38Z", "jobs": [ { "appOrchestration": { "app": { "creatorId": "10df6011-2837-4fdb-ad92-356a679a60ca", "description": "for java", "favoured": false, "gmtCreate": "2024-09-01 00:00:00", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "name": "my-web-app", "type": "APP" }, "componentList": [ { "content": "---\napiVersion: v1\nkind: Service\nmetadata:\n name: prod-sidecar-test-{{ .AppStack.envName }}\n # 命名空间配置：\n # 建议每个环境使用不同的Kubernetes集群命名空间，以便达到环境隔离效果\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\n namespace: {{ .Values.namespace }}\nspec:\n selector:\n run: prod-sidecar-test-{{ .AppStack.envName }}\n ports:\n - protocol: TCP\n port: 80\n targetPort: 8080", "description": "示例描述", "kind": "Service", "name": "demo-service", "priority": 1, "type": "KUBERNETES" } ], "creatorId": "app-builtin-creator-id", "description": "app-builtin-orchestration-description", "format": "MANIFEST", "gmtCreate": "2024-09-01 00:00:00", "gmtModified": "2024-09-01 00:00:00", "groupNameMap": { }, "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "labelPolicy": "NONE", "modifierId": "app-builtin-modifier-id", "name": "app-builtin-orchestration-name", "placeholderList": [ { "description": "内存限制", "name": "memoryLimit", "overridable": true, "predefined": false, "rsType": "KUBERNETES", "rule": "", "type": "string", "value": "1024Mi", "valueSource": "CONSTANT" } ], "revision": { "author": "10df6011-2837-4fdb-ad92-356a679a60ca", "commitTime": "2024-09-01 00:00:00", "message": "3t7cb880d20614038740e00e819dcdb13a37ce31", "sha": "c229f22024535638af41838daa43af1e6d468116" }, "sn": "app-builtin-orchestration-1", "storageType": "BUILTIN", "suitableResourceTypes": [ ], "syncSourceTemplate": { "appTemplateName": "app-template-name", "orchestrationSha": "app-template-version-sha" }, "type": "AppBuiltInOrchestration" } "endedAt": "2024-10-08T09:11:38Z", "envName": "test", "sn": "40bfa492838047ce91870f52f6017ca6", "stages": [ { "endedAt": "2024-10-08T09:11:38Z", "sn": "37bfa492838047ce91870f52f6017cb8", "startedAt": "2024-10-08T09:11:38Z", "state": "状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功", "tasks": [ { "behavior": "Upsert", "endedAt": "2024-10-08T09:11:38Z", "errorMessage": "error-message", "sn": "27bfa492838047ce91870f52f6017dj3", "spec": "--- apiVersion: "v1" kind: "Service" metadata: name: "app-test" namespace: "ns-aaa" labels: devops.aliyun.com/app-name: "app-test" devops.aliyun.com/version: "20241202120555-308" devops.aliyun.com/org-id: "aaa-bbb-ccc" devops.aliyun.com/env-name: "test" spec: selector: run: "app-test" ports: - name: "http-8080" protocol: "TCP" port: 8080 targetPort: 8080", "startedAt": "2024-10-08T09:11:38Z", "state": "状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功" } ] } ], "startedAt": "2024-10-08T09:11:38Z", "state": "状态类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功", "type": "操作类型:Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-销毁,Revert-回退", "variableGroups": [ { "name": "test", "revisionSha": "my-revision-sha", "type": "类型：GLOBAL-全局,TEMPLATE-模板，APP-应用" } ] } ], "name": "20241008171130-部署", "sn": "bc62b3e953714aa8be431f47b9c9b72a", "startedAt": "2024-10-08T09:11:38Z", "state": "操作类型:RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功", "type": "操作类型:Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-销毁", "version": "20241008171130-762" }`

### 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。