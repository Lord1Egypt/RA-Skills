import net from "node:net";
import os from "node:os";
import { encodeCommand, parseProtocolFrame } from "./protocol.mjs";
import { PROTOCOL_CATALOG } from "./catalog.mjs";
import { isEligibleLocalUnicastIPv4, normalizeIPv4, validateControlEndpoint } from "./network-policy.mjs";

export class MusicError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "MusicError";
    this.code = code;
    this.details = details;
  }
}

const clone = (value) => value === undefined ? undefined : structuredClone(value);

export function selectLocalIPv4({ requestedHost, interfaces = os.networkInterfaces() } = {}) {
  if (requestedHost !== undefined) {
    const host = normalizeIPv4(requestedHost);
    if (!host || !isEligibleLocalUnicastIPv4(host)) throw new MusicError("music_host_invalid", "音乐模式只能使用本机局域网 IPv4 地址。");
    const entries = Object.values(interfaces).flat().filter(Boolean);
    if (!entries.some((entry) => normalizeIPv4(entry.address) === host && entry.family === "IPv4" && entry.internal !== true)) throw new MusicError("music_host_not_local", "音乐模式地址不是当前启用的本机网卡地址。");
    return host;
  }
  const entries = Object.values(interfaces).flat().filter(Boolean);
  const candidate = entries.find((entry) => entry.family === "IPv4" && entry.internal !== true && isEligibleLocalUnicastIPv4(entry.address));
  if (!candidate) throw new MusicError("music_local_interface_unavailable", "没有可用于音乐模式的局域网网卡。");
  return normalizeIPv4(candidate.address);
}

export function validateMusicSequence(sequence, maxCommands = 16) {
  if (sequence === undefined) return [];
  if (!Array.isArray(sequence) || sequence.length > maxCommands) throw new MusicError("music_sequence_invalid", "音乐模式命令序列超出上限。");
  return sequence.map((command) => {
    if (!command || typeof command !== "object" || Array.isArray(command) || typeof command.method !== "string" || !Array.isArray(command.params)) throw new MusicError("music_sequence_invalid", "音乐模式命令必须是结构化协议命令。");
    if (command.method === "set_music") throw new MusicError("music_sequence_invalid", "音乐模式序列不能嵌套 set_music。");
    const frame = encodeCommand(1, command.method, command.params, { maxFrameBytes: PROTOCOL_CATALOG.limits.maxFrameBytes });
    return { method: command.method, params: clone(command.params), frame };
  });
}

export async function runMusicSession({
  device,
  transport,
  requestedHost,
  sequence = [],
  durationMs = 1000,
  listenerFactory,
  now = () => Date.now(),
} = {}) {
  if (!device?.endpoint) throw new MusicError("music_device_required", "音乐模式需要一个已发现的设备。");
  validateControlEndpoint(device.endpoint, { requirePrivate: true, controlPort: PROTOCOL_CATALOG.limits.controlPort });
  if (!transport || typeof transport.request !== "function") throw new MusicError("music_transport_required", "音乐模式需要控制连接。");
  if (!Number.isInteger(durationMs) || durationMs < 100 || durationMs > 60000) throw new MusicError("music_duration_invalid", "音乐模式时长超出安全范围。");
  const commands = validateMusicSequence(sequence);
  const host = selectLocalIPv4({ requestedHost });
  const server = listenerFactory ? listenerFactory() : net.createServer();
  let listener;
  let peer;
  let stopped = false;
  const close = () => {
    if (stopped) return;
    stopped = true;
    try { peer?.destroy?.(); } catch {}
    try { server.close?.(); } catch {}
  };
  try {
    listener = await new Promise((resolve, reject) => {
      let settled = false;
      const timer = setTimeout(() => {
        if (settled) return;
        settled = true;
        reject(new MusicError("music_listener_timeout", "音乐模式监听器启动超时。"));
      }, 3000);
      server.once("error", (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        reject(new MusicError("music_listener_failed", "音乐模式监听器无法启动。", { name: error?.code || "listener_error" }));
      });
      server.listen(0, host, () => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        const address = server.address();
        resolve({ host, port: typeof address === "object" && address ? address.port : null });
      });
    });
    if (!listener.port) throw new MusicError("music_listener_failed", "音乐模式没有获得有效监听端口。");
    const peerPromise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new MusicError("music_peer_timeout", "设备未在限定时间内建立音乐连接。")), durationMs);
      server.once("connection", (socket) => {
        const remote = normalizeIPv4(socket.remoteAddress?.replace(/^::ffff:/u, ""));
        if (remote !== device.endpoint.host) {
          socket.destroy();
          clearTimeout(timer);
          reject(new MusicError("music_peer_mismatch", "音乐模式连接不是所选设备。"));
          return;
        }
        clearTimeout(timer);
        resolve(socket);
      });
    });
    await transport.request("set_music", [1, host, listener.port], { support: device.support });
    peer = await peerPromise;
    for (const command of commands) {
      if (stopped) throw new MusicError("music_stopped", "音乐模式已停止。");
      peer.write(command.frame);
    }
    await new Promise((resolve) => setTimeout(resolve, Math.min(durationMs, 1000)));
    return { status: "acknowledged", host, commandCount: commands.length, startedAt: now() };
  } finally {
    close();
    try { await transport.request("set_music", [0], { support: device.support }); } catch {}
  }
}

export const stopMusicSession = ({ transport, device } = {}) => transport.request("set_music", [0], { support: device?.support });
