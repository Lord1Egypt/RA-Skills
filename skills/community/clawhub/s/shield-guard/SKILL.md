---
name: openclaw-shield
description: OpenClaw 安全扫描与防护技能：检查端口暴露、认证配置、插件安全、凭证管理，修复工信部2026年预警风险点。触发词：OpenClaw安全吗、帮我检查安全、扫描风险、工信部。
version: 1.0.0
author: clawhub-master
trigger:
  - "OpenClaw安全吗"
  - "帮我检查安全"
  - "扫描风险"
  - "工信部"
  - "安全扫描"
  - "检查OpenClaw安全隐患"
---

# openclaw-shield

> 保障 OpenClaw AI 助手安全运行的防护技能，符合工信部2026年安全规范。

## 触发条件
当用户询问"OpenClaw 安全吗？"、"帮我检查安全"、"扫描风险"、"工信部"等关键词时触发。

---

## 第一步：自动化安全扫描

### 1.1 检查 Gateway 配置
通过 `gateway(action="config.get", path="gateway")` 获取：
- `bind` 是否为 `loopback`（✅ 安全）或 `0.0.0.0`（⚠️ 公网暴露）
- `auth.mode` 是否为 `token`（✅ 安全）或 `none`（⚠️ 无认证）
- `controlUi.allowInsecureAuth`（建议 false）
- `tailscale.mode`（建议 off）

### 1.2 检查端口暴露
执行命令检查真实监听地址：
```powershell
netstat -ano | Select-String '18789' | Select-String 'LISTENING'
```
- 仅 `127.0.0.1:18789` ✅ 安全
- `0.0.0.0:18789` 或 `:::18789` ❌ 公网暴露

### 1.3 检查插件安全
通过 `gateway(action="config.get", path="plugins")` 获取：
- `plugins.allow` 列表是否非空（白名单制 ✅）
- 是否有非官方/未知插件

### 1.4 检查 Skills 来源
扫描 `~/.openclaw/skills/` 和 `workspace/skills/`：
- 是否包含非 ClawHub 官方 Skills
- 是否有可疑的第三方 Skills

### 1.5 检查凭证管理
- 敏感配置文件是否在 workspace 内（风险）
- 是否有硬编码 API Key 在 Skills 中
- credentials/ 目录是否在 workspace 外

### 1.6 检查飞书/微信配置
通过 `gateway(action="config.get", path="channels")` 获取：
- 飞书群组 `requireMention` 配置
- 微信 `dmPolicy` 配置

---

## 第二步：生成安全报告

基于以上扫描结果，生成以下格式的安全报告文件：
```
D:\openclaw-data\.openclaw\workspace\IMA_Notes\OpenClaw安全扫描报告_YYYY-MM-DD.md
```

### 报告内容要求
1. **安全评级**（🟢 优秀 / 🟡 中等 / 🔴 高危）
2. **工信部六要六不要对照检查表**
3. **已确认安全项**（绿色清单）
4. **存在的风险点**（⚠️ 列表，按 P0/P1/P2 分类）
5. **修复建议**（具体操作步骤）

---

## 第三步：自动修复（需要用户同意）

### P0 立即修复
1. **关闭控制台弱认证**：
   - 修改 `gateway.config.patch` path: `gateway.controlUi` value: `{ "allowInsecureAuth": false }`
   - 需要 `gateway restart`

### P1 本周修复
2. **飞书群组安全**：建议开启 `requireMention: true`
3. **端口暴露自查**：提供 PowerShell 命令让用户自行检查

---

## 安全红线（绝对不能做的事）

1. **不要**将 Gateway 端口暴露到 `0.0.0.0`
2. **不要**关闭 `auth.mode`（即不要改成 `none`）
3. **不要**安装来源不明的 ClawHub Skills
4. **不要**在 Skills 中硬编码 API Key 或凭证
5. **不要**将 credentials 目录放在 workspace 内

---

## 工信部"六要六不要"核心要求（内置知识）

### 六要
1. 优先使用官方渠道最新稳定版本，启用自动更新
2. 严格控制互联网暴露面，SSH 加密通道，硬件密钥
3. 不将默认端口暴露到公网，配置为仅本地访问
4. 不使用管理员/超级用户权限运行
5. 安装可信 Skills（白名单制）
6. 定期审计操作日志

### 六不要
1. 严禁使用第三方镜像或历史版本
2. 杜绝直接暴露实例至公网
3. 禁止无认证访问
4. 禁止全权限运行
5. 禁止安装非官方 Skills
6. 禁止在配置文件中明文存储凭证

---

## 关联事件（2026年3月工信部预警）

- **CVE-2026-30891**：CVSS 9.1，OpenClaw 2.0 前版本默认无认证
- **ClawHavoc 供应链攻击**：1184 个恶意 Skill 伪装发布
- **ClawJacked 攻击链**：公网暴露实例可被恶意网页静默接管
- **Moltbook 数据泄露**：150万 API Token，Supabase 配置错误

---

## 紧急响应流程

如果发现实例已被入侵：
1. **立即断网**：关闭机器或禁用网络适配器
2. **不要重启 Gateway**：避免覆盖内存中的入侵痕迹
3. **检查日志**：查找异常命令执行记录
4. **重置所有 Token**：微信/飞书/Gateway token/所有 API Key
5. **报告**：联系 OpenClaw 官方安全团队

---

## 相关文件路径
- Gateway 配置：`D:\openclaw-data\openclaw.json`
- 凭证目录：`D:\openclaw-data\.openclaw\workspace\credentials\`
- Skills 目录：`D:\openclaw-data\.openclaw\workspace\skills\`
- 安全报告：`D:\openclaw-data\.openclaw\workspace\IMA_Notes\OpenClaw安全扫描报告_YYYY-MM-DD.md`