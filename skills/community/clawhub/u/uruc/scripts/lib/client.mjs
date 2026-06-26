import net from 'net';

import { getSocketPath, uuid } from './common.mjs';

export async function callDaemon(action, payload, timeoutMs = 15000) {
  const request = { id: uuid(), action, payload };
  const response = await sendRequest(request, timeoutMs);
  if (!response.ok) {
    throw new Error(response.error ?? 'daemon request failed');
  }
  return response.data;
}

export async function isDaemonRunning(timeoutMs = 1000) {
  try {
    await callDaemon('ping', undefined, timeoutMs);
    return true;
  } catch {
    return false;
  }
}

function sendRequest(request, timeoutMs) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(getSocketPath());
    let timer;
    let buffer = '';
    let settled = false;

    const finish = (fn) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      socket.removeAllListeners();
      socket.destroy();
      fn();
    };

    timer = setTimeout(() => {
      finish(() => reject(new Error(`daemon request timed out: ${request.action}`)));
    }, timeoutMs);

    socket.on('error', (error) => {
      finish(() => reject(error));
    });

    socket.on('connect', () => {
      socket.write(`${JSON.stringify(request)}\n`);
    });

    socket.on('data', (chunk) => {
      buffer += chunk.toString();
      const newlineIndex = buffer.indexOf('\n');
      if (newlineIndex === -1) return;
      const line = buffer.slice(0, newlineIndex);
      try {
        const response = JSON.parse(line);
        finish(() => resolve(response));
      } catch (error) {
        finish(() => reject(error));
      }
    });
  });
}
