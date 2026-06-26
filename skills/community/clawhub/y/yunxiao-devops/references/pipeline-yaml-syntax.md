# 云效流水线 YAML 语法参考（官方文档整合）

> 来源：官方文档包 `流水线yaml语法.zip`，整合于 2026-03-16
> 使用时配合 `pipeline-yaml-guide.md`（踩坑经验）一起参考

---

## 一、YAML 整体结构

```yaml
name: pipeline-name          # 流水线展示名称

sources:                     # 代码源/制品源
  <source_id>:
    type: codeup
    ...

defaultWorkspace: <source_id>  # 多代码源时必填，指定默认工作区

mountDirs:                   # 私有构建集群目录挂载（可选）
  - hostDir: /root/.m2
    containerMountDir: /root/.m2

cache:                       # 构建缓存（可选）
  cacheDirs:
    - /root/.m2
  cacheMode: remote          # remote（公共集群）或 local（私有集群）

variables:                   # 流水线级环境变量（可选）
  - key: appname
    value: myapp

variableGroups: [<groupId>]  # 关联变量组（可选）

concurrencyConfig:           # 并发控制（可选）
  maxRunningPipelineInstances: 1
  pipelineMaxRunningBehavior: preemptOldest

stages:                      # 流水线阶段（必填）
  <stage_id>:
    name: 阶段名
    jobs:
      <job_id>:
        ...
```

---

## 二、sources 代码源

### 支持的源类型

| 类型 | YAML 标识 | 备注 |
|------|-----------|------|
| 云效 Codeup | `codeup` | 支持 push/tagPush/mergeRequest 触发 |
| GitHub | `github` | 支持 push 触发 |
| GitLab | `gitlab` | 支持 push/tagPush/mergeRequest |
| SVN | `svn` | 支持 push 触发 |
| 通用 Git | `git` | 支持 push 触发 |
| Flow 流水线 | `flowPipeline` | 流水线之间互相触发 |
| Packages 通用制品 | `packages` | repoType 只支持 generic |
| ACR 企业版镜像 | `acr` | 支持 pushCompleted/scanCompleted |
| Jenkins | `jenkins` | 外部 Jenkins 触发 |
| 示例代码 | `gitSample` | 多语言示例库，不支持触发 |

### Codeup 代码源示例

```yaml
sources:
  main_repo:
    type: codeup
    name: 代码源名称
    endpoint: https://codeup.aliyun.com/<orgId>/<repo>.git
    branch: master
    branchesFilter: release_*        # 分支过滤（正则），可选
    cloneDepth: 10                   # 克隆深度，0=全部，可选
    submodule: false                 # 是否克隆子模块，可选
    triggerEvents:
      - push
      - tagPush
      - mergeRequestMerged
      - mergeRequestOpenedOrUpdate
    pathFilter: ^src/.*              # 路径过滤（正则），可选
    certificate:
      type: serviceConnection
      serviceConnection: <uuid>
```

### ACR 镜像源示例

```yaml
sources:
  my_acr:
    type: acr
    region: cn-hangzhou
    instance: yunxiao               # ACR 企业版实例名
    namespace: default
    imageRepo: my-image
    imageTag: v1.0
    versionFilter: .*               # 版本过滤（正则），可选
    triggerEvents:
      - pushCompleted
      - scanCompleted
    certificate:
      type: serviceConnection
      serviceConnection: <uuid>
```

### Flow 流水线源示例

```yaml
sources:
  ci_pipeline:
    type: flowPipeline
    name: CI流水线
    flowPipeline: <16位流水线ID>
    build: lastSuccessfulBuild
    triggerEvents: buildSuccess
```

---

## 三、stages / jobs / steps 结构

### 核心结构

```yaml
stages:
  <stage_id>:
    name: 阶段名
    jobs:
      <job_id>:
        name: 任务名
        runsOn: public/cn-beijing           # 构建环境（简写）
        # 或指定容器：
        runsOn:
          group: public/cn-beijing          # 公共集群：cn-beijing / cn-hangzhou / cn-hongkong
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
          instanceType: LARGE_4C8G          # 可选：SMALL_1C2G / MEDIUM_2C4G / LARGE_4C8G / XLARGE_8C16G
        timeoutMinutes: 60                  # 超时分钟数，默认240，可选
        driven: auto                        # auto（自动）/ manual（手动确认），可选
        needs:                             # 依赖的前序 job_id，可选
          - other_job_id
        condition: |                       # 执行条件表达式，可选
          "${CI_COMMIT_REF_NAME}" == "master"
        sourceOption: [repo1, repo2]       # 指定下载哪些代码源，[] 表示不下载，可选
        steps:
          <step_id>:
            name: 步骤名
            step: <StepType>
            workspace: repo2               # 指定工作目录（多源时），可选
            with:
              <参数>: <值>
        plugins:                           # 通知插件，可选
          - name: 飞书通知
            plugin: FeishuPlugin
            triggerState: [success, fail]
            with: ...
```

