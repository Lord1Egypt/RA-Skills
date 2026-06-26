const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function ensureNodeNotifierInstalled(skillDir) {
  const modulePath = path.join(skillDir, 'node_modules', 'node-notifier');
  if (fs.existsSync(modulePath)) return;

  const result = process.platform === 'win32'
    ? spawnSync(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', 'npm.cmd install --no-fund --no-audit'], {
        cwd: skillDir,
        stdio: 'inherit',
        windowsHide: true,
      })
    : spawnSync('npm', ['install', '--no-fund', '--no-audit'], {
        cwd: skillDir,
        stdio: 'inherit',
      });

  if (result.error) {
    throw new Error(`npm install failed: ${result.error.message || String(result.error)}`);
  }

  if (result.status !== 0) {
    throw new Error(`npm install failed with exit code ${result.status ?? 'unknown'}`);
  }
}

function escapePsSingleQuoted(value) {
  return String(value).replace(/'/g, "''");
}

function canUseWpfWindowsDialog() {
  if (process.platform !== 'win32') return false;

  const command = 'powershell.exe';
  const probeScript = [
    "$ErrorActionPreference = 'Stop'",
    'Add-Type -AssemblyName PresentationCore',
    'Add-Type -AssemblyName PresentationFramework',
    'Add-Type -AssemblyName WindowsBase',
    "Write-Output 'WPF_OK'",
  ].join('; ');

  const result = spawnSync(command, [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-STA',
    '-Command', probeScript,
  ], {
    windowsHide: true,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  return result.status === 0 && String(result.stdout || '').includes('WPF_OK');
}

function buildModernDialogPowerShell(title, message, appName, sound = true) {
  return String.raw`
param()
$Title = '${escapePsSingleQuoted(title)}'
$Message = '${escapePsSingleQuoted(message)}'
$AppName = '${escapePsSingleQuoted(appName)}'
$PlaySound = ${sound ? '$true' : '$false'}
$DurationSeconds = 60

Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName WindowsBase
if ($PlaySound) {
  try {
    [System.Media.SystemSounds]::Exclamation.Play()
  } catch {
    try {
      [console]::Beep(880, 180)
    } catch {
      # ignore sound failures
    }
  }
}

Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class Win32WindowStyles
{
    public const int GWL_EXSTYLE = -20;
    public const int WS_EX_TOOLWINDOW = 0x00000080;
    public const int WS_EX_APPWINDOW = 0x00040000;

    [DllImport("user32.dll", EntryPoint = "GetWindowLongPtrW", SetLastError = true)]
    public static extern IntPtr GetWindowLongPtr64(IntPtr hWnd, int nIndex);

    [DllImport("user32.dll", EntryPoint = "SetWindowLongPtrW", SetLastError = true)]
    public static extern IntPtr SetWindowLongPtr64(IntPtr hWnd, int nIndex, IntPtr dwNewLong);

    [DllImport("user32.dll", EntryPoint = "GetWindowLongW", SetLastError = true)]
    public static extern int GetWindowLong32(IntPtr hWnd, int nIndex);

    [DllImport("user32.dll", EntryPoint = "SetWindowLongW", SetLastError = true)]
    public static extern int SetWindowLong32(IntPtr hWnd, int nIndex, int dwNewLong);

    public static IntPtr GetWindowLongPtr(IntPtr hWnd, int nIndex)
    {
        return IntPtr.Size == 8 ? GetWindowLongPtr64(hWnd, nIndex) : new IntPtr(GetWindowLong32(hWnd, nIndex));
    }

    public static IntPtr SetWindowLongPtr(IntPtr hWnd, int nIndex, IntPtr dwNewLong)
    {
        return IntPtr.Size == 8 ? SetWindowLongPtr64(hWnd, nIndex, dwNewLong) : new IntPtr(SetWindowLong32(hWnd, nIndex, dwNewLong.ToInt32()));
    }
}
"@

function New-Brush([string]$Color) {
  return ([System.Windows.Media.BrushConverter]::new()).ConvertFromString($Color)
}

$bg = New-Brush '#FF1C1C1C'
$border = New-Brush '#FF525252'
$headerText = New-Brush '#F3F3F3'
$bodyText = New-Brush '#EAEAEA'
$avatarBg = New-Brush '#FF3E332C'
$avatarBorder = New-Brush '#D8C8A06A'
$avatarText = New-Brush '#F5E8D2'

if ($Message.Length -gt 30) {
  $Message = $Message.Substring(0, 30) + '...'
}

$window = New-Object System.Windows.Window
$window.Width = 360
$window.Height = 86
$window.WindowStartupLocation = [System.Windows.WindowStartupLocation]::Manual
$window.ResizeMode = [System.Windows.ResizeMode]::NoResize
$window.Background = [System.Windows.Media.Brushes]::Transparent
$window.WindowStyle = [System.Windows.WindowStyle]::None
$window.ShowInTaskbar = $false
$window.Topmost = $true
$window.AllowsTransparency = $true
$window.ShowActivated = $true
$window.Focusable = $true
$window.Title = $Title

$outerBorder = New-Object System.Windows.Controls.Border
$outerBorder.Width = 360
$outerBorder.Height = 86
$outerBorder.Background = $bg
$outerBorder.BorderBrush = $border
$outerBorder.BorderThickness = [System.Windows.Thickness]::new(1.2)
$outerBorder.CornerRadius = [System.Windows.CornerRadius]::new(10)
$outerBorder.SnapsToDevicePixels = $true
$outerBorder.Opacity = 0.95

$shadow = New-Object System.Windows.Media.Effects.DropShadowEffect
$shadow.Color = [System.Windows.Media.Color]::FromArgb(255, 0, 0, 0)
$shadow.BlurRadius = 24
$shadow.ShadowDepth = 6
$shadow.Opacity = 0.24
$outerBorder.Effect = $shadow

$canvas = New-Object System.Windows.Controls.Canvas
$canvas.Width = 360
$canvas.Height = 86

$appNameBlock = New-Object System.Windows.Controls.TextBlock
$appNameBlock.Text = $AppName
$appNameBlock.FontSize = 10
$appNameBlock.Foreground = $headerText
[System.Windows.Controls.Canvas]::SetLeft($appNameBlock, 10)
[System.Windows.Controls.Canvas]::SetTop($appNameBlock, 6)
$canvas.Children.Add($appNameBlock) | Out-Null


$avatarBox = New-Object System.Windows.Controls.Border
$avatarBox.Width = 35
$avatarBox.Height = 35
$avatarBox.CornerRadius = [System.Windows.CornerRadius]::new(7)
$avatarBox.Background = $avatarBg
$avatarBox.BorderBrush = $avatarBorder
$avatarBox.BorderThickness = [System.Windows.Thickness]::new(1)

$avatarTextBlock = New-Object System.Windows.Controls.TextBlock
$avatarTextBlock.Text = 'Zz'
$avatarTextBlock.FontSize = 15
$avatarTextBlock.FontWeight = [System.Windows.FontWeights]::SemiBold
$avatarTextBlock.Foreground = $avatarText
$avatarTextBlock.HorizontalAlignment = [System.Windows.HorizontalAlignment]::Center
$avatarTextBlock.VerticalAlignment = [System.Windows.VerticalAlignment]::Center
$avatarBox.Child = $avatarTextBlock
[System.Windows.Controls.Canvas]::SetLeft($avatarBox, 10)
[System.Windows.Controls.Canvas]::SetTop($avatarBox, 34)
$canvas.Children.Add($avatarBox) | Out-Null

$textLeft = 52

$titleBlock = New-Object System.Windows.Controls.TextBlock
$titleBlock.Text = $Title
$titleBlock.FontSize = 13
$titleBlock.FontWeight = [System.Windows.FontWeights]::SemiBold
$titleBlock.Foreground = $headerText
[System.Windows.Controls.Canvas]::SetLeft($titleBlock, $textLeft)
[System.Windows.Controls.Canvas]::SetTop($titleBlock, 35)
$canvas.Children.Add($titleBlock) | Out-Null

$messageBlock = New-Object System.Windows.Controls.TextBlock
$messageBlock.Text = $Message
$messageBlock.TextWrapping = [System.Windows.TextWrapping]::NoWrap
$messageBlock.TextTrimming = [System.Windows.TextTrimming]::CharacterEllipsis
$messageBlock.FontSize = 10.5
$messageBlock.Foreground = $bodyText
$messageBlock.Width = 250
[System.Windows.Controls.Canvas]::SetLeft($messageBlock, $textLeft)
[System.Windows.Controls.Canvas]::SetTop($messageBlock, 57)
$canvas.Children.Add($messageBlock) | Out-Null

$outerBorder.Child = $canvas
$window.Content = $outerBorder

$window.Add_SourceInitialized({
  $helper = New-Object System.Windows.Interop.WindowInteropHelper($window)
  $hwnd = $helper.Handle
  if ($hwnd -ne [IntPtr]::Zero) {
    $exStyle = [Win32WindowStyles]::GetWindowLongPtr($hwnd, [Win32WindowStyles]::GWL_EXSTYLE).ToInt64()
    $newStyle = ($exStyle -bor [Win32WindowStyles]::WS_EX_TOOLWINDOW) -band (-bnot [Win32WindowStyles]::WS_EX_APPWINDOW)
    [void][Win32WindowStyles]::SetWindowLongPtr($hwnd, [Win32WindowStyles]::GWL_EXSTYLE, [IntPtr]$newStyle)
  }
})

$outerBorder.Cursor = [System.Windows.Input.Cursors]::Hand
$outerBorder.Add_MouseLeftButtonUp({
  $window.Close()
})

$window.Add_KeyDown({
  param($sender, $eventArgs)
  if ($eventArgs.Key -eq [System.Windows.Input.Key]::Escape -or $eventArgs.Key -eq [System.Windows.Input.Key]::Enter) {
    $window.Close()
  }
})

$window.Add_Loaded({
  $window.UpdateLayout()
  $workArea = [System.Windows.SystemParameters]::WorkArea
  $marginRight = 16
  $marginTop = 12
  $window.Left = $workArea.Right - $window.ActualWidth - $marginRight
  $window.Top = $workArea.Top + $marginTop
})

$window.Add_Closed({
  [System.Windows.Threading.Dispatcher]::CurrentDispatcher.BeginInvokeShutdown([System.Windows.Threading.DispatcherPriority]::Background)
})

if ($DurationSeconds -gt 0) {
  $timer = New-Object System.Windows.Threading.DispatcherTimer
  $timer.Interval = [TimeSpan]::FromSeconds($DurationSeconds)
  $timer.Add_Tick({
    $timer.Stop()
    $window.Close()
  })
  $timer.Start()
}

$window.ShowDialog() | Out-Null
`;
}

function showModernWindowsDialog(title, message, appName = 'OpenClaw', wait = false, sound = true) {
  if (process.platform !== 'win32') {
    throw new Error('modern dialog is only supported on Windows');
  }

  if (!canUseWpfWindowsDialog()) {
    throw new Error('WPF is unavailable in the current Windows session');
  }

  const command = 'powershell.exe';
  const script = buildModernDialogPowerShell(title, message, appName, sound);
  const encodedScript = Buffer.from(script, 'utf16le').toString('base64');
  const psArgs = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-STA', '-EncodedCommand', encodedScript];

  if (wait) {
    const result = spawnSync(command, psArgs, {
      windowsHide: false,
      stdio: 'ignore',
    });

    if (result.status !== 0) {
      throw new Error(`modern dialog failed with exit code ${result.status ?? 'unknown'}`);
    }
    return;
  }

  const launcherScript = `Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-STA', '-EncodedCommand', '${encodedScript}') -WindowStyle Hidden`;
  const result = spawnSync(command, [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-Command', launcherScript,
  ], {
    windowsHide: true,
    stdio: 'ignore',
  });

  if (result.status !== 0) {
    throw new Error(`modern dialog launcher failed with exit code ${result.status ?? 'unknown'}`);
  }
}

function showNodeNotifier(title, message, appName, wait, timeout, sound, skillDir) {
  ensureNodeNotifierInstalled(skillDir);
  const notifier = require(path.join(skillDir, 'node_modules', 'node-notifier'));

  return new Promise((resolve, reject) => {
    notifier.notify({
      title,
      message,
      wait,
      timeout,
      appID: appName,
      appName,
      sound,
    }, (error) => {
      if (error) {
        reject(error);
        return;
      }
      resolve();
    });
  });
}

(async () => {
  try {
    const skillDir = path.resolve(__dirname, '..');
    const args = parseArgs(process.argv);
    const title = args.title || 'OpenClaw 提醒';
    const message = args.message || '你有一条新的提醒。';
    const appName = args.appName || args.app || 'OpenClaw';
    const timeoutArg = String(args.timeout ?? 'false').toLowerCase();
    const timeout = (timeoutArg === 'false' || timeoutArg === 'permanent' || timeoutArg === 'sticky' || timeoutArg === '0')
      ? false
      : Number(timeoutArg);
    const wait = String(args.wait || 'false').toLowerCase() === 'true';
    const soundArg = String(args.sound || 'true').toLowerCase();
    const sound = !(soundArg === 'false' || soundArg === '0' || soundArg === 'off');
    const modeArg = String(args.mode || '').toLowerCase();
    const wantsModern = modeArg === 'modern' || modeArg === 'card' || modeArg === 'dialog';

    if (process.platform === 'win32' && wantsModern) {
      try {
        showModernWindowsDialog(title, message, appName, wait, sound);
        process.exit(0);
        return;
      } catch {
        // Fall through to node-notifier fallback.
      }
    }

    await showNodeNotifier(title, message, appName, wait, timeout, sound, skillDir);
    process.exit(0);
  } catch (error) {
    console.error('WINDOWS_NOTIFY_ERROR');
    console.error(error?.message || String(error));
    process.exit(1);
  }
})();
