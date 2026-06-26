import nodeFetch from 'node-fetch';
import { ethers } from 'ethers';

/**
 * Monitoring primitive. Watches targets for changes/conditions.
 *
 * Modes:
 *   poll     — Fetch target every interval, fire callback on change
 *   websocket — Connect to WSS endpoint, listen for events
 *   webhook  — Register with webhook server (requires webhook-server.js running)
 *   contract — Watch contract events via ethers provider
 *
 * @param {string} target - URL, contract address, or WSS endpoint
 * @param {object} options
 * @param {function} options.condition - (newState, oldState) => boolean — when to fire
 * @param {number} options.interval - Poll interval in ms (default: 30000)
 * @param {string} options.method - 'poll' | 'websocket' | 'webhook' | 'contract' (auto-detected)
 * @param {string} options.field - JSON field path to watch (dot notation, e.g. 'data.price')
 * @param {string} options.event - Contract event name (for contract mode)
 * @param {string} options.abi - Contract ABI (for contract mode)
 * @param {string} options.rpc - RPC URL (for contract mode)
 * @param {string} options.path - Webhook path (for webhook mode)
 * @param {object} options.headers - HTTP headers for poll requests
 * @param {number} options.threshold - Price threshold for price monitoring
 * @param {string} options.direction - 'above' | 'below' for threshold
 * @param {function} callback - Called with (event) when condition is met
 * @returns {object} Observer handle with .stop() method
 */
export async function observe(target, options = {}, callback) {
  // Support old 3-arg signature: observe(target, condition, callback)
  if (typeof options === 'function' && callback === undefined) {
    callback = options;
    options = {};
  }
  if (typeof options === 'function' && typeof callback === 'function') {
    // observe(target, conditionFn, callback) — old signature
    const condFn = options;
    options = { condition: condFn };
    // callback stays as-is
  }

  const method = options.method || detectMethod(target);

  switch (method) {
    case 'poll':
      return startPollObserver(target, options, callback);
    case 'websocket':
      return startWebSocketObserver(target, options, callback);
    case 'contract':
      return startContractObserver(target, options, callback);
    case 'webhook':
      return startWebhookObserver(target, options, callback);
    default:
      throw new Error(`Unknown observe method: ${method}`);
  }
}

/**
 * Auto-detect the best observation method based on the target.
 */
function detectMethod(target) {
  if (!target) return 'poll';

  // Contract address
  if (/^0x[a-fA-F0-9]{40}$/.test(target)) {
    return 'contract';
  }

  // WebSocket URL
  if (target.startsWith('wss://') || target.startsWith('ws://')) {
    return 'websocket';
  }

  // Everything else: poll
  return 'poll';
}

/**
 * Resolve a dot-notation field path on an object.
 * e.g. getField({ data: { price: 42 } }, 'data.price') => 42
 */
function getField(obj, fieldPath) {
  if (!fieldPath) return obj;
  const parts = fieldPath.split('.');
  let current = obj;
  for (const part of parts) {
    if (current == null) return undefined;
    current = current[part];
  }
  return current;
}

// --- Poll Observer ---

function startPollObserver(target, options, callback) {
  const {
    interval = 30000,
    condition,
    field,
    headers = {},
    threshold,
    direction = 'above',
  } = options;

  let lastState = null;
  let running = true;
  let pollCount = 0;
  const id = `obs-poll-${Date.now()}`;

  console.log(`[observe] Poll started: ${target} every ${interval}ms`);

  const poll = async () => {
    if (!running) return;

    try {
      const response = await nodeFetch(target, {
        headers: {
          'User-Agent': 'reach-agent/0.1.0',
          'Accept': 'application/json, text/html, */*',
          ...headers,
        },
        timeout: 15000,
      });

      let newState;
      const contentType = response.headers.get('content-type') || '';

      if (contentType.includes('application/json')) {
        const json = await response.json();
        newState = field ? getField(json, field) : json;
      } else {
        newState = await response.text();
      }

      pollCount++;

      let shouldFire = false;

      // Threshold check (price monitoring)
      if (threshold !== undefined && typeof newState === 'number') {
        if (direction === 'above' && newState > threshold) shouldFire = true;
        if (direction === 'below' && newState < threshold) shouldFire = true;
      }
      // Custom condition function
      else if (typeof condition === 'function') {
        shouldFire = condition(newState, lastState);
      }
      // Default: fire on any change
      else if (lastState !== null) {
        const newStr = typeof newState === 'object' ? JSON.stringify(newState) : String(newState);
        const oldStr = typeof lastState === 'object' ? JSON.stringify(lastState) : String(lastState);
        shouldFire = newStr !== oldStr;
      }

      if (shouldFire && callback) {
        callback({
          type: 'change',
          target,
          newState,
          oldState: lastState,
          pollCount,
          timestamp: new Date().toISOString(),
        });
      }

      lastState = newState;
    } catch (e) {
      console.log(`[observe] Poll error for ${target}: ${e.message}`);
      if (callback) {
        callback({
          type: 'error',
          target,
          error: e.message,
          pollCount,
          timestamp: new Date().toISOString(),
        });
      }
    }

    if (running) {
      setTimeout(poll, interval);
    }
  };

  // Start first poll immediately
  poll();

  return {
    id,
    target,
    method: 'poll',
    status: 'running',
    stop: () => {
      running = false;
      console.log(`[observe] Poll stopped: ${target} (${pollCount} polls)`);
      return { id, stopped: true, pollCount };
    },
    getState: () => lastState,
    getPollCount: () => pollCount,
  };
}

// --- WebSocket Observer ---

