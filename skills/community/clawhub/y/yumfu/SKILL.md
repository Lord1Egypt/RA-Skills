---
name: yumfu
description: "Multiplayer text RPG with 10 playable worlds — play together in Telegram groups! Worlds: 笑傲江湖, Harry Potter, Warrior Cats, F15 Down, 龙虾三国, 倚天屠龙记, Game of Thrones, Lord of the Rings, 西游记 (Journey to the West), 战国乱世 (Sengoku Chaos). Each player gets their own character in a shared world with AI art every scene. PvP, team quests, natural language — no commands needed. Use when: /yumfu, group RPG, text adventure, 武侠, 西游记, 孙悟空, LOTR, 指环王, 权力的游戏, 三国, 张无忌, 战国, 织田信长, 丰臣秀吉, 德川家康, 武田信玄."
homepage: https://github.com/yumyumtum/yumfu
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "requires": { "bins": ["uv"] },
        "triggers": ["/yumfu", "/江湖", "笑傲江湖", "华山派", "武当", "Harry Potter", "Hogwarts", "warrior cats", "ThunderClan", "倚天屠龙记", "张无忌", "赵敏", "九阳神功", "明教", "龙虾三国", "三国", "Game of Thrones", "Westeros", "Iron Throne", "Stark", "Lannister", "Targaryen", "权力的游戏", "Lord of the Rings", "LOTR", "Fellowship", "Frodo", "Aragorn", "Gandalf", "指环王", "魔戒", "西游记", "孙悟空", "唐僧", "猪八戒", "牛魔王", "取经", "Journey to the West", "内裤超人", "Captain Underpants", "乔治", "哈罗德", "屎尿教授", "Professor Poopypants", "战国乱世", "战国", "织田信长", "丰臣秀吉", "德川家康", "武田信玄", "新选组", "绯村剑心"]
      }
  }
---

# YumFu 🌍

**Multi-world text adventure RPG with AI art.** Play solo or with friends across 10 universes.

**Start**: `/yumfu start` &nbsp;|&nbsp; **Continue**: `/yumfu continue`

If YumFu is useful to you, you can support future development here:
**Donate via Stripe:** https://buy.stripe.com/8x26oHc329ha6GvaiggjC00

Just talk naturally after starting — no commands needed. Say what you want to do and the story unfolds.

### 🗺️ Worlds

| World | Genre | Status |
|-------|-------|--------|
| ⚔️ 笑傲江湖 | Wuxia / 武侠 | ✅ Ready |
| ⚡ Harry Potter | Magic school | ✅ Ready |
| 🐱 Warrior Cats | Animal clan | ✅ Ready |
| 🛵 F15 Down | Modern military | ✅ NEW |
| 🧙 Lord of the Rings | Epic fantasy | ✅ Playable |
| 🐉 Game of Thrones | Political | 🚧 Soon |
| ⚔️ 倚天屠龙记 | Jin Yong wuxia | 🚧 Soon |
| 🏯 战国乱世 | Sengoku alt-history | ✅ NEW |

### ✨ Features
- 🎨 AI-generated art every scene (world-specific style)
- 🔊 Default per-turn voice narration (can be turned off per save)
- 🗓️ Optional daily world evolution updates (opt-in per player)
- 📖 30+ story branches, 6-8 unique endings per world
- 🧠 NPCs remember your choices
- 💾 Persistent saves across sessions
- 📚 Storybook PDF export of your adventure

---

<!-- ============================================================
     AI AGENT INSTRUCTIONS BELOW — not shown to end users
     ============================================================ -->

## ⚠️ CRITICAL: Always Use This Skill for Game Sessions!

**This is a modern AI MUD — high tolerance, natural language first.**

**If the user is:**
- Playing an ongoing YumFu game (笑傲江湖, Harry Potter, Warrior Cats, F15 Down, etc.)
- Saying anything that sounds like a game action ("I attack", "我去华山", "talk to Hermione", "B", etc.)
- Replying with just a letter/number choice (A/B/C, 1/2/3)

**Just respond and continue the story. No slash commands required.**

**Input tolerance:**
- ✅ "I want to fight" = fight
- ✅ "打他" = fight  
- ✅ "go to the market" = travel
- ✅ "B" = pick option B
- ✅ "what's around me" = look
- ✅ "我要修炼剥龙十八掌" = train that skill
- ✅ Any natural language description of intent

**Only use `/yumfu start` and `/yumfu continue` as entry points. Everything else = natural language.**
- Asking about their character/progress
- Describing game actions ("I want to fight", "去华山派", "explore the forest")

**Then you MUST:**
1. ✅ Load their save file with `load_game.py`
1b. ✅ For **normal gameplay turns**, prefer building hidden turn context via `uv run ~/clawd/skills/yumfu/scripts/build_gameplay_context.py --user-id <id> --universe <world> --player-input "..."`
   - This is the standard helper for aligning a normal turn with save state + world main questline + current story spine
   - It is **backend-only** context; never dump its field names, checklist labels, or helper wording into the player-facing turn
2. ✅ Generate images for **every game turn** (mandatory), with especially strong prompts for location / NPC / combat / chapter moments
3. ✅ In group chats, do **not** downgrade YumFu to text-only mode by default — if the turn generates an image, the image must also be delivered into that same group chat unless the user explicitly disables images
4. ✅ Generate **TTS by default for every gameplay turn** unless the player has explicitly turned TTS off for that save
   - TTS content must be the **player-facing story/narration text only**
   - Do **not** send meta execution chatter, progress updates, or internal action announcements as TTS
5. ✅ Save their progress with `save_game.py`
6. ✅ Use the world's art style and narrative tone
7. ✅ For established canon worlds / existing IPs (especially LOTR, Harry Potter, Game of Thrones, Journey to the West), keep turns tightly anchored to the source world
   - Next moves, targets, battlefields, NPC pressure, travel routes, and quest hooks should preferentially use **real canon geography / factions / characters / warfronts / artifacts** from that setting
   - Do **not** answer with vague generic-fantasy abstractions like “a breach”, “a watchtower”, “the next strongpoint”, or “some captain” when a more source-grounded option exists
   - If the player asks “where can I go / what can I fight / what’s next,” answer with concrete in-world options tied to the current route, e.g. LOTR should lean on places like Mount Gundabad, Moria, Isengard, Cirith Ungol, Minas Tirith, Osgiliath, Pelennor, the Black Gate, etc. when appropriate to the current branch
   - Alternate-perspective branches (for example an orc / Mordor route) are allowed, but they must still respect the original world’s geography, power structure, tone, and ongoing conflict instead of drifting into generic dark-fantasy filler
   - When inventing connective material between canon beats, keep it as a **bridge inside the canon world**, not as a replacement for the world
8. ✅ Keep the **main story / major task / current line** visible during play
   - Every YumFu world must have a recognizable **story spine**: what the larger plot is, what the player is currently trying to do inside it, and what concrete route naturally follows next
   - Do **not** let turns drift into disconnected vibe scenes where the player slowly forgets what the game is about
   - In normal turns, daily evolution, and `/yumfu continue` re-entry, briefly remind the player of the current main line when useful, especially after detours, battles, travel, or offline time
   - Each world should surface its own equivalent of: **main objective / current major task / active pressure / easiest next route**
   - This applies to **every world**, not only canon IPs. Wuxia, school fantasy, animal clan survival, military worlds, and political worlds all need a clear through-line
   - The reminder should be compact and in-world; do not dump homework or a giant lore recap
   - For **every normal gameplay turn**, run a hidden backend check before finalizing the turn:
     1. what larger main line is this save currently inside?
     2. what concrete major task / pressure matters right now?
     3. did this turn actually move, sharpen, complicate, or threaten that line?
     4. does the end of the turn leave the player with a clear next move?
   - If the answer to (3) and (4) is weak, revise the turn so it regains direction before delivery
   - This check is **internal only**; never expose the checklist itself to the player
   - When a turn materially changes the run's direction, update the save-side story spine state via `uv run ~/clawd/skills/yumfu/scripts/story_spine_state.py --set ...` so later turns, daily evolution, and continue/re-entry all stay aligned
9. ✅ Keep all internal scaffolding **invisible to the player**
   - Internal helper ideas such as story spine, active route, default route, pending hooks, recap policy, prompt scaffolding, quest template, or delivery plan are **for backend orchestration only**
   - Never leak raw helper labels, JSON-ish fields, planning bullets, or meta wording like “当前主线模板 / default route / suggested route / pending hook / system recap” into the player-facing message
   - Convert all such internal structure into **natural in-world narration, pressure, dialogue, mission framing, and choices**
   - The player should feel they are inside a living game world, not looking at how the skill is organized
10. ✅ Default to **silent execution** for YumFu operations — do the work, then deliver the finished turn; avoid AI process chatter unless the player explicitly asks for it or something failed

