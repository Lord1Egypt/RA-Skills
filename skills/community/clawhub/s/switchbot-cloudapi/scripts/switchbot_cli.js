#!/usr/bin/env node
// SwitchBot OpenAPI v1.1 CLI (Node.js)
// Requires env: SWITCHBOT_TOKEN, SWITCHBOT_SECRET
// Usage:
//   node switchbot_cli.js list
//   node switchbot_cli.js status <deviceId>
//   node switchbot_cli.js cmd <deviceId> <command> [--param=...] [--pos=50] [--commandType=customize]
//   node switchbot_cli.js scenes
//   node switchbot_cli.js scene <sceneId>

const crypto = require('crypto');
const https = require('https');

function baseUrl() {
  return 'https://api.switch-bot.com';
}

function headers() {
  const token = process.env.SWITCHBOT_TOKEN;
  const secret = process.env.SWITCHBOT_SECRET;
  if (!token || !secret) {
    console.error('Missing SWITCHBOT_TOKEN or SWITCHBOT_SECRET');
    process.exit(2);
  }
  const t = Date.now().toString();
  const nonce = crypto.randomUUID();
  const sign = crypto
    .createHmac('sha256', secret)
    .update(token + t + nonce)
    .digest('base64');
  return {
    'Content-Type': 'application/json; charset=utf8',
    'Authorization': token,
    't': t,
    'nonce': nonce,
    'sign': sign,
    'src': 'OpenClaw',
  };
}

