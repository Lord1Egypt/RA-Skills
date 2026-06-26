# Razor Core Reference for OpenClaw Skill Pack

## Overview of Razor

Razor is a **light‑weight assistant** for **Ultima Online** that sits between the game client and the server.  It offers a set of automation features – such as hot‑keys, recorded macros and a command‑based scripting engine – designed to simplify repetitive tasks.  Unlike heavier assistants, Razor stores all its data inside its own folder, so it can run from a USB stick or move between computers.  Each character has a **profile** that holds your options and hot‑keys.  Profiles are stored under `\Profiles\` next to `Razor.exe` and you should create a separate profile for each character to avoid accidental overwrites.  Macros live in a `Macros` folder (file extension `.macro`), while scripts live in a `Scripts` folder (extension `.razor`).  Razor can migrate by copying these folders along with `counters.xml` and `Razor.exe.config`.  Because macros are shared across characters but hot‑keys are profile specific, keep profiles and macros organised.

### Macros vs Scripts

* **Macros** are sequences of recorded actions saved in a serialized format.  They are great for quickly automating simple in‑game tasks but were never designed to be edited directly.  Macros are stored in the `Macros` folder and appear in the macro list with optional categories.  To create one, click **New**, enter a name, then record actions in‑game using the **Record** button; stop recording when finished.  Right‑click the macro to move it into a category or use options such as **Reload** (refresh macros on disk), **Save**, **Move Up/Down**, **Remove Action**, **Begin Recording Here**, **Play From Here** and **Special Constructs**.  Special constructs let you insert pauses, waits, set last target, comments, `If/Else` conditionals or `For` loops into recorded macros.  Razor also supports **absolute target variables** so one macro can target different runebooks or runes across characters.  Additional options include range checks for `TargetByType`/`DoubleClickType`, a step‑through mode, a default 50 ms delay for OSI clients and the ability to hide play/finished messages.

* **Scripts** use a **command‑based scripting language** that is easier to read and edit than macro files.  Scripts can be written in any text editor or in Razor’s built‑in script editor, which provides syntax highlighting and auto‑completion.  Simple macros can be converted to scripts by right‑clicking the macro and selecting **Convert to Script**.  For example, a macro that casts *Blade Spirits*, waits for a target and targets a relative location looks like this in macro form:

```text
Assistant.Macros.MacroCastSpellAction|33
Assistant.Macros.WaitForTargetAction|30
Assistant.Macros.TargetRelLocAction|3|1
```

The equivalent script is much clearer:

```text
cast 'blade spirits'
waitfortarget
targetrelloc 3 1
```

In a more complex example, a macro that uses **Detect Hidden**, waits for target, presses a hot‑key, pauses, checks a system message, speaks and then targets the closest grey humanoid generates several serialized lines.  The script version uses straight‑forward commands and control flow.  Because scripts are readable and portable, they are preferred for complex automation.

### Command Families

The scripting engine groups commands into families.  Below is a non‑exhaustive overview; see the full command reference for details.

| Family | Purpose |
|------|---------|
| **Action commands** | Direct actions such as `attack`, `cast`, `dclick`, `dclicktype`, `dress`, `drop`, `lift`, `lifttype`, `rename`, `skill`, `virtue`, `walk`, `wait/pause` etc. |
| **Agent commands** | Interact with agents like `organizer`, `restock`, `scavenger`, `sell`, `useonce` etc. |
| **Gumps, menus & prompts** | Handle in‑game dialogues via `gumpresponse`, `gumpclose`, `menu`, `menuresponse`, `promptresponse`, `waitforgump`, `waitformenu`, `waitforprompt`. |
| **Ignore commands** | Manage ignore lists with `clearignore`, `ignore`, `unignore`. |
| **List commands** | Work with lists via `createlist`, `clearlist`, `pushlist`, `poplist`, `removelist`. |
| **Messaging commands** | Communicate using `say`, `emote`, `guild`, `overhead`, `sysmsg`, `waitforsysmsg`, `whisper`, `yell` etc. |
| **Targeting commands** | Control targeting through `clearall`, `lasttarget`, `setlasttarget`, `target`, `targetrelloc`, `targetloc`, `targettype`, `waitfortarget`. |
| **Timer commands** | Manage timers via `createtimer`, `removetimer` and `settimer`. |

The Outlands fork extends these families with additional search commands (`findtype`, `lifttype`), variables, list operations, timers and cooldowns (see the Outlands module).

### Profiles and File Structure

Razor creates a **profile** for each character.  Profiles store your settings, options and hot‑keys in a file located under `\Profiles\`; you can create, save, clone and delete profiles from the **General** tab.  Multiple profiles allow you to keep different hot‑keys for different characters.  A profile is saved either when you log out (opening the paperdoll and clicking *Logout* triggers a save) or when you click the **Save** button.  Macros are stored in a global `Macros` folder and are shared across profiles.  Scripts are stored in a `Scripts` folder and can be edited directly in a text editor.  Keep backups of these folders; copying `Profiles`, `Macros`, `Scripts`, `counters.xml` and `Razor.exe.config` will migrate Razor to another machine.

### Tab Overview

#### General

The **General** tab contains settings related to the Razor client itself.  You can manage **profiles** (create, clone, save or delete).  The **Maps/Boat** sub‑section provides a basic map (UOPS) and a boat control tool with directional controls.  The **Other** sub‑section allows you to toggle the welcome screen, enable “smart always‑on‑top” (keep Razor above the UO window), choose whether Razor appears in the taskbar or system tray, adjust client priority, set window opacity and select the interface language.

#### Options

The **Options** tab controls client‑side behaviour.  In **Speech & Messages** you can choose hues for Razor messages, warnings and speech; override spell hues and format; highlight last target; and display buff/debuff messages.  **Targeting & Queues** offers options to queue `LastTarget` and `TargetSelf` commands, display action‑queue status messages, auto‑queue object delays (set delay equal to ping + 500 ms), and adjust the object delay.  Additional options include queuing system messages, disabling message spam and toggling container labels or health/mana/stam overhead displays.

#### Display/Counters

Use this tab to customise on‑screen information and counters.  The **Title Bar Display** can show built‑in counters such as `{char}` (character name), `{hp}/{hpmax}`, `{mana}/{manamax}`, `{stam}/{stammax}`, `{ar}` (armor rating), `{gold}` (gold in backpack), `{followers}` (current followers) and many others.  You can colour sections of the title bar with HTML hex codes using the `~#rrggbb` notation and `~#~` to terminate the colour.  The **Counters** sub‑tab lets you add custom counters (e.g., reagents) and display them in Razor or the title bar.  There is also a **Bandage Timer**, **Overhead Messages** (create custom overhead messages with colour), and **Waypoints** for mapping and navigation.

