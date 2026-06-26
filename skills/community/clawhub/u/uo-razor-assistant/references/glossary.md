# Glossary of Razor Terms

This glossary defines key terms used throughout the Razor skill pack.  Where possible, definitions are based on official documentation or the Outlands extensions.  Use this glossary to clarify terminology when building or debugging macros and scripts.

## A–F

**Action commands** – A family of script commands that perform direct actions such as attacking, casting spells, clicking items, lifting or dropping items, using skills and moving the character.  Examples include `attack`, `cast`, `dclick`, `dclicktype`, `lift`, `drop` and `skill`.

**Agent** – A Razor feature that automates common tasks like organising items, restocking supplies, selling items or using items once.  Agents are configured in the **Agents** tab and can be triggered via commands or hot‑keys.

**Alias (Outlands)** – A shorthand name for a mobile or item serial.  Outlands introduces the `ground` alias to represent items on the ground, usable in commands like `findtype` or `dclicktype`.

**Bandaging** – An Outlands expression that returns the remaining bandage timer on your character or a target.  Useful for replacing fixed pauses in healing macros.

**Built‑in hot‑key** – A predefined action that Razor recognises internally (e.g., Attack, Last Target, Cast Spell).  Built‑ins are bound by numeric IDs in the profile XML and appear without `Play:` in the Hot Keys tab.

**Cooldown** – A mechanism introduced by Outlands that tracks the delay before a specific ability can be used again.  The `cooldown` expression returns how much time remains.  The `cooldown` command can start or reset a named cooldown.

**Cooldown debuff (PvP)** – When structured PvP is active on Outlands, many commands and expressions (including cooldowns) are disabled.

**Command** – The primary building block of a Razor script.  Commands are case‑insensitive keywords followed by arguments.  They fall into families like action commands, agent commands, targeting commands, timer commands and list commands.

**Counter** – A Razor display element that tracks the quantity of a resource (e.g., reagents) and can appear in the title bar or counters window.

**createtimer, settimer, removetimer** – Timer commands that create, start or delete timers.  Timers run independently of the main script and can be queried with the `timer` expression.

**DoubleClickTypeAction** – A serialized macro line that double‑clicks any item of a specific type.  The script equivalent is `dclicktype <type>`.

**Drop** – In a script, the `drop` command releases the item currently being held (lifted).  See also `lift`.

**Expressions** – Values that can be evaluated in `if` statements or assigned to variables.  Common expressions include `insysmsg`, `bandaging`, `followers`, `targetexists`, `timer`, `cooldown` and `findlayer`.

## G–L

**Gump** – A user interface dialog in UO.  Outlands adds commands like `waitforgump`, `gumpresponse` and `gumpclose` to interact with gumps.  The expressions `gumpexists` and `ingump` detect the presence of a gump or text inside it.

**Hot‑KeyAction** – A serialized macro line that invokes a built‑in Razor action by numeric ID.  When ID 0 is used, the line references a macro or script via the `Play:` wrapper.

**IfAction/ElseAction/EndIfAction** – Serialized macro constructs that implement conditionals.  In scripts, use `if … else … endif`.

**ignore / unignore / clearignore** – Commands that manage the ignore list in Outlands.  Ignoring a mobile or item prevents scripts from interacting with it.

**in operator** – Outlands operator that tests whether a substring appears in a string or whether an element is in a list.

**insysmsg** – Expression that checks the last system message for a substring.  Often used to branch based on success or failure of an action.

**Lifttype** – Command (and macro action) that lifts an item of a specific type into the cursor.  In Outlands it accepts optional parameters for container, hue, quantity and range.

**List commands** – Commands for creating and manipulating lists: `createlist`, `pushlist`, `poplist`, `removelist`, `clearlist`, `list`, `inlist` and `atlist`.  Lists hold serials or values and can be iterated with `for`/`foreach`.

**Loop** – A repeated sequence of commands.  In macros, loops are implemented with `ForAction` and `EndForAction` lines; in scripts, loops are implemented with `for`, `foreach` or `while` constructs.

## M–R

**Macro** – A recorded sequence of actions saved in a `.macro` file.  Macros are brittle because they store absolute serials and rely on fixed pauses, but they are easy to create via recording.

**MacroCastSpellAction** – Serialized macro line that casts a spell by ID.

**PauseAction** – Serialized macro line that pauses for a specified duration.  In scripts, use `wait <milliseconds>`.

**Play:** – Prefix used in hot‑key names to indicate a macro or script should be executed.  Hot‑keys with this prefix always have ID 0 in the profile XML.

**Profile** – A collection of settings, counters, agents and hot‑keys specific to a character.  Profiles are stored in the `Profiles` folder and can be cloned or saved via the General tab.

**PvP debuff** – Outlands restriction that disables many automation features during structured PvP and zeroes player serials.

## S–Z

**Script** – A text file (`.razor`) containing Razor commands.  Scripts are more readable and modifiable than macros and can be converted from macros via the **Convert to Script** option.

**setvar / unsetvar** – Commands that assign or delete variables.  Outlands allows a second parameter for serial assignment and uses `!` to mark variables as non‑persistent.

**Target commands** – Commands for selecting targets: `target`, `targetself`, `lasttarget`, `targettype`, `targetrelloc`, `targetloc` and `waitfortarget`.  Macros may also record `LastTargetAction` or `TargetTypeAction`.

**Timer** – A named countdown used to measure delays or throttle actions.  Created with `createtimer`, modified with `settimer`, removed with `removetimer` and queried with `timer` and `timerexists`.

**Variable** – A named value stored in memory.  Variables can hold numbers, strings or serials.  Use `setvar <name> <value>` to assign.  Use `varexist <name>` to test for existence.  In Outlands, prefixing the name with `!` makes it non‑persistent.

**wait / waitfortarget** – Commands that pause script execution.  `wait <ms>` pauses for a fixed time; `waitfortarget` waits until a target cursor appears.  In macros, similar functionality is provided by `PauseAction` and `WaitForTargetAction`.