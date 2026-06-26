# 云效流水线 YAML 编写指南

## 关键经验总结（踩坑记录）

### 1. `create_pipeline_from_description` 完整用法（重要）

**必传参数（否则会用占位符地址导致创建失败）：**

```python
{
    "_tool": "create_pipeline_from_description",
    "organizationId": "<orgId>",
    "name": "<流水线名称>",
    "buildLanguage": "nodejs",       # java/nodejs/python/go/dotnet
    "buildTool": "npm",              # maven/gradle/npm/yarn/pip/go/dotnet
    "repoUrl": "git@codeup.aliyun.com:<orgId>/<repo>.git",   # ⚠️ 必传！
    "branch": "main",
    "serviceName": "<项目名>",
    "serviceConnectionId": "<codeup-uuid>",                   # ⚠️ 必传！
    "deployTarget": "k8s",           # k8s/vm/none
    "kubernetesClusterId": "<your-k8s-cluster-id>",           # deployTarget=k8s 时
    "namespace": "<namespace>",
    "yamlPath": "k8s",
    "dockerImage": "registry.cn-hangzhou.aliyuncs.com/<ns>/<image>"
}
```

**行为说明：**
- 返回 `pipelineId`，但**生成的 YAML 是默认模板**（Node.js 构建 + ArtifactUpload），不是最终可用的
- 必须紧接着调 `update_pipeline` 替换为正确的 Docker 构建 + K8s 部署 YAML
- `buildLanguage` + `buildTool` 即使是纯 Docker 项目也要传（用 `nodejs` + `npm` 绕过）
- 调用耗时较长（10-60秒）

---

### 3. `update_pipeline` 注意事项

```python
{
    "_tool": "update_pipeline",
    "organizationId": "<orgId>",
    "pipelineId": "<id>",
    "name": "<流水线名称>",    # ⚠️ 必传！否则报 required 错误
    "content": "<YAML字符串>"
}
```

YAML 使用 `sources` + `stages` 新格式。

---

### 4. Docker 构建推送：只用 `DockerBuildPushACR`

**✅ 唯一经过验证可用的方式：**

```yaml
docker_build_step:
  name: 构建并推送镜像到ACR
  step: DockerBuildPushACR
  with:
    artifact: app_image
    dockerfilePath: Dockerfile
    dockerRegistry: registry.cn-hangzhou.aliyuncs.com/<namespace>/<image>
    useVpcAddress: false
    dockerTag: <项目名>-${PIPELINE_ID}-${BUILD_NUMBER}
    region: cn-hangzhou
    cacheType: remote
    serviceConnection: <ACR服务连接uuid>
```

**❌ 不要用的方式：**
- `DockerBuild` step：API 要求填明文凭证
- `Command` step + `docker login`：serviceConnection 不会注入凭证环境变量

---

### 5. KubectlApply step 正确参数

```yaml
kubectl_apply:
  step: KubectlApply
  name: Kubectl发布
  with:
    kubernetesCluster: <your-k8s-cluster-id>    # ⚠️ 集群标识，不是数字ID，不是ACK服务连接UUID
    kubectlVersion: "1.25.16"
    namespace: <namespace>
    yamlPath: k8s
    skipTlsVerify: false
    useReplace: false
    skipVariableVerify: false
    variables:
      - key: image
        value: $[stages.build_stage.docker_build_job.docker_build_step.artifacts.app_image]
```

> `kubernetesCluster` 三种易混淆的值：
> - `174472` — ❌ 这是界面显示的数字 ID，不能用
> - `j8ufzdacpc16nrrg` — ❌ 这是 ACK 服务连接 UUID，不能用
> - `<your-k8s-cluster-id>` — 集群标识，从已有流水线的 YAML 里获取，或调 `list_service_connections` 查询

---

### 6. 服务连接查询

使用全局 MCP client（workspace/scripts/mcp/mcp-client.mjs）：

```bash
node /root/.openclaw/workspace/scripts/mcp/mcp-client.mjs call yunxiao list_service_connections '{"organizationId":"<orgId>","serviceConnectionType":"codeup"}'
node /root/.openclaw/workspace/scripts/mcp/mcp-client.mjs call yunxiao list_service_connections '{"organizationId":"<orgId>","serviceConnectionType":"acr"}'
node /root/.openclaw/workspace/scripts/mcp/mcp-client.mjs call yunxiao list_service_connections '{"organizationId":"<orgId>","serviceConnectionType":"ack"}'
```

将查到的 UUID 填入 YAML 模板中的 `serviceConnection` / `kubernetesCluster` 字段。

---

### 8. 标准推荐流程

```
1. list_service_connections           →  查 codeup / ACR / K8s UUID
2. create_pipeline_from_description   →  创建基础模板，获得 pipelineId（必传 repoUrl 等）
3. update_pipeline                    →  替换为正确的 Docker+K8s YAML（必传 name）
4. create_pipeline_run                →  触发运行，获得 runId
5. nohup python3 poll-pipeline.py <runId> <pipelineId> > /tmp/poll-pipeline-<runId>.log 2>&1 & disown $!  →  后台轮询 + 飞书卡片通知（必须用 nohup+disown，防进程被 session 回收）
```

---

### 9. 完整可用的 YAML 模板

**经过验证的完整 YAML 模板（Node.js + Docker + K8s）：**

```yaml
sources:
  main_repo:
    type: codeup
    name: <项目名>
    endpoint: git@codeup.aliyun.com:<orgId>/<repo>.git
    branch: main
    triggerEvents: push
    certificate:
      type: serviceConnection
      serviceConnection: <codeup-uuid>
defaultWorkspace: main_repo

stages:
  build_stage:
    name: 构建镜像
    jobs:
      docker_build_job:
        name: 构建并推送镜像
        runsOn:
          group: public/cn-beijing
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
        steps:
          docker_build_step:
            name: 构建并推送到ACR
            step: DockerBuildPushACR
            with:
              artifact: app_image
              dockerfilePath: Dockerfile
              dockerRegistry: registry.cn-hangzhou.aliyuncs.com/<namespace>/<image>
              useVpcAddress: false
              dockerTag: <项目名>-${PIPELINE_ID}-${BUILD_NUMBER}
              region: cn-hangzhou
              cacheType: remote
              serviceConnection: <your-acr-service-connection-uuid>
        driven: auto
        plugins: []

  deploy_stage:
    name: 部署到K8s
    jobs:
      kubectl_apply_job:
        name: Kubectl发布
        runsOn:
          group: public/cn-beijing
          container: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alinux3:latest
        steps:
          kubectl_apply:
            name: Kubectl发布
            step: KubectlApply
            with:
              kubernetesCluster: <your-k8s-cluster-id>
              kubectlVersion: "1.25.16"
              namespace: <namespace>
              yamlPath: k8s
              skipTlsVerify: false
              useReplace: false
              skipVariableVerify: false
              variables:
                - key: image
                  value: $[stages.build_stage.docker_build_job.docker_build_step.artifacts.app_image]
        driven: auto
        plugins: []
```

---

### 10. Dockerfile 基础镜像

构建机无法访问 `docker.io`（DockerHub），使用 Amazon ECR Public Gallery 代理：

```
public.ecr.aws/docker/library/node:20-alpine
public.ecr.aws/docker/library/nginx:alpine
public.ecr.aws/docker/library/python:3.11-slim
public.ecr.aws/docker/library/golang:1.22-alpine
public.ecr.aws/docker/library/eclipse-temurin:17-jdk-alpine
public.ecr.aws/docker/library/alpine:latest
```

> ECR Public 网络偶尔不稳定，失败可重试。