#### Arm/Dress

The **Arm/Dress** tab is for outfitting your character.  You can create arm/dress lists for outfits or single items, assign hot‑keys to equip them and let Razor automatically move conflicting items (e.g., unequip a halberd before equipping a war axe).  The **Arm/Dress Items** section lets you dress or undress lists, add items (targeting items or entire bags), add your current worn items, remove items, clear lists or set/change the undress bag.  Converting entries to “dress by type” tells Razor to find any item of the same type rather than a specific item.

#### Skills

The **Skills** tab displays every skill, showing your current value, base (real) value, +/- changes since logon, cap and lock status.  Buttons allow you to reset the +/- counters, set all locks at once, copy selected/all skills to the clipboard, log skill changes to a CSV file and display a **Base Total** of your skills.  Capturing MIBs writes a file to your Razor folder (RunUO only).

#### Agents

Agents automate item management.  Right‑click agents to assign an alias for easier identification.  Important agents include:

* **Use Once Agent** – holds items to use once via a hot‑key; useful for trapped pouches.  You can add single items or all items in a container; Razor removes each item after use and warns when the list is empty.
* **Sell Agent** – automatically sells listed items to vendors.  You choose how many to sell, add items by targeting them, set a “hot bag” to sell items from and toggle the agent on/off.  Since items are sold by type, Razor may sell all variants of an item.
* **Organizer Agent** – moves items from one container to another.  You can maintain multiple organiser lists, add items or entire bags, set a target container, organise or stop organising via hot‑keys.
* **Scavenger Agent** – picks up items off the ground within range; often used at IDOCs (in‑game collapse events).  Other agents include **Buy**, **Restock** and an **IgnoreList** for ignoring mobiles and items.

