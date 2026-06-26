---
name: ssh-agentd-control
description: 管理并使用本地 ssh-agentd（systemd 常驻 + API 调用 + 连通性验证）。当用户提到 ssh-agentd、持久 SSH 会话、/run /upload /tail_logs、开机自启、会话状态/指标排查时使用。
---

# ssh-agentd 控制技能

适用环境（当前）：
- 二进制：`/home/krex/.openclaw/workspace-hermes/ssh-agentd/bin/ssh-agentd`
- 配置：`/home/krex/.openclaw/ssh-agentd/hosts.yaml`
- systemd：`ssh-agentd.service`
- 默认监听：`127.0.0.1:18081`

## 快速检查

```bash
sudo systemctl is-enabled ssh-agentd.service
sudo systemctl is-active ssh-agentd.service
ss -ltnp | grep 18081
sudo systemctl status ssh-agentd.service --no-pager -l | sed -n '1,80p'
```

## 启停与自启

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ssh-agentd.service
sudo systemctl restart ssh-agentd.service
sudo systemctl stop ssh-agentd.service
```

## API 调用要点

1) 默认使用 Bearer Token 鉴权（若配置启用）
2) 本机常有代理变量，调用本地 API 时必须绕过代理

推荐统一用脚本：`scripts/api.sh`

### 示例：运行远程命令

```bash
SSH_AGENTD_TOKEN='<token>' \
  scripts/api.sh POST /run '{"host":"nas","cmd":"hostname && whoami","timeoutSec":10}'
```

### 示例：查看会话与指标

```bash
SSH_AGENTD_TOKEN='<token>' scripts/api.sh GET /sessions
SSH_AGENTD_TOKEN='<token>' scripts/api.sh GET /metrics
SSH_AGENTD_TOKEN='<token>' scripts/api.sh GET /health
```

## 常见故障

### 1) 返回 401 unauthorized
- 检查 `apiAuth.enabled/token` 配置
- 确认请求头 `Authorization: Bearer <token>`

### 2) 调本地 API 返回 502
- 原因：请求被系统代理劫持
- 处理：用 `--noproxy '*'` 或临时 unset 代理变量（脚本已内置）

### 3) run 失败且提示 host key/known_hosts
- 原因：v1 已启用 HostKey 校验
- 处理：把目标主机 key 加入 `known_hosts`

## 安全约束

- 不要把真实 token/密码写进 skill 文件。
- 不要把 `hosts.yaml` 放进仓库。
- 修改服务配置后必须重启并验证 `status + /health + /sessions`。
