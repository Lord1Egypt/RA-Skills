import { spawn } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

// 快捷键配置
interface ShortcutConfig {
  today: string;  // Ctrl+T
  week: string;   // Ctrl+W
  total: string;  // Ctrl+A
  history: string; // Ctrl+H
  save: string;   // Ctrl+S
  interactive: string; // Ctrl+I
}

const SHORTCUTS: ShortcutConfig = {
  today: 'ctrl+t',
  week: 'ctrl+w',
  total: 'ctrl+a',
  history: 'ctrl+h',
  save: 'ctrl+s',
  interactive: 'ctrl+i'
};

/**
 * 检查是否在交互式终端中运行
 */
function isInteractiveTerminal(): boolean {
  return process.stdin.isTTY && process.stdout.isTTY;
}

/**
 * 检测操作系统
 */
function getOS(): 'linux' | 'macos' | 'windows' {
  const platform = process.platform;
  if (platform === 'darwin') return 'macos';
  if (platform === 'win32') return 'windows';
  return 'linux';
}

/**
 * Linux 系统设置快捷键
 */
function setupLinuxShortcuts(): Promise<boolean> {
  return new Promise((resolve) => {
    const configDir = path.join(process.env.HOME!, '.config', 'autostart');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }

    const shortcutApps = {
      [SHORTCUTS.today]: 'token-tracker today',
      [SHORTCUTS.week]: 'token-tracker week',
      [SHORTCUTS.total]: 'token-tracker total',
      [SHORTCUTS.history]: 'token-tracker history',
      [SHORTCUTS.save]: 'token-tracker save',
      [SHORTCUTS.interactive]: 'token-tracker i'
    };

    for (const [shortcut, command] of Object.entries(shortcutApps)) {
      const desktopFile = path.join(configDir, `token-tracker-${shortcut.replace('ctrl-', '')}.desktop`);

      const desktopContent = `[Desktop Entry]
Type=Application
Name=Token Tracker - ${shortcut}
Exec=sh -c "token-tracker ${command}"
Icon=terminal
Terminal=true
`;
      fs.writeFileSync(desktopFile, desktopContent);
    }

    // 更新环境变量以支持全局快捷键
    const bashrcPath = path.join(process.env.HOME!, '.bashrc');
    const bashrcContent = fs.readFileSync(bashrcPath, 'utf8');

    if (!bashrcContent.includes('token-tracker-shortcuts')) {
      const newContent = bashrcContent + `
# Token Tracker Shortcuts
export PATH="$HOME/.openclaw/skills/token-tracker/bin:$PATH"
`;
      fs.writeFileSync(bashrcPath, newContent);
    }

    console.log('✅ Linux 快捷键已配置');
    resolve(true);
  });
}

/**
 * macOS 系统设置快捷键（使用 Automator）
 */
function setupMacOSShortcuts(): Promise<boolean> {
  return new Promise((resolve) => {
    const workflowDir = path.join(process.env.HOME!, 'Library', 'Services');

    if (!fs.existsSync(workflowDir)) {
      fs.mkdirSync(workflowDir, { recursive: true });
    }

    const shortcutApps = {
      [SHORTCUTS.today]: 'token-tracker today',
      [SHORTCUTS.week]: 'token-tracker week',
      [SHORTCUTS.total]: 'token-tracker total',
      [SHORTCUTS.history]: 'token-tracker history',
      [skip]: 'token-tracker save',
      [SHORTCUTS.interactive]: 'token-tracker i'
    };

    for (const [shortcut, command] of Object.entries(shortcutApps)) {
      const workflowFile = path.join(workflowDir, `token-tracker-${shortcut}.workflow`);

      const workflowContent = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>/usr/local/bin/bash</string>
  <key>CFBundleArguments</key>
  <array>
    <string>-c</string>
    <string>token-tracker ${command}</string>
  </array>
</dict>
</plist>`;

      fs.writeFileSync(workflowFile, workflowContent);
    }

    console.log('✅ macOS 快捷键已配置');
    console.log('⚠️  请在系统设置中添加快捷键');
    resolve(true);
  });
}

/**
 * Windows 系统设置快捷键（使用 AutoHotkey）
 */
function setupWindowsShortcuts(): Promise<boolean> {
  return new Promise((resolve) => {
    const ahkScript = path.join(process.env.APPDATA!, 'AutoHotkey', 'TokenTracker.ahk');

    if (!fs.existsSync(path.dirname(ahkScript))) {
      fs.mkdirSync(path.dirname(ahkScript), { recursive: true });
    }

    const shortcuts = [
      `^t::Run, token-tracker today`,
      `^w::Run, token-tracker week`,
      `^a::Run, token-tracker total`,
      `^h::Run, token-tracker history`,
      `^s::Run, token-tracker save`,
      `^i::Run, token-tracker i`
    ];

    const ahkContent = `#NoEnv
#SingleInstance, Force
SendMode Input

${shortcuts.join('\n')}

return
`;

    fs.writeFileSync(ahkScript, ahkContent);

    console.log('✅ Windows 快捷键已配置');
    console.log('⚠️  请运行 AutoHotkey 脚本以启用快捷键');
    console.log(`   脚本位置: ${ahkScript}`);
    resolve(true);
  });
}

/**
 * 显示快捷键帮助
 */
function showShortcutsHelp(): void {
  console.log('\n⌨️  Token Tracker 快捷键');
  console.log('='.repeat(50));
  console.log(`Ctrl+T: ${SHORTCUTS.today} - 查看今日统计`);
  console.log(`Ctrl+W: ${SHORTCUTS.week} - 查看本周统计`);
  console.log(`Ctrl+A: ${SHORTCUTS.total} - 查看累计统计`);
  console.log(`Ctrl+H: ${SHORTCUTS.history} - 查看历史记录`);
  console.log(`Ctrl+S: ${SHORTCUTS.save} - 查看节省建议`);
  console.log(`Ctrl+I: ${SHORTCUTS.interactive} - 交互式菜单`);
  console.log('='.repeat(50));
  console.log();
}

/**
 * 检查并安装依赖
 */
function checkDependencies(): boolean {
  try {
    // 检查是否安装了 express
    require('express');
    return true;
  } catch {
    console.log('⚠️  需要安装 express 依赖');
    console.log('   npm install express');
    return false;
  }
}

/**
 * 主函数
 */
export async function setupShortcuts(): Promise<void> {
  console.log('🚀 Token Tracker 快捷键设置\n');

  // 检查依赖
  if (!checkDependencies()) {
    process.exit(1);
  }

  // 检测操作系统
  const os = getOS();

  console.log(`检测到操作系统: ${os.toUpperCase()}\n`);

  // 根据操作系统设置快捷键
  try {
    switch (os) {
      case 'linux':
        await setupLinuxShortcuts();
        break;
      case 'macos':
        await setupMacOSShortcuts();
        break;
      case 'windows':
        await setupWindowsShortcuts();
        break;
    }

    // 显示快捷键帮助
    showShortcutsHelp();

    console.log('✅ 快捷键配置完成！');
    console.log('💡 提示: 某些快捷键可能需要在系统设置中手动配置\n');

  } catch (error: any) {
    console.error('❌ 配置快捷键失败:', error.message);
    process.exit(1);
  }
}

/**
 * 显示快捷键帮助（命令行）
 */
export function showShortcutHelp(): void {
  showShortcutsHelp();
}

// 命令行入口
if (require.main === module) {
  setupShortcuts().catch((error) => {
    console.error('Error:', error);
    process.exit(1);
  });
}