#### Filters

Filters change how the client displays graphics or plays audio.  **General** options include sound filters, light filter (100% light), death filter (removes death animation) and graphical replacements for dragons, drakes and daemons.  **Text & Messages** options can block text from specific mobiles, filter repetitive system or overhead messages and set delays before showing filtered messages.  The **Target Filter** ignores specific mobiles completely – useful when NPCs might be accidentally targeted during events.  **Sound & Music** options let you block particular sounds, play them on demand, show the names of filtered or non‑filtered sounds and play specific music tracks in the client.

#### Hot Keys

Hot‑keys bind key combinations to actions.  The **Filter Box** narrows the list as you type.  To assign a key, select the entry in the index, choose the key combination (Ctrl/Alt/Shift), then click **Set**; **Unset** clears a binding.  You can optionally specify a **Command** (a text alias accessed via `>command`), pass the key to the UO client (**Pass to UO**), or execute the selected action once (**Execute Selected**).  Hot‑keys are grouped into categories: *Agents*, *Dress*, *Friends*, *Items*, *Macros*, *Misc*, *Scripts*, *Skills*, *Spells* and *Targets*.  A table on the hot‑keys page defines notoriety colours (blue for innocent, green for guild/ally, grey for attackable/criminal, orange for enemy, red for murderer) and target type groupings (non‑friendly, friendly, enemy, red, grey, criminal, innocent).

#### Macros and Absolute Target Variables

The **Macros** tab stores your recorded macros.  Macros are organised into categories; right‑click to add categories, delete or move macros and refresh the list.  Recording is done through the **Record/Stop** buttons.  You can edit macros by moving lines, removing actions or inserting new recorded actions mid‑macro.  Special constructs allow for pauses/waits, last‑target assignments, comments, conditionals and loops.  Absolute target variables let you define variables (e.g., `$rune`) bound to items; macros referencing the variable will work across profiles.  You can add, insert, retarget or remove variables.  Additional macro options include range checks for `TargetByType` and `DoubleClickType`, step‑through execution, setting a default macro action delay and hiding play/finish messages.

#### Scripts and Script Editor

Scripts reside in the **Scripts** tab.  The scripting engine uses clear, line‑oriented commands.  Scripts can be edited in Razor’s built‑in editor or an external text editor.  Right‑click a macro and select **Convert to Script** to generate a script version.  The script editor supports syntax highlighting, auto‑completion and a set of keyboard shortcuts: `Ctrl+G` (go to line), `Ctrl+F` (find), `F3` (find next), `Ctrl+H` (search & replace), `Ctrl+Shift+C` (comment/uncomment), `Alt+Drag` (multi‑select), `Ctrl+Home/End` (jump to first/last line), `Alt+Up/Down` (move selected lines), bookmark commands (`Ctrl+B`, `Ctrl+Shift+B`, `Ctrl+Shift+N`) and auto‑complete (`Ctrl+Space`).  You can also zoom the editor with `Ctrl+Mouse Wheel` or reset zoom with `Ctrl+0`.

#### Friends, Screen Shots and Advanced

The **Friends** tab lets you manage friend lists and friend groups – useful when using the **Friends** hot‑key category.  **Screen Shots** allows you to capture in‑game screenshots and define the save path and format.  The **Advanced** tab contains lower‑level options (e.g., enabling/disabling specific client hooks, debug options and resource counters) and is generally left to advanced users.
