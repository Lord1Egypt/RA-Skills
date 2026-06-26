import { execFile } from 'node:child_process';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const DEFAULT_INSTALLER_URL =
  'https://cdn.aidenote.cn/tunnel/install-macos.sh';
const DEFAULT_WINDOWS_INSTALLER_URL =
  'https://cdn.aidenote.cn/tunnel/install-windows.ps1';
const MAC_LABEL = 'cn.aidenote.openclaw-tunnel';
const WINDOWS_TASK_NAME = 'AideNoteOpenClawBridge';

export function registerBridgeTools(api) {
  function getConfig() {
    const config = api.getConfig();
    if (!config?.apiKey) {
      throw new Error(
        '未配置 SlonAide API Key。请运行: openclaw config set slonaide.apiKey YOUR_API_KEY'
      );
    }
    return config;
  }

  api.registerTool({
    name: 'slonaide_setup_remote_bridge',
    description:
      '安装并启动 AideNote OpenClaw 远程对话 bridge，让手机 App 可以连接本机 OpenClaw',
    parameters: {
      type: 'object',
      properties: {
        reinstall: {
          type: 'boolean',
          description: '是否重新安装 bridge',
          default: false
        }
      }
    },
    async execute(_toolCallId, params) {
      try {
        if (!isSupportedPlatform()) {
          return textResult('当前自动安装支持 macOS 和 Windows。Linux 后续需要单独的服务安装脚本。');
        }

        const status = await bridgeStatus();
        if (status.running && !params?.reinstall) {
          return textResult(
            'AideNote OpenClaw bridge 已经在运行。\n' +
              status.output.trim() +
              '\n\n手机 App 里点机器人图标即可进入远程对话。'
          );
        }

        const config = getConfig();
        const installerUrl = installerUrlForPlatform(config);
        const installer = await downloadInstaller(installerUrl, installerFileName());
        const env = {
          ...process.env,
          AIDE_NOTE_API_KEY: config.apiKey,
          AIDE_NOTE_RELAY_HOST: config.bridgeRelayHost || 'api.aidenote.cn',
          AIDE_NOTE_TUNNEL_BASE_URL:
            config.bridgeTunnelBaseUrl || 'https://cdn.aidenote.cn/tunnel',
          // 注意: 不传 AIDE_NOTE_TOKEN_ENDPOINT
          // tunnel 二进制内置了默认的 token 交换地址，额外指定 --token-endpoint
          // 会覆盖默认导致认证失败（auth rejected: invalid token）
          OPENCLAW_LOCAL_PORT: String(config.openClawLocalPort || 18789)
        };

        const output = await run(installerCommand(), installerArgs(installer), {
          env,
          timeout: 120000
        });
        return textResult(
          'AideNote OpenClaw bridge 安装完成。\n\n' +
            summarizeOutput(output) +
            `\n\n以后 ${platformLabel()} 登录后 bridge 会自动启动，手机 App 可直接连接。`
        );
      } catch (error) {
        return textResult(`AideNote OpenClaw bridge 安装失败: ${error.message}`);
      }
    }
  });

  api.registerTool({
    name: 'slonaide_bridge_status',
    description: '检查 AideNote OpenClaw 远程对话 bridge 是否已安装并运行',
    parameters: { type: 'object', properties: {} },
    async execute() {
      try {
        if (!isSupportedPlatform()) {
          return textResult('当前 bridge 状态检查支持 macOS 和 Windows。');
        }
        const status = await bridgeStatus();
        return textResult(
          status.running
            ? `AideNote OpenClaw bridge 正在运行。\n${status.output.trim()}`
            : `AideNote OpenClaw bridge 未运行。\n${status.output.trim()}`
        );
      } catch (error) {
        return textResult(`检查 bridge 状态失败: ${error.message}`);
      }
    }
  });
}

function isSupportedPlatform() {
  return process.platform === 'darwin' || process.platform === 'win32';
}

function platformLabel() {
  return process.platform === 'win32' ? 'Windows' : 'Mac';
}

function installerUrlForPlatform(config) {
  if (process.platform === 'win32') {
    return config.bridgeWindowsInstallerUrl || DEFAULT_WINDOWS_INSTALLER_URL;
  }
  return config.bridgeInstallerUrl || DEFAULT_INSTALLER_URL;
}

function installerFileName() {
  return process.platform === 'win32' ? 'install-windows.ps1' : 'install-macos.sh';
}

function installerCommand() {
  return process.platform === 'win32' ? 'powershell.exe' : 'bash';
}

function installerArgs(installer) {
  if (process.platform === 'win32') {
    return ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', installer];
  }
  return [installer];
}

async function downloadInstaller(url, fileName) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`下载安装脚本失败: HTTP ${response.status}`);
  }
  const script = await response.text();
  const dir = await mkdtemp(join(tmpdir(), 'aidenote-openclaw-'));
  const file = join(dir, fileName);
  await writeFile(file, script, { mode: 0o700 });
  return file;
}

async function bridgeStatus() {
  if (process.platform === 'win32') {
    const script =
      `$task = Get-ScheduledTask -TaskName '${WINDOWS_TASK_NAME}' -ErrorAction SilentlyContinue; ` +
      `$proc = Get-Process aide-note-tunnel -ErrorAction SilentlyContinue | Select-Object -First 1; ` +
      `if ($task) { $task | Format-List TaskName,State | Out-String } else { 'Task not found' }; ` +
      `if ($proc) { $proc | Format-List Id,ProcessName,StartTime | Out-String } else { 'Process not running' }`;
    const output = await run(
      'powershell.exe',
      ['-NoProfile', '-Command', script],
      { timeout: 10000, rejectOnExit: false }
    );
    const running = /State\s*:\s*Running|ProcessName\s*:\s*aide-note-tunnel/i.test(output);
    return { running, output };
  }

  const output = await run('launchctl', ['print', `gui/${process.getuid()}/${MAC_LABEL}`], {
    timeout: 10000,
    rejectOnExit: false
  });
  const running = /state = running|pid = \d+/.test(output);
  return { running, output };
}

function run(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    execFile(command, args, options, (error, stdout, stderr) => {
      const output = [stdout, stderr].filter(Boolean).join('\n');
      if (error && options.rejectOnExit !== false) {
        reject(new Error(output.trim() || error.message));
        return;
      }
      resolve(output || error?.message || '');
    });
  });
}

function summarizeOutput(output) {
  const lines = output.split('\n').filter((line) => line.trim().length > 0);
  return lines.slice(-12).join('\n');
}

function textResult(text) {
  return { content: [{ type: 'text', text }] };
}