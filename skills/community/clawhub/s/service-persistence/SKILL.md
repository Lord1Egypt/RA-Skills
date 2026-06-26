---
name: service-persistence
description: >
  macOS 服務持久化與重啟恢復。管理 LaunchAgent、tmux bootstrap、wrapper daemon 三層架構，
  確保電腦重啟後所有服務自動恢復。Use when: (1) 新增需要常駐的服務，(2) 把現有 tmux session 升級成 LaunchAgent，
  (3) 為互動式程式建立 wrapper daemon，(4) 檢查或修復重啟後的服務狀態，
  (5) 更新 service registry（服務名單），(6) 生成或更新 bootstrap/restore script，
  (7) 診斷服務為什麼沒自動起來。
---

# Service Persistence — macOS 服務持久化

## 核心概念

macOS 重啟後 `/tmp` 被清空 → tmux socket 消失 → 所有 tmux session 全滅。
本 skill 用三層架構解決這個問題。

## 檔案結構

```
skills/service-persistence/
├── SKILL.md                              ← 本文件（方法論 + 操作流程）
├── service-registry.json                 ← 本機服務名單（symlink 到 workspace 根目錄）
├── scripts/
│   ├── bootstrap-services.sh             ← 實際在跑的 Tier 2 bootstrap script
│   └── restore-claude-telegram.sh        ← 實際在跑的 Tier 3 wrapper daemon script
└── references/
    ├── registry-spec.md                  ← service-registry.json 格式規格
    ├── launchagent-template.md           ← plist 模板（3 種）
    ├── bootstrap-template.md             ← bootstrap script 通用模板
    └── wrapper-template.md               ← wrapper daemon 通用模板
```

**實際部署位置**：
- script 部署到 `~/.openclaw/scripts/`（LaunchAgent 引用的路徑）
- plist 部署到 `~/Library/LaunchAgents/`
- registry 在 `~/.openclaw/workspace/service-registry.json`

修改 skill 裡的 script 後，必須同步複製到部署位置。

## 三層架構

### Tier 1：LaunchAgent（基礎設施）

**適用條件**（符合任一）：
- 是其他服務的共同依賴（掛了整批失效）
- 不需要互動式終端
- 掛掉必須秒級自動重拉

**特性**：
- `RunAtLoad: true` → 開機自動起
- `KeepAlive: true` → process 掛掉自動重拉
- macOS 有內建 backoff，不會無限每秒重啟

**plist 模板**：見 `references/launchagent-template.md`

### Tier 2：tmux + bootstrap script（應用服務）

**適用條件**：
- 需要保留終端（偶爾 attach 看 log）
- dev server / watch mode
- 不需要 crash 自動重拉（開機恢復即可）

**特性**：
- 統一用 OpenClaw tmux socket：`/tmp/openclaw-tmux/openclaw.sock`
- 一個 bootstrap script 重建所有 session
- 一個 LaunchAgent（`KeepAlive: false`）開機跑一次 bootstrap

**實際 script**：`scripts/bootstrap-services.sh`
**通用模板**：`references/bootstrap-template.md`

### Tier 3：wrapper daemon（永久互動式服務）

**適用條件**：
- 需要 PTY + 可 attach + 人工接手
- 但又太重要不能只靠開機恢復
- 需要 crash 後自動重建

**特性**：
- 常駐 daemon（`KeepAlive: true`），每 N 秒檢查
- 不只檢查 session 存在，還**檢查 pane process**（`zsh`/`bash` = 程式退出了）
- 連續失敗 N 次後 cooldown（避免無限重建）
- 放**預設 tmux socket**（人操作方便）

**實際 script**：`scripts/restore-claude-telegram.sh`
**通用模板**：`references/wrapper-template.md`

#### 🚨 Tier 3 建立 checklist（每次新增都必須逐項確認）

1. **決定 tmux session 名**：固定名稱，之後 wrapper 用這個名字
2. **決定工作目錄**：建立專屬目錄，不要用 `/` 或 `~`
3. **確認正確的啟動指令**：從 `ps aux` 驗證真實指令，不要憑記憶寫
4. **確認 tmux socket**：預設 socket（人操作）還是 OpenClaw socket（agent 管）
5. **第一次手動啟動 + 確認 trust folder**：trust 是 per-directory 一次性的
6. **寫 wrapper script**：從 `references/wrapper-template.md` 改
7. **建 LaunchAgent plist**：`KeepAlive: true`
8. **測試 1：kill session → wrapper 自動重建**
9. **測試 2：kill 程式但 session 殘留 → wrapper 偵測 pane process 是 shell → 自動重建**
10. **更新 service-registry.json**
11. **更新恢復文件**

