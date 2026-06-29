# self-update-zero-downtime

## 用途

**零停机升级 OpenClaw**。适用于以下指令：
- "升级 OpenClaw"
- "更新 openclaw" / "帮我更新"
- "检查更新" / "检查升级"
- "升级到最新版"
- "帮我升级一下"
- 任何涉及 OpenClaw 自身升级的对话

## 核心策略

```
查 release notes → 主公确认无 breaking change →
旁路备份（安全锚点）→ npm install -g（不用本地 build）→
更新 systemd 版本号 → 重启 + 健康检查 →
失败则从备份回滚 / 成功则自动清理
```

**特点**：
- ✅ 零停机：仅重启瞬间闪断（~10s），systemd `Restart=always` 自动恢复
- ✅ 永不 offline：旁路备份 + 回滚机制确保任何情况可恢复
- ✅ 用户确认：先展示 release notes，确认无 breaking change 后再执行
- ✅ 全日志：所有输出落文件，不依赖终端
- ✅ 路径自适应：自动探测 systemd ExecStart 指向的代码目录、npm global 目录

## 触发条件

- 主公明确要求升级/更新 OpenClaw
- 会话上下文表明需要进行 OpenClaw 自身升级

## 环境要求

| 项目 | 说明 |
|------|------|
| 操作系统 | Linux（WSL2 亦可） |
| Node.js | ≥ 22 |
| npm | 任意（需要能访问 npm registry） |
| service 管理 | systemd user 模式（非必需，无 systemd 仅替换代码） |
| 磁盘空间 | 至少 2G 可用 |
| 网络 | 能访问 `registry.npmjs.org` 和 `api.github.com` |

## 前提假设

- OpenClaw 是 **`npm install -g` 全局安装**的（不是 git checkout / 手动构建）
- 有 `systemctl --user` 权限
- npm prefix 可写（`npm config get prefix` 返回用户可写的目录）

## 安装类型检测

脚本会探测安装方式，以下情况会中止并提示：

| 情况 | 检测方式 | 处理 |
|------|---------|------|
| npm global install（推荐） | 代码目录含 package.json，无 .git | ✅ 正常升级 |
| git checkout | 代码目录含 .git | ❌ 中止，提示用 `openclaw update` |
| 运行目录 ≠ npm global 目录 | systemd ExecStart vs npm root -g 不一致 | ❌ 中止，需先统一 |
| npm prefix 不可写 | `npm config get prefix` 返回不可写路径 | ❌ 中止，提示配置用户级 prefix |
| 运行目录无 package.json | 目录不存在或为空架子 | ❌ 中止 |

### npm prefix 不可写的解决方法

```bash
npm config set prefix "$HOME/.npm-global"
# 确保 $HOME/.npm-global/bin 在 PATH 中
# 然后把 openclaw binary 链接过去:
ln -sf "$HOME/.npm-global/lib/node_modules/openclaw/openclaw.mjs" "$HOME/.npm-global/bin/openclaw"
# 更新 systemd unit 中的 PATH 后重启服务
```

## 路径探测策略

1. 从 `systemctl --user show <service> -p ExecStart` 反推实际运行的代码目录
2. 从 `npm root -g` 获取 npm global 安装目录
3. 两者一致 → 标准 npm global install 场景
4. 两者不一致 → 中止（需先处理目录不一致问题）
5. 升级后如果运行目录和 npm global 目录不同，自动同步新代码到运行目录

## 流程

### 阶段 0: 探测 + 校验

1. 自动探测代码目录（ExecStart）、npm global 目录、npm prefix
2. 校验安装类型（git vs npm global）、目录一致性、prefix 可写性
3. 查询 npm registry 获取最新稳定版
4. 从 GitHub API 获取 release notes
5. 询问主公确认

### 阶段 1: 旁路备份

完整 `cp -r` 运行目录到 `{运行目录}-fallback`。

### 阶段 2: npm install -g

`npm install -g openclaw@latest` → 验证版本 → 检查入口文件（`dist/*.js` 或 `openclaw.mjs`）→ 如需同步到非一致的运行目录。

### 阶段 3: 更新 systemd 版本号

更新 unit 文件 `OPENCLAW_SERVICE_VERSION`。

### 阶段 4: 重启 + 健康检查

`systemctl --user restart` → 最长等 60s。

### 阶段 5: 汇报

## 安全机制

| 机制 | 说明 |
|------|------|
| 旁路备份 | `cp -r` 运行目录到 `{目录}-fallback` |
| 自动回滚 | 健康检查失败后从 fallback 恢复 + 重启旧版 |
| systemd 兜底 | `Restart=always` + `StartLimitBurst=5` |
| 日志落盘 | 所有输出写日志文件 |
| 人工确认 | 必须展示 release notes，主公确认后再执行 |
| 兼容性校验 | 检测 git checkout / 目录不一致 / prefix 不可写，提前中止 |

## 故障排除

### 升级后需要重新输密码

部分版本可能改动了认证机制。如果升级后 WebChat 提示密码错误：
- 检查 `~/.openclaw/openclaw.json` 中的 gateway password 配置
- 在 WebChat Control UI 设置中重新输入密码

### 服务启动失败

```bash
systemctl --user status openclaw-gateway
journalctl --user -u openclaw-gateway -n 50
```

### 手动回滚

```bash
rm -rf $(npm root -g)/openclaw
cp -r $(npm root -g)/openclaw-fallback $(npm root -g)/openclaw
systemctl --user restart openclaw-gateway
```

## 安装

```bash
clawhub install self-update-zero-downtime
```

## 变更日志

### v1.0.3
- git checkout 安装精确检测（检查 .git）
- 运行目录与 npm global 目录不一致时中止
- npm prefix 不可写检测并给出解决步骤
- 目录不一致时自动同步新代码的 fallback 处理
- 安装类型校验前置到备份前，避免无效备份

### v1.0.2
- 动态路径探测
- 入口文件检查放宽
- 修复拼写错误

### v1.0.1
- 完全动态路径探测
- 修复多处硬编码

### v1.0.0
- 初始发布
