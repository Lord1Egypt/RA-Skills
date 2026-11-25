# WorkBuddy 一键迁移（换电脑）

把一台电脑上的全部 WorkBuddy 内容搬到新电脑：**旧电脑一键打包 → 移动硬盘直拷 → 新电脑一键恢复**。

- 自动探测：账号、工作区、项目所在磁盘，无需任何配置
- 三层全覆盖：配置层（技能/记忆/工作区）+ 项目层（git 仓库+数据）+ 数据层（会话历史/修改备份/blob/索引）
- 新电脑零预装：不需要 git、不需要 7z（内置免安装 git + Windows 自带 tar）
- 断点可续：任何一步失败，修掉后重跑对应脚本即可

## 快速开始

### 旧电脑（打包）

1. 完全退出 WorkBuddy
2. 双击 `scripts\一键制作迁移包.cmd`，选 `1`（完整迁移包）
3. 完成后得到 `桌面\WorkBuddy-迁移包\` 文件夹

### 搬运

整个文件夹拷到移动硬盘。
**内含 API 密钥等凭证数据，严禁上传公有网盘/微信/邮件。**

### 新电脑（恢复）

1. 安装 WorkBuddy（同版本），登录同一账号（资料库/云记忆/定时任务自动恢复；连接器重新授权一次）
2. 双击迁移包里的 `一键恢复.cmd` —— 自动依次还原 配置层 → 项目层 → 数据层
3. 重启 WorkBuddy，按 `使用说明.txt` / `环境清单.txt` 做手工收尾

## 分步入口（想单独重跑某层时）

| 文件 | 作用 |
|---|---|
| `1-oneclick-restore.cmd` | 配置层：技能 / 长期记忆 / 会话工作区 / .claude / opencode / 配置 / .gitconfig（SSH 私钥按使用说明手工拷） |
| `2-restore-projects.cmd` | 项目层：clone 全部 bundle + 未提交文件 + 数据目录（跑完自动接数据层） |
| `3-restore-wbdata.cmd` | 数据层：会话历史 / 文件修改备份 / blob / 记忆 / 索引 |

## 先看清单再打包（不拷贝任何文件）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\Build-WBMigration.ps1 -DryRun
```

## 常见范围

| 场景 | 做法 |
|---|---|
| 只要技能和设置，项目自己 clone | 打包选 `2`（仅配置层） |
| 数据层太大（修改备份几个 GB） | 打包选 `1` 后单独处理，或 `-SkipWbExtra workspace-sessions` |
| 新电脑没有 D 盘 | 无需处理：项目自动落到第一个数据盘，脚本会提示 |
| 换账号登录 | 无需处理：账号相关数据自动改名到新账号 |

## 目录说明

```
workbuddy-migration/
├── SKILL.md                     技能说明（agent 自动触发用）
├── README.md                    本文件
├── scripts/
│   ├── Build-WBMigration.ps1    打包生成器（自动探测 + 三层分流）
│   └── 一键制作迁移包.cmd        打包入口（带菜单）
└── references/
    ├── migration-layout.md      数据落盘全景图
    └── troubleshooting.md       排障手册
```

## 安全须知

- 迁移包含 API 密钥、各应用令牌：只走移动硬盘/加密 U 盘直拷
- SSH 私钥默认不进包（避免密钥随包扩散）：需要 git SSH 推送时，按使用说明的 icacls 加固步骤手工拷贝 `.ssh`
- 打包前退出 WorkBuddy，否则缺最新数据
- DPAPI 加密的本地凭据（连接器授权等）跨机无效，需重新授权——这是设计使然，不是失败