**DO NOT:**
- ❌ Manually roleplay without checking save files
- ❌ Skip image generation for key scenes
- ❌ In group chats, generate the image but fail to actually send it to the group
- ❌ Forget to save progress
- ❌ End a story branch with a simple choice (every choice opens a new path)
- ❌ Design "dead end" options (B is never "game over", it's a different road)
- ❌ Hide the actionable choices inside one long block of prose without a clearly separated options list
- ❌ Fill YumFu turns with AI process chatter, self-narration, or “I am now doing X” filler that weakens the game feel

**This ensures:**
- Consistent character progression
- Visual immersion with AI art
- Data persistence across sessions

---

## 🎭 Deep Narrative Engine (DNE) - MANDATORY

**Read full spec**: `~/clawd/skills/yumfu/DEEP_NARRATIVE_ENGINE.md`

### Core Rules (apply to ALL worlds):

**1. Every choice opens a door, never closes the game**
- Minimum 30 decision nodes per character arc
- Minimum 6 different endings per world
- Option A/B/C all lead to rich story branches

**1b. Choice presentation must be visually clear**
- This rule applies to **all YumFu worlds by default**
- Whenever a turn offers player choices, render them as a separate, easy-to-scan choice block
- Prefer `1 / 2 / 3` for Chinese gameplay and `A / B / C` or `1 / 2 / 3` for English gameplay
- Do **not** bury the choices inside a dense paragraph and expect the player to fish them out
- Keep each option to one short line when possible
- Default output structure for gameplay turns:
  1. short story scene / consequence
  2. one blank line
  3. `你现在可以：` / `Choose your next move:`
  4. separate numbered or lettered options on their own lines
- Default pattern:
  - `1. ...`
  - `2. ...`
  - `3. ...`
- The story paragraph should lead into the decision, then the options should appear on their own lines below it
- The player may still answer naturally in free text; the numbered/lettered options are for readability, not command restriction
- If a turn has an especially obvious next move, still render the options block; do not rely on prose-only implied choices

**2. Three-Arc Story Structure**
```
Arc 1 (20%): Establishment - character, world, first crisis
Arc 2 (60%): Development - conflicts, relationships, moral dilemmas  
Arc 3 (20%): Climax - final choices, multiple endings
```

**3. Hidden Tracking Stats (ALL worlds)**
```json
{
  "reputation": 50,       // affects NPC attitudes
  "moral_alignment": 50,  // 0=dark, 100=light
  "risk_exposure": 0,     // danger level
  "npc_trust": {}         // per-NPC trust values
}
```
Plus 2-4 world-specific stats (e.g., 武功 for 笑傲江湖, magic power for HP)

**4. NPC Memory System**
- NPCs remember player choices
- High trust → share secrets, provide help
- Low trust → may betray, give false info
- Always reference past interactions in dialogue

**5. Consequence Types**
- **Immediate**: scene changes right away
- **Delayed**: triggers 3-5 nodes later (butterfly effect)
- **Cumulative**: multiple similar choices compound
- **Hidden**: player doesn't know until much later

**6. Image Generation - MANDATORY at:**
- New character introduction (portrait)
- Entering new location (scene)
- Major combat moments
- Key emotional turning points
- Story twist moments
- All ending scenes

**6b. Telegram Image+Text Delivery - CRITICAL:**

⚠️ **NEVER send image and story text as two separate messages on Telegram.**
This causes the text to appear AFTER the image and get ignored/folded.

✅ **CORRECT pattern** — put ALL story text in the image `caption`:
```
message(action="send", media="path/to/image.jpg", message="[full story text here]", target=...)
```

✅ **CRITICAL tool rule for YumFu gameplay**:
Use an image generation path that writes a **local file only** and does **not** auto-send media to the chat by itself.
For official YumFu turns, prefer local-file generators such as `scripts/generate_image.py` or an equivalent wrapper that returns only a saved path.

✅ **Image backend fallback order — REQUIRED**:
1. First try local-file generation via `uv run ~/clawd/skills/yumfu/scripts/generate_image.py ...` (always use `uv run`, not plain `python3`, so inline dependencies load correctly)
2. If that fails because `GEMINI_API_KEY` / `GOOGLE_API_KEY` is missing, provider auth is unavailable, the local script errors, or the local runtime/import path is broken, immediately fall back to OpenClaw `image_generate` and then deliver the resulting local media path through the normal YumFu turn-delivery flow
3. In group chats, if either image path succeeds, send that image back into the same group automatically for the current turn
4. If both image paths fail, send the turn as text-only once, explicitly noting that image generation is temporarily unavailable

⚠️ Never silently skip the image step. Either deliver the image, or clearly state that the turn is temporarily running without image support.

❌ Do **not** use any image tool/path that auto-inserts or auto-delivers the generated image into the current chat before the turn delivery logic runs.

❌ **WRONG pattern** — two separate messages:
```
message(action="send", message="story text")   # DON'T
message(action="send", media="path/to/image.jpg")  # DON'T
```

❌ **ALSO WRONG** — send image first, then send image+caption again:
```
message(action="send", media="path/to/image.jpg")
message(action="send", media="path/to/image.jpg", message="story text")
```
This causes the same turn to feel like a duplicate image send.

Telegram caption limit is 1024 chars. If story text exceeds that:
1. Put a short scene summary (~200 chars) as caption
2. Send the full story text as a FOLLOW-UP message immediately after

This ensures the image and story are always visually paired together.

### 6c. Turn Delivery Rule - CRITICAL
For each gameplay turn, enforce a single `turn_id` and delivery state.

**Default implementation path (MANDATORY):**
Use `uv run ~/clawd/skills/yumfu/scripts/deliver_yumfu_turn.py ...` as the default per-turn delivery preparation helper.
This helper is now the standard YumFu path for:
- preparing caption/follow-up text split
- generating local turn image first
- preparing TTS voice bubble output
- carrying per-turn delivery state
- deciding whether OpenClaw image fallback is needed

For Telegram/group gameplay, do not hand-roll turn delivery if this helper can be used.

Hard limits per turn:
- **main_text_sent**: at most once
- **image_sent**: at most once
- **tts_sent**: at most once
- **Never send a standalone image first if you still intend to send image+caption for the same turn later**

Preferred delivery order:
1. Run `deliver_yumfu_turn.py` to prepare assets/state for the turn
2. Try image+caption as the main message
3. If local image generation fails and the helper marks fallback required, use OpenClaw `image_generate` and continue the same turn delivery flow
4. If image generation times out or both image paths fail, send text-only once as the main story message
5. If the delayed image later arrives, send image-only once as a fallback visual add-on
6. TTS follows the main story message; never jumps ahead of the story
7. Never generate/send TTS for assistant-side execution chatter such as “我来继续这回合”, “我现在发图文和语音”, “我把存档补上” — these are meta updates, not gameplay content

Fallback sequencing rule:
- If a turn needs two sends because image generation was slow, the order must be:
  **text first → delayed image later**
- Never do:
  **image first → image+caption later**
- If text has already been sent for a turn, the delayed image must stay image-only (or ultra-short visual note), not a second full story delivery.

**7. World-Specific Art Styles**
- 笑傲江湖: Chinese ink painting, classical wuxia illustration
- Harry Potter: British fantasy illustration style
- Warrior Cats: Animal illustration, forest scenes
- F15 Down: Command & Conquer RTS game aesthetic
- LOTR: Epic fantasy, oil painting style
- 倚天屠龙记: Chinese ink painting, dramatic lighting

**8. Random Events (every 3-5 nodes)**
Trigger one of: Encounter / Crisis / Discovery / Opportunity / Echo (delayed consequence)

---

---

## 🤖 AI Agent Instructions (READ FIRST!)

**CRITICAL Save/Load Rules:**
1. **ALWAYS use unified scripts** for save/load operations:
   - Load: `~/clawd/skills/yumfu/scripts/load_game.py`
   - Save: `~/clawd/skills/yumfu/scripts/save_game.py`
2. **NEVER manually construct save file paths or JSON format**
3. **Auto-detect new users** - Check save existence before every command
4. **Quick reference**: `~/clawd/skills/yumfu/scripts/SAVE_LOAD_REFERENCE.md`

**See detailed instructions in "💾 Save File Management" section below.**

---

### ✅ **Available Now:**
- ⚔️ **Xiaoao Jianghu** (笑傲江湖) - Jin Yong wuxia classic
- ⚡ **Harry Potter** - Hogwarts, magic, wizarding duels
- 🐱 **Warrior Cats** - Clan life, forest territories, warrior code
- 🛵 **F15 Down: Azure Peninsula War** - Modern military strategy, 14 frontline roles, C&C aesthetic
- 🦞 **龙虾三国** - Three Kingdoms era, 5 roles, weapons/mounts/ultimate skills
- 🗡️ **倚天屠龙记** - The Heaven Sword & Dragon Saber, 4 romance routes, 6 endings
- 🐉 **Game of Thrones** - Seven Kingdoms, 7 houses, play as Jon/Dany/Tyrion/Arya/Cersei
- 🏯 **战国乱世** - 日本战国架空沙盒，含信长/秀吉/家康/武田、朝鲜名将、明朝名臣、南蛮火器技师、名妓与密探

### 🚧 **Coming Soon (Roadmap):**
- 🧙 **Lord of the Rings** - Middle-earth, 5 races, Ring corruption system, play as Frodo/Aragorn/Gandalf
- 🐒 **西游记** - Journey to the West: 9 factions, play as gods/demons/pilgrims
- 🩲 **内裤超人** - Captain Underpants: 搞怪漫画RPG，屁声震天
- 🏹 **射雕英雄传** - Legend of the Condor Heroes *(coming soon)*

---

## 🌐 Language & World Selection | 语言与世界选择

**First time?** Start with language selection:
```
/yumfu start
```

You'll see / 你会看到:
```
🌍 Welcome to YumFu! | 欢迎来到YumFu！

1. 中文 (Chinese) - 武侠世界
2. English - Fantasy Realms

Reply: /yumfu lang <1|2>
```

Then choose your world / 然后选择世界:

**After world + character setup, ask one more onboarding question (MANDATORY):**

**This is a unified YumFu rule across worlds, not a one-off reminder.**
Daily evolution is always optional, but the system should proactively ask during `/yumfu start` so the player does not need to remember to enable it later.

```text
Do you want this world to evolve automatically every day, even when you're offline?

1. Yes — send me one daily world update with art
2. No — only progress when I play
```

If the player says **Yes**, enable **Daily Evolution Mode** for that save.
If the player says **No**, keep the default manual-only mode.

**中文 (Available Now):**
- **笑傲江湖** (Xiaoao Jianghu) - 华山派、武当、少林、江湖恩怨
- **战国乱世** (Sengoku Chaos) - 日本战国架空乱世、火枪火炮、名将名臣、花街权谋

**战国乱世专用 start 路径（MANDATORY when selected）**
If the player chooses `战国乱世` / `Sengoku Chaos` during `/yumfu start`, route the setup through:
```bash
python3 ~/clawd/skills/yumfu/scripts/start_sengoku_game.py \
  --user-id {user_id} \
  --name {player_name} \
  --role {selected_role_id} \
  --faction {selected_faction_id} \
  --scenario {selected_scenario_id} \
  --language {zh|en} \
  --daily-evolution {yes|no} \
  --target {chat_id}
```
Then:
1. generate exactly one opening image from `rendered_opening.image_prompt`
2. send `rendered_opening.player_opening_message` with that image as the first playable opening scene
3. let the player answer with one of the rendered first-turn choices

**English (Available Now):**
- **Harry Potter** - Hogwarts houses, magic, wizarding adventures
- **Warrior Cats** - ThunderClan, RiverClan, forest territories

**Coming Soon:** LOTR, Game of Thrones, The Witcher, 倚天屠龙记, 射雕英雄传

---

## 🎮 核心特色 | Core Features

- ⚔️ **多人在线** - 在群聊中 @我 即可加入江湖
- 🤝 **组队冒险** - 最多5人组队，共享经验和战利品
- 💥 **PvP 切磋** - 友谊切磋或生死决斗
- 🌐 **共享世界** - 击杀 NPC、抢夺秘籍会影响所有玩家
- 🎨 **水墨风配图** - 每个场景自动生成水墨画风图片
- 📊 **实时排行榜** - 等级、善恶值、财富榜

---

## 触发指令

所有指令以 `/yumfu` 或 `/江湖` 开头

### 🌐 Language Support | 双语支持

**All commands support both English and Chinese aliases:**

| English | 中文 | Action |
|---------|------|--------|
| `/yumfu start` | `/yumfu 开始` | Start new game / 开始新游戏 |
| `/yumfu continue` | `/yumfu 继续` | Continue saved game / 继续游戏 |
| `/yumfu status` | `/yumfu 状态` | Show character stats / 显示状态 |
| `/yumfu help` | `/yumfu 帮助` | Show all commands / 显示帮助 |
| `/yumfu go <place>` | `/yumfu 去 <地点>` | Travel to location / 前往某地 |
| `/yumfu look` | `/yumfu 看` | Look around / 查看四周 |
| `/yumfu map` | `/yumfu 地图` | Show map / 显示地图 |
| `/yumfu fight <target>` | `/yumfu 战 <对手>` | Start combat / 发起战斗 |
| `/yumfu train <skill>` | `/yumfu 练 <功法>` | Train skill / 修炼武功 |

**Use the language that matches your selected world!**

---

### 游戏管理
- `/yumfu start` 或 `/yumfu 开始` — 开始新游戏（创建角色）
- `/yumfu continue` 或 `/yumfu 继续` — 继续已保存的游戏
- `/yumfu save` — 保存当前游戏状态
- `/yumfu status` 或 `/yumfu 状态` — 显示角色属性、物品、位置
- `/yumfu help` 或 `/yumfu 帮助` — 显示所有指令

**🚨 First-time users:** If you try any command and see "Welcome! You don't have a character yet", use `/yumfu start` to create your character first. The system will auto-detect this and guide you!

#### 📋 `/yumfu continue` Workflow (详细流程)

**Before resuming active play, also check whether a daily evolution sidecar exists:**
```bash
python3 ~/clawd/skills/yumfu/scripts/build_reentry_context.py \
  --user-id {user_id} \
  --universe {selected_world}
```

Then prepare the actual continue-time delivery bundle:
```bash
python3 ~/clawd/skills/yumfu/scripts/prepare_continue_reentry_delivery.py \
  --user-id {user_id} \
  --universe {selected_world} \
  --target {chat_id}
```

If a sidecar exists:
- Use the latest daily evolution summary as a **short re-entry scene hook**
- Surface only the most relevant pending hook(s)
- Respect the save's canonical language first; do **not** let old sidecar English/Chinese drift override `save.language` unless the player explicitly switched play language
- **Continue/reentry is image-first and mandatory image+text**
- If a recent save-matched image exists, reuse it
- If no recent save-matched image exists, **generate a fresh image before sending**
- Do **not** send continue reminders as text-only unless image generation failed and there is absolutely no recovery path
- Do **not** dump the whole evolution history
- Make it easy for the player to continue with one short reply


**When user says `/yumfu continue`:**

**Step 1: Check for existing saves**
```bash
python3 ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id {user_id} \
  --check-all \
  --pretty
```

**Step 2: Parse results**
- If **0 saves found** → Guide user to `/yumfu start`
- If **1 save found** → Auto-load that world
- If **2+ saves found** → List all saves and ask user to choose

**Step 3: Display saves (if multiple)**
Example output:
```
🎮 You have 3 saved games:

1. 🗡️ 笑傲江湖 - 小虾米 (Lv.3)
   📍 Location: 华山派·思过崖
   🕐 Last played: 2 days ago

2. 🪄 Harry Potter - Tom Brady (Lv.5)
   📍 Location: Gryffindor Common Room
   🕐 Last played: 1 hour ago

3. 🐱 Warrior Cats - Tumpaw (Lv.2)
   📍 Location: ThunderClan Camp
   🕐 Last played: 3 days ago

Which adventure do you want to continue?
Reply: 1, 2, 3, or world name (xiaoao/harry/warrior)
```

**Step 4: Load selected world**
```bash
python3 ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id {user_id} \
  --universe {selected_world} \
  --pretty
```

**Step 5: Resume gameplay**
Continue from their last location with a recap:
```
欢迎回来，小虾米！

你站在华山派思过崖边缘，冷风呼啸。上次你刚从山洞中获得了一本破旧的剑谱...

[内力] 250/300  [体力] 180/200
[装备] 长剑（品质：普通）
[任务] 破解剑谱秘密 (进度: 30%)

你打算做什么？
```

### 移动与探索
- `/yumfu go <地点>` 或 `/yumfu 去 <地点>` — 前往某地
- `/yumfu look` 或 `/yumfu 看` — 查看当前位置
- `/yumfu map` 或 `/yumfu 地图` — 显示已知地点

### 战斗
- `/yumfu fight <目标>` 或 `/yumfu 战 <对手>` — 发起战斗
- `/yumfu attack <招式>` 或 `/yumfu 攻 <招式>` — 战斗中使用特定招式
- `/yumfu defend` 或 `/yumfu 守` — 防御姿态
- `/yumfu flee` 或 `/yumfu 逃` — 尝试逃跑

### 修炼与技能
- `/yumfu train <功法>` 或 `/yumfu 练 <功法>` — 修炼武功
- `/yumfu meditate` 或 `/yumfu 打坐` — 恢复体力/内力，有机会顿悟
- `/yumfu skills` 或 `/yumfu 武功` — 列出已学武功和等级

### 社交
- `/yumfu talk <NPC>` 或 `/yumfu 对话 <人物>` — 与NPC对话
- `/yumfu join <门派>` 或 `/yumfu 拜入 <门派>` — 加入武林门派
- `/yumfu reputation` 或 `/yumfu 名望` — 查看各门派声望

### 物品
- `/yumfu inventory` 或 `/yumfu 背包` — 显示背包
- `/yumfu use <物品>` 或 `/yumfu 用 <物品>` — 使用物品
- `/yumfu buy <物品>` 或 `/yumfu 买 <物品>` — 从当前商店购买
- `/yumfu sell <物品>` 或 `/yumfu 卖 <物品>` — 向当前商店出售

---

## 🤝 多人指令（新增）

### 组队系统
- `/yumfu team create <队名>` — 创建队伍
- `/yumfu team invite @用户` — 邀请队友
- `/yumfu team join <队名>` — 加入队伍
- `/yumfu team leave` — 离队
- `/yumfu team status` — 查看队伍状态
- `/yumfu team list` — 列出所有队伍

### PvP 切磋
- `/yumfu duel @用户` — 友谊切磋（点到为止）
- `/yumfu duel @用户 --death-match` — 生死决斗（战至一方HP=0）
- `/yumfu watch` — 观战当前战斗

### 江湖信息
- `/yumfu world` — 查看世界状态（NPC位置、门派控制）
- `/yumfu events` — 查看今日江湖大事
- `/yumfu leaderboard` — 查看排行榜
- `/yumfu players` — 查看在线玩家

---

## 🌐 多人机制

### 共享世界
- **NPC 唯一性** - 洪七公只有一个，被杀后所有玩家都看到"已死"
- **秘籍争夺** - 九阴真经只有一本，先得者得，其他人需抢夺
- **门派战争** - 多人加入不同门派可攻城略地
- **世界事件** - 所有玩家行为记录到事件日志

### 组队机制
- **人数限制** - 最多5人
- **善恶限制** - 善恶值差>50 无法组队（正邪难两立）
- **门派限制** - 敌对门派无法组队
- **经验分配** - 按战斗贡献分配
- **战利品** - 队长分配或投骰

### PvP 机制

**友谊切磋**（默认）:
- HP 降至 20% 自动停止
- 不影响善恶值
- 胜者获得经验

**生死决斗**:
- 战至一方 HP = 0
- 败者掉落装备/秘籍
- 杀人者善恶值 -20
- 需要双方同意

### 相互影响

**1. NPC 击杀**
- 玩家A杀了洪七公 → 世界状态更新
- 玩家B去找洪七公 → "洪七公已被玩家A所杀"
- 江湖通缉：杀人者善恶值-50，各大门派追杀

**2. 门派争霸**
- 多个玩家加入不同门派
- 可攻占城市（如：魔教攻占洛阳）
- 影响所有玩家的任务和交易

**3. 秘籍争夺**
- 九阴真经只有一本（首先获得者拥有）
- 其他玩家想要？抢！或者拜师学习
- 可交易、可掉落

**4. 声望系统**
- **武林至尊榜** - 等级排行
- **善恶榜** - 善恶值排行
- **财富榜** - 银两排行
- 实时更新，所有玩家可见

---

## 游戏设计

### 世界观
金庸、古龙经典武侠世界：
- 金庸、古龙小说中的经典地点
- 著名人物作为NPC（部分友善，部分敌对）
- 多条故事线和任务
- **共享世界状态** - 所有玩家影响同一个江湖

### 角色系统
- **属性**: 体力(HP)、内力(MP)、攻击、防御、速度、悟性
- **武功**: 向高手学习、寻找秘籍、打坐顿悟
- **门派**: 少林、武当、峨嵋、丐帮、明教、古墓派、华山、全真教、日月神教、独行侠(无门派)
- **善恶值**: 影响NPC互动、可接任务、结局、组队限制
- **等级**: 1-100，称号（无名小卒 → 江湖新秀 → 一流高手 → 绝世高手 → 武林至尊）

### 战斗系统
- 回合制，先手基于速度
- 每种武功有独特招式和效果
- 内力驱动特殊招式
- 装备影响属性
- Boss战需要策略
- **PvP 战斗** - 玩家间切磋/决斗

### 成长系统
- 修炼武功提升等级
- 寻找秘籍（九阴真经、九阳神功、独孤九剑等）
- 完成任务获得奖励
- 积累门派声望
- 解锁传世神兵
- **组队经验加成** - 组队战斗获得额外经验

---

## 技术实现

### 多人存档系统
```
memory/yumfu/
├── world-state.json          # 共享世界状态（NPC、秘籍、门派控制）
├── saves/
│   ├── xiaoao/               # 笑傲江湖存档目录
│   │   ├── user-123456789.json
│   │   └── user-2345678901.json
│   ├── harry-potter/         # Harry Potter存档目录
│   │   └── user-123456789.json
│   └── warrior-cats/         # Warrior Cats存档目录
│       └── user-123456789.json
├── teams/
│   └── team-华山论剑.json     # 临时队伍状态
└── events/
    └── 2026-04-01.json        # 今日江湖大事
```

**Note:** Each world uses a separate subfolder to prevent save conflicts.

### 世界状态（world-state.json）
```json
{
  "version": 1,
  "game_time": { "year": "南宋", "season": "春", "day": 1 },
  "npcs": {
    "洪七公": {
      "location": "洛阳",
      "hp": 1000,
      "status": "alive",
      "reputation": {
        "user-123456789": 50,
        "user-2345678901": -20
      },
      "killed_by": null
    }
  },
  "world_events": [...],
  "faction_control": { "洛阳": "丐帮" },
  "rare_items": {
    "九阴真经": { "owner": "user-123456789", "status": "owned" }
  },
  "leaderboards": {
    "level": [...],
    "morality": [...],
    "wealth": [...]
  }
}
```

### 玩家存档（user-{id}.json）
```json
{
  "version": 2,
  "user_id": "123456789",
  "language": "zh",
  "universe": "xiaoao",
  "character": { "name": "大红虾🦐", "level": 1, ... },
  "location": "洛阳城",
  "inventory": [...],
  "skills": [...],
  "quests": [...],
  "team_id": null,
  "in_combat_with": null,
  "tts": {
    "enabled": true,
    "provider": "edge-tts",
    "delivery": "voice-bubble",
    "language_voices": {
      "zh": "zh-CN-XiaoxiaoNeural",
      "en": "en-GB-SoniaNeural"
    },
    "current_voice": "zh-CN-XiaoxiaoNeural",
    "last_language": "zh",
    "switch_policy": "keep same voice for same language within one save unless user explicitly asks to change"
  },
  "daily_evolution": {
    "enabled": false,
    "cadence": "daily",
    "channel": "telegram",
    "last_tick_at": null,
    "next_tick_at": null,
    "cron_id": null,
    "last_summary": null
  }
}
```

**Important:** Save path is `~/clawd/memory/yumfu/saves/{universe}/user-{id}.json`

### 💾 Save File Management (Agent Instructions)

**CRITICAL:** Persist game state after every significant action to prevent data loss!

#### When to Save:
1. **Character creation** - 🚨 **IMMEDIATE save after name/faction selection** (HIGHEST PRIORITY)
2. **Daily evolution preference** - Save immediately after player answers Yes/No
3. **TTS preference or voice change** - Save immediately after player turns TTS on/off or explicitly changes voice
4. **Training completion** - New skill learned
5. **Combat end** - HP/stats changed
6. **Quest milestone** - Progress updated
7. **Location change** - Player moved
8. **Inventory change** - Item gained/used
9. **Daily evolution tick** - After each offline world update is generated and delivered

**🚨 CRITICAL: Character creation MUST save immediately before any other actions!**

#### 🛠️ Unified Save/Load Scripts (USE THESE!)

**DO NOT manually construct save logic.** Use the standard scripts to avoid format errors:

##### 📥 Load Game
```bash
# Load specific user's save
uv run ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id 1309815719 \
  --universe xiaoao \
  --quiet

# Check all worlds for a user
uv run ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id 1309815719 \
  --check-all
```

**Output (JSON):**
```json
{
  "exists": true,
  "data": { "character": {...}, "location": "...", ... },
  "character_name": "小虾米",
  "level": 1,
  "location": "洛阳城·同福客栈门口",
  "save_path": "/Users/tommy/clawd/memory/yumfu/saves/xiaoao/user-1309815719.json"
}
```

##### 💾 Save Game
```bash
# Save from JSON string
uv run ~/clawd/skills/yumfu/scripts/save_game.py \
  --user-id 1309815719 \
  --universe xiaoao \
  --data '{"character": {"name": "小虾米", "level": 2, ...}, "location": "华山派"}'

# Or pipe JSON (preferred for large saves)
echo '{"character": {...}}' | \
  uv run ~/clawd/skills/yumfu/scripts/save_game.py \
    --user-id 1309815719 \
    --universe xiaoao
```

**Output:**
```
✅ Game saved successfully!
📁 Path: /Users/tommy/clawd/memory/yumfu/saves/xiaoao/user-1309815719.json
💾 Backup: /Users/tommy/clawd/memory/yumfu/backups/user-1309815719-xiaoao-20260404-101234.json
👤 Character: 小虾米 (Lv.2)
```

#### Agent Workflow (Recommended)

```python
import json

# 1. Load existing save (or detect new user)
# Note: user_id should be validated/sanitized by OpenClaw before reaching this point
result = exec({
    "command": f"uv run ~/clawd/skills/yumfu/scripts/load_game.py --user-id {user_id} --universe {universe} --quiet"
})
save_data = json.loads(result.stdout)

if not save_data["exists"]:
    # New user - guide to character creation
    return "Welcome! Use /yumfu start to create your character."

# 2. Modify game state
save_data["data"]["character"]["hp"] -= 15
save_data["data"]["location"] = "华山派·练武场"

# 3. Save back using stdin (avoids command injection)
save_json = json.dumps(save_data["data"])
result = exec({
    "command": f"uv run ~/clawd/skills/yumfu/scripts/save_game.py --user-id {user_id} --universe {universe}"
})
# Pass JSON via stdin to avoid shell escaping issues
process.write({"sessionId": result.sessionId, "data": save_json, "eof": True})
```

#### Error Recovery:
- Scripts automatically create backups before overwriting
- If save fails: Scripts will attempt emergency save to `/tmp/`
- **Never silently fail** - player must know their progress may be lost
- Check script exit code: `0` = success, `1` = failure

### 队伍状态（team-{name}.json）
```json
{
  "team_name": "华山论剑",
  "created": "2026-04-01T22:00:00",
  "leader": "user-123456789",
  "members": [
    { "user_id": "123456789", "name": "大红虾🦐", "hp": 90 },
    { "user_id": "2345678901", "name": "小龙虾", "hp": 100 }
  ],
  "exp_share": true,
  "loot_mode": "leader"
}
```

### 游戏引擎
Agent **就是**游戏引擎：

#### 🚨 **Step 0: Auto-Detect Save File (MANDATORY)**
**EVERY command (except `/yumfu start` and `/yumfu help`) MUST start with this check:**

```python
import os
import json

def check_or_create_save(user_id, universe="xiaoao"):
    """Auto-detect save file. If missing, guide user to create character."""
    save_path = os.path.expanduser(f"~/clawd/memory/yumfu/saves/{universe}/user-{user_id}.json")
    
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            return (True, json.load(f))
    else:
        return (False, None)

# Usage at START of every command handler:
user_id = message_context.get("sender_id") or message_context.get("user_id")
has_save, save_data = check_or_create_save(user_id)

if not has_save:
    return """🌍 Welcome to YumFu! You don't have a character yet.

Let's create one! Use: /yumfu start

Available worlds:
⚔️ Xiaoao Jianghu (笑傲江湖)
⚡ Harry Potter
🐱 Warrior Cats"""
```

**This prevents "no save found" errors and auto-guides new players.**

#### Main Engine Flow:
1. **识别玩家** - 从 Telegram ID 加载对应存档（Step 0自动处理）
2. **读取世界状态** - `world-state.json`
3. **处理玩家指令** - 修炼、战斗、组队、PvP
4. **生成武侠文风剧情** - 中文叙述
5. **计算结果** - 战斗/修炼/骰子系统
6. **更新世界状态** - 影响所有玩家
7. **记录事件** - 写入今日事件日志
8. **生成配图** - 水墨风场景图
9. **保存状态** - 更新玩家存档和世界状态

#### 🗓️ Daily Evolution Mode (NEW)

**Purpose:** keep the world moving even when the player is offline, so they receive one short daily update with fresh context, image, and meaningful pressure to come back.

### Product decision
Use a **unified YumFu framework** for this feature, but make the **actual evolution content dynamic at runtime**.

**Fixed / shared across YumFu:**
- onboarding question at character creation
- opt-in/opt-out toggle stored in sidecar state
- daily cron / scheduled turn per player save
- one daily Telegram update message with image
- sidecar update after each evolution tick
- anti-spam rule: max 1 evolution update per day per save
- save mutation boundaries and safety rules

**Dynamic at runtime (NOT hardcoded event scripts):**
- read the player's current save first
- read their chosen world, role, faction, current quest state, location, known NPCs, recent flags, and inventory
- infer what the surrounding world would plausibly do next
- generate one in-world update using AI reasoning grounded in that save + world background
- optionally mutate relevant save fields to reflect the consequences

### Core design principle
**Do not hardcode daily story content unless absolutely necessary.**

This feature should feel like a living world, not a rotating calendar of canned events.
The best approach is:
- **hardcode the engine and guardrails**
- **generate the content dynamically from the save + world lore**

### Why this is better
- Different players in the same world may have different roles, alliances, enemies, and unfinished quests
- A static event table would quickly feel fake or contradictory
- Dynamic generation lets the world react to the player’s actual position in the story
- This is especially important for worlds like **Game of Thrones**, where faction alignment and covert relationships matter

### Daily Evolution onboarding rule
During `/yumfu start`, after world choice and initial character setup, ask:
- Do you want daily world evolution updates? Yes / No
- Default should be **No** unless the player explicitly opts in

**Exact onboarding flow for any world:**
1. Ask the player the Yes/No question after character setup
2. Pass the result into:
```bash
python3 ~/clawd/skills/yumfu/scripts/handle_daily_evolution_choice.py \
  --user-id {user_id} \
  --universe {selected_world} \
  --target {chat_id} \
  --choice yes|no \
  --channel telegram \
  --time 10:00 \
  --tz America/Los_Angeles
```
3. Use the returned `message_zh` / `message_en` as the short confirmation to the player
4. Do **not** send a separate technical report

This is world-agnostic. Any YumFu world should use the same post-start activation flow.

If the player later disables it:
- use `~/clawd/skills/yumfu/scripts/disable_daily_evolution_cron.py`
- keep old sidecar history unless the user explicitly asks to erase it

### Runtime input for each evolution tick
Before generating the update, load and consider:
- current save JSON
- selected world / universe
- player role, faction, loyalty, reputation, party/team
- active quests and unresolved hooks
- current location and nearby regions
- known NPCs and relationship values
- recent flags, injuries, resources, inventory, travel state
- any previous daily evolution summaries

### Daily Evolution output requirements
Each daily evolution update should include:
1. **1 short front-context recap** (1-3 sentences) reminding the player why they are here, what line/faction/quest they are already tied to, and why today's scene matters
2. **1 short story update** (100-220 words)
3. **1 generated image** showing the new situation, with prompt continuity from the current arc instead of a context-free fresh scene
   - YumFu-generated images should include the **YumFu logo stamped in a corner** after generation (do not rely on the model to hallucinate the logo)
4. **1 meaningful state change** (rumor, faction shift, patrol increase, resource loss, NPC movement, political signal, etc.)
5. **1 hook** that invites the player back into active play
6. **1 TTS voice-bubble delivery by default** unless that save has explicitly disabled TTS
7. **1 practical route suggestion block** grounded in the save, not generic advice. This should name the most relevant scene / person / faction / object / danger line to follow next.
8. **1 default route** that the story will assume if the player does nothing for a while, so the plot still advances instead of freezing.

The recap is mandatory. Do not assume the player remembers yesterday's update, the hidden faction line, or why the current image matters.

### Daily Evolution delivery rule (MANDATORY)
Daily evolution is not text-only. If a daily evolution update is delivered to the player, the default delivery bundle is:
1. image + recap-aware main story text
2. follow-up TTS voice bubble for the same update using that same recap-aware text

The player-facing text should normally read like:
- short recap / 前情
- today's world movement
- one easy re-entry hook

Rules:
- If `save.tts.enabled != false`, generate and send TTS for daily evolution too.
- Use the same stable per-save language/voice continuity rules as normal gameplay turns.
- On channels that support it, send TTS as a **voice bubble** (`message(..., asVoice=true)`).
- The TTS must follow the main image/text update, not precede it.
- Do not silently drop TTS just because this is an offline daily evolution tick.
- Only skip TTS when:
  - the save explicitly disabled TTS, or
  - TTS generation failed after an honest attempt.
- If TTS fails, still send the image/text update, but treat the missing TTS as a delivery gap to be fixed rather than intended behavior.

### Re-entry design principle (VERY IMPORTANT)
The core goal is **not** to generate a long lore report.
The core goal is to **pull the player back into the current scene naturally and easily**.

For daily evolution pushes, that re-entry starts immediately with a short recap. If the update opens cold, the player forgets the plot and the image loses meaning.

That recap should usually answer 3 things in compact form:
1. **What larger main line is this run inside?**
2. **What major task / pressure is on the player right now?**
3. **What is the easiest concrete next route back into play?**

But those answers must be rendered as **story**, not as backend labels. The player should feel scene pressure and purpose, not see the scaffolding behind it.

Daily evolution should feel like:
- “while you were away, something moved”
- “here is the new pressure/context”
- “here is the easiest natural next move if you want to continue now”
- “if you do nothing, here is the road the story is most likely to take next”

It should **not** feel like:
- a long news bulletin
- a disconnected worldbuilding dump
- a giant state report the player has to study before playing
- a pretty atmospheric scene that forgot the actual plot

### Practical writing rule
Every daily evolution update should end with a **simple re-entry hook** the player can answer naturally.
Good examples:
- “A rider is already waiting at the inn. Do you speak to him?”
- “The red-sealed note is now in another pair of hands. Do you follow?”
- “Your rival sect moved first. Do you intercept or stay hidden?”

Bad examples:
- “Here are 8 things that changed in the world today...”
- “System update: faction matrix +3/-2...”
- anything that makes the player do homework before playing

### Continuation UX rule
The update should make it easy for the player to resume with a short natural reply.
Ideally the player should be able to continue by replying with:
- one short sentence
- one choice
- one action verb
- or even just a letter option

This feature exists to increase re-engagement, not to increase reading burden.

### Language continuity rule (MANDATORY)
Daily evolution updates should respect the player's established language, instead of switching arbitrarily.

### TTS continuity rule (MANDATORY)
Gameplay TTS is **enabled by default** for each save unless the player explicitly turns it off.

TTS rules:
1. Use **voice-bubble delivery** when the channel supports it.
2. Choose a voice that matches the active gameplay language:
   - Chinese gameplay → use a fitting Chinese voice
   - English gameplay → use a fitting English voice
3. Keep the **same voice for the same language within the same save**.
4. If the player switches gameplay language, it is acceptable to switch to the corresponding language voice.
5. Do **not** randomly change voices mid-campaign for the same language.
6. Only change voice within the same language if the player explicitly asks to change it.
7. Persist this state in `save.tts`.

Supporting scripts:
- `scripts/resolve_tts_voice.py` — resolve stable per-save TTS settings and language-matched voices
- `scripts/generate_turn_tts.py` — generate one gameplay-turn TTS file using the save's stable current voice

Use this priority order:
1. `save.language` if present (**canonical per save**)
2. **The player's recent actual conversation language** only as an advisory / explicit-switch signal
3. the world's default language
4. channel/system default only as a last fallback

Examples:
- If a player created or has been preserving a save in Chinese, keep continue reminders / daily evolution in Chinese unless the player clearly asks or consistently switches active play into English.
- If a player has consistently been playing the world in English, keep daily evolution in English.
- Do not randomly alternate between Chinese and English from day to day.
- Do not let old sidecar text silently drag the save into another language.

The daily update should feel like a natural continuation of how the player has already been playing.
### Daily Evolution severity model
Most days should be **light but meaningful**:
- 60% minor movement (rumor, patrols, sightings, small supply shift)
- 30% medium movement (faction pressure, new NPC action, failed delivery, local conflict)
- 10% major movement (death, betrayal, breakthrough, exposed route, stolen relic, siege step, etc.)

Major movement should be rare, but possible, so the world feels alive.

### Weekly advancement rule (NEW)
Daily evolution may stay light on many days, but **at least once per 7 days of real time** the player should receive a more substantive advancement signal tied to the current arc.

That weekly advancement should usually include at least one of:
- a named NPC making a move
- a faction line becoming clearer
- a concrete item / document / resource / clue entering play
- a route becoming newly viable or newly dangerous
- a stronger recommendation about which line the player should pick up next

Implementation expectation:
- track `last_major_advancement_at` in the evolution sidecar
- if ~7 days pass without a substantive push, generate the next update in `advancement_level=major`
- major weekly advancement should remain compatible with the save, but must feel more playable and more legible than a normal atmospheric nudge

The goal is to avoid the feeling that the game only emits atmospheric nudges forever. Even when the player is absent, the world should occasionally become more legible and more playable.

### Save safety rule (IMPORTANT)
If there is meaningful risk of corrupting or derailing the player's real save, **do not mutate the main player save at all**.

Preferred design for MVP:
- keep the player's main save as the canonical active-play state
- store daily evolution results in a **separate sidecar state file**
- daily updates must remain **compatible** with the player's save, not overwrite it

This means the daily evolution system should generate:
- rumor
n- pressure
- faction movement
- off-screen developments
- investigation hooks
- regional tension

...without force-changing the player's core location, inventory, quest completion, or irreversible main-story state.

### Sidecar evolution state
Store daily evolution context in a separate file such as:
`~/clawd/memory/yumfu/evolution/{universe}/user-{id}.json`

Supporting scripts:
- `scripts/set_daily_evolution.py` — enable/disable sidecar state
- `scripts/load_daily_evolution.py` — inspect sidecar state
- `scripts/detect_recent_language.py` — infer preferred recent player language
- `scripts/handle_daily_evolution_choice.py` — world-agnostic post-start yes/no activation handler
- `scripts/story_spine_state.py` — read/update the save-side current story spine
- `scripts/build_gameplay_context.py` — build hidden normal-turn context from save + world + story spine before writing a regular gameplay turn
- `scripts/daily_evolution_prepare.py` — build dynamic runtime context
- `scripts/run_daily_evolution_job.py` — generate a daily evolution update
- `scripts/run_daily_evolution.py` — persist generated result into sidecar
- `scripts/prepare_daily_evolution_delivery.py` — prepare image/text/TTS delivery plan for one daily evolution tick
- `scripts/execute_daily_evolution_delivery.py` — emit exact send/mark/apply steps for one daily evolution tick with low freedom
- `scripts/create_daily_evolution_cron.py` — create per-player daily cron
- `scripts/disable_daily_evolution_cron.py` — disable per-player daily cron
- `scripts/build_reentry_context.py` — merge save + sidecar for continue flow
- `scripts/render_continue_reentry.py` — render a concise continue-time re-entry prompt
- `assets/yumfu-logo.png` — corner logo stamped onto YumFu-generated images
- `scripts/init_sengoku_save.py` — initialize a 战国乱世 / Sengoku Chaos starting save
- `scripts/start_sengoku_game.py` — initialize Sengoku save + daily evolution choice + opening scene payload

This sidecar can track:
- last daily summary
- recent evolution history
- soft world pressure
- rumor threads
- pending hooks for the next active session
- suggested routes for next active play
- one default route if the player does not respond
- one active route representing the current narrative inertia when the player keeps not choosing
- npc / faction / item threads worth resurfacing on continue
- cron metadata / tick timestamps

### What the next active play session should do
When the player returns, the game engine may **read both**:
1. the main save
2. the evolution sidecar

Then merge them narratively:
- surface the most relevant daily evolution updates
- convert compatible hooks into active scene context
- prefer one concrete route suggestion over a vague lore recap
- if the player has been away a long time, surface the stored default route as the easiest way back in
- avoid contradictions with the canonical save

### Main-save mutation policy
For now, default to:
- **main save = read-only for daily evolution**
- **sidecar file = writable**

Default-route behavior:
- when a daily evolution tick has a clear `default_route`, treat it as the current `active_route` unless a newer active route replaces it
- later daily evolution ticks should preferentially continue from that active route instead of scattering into unrelated atmospheric nudges
- continue/reentry should surface the active route first, because that is the easiest way for a cold player to resume

Only after the system is proven safe should limited main-save mutation be considered.
### Messaging rule
If the daily evolution message is already delivered to the intended player/channel, do **not** send a separate “report generated” notification.
Only send the actual in-world update.

### Compliance note
Daily evolution adds new sidecar workflows, but it must **not** weaken older YumFu guarantees.
The following original behaviors remain mandatory unless the user explicitly requests otherwise:
- every game turn gets an image before narration
- every game turn is logged for storybook/session replay
- Telegram story text should stay paired with the image, preferably in the caption
- active play saves should still persist through the normal save workflow after meaningful state changes

### World grounding rule
Even though the content is dynamically generated, it must still stay grounded in each world’s canon/setting documents.

**Canon reference files (source-based worlds):** for IP worlds that have one, also load `worlds/canon/<world-id>.md` together with `worlds/<world-id>.json`. The JSON drives systems/mechanics; the `canon.md` keeps the *story* faithful to the source (real geography, factions/houses/clans, characters, plot beats, artifacts, themes). Currently available: `xiaoao` (笑傲江湖), `yitian` (倚天屠龙记), `game-of-thrones`, `lotr`, `harry-potter`, `warrior-cats`. These canon files are fan-authored digests, **not** original text; plot may diverge from canon.

### Rich world-detail rule (NEW)
Do not let YumFu worlds flatten into generic atmosphere.
Whenever active play, daily evolution, or continue/re-entry is generated, actively look for chances to surface concrete detail from the save/world state such as:

Also make sure those details are not random garnish — they should help the player re-understand the **main story line** and the **current major task** of this run.

If you use hidden route logic internally, translate it into natural stakes, rumors, orders, temptations, battlefield pressure, travel needs, or NPC requests before showing anything to the player.
- named NPCs and how the player currently stands with them
- faction interests, rivalries, and leverage
- objects, letters, ledgers, relics, weapons, beasts, cargo, maps, seals, or other tangible things in play
- why the current location matters strategically or emotionally
- what route is currently blocked, risky, tempting, or newly open

The player should feel there is a world with people, loyalties, and usable leads — not just tone.

Examples of what the AI should infer dynamically:
- **Game of Thrones**: if the player serves House Martell and has touched covert supply lines, daily changes should involve spies, shipping, banners, captains, watchers, coded messages, political pressure
- **Xiaoao Jianghu**: sect rumors, stolen manuals, ambushes, disciples disappearing, changing loyalties
- **Harry Potter**: patrols, prefect scrutiny, forbidden corridor rumors, House tensions, teacher intervention
- **Warrior Cats**: prey movement, scent changes, border pressure, patrol injuries, rival clan signs

### Important constraint
Daily evolution should **nudge** the player, not replace the game.
It must create pressure, intrigue, and hooks — but should not auto-finish the main story without player participation.

### 叙述风格

**Narrative style adapts to the world:**

#### 🇨🇳 **Chinese Worlds (Xiaoao Jianghu)**
- Use Chinese throughout
- Wuxia literary style (武侠文风)
- Show attributes: `[体力 -15] [内力 +5]`
- Combat descriptions with flair
- NPC dialogue matches personality

#### 🇬🇧 **English Worlds (Harry Potter, Warrior Cats)**
- Use English throughout
- Genre-appropriate style (magical/wilderness)
- Show attributes: `[HP -15] [Stamina +5]`
- Combat/action descriptions fitting the world
- NPC dialogue matches character voice

**Universal:**
- Blend narrative with game mechanics
- Combat writing has tension
- **Multiplayer interactions are immersive** - "You see 大红虾 sparring with 洪七公" / "You see Tumpaw training with Willowpelt"

### 📝 Response Length Guidelines

**Target: 150-300 words per turn** (每回合150-300词)

**⚠️ Avoid these extremes:**
- ❌ **Too short** (< 100 words): Feels lazy, lacks immersion
  - Bad: "You walk into the room. There's a table. What do you do?"
  - Good: Describe the atmosphere, NPC reactions, sensory details

- ❌ **Too long** (> 400 words): Overwhelming, slows gameplay
  - Bad: 3 paragraphs of backstory + detailed room description + NPC monologue
  - Good: Focus on the immediate scene, keep action moving

**✅ Ideal structure (150-300 words):**
1. **Scene setting** (2-3 sentences): Where you are, what's happening
2. **Action/Event** (3-4 sentences): What just happened, NPC reaction
3. **Status update** (1-2 lines): HP/Stamina changes, skill gains
4. **Options/Hook** (1-2 sentences): What you can do next

**Example (good length)**:
```
你推开酒楼木门，一阵酒肉香气扡19面而来。厅内三五江湖人士正低声交谈，角落里一名蒙面人独自饮酒。小二点头哈腰：“客官里边请！”

你刚坐下，那蒙面人忽然抬头，目光如电。他缓缓起身，手按刀柄：“华山派的？”声音冰冷而警惕。周围食客纷纷侧目，空气骤然紧绗。

[内力] 95/100  [体力] 80/100

你可以：1) 回应他的质问  2) 装作不闻  3) 先发制人
```
(~150 words - perfect!)

**Remember:** Quality over quantity. Make every word count.

### 骰子与随机
使用透明的随机系统：
```bash
# 百分比检定
shuf -i 1-100 -n 1

# D20检定
shuf -i 1-20 -n 1

# 战斗示例
攻击检定: 1d20+5 = 18 (成功!)
伤害: 2d10+3 = 16
```

### 战斗日志格式
```
⚔️ 大红虾 vs 小龙虾

[回合1] 大红虾使用【降龙十八掌】
[投骰] 攻击检定: 1d20+5 = 18 (命中!)
[投骰] 伤害: 2d10+3 = 16
💥 小龙虾未能闪避！
[体力] 小龙虾 100 → 84

[回合2] 小龙虾使用【玉女剑法】
...
```

---

## 场景配图 (Scene Illustration)

**🚨 CRITICAL RULE**: **EVERY game turn MUST generate an image BEFORE narration. No exceptions.**

### ⚡ Image Generation Policy (UPDATED 2026-04-05)

**🔴 MANDATORY: Generate image for EVERY game response**

If the user's message is a **game action** (not `/yumfu status`, `/yumfu help`, or meta commands):

✅ **ALWAYS generate image FIRST, then narrate**
✅ **Generate exactly ONE primary scene image per game turn**

That means:
- not zero images
- not two or more competing images
- one turn = one main image + one paired narrative response

**Execution order (STRICT):**
1. 🔍 Parse user action
2. 🎨 **Generate image immediately** (DO NOT narrate first!)
3. 📸 Send image with narrative text
4. 💾 Update game state
5. 📝 Log turn to session file

**DO NOT:**
- ❌ Narrate without image
- ❌ Send text first, image later
- ❌ Skip images for "minor" scenes
- ❌ Wait for user to ask "where's the picture?"
- ❌ Send duplicate scene images for the same turn
- ❌ Send one image and then a second "replacement" image unless the user explicitly asks for a redo

**Why every turn needs an image:**
- Maintains visual novel immersion
- Provides consistent experience
- Prevents forgetting to generate
- Creates complete storybook logs

### ⚡ Agent Execution Order (MANDATORY)

**🔍 PRE-CHECK before EVERY response:**
1. Is this a game action? (not just status/help/meta)
2. If YES → **MUST generate image FIRST!**
3. `/yumfu start` counts as a full game opening turn, so it also **MUST** generate an opening image before narration
4. If NO (status/help) → Skip image, reply directly

**When user takes ANY game action:**
1. **FIRST**: Generate exactly one scene image (location, NPC, action, etc.)
2. **SECOND**: Write 150-300 word narrative for that same scene
3. **THIRD**: Send exactly one image + that paired narrative together via message tool
4. **FOURTH**: Update save file
5. **FIFTH**: Log turn to session JSONL

**`/yumfu start` special case:**
- character creation / world onboarding culminates in a real playable opening scene
- that opening scene is **not image-exempt**
- after setup is complete, generate exactly one opening image and send the first playable scene with it

**Image-exempt commands (only these!):**
- `/yumfu status` / `/yumfu 状态` - Character sheet
- `/yumfu help` / `/yumfu 帮助` - Command list
- `/yumfu save` - Save operation
- Meta questions ("what can I do?", "explain combat")

**Everything else = Image required!**

### Single-image-per-turn rule
For active gameplay, the default contract is:
- **1 turn = 1 image = 1 paired narrative reply**

Only break this when the user explicitly asks for:
- another angle
- a redraw / redo
- extra gallery images
- a separate portrait after the main scene

If none of those were asked for, do not send a second image for the same turn.


**Example Flow:**
```
User: "I want to talk to Firestar"
→ Agent: "This is NPC encounter trigger!"
→ IMMEDIATELY run generate_image.py
→ Send image + start dialogue
→ NOT: Start dialogue, then "oh wait, I should generate image"
```

### Image Generation Command
```bash
uv run ~/clawd/skills/yumfu/scripts/generate_image.py \
  --prompt "<scene prompt>" \
  --filename "~/.openclaw/media/outbound/yumfu/$(date +%Y%m%d-%H%M%S)-<scene>.png" \
  --resolution 2K
```

**Do not use** `python3 ~/clawd/skills/yumfu/scripts/generate_image.py ...` directly unless the equivalent dependencies are already installed in that exact interpreter; the supported/default path is `uv run`.

**Note**: Script does NOT auto-send. After generation, send the image through the normal YumFu turn delivery flow. In Telegram group chats, this means the image must be delivered back into that same group for the turn.

---

### Art Styles by World

**Each world has its own signature art style. ALWAYS include the style prefix in prompts.**

**Global anti-text rule (MANDATORY for every YumFu image prompt):**
Append an explicit negative constraint such as:
`No text, no words, no letters, no captions, no signs, no speech bubbles, no book pages, no paragraph blocks, no watermark, no logo, image-only illustration.`
If the model still renders text-like artifacts, strengthen the next prompt further instead of accepting the bad output as final turn art.

#### 🇨🇳 Xiaoao Jianghu (笑傲江湖)
```
Chinese wuxia ink wash painting style (水墨武侠风), dramatic cinematic composition, muted earth tones with selective vivid accents (red, gold), atmospheric fog and light rays, textured rice paper background,
```

#### 🧙 Harry Potter
```
Hogwarts watercolor illustration style, magical atmosphere, warm candlelight and moonlight, storybook composition, detailed wizarding world architecture, enchanted particle effects, painterly texture,
```

#### 🐱 Warrior Cats
```
Semi-realistic warrior cats art style, forest atmosphere with dappled sunlight, detailed cat anatomy and expressions, natural woodland setting, dramatic lighting through trees, storybook illustration quality,
```

#### 🐒 Journey to the West（西游记）
```
Bright classic Journey to the West fairytale illustration style, colorful and simple mythic Chinese storybook aesthetic, cloud-edged shapes and auspicious 祥云 motifs, clean outlines, vivid but gentle colors, playful heavenly atmosphere, classic children's mythology illustration feeling, not wuxia, not xianxia, not dark realism,
```

### 场景类型与提示词模板

#### 🏞️ 探索 / 到达新地点
```
[风格前缀] wide establishing shot of <地点>, <时间>, <天气/氛围>, small figure of a lone swordsman in the scene, architectural details of <建筑>, <自然元素>
```

#### 👤 NPC遭遇 / 对话
```
[风格前缀] medium close-up portrait of <NPC描述>, <表情>, <特征>, <服饰细节>, <背景>, dramatic side lighting
```

#### ⚔️ 战斗（PvE / PvP）
```
[风格前缀] dynamic action shot, <角色> vs <敌人/玩家>, <正在使用的招式>, motion blur on weapon, debris/leaves flying, intense facial expressions, <环境>
```

**多人战斗**：
```
[风格前缀] chaotic multi-person combat, 3-5 martial artists in intense battle, various weapons and techniques, swirling energy effects, dramatic composition, <location>
```

#### 🧘 修炼 / 打坐
```
[风格前缀] serene composition, <角色> in <修炼姿势>, <地点>, mystical qi energy swirling around body as translucent wisps, soft golden light, tranquil atmosphere
```

#### 📜 剧情时刻 / 关键物品
```
[风格前缀] dramatic still life or vignette, <关键物品或象征>, <氛围光>, cinematic depth of field, <相关元素>
```

#### 🏪 商店 / 城镇室内
```
[风格前缀] warm interior scene, <商店/客栈描述>, lantern light, wooden beams, <NPC和物品>, cozy detailed atmosphere, period-accurate props
```

#### 🤝 组队场景（新增）
```
[风格前缀] group portrait, <team members> standing together in heroic formation, various weapons and martial arts stances, sense of camaraderie, <location background>
```

### 工作流程
1. 根据游戏动作判断场景类型
2. 使用风格前缀 + 场景模板组合提示词
3. 生成 1K 分辨率图片（快速）
4. 通过 `message` tool 发送图片（`media` 参数）
5. 图片自动归档到 `~/.openclaw/media/outbound/yumfu/`

### 规则
- 每回合一张图（不可跳过）
- 匹配该回合最戏剧性/有趣的时刻
- 战斗：展示动作，不是结果
- 对话：聚焦NPC面部/性格
- **多人场景**：包含所有相关玩家
- 文件名包含时间戳（唯一性）
- 图片发送后自动归档

---

## 🎮 世界特色系统 | World-Specific Features

Each world has unique progression systems designed for its target age group:

### ⚔️ **笑傲江湖 (Xiaoao Jianghu)** - 成人向 18+

**核心系统**:
- **装备品质**: 凡品 → 良品 → 宝器 → 神兵 (影响技能发挥)
- **武功境界**: 初窥门径 → 返璞归真 (6级，可自创招式)
- **道德系统**: 善恶值 -100~+100 (决定5种结局)
- **恋爱系统**: 3条情感线 (任盈盈/岳灵珊/仪琳)
- **制造系统**: 锻造武器 + 炼丹
- **7章节门槛**: 入门→危机→内斗→复仇→大战→传承→对决

**防速通机制**:
- 技能需师父认可才能学
- 装备影响技能威力（剑法必须用剑）
- 等级门槛锁定主线剧情
- 绝学需特殊条件（独孤九剑=Lv30+悟性80+风清扬）

---

### ⚡ **Harry Potter** - 青年向 13+

**核心系统**:
- **7学年制**: 不可跳年，每年4-6小时游戏时间
- **考试系统**: O.W.L.s (Year 5) + N.E.W.T.s (Year 7)，6级评分
- **友谊系统**: 5好友槽，关系分5级，解锁组队咒语
- **魁地奇**: 4位置可选，QTE小游戏
- **分院帽**: 7题性格测试决定学院（可请求）
- **学术**: 7必修课 + 5选修课，作业影响考试

**防速通机制**:
- 必须通过年终考试才能升年级
- 咒语分4层，需对应年级才能学
- 友谊等级解锁剧情任务
- 魔法物品需购买（隐形斗篷=传奇稀有）

---

### 🐱 **Warrior Cats** - 儿童向 8-12

**核心系统**:
- **7等级仪式链**: Kit → Apprentice → Warrior → Deputy → Leader (每级有仪式)
- **4季节系统**: 新叶/绿叶/落叶/寒叶 (影响猎物/疾病/战争)
- **导师制度**: 性格匹配，每日训练，关系4阶段
- **星族/黑森林**: 正邪双路线，梦境训练，预言引导
- **武士守则**: 14条规则，违反=流放/黑森林

**防速通机制**:
- 学徒必须学满7技能才能成为武士
- 需抓10只猎物 + 赢3场战斗 + 导师批准
- 副族长需先带过1个徒弟
- 族长需去月池接受九命加身

---

## 平台兼容性 | Platform Support

YumFu works across multiple AI platforms with varying feature sets:

### 🌟 **OpenClaw (Telegram, Discord, etc.)**
**Full multiplayer experience:**
- ✅ Multi-player (teams, PvP, shared world)
- ✅ AI-generated images (auto-sent)
- ✅ Persistent saves across sessions
- ✅ Group chat support
- ✅ User identification via platform ID

**Best for:** Group adventures, PvP, shared world events

---

### 🖥️ **Claude Code / Desktop AI**
**Single-player mode:**
- ✅ Full gameplay (exploration, combat, quests)
- ✅ AI-generated images (manual save/view)
- ✅ Persistent saves (local files)
- ❌ No multiplayer (PvP/teams disabled)
- ❌ No shared world state

**Best for:** Solo story-driven campaigns

---

### 💬 **Native Claude (Web/Mobile)**
**Text-only mode:**
- ✅ Basic gameplay (limited features)
- ✅ Manual save/load via copy-paste JSON
- ❌ No images
- ❌ No multiplayer
- ❌ No persistent saves (session-based)

**Best for:** Quick casual play, testing stories

---

## 初始化

### 首次游戏

**OpenClaw (Telegram/Discord):**
1. 玩家在群聊中 `@我 /yumfu start`
2. 角色创建流程：姓名、门派、属性
3. 生成该玩家的存档 `~/clawd/memory/yumfu/saves/{universe}/user-{platform_id}.json`
4. 显示开场剧情
5. 生成第一张场景图
6. 记录到世界事件

### 继续游戏
1. 玩家 `@我 /yumfu continue`
2. 读取 `user-{telegram_id}.json`
3. 读取 `world-state.json`（NPC状态、世界变化）
4. 显示当前状态 + 最新江湖大事
5. 等待玩家指令

### 多人交互
1. 玩家A `@我 /yumfu duel @玩家B`
2. 系统检查双方存档
3. 进入战斗流程
4. 更新双方存档
5. 记录到世界事件
6. 其他玩家可 `/yumfu events` 查看

---

## 最佳实践

### 对于游戏设计者（Agent）
- 武侠文风要有韵味，但不能过于文绉绉
- 战斗要有策略性，不能只是数字游戏
- NPC性格要鲜明（郭靖憨厚、黄药师古怪、欧阳锋阴险）
- 善恶值要有明显后果（杀人过多会被正派追杀）
- 秘籍要难获得，但值得追求
- **多人互动要公平** - 不能偏袒某个玩家
- **世界状态要一致** - 所有玩家看到同一个NPC状态
- **PvP要平衡** - 等级差过大可以拒绝决斗

### 🔴 MANDATORY: Session Logging (对话记录 - 必须执行)

**Every single game turn MUST be logged for storybook generation.**

### Storybook Tracking Default Rule (NEW)

- **Default behavior: storybook tracking ON**
- At the start of a new game / new save, the player may change this preference
- If the player opts out, disable storybook/session logging for that save
- If the player does not opt out, keep appending the journey as an evolving illustrated storybook source

Suggested onboarding wording:
- Chinese: `这局默认会自动记录并整理成可生成 Storybook 的旅程档案；如果你不想记录，我也可以关掉。`
- English: `This run will be auto-recorded for an illustrated storybook by default; if you don't want that, I can turn it off.`

#### When to Log

**After EVERY player action**, immediately run:

```python
from scripts.session_logger import log_turn

# Log complete turn
log_turn(
    user_id="1309815719",           # Telegram user ID
    universe="warrior-cats",         # Current world
    player_input="/yumfu look",      # What player typed
    ai_response="You see...",        # Your narrative response
    image="tumpaw-camp-123.png"      # Optional: if image generated this turn
)
```

#### Integration Points

1. **Player command received** → Store `player_input`
2. **Generate narrative** → Store `ai_response`
3. **Generate image (if triggered)** → Store `image` filename
4. **Before sending reply** → Call `log_turn()` with all 3 components
5. Create a unique `turn_id` and initialize delivery state with:
```bash
python3 ~/clawd/skills/yumfu/scripts/turn_delivery_state.py \
  --user-id {user_id} \
  --universe {universe} \
  --turn-id {turn_id}
```
6. **If `save.tts.enabled != false`** → Generate turn TTS with:
```bash
python3 ~/clawd/skills/yumfu/scripts/generate_turn_tts.py \
  --user-id {user_id} \
  --universe {universe} \
  --language {active_language} \
  --text "{final_story_text}"
```
7. Send gameplay TTS as a **voice bubble** whenever the channel supports it (`message(..., asVoice=true)`)
8. Never send a standalone image first if the same turn may still send image+caption later
9. For official YumFu turns, do **not** use auto-media-return image generation paths; generate to a local file first, then let turn delivery decide how to send it

#### Example Flow

```python
# 1. Player types: "/yumfu look"
player_input = "/yumfu look"

# 2. Generate response
ai_response = "You see the ThunderClan camp bustling with activity. Warriors share tongues near the fresh-kill pile..."

# 3. Check if image should be generated (see Image Generation rules)
image_filename = None
if should_generate_image("location"):  # Location arrival
    image_filename = generate_image("tumpaw-thunderclan-camp")
    # Returns: "tumpaw-thunderclan-camp-20260403-075523.png"

# 4. Log the turn BEFORE sending
from scripts.session_logger import log_turn
log_turn(
    user_id="1309815719",
    universe="warrior-cats",
    player_input=player_input,
    ai_response=ai_response,
    image=image_filename
)

# 5. Send response to user
reply(ai_response)
if image_filename:
    send_image(image_filename)
```

#### What Gets Logged

- ✅ **Player input (raw)** - Exact command / reply typed by player
- ✅ **Player input (storybook-ready)** - A lightly normalized narrative version of the player's action, suitable for book-style retelling
- ✅ **AI response (raw)** - Complete narrative text actually delivered
- ✅ **AI response (storybook-ready)** - A cleaner book-style scene paragraph when needed for later compilation
- ✅ **Images** - Filename if generated
- ✅ **Timestamp** - Auto-added by logger

#### Storybook Writing Intent

The storybook should not read like a raw terminal log forever. During logging and later compilation:
- preserve the **true player action**
- but also keep / derive a **more literary retelling** for the storybook layer
- convert ultra-short player replies like `A`, `1`, `go`, `attack him`, `跟上` into clearer narrative intent inside the book version
- keep major dialogue, choices, and scene transitions readable like an illustrated novella

#### Where Logs Are Stored

```
~/clawd/memory/yumfu/sessions/{universe}/user-{id}/session-{timestamp}.jsonl
```

Example:
```
~/clawd/memory/yumfu/sessions/warrior-cats/user-1309815719/session-20260403-001349.jsonl
```

#### JSONL Format

Each line in the log file:
```json
{"timestamp": "2026-04-03T00:15:23", "type": "turn", "player": "/yumfu look", "ai": "You see...", "image": "tumpaw-camp-123.png"}
```

#### ⚠️ DO NOT SKIP THIS

Logging is **NOT optional**. Every turn must be logged or storybook generation will be incomplete.

### 对于玩家
- 多与NPC对话，触发隐藏任务
- 善用打坐恢复和顿悟
- 装备和武功要配合（重剑配内功，轻功配暗器）
- 善恶值会影响剧情分支
- 存档多用几个槽位，避免后悔
- **组队时注意队友善恶值** - 正邪难两立
- **秘籍争夺要谨慎** - 可能树敌
- **PvP前评估实力** - 不要轻易生死决斗

---

## 触发规则

当玩家消息以下列任一开头时激活：
- `/yumfu`
- `/江湖`

**群聊支持**：
- 在群聊中使用 `@我 /yumfu <指令>` 即可触发
- 每个玩家独立存档
- 共享世界状态

---

**武侠江湖，等你来闯！邀上好友，共闯江湖！** ⚔️

---

## 📚 Storybook Feature

**NEW**: Every adventure is automatically recorded and can be turned into a beautiful PDF storybook!

### How It Works

**1. During Gameplay:**
- **Every turn is automatically logged** via `scripts/session_logger.py` (see Mandatory Logging above)
- Logs include player input + AI response + images
- Session files use JSONL format: `~/clawd/memory/yumfu/sessions/{universe}/user-{id}/session-{timestamp}.jsonl`
- Each session auto-expires after 2 hours of inactivity (new session starts on next play)

**2. Generate Storybook:**
```bash
# V3 - Full conversation flow (canonical)
uv run ~/clawd/skills/yumfu/scripts/generate_storybook_v3.py \
  --user-id 1309815719 \
  --universe warrior-cats

# Auto-detects latest session or specify one:
uv run ~/clawd/skills/yumfu/scripts/generate_storybook_v3.py \
  --user-id 1309815719 \
  --universe warrior-cats \
  --session-id 20260403-001349

# Ending / retire / archive branch (preferred for final delivery)
uv run ~/clawd/skills/yumfu/scripts/deliver_yumfu_turn.py \
  --user-id 1309815719 \
  --universe warrior-cats \
  --language en \
  --turn-id warrior-cats-final-001 \
  --story-text "<final in-world ending text>" \
  --ending-storybook \
  --session-id 20260403-001349
```

**3. Output:**
```
~/clawd/memory/yumfu/storybooks/warrior-cats/user-1309815719-20260403-075523/
├── storybook.html        # canonical shareable artifact (HTML first)
└── images/               # copied source images for local reference
    ├── tumpaw-ceremony-20260403.png
    ├── tumpaw-firestar-20260403.png
    └── tumpaw-fishing-20260403.png
```

### Features

- ✅ **Auto-tracking** - Every turn logged via SessionLogger
- ✅ **Complete conversation** - Full player input + AI response flow
- ✅ **Beautiful formatting** - Professional HTML → PDF layout
- ✅ **Image integration** - All AI-generated art at correct positions
- ✅ **Stats summary** - Final character stats and relationships
- ✅ **Achievements** - All unlocked achievements listed
- ✅ **Multi-language** - Works with Chinese and English worlds
- ✅ **Session management** - Auto-creates new sessions after 2h inactivity

### V3 Storybook Structure (Complete Conversation)

The V3 generator creates a **complete dialogue flow** storybook:

```html
[Tumpaw's Adventure - Title Page]

▶️ Player: /yumfu look
You see the ThunderClan camp bustling with activity. Warriors share tongues 
near the fresh-kill pile while apprentices practice battle moves...

[Image: ThunderClan Camp - embedded here]

▶️ Player: /yumfu train swimming
Willowpelt leads you to the river border. "Swimming is unusual for ThunderClan," 
she purrs, "but if you have the talent, we'll develop it..."

▶️ Player: /yumfu go river
You pad down to the river. The water flows swiftly, sunlight glinting off the surface...

[Image: Tumpaw at River - embedded here]

---
[Final Stats & Achievements]
```

**Key difference from V2:**
- V3 shows **every command you typed** + AI's full response
- Images appear exactly where they were generated in the conversation
- V2 only shows summary events from save file notes

### When to Generate

**Trigger storybook generation when:**
- Player reaches major milestone (becomes warrior, leader, etc.)
- Player explicitly requests (`/yumfu storybook` or asks for PDF)
- Session ends (character dies, quest completed)
- Player hasn't played in 24+ hours (auto-archive)
- **Player explicitly ends / retires / abandons / terminates a save or story run**

### End-of-Journey Storybook Rule (UPDATED)

When a run reaches a meaningful ending **or** the player explicitly says they want to stop / end / archive / retire that game record:

1. **If storybook tracking is enabled, auto-generate the final HTML storybook immediately.**
2. The ending storybook must be an **art-rich illustrated HTML storybook** containing:
   - the journey summary
   - key player choices
   - major AI responses / scene narration
   - generated images from the run
   - final stats / relationships / achievements when available
3. Preferred formats:
   - **HTML first** (canonical, richly styled, easy to preserve, image-embedded single file)
   - **PDF only as an optional secondary export** if conversion succeeds and layout is visually acceptable
4. **Scene-binding rule (MANDATORY)**:
   - storybook pages must be organized as **scene blocks**
   - each scene block should contain: **one image + the exact matching scene/dialogue text directly below or beside it**
   - do **not** put images into a detached gallery while moving all text to separate long prose sections
   - do **not** separate a scene's picture from its corresponding dialogue/narration across distant sections unless the user explicitly asks for a gallery-style export
5. **Quality rule (MANDATORY)**:
   - decode accidental unicode-escaped strings (for example `\u9aa8\u602a\u7cbe\u7075`) before rendering titles / prose
   - final stats section must not be left empty when the save contains HP / stamina / level / inventory / relationships / attributes / skills / achievements
   - image captions must be derived from scene meaning, not lazy filename fragments like `Watch` / `Thread`
   - visual style should read like a **formal illustrated storybook**, not a raw terminal transcript dump
6. Delivery rule:
   - If generated, **send it back into chat** as a file/message whenever possible
   - Also keep the generated file(s) on disk under the YumFu storybook output directory
7. If the player has explicitly disabled storybook tracking for that save, skip the auto-generation.
8. During normal play, keep the **underlying rolling storybook source** updated by default.

Recommended helper:
- `uv run ~/clawd/skills/yumfu/scripts/prepare_end_storybook.py --user-id <id> --universe <world> [--session-id ...]`
- This refreshes/generates the latest HTML storybook and returns JSON for chat delivery.
- The standard delivery helper now also supports this path directly:
  - `uv run ~/clawd/skills/yumfu/scripts/deliver_yumfu_turn.py ... --ending-storybook [--session-id ...]`
  - when enabled, it will prepare TTS and the end-storybook together in one structured payload.

### Daily Evolution + Storybook Entry Rule

If daily evolution is enabled and a storybook source already exists for that save:
- daily evolution **may** mention that the journey archive/storybook has been updated
- if there is a real user-openable destination, send that entry point
- if there is **no real public/clickable URL**, do **not** send a fake `file://` or local-path link as if it were usable on chat surfaces
- instead, prefer one of:
  - send the HTML file directly
  - send the PDF directly
  - send a short message saying the latest storybook can be generated/refreshed on request

### Agent Instructions for Storybook Generation

When player requests storybook or reaches milestone:

```python
# 1. Generate HTML storybook first
result = exec({
    "command": "uv run ~/clawd/skills/yumfu/scripts/generate_storybook_v3.py --user-id 1309815719 --universe warrior-cats"
})

# 2. Confirm the HTML uses scene-bound layout
# Each major scene should read as:
#   image
#   matching scene/dialogue text
# not: detached image gallery + separate prose dump

# 3. Send HTML as the canonical deliverable
message({
    "action": "send",
    "channel": "telegram",
    "target": "1309815719",
    "media": html_file_path,
    "message": "📖 Your illustrated storybook is ready in HTML. This version keeps each image paired with its matching scene text."
})

# 4. Only generate/send PDF if the layout is visually confirmed good
pdf_path = browser({
    "action": "pdf",
    "url": f"file://{html_file_path}",
    "path": "~/.openclaw/media/outbound/tumpaw-adventure.pdf"
})
```

### Agent Instructions for Ending / Retire / Archive Branches (DEFAULT)

When the run has clearly reached an ending, death, finale, retirement, archive, or explicit stop:

1. **Do not ask again whether to make a storybook** if storybook tracking is enabled.
2. Treat the final storybook HTML as part of the default ending delivery.
3. Use the standard delivery helper with `--ending-storybook` so the normal turn package and the ending storybook are prepared together.
4. If `next_actions.send_end_storybook_html == true`, send the generated HTML file back into chat.
5. After successful delivery, mark `storybook_sent` so the same ending storybook is not re-sent repeatedly.

**Default ending-branch workflow:**

```bash
uv run ~/clawd/skills/yumfu/scripts/deliver_yumfu_turn.py \
  --user-id <id> \
  --universe <world> \
  --language <zh|en> \
  --turn-id <stable-ending-turn-id> \
  --story-text "<final in-world ending text>" \
  --ending-storybook \
  [--session-id <session-id>]
```

Then, from the returned JSON:
- send the normal text / image / TTS as usual
- if present, send `end_storybook.html` back into chat as the canonical final storybook deliverable
- keep PDF optional, never primary

**Preferred OpenClaw workflow:**

```bash
# For normal manual storybook export
cd ~/clawd/skills/yumfu
uv run scripts/generate_storybook_v3.py --user-id 1309815719 --universe warrior-cats

# For ending / retire / archive branches, prefer the delivery helper
uv run scripts/deliver_yumfu_turn.py ... --ending-storybook [--session-id ...]

# Ship HTML first if it reads well in-chat
# Only convert to PDF after verifying the HTML layout preserves scene binding
```

---
