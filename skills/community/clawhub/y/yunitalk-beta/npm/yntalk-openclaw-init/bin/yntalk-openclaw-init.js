#!/usr/bin/env node

import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';

const PUBLIC_IP_SERVICES = [
  'https://api64.ipify.org',
  'https://api.ipify.org',
  'https://ifconfig.me',
  'https://ip.sb'
];
const OPENCLAW_CONFIG_FILE = 'openclaw.json';
const QR_OUTPUT_SCALE = 1;
const DEFAULT_GATEWAY_PORT = 18789;

function usage() {
  return [
    'Usage:',
    '  yntalk-openclaw-init',
    '  yntalk-openclaw-init -v',
    '  yntalk-openclaw-init -h',
    '',
    'Options:',
    '  -h, --help       Show this help message.',
    '  -v, --verbose    Show OpenClaw lookup logs.',
    '',
    'Default output:',
    '  Prints the scannable "/openclaw --init <base64-json>" command and a 1x1 scale terminal QR code.',
    ''
  ].join('\n');
}

function parseArgs(argv) {
  const opts = {
    help: false,
    verbose: false
  };

  for (const arg of argv) {
    if (arg === '--help' || arg === '-h') {
      opts.help = true;
    } else if (arg === '--verbose' || arg === '-v') {
      opts.verbose = true;
    } else {
      throw new Error('unknown argument: ' + arg);
    }
  }

  return opts;
}

function normalizeOpenClawURL(value) {
  return String(value || '').trim().replace(/\/+$/g, '');
}

function stripOpenAIBasePath(value) {
  const normalized = normalizeOpenClawURL(value);
  if (!normalized) return '';
  return normalized.replace(/\/v1$/i, '');
}

function normalizeToken(value) {
  return String(value || '').trim();
}

function payloadToBase64(payload) {
  return Buffer.from(JSON.stringify(payload), 'utf8').toString('base64');
}

function valueAtPath(source, pathText) {
  let current = source;
  for (const key of pathText.split('.')) {
    if (!current || typeof current !== 'object') return '';
    current = current[key];
  }
  return current === undefined || current === null ? '' : String(current);
}

function findFirstValue(source, paths) {
  for (const pathText of paths) {
    const value = valueAtPath(source, pathText);
    if (value) return value;
  }
  return '';
}

function normalizeOpenClawPayload(payload) {
  payload = payload || {};
  const openclawURL = normalizeOpenClawURL(
    payload.OPENCLAW_URL ||
    payload.openclaw_url ||
    payload.openclawUrl ||
    payload.url ||
    payload.gateway_url ||
    payload.gatewayUrl ||
    findFirstValue(payload, [
      'gateway.url',
      'gateway.base_url',
      'gateway.baseUrl',
      'config.gateway.url',
      'config.OPENCLAW_URL',
      'env.OPENCLAW_URL'
    ])
  );
  const openclawToken = normalizeToken(
    payload.OPENCLAW_TOKEN ||
    payload.openclaw_token ||
    payload.openclawToken ||
    payload.token ||
    payload.gateway_token ||
    payload.gatewayToken ||
    findFirstValue(payload, [
      'gateway.token',
      'gateway.gateway_token',
      'gateway.gatewayToken',
      'config.gateway.token',
      'config.OPENCLAW_TOKEN',
      'env.OPENCLAW_TOKEN'
    ])
  );

  if (!openclawURL || !openclawToken) return null;
  return {
    OPENCLAW_URL: openclawURL,
    OPENCLAW_TOKEN: openclawToken
  };
}

function compactErrorText(value) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  return text.length > 220 ? text.slice(0, 220) + '...' : text;
}

function verboseLog(enabled, message) {
  if (enabled) process.stderr.write('[yntalk-openclaw-init] ' + message + '\n');
}

function uniqueStrings(values) {
  return Array.from(new Set(values.filter(Boolean)));
}

