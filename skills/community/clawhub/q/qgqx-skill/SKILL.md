---
name: qiguo-strategy-game
description: This skill launches the single-file HTML strategy game 七国群雄传 (Seven Kingdoms Tactics), a 三国群英传-style isometric turn-based wargame. Use it when the user wants to play a browser strategy game, mentions 七国群雄传 / 战棋 / 三国群英传-style web game, or asks to open / play this game. It copies the self-contained HTML into the workspace and opens it directly in the built-in preview so the user can play immediately with zero setup.
metadata:
  agent_created: true
---

# 七国群雄传 · 网页战棋（Seven Kingdoms Tactics）

## Overview

A zero-dependency, single-file HTML5 Canvas strategy wargame in the spirit of 三国群英传 — isometric 3D 战棋, seven-warring-states theme, with combo chains, bond auras, co-op ultimate (合击必杀), and a general codex (武将图鉴). Two modes are bundled, and **each supports two play styles**:

- **人机对战 (vs AI)** — default; you command one side, the computer commands the other.
- **双人轮流 Hotseat（同设备）** — two human players share one device and take turns on the same screen. Chosen on the state-select screen via the 👥 双人轮流（同设备） toggle.
- **联机对战 (Net Play)** — two players on **separate tabs / separate devices** play live. Chosen on the state-select screen via the 🌐 联机对战 toggle. Two transports: 本机多标签 (BroadcastChannel, same browser, zero setup) and 跨设备 (WebSocket relay `net-server.js`, two devices). **Both skirmish and campaign support net play**, host = red/我方, client = blue/敌方 (viewpoint swapped on client).

- **战役模式 (Campaign)** — `campaign-mode.html`: pick a state, conquer cities, recruit generals, and unify the realm. Includes the 武将图鉴 collection system. Hotseat **and 联机** apply to each battle (the strategic map stays single-player setup).
- **普通模式 (Skirmish)** — `skirmish-mode.html`: pick a state + scenario, fast single battle. Hotseat **and 联机** fully supported.

The skill is purely a launcher: it copies the bundled HTML into the current workspace and opens it in the built-in preview panel so the user plays instantly. No server, no build step, no network.

## When To Use

- The user says "玩七国群雄传", "打开战棋游戏", "来一局三国群英传那种游戏", or similar.
- The user references 战棋 / 回合制策略 / 七国群雄传 by name.
- The user wants **two-player / 双人 / 双人对战 / Hotseat / 同设备轮流** — launch either mode and tell them to pick 👥 双人轮流 on the state-select screen.
- The user wants **联机 / 远程双人 / 双设备 / 线上对战 / 一起玩 / 不在一个设备** — launch either mode and tell them to pick 🌐 联机对战, then 创建房间（主机）on one side and 加入房间（客机）with the same room number on the other. Same browser → 本机多标签 (no server); different devices → run `net-server.js` and use 跨设备.
- The user installs the skill and invokes it to play.

## How To Launch (required procedure)

Follow these steps exactly. The game is bundled under `assets/` in this skill's directory.

1. **Resolve the skill directory.** The current skill lives at `~/.workbuddy/skills/qiguo-strategy-game/`. The bundled files are:
   - `assets/campaign-mode.html` — 战役模式
   - `assets/skirmish-mode.html` — 普通模式
   - `net-server.js` — zero-dependency WebSocket relay for 跨设备 联机 (only needed for two-device matches)

2. **Choose which mode to open** based on the user's words:
   - Mentions 战役 / 剧情 / 统一 / campaign / 天下 → `campaign-mode.html`
   - Mentions 普通 / 快速 / 单局 / skirmish / 一局 → `skirmish-mode.html`
   - Mentions 双人 / 双人对战 / Hotseat / 同设备轮流 / 两个人玩 → open either mode (both support Hotseat); tell the user to tap 👥 双人轮流（同设备） on the state-select screen before picking a state.
   - Ambiguous or just "玩这个游戏" → open **both** (present as two files).

   > **Hotseat note:** the 人机 / 双人 toggle lives on the state-select screen (a row reading `对战模式： 🤖 人机对战 · 👥 双人轮流（同设备）`). It is selected *before* choosing a state and applies to the whole battle. In Hotseat, Player 1 commands the blue side and Player 2 the red side; 结束回合 passes control to the other player (not the AI).

3. **Copy the chosen HTML into the current workspace** so the user owns a playable, editable copy. Use the Bash tool:
   ```bash
   mkdir -p "<cwd>/七国群雄传" && cp "<skill_dir>/assets/<file>.html" "<cwd>/七国群雄传/<file>.html"
   ```
   Replace `<cwd>` with the current working directory (from context) and `<skill_dir>` with the resolved skill path. Keep the English filename so the path stays portable.

4. **CRITICAL — open in the built-in preview via present_files.** After copying, call the `present_files` tool with the **absolute path** of the copied HTML file(s). This renders the game directly inside the conversation's preview panel and shows an artifact card.

   - ✅ MUST: `present_files` with the absolute local path, e.g. `C:\Users\...\七国群雄传\campaign-mode.html`
   - ❌ NEVER: only print a `file://...` URL or a relative path and tell the user to open it themselves. The user must be able to play immediately in the preview.

