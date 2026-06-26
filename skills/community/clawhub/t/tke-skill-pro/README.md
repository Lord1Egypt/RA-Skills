**English** | [中文](README_CN.md)

# TKE Skill

Tencent Cloud TKE (Tencent Kubernetes Engine) operations Skill. No MCP Server required — manage TKE clusters directly through the Skill mechanism of AI Coding Agents.

Supports OpenClaw, CodeBuddy, Claude Code, Gemini CLI, and other mainstream AI Coding Agents.

## Prerequisites

```bash
pip install tencentcloud-sdk-python-tke
```

## Credential Configuration

Two methods are supported (CLI arguments take precedence):

### Method 1: Environment Variables (Recommended)

```bash
export TENCENTCLOUD_SECRET_ID=YourSecretId
export TENCENTCLOUD_SECRET_KEY=YourSecretKey
```

### Method 2: CLI Arguments

```bash
python tke_cli.py clusters --secret-id AKIDxxx --secret-key xxxxx --region ap-guangzhou
```

## Install Skill

Copy SKILL.md and tke_cli.py to the Skills directory of your Agent. Here are the installation instructions for common Agents:

### OpenClaw

```bash
# Place SKILL.md and tke_cli.py into the OpenClaw skills directory
mkdir -p skills/tke/
cp SKILL.md tke_cli.py skills/tke/
```

### CodeBuddy

```bash
# Project-level (current project only, can be distributed via git)
mkdir -p <your-project>/.codebuddy/skills/tke/
cp SKILL.md tke_cli.py <your-project>/.codebuddy/skills/tke/

# User-level (global)
mkdir -p ~/.codebuddy/skills/tke/
cp SKILL.md tke_cli.py ~/.codebuddy/skills/tke/
```

### Claude Code

```bash
# Project-level
mkdir -p <your-project>/.claude/skills/tke/
cp SKILL.md tke_cli.py <your-project>/.claude/skills/tke/

# User-level
mkdir -p ~/.claude/skills/tke/
cp SKILL.md tke_cli.py ~/.claude/skills/tke/
```

### Other Agents

Refer to your Agent's Skill/Prompt loading mechanism. Load `SKILL.md` as a system prompt and ensure `tke_cli.py` is executable by the Agent.

## Usage

After installation, in your AI Coding Agent:

- **Auto-trigger**: The Agent will automatically use this Skill when you mention TKE, clusters, or container services
- **Manual trigger**: Type `/tke` followed by your request (supported by some Agents)

### Example Conversations

```
List all clusters in the Guangzhou region
Check the status of cluster cls-xxx
Get the kubeconfig for cluster cls-xxx
```

## Supported Commands

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `clusters` | List clusters | `--cluster-ids`, `--cluster-type`, `--limit` |
| `cluster-status` | Query cluster status | `--cluster-ids` |
| `cluster-level` | Query cluster specifications | `--cluster-id` |
| `endpoints` | Query cluster access endpoints | `--cluster-id` (required) |
| `endpoint-status` | Query endpoint status | `--cluster-id` (required), `--is-extranet` |
| `kubeconfig` | Get kubeconfig | `--cluster-id` (required), `--is-extranet` |
| `node-pools` | Query node pools | `--cluster-id` (required), `--limit` |
| `create-endpoint` | Enable cluster access endpoint | `--cluster-id` (required), `--is-extranet`, `--subnet-id`, `--security-group`, `--existed-lb-id`, `--domain`, `--extensive-parameters` |
| `delete-endpoint` | Disable cluster access endpoint | `--cluster-id` (required), `--is-extranet` |

All commands support `--region` (default: `ap-guangzhou`) and `--secret-id` / `--secret-key` parameters.

> `create-endpoint` and `delete-endpoint` are write operations. All other commands are read-only queries.

## Use with Kubernetes Specialist Skill

This Skill focuses on **cloud-side management** of TKE clusters (querying clusters, node pools, getting kubeconfig, etc.). For **in-cluster Kubernetes operations** (deploying workloads, configuring Services/Ingress, troubleshooting Pods, writing YAML manifests, Helm deployments, etc.), it is recommended to install the [Kubernetes Specialist](https://github.com/jeffallan/claude-skills) Skill alongside:

```bash
npx skills add https://github.com/jeffallan/claude-skills --skill kubernetes-specialist
```

**Typical workflow**:

1. Use TKE Skill to query cluster info and obtain kubeconfig
2. Use Kubernetes Specialist Skill for in-cluster resource deployment, troubleshooting, and security hardening

Together, the two Skills cover the full operations spectrum from TKE cluster management to in-cluster K8s operations.

## Standalone CLI Usage

Can also be used as a standalone CLI tool without any AI Agent:

```bash
# List clusters
python tke_cli.py clusters --region ap-guangzhou

# Query cluster status
python tke_cli.py cluster-status --region ap-guangzhou --cluster-ids cls-xxx

# Query node pools
python tke_cli.py node-pools --region ap-guangzhou --cluster-id cls-xxx

# Get kubeconfig
python tke_cli.py kubeconfig --region ap-guangzhou --cluster-id cls-xxx
```