function openClawConfigCandidates() {
  const home = os.homedir();
  const cwd = process.cwd();
  const parents = [];
  let current = cwd;
  while (current && current !== path.dirname(current)) {
    parents.push(path.join(current, OPENCLAW_CONFIG_FILE));
    parents.push(path.join(current, '.openclaw', OPENCLAW_CONFIG_FILE));
    current = path.dirname(current);
  }

  return uniqueStrings([
    process.env.OPENCLAW_CONFIG,
    ...parents,
    path.join(home, OPENCLAW_CONFIG_FILE),
    path.join(home, '.openclaw', OPENCLAW_CONFIG_FILE),
    path.join(home, '.config', 'openclaw', OPENCLAW_CONFIG_FILE),
    path.join(home, 'Library', 'Application Support', 'OpenClaw', OPENCLAW_CONFIG_FILE)
  ]);
}

async function readJSONFile(filePath) {
  const text = await fs.readFile(filePath, 'utf8');
  return JSON.parse(text.replace(/^\uFEFF/, ''));
}

async function readOpenClawConfig(verbose) {
  const errors = [];
  for (const filePath of openClawConfigCandidates()) {
    verboseLog(verbose, 'try config: ' + filePath);
    try {
      const config = await readJSONFile(filePath);
      verboseLog(verbose, 'matched config: ' + filePath);
      return { config, filePath };
    } catch (err) {
      if (err && err.code === 'ENOENT') continue;
      const detail = compactErrorText(err && err.message ? err.message : String(err));
      errors.push(filePath + ': ' + detail);
      verboseLog(verbose, filePath + ': ' + detail);
    }
  }

  throw new Error([
    'failed to find local OpenClaw config file.',
    'Expected openclaw.json in current directory, parent directories, ~/.openclaw, or ~/.config/openclaw.',
    errors.length ? 'Read errors:\n' + errors.join('\n') : ''
  ].filter(Boolean).join('\n'));
}

function firstConfigValue(config, paths) {
  const value = findFirstValue(config, paths);
  return value ? String(value).trim() : '';
}

function readGatewayToken(config) {
  return normalizeToken(firstConfigValue(config, [
    'gateway.auth.token',
    'gateway.token',
    'gateway.access_token',
    'gateway.accessToken',
    'gateway.auth_token',
    'gateway.authToken',
    'gateway.bearer_token',
    'gateway.bearerToken',
    'gateway.api_key',
    'gateway.apiKey',
    'gateway.secret',
    'gateway.key',
    'config.gateway.token',
    'services.gateway.token',
    'auth.gateway.token'
  ]));
}

function hostForURL(host) {
  return String(host || '').includes(':') ? '[' + host + ']' : String(host || '');
}

function isPrivateIPv4(address) {
  return address.startsWith('10.') ||
    address.startsWith('192.168.') ||
    /^172\.(1[6-9]|2\d|3[0-1])\./.test(address);
}

function readLocalLANIP() {
  const addresses = [];
  const interfaces = os.networkInterfaces();
  for (const items of Object.values(interfaces)) {
    for (const item of items || []) {
      if (!item || item.internal || item.family !== 'IPv4') continue;
      const address = String(item.address || '').trim();
      if (!address || address === '0.0.0.0' || address.startsWith('127.') || address.startsWith('169.254.')) continue;
      addresses.push(address);
    }
  }
  return addresses.find(isPrivateIPv4) || addresses[0] || '';
}

function gatewayURLWithHost(port, host) {
  return normalizeOpenClawURL('http://' + hostForURL(host) + ':' + port);
}

function gatewayURLWithLANHost(port) {
  const localIP = readLocalLANIP();
  if (!localIP) {
    throw new Error('failed to find LAN IPv4 address for OpenClaw gateway URL');
  }
  return gatewayURLWithHost(port, localIP);
}

function openAIBaseURL(openclawURL) {
  return stripOpenAIBasePath(openclawURL) + '/v1';
}

