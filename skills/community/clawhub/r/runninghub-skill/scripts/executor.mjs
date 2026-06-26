#!/usr/bin/env node
/**
 * RHMCP Skill Executor - OpenClaw 智能决策层
 *
 * 功能：
 * 1. 加载 RHMCP 配置和 APP 定义
 * 2. 提供智能决策（参数默认值、存储模式选择）
 * 3. 作为命令行工具使用，方便调试
 *
 * 使用方式：
 *   node executor.mjs list                    # 列出推荐APP
 *   node executor.mjs info <alias>           # 查看APP参数
 *   node executor.mjs decide <context>       # 智能存储决策
 *   node executor.mjs defaults <alias>        # 获取参数默认值
 */

import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ============================================
// 配置加载
// ============================================

/**
 * 加载 RHMCP 配置
 */
function loadRHMCPConfig() {
  // 尝试多个可能的配置目录
  const configDirs = [
    process.env.RHMCP_CONFIG,
    join(__dirname, "../../../"), // RHMCP 根目录
    process.cwd(),
  ].filter(Boolean);

  for (const dir of configDirs) {
    const servicePath = join(dir, "service.json");
    const appsPath = join(dir, "apps.json");

    if (existsSync(servicePath) || existsSync(appsPath)) {
      const service = existsSync(servicePath) ? JSON.parse(readFileSync(servicePath, "utf-8")) : {};

      let apps = { server: {}, user: {} };
      if (existsSync(appsPath)) {
        apps = JSON.parse(readFileSync(appsPath, "utf-8"));
      }

      return {
        configDir: dir,
        service,
        apps,
        mergedApps: mergeApps(apps),
      };
    }
  }

  return null;
}

/**
 * 合并 server 和 user APP 配置
 */
function mergeApps(appsConfig) {
  if (!appsConfig) return {};

  const merged = {};

  if (appsConfig.server) {
    for (const [alias, app] of Object.entries(appsConfig.server)) {
      if (!alias.startsWith("_")) {
        merged[alias] = app;
      }
    }
  }

  if (appsConfig.user) {
    for (const [alias, app] of Object.entries(appsConfig.user)) {
      if (!alias.startsWith("_")) {
        merged[alias] = app;
      }
    }
  }

  return merged;
}

/**
 * 加载推荐APP列表
 */
function loadRecommendedApps() {
  const recommendedPath = join(__dirname, "../references/recommended-apps.json");
  if (existsSync(recommendedPath)) {
    return JSON.parse(readFileSync(recommendedPath, "utf-8"));
  }
  return { apps: {} };
}

// ============================================
// 智能决策
// ============================================

/**
 * 存储模式智能决策
 */
function decideStorageMode(context) {
  const {
    isChainStep = false, // 是否是链式流程中间步骤
    userRequestedSave = false, // 用户明确要保存
    outputType = "url", // 输出类型
  } = context;

  // 链式流程中间步骤：返回 URL 即可
  if (isChainStep) {
    return "none";
  }

  // 用户明确要保存
  if (userRequestedSave) {
    return "network";
  }

  // 默认：返回 URL
  return "none";
}

/**
 * 获取APP参数默认值
 */
function getParamDefaults(alias, apps) {
  const app = apps[alias];
  if (!app) return null;

  const defaults = {};

  if (app.inputs) {
    for (const [key, config] of Object.entries(app.inputs)) {
      if (config.default !== undefined) {
        defaults[key] = config.default;
      }
    }
  }

  // 预设默认值
  const presetDefaults = {
    "qwen-text-to-image": {
      width: 1024,
      height: 1024,
    },
  };

  return { ...presetDefaults[alias], ...defaults };
}

/**
 * 场景 → APP 映射
 */
