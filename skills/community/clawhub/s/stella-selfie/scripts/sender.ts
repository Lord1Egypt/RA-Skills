import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

export interface SendMessageOptions {
  channel: string;
  target: string;
  media?: string;
  message?: string;
}

/**
 * Send a message to an OpenClaw channel.
 */
export async function sendMessage(options: SendMessageOptions): Promise<void> {
  const { channel, target, media, message = "" } = options;
  await sendViaCLI({ channel, target, media, message });
}

/**
 * Backward-compatible image send helper.
 */
export async function sendImage(options: {
  channel: string;
  target: string;
  media: string;
  message?: string;
}): Promise<void> {
  await sendMessage(options);
}

/**
 * Send via `openclaw message send` CLI (OpenClaw 2026.3.13).
 * Command format:
 *   openclaw message send --channel <provider> --target <destination> [--message <caption>] [--media <url_or_path>]
 */
async function sendViaCLI(options: {
  channel: string;
  target: string;
  media?: string;
  message: string;
}): Promise<void> {
  const { channel, target, media, message } = options;

  const parts = [
    "openclaw message send",
    `--channel ${shellEscape(channel)}`,
    `--target ${shellEscape(target)}`,
  ];

  if (media) {
    parts.push(`--media ${shellEscape(media)}`);
  }

  if (message) {
    parts.push(`--message ${shellEscape(message)}`);
  }

  const cmd = parts.join(" ");
  console.log(`[stella] Running: ${cmd}`);

  const { stdout, stderr } = await execAsync(cmd);
  if (stdout) console.log(`[stella] CLI stdout: ${stdout.trim()}`);
  if (stderr) console.warn(`[stella] CLI stderr: ${stderr.trim()}`);
}

/**
 * Minimal shell argument escaping: wrap in single quotes, escape embedded single quotes.
 */
function shellEscape(value: string): string {
  return `'${value.replace(/'/g, "'\\''")}'`;
}
