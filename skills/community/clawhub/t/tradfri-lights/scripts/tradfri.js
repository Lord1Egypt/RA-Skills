#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { TradfriClient, AccessoryTypes } = require('node-tradfri-client');

const configPath = path.join(__dirname, '..', 'config.json');
const fileConfig = fs.existsSync(configPath)
  ? JSON.parse(fs.readFileSync(configPath, 'utf8'))
  : {};

const host = process.env.TRADFRI_HOST || fileConfig.host;
const identity = process.env.TRADFRI_IDENTITY || fileConfig.identity;
const psk = process.env.TRADFRI_PSK || fileConfig.psk;

const cmd = process.argv[2];
const targetName = process.argv[3];
const value = process.argv[4];
const extra = process.argv.slice(5);
const EXCLUDED_GROUPS = new Set(['SuperGroup', 'Instellen']);
const DEFAULT_SETTLE_MS = Number(process.env.TRADFRI_SETTLE_MS || 1500);
const DEFAULT_RETRIES = Number(process.env.TRADFRI_RETRIES || 3);
const DEFAULT_RETRY_DELAY_MS = Number(process.env.TRADFRI_RETRY_DELAY_MS || 1200);
const FLOOR_MAP = {
  '1': ['Eetkamer 1', 'Eetkamer 2', 'Eetkamer 3', 'Eetkamer 4', 'Eetkamer 5', 'Eetkamer 6', 'Eetkamer 7', 'Hal 0', 'Gang 0', 'Speelkamer 1', 'Speelkamer 2'],
  '2': ['Woonkamer 1', 'Woonkamer 2', 'Woonkamer 3', 'Woonkamer 4', 'Woonkamer 5', 'Woonkamer 6', 'Woonkamer 7', 'Gang 1', 'Slaapkamer Tommi'],
  '3': ['Slaapkamer ouders 1', 'Slaapkamer ouders 2', 'Slaapkamer Sanne', 'Slaapkamer Swiss', 'Gang 2', 'Badkamer ouders'],
  '4': ['Slaapkamer Jesse', 'Slaapkamer Wilbert', 'Gang 3'],
};
const LAYOUTS = {
  day: {
    on: [
      { floor: '1', brightness: 50 },
      { floor: '2', brightness: 50 },
    ],
    off: ['3', '4'],
  },
  evening: {
    on: [
      { floor: '1', brightness: 50 },
      { floor: '2', brightness: 50 },
    ],
    off: ['3', '4'],
  },
  night: {
    on: [],
    off: ['1', '2', '3', '4'],
  },
};

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

if (!host || !identity || !psk) {
  die('Missing TRADFRI config. Set config.json or TRADFRI_HOST/TRADFRI_IDENTITY/TRADFRI_PSK.');
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeName(name) {
  return String(name || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
    .toLowerCase();
}

function lightState(device) {
  return device.lightList && device.lightList[0] ? device.lightList[0] : null;
}

function summarizeDevice(device, groups = new Map()) {
  const light = lightState(device);
  const group = [...groups.values()].find((g) => Array.isArray(g.deviceIDs) && g.deviceIDs.includes(device.instanceId));
  return {
    instanceId: device.instanceId,
    name: device.name,
    type: device.type,
    alive: device.alive,
    onOff: light ? light.onOff : undefined,
    dimmer: light ? light.dimmer : undefined,
    group: group ? group.name : undefined,
  };
}

function summarizeGroup(group) {
  return {
    instanceId: group.instanceId,
    name: group.name,
    onOff: group.onOff,
    dimmer: group.dimmer,
  };
}

async function collect(tradfri) {
  const devices = new Map();
  const groups = new Map();

  tradfri
    .on('device updated', (device) => devices.set(device.instanceId, device))
    .on('group updated', (group) => groups.set(group.instanceId, group));

  await tradfri.connect(identity, psk);
  await tradfri.observeDevices();
  await tradfri.observeGroupsAndScenes();
  await sleep(3000);
  return { devices, groups };
}

async function withRetries(work, { retries = DEFAULT_RETRIES, delayMs = DEFAULT_RETRY_DELAY_MS } = {}) {
  let lastError;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      return await work(attempt);
    } catch (err) {
      lastError = err;
      if (attempt < retries) await sleep(delayMs);
    }
  }
  throw lastError;
}

async function snapshot({ retries = DEFAULT_RETRIES } = {}) {
  return withRetries(async () => {
    const tradfri = new TradfriClient(host);
    try {
      const { devices, groups } = await collect(tradfri);
      return { devices, groups };
    } finally {
      try { tradfri.destroy(); } catch {}
    }
  }, { retries });
}

