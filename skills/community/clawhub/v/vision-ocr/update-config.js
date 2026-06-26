#!/usr/bin/env node

/**
 * vision-ocr local config helper
 *
 * This script only reads VISION_* environment variables and writes the local
 * config.json in the skill directory. It does not read or modify any global
 * OpenClaw configuration files.
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const LOCAL_CONFIG = path.join(__dirname, 'config.json');
const EXAMPLE_CONFIG = path.join(__dirname, 'config.example.json');
const REQUIRED_FIELDS = [
  'ocr.imageocr.token',
  'ocr.imageocr.endpoint',
  'ocr.multimodal.baseUrl',
  'ocr.multimodal.token',
  'ocr.multimodal.model'
];

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level}] ${message}`);
}

function readJsonFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }

    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    log(`读取文件失败：${filePath} - ${error.message}`, 'ERROR');
    return null;
  }
}

function writeJsonFile(filePath, data) {
  try {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    log(`文件已更新：${filePath}`, 'SUCCESS');
    return true;
  } catch (error) {
    log(`写入文件失败：${filePath} - ${error.message}`, 'ERROR');
    return false;
  }
}

function buildEnvConfig() {
  return {
    ocr: {
      imageocr: {
        token: process.env.VISION_IMAGEOCR_TOKEN || undefined,
        endpoint: process.env.VISION_IMAGEOCR_ENDPOINT || undefined
      },
      multimodal: {
        baseUrl: process.env.VISION_BASE_URL || undefined,
        token: process.env.VISION_MULTIMODAL_TOKEN || undefined,
        model: process.env.VISION_MODEL || undefined
      }
    },
    autoSendToFeishu: process.env.VISION_AUTO_SEND_TO_FEISHU
      ? /^(1|true|yes)$/i.test(process.env.VISION_AUTO_SEND_TO_FEISHU)
      : undefined
  };
}

function mergeConfig(baseConfig, overrideConfig) {
  return {
    ...baseConfig,
    ...overrideConfig,
    ocr: {
      ...baseConfig?.ocr,
      ...overrideConfig?.ocr,
      imageocr: {
        ...baseConfig?.ocr?.imageocr,
        ...overrideConfig?.ocr?.imageocr
      },
      multimodal: {
        ...baseConfig?.ocr?.multimodal,
        ...overrideConfig?.ocr?.multimodal
      }
    }
  };
}

function getByPath(target, dottedPath) {
  return dottedPath.split('.').reduce((acc, key) => acc?.[key], target);
}

function getMissingFields(config) {
  return REQUIRED_FIELDS.filter(field => !getByPath(config, field));
}

function printSummary(config, missingFields) {
  console.log('\nLocal config status');
  console.log('-------------------');
  console.log('config.json:', fs.existsSync(LOCAL_CONFIG) ? LOCAL_CONFIG : 'not created');
  console.log('imageocr.token:', config?.ocr?.imageocr?.token ? 'configured' : 'missing');
  console.log('imageocr.endpoint:', config?.ocr?.imageocr?.endpoint || 'missing');
  console.log('multimodal.baseUrl:', config?.ocr?.multimodal?.baseUrl || 'missing');
  console.log('multimodal.token:', config?.ocr?.multimodal?.token ? 'configured' : 'missing');
  console.log('multimodal.model:', config?.ocr?.multimodal?.model || 'missing');
  console.log(
    'autoSendToFeishu:',
    typeof config?.autoSendToFeishu === 'boolean' ? String(config.autoSendToFeishu) : 'unset'
  );

  if (missingFields.length > 0) {
    console.log('\nMissing fields:');
    for (const field of missingFields) {
      console.log(`  - ${field}`);
    }
  } else {
    console.log('\nRequired fields are complete.');
  }
}

function loadBaseConfig() {
  return readJsonFile(LOCAL_CONFIG) || readJsonFile(EXAMPLE_CONFIG) || {};
}

async function main() {
  console.log('\nvision-ocr local config helper\n');

  const checkOnly = args.includes('--check');
  const forceUpdate = args.includes('--force');
  const envConfig = buildEnvConfig();
  const baseConfig = loadBaseConfig();
  const mergedConfig = mergeConfig(baseConfig, envConfig);
  const missingFields = getMissingFields(mergedConfig);

  printSummary(mergedConfig, missingFields);

  if (checkOnly) {
    process.exit(missingFields.length === 0 ? 0 : 1);
  }

  const hasVisionEnv = Object.keys(process.env).some(name => name.startsWith('VISION_'));
  if (!forceUpdate && !hasVisionEnv) {
    log('未检测到任何 VISION_* 环境变量，未改写本地配置。', 'WARN');
    console.log('\n如需写入本地 config.json，请先设置对应的 VISION_* 环境变量，再运行该命令。');
    process.exit(missingFields.length === 0 ? 0 : 1);
  }

  if (!writeJsonFile(LOCAL_CONFIG, mergedConfig)) {
    process.exit(1);
  }

  log(`仅更新技能目录本地配置：${LOCAL_CONFIG}`, 'SUCCESS');
}

main().catch(error => {
  log(`执行失败：${error.message}`, 'ERROR');
  process.exit(1);
});

