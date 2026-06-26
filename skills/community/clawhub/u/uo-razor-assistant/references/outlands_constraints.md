# UO Outlands Razor Extensions and Restrictions

The **Outlands** shard distributes a fork of Razor Community Edition that extends the scripting language and imposes shard‑specific restrictions.  This module summarises the key changes so an OpenClaw agent can safely generate scripts and macros that comply with Outlands rules.

## Expanded Commands and Aliases

Outlands extends several **search and targeting commands**.  These commands accept additional parameters such as container/hue/quantity/range and support the new alias `ground` for items on the floor.  Commands impacted include:

* `dclicktype`, `findtype`, `findtypelist`, `targettype` and `lifttype` – Each can take optional arguments specifying where to search (e.g., `ground`, `backpack`, `bank`), hue filters, quantities and range.
* `setvar` – Modified to accept a second parameter to store a serial; prefixing the variable name with `!` makes it **non‑persistent**.  `unsetvar` deletes variables.
* `ignore`, `unignore`, `clearignore` – Manage ignore lists.
* `warmode` – Toggle your war mode status.
* `getlabel` and `rename` – Retrieve or change the label of an item or mobile.
* `skill` and `setskill` – Activate or adjust skills in script.
* `waitforgump`, `gumpresponse`, `gumpclose` – Interact with gumps (UI dialogs).
* `cooldown` – Exposes a new cooldown mechanism (see Cooldowns section).

## New Expressions

Outlands adds numerous expressions that can be used in `if` statements or assigned to variables.  These expressions enable your scripts to make decisions based on game state.  Notable additions include:

* **Find expressions:** `find` returns a serial matching search criteria (source/hue/quantity/range); `findlayer <layer>` returns the serial of an item worn on a specific equipment layer.
* **Target status:** `targetexists` returns true when a targeting cursor is active.
* **Player stats:** `followers` returns your current follower count; `hue`, `name`, `paralyzed`, `invul`, `warmode` and `noto` return properties of mobiles.
* **Status checks:** `dead` checks if a mobile is dead; `maxweight` and `diffweight` calculate carrying capacity; `diffhits`, `diffmana` and `diffstam` compare your current and maximum values.
* **Item counts:** `counttype` counts items of a given type in a container.
* **Gump checks:** `gumpexists` and `ingump` detect gumps or text within gumps.
* **Variables and bandaging:** `varexist` tests if a variable is defined; `bandaging` returns the remaining bandage timer.
* **Cooldown:** `cooldown` returns the time remaining on a named cooldown (e.g., `cooldown 'Explosion'`).

Outlands also introduces the **`as` operator** to assign the result of an expression to a variable and the **`in` operator** to test string or list membership.

## Lists

Lists provide built‑in support for dynamic collections.  Scripts can create lists with `createlist <name>`, add items using `pushlist`, remove items using `poplist` or `removelist`, and iterate through items using `for`/`foreach` loops.  The `list <name>` expression returns the list for iteration, and `inlist` tests membership.  These constructs enable complex inventory or travel automation (e.g., cycling through runebooks).  Lists are one of the most significant differences between Razor CE and Outlands.

## Timers and Cooldowns

Outlands provides a **timer subsystem** via `createtimer`, `removetimer` and `settimer`, along with expressions `timer` and `timerexists` to query a timer’s value.  Timers run independently of the main script and can trigger actions after specific durations.  The **cooldown system** exposes ability cooldowns; the `cooldown` command can set or reset cooldowns and the expression `cooldown 'Name'` returns how much time remains.  Cooldowns allow scripts to throttle actions like potion throws or weapon special moves.

## PvP Restrictions

During structured or consensual **PvP** (e.g., tournaments or faction fights), Outlands applies a debuff that disables certain automation features.  These restrictions do **not** affect non‑consensual player‑killing in the open world.  Key points:

* **Commands disabled:** `setvar` on other players, `droprelloc`, `waitforsysmsg`, `settimer`, `removetimer`, `getlabel`, `rename`, `cooldown`, and `wait`/`pause` commands are disabled.
* **Expressions disabled:** Many status expressions, including `bandaging`, buffs, `mana`, `hits`, `stam`, `poisoned`, `paralyzed`, `hidden`, `followers`, `hue`, `noto`, `dead` (for other players), `maxweight`, `diffweight`, `gumpexists`, `ingump`, `cooldown` and `casting`, are disabled.
* **Serial handling:** When the PvP debuff is active, variables holding player serials resolve to `0x0`, preventing scripts from targeting other players.
* **Item handling:** Search commands (e.g., `find`, `findtype`, `findtypelist`) only return items in your own inventory during PvP.  Party and guild messages are ignored.
* **PvP expression:** A new `pvp` expression is true when the debuff is active; use it to disable or alter scripts during PvP.

Scripts should always check `pvp` before running actions that rely on disabled commands or expressions.  For instance:

```text
if pvp
    sysmsg 'Automation disabled during PvP'
else
    // normal script logic here
endif
```

Using the debuff state ensures scripts do not fail unexpectedly.