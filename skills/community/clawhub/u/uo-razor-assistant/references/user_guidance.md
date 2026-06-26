# User Guidance for UO Razor Assistant

This guide describes how to install and use the provided **UO Razor Assistant** modules. It assumes you have downloaded the contents of the `uo-razor-assistant` directory and unzipped them into a folder for reference. The modules are designed to complement, not replace, the official Razor documentation and UO Outlands wiki.

## Installation and Setup

1. **Backup your data** – Before making any changes, back up your existing `Profiles`, `Macros` and `Scripts` folders as well as `counters.xml` and `Razor.exe.config`.
2. **Locate Razor folders** – The Razor executable stores profiles, macros and scripts in subfolders next to `Razor.exe`. Locate these folders before proceeding.
3. **Review the modules** – The skill pack includes:
   * `core_reference.md` – A detailed overview of Razor’s features and tabs.
   * `hotkey_action_map.csv` – A sample mapping of hotkeys to built-in actions, macros and scripts.
   * `macro_serialization_legend.md` – Explains macro file lines and how they map to in-game actions.
   * `examples/macros/` – Text-safe markdown files containing macro examples that can be copied into local `.macro` files.
   * `examples/scripts/` – Text-safe markdown files containing Razor script examples that can be copied into local `.razor` files.
   * `profile_xml_examples.md` – Illustrative profile hotkey entries for built-ins, macros and scripts.
   * `outlands_constraints.md` – Summarises Outlands-specific commands, expressions and PvP restrictions.
   * `validation_workflow.md` – Step-by-step instructions for testing macros and scripts.
   * `troubleshooting_registry.md` – Common problems and solutions.
   * `glossary.md` – Definitions of key terms and concepts.

## Applying Macro Examples

1. **Open the macro example** – Open the desired file from `examples/macros/`.
2. **Copy the serialized macro lines** – Copy the macro contents into a new local file in your Razor `Macros` folder and save it with a `.macro` extension.
3. **Reload macros** – In Razor’s **Macros** tab, click **Reload** to refresh the list. The new macro should appear. If it does not, check the file extension and name.
4. **Assign a hotkey** – Select the macro in the list, then switch to the **Hot Keys** tab. Find the **Play:MacroName** entry under the *Macros* category and assign a key combination. Ensure the combination does not conflict with existing bindings.
5. **Test the macro** – Press the hotkey in-game and observe the macro’s behaviour. Use the **Step-Through** option to debug if necessary.

## Applying Script Examples

1. **Open the script example** – Open the desired file from `examples/scripts/`.
2. **Copy the script text** – Copy the script contents into a new local file in your Razor `Scripts` folder and save it with a `.razor` extension.
3. **Reload scripts** – In the **Scripts** tab, click **Reload** to load new scripts into Razor’s list. The script names should match the local `.razor` file names you created.
4. **Assign a hotkey** – Under the *Scripts* category in the **Hot Keys** tab, locate **Play:ScriptName** and bind a key combination (the ID will be 0 in the profile XML). Do not guess built-in IDs.
5. **Verify behaviour** – Test the script in a safe environment. If the script uses Outlands-only features like `findtype`, `cooldown` or `as`, ensure you are running the Outlands Razor fork.

## Creating Your Own Macros and Scripts

1. **Record and refine macros** – Use the **Record** button to capture actions. Right-click lines to move them, insert pauses or waits, insert conditionals, or use special constructs like comments, `if/else`, and `for` loops. Replace fixed pauses with `WaitForTargetAction` where possible. Use absolute target variables for items that may change serials.
2. **Convert macros to scripts** – Right-click a macro and choose **Convert to Script**. Edit the resulting script to replace hotkey IDs with descriptive commands and to use expressions like `insysmsg` or `bandaging` for control flow.
3. **Write scripts from scratch** – Follow the command syntax described in the **core_reference** and the Outlands module. Use single quotes around strings, separate commands on new lines, and indent nested blocks for readability. Use `setvar` to store serials, `waitfortarget` to await a cursor, and lists, timers, and cooldowns on Outlands.
4. **Test and iterate** – Use the validation workflow to test your scripts. If they fail, consult the troubleshooting registry.

## Staying Outlands-Friendly

1. **Check `pvp`** – If you play on Outlands, wrap your scripts with `if pvp` guards to avoid running restricted commands during structured PvP.
2. **Use expanded commands** – Prefer `findtype`, `targettype`, `lifttype` and `findlayer` with the `ground` alias over old macros. These commands accept additional parameters like hue, quantity, and range and are more reliable.
3. **Leverage lists and timers** – For advanced automation, use `createlist` and timer commands to cycle through collections of items or runes.
4. **Watch for disabled features** – Remember that certain commands and expressions such as `setvar` on players, timers, cooldowns, and `bandaging` are disabled during structured PvP. Write scripts with alternate behaviour when `pvp` is true.

## Final Notes

* **Use this skill pack as a foundation.** It is a starting point for building robust, agent-driven Razor automation. Extend the exemplars, update the hotkey map as you discover internal IDs, and contribute new macro patterns as needed.
* **Keep your sources authoritative.** When in doubt, consult the official Razor documentation and the Outlands wiki. Community guides are useful but may contain outdated or shard-specific information.
* **Do not guess.** Unknown IDs, variables, or behaviours must be verified in the client. Ambiguity should be treated explicitly rather than masked.