## tmux socket 分工

| socket | 路徑 | 誰用 | `tmux ls` 看得到 |
|---|---|---|---|
| 預設 | `/tmp/tmux-$(id -u)/default` | 人手動操作 | ✅ |
| OpenClaw | `/tmp/openclaw-tmux/openclaw.sock` | Agent 管理 | ❌ 要加 `-S` |

**原則**：人需要經常 attach 的 → 預設 socket。Agent 管的 → OpenClaw socket。

## Service Registry

**位置**：`~/.openclaw/workspace/service-registry.json`（skill 目錄有 symlink）

這份 JSON 定義這台機器所有需要持久化的服務，包含：

- **machine**：機器名稱、OS、描述
- **proxy_chain**：特殊網路代理設定
- **tunnels**：tunnel provider + 子域名對照
- **services**：每個服務的 tier、type、名稱、port、指令、工作目錄、LaunchAgent label、tmux session name

結構和欄位說明：見 `references/registry-spec.md`

**每次新增 / 移除 / 修改服務，都必須更新這份 registry。**

## 操作流程

### 新增服務

1. 判斷屬於哪個 Tier（見上方適用條件）
2. 在 `service-registry.json` 新增 entry
3. 根據 Tier：
   - Tier 1：從模板生成 plist → 部署到 `~/Library/LaunchAgents/` → `launchctl load`
   - Tier 2：更新 `scripts/bootstrap-services.sh` 加新 session → 複製到部署位置
   - Tier 3：走 Tier 3 建立 checklist（上方 11 步）
4. 測試
5. 更新恢復文件

### 升級服務（例如 tmux → LaunchAgent）

1. 修改 registry 中的 tier 和 type
2. 生成新 plist
3. 從 bootstrap script 移除該 session
4. kill tmux session
5. 部署 plist → `launchctl load`
6. 驗證
7. 更新恢復文件

### 診斷服務沒起來

```bash
# Tier 1
launchctl list | grep <label>
tail -20 ~/.openclaw/logs/<service>.err.log

# Tier 2
tmux -S /tmp/openclaw-tmux/openclaw.sock has-session -t <session>
tmux -S /tmp/openclaw-tmux/openclaw.sock capture-pane -pt <session>:0.0 | tail -20

# Tier 3
launchctl list | grep <wrapper-label>
tail -20 ~/.openclaw/logs/<wrapper>.log
tmux list-panes -t <session> -F '#{pane_current_command}'
# 如果是 zsh/bash = 程式退出了，wrapper 應該會自動重建
# 如果 wrapper 也沒在跑 = LaunchAgent 掛了
```

## 文件同步規則

任何 infra 變更必須同步更新：
1. `service-registry.json`
2. 對應 script（skill 目錄 + 部署位置）
3. `~/.openclaw/RECOVER-SERVICES.md`
4. Obsidian 設計文件

**不更新 = 任務未完成。**

## ⚠️ PATH 陷阱（重要）

LaunchAgent 的預設 PATH 是 `/usr/bin:/bin:/usr/sbin:/sbin`，**不包含**：
- `/opt/homebrew/bin`（brew 安裝的工具）
- `~/.bun/bin`（bun）
- `~/.local/bin`、`~/.cargo/bin` 等用戶級工具

所有 script 的 `export PATH` 必須包含服務依賴的所有 binary 路徑。

**踩坑紀錄（2026-04-09）**：Claude Code Telegram 的 plugin 用 bun 跑，但 wrapper script PATH 沒有 `~/.bun/bin` → plugin 啟動失敗 → Claude 顯示 `Listening` 但實際不收訊息。表面看正常，底層 subprocess 全死。debug log 才看到 `Executable not found in $PATH: "bun"`。

## 已知限制

1. **Tier 2 沒有 crash 自動重拉**：bootstrap 只保護開機恢復
2. **Tier 3 wrapper 無法偵測程式內部狀態**：只看 pane process，不看程式是否正常運作
3. **auth 過期**：需要人工重新登入的服務，wrapper 會 cooldown 但無法自動修復
4. **script 有兩份**：skill 目錄（source of truth）和部署位置（`~/.openclaw/scripts/`），修改後必須同步
5. **plugin subprocess 可能 silent fail**：主程式顯示正常但 plugin 沒起來。需查 debug log 或檢查 subprocess（如 `ps aux | grep bun`）