async function readPublicIP(verbose) {
  for (const serviceURL of PUBLIC_IP_SERVICES) {
    verboseLog(verbose, 'fetch public ip: ' + serviceURL);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 3000);
    try {
      const response = await fetch(serviceURL, {
        signal: controller.signal,
        headers: { 'User-Agent': 'yntalk-openclaw-init' }
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const text = (await response.text()).trim();
      if (!/^[0-9a-fA-F:.]+$/.test(text)) throw new Error('invalid public IP response: ' + text);
      verboseLog(verbose, 'public ip: ' + text);
      return text;
    } catch (err) {
      verboseLog(verbose, serviceURL + ': ' + compactErrorText(err && err.message ? err.message : String(err)));
    } finally {
      clearTimeout(timer);
    }
  }
  return '';
}

function readGatewayPort(config) {
  const raw = firstConfigValue(config, [
    'gateway.port',
    'gateway.http.port',
    'config.gateway.port',
    'services.gateway.port'
  ]);
  const port = Number(raw || DEFAULT_GATEWAY_PORT);
  if (!Number.isInteger(port) || port <= 0 || port > 65535) {
    throw new Error('invalid gateway.port in openclaw.json: ' + raw);
  }
  return port;
}

function readGatewayBind(config) {
  return firstConfigValue(config, [
    'gateway.bind',
    'gateway.host',
    'gateway.http.bind',
    'gateway.http.host',
    'config.gateway.bind',
    'services.gateway.bind'
  ]) || 'localhost';
}

function isPublicGatewayBind(bind) {
  const value = String(bind || '').trim().toLowerCase();
  return value === 'lan' || value === 'all' || value === '0.0.0.0' || value === '::';
}

function readChatCompletionsEnabled(config) {
  const value = firstConfigValue(config, [
    'gateway.http.endpoints.chatCompletions.enabled',
    'gateway.http.endpoints.chat_completions.enabled',
    'gateway.endpoints.chatCompletions.enabled',
    'gateway.chatCompletions.enabled'
  ]);
  if (value === '') return false;
  return ['true', '1', 'yes', 'on'].includes(String(value).trim().toLowerCase());
}

async function readOpenClawInfoFromLocalConfig(verbose) {
  const { config, filePath } = await readOpenClawConfig(verbose);
  const gatewayPort = readGatewayPort(config);
  const gatewayBind = readGatewayBind(config);
  const chatEnabled = readChatCompletionsEnabled(config);
  const lanURL = gatewayURLWithLANHost(gatewayPort);
  const publicIP = await readPublicIP(verbose);
  const publicURL = publicIP ? gatewayURLWithHost(gatewayPort, publicIP) : lanURL;
  const openclawToken = readGatewayToken(config);

  if (!lanURL || !publicURL || !openclawToken) {
    throw new Error([
      'failed to read OpenClaw connection info from ' + filePath + '.',
      !lanURL ? 'Missing LAN gateway address from openclaw.json.' : '',
      !publicURL ? 'Failed to build public gateway address from public IP.' : '',
      !openclawToken ? 'Missing gateway token in openclaw.json.' : ''
    ].filter(Boolean).join('\n'));
  }

  const payload = normalizeOpenClawPayload({
    OPENCLAW_URL: publicURL,
    OPENCLAW_TOKEN: openclawToken
  });
  return {
    payload: {
      ...payload,
      OPENCLAW_LAN_URL: lanURL
    },
    lanURL,
    publicURL,
    openAIBaseURL: openAIBaseURL(publicURL),
    openAIBaseLANURL: openAIBaseURL(lanURL),
    gatewayBind,
    gatewayPort,
    authMode: firstConfigValue(config, ['gateway.auth.mode']) || 'none',
    chatEnabled,
    publicReachable: isPublicGatewayBind(gatewayBind),
    publicIP
  };
}

const QR_ECC_CODEWORDS_PER_BLOCK_LOW = [
  -1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28,
  28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30
];
const QR_NUM_ERROR_CORRECTION_BLOCKS_LOW = [
  -1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8,
  8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25
];

function makeQRCode(text) {
  const data = Array.from(Buffer.from(text, 'utf8'));
  for (let version = 1; version <= 40; version++) {
    const dataCapacity = getNumDataCodewords(version);
    const countBits = version <= 9 ? 8 : 16;
    const neededBits = 4 + countBits + data.length * 8;
    if (neededBits <= dataCapacity * 8) {
      return makeQRCodeForVersion(data, version, dataCapacity);
    }
  }
  throw new Error('QR content is too large');
}

function makeQRCodeForVersion(data, version, dataCapacity) {
  const countBits = version <= 9 ? 8 : 16;
  const bits = [];
  appendBits(bits, 0x4, 4);
  appendBits(bits, data.length, countBits);
  for (const b of data) appendBits(bits, b, 8);
  appendBits(bits, 0, Math.min(4, dataCapacity * 8 - bits.length));
  while (bits.length % 8 !== 0) bits.push(0);

  const dataCodewords = [];
  for (let i = 0; i < bits.length; i += 8) {
    let b = 0;
    for (let j = 0; j < 8; j++) b = (b << 1) | bits[i + j];
    dataCodewords.push(b);
  }
  for (let pad = 0xec; dataCodewords.length < dataCapacity; pad ^= 0xfd) {
    dataCodewords.push(pad);
  }

  const codewords = addErrorCorrectionAndInterleave(dataCodewords, version);
  const qr = new QRCanvas(version);
  qr.drawFunctionPatterns();
  qr.drawCodewords(codewords);
  qr.drawFormatBits(0);
  return qr;
}

function appendBits(bits, value, length) {
  for (let i = length - 1; i >= 0; i--) bits.push((value >>> i) & 1);
}

function getNumRawDataModules(version) {
  let result = (16 * version + 128) * version + 64;
  if (version >= 2) {
    const numAlign = Math.floor(version / 7) + 2;
    result -= (25 * numAlign - 10) * numAlign - 55;
    if (version >= 7) result -= 36;
  }
  return result;
}

function getNumDataCodewords(version) {
  const rawCodewords = Math.floor(getNumRawDataModules(version) / 8);
  return rawCodewords -
    QR_ECC_CODEWORDS_PER_BLOCK_LOW[version] * QR_NUM_ERROR_CORRECTION_BLOCKS_LOW[version];
}

function addErrorCorrectionAndInterleave(data, version) {
  const numBlocks = QR_NUM_ERROR_CORRECTION_BLOCKS_LOW[version];
  const blockEccLen = QR_ECC_CODEWORDS_PER_BLOCK_LOW[version];
  const rawCodewords = Math.floor(getNumRawDataModules(version) / 8);
  const numShortBlocks = numBlocks - rawCodewords % numBlocks;
  const shortBlockDataLen = Math.floor(rawCodewords / numBlocks) - blockEccLen;
  const rsDivisor = reedSolomonComputeDivisor(blockEccLen);

  const blocks = [];
  let offset = 0;
  for (let i = 0; i < numBlocks; i++) {
    const dataLen = shortBlockDataLen + (i < numShortBlocks ? 0 : 1);
    const dataBlock = data.slice(offset, offset + dataLen);
    offset += dataLen;
    const ecc = reedSolomonComputeRemainder(dataBlock, rsDivisor);
    blocks.push({ data: dataBlock, ecc });
  }

  const result = [];
  for (let i = 0; i <= shortBlockDataLen; i++) {
    for (let j = 0; j < blocks.length; j++) {
      if (i < blocks[j].data.length) result.push(blocks[j].data[i]);
    }
  }
  for (let i = 0; i < blockEccLen; i++) {
    for (const block of blocks) result.push(block.ecc[i]);
  }
  return result;
}

function reedSolomonComputeDivisor(degree) {
  const result = new Array(degree).fill(0);
  result[degree - 1] = 1;
  let root = 1;
  for (let i = 0; i < degree; i++) {
    for (let j = 0; j < result.length; j++) {
      result[j] = reedSolomonMultiply(result[j], root);
      if (j + 1 < result.length) result[j] ^= result[j + 1];
    }
    root = reedSolomonMultiply(root, 0x02);
  }
  return result;
}

function reedSolomonComputeRemainder(data, divisor) {
  const result = new Array(divisor.length).fill(0);
  for (const b of data) {
    const factor = b ^ result.shift();
    result.push(0);
    for (let i = 0; i < result.length; i++) {
      result[i] ^= reedSolomonMultiply(divisor[i], factor);
    }
  }
  return result;
}

function reedSolomonMultiply(x, y) {
  let z = 0;
  for (let i = 7; i >= 0; i--) {
    z = (z << 1) ^ ((z >>> 7) * 0x11d);
    z ^= ((y >>> i) & 1) * x;
  }
  return z & 0xff;
}

class QRCanvas {
  constructor(version) {
    this.version = version;
    this.size = version * 4 + 17;
    this.modules = Array.from({ length: this.size }, () => new Array(this.size).fill(false));
    this.functionModules = Array.from({ length: this.size }, () => new Array(this.size).fill(false));
  }

  setFunction(x, y, dark) {
    this.modules[y][x] = !!dark;
    this.functionModules[y][x] = true;
  }

  drawFunctionPatterns() {
    const size = this.size;
    this.drawFinderPattern(3, 3);
    this.drawFinderPattern(size - 4, 3);
    this.drawFinderPattern(3, size - 4);

    const align = this.alignmentPatternPositions();
    for (const x of align) {
      for (const y of align) {
        if (!this.functionModules[y][x]) this.drawAlignmentPattern(x, y);
      }
    }

    for (let i = 0; i < size; i++) {
      if (!this.functionModules[6][i]) this.setFunction(i, 6, i % 2 === 0);
      if (!this.functionModules[i][6]) this.setFunction(6, i, i % 2 === 0);
    }
    this.setFunction(8, size - 8, true);
    this.drawFormatBits(0);
    this.drawVersion();
  }

  drawFinderPattern(cx, cy) {
    for (let dy = -4; dy <= 4; dy++) {
      for (let dx = -4; dx <= 4; dx++) {
        const x = cx + dx;
        const y = cy + dy;
        if (x < 0 || y < 0 || x >= this.size || y >= this.size) continue;
        const dist = Math.max(Math.abs(dx), Math.abs(dy));
        this.setFunction(x, y, dist !== 2 && dist !== 4);
      }
    }
  }

  drawAlignmentPattern(cx, cy) {
    for (let dy = -2; dy <= 2; dy++) {
      for (let dx = -2; dx <= 2; dx++) {
        this.setFunction(cx + dx, cy + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
      }
    }
  }

  alignmentPatternPositions() {
    if (this.version === 1) return [];
    const numAlign = Math.floor(this.version / 7) + 2;
    const step = this.version === 32 ? 26 : Math.ceil((this.size - 13) / (numAlign * 2 - 2)) * 2;
    const result = [6];
    for (let pos = this.size - 7 - (numAlign - 2) * step; result.length < numAlign; pos += step) {
      result.push(pos);
    }
    return result;
  }

  drawFormatBits(mask) {
    const eclFormatBits = 1;
    const data = (eclFormatBits << 3) | mask;
    let rem = data;
    for (let i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
    const bits = ((data << 10) | rem) ^ 0x5412;
    const size = this.size;

    for (let i = 0; i <= 5; i++) this.setFunction(8, i, getBit(bits, i));
    this.setFunction(8, 7, getBit(bits, 6));
    this.setFunction(8, 8, getBit(bits, 7));
    this.setFunction(7, 8, getBit(bits, 8));
    for (let i = 9; i < 15; i++) this.setFunction(14 - i, 8, getBit(bits, i));
    for (let i = 0; i < 8; i++) this.setFunction(size - 1 - i, 8, getBit(bits, i));
    for (let i = 8; i < 15; i++) this.setFunction(8, size - 15 + i, getBit(bits, i));
    this.setFunction(8, size - 8, true);
  }

  drawVersion() {
    if (this.version < 7) return;
    let rem = this.version;
    for (let i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25);
    const bits = (this.version << 12) | rem;
    for (let i = 0; i < 18; i++) {
      const bit = getBit(bits, i);
      const a = this.size - 11 + (i % 3);
      const b = Math.floor(i / 3);
      this.setFunction(a, b, bit);
      this.setFunction(b, a, bit);
    }
  }

  drawCodewords(codewords) {
    const dataBits = [];
    for (const b of codewords) {
      for (let i = 7; i >= 0; i--) dataBits.push(((b >>> i) & 1) !== 0);
    }

    let i = 0;
    for (let right = this.size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (let vert = 0; vert < this.size; vert++) {
        for (let j = 0; j < 2; j++) {
          const x = right - j;
          const upward = ((right + 1) & 2) === 0;
          const y = upward ? this.size - 1 - vert : vert;
          if (this.functionModules[y][x]) continue;
          let dark = i < dataBits.length ? dataBits[i] : false;
          i++;
          if ((x + y) % 2 === 0) dark = !dark;
          this.modules[y][x] = dark;
        }
      }
    }
  }
}

function getBit(value, index) {
  return ((value >>> index) & 1) !== 0;
}

function qrToTerminal(qr, scale = QR_OUTPUT_SCALE) {
  const margin = 2;
  const rows = [];
  const sourceSize = qr.size + margin * 2;
  const pixelSize = sourceSize * Math.max(1, scale);

  function darkAt(pixelX, pixelY) {
    const sourceX = Math.floor(pixelX * sourceSize / pixelSize) - margin;
    const sourceY = Math.floor(pixelY * sourceSize / pixelSize) - margin;
    return sourceX >= 0 && sourceY >= 0 && sourceX < qr.size && sourceY < qr.size && qr.modules[sourceY][sourceX];
  }

  for (let y = 0; y < pixelSize; y += 2) {
    let line = '';
    for (let x = 0; x < pixelSize; x++) {
      const top = darkAt(x, y);
      const bottom = y + 1 < pixelSize && darkAt(x, y + 1);
      if (top && bottom) {
        line += '█';
      } else if (top) {
        line += '▀';
      } else if (bottom) {
        line += '▄';
      } else {
        line += ' ';
      }
    }
    rows.push(line);
  }
  return rows.join('\n');
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    process.stdout.write(usage());
    return;
  }

  const result = await readOpenClawInfoFromLocalConfig(opts.verbose);
  const payload = result.payload;
  if (!payload) throw new Error('OpenClaw connection info is incomplete.');

  const encoded = payloadToBase64(payload);
  const command = '/openclaw --init ' + encoded;
  const qr = makeQRCode(command);

  process.stdout.write('局域网访问地址:\n');
  process.stdout.write(result.lanURL + '\n\n');
  process.stdout.write('局域网 OpenAI Base URL:\n');
  process.stdout.write(result.openAIBaseLANURL + '\n\n');
  process.stdout.write('公网访问地址:\n');
  process.stdout.write(result.publicURL + '\n\n');
  process.stdout.write('公网 OpenAI Base URL:\n');
  process.stdout.write(result.openAIBaseURL + '\n\n');
  process.stdout.write('Gateway:\n');
  process.stdout.write('bind: ' + result.gatewayBind + '\n');
  process.stdout.write('port: ' + result.gatewayPort + '\n');
  process.stdout.write('auth_mode: ' + result.authMode + '\n');
  process.stdout.write('chatCompletions: ' + (result.chatEnabled ? 'enabled' : 'disabled') + '\n\n');
  process.stdout.write('扫码连接内容:\n');
  process.stdout.write(command + '\n\n');
  process.stdout.write('二维码(1x1):\n');
  process.stdout.write(qrToTerminal(qr, QR_OUTPUT_SCALE) + '\n');

  if (!result.chatEnabled) {
    process.stderr.write('yntalk-openclaw-init: warning: gateway.http.endpoints.chatCompletions.enabled is not true; OpenClaw Chat may not respond.\n');
  }
  if (!result.publicReachable) {
    process.stderr.write('yntalk-openclaw-init: warning: gateway.bind is "' + result.gatewayBind + '"; public access may fail unless the gateway is reachable from outside.\n');
  }
  if (!result.publicIP) {
    process.stderr.write('yntalk-openclaw-init: warning: failed to detect public IP; public URL fell back to LAN URL.\n');
  }
}

main().catch((err) => {
  process.stderr.write('yntalk-openclaw-init: ' + (err && err.message ? err.message : String(err)) + '\n\n');
  process.stderr.write(usage());
  process.exit(1);
});