### 使用 component（组件任务）

```yaml
jobs:
  deploy_job:
    name: 部署
    component: VMDeploy           # 指定组件（不使用 steps）
    with:
      artifact: $[stages.build_stage.build_job.upload_step.artifacts.default]
      machineGroup: <machine-group-id>
      artifactDownloadPath: /home/admin/app/package.tgz
      executeUser: root
      run: |
        tar zxvf /home/admin/app/package.tgz -C /home/admin/application/
        sh /home/admin/application/deploy.sh restart
```

---

## 四、condition 条件语法

### 关系/逻辑操作符

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `"${BRANCH}" == "master"` |
| `!=` | 不等于 | `"${BRANCH}" != "master"` |
| `&&` | 与 | `"${A}" == "x" && succeed()` |
| `\|\|` | 或 | `"${A}" == "x" \|\| "${A}" == "y"` |

### 内置函数

| 函数 | 说明 |
|------|------|
| `startsWith(str, prefix)` | 字符串开头匹配 |
| `endsWith(str, suffix)` | 字符串结尾匹配 |
| `contains(array, item)` | 数组包含某元素 |
| `weekDay()` | 返回周几（Monday...Sunday） |
| `timeIn(start, end)` | 当前时间是否在范围内 |
| `always()` | 始终返回 true（无论前序结果） |
| `succeed(job_id...)` | 前序任务成功才返回 true |
| `failed(job_id...)` | 前序任务失败才返回 true |

### 示例

```yaml
# 分支为 master 时执行
condition: |
  "${CI_COMMIT_REF_NAME}" == "master"

# 发布窗口期（工作日 20:00-22:00）自动跳过审核
condition: |
  timeIn("20:00:00", "22:00:00") && weekDay() != "Saturday" && weekDay() != "Sunday"

# 前序 job1 或 job2 任意成功才执行
condition: succeed(job_1) || succeed(job_2)
```

---

## 五、artifacts 制品引用语法

### 制品生成步骤

| Step | 生成类型 |
|------|---------|
| `DockerBuildPushACR` / `ACRDockerBuild` | dockerImage |
| `ArtifactUpload` | flowPublic / packages |

### 引用语法

```yaml
# 同阶段跨 Job 引用
$[jobs.<job_id>.<step_id>.artifacts.<artifact_name>]

# 跨阶段引用
$[stages.<stage_id>.<job_id>.<step_id>.artifacts.<artifact_name>]

# 跨流水线引用（flowPipeline 源）
$[sources.<source_id>.stages.<stage_id>.<job_id>.<step_id>.artifacts.<artifact_name>]

# 从制品源引用
$[sources.<source_id>]                  # 引用整个制品
$[sources.<source_id>.downloadUrl]      # 引用下载地址
$[sources.<source_id>.dockerUrl]        # 引用镜像地址（ACR 源）
```

---

## 六、variables 环境变量

```yaml
variables:
  - key: APP_NAME
    value: myapp                        # 默认 String 类型
  - key: RETRY
    type: Number
    value: 3
  - key: IS_GRAY
    type: Boolean
    value: true
  - key: APP_LIST
    type: Object
    value: ["app1", "app2", "app3"]

# 引用变量：${KEY}
```

### 变量优先级（高→低）

1. 运行时手动输入
2. YAML step 参数
3. YAML variables 配置
4. YAML variableGroups 关联变量组
5. UI 页面配置变量
6. UI 页面配置变量组

### 系统内置环境变量（常用）

| 变量 | 说明 |
|------|------|
| `${PIPELINE_ID}` | 流水线 ID |
| `${BUILD_NUMBER}` | 流水线运行编号（从1开始自增） |
| `${PIPELINE_NAME}` | 流水线名称 |
| `${DATETIME}` | 当前时间（如 2017-06-22-23-26-33） |
| `${TIMESTAMP}` | 当前时间戳（如 1581581273232） |
| `${BUILD_EXECUTOR}` | 流水线触发人 |
| `${CI_COMMIT_REF_NAME}` | 当前运行分支或 Tag |
| `${CI_COMMIT_ID}` | 8 位 commit ID |
| `${CI_COMMIT_SHA}` | 完整 commit ID |
| `${CI_COMMIT_TITLE}` | 最后一次提交信息 |