function startWebSocketObserver(target, options, callback) {
  const { condition } = options;
  const id = `obs-ws-${Date.now()}`;
  let messageCount = 0;

  // Dynamic import WebSocket (Node.js built-in in v22+)
  let ws;

  console.log(`[observe] WebSocket connecting: ${target}`);

  const connect = async () => {
    const { WebSocket } = await import('ws').catch(() => {
      // Fallback: try global WebSocket (Node 22+)
      return { WebSocket: globalThis.WebSocket };
    });

    if (!WebSocket) {
      throw new Error('WebSocket not available. Install ws package: npm install ws');
    }

    ws = new WebSocket(target);

    ws.on('open', () => {
      console.log(`[observe] WebSocket connected: ${target}`);
    });

    ws.on('message', (data) => {
      messageCount++;
      let parsed;
      try {
        parsed = JSON.parse(data.toString());
      } catch {
        parsed = data.toString();
      }

      let shouldFire = true;
      if (typeof condition === 'function') {
        shouldFire = condition(parsed);
      }

      if (shouldFire && callback) {
        callback({
          type: 'message',
          target,
          data: parsed,
          messageCount,
          timestamp: new Date().toISOString(),
        });
      }
    });

    ws.on('error', (err) => {
      console.log(`[observe] WebSocket error: ${err.message}`);
      if (callback) {
        callback({
          type: 'error',
          target,
          error: err.message,
          timestamp: new Date().toISOString(),
        });
      }
    });

    ws.on('close', () => {
      console.log(`[observe] WebSocket closed: ${target}`);
    });
  };

  connect().catch(e => {
    console.log(`[observe] WebSocket connect failed: ${e.message}`);
  });

  return {
    id,
    target,
    method: 'websocket',
    status: 'connecting',
    stop: () => {
      if (ws) {
        ws.close();
      }
      console.log(`[observe] WebSocket stopped: ${target} (${messageCount} messages)`);
      return { id, stopped: true, messageCount };
    },
    send: (data) => {
      if (ws && ws.readyState === 1) { // OPEN
        ws.send(typeof data === 'string' ? data : JSON.stringify(data));
      }
    },
    getMessageCount: () => messageCount,
  };
}

// --- Contract Event Observer ---

function startContractObserver(target, options, callback) {
  const {
    event = '*',
    abi,
    rpc = process.env.RPC_URL || 'https://mainnet.base.org',
  } = options;

  const id = `obs-contract-${Date.now()}`;
  let eventCount = 0;
  let provider;
  let contract;

  console.log(`[observe] Contract watch started: ${target} event=${event}`);

  const setup = async () => {
    provider = new ethers.JsonRpcProvider(rpc);

    if (abi) {
      // Watch specific contract events
      contract = new ethers.Contract(target, abi, provider);

      if (event === '*') {
        // Watch all events
        contract.on('*', (eventObj) => {
          eventCount++;
          if (callback) {
            callback({
              type: 'contract-event',
              target,
              event: eventObj.eventName || eventObj.fragment?.name || 'unknown',
              args: eventObj.args ? Array.from(eventObj.args) : [],
              log: eventObj.log,
              blockNumber: eventObj.log?.blockNumber,
              transactionHash: eventObj.log?.transactionHash,
              eventCount,
              timestamp: new Date().toISOString(),
            });
          }
        });
      } else {
        // Watch specific event
        contract.on(event, (...args) => {
          eventCount++;
          const eventObj = args[args.length - 1]; // Last arg is the event object
          if (callback) {
            callback({
              type: 'contract-event',
              target,
              event,
              args: args.slice(0, -1).map(a => a.toString()),
              blockNumber: eventObj?.log?.blockNumber,
              transactionHash: eventObj?.log?.transactionHash,
              eventCount,
              timestamp: new Date().toISOString(),
            });
          }
        });
      }
    } else {
      // No ABI — watch raw logs from the address
      const filter = { address: target };
      provider.on(filter, (log) => {
        eventCount++;
        if (callback) {
          callback({
            type: 'raw-log',
            target,
            topics: log.topics,
            data: log.data,
            blockNumber: log.blockNumber,
            transactionHash: log.transactionHash,
            eventCount,
            timestamp: new Date().toISOString(),
          });
        }
      });
    }
  };

  setup().catch(e => {
    console.log(`[observe] Contract setup failed: ${e.message}`);
  });

  return {
    id,
    target,
    method: 'contract',
    status: 'watching',
    stop: () => {
      if (contract) {
        contract.removeAllListeners();
      }
      if (provider) {
        provider.removeAllListeners();
      }
      console.log(`[observe] Contract watch stopped: ${target} (${eventCount} events)`);
      return { id, stopped: true, eventCount };
    },
    getEventCount: () => eventCount,
  };
}

// --- Webhook Observer ---

function startWebhookObserver(target, options, callback) {
  const { path: hookPath = `/hook-${Date.now()}` } = options;
  const id = `obs-webhook-${Date.now()}`;

  console.log(`[observe] Webhook registered: ${hookPath} for ${target}`);
  console.log('[observe] Note: Requires WebhookServer to be running (src/utils/webhook-server.js)');

  // Store the callback for the webhook server to find
  if (!globalThis.__reachWebhooks) {
    globalThis.__reachWebhooks = new Map();
  }
  globalThis.__reachWebhooks.set(hookPath, { target, callback, id });

  return {
    id,
    target,
    method: 'webhook',
    path: hookPath,
    status: 'waiting',
    stop: () => {
      if (globalThis.__reachWebhooks) {
        globalThis.__reachWebhooks.delete(hookPath);
      }
      console.log(`[observe] Webhook unregistered: ${hookPath}`);
      return { id, stopped: true };
    },
  };
}
