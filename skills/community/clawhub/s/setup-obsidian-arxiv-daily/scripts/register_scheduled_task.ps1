[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory = $true)]
    [string]$Vault,

    [string]$ProjectName = 'arxiv-daily',

    [Parameter(Mandatory = $true)]
    [string]$TaskName,

    [Parameter(Mandatory = $true)]
    [string]$At,

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

if (
    [string]::IsNullOrWhiteSpace($ProjectName) -or
    $ProjectName -in @('.', '..') -or
    $ProjectName -match '[<>:"/\\|?*]'
) {
    throw "Invalid project name: $ProjectName"
}

$VaultPath = (Resolve-Path -LiteralPath $Vault).Path
$WrapperPath = Join-Path $VaultPath "$ProjectName\scripts\arxiv_daily.ps1"
if (-not (Test-Path -LiteralPath $WrapperPath -PathType Leaf)) {
    throw "Installed wrapper not found: $WrapperPath"
}

try {
    $StartTime = [datetime]::ParseExact(
        $At,
        'HH:mm',
        [Globalization.CultureInfo]::InvariantCulture
    )
} catch {
    throw "Invalid daily start time '$At'. Use HH:mm, for example 10:30."
}

$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -ne $ExistingTask -and -not $Force) {
    throw "Scheduled task '$TaskName' already exists. Use -Force to replace it."
}

$Arguments = (
    '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass ' +
    "-File `"$WrapperPath`""
)
$Action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument $Arguments `
    -WorkingDirectory $VaultPath
$Trigger = New-ScheduledTaskTrigger -Daily -At $StartTime
$Description = "Generate the Obsidian arXiv daily digest in $VaultPath"

if ($PSCmdlet.ShouldProcess($TaskName, 'Register daily arXiv digest task')) {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Description $Description `
        -Force:$Force | Out-Null

    $Task = Get-ScheduledTask -TaskName $TaskName
    $TaskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
    [pscustomobject]@{
        TaskName = $Task.TaskName
        State = [string]$Task.State
        Action = "$($Action.Execute) $($Action.Arguments)"
        WorkingDirectory = $Action.WorkingDirectory
        NextRunTime = $TaskInfo.NextRunTime
    }
} else {
    [pscustomobject]@{
        TaskName = $TaskName
        State = 'Preview'
        Action = "$($Action.Execute) $($Action.Arguments)"
        WorkingDirectory = $Action.WorkingDirectory
        NextRunTime = $null
    }
}
