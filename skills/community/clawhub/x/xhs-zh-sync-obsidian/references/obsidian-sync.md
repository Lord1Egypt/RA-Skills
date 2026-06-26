# Obsidian 同步选择

本技能支持两种模式：

- `headless-sync`：使用 Obsidian 官方 Sync，通过 `obsidian-headless` 提供的 `ob sync` 命令同步。
- `local-only`：不安装、不初始化 `ob`，只创建一个本地 Obsidian 目录。用户可以自行用 Syncthing、Git、网盘或其它方案同步。

## 首次本地目录

首次运行前必须先问用户 vault 模式：

1. 自动创建本地 vault，并使用官方 Obsidian Sync。
2. 自动创建本地 vault，但只本地导出，不自动同步。
3. 使用当前已有本地 vault 目录。

如果用户选择自动创建，`setup.py --init` 会随机创建本地 Obsidian 存储目录，例如：

```text
~/.local/share/social-favorites-to-obsidian/obsidian-vault-a1b2c3d4
```

如果用户指定目录：

```bash
python scripts/setup.py --init --obsidian-vault /path/to/vault
```

## 只使用自建同步

运行：

```bash
python scripts/setup.py --init --obsidian-mode local-only
```

这种模式下：

- `obsidian.run_ob_sync=false`
- 导出只写入本地目录
- 不执行 `ob sync`
- 用户自行搭建同步

## 使用官方 Obsidian Sync

选择官方 Obsidian Sync 时，先询问用户：

- Obsidian 官方账号邮箱/用户名。
- Obsidian 官方账号密码；如果用户不愿提供，让 `ob login` 交互输入。
- 远程 vault 名字或 ID。
- 端到端加密密码；如果不提供，让 `ob sync-setup` 交互输入。

安装 `obsidian-headless`：

```bash
python scripts/setup.py --install-ob
```

该命令会尝试执行：

```bash
npm install -g obsidian-headless
```

然后初始化官方 Sync：

```bash
ob login
python scripts/setup.py --setup-ob-sync
```

脚本会引导用户输入：

- Obsidian Sync 远程仓库名或 ID
- Obsidian 账号用户名/邮箱，用于用户识别后续 `ob` 交互登录提示
- Obsidian Sync 端到端加密密码，没有则回车让 `ob` 自己交互处理

注意：`setup.py --setup-ob-sync` 不会自动执行 `ob login`，agent 需要在它之前运行 `ob login` 或确认 `ob login` 已完成。

底层使用官方命令：

```bash
ob sync-setup --vault <id-or-name> --path <local-path> [--password <password>] [--device-name <name>] [--config-dir <name>]
```

也可以非交互传参：

```bash
python scripts/setup.py --setup-ob-sync \
  --obsidian-sync-vault "远程仓库名" \
  --obsidian-device-name "social-favorites-to-obsidian"
```

完成后配置会改为：

```yaml
obsidian:
  run_ob_sync: true
  sync:
    mode: "headless-sync"
```

导出流程随后会在写入 Markdown 后执行 `ob sync`。

## 判断是否首次安装

其它 agent 不要凭目录猜测。优先运行：

```bash
python scripts/setup.py --status --json
```

可靠判断规则：

- `first_install=true`：还没完成首次初始化，需要先跑 `setup.py --init`
- `config_exists=true` 且 `state.initialized=true`：已完成首次初始化
- `state.obsidian_mode=local-only`：只使用本地目录，不应要求 `ob`
- `state.ob_sync_configured=true`：官方 Headless Sync 已完成 `ob sync-setup`

状态文件位置：

```text
~/.config/social-favorites-to-obsidian/install_state.json
```
