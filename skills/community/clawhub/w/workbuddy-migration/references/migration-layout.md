# WorkBuddy 数据落盘全景图

换机迁移的本质 = 把"本机磁盘上的 WorkBuddy 状态"完整搬到新电脑。本图说明哪类数据在哪里、归哪层管、能否自动恢复。

## 一、目录总览（Windows）

```
%USERPROFILE%\
├── .workbuddy\                          ← WorkBuddy 用户级数据根
│   ├── skills\                          用户级技能（配置层）
│   ├── user-<UUID>-personal\            长期记忆 MEMORY/SOUL/IDENTITY/USER（配置层，UUID=账号）
│   ├── projects\                        会话对话历史 JSONL（数据层，通常数百 MB）
│   ├── workspace\sessions\              文件修改备份快照（数据层，通常 1GB+）
│   ├── blobs\                           artifact 图片 blob（数据层）
│   ├── plans\ scripts\ backups\         Plan 文档 / 用户脚本 / 各类备份（数据层）
│   ├── memory\<UUID>_memory.md          账号记忆文件（数据层，按账号改名还原）
│   ├── connectors\<UUID>\               连接器本地配置（数据层）
│   ├── storage\                         会话显示状态/专家选择/账号快照（数据层）
│   ├── <UUID>\                          侧边栏账号快照目录（数据层）
│   ├── mcp.json models.json settings.json workbuddy.db 等零散文件（配置层）
│   └── 其余目录（artifact-index / file-history / skills-marketplace / security ...）兜底收集（数据层）
├── WorkBuddy\                           ← 会话工作区父目录（配置层）
│   └── <日期-时间戳>\                    每次会话一个工作区（含 .workbuddy\memory 等）
├── .claude\                             Claude Code 切换器/ccproxy 配置（配置层，排除 cache/logs）
├── .local\share\opencode\               opencode 数据（配置层，排除 log/repos）
├── .gitconfig                           git 身份与别名（配置层）
├── .ssh\                                SSH 私钥（**不自动收集**：避免密钥随包扩散，按使用说明 icacls 加固后手工拷贝）
└── <项目目录>\                           git 仓库与数据目录（项目层，自动发现数据盘）
```

## 二、四层分流与恢复方式

| 层 | 打包产物 | 新电脑还原方式 | 预装要求 |
|---|---|---|---|
| 云端 | 无需打包 | 登录同一账号自动同步（资料库/云记忆/定时任务） | 无 |
| 配置层 | `WorkBuddy-Migration.zip` | 双击 `1-oneclick-restore.cmd` 或 `一键恢复.cmd` | 无（Windows 自带 tar 解压；无 tar 时自动 Expand-Archive） |
| 项目层 | `project-data\git-bundles\*.bundle` + `git-dirty\` + `plain\` + `git-portable\` | 双击 `2-restore-projects.cmd` | 无（内置免安装 git；都没有时 winget 自动装） |
| 数据层 | `project-data\wb-extra\`（manifest 驱动） | 双击 `3-restore-wbdata.cmd` | 无 |

## 三、项目层细节

**git 仓库**（含 `.git` 的顶层目录）：
- `git bundle create --all` → 含全部提交历史的单文件（`git-bundles\<名>.bundle`）
- `git status --porcelain`（`core.quotepath=false`）→ 未提交的 modified / untracked 文件与目录（`git-dirty\<名>\`）
- 还原：`git clone <bundle>` → 恢复 origin 为真实远端 → 切回原分支 → 覆盖脏文件
- 已知边界：已删除但未提交的文件不随脏文件还原（bundle 中是已提交版本，需手动处理）

**非 git 目录**：整目录拷贝到 `plain\<名>\`（排除 node_modules/.venv/venv/__pycache__/.git），还原时 robocopy 回原位。

**路径重映射**：manifest 记录每个项目的原始根目录（如 `D:\`）。新电脑该盘符不存在时，自动落到"第一个数据盘"或 `用户目录\Projects`，并明确提示；也可 `restore-projects.ps1 -TargetRoot <path>` 指定。

## 四、数据层细节（manifest 驱动）

`wb-extra\manifest.json` 记录 `src → dst` 映射（dst 相对 `%USERPROFILE%\.workbuddy\`）：

- 普通目录：原名还原（projects / workspace-sessions / blobs / plans / scripts / backups / 兜底目录）
- 账号相关：按新电脑 UUID **自动改名**——`connectors\<旧UUID>`、`storage\user-<旧UUID>-personal`、账号快照目录 `<旧UUID>`、`memory\<旧UUID>_memory.md` 都会改成新电脑探测到的 UUID（探测不到则保持原名并提示）
- 顶层零散文件：除 db/日志外全部收入 `root-files\`，还原到 `.workbuddy\` 根部
- 兜底目录：`.workbuddy` 下未显式收集的目录 → 还原到根部（新版本 WorkBuddy 新增的数据目录也能吃到）
- 明确跳过：`plugins`（可重装）、`cache`/`logs`/`tmp`（可再生）、单目录 > 5GB（需手工处理）

## 五、覆盖度对账（打包后自查）

| 检查项 | 方法 |
|---|---|
| 配置层完整 | zip 大小与 DryRun 预估一致；restore-config.ps1 输出每项文件数，src/dst 不一致会 warn |
| 项目完整 | `project-data\manifest.json` 的 repos/plainDirs 数与 DryRun 扫描一致 |
| 数据完整 | `wb-extra\manifest.json` items 数；还原时每项打印文件数 |
| 账号对齐 | 还原时若新旧 UUID 不同会打印 info 并自动改名 |

## 六、不能自动迁移的（需手工）

1. 连接器授权（腾讯文档等）：DPAPI/凭据管理器加密，跨机无效，重新扫码授权
2. Chrome 书签/扩展：登录 Google 账号同步
3. claude-code-third-party-model 切换器：还原后打开一次，自动拉起 ccproxy + zen_bridge
4. git 推送密码短语 / Windows 凭据管理器里的 git 密码
5. 系统级软件（Python/Node/Go/Qt 等）：按 `环境清单.txt`（注册表导出 + 工具探测）对照安装
