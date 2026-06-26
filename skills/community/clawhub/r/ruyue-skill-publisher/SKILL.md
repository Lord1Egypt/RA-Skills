---
name: skill-publisher
description: >
  OpenClaw 技能包的发布与管理技能。当用户需要将技能发布到 ClawHub 或 Gitee、
  创建新技能、更新技能版本、通用化技能内容、或管理多渠道分发时使用此技能。
  触发场景：用户提到"发布技能"、"发布到技能商店"、"skill publish"、"上传Gitee"、
  "技能通用化"、"技能包管理"、"多渠道发布"、"安装clawhub"等。
---

# Skill Publisher

OpenClaw 技能包的发布、管理、通用化与多渠道分发指南。包含从实战中总结的经验教训。

## 核心决策树

```
用户要发布技能？
├── 发布到 ClawHub（海外）→ 流程A
├── 发布到 Gitee（国内）→ 流程B
├── 两个渠道都发 → 流程A + 流程B
└── 技能需要通用化改造 → 先做通用化，再发布
```

## 流程A：发布到 ClawHub

### 前置条件

1. **安装 ClawHub CLI**

   沙盒环境通常没有 npm，需要手动安装 Node.js：

   ```powershell
   # 下载便携版 Node.js
   Invoke-WebRequest -Uri "https://nodejs.org/dist/v22.14.0/node-v22.14.0-win-x64.zip" -OutFile "$env:TEMP\node-portable.zip"
   Expand-Archive -Path "$env:TEMP\node-portable.zip" -DestinationPath "$env:USERPROFILE\node-portable" -Force

   # 启用 npm（通过 corepack）
   cmd /c "set PATH=$env:USERPROFILE\node-portable\node-v22.14.0-win-x64;%PATH%&& corepack enable npm"

   # 安装 clawhub
   cmd /c "set PATH=$env:USERPROFILE\node-portable\node-v22.14.0-win-x64;%PATH%&& npm i -g clawhub"
   ```

   **注意**：便携版 Node.js 的 zip 包不含完整 npm，需要通过 corepack 下载。安装后 npm 路径为 `$env:USERPROFILE\node-portable\node-v22.14.0-win-x64\`，所有 clawhub 命令都需要通过 `cmd /c "set PATH=...&&"` 调用。

   **教训**：Node.js zip 版没有 npm.cmd，不能用 PowerShell 的 `& $npm` 直接调用，必须用 `cmd /c` 设置 PATH 后调用。PowerShell 的执行策略会阻止 npm.ps1 执行，但 cmd 不受影响。

2. **登录 ClawHub**

   ```powershell
   # 方式一：浏览器登录（需要回调端口通畅）
   cmd /c "set PATH=$env:USERPROFILE\node-portable\node-v22.14.0-win-x64;%PATH%&& clawhub login"

   # 方式二：Token 登录（推荐，避免回调超时）
   # Token 从 https://clawhub.ai 获取
   cmd /c "set PATH=$env:USERPROFILE\node-portable\node-v22.14.0-win-x64;%PATH%&& clawhub login --token <YOUR_TOKEN>"
   ```

   **教训**：浏览器登录依赖 localhost 回调端口，沙盒环境下通常超时。优先使用 `--token` 方式登录。

3. **验证登录**

   ```powershell
   cmd /c "set PATH=...&& clawhub whoami"
   ```

### 发布命令

```powershell
cmd /c "set PATH=$env:USERPROFILE\node-portable\node-v22.14.0-win-x64;%PATH%&& clawhub publish <技能目录路径> --slug <slug> --name ""<显示名>"" --version <版本号> --tags <标签> --changelog ""<变更说明>"" --no-input"
```

### 更新版本

```powershell
# 升版本号重新发布即可（patch/minor/major）
cmd /c "set PATH=...&& clawhub publish <路径> --slug <slug> --name ""<名称>"" --version 1.0.1 --tags latest --changelog ""修复xxx"" --no-input"
```

**教训**：ClawHub 没有覆盖更新，每次 publish 都是新建版本。相同版本号不能重复发布，必须递增。

## 流程B：发布到 Gitee（国内渠道）

### 前置条件

1. **Gitee 账号**：https://gitee.com/signup
2. **私人令牌**：https://gitee.com/profile/personal_access_tokens
   - 勾选 `projects` 权限

### 创建仓库

```powershell
$body = @{
    access_token = "<TOKEN>"
    name = "openclaw-skills"
    description = "OpenClaw AgentSkills 技能包集合"
    private = $false
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri "https://gitee.com/api/v5/user/repos" -Method Post -ContentType "application/json" -Body $body
```

### 上传文件

```powershell
# 读取文件并 Base64 编码
$content = Get-Content "<文件路径>" -Raw -Encoding UTF8
$base64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))

