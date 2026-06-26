# UpdateReleaseStage - 更新研发阶段

通过 OpenAPI 更新研发阶段。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 研发阶段 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| releaseWorkflowSn | string | path | 是 | 发布流程唯一序列号。 | app-release-sn-xxx |
| releaseStageSn | string | path | 是 | 发布流程阶段唯一序列号。 | app-release-stage-sn-xxx |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |
| \- | object | body | 否 | 创建发布阶段请求。 |  |
| commitMessage | string | body | 否 | 版本 commit 信息。 | message-xxxxx |
| labelList | array | body | 是 | 标签列表。 |  |
| \- | object | body | 否 | AppStack 标签。 |  |
| displayName | string | body | 否 | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | body | 否 | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | body | 否 | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | body | 否 | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | body | 否 | 标签命名空间，决定了标签的作用域。 | default |
| value | string | body | 否 | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| name | string | body | 是 | 名称。 | stage-name |
| order | string | body | 否 | 排序。 | 1 |
| variableGroups | array | body | 是 | 变量组列表。 |  |
| \- | object | body | 否 | 通用变量组模型。 |  |
| displayName | string | body | 否 | 变量组显示名。 | 开发变量组 |
| name | string | body | 否 | 变量组标识。 | dev |
| type | string | body | 否 | 变量组类型。 | GLOBAL |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-web-service/releaseWorkflows/app-release-sn-xxx/releaseStages/app-release-stage-sn-xxx' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "commitMessage": "message-xxxxx", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "name": "stage-name", "order": "1", "variableGroups": [ { "displayName": "开发变量组", "name": "dev", "type": "GLOBAL" } ] }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 流程阶段。 |  |
| appName | string | 应用名。 | app-name-xxxx |
| labels | array | 标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| name | string | 名称。 | name-xxxx |
| order | string | 阶段顺序。 | 1 |
| pipeline |   |  |  |
| \- OneOf | object | 流水线 V1版本。 |  |
| engineSn | string | Flow流水线标识符 | 321 |
| engineType | string | 可能的值：\[FlowV1 FlowV2 FlowAny\]。 | FlowV2 |
| pipeline | object |  |  |
| pipelineYaml | string | 流水线YAML内容 | {"name":"my-flow-name","owner":"31a62065395ee4198d5516a8","pipelineConfigVo":{"triggerVoList":\[{"type":"MANUAL"}\],"settings":"{\\\\"executeScope\\\\":\\\\"\\\\",\\\\"caches\\\\":\[{\\\\"directory\\\\":\\\\"/root/.m2\\\\",\\\\"desc\\\\":\\\\"maven依赖缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.gradle/caches\\\\",\\\\"desc\\\\":\\\\"gradle依赖缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.npm\\\\",\\\\"desc\\\\":\\\\"npm依赖全局缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.yarn\\\\",\\\\"desc\\\\":\\\\"yarn依赖全局缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/go/pkg/mod\\\\",\\\\"desc\\\\":\\\\"go mod缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.cache\\\\",\\\\"desc\\\\":\\\\"其它缓存\\\\",\\\\"disable\\\\":false}\]}","flow":"schema: tb\\\\npipeline:\\\\n - name: 阶段1\\\\n stages:\\\\n - driven: AUTO\\\\n jobs:\\\\n - displayName: 空任务\\\\n task: execution-component@66\\\\n identifier: \\'10\_1726646111967\\'\\\\n templateType: task\\\\n templateSign: \\'\\'\\\\n templateBatchUpdate: \\'N\\'\\\\n extraInfo: \\'\\'\\\\n params:\\\\n ENGINE\_PIPELINE\_NAME: \\'${INPUTS.ENGINE\_PIPELINE\_NAME}\\'\\\\n ENGINE\_PIPELINE\_ID: \\'${INPUTS.ENGINE\_PIPELINE\_ID}\\'\\\\n ENGINE\_PIPELINE\_INST\_ID: \\'${INPUTS.ENGINE\_PIPELINE\_INST\_ID}\\'\\\\n ENGINE\_PIPELINE\_INST\_NUMBER: \\'${INPUTS.ENGINE\_PIPELINE\_INST\_NUMBER}\\'\\\\n buildNodeGroup: K8S-4\\\\n capabilities: \\'Linux,amd64\\'\\\\n buildEnvironment: container\\\\n specifyContainerImageId: >-\\\\n build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest\\\\n clone\_option: all\\\\n selected\_sources: \\'\\'\\\\n steps: \[\]\\\\n plugins: \[\]\\\\n output: \[\]\\\\n freeInTaskGroupModeFields: \[\]\\\\n","sources":"\[\]","webhook":"e0aO78pcq8n5XaFe81b1"},"originPipelineId":1} |
| plugins | object | 插件列表。 | \[\] |
| refObjectList | object | 插件列表。 | \[\] |
| \- OneOf | object | 流水线 V2版本。 |  |
| engineSn | string | Flow流水线标识符 | 321 |
| engineType | string | 可能的值：\[FlowV1 FlowV2 FlowAny\]。 | FlowV2 |
| pipeline | object |  |  |
| pipelineYaml | string | 流水线YAML内容 | {"name":"my-flow-name","owner":"31a62065395ee4198d5516a8","pipelineConfigVo":{"triggerVoList":\[{"type":"MANUAL"}\],"settings":"{\\\\"executeScope\\\\":\\\\"\\\\",\\\\"caches\\\\":\[{\\\\"directory\\\\":\\\\"/root/.m2\\\\",\\\\"desc\\\\":\\\\"maven依赖缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.gradle/caches\\\\",\\\\"desc\\\\":\\\\"gradle依赖缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.npm\\\\",\\\\"desc\\\\":\\\\"npm依赖全局缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.yarn\\\\",\\\\"desc\\\\":\\\\"yarn依赖全局缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/go/pkg/mod\\\\",\\\\"desc\\\\":\\\\"go mod缓存\\\\",\\\\"disable\\\\":false},{\\\\"directory\\\\":\\\\"/root/.cache\\\\",\\\\"desc\\\\":\\\\"其它缓存\\\\",\\\\"disable\\\\":false}\]}","flow":"schema: tb\\\\npipeline:\\\\n - name: 阶段1\\\\n stages:\\\\n - driven: AUTO\\\\n jobs:\\\\n - displayName: 空任务\\\\n task: execution-component@66\\\\n identifier: \\'10\_1726646111967\\'\\\\n templateType: task\\\\n templateSign: \\'\\'\\\\n templateBatchUpdate: \\'N\\'\\\\n extraInfo: \\'\\'\\\\n params:\\\\n ENGINE\_PIPELINE\_NAME: \\'${INPUTS.ENGINE\_PIPELINE\_NAME}\\'\\\\n ENGINE\_PIPELINE\_ID: \\'${INPUTS.ENGINE\_PIPELINE\_ID}\\'\\\\n ENGINE\_PIPELINE\_INST\_ID: \\'${INPUTS.ENGINE\_PIPELINE\_INST\_ID}\\'\\\\n ENGINE\_PIPELINE\_INST\_NUMBER: \\'${INPUTS.ENGINE\_PIPELINE\_INST\_NUMBER}\\'\\\\n buildNodeGroup: K8S-4\\\\n capabilities: \\'Linux,amd64\\'\\\\n buildEnvironment: container\\\\n specifyContainerImageId: >-\\\\n build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest\\\\n clone\_option: all\\\\n selected\_sources: \\'\\'\\\\n steps: \[\]\\\\n plugins: \[\]\\\\n output: \[\]\\\\n freeInTaskGroupModeFields: \[\]\\\\n","sources":"\[\]","webhook":"e0aO78pcq8n5XaFe81b1"},"originPipelineId":1} |
| plugins | object | 插件列表。 | \[\] |
| refObjectList | object | 插件列表。 | \[\] |
| releaseWorkflowSn | string | 所属的流程 sn。 | workflow-sn-xxxx |
| sn | string | 唯一序列号。 | sn-xxxx |
| variableGroups | array | 变量组列表。 |  |
| \- | object | 通用变量组模型。 |  |
| displayName | string | 变量组显示名。 | 开发变量组 |
| name | string | 变量组标识。 | dev |
| type | string | 变量组类型。 | GLOBAL |

