---
name: sshot
slug: sshot
description: Take full screen screenshot using PowerShell
metadata: {"clawdbot":{"emoji":"📷","os":["win32"]}}
---

When the user types `/sshot`, take a full screen screenshot.

Use `system.run` on node `My Windows Node`.

Execute:

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File "C:\Users\AlenZhu\.openclaw\scripts\sshot.ps1"

Wait until the command finishes and return stdout (screenshot file path).