---

## 七、template 动态渲染语法

首行加 `# template=true` 开启，遵循 Go template 语法：

```yaml
# template=true
variables:
  - key: envList
    type: Object
    value: ["dev", "staging", "prod"]

stages:
  deploy_stage:
    name: 部署
    jobs:
      {{ range $env := .envList }}
      deploy_{{ $env }}_job:
        name: 部署到-{{ $env }}
        steps:
          deploy_step:
            step: Command
            name: 部署
            with:
              run: echo deploying to {{ $env }}
      {{ end }}
```

### 扩展函数

```
{{ add 1 2 }}                            # 整数相加，返回 3
{{ "Hello World" | replace "World" "Yunxiao" }}  # 字符串替换
```

---

## 八、常用 Step 类型

| Step | 用途 |
|------|------|
| `Command` | 执行 Shell 命令 |
| `JavaBuild` | Java Maven 构建 |
| `NodeBuild` | Node.js 构建 |
| `DockerBuildPushACR` | ✅ Docker 构建推送 ACR（推荐） |
| `KubectlApply` | K8s 部署 |
| `ArtifactUpload` | 上传构建物 |
| `ManualValidate` | 人工卡点审核 |
| `SetupNode` | 安装 Node.js 环境 |
| `SetupNpmrc` | 配置 npmrc |

---

## 九、常用 component 类型

| Component | 用途 |
|-----------|------|
| `VMDeploy` | 主机组部署 |
| `KubernetesBatchDeploy` | K8s 分批发布 |
| `KubernetesBlueGreenDeploy` | K8s 蓝绿发布 |
| `AppStackFlowDeploy` | 云效 AppStack 部署 |
| `ManualValidate` | 人工卡点 |
| `ECSAppDeploy` | ECS 应用部署 |

---

## 十、plugins 通知插件

```yaml
plugins:
  - name: 飞书通知
    plugin: FeishuPlugin           # DingTalkPlugin / WechatPlugin / EmailPlugin / WebhookPlugin
    triggerState:
      - success
      - fail
    with:
      webhook: <飞书群 webhook>
      noticeContent:
        - pipelineName
        - status
      customContent: 构建完成
```

---

## 十一、完整示例：Codeup → Docker → K8s

```yaml
name: my-cicd-pipeline

sources:
  main_repo:
    type: codeup
    name: 主仓库
    endpoint: git@codeup.aliyun.com:<orgId>/<repo>.git
    branch: main
    triggerEvents: push
    certificate:
      type: serviceConnection
      serviceConnection: <codeup-service-connection-uuid>
defaultWorkspace: main_repo

stages:
  build_stage:
    name: 构建镜像
    jobs:
      docker_build_job:
        name: Docker构建推送
        runsOn:
          group: public/cn-beijing
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
        steps:
          docker_step:
            name: 构建并推送到ACR
            step: DockerBuildPushACR
            with:
              artifact: app_image
              dockerfilePath: Dockerfile
              dockerRegistry: registry.cn-hangzhou.aliyuncs.com/<namespace>/<image>
              useVpcAddress: false
              dockerTag: ${PIPELINE_ID}
              region: cn-hangzhou
              cacheType: remote
              serviceConnection: <acr-service-connection-uuid>

  deploy_stage:
    name: 部署
    jobs:
      kubectl_job:
        name: K8s部署
        runsOn:
          group: public/cn-beijing
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
        steps:
          kubectl_step:
            name: Kubectl发布
            step: KubectlApply
            with:
              kubernetesCluster: <k8s-cluster-id>
              kubectlVersion: "1.25.16"
              namespace: default
              yamlPath: k8s/deployment.yaml
              variables:
                - key: image
                  value: $[stages.build_stage.docker_build_job.docker_step.artifacts.app_image]
```

> 配合 `pipeline-yaml-guide.md` 踩坑记录使用，特别注意：
> - 服务连接 ID 需通过 `list_service_connections` API 查询真实 UUID
> - K8s YAML 中变量占位符用 `${image}`（云效语法，非 K8s 原生 `$(image)`）
