[English](README.md) | **中文**

# TKE Skill

腾讯云 TKE 容器服务运维 Skill，无需安装 MCP Server，通过 AI Coding Agent 的 Skill 机制直接管理 TKE 集群。

支持 OpenClaw、CodeBuddy、Claude Code、Gemini CLI 等主流 AI Coding Agent。

## 安装依赖

```bash
pip install tencentcloud-sdk-python-tke
```

## 凭证配置

支持两种方式（命令行参数优先级更高）：

### 方式一：环境变量（推荐）

```bash
export TENCENTCLOUD_SECRET_ID=你的SecretId
export TENCENTCLOUD_SECRET_KEY=你的SecretKey
```

### 方式二：命令行参数

```bash
python tke_cli.py clusters --secret-id AKIDxxx --secret-key xxxxx --region ap-guangzhou
```

## 安装 Skill

将 SKILL.md 和 tke_cli.py 复制到你的 Agent 对应的 Skills 目录。以下是常见 Agent 的安装方式：

### OpenClaw

```bash
# 将 SKILL.md 和 tke_cli.py 放入 OpenClaw 的 skills 目录
mkdir -p skills/tke/
cp SKILL.md tke_cli.py skills/tke/
```

### CodeBuddy

```bash
# 项目级（仅当前项目生效，可随 git 分发）
mkdir -p <你的项目>/.codebuddy/skills/tke/
cp SKILL.md tke_cli.py <你的项目>/.codebuddy/skills/tke/

# 用户级（全局生效）
mkdir -p ~/.codebuddy/skills/tke/
cp SKILL.md tke_cli.py ~/.codebuddy/skills/tke/
```

### Claude Code

```bash
# 项目级
mkdir -p <你的项目>/.claude/skills/tke/
cp SKILL.md tke_cli.py <你的项目>/.claude/skills/tke/

# 用户级
mkdir -p ~/.claude/skills/tke/
cp SKILL.md tke_cli.py ~/.claude/skills/tke/
```

### 其他 Agent

请参考对应 Agent 的 Skill/Prompt 加载机制，将 `SKILL.md` 作为系统提示词加载，并确保 `tke_cli.py` 可被 Agent 执行即可。

## 使用方式

安装后在 AI Coding Agent 中：

- **自动触发**：当你提到 TKE、集群、容器服务相关话题时，Agent 会自动使用此 Skill
- **手动触发**：输入 `/tke` 后跟你的需求（部分 Agent 支持）

### 示例对话

```
帮我查一下广州地域的所有集群
巡检一下集群 cls-xxx 的状态
获取集群 cls-xxx 的 kubeconfig
```

## 支持的命令

| 命令 | 说明 | 关键参数 |
|------|------|---------|
| `clusters` | 查询集群列表 | `--cluster-ids`, `--cluster-type`, `--limit` |
| `cluster-status` | 查询集群状态 | `--cluster-ids` |
| `cluster-level` | 查询集群规格 | `--cluster-id` |
| `endpoints` | 查询集群访问地址 | `--cluster-id` (必填) |
| `endpoint-status` | 查询端点状态 | `--cluster-id` (必填), `--is-extranet` |
| `kubeconfig` | 获取 kubeconfig | `--cluster-id` (必填), `--is-extranet` |
| `node-pools` | 查询节点池 | `--cluster-id` (必填), `--limit` |
| `create-endpoint` | 开启集群访问端点 | `--cluster-id` (必填), `--is-extranet`, `--subnet-id`, `--security-group`, `--existed-lb-id`, `--domain`, `--extensive-parameters` |
| `delete-endpoint` | 关闭集群访问端点 | `--cluster-id` (必填), `--is-extranet` |

所有命令均支持 `--region`（默认 `ap-guangzhou`）和 `--secret-id` / `--secret-key` 参数。

> `create-endpoint` 和 `delete-endpoint` 为写操作，其他命令均为只读查询。

## 搭配 Kubernetes Specialist Skill 使用

本 Skill 专注于 TKE 集群的**云平台侧管理**（查询集群、节点池、获取 kubeconfig 等）。如果你需要在集群内进行 **Kubernetes 资源操作**（部署工作负载、配置 Service/Ingress、排查 Pod 问题、编写 YAML 清单、Helm 部署等），推荐安装 [Kubernetes Specialist](https://github.com/jeffallan/claude-skills) Skill 配合使用：

```bash
npx skills add https://github.com/jeffallan/claude-skills --skill kubernetes-specialist
```

**典型协作流程**：

1. 使用 TKE Skill 查询集群信息、获取 kubeconfig
2. 使用 Kubernetes Specialist Skill 进行集群内的资源部署、故障排查、安全加固等操作

两个 Skill 配合可以覆盖从 TKE 集群管理到 K8s 集群内操作的完整运维场景。

## 直接使用 CLI

也可以脱离 AI Agent，直接作为命令行工具使用：

```bash
# 查询集群列表
python tke_cli.py clusters --region ap-guangzhou

# 查询集群状态
python tke_cli.py cluster-status --region ap-guangzhou --cluster-ids cls-xxx

# 查询节点池
python tke_cli.py node-pools --region ap-guangzhou --cluster-id cls-xxx

# 获取 kubeconfig
python tke_cli.py kubeconfig --region ap-guangzhou --cluster-id cls-xxx
```