# 上传（POST 创建，PUT 更新需要 sha）
Invoke-WebRequest -Uri "https://gitee.com/api/v5/repos/<用户名>/<仓库名>/contents/<文件路径>" -Method Post -ContentType "application/x-www-form-urlencoded" -Body "access_token=<TOKEN>&message=描述&content=$base64&encoding=base64" -UseBasicParsing
```

**教训**：
- Gitee API 的 PATCH 改私有仓库为公开可能被拒绝，建议创建时就选好公开/私有
- 上传文件用 `application/x-www-form-urlencoded` 而不是 `application/json`，否则返回 400
- 文件已存在时 POST 会报错，需要先 GET 获取 sha，再 PUT 更新
- 仓库描述中文可能乱码（GBK编码），英文描述更安全

### 设置仓库为公开

```powershell
# 如果创建时默认私有，尝试改公开
$body = "access_token=<TOKEN>&name=<仓库名>&private=false"
Invoke-WebRequest -Uri "https://gitee.com/api/v5/repos/<用户名>/<仓库名>" -Method Patch -ContentType "application/x-www-form-urlencoded" -Body $body -UseBasicParsing
```

**教训**：新建私有仓库可能不支持直接转公开，创建时确认 `private = $false`。

## 技能通用化改造

发布公开技能前，应将项目特定内容通用化：

### 改造原则

| 改造前（项目限定） | 改造后（通用化） |
|---|---|
| 具体平台 API 端点作为核心内容 | 移到「附录：已知平台示例」 |
| 项目特定的文件命名规范 | 改为通用建议，原项目作为示例 |
| 项目特定的 token 格式 | 改为通用描述：格式因平台而异 |
| 项目特定经验教训 | 提炼为通用规律 |

### 关键检查点

1. **description** 中是否包含项目特定名称？（如有，改为通用描述）
2. **核心方法**是否绑定了特定平台？（如有，抽取为通用步骤）
3. **附录**是否保留了有用的平台示例？（保留，标注"仅供参考"）
4. **经验教训**是否可以泛化？（能泛化的泛化，不能的保留为具体案例）

## 用户安装指南模板

发布后应提供清晰的安装说明：

### ClawHub 安装

```bash
npm i -g clawhub
clawhub install <slug>
# 重启 OpenClaw 会话
```

### Gitee 安装

```bash
git clone https://gitee.com/<用户名>/openclaw-skills.git
cp -r openclaw-skills/<技能名> ~/.openclaw/skills/
# 重启 OpenClaw 会话
```

### Windows PowerShell 版

```powershell
git clone https://gitee.com/<用户名>/openclaw-skills.git
Copy-Item -Recurse openclaw-skills\<技能名> $env:USERPROFILE\.openclaw\skills\
```

## 关键经验教训总结

### 环境与工具

1. **沙盒无 npm/git**：OpenClaw 沙盒通常没有包管理器和 git，需要手动安装便携版
2. **PowerShell 执行策略**：阻止 .ps1 脚本执行，用 `cmd /c` 绕过
3. **PowerShell 编码**：默认 GBK，API 请求中的中文可能乱码，描述字段用英文更稳妥
4. **便携版 Node.js**：zip 包不含 npm.cmd，需要 corepack 下载完整 npm

### ClawHub 相关

5. **浏览器登录超时**：沙盒 localhost 回调端口不通，必须用 `--token` 方式
6. **clawhub 命令格式**：`--name` 和 `--changelog` 的值在 PowerShell 中需要双引号 `""`，否则参数截断
7. **版本号必须递增**：相同版本号不能重复发布
8. **exit code**：clawhub 命令即使成功也返回 code 1（stderr 输出 ANSI 颜色码），判断成功看输出内容而非 exit code

### Gitee 相关

9. **API 用 form-urlencoded**：`application/json` 上传文件会返回 400
10. **文件已存在报错**：需要 GET 获取 sha 后用 PUT 更新
11. **私有转公开限制**：某些情况下 API 不支持，创建时确认好
12. **中文描述乱码**：API 返回的中文可能是 GBK 乱码，实际内容正确，不影响使用

### 技能设计

13. **通用化优先**：公开发布的技能应去除项目绑定，平台特定内容放附录
14. **description 是触发器**：SKILL.md 的 description 决定技能何时被加载，要写全触发场景
15. **progressive disclosure**：核心流程放 SKILL.md，详细参考放 references/ 子目录
16. **保持 SKILL.md 精简**：控制在 500 行以内，超出的拆到 references 文件

## 账号信息

- **ClawHub**: @RuyueChina → https://clawhub.ai/skills/
- **Gitee**: @ruyueteam → https://gitee.com/ruyueteam/openclaw-skills
- **Gitee Token**: 已配置（存储在本地，不外泄）

## 命令速查

```powershell
# 设置 PATH（每次调用 clawhub 前需要）
$NODE = "$env:USERPROFILE\node-portable\node-v22.14.0-win-x64"
$CMD = "cmd /c `"set PATH=$NODE;%PATH%&&"

# ClawHub 操作
& "$CMD clawhub whoami"
& "$CMD clawhub publish <路径> --slug <slug> --name ""<名>"" --version <ver> --tags latest --changelog ""<说明>"" --no-input"
& "$CMD clawhub search ""关键词"""
```
