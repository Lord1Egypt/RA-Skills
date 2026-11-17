---
name: "self-upgrade-gateway"
description: "零停机升级 OpenClaw Gateway：查 release notes → 主公确认 → 旁路备份 → npm install → node版本自动检测 → 重启 + 回滚兜底"
---

# self-upgrade-openclaw

## 用途

**零停机升级 OpenClaw**。

## 核心策略

```
查 release notes → 主公确认无 breaking change → 
旁路备份（安全锚点）→ npm install -g → 
修正 systemd Node 路径 → 更新 systemd 版本号 → 重启 + 健康检查 →
失败则从备份回滚 / 成功则自动清理
```

## 环境要求

| 项目 | 说明 |
|------|------|
| 操作系统 | Linux（WSL2 亦可） |
| Node.js | 至少一个版本满足新版 openclaw 的 engines.node 要求 |
| npm | 任意 |
| service 管理 | systemd user 模式 |
| 磁盘空间 | 至少 2G 可用 |
| 网络 | 能访问 registry.npmjs.org 和 api.github.com |

## 前提假设

- OpenClaw 通过 `npm install -g` 全局安装
- 服务通过 systemd user 管理（`openclaw-gateway.service`）
- npm global 在 `$HOME/.npm-global/`
- 有 `systemctl --user` 权限

## 流程

### 阶段 0: 获取当前状态 + Node 版本兼容性预检

1. 读取 systemd 单元文件和 npm 全局目录，获取当前版本
2. 查询 npm registry 获取最新稳定版版本号
3. 如果最新版 ≤ 当前版，告知主公已是最新版，结束
4. Node 兼容性预检：用 `npm pack` 下载目标版本 → 读取 `engines.node` 要求 → 遍历 `which -a node` 及常见 Node 安装路径 → 如果没有一个 Node 版本满足要求则提示升级 Node 后重试

### 阶段 1: 获取 release notes，主公确认

1. 从 GitHub API 获取目标版本的 release notes
2. 展示给主公：当前版本 → 目标版本、Node 版本兼容性检查结果、release notes 核心摘要、是否包含 breaking changes
3. 询问主公是否现在升级

### 阶段 2: 执行升级

运行升级脚本，全自主执行：

1. 前置检查（命令可用性、磁盘空间、服务状态）
2. Node 版本兼容性预检（预下载包、读 engines、扫描兼容 Node）
3. 查 release notes（备忘）
4. 旁路备份
5. npm install -g openclaw@latest（失败自动回滚）
6. 修正 systemd ExecStart 中的 Node 路径（如果旧 Node 不满足新版本要求）
7. 更新 systemd 版本号
8. 重启 + 健康检查（60s 超时）
9. 失败回滚 / 成功清理

### 阶段 3: 汇报结果

## 安全机制

| 机制 | 说明 |
|------|------|
| Node 兼容性预检 | 预下载包 → 解析 engines.node → 检查系统所有 Node → 无兼容版本则中止 |
| systemd Node 路径自动修正 | 检测 ExecStart 中的 node 路径，不满足要求时自动切换到兼容版本 |
| 旁路备份 + 自动回滚 | 健康检查失败后恢复旧代码 + 旧 Node 路径 + 重启旧版 |
| 全日志落盘 | 不依赖终端 |
| 人工确认 | 先展示 release notes 再执行 |

## 变更日志

### v2.0.0
- 新增 Node 版本兼容性预检
- 新增自动修正 systemd ExecStart 路径
- 兼容两种版本号格式
- 修复 release notes 查询硬编码版本号的 bug

### v1.0.0
- 初始版本
