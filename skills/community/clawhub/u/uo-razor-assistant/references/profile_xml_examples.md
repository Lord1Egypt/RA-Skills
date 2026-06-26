# Profile XML Examples

Razor stores hot‑key bindings inside your **profile** file (found in the `Profiles` folder).  Each hot‑key appears as a `<hotkey>` element with attributes describing the key combination and the action to execute.  The examples below illustrate how built‑in actions, macros and scripts are represented.  **Never guess numeric IDs**; inspect a profile or record a macro to discover the correct value.

## Built‑in Hot‑Key Example

A built‑in hot‑key references an internal action ID.  In this example, the hot‑key binds `Ctrl + A` to the **Attack Last Target** action.  The `id` attribute is Razor’s internal command ID.  Built‑ins have no `Play:` prefix because they call the command directly.  IDs vary by Razor version and shard; 1059 is used here as a placeholder.

```xml
<hotkey name="Attack Last Target" id="1059" ctrl="true" alt="false" shift="false" key="A" />
```

## Macro Hot‑Key Example

Macros are invoked through the `Play:` wrapper and always use ID `0`.  The `name` attribute includes `Play:` followed by the macro name as it appears in the Macros tab.  This binding ties `Shift + R` to a user macro called **Recall**.

```xml
<hotkey name="Play:Recall" id="0" ctrl="false" alt="false" shift="true" key="R">Play:Recall</hotkey>
```

## Script Hot‑Key Example

Scripts are invoked similarly to macros: the `name` starts with `Play:` and the ID is `0`.  The difference is that the name refers to a script in the Scripts folder.  This example binds `Alt + E` to a script named **ExplosionHelper**.  When executed, Razor will run `ExplosionHelper.razor` from your Scripts folder.

```xml
<hotkey name="Play:ExplosionHelper" id="0" ctrl="false" alt="true" shift="false" key="E">Play:ExplosionHelper</hotkey>
```

### Notes

* **ID vs Name** – Built‑ins use a numeric `id` while macros/scripts use ID 0 and encode the target in the `name`/value field.  Razor differentiates the two at runtime.
* **Modifier attributes** – `ctrl`, `alt` and `shift` attributes record which modifier keys are held.  The `key` attribute records the physical key pressed.
* **Unknown IDs** – If you cannot find a built‑in ID, record a macro that triggers the desired command and inspect the resulting `Assistant.Macros.HotKeyAction|<id>|` line.
* **Conflicts** – Avoid binding the same key combination to multiple actions.  Razor will warn you when duplicates occur.