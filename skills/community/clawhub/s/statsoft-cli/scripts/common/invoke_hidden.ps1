# invoke_hidden.ps1 — shared headless launcher for statsoft-cli
#
# Purpose
# -------
# Every third-party statistical binary invoked by this skill is launched
# through THIS helper so that NO visible window ever appears (the skill's
# default: never pop a GUI). Detection-only scripts (setup_*.ps1) never run
# binaries, so they are unaffected; this is used only by the execution
# wrappers (statsoft-*.ps1) and by the cross-platform verify steps.
#
# Why cmd.exe /c (and not Start-Process)
# --------------------------------------
# Start-Process (and the Env: provider) build a case-SENSITIVE dictionary of the
# current process environment and throw "已添加项。字典中的关键字" when the
# environment contains the same variable name in two cases (e.g. HTTPS_PROXY and
# https_proxy) — which some host shells inject. That crash prevented the child
# from ever launching. cmd.exe inherits the native Windows environment block
# (which tolerates such case variants) and performs > / 2> redirection natively,
# so routing through `cmd /c` sidesteps the bug entirely.
#
# WindowStyle=Hidden only — do NOT set CreateNoWindow. CreateNoWindow strips the
# window station from GUI-subsystem children (Stata is one) and makes them fail
# to start (exit code 1, no output). WindowStyle=Hidden hides the window while
# keeping a valid window station; console children (SAS/StatTransfer) show no
# window either way.
#
# Behaviour
# ---------
#   * Launches via cmd.exe /c with output redirected to temp files.
#   * -Wait blocks until the process exits; exit code is captured.
#   * stdout/stderr are read back into strings so callers can still surface
#     output without showing a window.
#   * Temp files are always removed in the finally block, even on failure.
#
# This is the single enforcement point for the "no popup" default. Do not bypass
# it by calling `& <exe>` directly from an executor.

function Invoke-StatExe {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [string[]]$ArgumentList = @(),

        [string]$WorkingDirectory
    )

    $outFile = (New-TemporaryFile).FullName
    $errFile = (New-TemporaryFile).FullName

    # Build the inner command line: quote the exe and any argument containing
    # whitespace, then append cmd-style output redirection.
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append('"').Append($FilePath).Append('"')
    foreach ($a in $ArgumentList) {
        [void]$sb.Append(' ')
        if ($a -match '\s') { [void]$sb.Append('"').Append($a).Append('"') }
        else { [void]$sb.Append($a) }
    }
    [void]$sb.Append(' > "').Append($outFile).Append('" 2> "').Append($errFile).Append('"')
    $inner = $sb.ToString()

    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = 'cmd.exe'
        # Pass the whole inner command as a single /c argument (verified form); this
        # keeps the > / 2> redirections intact after ProcessStartInfo passes them
        # to cmd.exe, which performs the redirection natively.
        $psi.Arguments = ('/c "' + $inner + '"')
        $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        $psi.UseShellExecute = $false
        if ($WorkingDirectory) { $psi.WorkingDirectory = $WorkingDirectory }

        $p = New-Object System.Diagnostics.Process
        $p.StartInfo = $psi
        if (-not $p.Start()) {
            return [PSCustomObject]@{ ExitCode = -1; StdOut = ''; StdErr = 'Failed to start cmd.exe.' }
        }
        $p.WaitForExit()
        $code = $p.ExitCode
        $p.Dispose()

        $stdOut = ''
        $stdErr = ''
        if (Test-Path $outFile) { $stdOut = (Get-Content $outFile -Raw -ErrorAction SilentlyContinue) }
        if (Test-Path $errFile) { $stdErr = (Get-Content $errFile -Raw -ErrorAction SilentlyContinue) }

        return [PSCustomObject]@{
            ExitCode = $code
            StdOut   = $stdOut
            StdErr   = $stdErr
        }
    }
    catch {
        return [PSCustomObject]@{ ExitCode = -1; StdOut = ''; StdErr = $_.Exception.Message }
    }
    finally {
        Remove-Item $outFile -Force -ErrorAction SilentlyContinue
        Remove-Item $errFile -Force -ErrorAction SilentlyContinue
    }
}