function scoreMatch(itemName, rawName) {
  const item = normalizeName(itemName);
  const needle = normalizeName(rawName);
  if (!needle) return 0;
  if (item === needle) return 100;
  if (item.startsWith(needle)) return 80;
  if (item.includes(needle)) return 60;
  const words = item.split(/\s+/);
  if (words.some((w) => w.startsWith(needle))) return 40;
  return 0;
}

function resolveByName(items, rawName) {
  const arr = [...items.values()]
    .map((item) => ({ item, score: scoreMatch(item.name, rawName) }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score || normalizeName(a.item.name).localeCompare(normalizeName(b.item.name)));

  if (arr.length === 0) return { match: null, candidates: [] };
  if (arr.length === 1) return { match: arr[0].item, candidates: [] };
  if (arr[0].score >= 80 && arr[1].score < arr[0].score) return { match: arr[0].item, candidates: [] };
  return { match: null, candidates: arr.slice(0, 10).map((x) => x.item) };
}

function allLightDevices(devices) {
  return [...devices.values()].filter((d) => d.type === AccessoryTypes.lightbulb);
}

function realGroups(groups) {
  return [...groups.values()].filter((g) => !EXCLUDED_GROUPS.has(g.name));
}

function parseOptions(args) {
  const opts = { verify: false, settleMs: DEFAULT_SETTLE_MS };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--verify') opts.verify = true;
    if (arg === '--settle-ms') {
      const num = Number(args[i + 1]);
      if (Number.isFinite(num) && num >= 0) opts.settleMs = num;
      i += 1;
    }
  }
  return opts;
}

function expectedForCommand(command, numericValue) {
  if (command === 'light-on' || command === 'group-on' || command === 'floor-on') return { onOff: true, dimmer: numericValue };
  if (command === 'light-off' || command === 'group-off' || command === 'floor-off') return { onOff: false };
  if (command === 'brightness' || command === 'group-brightness') return { onOff: numericValue > 0, dimmer: numericValue };
  if (command === 'all-on') return { onOff: true, dimmer: numericValue };
  if (command === 'all-off') return { onOff: false, dimmer: 0 };
  return null;
}

function dimmerMatches(actual, expected) {
  if (expected == null || actual == null) return true;
  return Math.abs(Number(actual) - Number(expected)) <= 1;
}

function verifyLights(lights, groups, expected) {
  const mismatches = [];
  for (const light of lights) {
    const info = summarizeDevice(light, groups);
    if (!info.alive) continue;
    if (expected.onOff != null && info.onOff !== expected.onOff) {
      mismatches.push({ name: info.name, reason: `expected onOff=${expected.onOff}, got ${info.onOff}` });
      continue;
    }
    if (expected.onOff && expected.dimmer != null && !dimmerMatches(info.dimmer, expected.dimmer)) {
      mismatches.push({ name: info.name, reason: `expected dimmer≈${expected.dimmer}, got ${info.dimmer}` });
    }
  }
  return mismatches;
}

function resolveFloorLights(lights, floorNumber) {
  const names = FLOOR_MAP[String(floorNumber)];
  if (!names) die(`Unknown floor: ${floorNumber}`);
  const byName = new Map(lights.map((d) => [d.name, d]));
  return names.map((name) => byName.get(name)).filter(Boolean);
}