## **返回示例**

`{ "appName": "app-name-xxxx", "labels": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "name": "name-xxxx", "order": "1", "pipeline": "- OneOf": { "engineSn": "321", "engineType": "FlowV2", "pipeline": { }, "pipelineYaml": "{"name":"my-flow-name","owner":"31a62065395ee4198d5516a8","pipelineConfigVo":{"triggerVoList":[{"type":"MANUAL"}],"settings":"{\\"executeScope\\":\\"\\",\\"caches\\":[{\\"directory\\":\\"/root/.m2\\",\\"desc\\":\\"maven依赖缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.gradle/caches\\",\\"desc\\":\\"gradle依赖缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.npm\\",\\"desc\\":\\"npm依赖全局缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.yarn\\",\\"desc\\":\\"yarn依赖全局缓存\\",\\"disable\\":false},{\\"directory\\":\\"/go/pkg/mod\\",\\"desc\\":\\"go mod缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.cache\\",\\"desc\\":\\"其它缓存\\",\\"disable\\":false}]}","flow":"schema: tb\\npipeline:\\n - name: 阶段1\\n stages:\\n - driven: AUTO\\n jobs:\\n - displayName: 空任务\\n task: execution-component@66\\n identifier: \'10_1726646111967\'\\n templateType: task\\n templateSign: \'\'\\n templateBatchUpdate: \'N\'\\n extraInfo: \'\'\\n params:\\n ENGINE_PIPELINE_NAME: \'${INPUTS.ENGINE_PIPELINE_NAME}\'\\n ENGINE_PIPELINE_ID: \'${INPUTS.ENGINE_PIPELINE_ID}\'\\n ENGINE_PIPELINE_INST_ID: \'${INPUTS.ENGINE_PIPELINE_INST_ID}\'\\n ENGINE_PIPELINE_INST_NUMBER: \'${INPUTS.ENGINE_PIPELINE_INST_NUMBER}\'\\n buildNodeGroup: K8S-4\\n capabilities: \'Linux,amd64\'\\n buildEnvironment: container\\n specifyContainerImageId: >-\\n build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest\\n clone_option: all\\n selected_sources: \'\'\\n steps: []\\n plugins: []\\n output: []\\n freeInTaskGroupModeFields: []\\n","sources":"[]","webhook":"e0aO78pcq8n5XaFe81b1"},"originPipelineId":1}", "plugins": { }, "refObjectList": { } }, "- OneOf": { "engineSn": "321", "engineType": "FlowV2", "pipeline": { }, "pipelineYaml": "{"name":"my-flow-name","owner":"31a62065395ee4198d5516a8","pipelineConfigVo":{"triggerVoList":[{"type":"MANUAL"}],"settings":"{\\"executeScope\\":\\"\\",\\"caches\\":[{\\"directory\\":\\"/root/.m2\\",\\"desc\\":\\"maven依赖缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.gradle/caches\\",\\"desc\\":\\"gradle依赖缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.npm\\",\\"desc\\":\\"npm依赖全局缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.yarn\\",\\"desc\\":\\"yarn依赖全局缓存\\",\\"disable\\":false},{\\"directory\\":\\"/go/pkg/mod\\",\\"desc\\":\\"go mod缓存\\",\\"disable\\":false},{\\"directory\\":\\"/root/.cache\\",\\"desc\\":\\"其它缓存\\",\\"disable\\":false}]}","flow":"schema: tb\\npipeline:\\n - name: 阶段1\\n stages:\\n - driven: AUTO\\n jobs:\\n - displayName: 空任务\\n task: execution-component@66\\n identifier: \'10_1726646111967\'\\n templateType: task\\n templateSign: \'\'\\n templateBatchUpdate: \'N\'\\n extraInfo: \'\'\\n params:\\n ENGINE_PIPELINE_NAME: \'${INPUTS.ENGINE_PIPELINE_NAME}\'\\n ENGINE_PIPELINE_ID: \'${INPUTS.ENGINE_PIPELINE_ID}\'\\n ENGINE_PIPELINE_INST_ID: \'${INPUTS.ENGINE_PIPELINE_INST_ID}\'\\n ENGINE_PIPELINE_INST_NUMBER: \'${INPUTS.ENGINE_PIPELINE_INST_NUMBER}\'\\n buildNodeGroup: K8S-4\\n capabilities: \'Linux,amd64\'\\n buildEnvironment: container\\n specifyContainerImageId: >-\\n build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest\\n clone_option: all\\n selected_sources: \'\'\\n steps: []\\n plugins: []\\n output: []\\n freeInTaskGroupModeFields: []\\n","sources":"[]","webhook":"e0aO78pcq8n5XaFe81b1"},"originPipelineId":1}", "plugins": { }, "refObjectList": { } } , "releaseWorkflowSn": "workflow-sn-xxxx", "sn": "sn-xxxx", "variableGroups": [ { "displayName": "开发变量组", "name": "dev", "type": "GLOBAL" } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。