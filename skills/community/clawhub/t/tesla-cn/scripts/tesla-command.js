#!/usr/bin/env node

// 简单 Tesla 命令入口：
// 参数顺序为：
// 1) type=endpoints / commands / endpoints/commands
// 2) name=...
// 之后可选：vin=... data=...
//
// 已实现：
// - type=endpoints, name=list            → GET  /api/1/vehicles
// - type=commands, name=flash_lights    → POST /api/1/vehicles/{vin}/command/flash_lights
// - type=commands, name=door_lock       → POST /api/1/vehicles/{vin}/command/door_lock

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

const PROXY_URL = "https://tesla.dhuar.com";
const CONFIG_FILE_NAME = '.tesla_cn.json';

const config = {
  command: {
    auto_conditioning_start: {
      url: '/api/1/vehicles/{vin}/command/auto_conditioning_start',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    auto_conditioning_stop: {
      url: '/api/1/vehicles/{vin}/command/auto_conditioning_stop',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    charge_port_door_open: {
      url: '/api/1/vehicles/{vin}/command/charge_port_door_open',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    charge_port_door_close: {
      url: '/api/1/vehicles/{vin}/command/charge_port_door_close',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    honk_horn: {
      url: '/api/1/vehicles/{vin}/command/honk_horn',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    remote_boombox: {
      url: '/api/1/vehicles/{vin}/command/remote_boombox',
      method: 'POST',
      requiresVin: true,
      // 需要 data，例如：{"sound":2000}
      requiresData: true,
    },
    flash_lights: {
      url: '/api/1/vehicles/{vin}/command/flash_lights',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    door_lock: {
      url: '/api/1/vehicles/{vin}/command/door_lock',
      method: 'POST',
      requiresVin: true,
      requiresData: false,
    },
    actuate_trunk: {
      url: '/api/1/vehicles/{vin}/command/actuate_trunk',
      method: 'POST',
      requiresVin: true,
      // 需要 data，例如：{"which_trunk":"front"} 或 {"which_trunk":"rear"}
      requiresData: true,
    },
  },
  endpoint: {
    drivers: {
      url: '/api/1/vehicles/{vin}/drivers',
      method: 'GET',
      requiresVin: true,
    },
    eligible_subscriptions: {
      url: '/api/1/dx/vehicles/subscriptions/eligibility?vin={vin}',
      method: 'GET',
      requiresVin: true,
    },
    fleet_status: {
      url: '/api/1/vehicles/fleet_status',
      method: 'POST',
      requiresVin: false,
      requiresData: true,
    },
    vehicle: {
      url: '/api/1/vehicles/{vin}',
      method: 'GET',
      requiresVin: true,
    },
    vehicle_data: {
      url: '/api/1/vehicles/{vin}/vehicle_data',
      method: 'GET',
      requiresVin: true,
    },
    wake_up: {
      url: '/api/1/vehicles/{vin}/wake_up',
      method: 'POST',
      requiresVin: true,
    },
    list: {
      url: '/api/1/vehicles',
      method: 'GET',
      requiresVin: false,
    },
  },
};

function loadApiKeyFromConfig() {
  try {
    const homeDir = process.env.HOME || process.env.USERPROFILE;
    if (!homeDir) {
      return null;
    }
    const configPath = path.join(homeDir, CONFIG_FILE_NAME);
    if (!fs.existsSync(configPath)) {
      return null;
    }
    const raw = fs.readFileSync(configPath, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed.apiKey === 'string' && parsed.apiKey.trim()) {
      return parsed.apiKey.trim();
    }
    return null;
  } catch {
    return null;
  }
}

function buildRequest(type, name, { apiKey, vin, data }) {
  const group =
    type === 'endpoints'
      ? 'endpoint'
      : type === 'commands'
        ? 'command'
        : null;

  if (!group || !config[group] || !config[group][name]) {
    return null;
  }

  const { url, method, requiresVin, requiresData } = config[group][name];

  if (requiresVin && !vin) {
    throw new Error(`vin is required for ${name}`);
  }

  if (requiresData && !data) {
    throw new Error(`data is required for ${name}`);
  }

  let path = url;
  if (vin) {
    path = path.replace('{vin}', encodeURIComponent(vin));
  }

  const separator = path.includes('?') ? '&' : '?';
  const fullUrl = `${PROXY_URL}${path}${separator}apiKey=${encodeURIComponent(apiKey)}`;

  let fetchOptions = {};
  if (method === 'POST') {
    fetchOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data ? data : '{}',
    };
  }

  return { url: fullUrl, options: fetchOptions };
}

// 解析形如 key=value 的参数（value 可带引号）
function parseArgs(argv) {
  const result = {};

  for (const token of argv) {
    const eqIndex = token.indexOf('=');
    if (eqIndex === -1) {
      continue;
    }
    const key = token.slice(0, eqIndex);
    let value = token.slice(eqIndex + 1);

    // 去掉首尾成对引号（' 或 "）
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    result[key] = value;
  }

  return result;
}

async function main() {
  if (args.length < 2) {
    console.error('error');
    console.error('expected at least 2 arguments: type= name=');
    console.log(
      JSON.stringify({
        error: 'expected at least type and name',
      }),
    );
    process.exit(1);
  }

  // 位置约定：前两个参数分别是 type、name
  const [typeToken, nameToken, ...restTokens] = args;

  const headParsed = parseArgs([typeToken, nameToken]);
  const tailParsed = parseArgs(restTokens);

  const type = headParsed.type;
  const name = headParsed.name;
  const apiKey = loadApiKeyFromConfig();

  if (
    !type ||
    (type !== 'endpoints' && type !== 'commands' && type !== 'endpoints/commands')
  ) {
    console.error('error');
    console.error(
      'invalid type, expected type=endpoints, commands or endpoints/commands',
    );
    console.log(
      JSON.stringify({
        error: 'invalid type, expected endpoints, commands or endpoints/commands',
      }),
    );
    process.exit(1);
  }

  if (!name) {
    console.error('error');
    console.error('name is required');
    console.log(JSON.stringify({ error: 'name is required' }));
    process.exit(1);
  }

  if (!apiKey) {
    console.error('error');
    console.error('apiKey is required via ~/.tesla_cn.json');
    console.log(
      JSON.stringify({
        error: 'missing_apiKey',
        message:
          '未找到 apiKey。请前往 https://tesla.dhuar.com 获取 apiKey，并通过 init-tesla-config.js 写入 ~/.tesla_cn.json（内容形如 {"apiKey":"YOUR_API_KEY"}）。',
      }),
    );
    process.exit(1);
  }

  try {
    const request = buildRequest(type, name, {
      apiKey,
      vin: tailParsed.vin,
      data: tailParsed.data,
    });

    if (!request) {
      console.error('error');
      console.error(`unknown combination: type=${type}, name=${name}`);
      console.log(
        JSON.stringify({ error: `unknown combination: type=${type}, name=${name}` }),
      );
      process.exit(1);
    }

    const res = await fetch(request.url, request.options);
    const bodyText = await res.text();

    if (!res.ok) {
      console.error('error');
      console.log(bodyText);
      process.exit(1);
    }

    console.log(bodyText);
  } catch (e) {
    console.error('error');
    console.log(String(e && e.message ? e.message : e));
    process.exit(1);
  }
}

main();