function mapSceneToApp(scene) {
  const sceneMap = {
    "generate-image": "qwen-text-to-image",
    "text-to-image": "qwen-text-to-image",
    text2img: "qwen-text-to-image",
    文生图: "qwen-text-to-image",
    生成图片: "qwen-text-to-image",
    画画: "qwen-text-to-image",

    "modify-image": "qwen-image-to-image",
    "image-to-image": "qwen-image-to-image",
    img2img: "qwen-image-to-image",
    图生图: "qwen-image-to-image",
    改图: "qwen-image-to-image",

    "image-to-video": "image-to-video",
    img2video: "image-to-video",
    图生视频: "image-to-video",
    视频: "image-to-video",
  };

  const normalizedScene = scene.toLowerCase().replace(/[_\s]/g, "-");
  return sceneMap[normalizedScene] || sceneMap[scene] || null;
}

/**
 * 推荐APP
 */
function recommendApp(scene) {
  const alias = mapSceneToApp(scene);
  if (!alias) return null;

  const config = loadRHMCPConfig();
  const apps = config?.mergedApps || loadRecommendedApps().apps;
  const app = apps[alias];

  if (!app) return null;

  const defaults = getParamDefaults(alias, apps);

  return {
    alias,
    appId: app.appId,
    category: app.category,
    description: app.description,
    inputs: app.inputs,
    defaults,
    usage: generateUsageExample(alias, app, defaults),
  };
}

/**
 * 生成使用示例
 */
function generateUsageExample(alias, app, defaults) {
  const params = {};

  if (app.inputs) {
    for (const [key, config] of Object.entries(app.inputs)) {
      if (config.description) {
        params[key] = `<${config.description}>`;
      }
    }
  }

  // 如果有默认值，填充
  if (defaults) {
    for (const [key, value] of Object.entries(defaults)) {
      params[key] = value;
    }
  }

  return {
    tool: "rh_execute_app",
    args: {
      alias,
      params,
    },
  };
}

// ============================================
// CLI 命令
// ============================================

function cmdList() {
  const config = loadRHMCPConfig();

  if (!config) {
    console.error("错误: 未找到 RHMCP 配置");
    console.error("请确保 RHMCP_CONFIG 环境变量正确，或在 RHMCP 目录下运行");
    process.exit(1);
  }

  console.log("\n可用 APP 列表:\n");
  console.log("别名".padEnd(25), "类型".padEnd(10), "APP ID".padEnd(25), "说明");
  console.log("-".repeat(80));

  for (const [alias, app] of Object.entries(config.mergedApps)) {
    console.log(
      alias.padEnd(25),
      (app.category || "unknown").padEnd(10),
      (app.appId || "-").padEnd(25),
      app.description || "-"
    );
  }

  console.log("\n共", Object.keys(config.mergedApps).length, "个 APP");
}

function cmdInfo(alias) {
  const config = loadRHMCPConfig();

  if (!config) {
    console.error("错误: 未找到 RHMCP 配置");
    process.exit(1);
  }

  const app = config.mergedApps[alias];

  if (!app) {
    console.error(`错误: 未找到 APP "${alias}"`);
    console.error('使用 "list" 命令查看所有可用 APP');
    process.exit(1);
  }

  console.log(`\n${alias} 详情:\n`);
  console.log("  APP ID:", app.appId);
  console.log("  类型:", app.category || "unknown");
  console.log("  说明:", app.description || "-");

  if (app.inputs) {
    console.log("\n  参数:");
    for (const [key, config] of Object.entries(app.inputs)) {
      const required = config.required === false ? "(可选)" : "(必填)";
      console.log(`    - ${key} ${required}`);
      console.log(`        nodeId: ${config.nodeId}`);
      console.log(`        fieldName: ${config.fieldName}`);
      if (config.description) console.log(`        说明: ${config.description}`);
      if (config.default !== undefined) console.log(`        默认值: ${config.default}`);
    }
  }

  const usage = generateUsageExample(alias, app, getParamDefaults(alias, config.mergedApps));
  console.log("\n  使用示例:");
  console.log("  ", JSON.stringify(usage, null, 2).replace(/\n/g, "\n  "));
}

function cmdDecide(contextJson) {
  try {
    const context = JSON.parse(contextJson);
    const mode = decideStorageMode(context);
    console.log(JSON.stringify({ storage: mode }, null, 2));
  } catch (e) {
    console.error("错误: 无效的 JSON 输入");
    console.error(
      '示例: node executor.mjs decide \'{"isChainStep":false,"userRequestedSave":true}\''
    );
    process.exit(1);
  }
}

