# Macro Serialization Legend

Razor saves each recorded macro as a plain‑text file in the **`Macros`** folder with the extension `.macro`.  The file format is a sequence of **serialized action lines**.  Each line is a fully qualified class name prefixed with `Assistant.Macros.` followed by pipe‑separated parameters.  The macro editor inside Razor hides this detail; however, understanding the serialization is useful when converting macros to scripts or for safely patching macros on disk.  The following table explains common macro actions and how they map to in‑game behaviour.

| Serialized line | Description | Notes |
|-----------------|-------------|-------|
| `Assistant.Macros.MacroCastSpellAction|<spellId>` | Casts the spell identified by `<spellId>`.  Spell IDs correspond to the ClassicUO spell table.  For example, `33` is *Blade Spirits*. | Equivalent script command: `cast 'blade spirits'`. |
| `Assistant.Macros.UseSkillAction|<skillId>` | Uses the skill identified by `<skillId>`.  In the example macro for *Detect Hidden*, `14` indicates the **Detect Hidden** skill. | Equivalent script command: `skill 'detecthidden'`. |
| `Assistant.Macros.WaitForTargetAction|<timeout>` | Pauses until a targeting cursor appears or until `<timeout>` ticks have passed.  Recorded macros typically use `30` as a default timeout (approx. 30 seconds). | Equivalent script command: `waitfortarget`. |
| `Assistant.Macros.TargetRelLocAction|<x>|<y>` | Targets a location relative to the player’s current position by offset `<x> <y>`.  In the *Blade Spirits* macro the offsets `3|1` target three tiles east and one tile north. | Equivalent script command: `targetrelloc 3 1`. |
| `Assistant.Macros.HotKeyAction|<id>|` | Executes a built‑in Razor hot‑key by its internal ID.  In the *Detect Hidden* macro, `1059` and `2003` refer to specific built‑in commands.  A trailing empty parameter terminates the line. | Macro hot‑keys call built‑ins directly; script hot‑keys are invoked via `hotkey 'Name'`. |
| `Assistant.Macros.PauseAction|hh:mm:ss.fffffff` | Pauses for the specified duration.  The *Detect Hidden* macro waits for **0.4 seconds** (`00:00:00.4000000`) between actions. | Equivalent script command: `wait 400`. |
| `Assistant.Macros.IfAction|<code>|<unknown>|<text>` | Begins a conditional statement.  `<code>` is the condition type, and `<text>` is usually a system message substring.  In the example, `4|0|'you can see nothing'` checks whether the most recent system message contains “you can see nothing”. | Script equivalent uses `if insysmsg '<message substring>'`. |
| `Assistant.Macros.ElseAction` | Begins the else branch of a conditional. | Equivalent script syntax: `else`. |
| `Assistant.Macros.SpeechAction|<mode>|<hue>|<font>|<lang>|…|<text>` | Sends a chat message with specific colour/font parameters.  In the *Detect Hidden* example, the macro says “I Ban Thee”. | Scripts use `say 'I ban thee'` or `overhead` for overhead text. |
| `Assistant.Macros.EndIfAction` | Ends the current `IfAction` block. | Script equivalent: `endif`. |
| `Assistant.Macros.LastTargetAction|<unused>` | Re‑targets the last thing you targeted (NPC, player, item).  Often recorded via **Set Last Target** special construct. | Script equivalent: `target lasttarget`. |
| `Assistant.Macros.TargetTypeAction|<id>|<x>` | Targets the nearest item or mobile of type `<id>`.  A second parameter may specify a count. | Script equivalent: `targettype <type>` or `findtype <type> as var`. |
| `Assistant.Macros.DoubleClickTypeAction|<id>` | Double‑clicks any item of type `<id>` (e.g., bandages or potion bottles). | Script equivalent: `dclicktype <type>`. |
| `Assistant.Macros.ForAction|<count>` | Begins a `for` loop that repeats the following actions `<count>` times.  Use `Assistant.Macros.EndForAction` to terminate the loop. | Scripts use `for 1 to <count> { … }` or `foreach`. |
| `Assistant.Macros.EndForAction` | Marks the end of a for‑loop begun with `ForAction`. | Script equivalent: `endfor`. |
| `Assistant.Macros.CommentAction|<text>` | Inserts a comment.  Comments do not affect macro execution. | Script equivalent: lines beginning with `//`. |

### Notes on HotKeyAction IDs

Razor’s built‑in actions are internally identified by numeric IDs.  When you assign a hot‑key to a built‑in action, Razor records a line like `Assistant.Macros.HotKeyAction|1059|`.  A similar line with ID `0` and the notation `Play:Name` is used to run a user macro or script (e.g., `Assistant.Macros.HotKeyAction|0|Play:Recall`).  **Never assume a numeric ID without verification.**  ID numbers can vary between Razor versions and shards.  To discover an ID, record a macro that executes the built‑in hot‑key and inspect the serialized line.  For an OpenClaw agent, treat unknown IDs as ambiguous and require user confirmation.