function request(method, path, body) {
  const data = body ? JSON.stringify(body) : undefined;
  const opts = new URL(baseUrl() + path);
  return new Promise((resolve, reject) => {
    const req = https.request({
      method,
      hostname: opts.hostname,
      path: opts.pathname + (opts.search || ''),
      headers: { ...headers(), ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}) },
    }, (res) => {
      let buf = '';
      res.on('data', (c) => (buf += c));
      res.on('end', () => {
        try { resolve(buf ? JSON.parse(buf) : {}); }
        catch { resolve(buf); }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const eq = a.indexOf('=');
      if (eq > 0) {
        out[a.slice(2, eq)] = a.slice(eq + 1);
      } else {
        out[a.slice(2)] = true;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

function printJson(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

async function main() {
  const args = parseArgs(process.argv);
  const [cmd, a1, a2] = args._;

  if (!cmd || cmd === 'help') {
    console.log(`SwitchBot OpenAPI v1.1 CLI

Commands:
  list                              List all devices
  status <deviceId>                 Get device status
  cmd <deviceId> <command> [opts]   Send a command
  scenes                            List all scenes
  scene <sceneId>                   Execute a scene

Command options:
  --param=<value>         Parameter (string or JSON)
  --pos=<0-100>           Curtain position shorthand
  --commandType=customize For IR DIY "Others" devices

Examples:
  node switchbot_cli.js list
  node switchbot_cli.js status AABBCCDD1122
  node switchbot_cli.js cmd AABBCCDD1122 turnOn
  node switchbot_cli.js cmd AABBCCDD1122 setPosition --pos=50
  node switchbot_cli.js cmd AABBCCDD1122 setAll --param="26,2,1,on"
  node switchbot_cli.js cmd AABBCCDD1122 setColor --param="255:100:0"
  node switchbot_cli.js cmd AABBCCDD1122 createKey --param='{"name":"Guest","type":"permanent","password":"123456"}'
  node switchbot_cli.js cmd AABBCCDD1122 myButton --commandType=customize
  node switchbot_cli.js scenes
  node switchbot_cli.js scene T02-xxxxx`);
    process.exit(0);
  }

  // === LIST ===
  if (cmd === 'list') {
    try { printJson(await request('GET', '/v1.1/devices')); }
    catch (e) { console.error('Error:', e.message); process.exit(1); }
    return;
  }

  // === STATUS ===
  if (cmd === 'status') {
    if (!a1) { console.error('Usage: status <deviceId>'); process.exit(2); }
    try { printJson(await request('GET', `/v1.1/devices/${a1}/status`)); }
    catch (e) { console.error('Error:', e.message); process.exit(1); }
    return;
  }

  // === SCENES ===
  if (cmd === 'scenes') {
    try { printJson(await request('GET', '/v1.1/scenes')); }
    catch (e) { console.error('Error:', e.message); process.exit(1); }
    return;
  }

  // === EXECUTE SCENE ===
  if (cmd === 'scene') {
    if (!a1) { console.error('Usage: scene <sceneId>'); process.exit(2); }
    try { printJson(await request('POST', `/v1.1/scenes/${a1}/execute`)); }
    catch (e) { console.error('Error:', e.message); process.exit(1); }
    return;
  }

  // === SEND COMMAND ===
  if (cmd === 'cmd') {
    const deviceId = a1;
    const command = a2;
    if (!deviceId || !command) { console.error('Usage: cmd <deviceId> <command> [--param=...]'); process.exit(2); }

    let devicesResp;
    try { devicesResp = await request('GET', '/v1.1/devices'); }
    catch (e) { console.error('Error fetching devices:', e.message); process.exit(1); }

    const deviceList = (devicesResp?.body?.deviceList) || [];
    const irList = (devicesResp?.body?.infraredRemoteList) || [];
    const dev = deviceList.find(d => d.deviceId === deviceId);
    const irDev = irList.find(d => d.deviceId === deviceId);
    const isIR = !!irDev;

    if (!dev && !irDev) {
      console.error(`Device ${deviceId} not found in device list or IR remote list.`);
      process.exit(3);
    }

    // Preflight for BLE devices
    if (dev) {
      const btTypes = ['Bot', 'Smart Lock', 'Smart Lock Pro', 'Lock Lite', 'Lock Ultra', 'Blind Tilt', 'Curtain', 'Curtain3'];
      const isBt = btTypes.includes(dev.deviceType);
      const cloud = dev.enableCloudService === true;
      const hasHub = !!(dev.hubDeviceId && dev.hubDeviceId !== '' && dev.hubDeviceId !== '000000000000');
      if (isBt && (!cloud || !hasHub)) {
        console.error(`Preflight failed: ${dev.deviceName || deviceId} (${dev.deviceType}) requires a Hub + Cloud Services enabled.\n  enableCloudService=${dev.enableCloudService}, hubDeviceId='${dev.hubDeviceId || ''}'\n  Fix in SwitchBot app, then retry.`);
        process.exit(4);
      }
    }

    // Build parameter
    let parameter = 'default';

    if (args.param != null && args.param !== true) {
      // Try to parse as JSON, fall back to string
      try { parameter = JSON.parse(args.param); }
      catch { parameter = String(args.param); }
    }

    // Shorthand: --pos for Curtain setPosition
    if (command === 'setPosition' && !args.param && dev) {
      const devType = (dev.deviceType || '').toLowerCase();
      if (devType.includes('curtain')) {
        let pos = Number(args.pos ?? args.position ?? 50);
        if (!Number.isFinite(pos)) pos = 50;
        pos = Math.max(0, Math.min(100, Math.round(pos)));
        parameter = `0,ff,${pos}`;
      }
    }

    // Determine commandType
    let commandType = args.commandType || 'command';

    // Build and send
    const body = { commandType, command, parameter };
    try {
      const resp = await request('POST', `/v1.1/devices/${deviceId}/commands`, body);
      printJson(resp);

      // Helpful hints on errors
      if (resp?.statusCode === 160) {
        const devType = (dev?.deviceType || irDev?.remoteType || '').toLowerCase();
        if (devType.includes('vacuum')) {
          console.warn('\nHint: This vacuum model may not support direct commands. Create a Scene in the SwitchBot app and execute via: node switchbot_cli.js scene <sceneId>');
        } else {
          console.warn('\nHint: Unknown command. Check references/commands.md for supported commands, or use a Scene.');
        }
      }
    } catch (e) {
      console.error('Error:', e.message);
      process.exit(1);
    }
    return;
  }

  console.error(`Unknown command: ${cmd}. Run with 'help' for usage.`);
  process.exit(1);
}

main();
