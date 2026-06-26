#!/usr/bin/env node
/**
 * wallpaper.js — AI Wallpaper Generator (zero neta-skills dependency)
 *
 * Commands:
 *   node wallpaper.js gen <prompt> [options]   → {status, url, task_uuid, device, width, height}
 *
 * Options:
 *   --device mobile|desktop|ultrawide|ipad   (default: mobile)
 *   --char   <name>                          Character name (optional)
 *   --pic    <uuid>                          Character picture UUID (optional)
 *   --style  <name>                          Style element, e.g. "cinematic" (repeatable)
 *
 * Device presets:
 *   mobile     576×1024  (9:16)   — iPhone / Android
 *   desktop    1024×576  (16:9)   — Desktop / laptop
 *   ultrawide  1024×432  (21:9)   — Ultrawide monitor
 *   ipad       768×1024  (3:4)    — iPad / tablet
 *
 */

// ── Config ────────────────────────────────────────────────────────────────────

const BASE = 'https://api.talesofai.com';

function getToken() {
  const idx = process.argv.indexOf('--token');
  if (idx !== -1 && process.argv[idx + 1]) return process.argv[idx + 1];
  throw new Error('Token required. Pass via: --token YOUR_TOKEN');
}

const HEADERS = {
  'x-token': getToken(),
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function api(method, path, body) {
  const res = await fetch(BASE + path, {
    method,
    headers: HEADERS,
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

const log = msg => process.stderr.write(msg + '\n');
const out = data => console.log(JSON.stringify(data));

// ── Device presets ────────────────────────────────────────────────────────────

const DEVICES = {
  mobile:    { width: 576,  height: 1024, label: 'Mobile (9:16)'    },
  desktop:   { width: 1024, height: 576,  label: 'Desktop (16:9)'   },
  ultrawide: { width: 1024, height: 432,  label: 'Ultrawide (21:9)' },
  ipad:      { width: 768,  height: 1024, label: 'iPad (3:4)'       },
};

// ── Parse argv ────────────────────────────────────────────────────────────────

function parseFlags(args) {
  const flags = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      flags[key] = flags[key] === undefined ? val : [].concat(flags[key], val);
    } else {
      flags._.push(args[i]);
    }
  }
  return flags;
}

// ── gen ───────────────────────────────────────────────────────────────────────

const [,, cmd, ...rawArgs] = process.argv;

if (cmd === 'gen') {
  const flags      = parseFlags(rawArgs);
  const prompt     = flags._.join(' ');
  const deviceKey  = flags.device ?? 'mobile';
  const charName   = flags.char   ?? null;
  const picUuid    = flags.pic    ?? null;
  const styles     = [].concat(flags.style ?? []);

  if (!prompt && !charName) {
    throw new Error('Usage: wallpaper.js gen <prompt> [--device mobile|desktop|ultrawide|ipad] [--char name] [--pic uuid] [--style name]');
  }

  const device = DEVICES[deviceKey] ?? DEVICES.mobile;
  log(`📱 Generating ${device.label} wallpaper...`);

  // 1. Resolve character vtoken
  const vtokens = [];
  let resolvedChar = null;

  if (charName) {
    log(`🔍 Looking up character: ${charName}...`);
    const search = await api('GET',
      `/v2/travel/parent-search?keywords=${encodeURIComponent(charName)}&parent_type=oc&sort_scheme=exact&page_index=0&page_size=1`);
    resolvedChar = search.list?.find(r => r.type === 'oc');
    if (resolvedChar) {
      vtokens.push({ type: 'oc_vtoken_adaptor', uuid: resolvedChar.uuid, name: resolvedChar.name, value: resolvedChar.uuid, weight: 1 });
      log(`✅ Character resolved: ${resolvedChar.name}`);
    } else {
      log(`⚠️  Character "${charName}" not found — using freetext`);
    }
  }

  // 2. Style vtokens
  for (const style of styles) {
    vtokens.push({ type: 'freetext', value: `/${style}`, weight: 1 });
  }

  // 3. Prompt — append wallpaper quality boosters
  let promptText = prompt;
  if (resolvedChar && promptText) {
    promptText = promptText.replace(new RegExp(`@${charName}[,，\\s]*`, 'g'), '').trim();
  }
  // Wallpaper-specific quality suffix
  const wallpaperSuffix = 'wallpaper, high resolution, ultra detailed, visually striking';
  if (promptText) {
    vtokens.push({ type: 'freetext', value: `${promptText}, ${wallpaperSuffix}`, weight: 1 });
  } else {
    vtokens.push({ type: 'freetext', value: wallpaperSuffix, weight: 1 });
  }

  // 4. Submit
  log(`🎨 Rendering at ${device.width}×${device.height}...`);
  const taskUuid = await api('POST', '/v3/make_image', {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: vtokens,
    width:  device.width,
    height: device.height,
    meta: { entrance: 'PICTURE' },
    ...(picUuid ? { inherit_params: { picture_uuid: picUuid } } : {}),
  });

  const task_uuid = typeof taskUuid === 'string' ? taskUuid : taskUuid?.task_uuid;
  log(`⏳ Task submitted: ${task_uuid}`);

  // 5. Poll (max 3 min)
  let warnedSlow = false;
  for (let i = 0; i < 90; i++) {
    await new Promise(r => setTimeout(r, 2000));
    if (!warnedSlow && i >= 14) {
      log('⏳ Still rendering, hang tight...');
      warnedSlow = true;
    }
    const result = await api('GET', `/v1/artifact/task/${task_uuid}`);
    if (result.task_status !== 'PENDING' && result.task_status !== 'MODERATION') {
      out({
        status: result.task_status,
        url:    result.artifacts?.[0]?.url ?? null,
        task_uuid,
        device: deviceKey,
        width:  device.width,
        height: device.height,
      });
      process.exit(0);
    }
  }

  out({ status: 'TIMEOUT', url: null, task_uuid, device: deviceKey, width: device.width, height: device.height });
}

else {
  process.stderr.write([
    'Usage:',
    '  node wallpaper.js gen <prompt> [--device mobile|desktop|ultrawide|ipad] [--char name] [--pic uuid] [--style name]',
    '',
    'Devices:',
    '  mobile     576×1024  (9:16)  — iPhone / Android',
    '  desktop    1024×576  (16:9)  — Desktop / laptop',
    '  ultrawide  1024×432  (21:9)  — Ultrawide monitor',
    '  ipad       768×1024  (3:4)   — iPad / tablet',
  ].join('\n') + '\n');
  process.exit(1);
}
