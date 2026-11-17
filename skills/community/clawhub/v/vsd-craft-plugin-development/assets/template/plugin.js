'use strict';

const WebSocket = require('ws');

function launchOptions(argv) {
  const options = new Map();
  if (argv.length % 2) throw new Error('Expected named argument/value pairs');
  for (let i = 0; i < argv.length; i += 2) {
    if (!/^--?[a-z]+$/i.test(argv[i])) throw new Error('Invalid launch argument');
    options.set(argv[i].replace(/^--?/, '').toLowerCase(), argv[i + 1]);
  }
  const port = Number(options.get('port'));
  const uuid = options.get('pluginuuid');
  const registerEvent = options.get('registerevent');
  if (!Number.isInteger(port) || port < 1 || port > 65535 || !uuid || !registerEvent) {
    throw new Error('Launch from VSD Craft with -port -pluginUUID -registerEvent -info');
  }
  JSON.parse(options.get('info') || '{}');
  return {port, uuid, registerEvent};
}

function validStep(value) {
  return Number.isInteger(value) && value >= 1 && value <= 100;
}

function createController(send, actionIds) {
  const contexts = new Map();
  const disconnected = new Set();
  const allowed = new Set(actionIds);
  const online = (entry) => !disconnected.has(entry.device);
  const settings = (raw) => ({
    ...(raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {}),
    step: validStep(raw?.step) ? raw.step : 1,
  });
  function reply(context, entry) {
    send({event: 'sendToPropertyInspector', action: entry.action, context,
      payload: {step: entry.settings.step, value: entry.value}});
  }
  function render(context, entry) {
    if (!online(entry)) return;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="144" height="144">` +
      `<rect width="144" height="144" rx="18" fill="#193657"/>` +
      `<text x="72" y="83" text-anchor="middle" font-size="40" fill="white">${entry.value}</text></svg>`;
    send({event: 'setImage', context, payload: {
      image: `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`, target: 0,
    }});
    reply(context, entry);
  }
  function update(context, entry, delta) {
    entry.value = Math.max(-999999, Math.min(999999, entry.value + delta));
    render(context, entry);
  }
  function receive(message) {
    if (!message || typeof message.event !== 'string') return;
    const {event, context, device, payload = {}} = message;
    if (event === 'deviceDidDisconnect' && typeof device === 'string') {
      disconnected.add(device);
      for (const entry of contexts.values()) if (entry.device === device) entry.held = null;
      return;
    }
    if (event === 'deviceDidConnect' && typeof device === 'string') {
      disconnected.delete(device);
      for (const [id, entry] of contexts) if (entry.device === device) render(id, entry);
      return;
    }
    if (event === 'willAppear') {
      if (!allowed.has(message.action) || typeof context !== 'string' || typeof device !== 'string') return;
      const prior = contexts.get(context);
      const entry = {action: message.action, device, settings: settings(payload?.settings),
        value: prior?.action === message.action ? prior.value : 0, held: null};
      contexts.set(context, entry);
      render(context, entry);
      return;
    }
    if (event === 'willDisappear') {
      contexts.delete(context);
      return;
    }
    // actionContext is our own PI payload field, not a vendor protocol field.
    const target = event === 'sendToPlugin' ? (payload?.actionContext || context) : context;
    const entry = contexts.get(target);
    if (!entry || (message.action && message.action !== entry.action)) return;
    if (event === 'didReceiveSettings') {
      entry.settings = settings(payload?.settings);
      render(target, entry);
      return;
    }
    if (event === 'sendToPlugin') {
      if (payload?.op === 'setStep' && validStep(payload.step)) {
        entry.settings = {...entry.settings, step: payload.step};
        send({event: 'setSettings', context: target, payload: entry.settings});
      }
      reply(target, entry);
      return;
    }
    if (!online(entry)) return;
    switch (event) {
      case 'keyDown': entry.held = 'key'; break;
      case 'keyUp':
        if (entry.held === 'key') update(target, entry, entry.settings.step);
        entry.held = null;
        break;
      case 'dialDown': entry.held = 'dial'; break;
      case 'dialUp':
        if (entry.held === 'dial') { entry.value = 0; render(target, entry); }
        entry.held = null;
        break;
      case 'dialRotate':
        if (Number.isSafeInteger(payload?.ticks)) update(target, entry, payload.ticks * entry.settings.step);
        break;
    }
  }
  return {receive};
}

function main() {
  const launch = launchOptions(process.argv.slice(2));
  const manifest = require('./manifest.json');
  const socket = new WebSocket(`ws://127.0.0.1:${launch.port}`, {maxPayload: 1024 * 1024});
  const send = (message) => {
    if (socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify(message));
  };
  const controller = createController(send, manifest.Actions.map((action) => action.UUID));
  socket.on('open', () => send({event: launch.registerEvent, uuid: launch.uuid}));
  socket.on('message', (data) => {
    try { controller.receive(JSON.parse(data.toString())); }
    catch { console.error('Ignored invalid or unsupported host message'); }
  });
  socket.on('error', (error) => { console.error(`Host socket: ${error.message}`); process.exitCode = 1; });
  socket.on('close', () => process.exit(process.exitCode || 0));
}

module.exports = {launchOptions, createController};
if (require.main === module) {
  try { main(); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