function cmdDefaults(alias) {
  const config = loadRHMCPConfig();

  if (!config) {
    console.error("错误: 未找到 RHMCP 配置");
    process.exit(1);
  }

  const defaults = getParamDefaults(alias, config.mergedApps);

  if (!defaults) {
    console.error(`错误: 未找到 APP "${alias}" 或无默认值`);
    process.exit(1);
  }

  console.log(JSON.stringify(defaults, null, 2));
}

function cmdRecommend(scene) {
  const result = recommendApp(scene);

  if (!result) {
    console.error(`错误: 无法识别场景 "${scene}"`);
    console.error("已知场景: generate-image, modify-image, image-to-video");
    process.exit(1);
  }

  console.log(JSON.stringify(result, null, 2));
}

// ============================================
// 主入口
// ============================================

function printHelp() {
  console.log(`
使用方式:
  node executor.mjs <command> [args]

命令:
  list                    列出所有可用 APP
  info <alias>            查看 APP 参数详情
  decide <context>        智能存储决策 (JSON)
  defaults <alias>        获取参数默认值
  recommend <scene>       根据场景推荐 APP

示例:
  node executor.mjs list
  node executor.mjs info qwen-text-to-image
  node executor.mjs decide '{"isChainStep":true}'
  node executor.mjs defaults qwen-text-to-image
  node executor.mjs recommend generate-image

环境变量:
  RHMCP_CONFIG            RHMCP 配置目录路径
`);
}

// CLI 入口
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case "list":
    cmdList();
    break;

  case "info":
    cmdInfo(args[1]);
    break;

  case "decide":
    cmdDecide(args[1]);
    break;

  case "defaults":
    cmdDefaults(args[1]);
    break;

  case "recommend":
    cmdRecommend(args[1]);
    break;

  case "help":
  case "-h":
  case "--help":
    printHelp();
    break;

  default:
    if (command) {
      console.error(`错误: 未知命令 "${command}"`);
    }
    printHelp();
    process.exit(command ? 1 : 0);
}

// ============================================
// 参数验证
// ============================================

/**
 * 验证图片尺寸比例
 */
function validateImageSize(width, height) {
  const ratios = [
    { ratio: 1, name: "1:1" },
    { ratio: 4 / 3, name: "4:3" },
    { ratio: 3 / 4, name: "3:4" },
    { ratio: 16 / 9, name: "16:9" },
    { ratio: 9 / 16, name: "9:16" },
    { ratio: 21 / 9, name: "21:9" },
  ];

  const actual = width / height;
  const tolerance = 0.01;

  for (const { ratio, name } of ratios) {
    if (Math.abs(actual - ratio) < tolerance) {
      return { valid: true };
    }
  }

  return {
    valid: true,
    warning: `非标准比例 ${width}:${height}，可能导致变形。推荐比例：1:1, 4:3, 16:9`,
  };
}

/**
 * 意图识别：区分"图片修改"和"图生图"
 */
function classifyImageIntent(userInput, hasOriginalImage) {
  if (!hasOriginalImage) {
    return { type: "text-to-image", needsImage: false };
  }

  const editKeywords = [
    "修改",
    "改",
    "换成",
    "去掉",
    "添加",
    "替换",
    "edit",
    "change",
    "remove",
    "add",
  ];
  const styleKeywords = ["风格", "类似", "参考", "style", "like", "based on"];

  const hasEditIntent = editKeywords.some((kw) => userInput.includes(kw));
  const hasStyleIntent = styleKeywords.some((kw) => userInput.includes(kw));

  if (hasEditIntent && !hasStyleIntent) {
    return { type: "image-edit", needsImage: true };
  }

  return { type: "image-to-image", needsImage: true };
}

// 导出模块供外部使用
export {
  loadRHMCPConfig,
  loadRecommendedApps,
  decideStorageMode,
  getParamDefaults,
  mapSceneToApp,
  recommendApp,
  validateImageSize,
  classifyImageIntent,
};