(async () => {
  try {
    const options = parseOptions(extra);
    const { devices, groups } = await snapshot();
    const lights = allLightDevices(devices);
    const usableGroups = realGroups(groups);

    if (cmd === 'status') {
      console.log(JSON.stringify({
        ok: true,
        host,
        counts: { devices: devices.size, lights: lights.length, groups: usableGroups.length },
      }, null, 2));
      return;
    }

    if (cmd === 'list-devices') {
      console.log(JSON.stringify({ ok: true, host, devices: lights.map((d) => summarizeDevice(d, groups)) }, null, 2));
      return;
    }

    if (cmd === 'list-groups') {
      console.log(JSON.stringify({ ok: true, host, groups: usableGroups.map(summarizeGroup) }, null, 2));
      return;
    }

    if (cmd === 'whats-on') {
      const onLights = lights.filter((d) => {
        const light = lightState(d);
        return d.alive && light && light.onOff;
      });
      console.log(JSON.stringify({ ok: true, host, lights: onLights.map((d) => summarizeDevice(d, groups)) }, null, 2));
      return;
    }

    if (cmd === 'offline') {
      const offline = lights.filter((d) => !d.alive);
      console.log(JSON.stringify({ ok: true, host, lights: offline.map((d) => summarizeDevice(d, groups)) }, null, 2));
      return;
    }

    if (!targetName && !['whats-on', 'offline', 'status', 'list-devices', 'list-groups'].includes(cmd)) {
      die('Target name required');
    }

    let actedLights = [];
    let result;
    let target;
    let numericValue = Number(value);

    const tradfri = new TradfriClient(host);
    try {
      await tradfri.connect(identity, psk);

      if (cmd === 'all-on' || cmd === 'all-off') {
        const brightness = value != null ? Number(value) : (cmd === 'all-on' ? 100 : 0);
        if (!Number.isFinite(brightness) || brightness < 0 || brightness > 100) die('Brightness must be 0-100');
        const results = [];
        for (const group of usableGroups) {
          const opResult = await withRetries(() => tradfri.operateGroup(group, { onOff: cmd === 'all-on', dimmer: brightness }, true));
          results.push({ name: group.name, instanceId: group.instanceId, result: opResult });
        }
        if (options.verify) {
          await sleep(options.settleMs);
          const verified = await snapshot();
          const verifiedLights = allLightDevices(verified.devices).filter((d) => {
            const g = [...verified.groups.values()].find((group) => Array.isArray(group.deviceIDs) && group.deviceIDs.includes(d.instanceId));
            return g && !EXCLUDED_GROUPS.has(g.name);
          });
          const mismatches = verifyLights(verifiedLights, verified.groups, expectedForCommand(cmd, brightness));
          console.log(JSON.stringify({ ok: mismatches.length === 0, host, command: cmd, brightness, count: results.length, results, verify: { checked: verifiedLights.length, mismatches } }, null, 2));
          return;
        }
        console.log(JSON.stringify({ ok: true, host, command: cmd, brightness, count: results.length, results }, null, 2));
        return;
      }

      if (cmd === 'layout') {
        const layout = LAYOUTS[normalizeName(targetName)];
        if (!layout) die(`Unknown layout: ${targetName}`);
        const results = [];
        const actedSet = new Map();

        for (const floor of layout.off) {
          const floorLights = resolveFloorLights(lights, floor);
          for (const light of floorLights) {
            actedSet.set(light.instanceId, light);
            if (!light.alive) {
              results.push({ name: light.name, action: 'off', skipped: true, reason: 'offline' });
              continue;
            }
            const opResult = await withRetries(() => tradfri.operateLight(light, { onOff: false }, true));
            results.push({ name: light.name, action: 'off', result: opResult });
          }
        }

        for (const spec of layout.on) {
          const floorLights = resolveFloorLights(lights, spec.floor);
          for (const light of floorLights) {
            actedSet.set(light.instanceId, light);
            if (!light.alive) {
              results.push({ name: light.name, action: 'on', skipped: true, reason: 'offline' });
              continue;
            }
            const opResult = await withRetries(() => tradfri.operateLight(light, { dimmer: spec.brightness, onOff: spec.brightness > 0 }, true));
            results.push({ name: light.name, action: 'on', brightness: spec.brightness, result: opResult });
          }
        }

        actedLights = [...actedSet.values()];
        result = results;
        target = { name: `layout-${targetName}` };
      }

      if (cmd === 'floor-on' || cmd === 'floor-off') {
        const floorLights = resolveFloorLights(lights, targetName);
        if (cmd === 'floor-on') {
          numericValue = Number.isFinite(Number(value)) ? Number(value) : 50;
          if (!Number.isFinite(numericValue) || numericValue < 0 || numericValue > 100) die('Brightness must be 0-100');
        }
        const results = [];
        for (const light of floorLights) {
          if (!light.alive) {
            results.push({ name: light.name, skipped: true, reason: 'offline' });
            continue;
          }
          if (cmd === 'floor-on') {
            const opResult = await withRetries(() => tradfri.operateLight(light, { dimmer: numericValue, onOff: numericValue > 0 }, true));
            results.push({ name: light.name, result: opResult });
          } else {
            const opResult = await withRetries(() => tradfri.operateLight(light, { onOff: false }, true));
            results.push({ name: light.name, result: opResult });
          }
        }
        actedLights = floorLights;
        result = results;
        target = { name: `floor-${targetName}`, floor: String(targetName) };
      }

      if (cmd === 'light-on' || cmd === 'light-off' || cmd === 'brightness') {
        const lightMap = new Map(lights.map((d) => [d.instanceId, d]));
        const resolved = resolveByName(lightMap, targetName);
        target = resolved.match;
        if (!target) {
          die(`Light not found or ambiguous: ${targetName}\nCandidates: ${resolved.candidates.map((c) => c.name).join(', ') || '-'}`);
        }
        if (!target.alive) die(`Light is offline: ${target.name}`);

        if (cmd === 'light-on') result = await withRetries(() => tradfri.operateLight(target, { onOff: true }, true));
        if (cmd === 'light-off') result = await withRetries(() => tradfri.operateLight(target, { onOff: false }, true));
        if (cmd === 'brightness') {
          if (!Number.isFinite(numericValue) || numericValue < 0 || numericValue > 100) die('Brightness must be 0-100');
          result = await withRetries(() => tradfri.operateLight(target, { dimmer: numericValue, onOff: numericValue > 0 }, true));
        }
        actedLights = [target];
      }

      if (cmd === 'group-on' || cmd === 'group-off' || cmd === 'group-brightness') {
        const groupMap = new Map(usableGroups.map((g) => [g.instanceId, g]));
        const resolved = resolveByName(groupMap, targetName);
        target = resolved.match;
        if (!target) {
          die(`Group not found or ambiguous: ${targetName}\nCandidates: ${resolved.candidates.map((c) => c.name).join(', ') || '-'}`);
        }

        if (cmd === 'group-on') result = await withRetries(() => tradfri.operateGroup(target, { onOff: true }, true));
        if (cmd === 'group-off') result = await withRetries(() => tradfri.operateGroup(target, { onOff: false }, true));
        if (cmd === 'group-brightness') {
          if (!Number.isFinite(numericValue) || numericValue < 0 || numericValue > 100) die('Brightness must be 0-100');
          result = await withRetries(() => tradfri.operateGroup(target, { dimmer: numericValue, onOff: numericValue > 0 }, true));
        }
        actedLights = lights.filter((d) => Array.isArray(target.deviceIDs) && target.deviceIDs.includes(d.instanceId));
      }
    } finally {
      try { tradfri.destroy(); } catch {}
    }

    if (!result && !['light-on', 'light-off', 'brightness', 'group-on', 'group-off', 'group-brightness', 'floor-on', 'floor-off', 'layout'].includes(cmd)) {
      die(`Unknown command: ${cmd}`);
    }

    const response = {
      ok: true,
      host,
      command: cmd,
      target: target ? (target.deviceIDs ? summarizeGroup(target) : target.instanceId ? summarizeDevice(target, groups) : target) : undefined,
      result,
    };

    if (options.verify) {
      await sleep(options.settleMs);
      const verified = await snapshot();
      const verifiedLights = allLightDevices(verified.devices).filter((d) => actedLights.some((a) => a.instanceId === d.instanceId));
      let mismatches;
      if (cmd === 'layout') {
        mismatches = [];
        const byName = new Map(verifiedLights.map((d) => [d.name, d]));
        const layout = LAYOUTS[normalizeName(targetName)];
        for (const floor of layout.off) {
          for (const light of resolveFloorLights(verifiedLights, floor)) {
            const info = summarizeDevice(byName.get(light.name), verified.groups);
            if (info.alive && info.onOff !== false) mismatches.push({ name: info.name, reason: `expected onOff=false, got ${info.onOff}` });
          }
        }
        for (const spec of layout.on) {
          for (const light of resolveFloorLights(verifiedLights, spec.floor)) {
            const info = summarizeDevice(byName.get(light.name), verified.groups);
            if (!info.alive) continue;
            if (info.onOff !== true) mismatches.push({ name: info.name, reason: `expected onOff=true, got ${info.onOff}` });
            else if (!dimmerMatches(info.dimmer, spec.brightness)) mismatches.push({ name: info.name, reason: `expected dimmer≈${spec.brightness}, got ${info.dimmer}` });
          }
        }
      } else {
        const expected = expectedForCommand(cmd, numericValue);
        mismatches = verifyLights(verifiedLights, verified.groups, expected);
      }
      response.ok = mismatches.length === 0;
      response.verify = {
        checked: verifiedLights.map((d) => summarizeDevice(d, verified.groups)),
        mismatches,
      };
    }

    console.log(JSON.stringify(response, null, 2));
  } catch (e) {
    console.error(e && e.stack ? e.stack : e);
    process.exit(1);
  }
})();