5. **Tell the user, in one short line**, that the game is open in the preview and how to start (choose a state → start battle; in campaign, march from your capital to an adjacent enemy city).

## Game Feature Summary (for describing to the user)

- **连击 Combo**: consecutive friendly hits build a combo counter; at 3+ a 🔥 badge pops; combo ≥5 scales damage up to +30%.
- **羁绊光援 (Bond Aura)**: adjacent friendly units buff each other (ATK +2 / DEF +4), shown as a gold ring under the unit.
- **合击必杀 (Co-op Ultimate)**: when a second different friendly unit hits the same enemy in one turn, a full-screen 合击 triggers with bonus splash damage + screen shake.
- **武将图鉴 (Codex, campaign only)**: every enemy general faced is recorded (defeated / captured / retreated) into `localStorage`; open via the 图鉴 button, shows "collected / total".
- Controls: click a unit → move/attack; 结束回合 (end turn) passes to the other side (AI in 人机 mode, the other human in 双人 Hotseat); terrain, morale, and formation bonuses apply.

## 上手友好 & 留存设计（Player Retention & Virality）

These hooks keep players coming back and help the game spread — mention them when describing the skill:

- **⚡ 快速开始（Quick Start）**: on the state-select screen, a one-tap button picks a random state and jumps straight into a battle / campaign — zero decision friction. The first launch auto-pops the tutorial so new players learn by playing.
- **AI 难度（Difficulty）**: in 人机 mode, choose 😌 简单 / 🙂 普通 / 😈 困难 (scales enemy troops / stats). Welcomes beginners and challenges veterans.
- **📖 玩法说明（Tutorial）**: both battle and strategy screens have a 📖 button that opens a rules cheat-sheet anytime (unit counters, 军师技, net play…).
- **📋 战绩分享（Share Battle Report）**: every end-of-battle banner has 「复制战绩」 — one tap generates a shareable battle-report text, ready to paste into WeChat groups / Moments for social virality.
- **🏆 成就系统 + 📖 武将图鉴（Campaign）**: cumulative wins unlock achievements and collect the realm's famous generals, giving long-term goals and a reason to return.
- **🏆 战绩记录（Best Records）**: per-scenario fastest-clear turns are saved locally and flagged as a new record on the win banner.

## Hotseat 双人轮流（同设备）— how it works

- On the state-select screen, tap **👥 双人轮流（同设备）** (default is 🤖 人机对战). This sets `gameMode='hotseat'`.
- Player 1 = blue side (你/玩家1 · 国名), Player 2 = red side (敌军/玩家2 · 国名). The active side is shown by the turn pill (e.g. `玩家1 · 秦 行动`) and the status bar (`玩家1` / `玩家2` counts, current side's 阵型 and 军师).
- Each side gets its own 阵型 and a random 军师技 per turn (the 阵型 selector and 军师技 dropdown switch to the active side automatically). The 结束回合 button reads `玩家2 结束回合 ▶` when it is Player 2's turn.
- Win banner shows `🏆 玩家1 · 秦 胜利！` / `🏆 玩家2 · 赵 胜利！` so both humans get credit.
- **Campaign caveat:** only the tactical battle is Hotseat; the overland strategy map (choose state, march cities, recruit) remains single-player setup — this is by design, since the map reacts to one player's moves.

## 联机对战 (Net Play) — how it works

On the state-select screen, tap **🌐 联机对战** (default 🤖 人机对战). A room row appears with a room number, a transport toggle (本机多标签 / 跨设备), an optional server box, and 创建房间（主机）/ 加入房间（客机）buttons.

**Two transports**
- **本机多标签 (BroadcastChannel)** — zero setup. Two tabs in the *same browser* join the same room number and play live. No server, no network.
- **跨设备 (WebSocket relay)** — two devices (or two different browsers) join the same room through a tiny zero-dependency relay server. Bundled as `net-server.js` in this skill's directory. Start it with `node net-server.js` (default port 8770) on a machine reachable by both players; both enter `ws://<host-ip>:8770` in the 服务器 box before joining.

**Match flow**
1. Host taps 创建房间（主机）and picks a state (campaign) / state+scenario (skirmish), then starts the battle.
2. Client taps 加入房间（客机）with the **same room number**. The client's 选国 modal closes automatically and a "等待主机开始战斗" overlay shows until the host launches the battle.
3. When the host starts, the full state is pushed to the client; both see the same board. The client's viewpoint is swapped (commands the blue/敌方 side, shown as 我方).

**Rules**
- Host is authoritative: the client only *sends* actions (move / attack / 军师技 / 武将技 / 结束回合); the host rebroadcasts the full state each turn. Latency is negligible at this scale.
- Turn pill reads `🟢 你方回合（红方）` / `⏳ 等待对方（蓝方）` so each side knows when to act.
- A 断线 / 服务器未启动 message appears if the WS relay is unreachable — start `net-server.js` first.

**Note:** in campaign net play, only the tactical battle is networked (host plays the strategy map; the client joins the battle the host launches). This is by design.

## Notes

- Both HTML files are fully self-contained (all CSS/JS inline, no external requests). Safe to open offline.
- If the user wants to tweak the game, they edit their copied file in the workspace — the bundled asset stays untouched.
- To add a new mode or balance change, edit the asset HTML, then re-run this skill's launch procedure.
