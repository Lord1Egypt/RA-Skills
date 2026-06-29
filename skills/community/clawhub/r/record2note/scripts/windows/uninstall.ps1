$ErrorActionPreference = "Stop"

Write-Host "=== record2note Uninstall ==="

# Stop and remove scheduled task
if (Get-ScheduledTask -TaskName "record2note-watch" -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName "record2note-watch" -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName "record2note-watch" -Confirm:$false
    Write-Host "Scheduled task removed."
}

Write-Host ""
Write-Host "Uninstall complete."
Write-Host "Note: config, recordings, and notes were NOT deleted."
Write-Host "  Config: <skill_folder>\config.json"
Write-Host "  Recordings: your configured directories"
Write-Host "  Notes: kept in your Obsidian vault"
Write-Host "To remove these manually, delete the directories above."