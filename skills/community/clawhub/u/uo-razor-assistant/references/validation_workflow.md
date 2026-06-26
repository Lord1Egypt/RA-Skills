# Validation and Deployment Workflow

Testing macros, scripts and hot‑keys before use is critical.  The following step‑by‑step workflow helps ensure Razor artifacts work as intended and do not cause unintended actions.  Perform these checks for each macro or script you create or modify.

## 1. File Integrity and Location

1. **Locate Files** – Confirm that the `.macro` file is saved in the `Macros` folder and the `.razor` script is saved in the `Scripts` folder.  Make sure the file names match the names used in hot‑key bindings or `Play:` wrappers.
2. **Check File Content** – Open macro files in a text editor and verify that serialized lines use valid action classes (see the Macro Serialization Legend).  Ensure there are no truncated or partially written lines.  For script files, verify that each command appears on its own line and uses correct syntax (e.g., commands in lowercase, arguments in quotes if needed).  Use the Razor built‑in editor for syntax highlighting.

## 2. Loading and Visibility

1. **Reload Macros/Scripts** – In Razor, open the **Macros** or **Scripts** tab and click **Reload** to refresh the list from disk.
2. **Verify Presence** – Confirm that the macro or script appears in the list with the expected name and category.  If it does not appear, check for typos in the file name or extension.
3. **Check Special Constructs** – For macros, make sure any `Pause/Wait`, `If/Else` or `For` constructs appear in the editor and have matching end markers.

## 3. Hot‑Key Binding Verification

1. **Assign Hot‑Key** – In the **Hot Keys** tab, locate the desired action.  Bind a key combination using the **Set** button and consider whether to **Pass to UO** or define a **Command**.
2. **Distinguish Binding Type** – Determine whether the hot‑key refers to a built‑in action, macro or script.  Built‑in actions display their name plainly (e.g., “Attack”), whereas macros and scripts appear prefixed with `Play:`.  In the profile XML, built‑ins have numeric IDs and macros/scripts have ID 0.
3. **Avoid Conflicts** – Ensure the key combination is not already used by another action.  Razor will warn about duplicates.

## 4. In‑Game Testing

1. **Enter a Safe Environment** – Test macros and scripts in a controlled area (e.g., at the bank or in a private house) to avoid unintended interactions.
2. **Observe Behaviour** – Run the macro or script via the **Play** button or the assigned hot‑key.  Watch for errors, unexpected messages or prompts.  In macros, use **Step‑Through** (right‑click ➔ Step Through) to execute line by line if necessary.
3. **Check Targeting** – Ensure that target actions (e.g., `target`, `targetself`, `targettype`, `lift`) operate on the intended objects.  If using absolute target variables, verify that the variable names correspond to valid items.
4. **Validate Waits and Pauses** – Replace fixed `PauseAction` entries with `waitfortarget` or Outlands expressions like `bandaging` whenever possible to avoid timing issues.  In scripts, ensure that `wait` durations are sufficient but not excessive.

## 5. Outlands Compliance

1. **Check for PvP Restrictions** – If your script is intended for Outlands, wrap critical sections in `if pvp` to prevent execution during structured PvP.  Disabled commands (e.g., `setvar`, `droprelloc`, `waitforsysmsg`, timers, `cooldown`) and expressions (e.g., `bandaging`, `mana`, `followers`, `cooldown`) should not be used unguarded.
2. **Validate Commands and Expressions** – Confirm that Outlands‑specific commands (`findtype`, `lifttype`, `targettype` with `ground` alias) and expressions (`find`, `findlayer`, `followers`, `cooldown`) are used correctly.
3. **Test Cooldowns** – When using `cooldown` checks, run the script once to trigger a cooldown, then attempt to use the ability again.  Ensure the script recognises the cooldown and waits appropriately.

## 6. Post‑Deployment Monitoring

1. **Monitor System Messages** – During gameplay, watch the system messages to ensure the macro or script is functioning (e.g., messages indicating spells cast, items used, or errors).  If the script expects a specific system message, verify that the check `insysmsg` matches the text precisely.
2. **Adjust and Iterate** – Based on testing, adjust delays, conditions or targeted objects.  It is often necessary to fine‑tune wait times or filter messages for reliability.
3. **Document Changes** – Update the corresponding module (macro file, script file or hot‑key map) and keep version history so that the OpenClaw agent can track modifications.

## 7. Backup and Migration

1. **Backup Data** – Regularly back up your `Profiles`, `Macros` and `Scripts` folders along with `counters.xml` and `Razor.exe.config`.  Copy these folders before making significant changes.
2. **Migration** – To migrate Razor to another machine, close Razor and copy these folders to the new installation.  Do not mix profiles across shards; Outlands‑specific profiles should remain on the Outlands client..