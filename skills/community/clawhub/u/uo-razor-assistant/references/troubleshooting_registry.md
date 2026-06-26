# Troubleshooting and Ambiguity Registry

This registry lists common problems you may encounter when creating or using Razor macros, scripts or hot‑keys, along with recommended solutions.  Refer to this list when debugging issues in an OpenClaw context.

## Hot‑Key Ambiguities

**Symptom:** A hot‑key does not perform the expected action or triggers the wrong macro/script.

**Causes & Solutions:**

* **ID confusion** – Built‑in hot‑keys are identified by numeric IDs, while macros/scripts use ID 0 with a `Play:` prefix.  If the profile XML incorrectly uses a number for a macro/script, Razor will attempt to call a built‑in command instead.  Inspect the `<hotkey>` entry and ensure that macros/scripts use ID 0 and the correct `Play:Name` value.
* **Name collision** – The same visible label (e.g., “Disarm”) may refer to both a built‑in action and a macro.  Avoid giving your macros the same names as built‑in commands.  Prefix custom macro names clearly (e.g., “Macro:DisarmToggle”).
* **Duplicate key** – Two different actions bound to the same key combination cause conflicts.  Unset conflicting keys and choose unique combinations.

## Macro Execution Issues

**Symptom:** A recorded macro stops unexpectedly, targets the wrong item or fails to find items.

**Causes & Solutions:**

* **Absolute serials** – Macros store serial numbers of targeted items.  If an item’s serial changes (e.g., new weapon), the macro fails.  Use absolute target variables or convert the macro to a script and use `targettype`, `findtype` or variables.
* **Range limitations** – The macro may attempt to target items out of range.  Enable the **range check** options for `TargetByType` and `DoubleClickType` in the macro options.
* **Pause timing** – Fixed `PauseAction` lines may be too short or too long depending on ping.  Replace pauses with `waitfortarget` or Outlands expressions like `bandaging`.
* **Missing variables** – If an absolute target variable is deleted or renamed, macros referencing it will fail.  Check the **absolute target variables** dialog and retarget or remove invalid variables.

## Script Syntax Errors

**Symptom:** Razor displays a syntax error or does nothing when running a script.

**Causes & Solutions:**

* **Incorrect command names** – Commands are case‑insensitive but must be spelled correctly.  Refer to the command lists in the core reference and Outlands module.
* **Missing quotes** – Enclose string parameters (e.g., spell names, skill names, overhead messages) in single quotes.  Do not mix single and double quotes unless using string interpolation on Outlands.
* **Lack of waitfortarget** – Some actions require a target.  Insert `waitfortarget` before a `target` or `targettype` command..
* **Indentation vs. syntax** – Razor scripts do not enforce indentation, but forgetting `endif`, `endfor` or `endforeach` will cause errors.  Ensure each `if`, `for` or `foreach` has a matching closing keyword.

## Outlands‑Specific Problems

**Symptom:** A script that works on other shards fails on Outlands or stops during tournaments.

**Causes & Solutions:**

* **Disabled commands/expressions** – During structured PvP, commands like `setvar`, `droprelloc`, timers and cooldowns and expressions like `bandaging`, `mana` and `cooldown` are disabled.  Wrap logic in `if pvp` and provide an alternate branch or return early.
* **Serial zeroing** – Player serials resolve to `0x0` in PvP; scripts that attack a player using a serial will fail.  In PvP, rely on built‑in targeting commands (e.g., attack) rather than variables.
* **Limited find functions** – `find`, `findtype` and related commands only find items in your own inventory during PvP.  Avoid searching the ground or world containers under the debuff.
* **Expectation of disabled features** – Outlands disables `waitforsysmsg`, `cooldown`, `settimer` and `removetimer` during structured PvP.  Scripts relying on these must detect `pvp` and avoid using them.

## Data Loss and Corruption

**Symptom:** Profiles, macros or scripts disappear or revert unexpectedly.

**Causes & Solutions:**

* **Failure to save** – Remember to click **Save** on the General tab or log out of UO to trigger profile save.
* **Concurrent modifications** – Editing a macro file while Razor is running can cause corruption.  Close Razor or use the **Reload** button after external edits.
* **Missing backups** – Always maintain backups of the `Profiles`, `Macros` and `Scripts` folders and the `counters.xml` and `Razor.exe.config` files.  Restore from backup if a file becomes corrupted.

## Miscellaneous

* **Auto‑queue latency** – In high‑ping environments, enable **Auto‑queue object delay** in the Options tab to automatically delay actions equal to your ping plus 500 ms.
* **Unexpected attacks** – Setting the Attack hot‑key may inadvertently target friendlies.  Use the notoriety filters (innocent, enemy, criminal, etc.) to narrow your target selections.
* **Language issues** – Razor’s interface language can be changed in the General tab.  Ensure you select the correct language to avoid confusion.