#!/usr/bin/env node
/**
 * wxmini-ci - 微信小程序 CI 工具
 * 支持：check, preview, upload, build-npm, upload-function, upload-storage, get-sourcemap
 * 
 * 使用方式：
 *   node wx-miniprogram-ci.js <command> [options]
 *   node wx-miniprogram-ci.js --help
 * 
 * 配置加载优先级（从高到低）：
 *   1. 命令行参数（--appid, --project-path 等）
 *   2. 配置文件（~/.wxmini-ci.config.js 或 --config-dir/.wxmini-ci.config.js）
 * 
 * 配置文件格式：
 *   module.exports = {
 *     projects: {
 *       'myapp': { appid: 'xxx', privateKeyPath: '...', projectPath: '...' }
 *     },
 *     setting: { es6: true, minify: true }  // 全局编译设置
 *   };
 * 
 * 使用 config 命令可以持久化配置到 ~/.wxmini-ci.config.js
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ============== 版本 ==============
const VERSION = '1.2.1';

// ============== 配置 ==============

// CLI 指定的配置目录（通过 --config-dir 设置）
let cliConfigDir = null;

// 运行时配置目录：CLI指定 > 用户主目录
function getConfigDir() {
  return cliConfigDir || os.homedir();
}

// 用户配置文件路径（~/.wxmini-ci.config.js 或 --config-dir/.wxmini-ci.config.js）
function getUserConfigFile() {
  return path.join(getConfigDir(), '.wxmini-ci.config.js');
}

// 默认输出目录（当前目录下的 wx-miniprogram-ci 子目录）
function getDefaultOutputDir() {
  return path.join(process.cwd(), 'wx-miniprogram-ci');
}

// 运行时配置对象（会被环境变量和配置文件覆盖）
let config = {
  appid: '',
  privateKeyPath: '',
  projectPath: '',
  type: 'miniProgram',
  outputDir: getDefaultOutputDir(),
  setting: {}
};

// ============== 工具函数 ==============

// 日志输出（带 emoji 前缀）
// type: info/success/error/warn
function log(msg, type = 'info') {
  const prefix = {
    info: 'ℹ️',
    success: '✅',
    error: '❌',
    warn: '⚠️'
  };
  console.log(`${prefix[type] || 'ℹ️'} ${msg}`);
}

// ============== 配置持久化函数 ==============
// 将配置写入 ~/.wxmini-ci.config.js
// 读取现有配置，合并后整体写入（简单粗暴但可靠）
function saveUserConfig(key, value) {
  let fileConfig = {};
  
  // 读取现有配置
  if (fs.existsSync(getUserConfigFile())) {
    try {
      delete require.cache[require.resolve(getUserConfigFile())];
      fileConfig = require(getUserConfigFile());
    } catch (e) {
      // 如果读取失败，忽略并使用空对象
    }
  }
  
  // 更新配置
  fileConfig[key] = value;
  
  // 确保目录存在
  const dir = path.dirname(getUserConfigFile());
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // 写入文件
  const content = `module.exports = ${JSON.stringify(fileConfig, null, 2)};\n`;
  fs.writeFileSync(getUserConfigFile(), content, 'utf-8');
  log(`配置已持久化到: ${getUserConfigFile()}`, 'success');
}

// 保存项目配置到用户配置文件
function saveProjectConfig(projectName, key, value) {
  let fileConfig = {};
  
  // 读取现有配置
  if (fs.existsSync(getUserConfigFile())) {
    try {
      delete require.cache[require.resolve(getUserConfigFile())];
      fileConfig = require(getUserConfigFile());
    } catch (e) {
      // 如果读取失败，忽略
    }
  }
  
  // 确保 projects 结构存在
  if (!fileConfig.projects) {
    fileConfig.projects = {};
  }
  if (!fileConfig.projects[projectName]) {
    fileConfig.projects[projectName] = {};
  }
  
  // 更新项目配置
  fileConfig.projects[projectName][key] = value;
  
  // 确保目录存在
  const dir = path.dirname(getUserConfigFile());
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // 写入文件
  const content = `module.exports = ${JSON.stringify(fileConfig, null, 2)};\n`;
  fs.writeFileSync(getUserConfigFile(), content, 'utf-8');
  log(`配置已持久化到: ${getUserConfigFile()}`, 'success');
}

// ============== 配置加载函数 ==============

// 1. 从环境变量加载（仅支持 WXMINI_OUTPUT_DIR）
function loadEnvConfig() {
  if (process.env.WXMINI_OUTPUT_DIR) {
    config.outputDir = process.env.WXMINI_OUTPUT_DIR;
    log('已从环境变量加载: WXMINI_OUTPUT_DIR', 'info');
  }
}

// 2. 从配置文件加载（仅一个文件）
// 配置加载后会合并到 config 对象（后者覆盖前者）
function loadConfig() {
  // 先加载环境变量（仅 WXMINI_OUTPUT_DIR）
  loadEnvConfig();
  
  // 加载配置文件（仅 ~/.wxmini-ci.config.js 或 --config-dir/.wxmini-ci.config.js）
  const configFile = getUserConfigFile();
  if (fs.existsSync(configFile)) {
    try {
      delete require.cache[require.resolve(configFile)];
      const fileConfig = require(configFile);
      config = { ...config, ...fileConfig };
      // 确保 outputDir 有默认值
      if (!config.outputDir) {
        config.outputDir = getDefaultOutputDir();
      }
      log(`已加载配置文件: ${configFile}`, 'success');
    } catch (e) {
      log(`配置文件加载失败: ${e.message}`, 'error');
    }
  }
}

// 从 projects 映射中解析最终配置
// projectName: 要使用的项目名称（从 --project 参数传入）
// 返回合并后的配置对象（全局配置 + 项目配置，项目配置优先）
function resolveProjectConfig(projectName) {
  // 必须有 projects 映射（不支持单项目顶层配置）
  if (!config.projects) {
    log('未配置任何项目，请使用 config --project <名> --set 添加项目', 'error');
    return null;
  }
  
  const projects = config.projects;
  
  // 确定要使用的项目名
  let targetProject = projectName;
  if (!targetProject) {
    // 尝试使用 default 默认项目
    if (config.default && projects[config.default]) {
      targetProject = config.default;
      log(`未指定项目，使用默认项目: ${targetProject}`, 'info');
    } else {
      log('请指定项目名: config --project <名> --get <key>', 'error');
      log(`可用项目: ${Object.keys(projects).join(', ')}`, 'info');
      if (config.default && !projects[config.default]) {
        log(`注意: 默认项目 "${config.default}" 不存在，请检查配置或使用 config --set default <名> 重设`, 'warn');
      }
      return null;
    }
  }
  
  if (!projects[targetProject]) {
    log(`未找到项目配置: ${targetProject}`, 'error');
    log(`可用项目: ${Object.keys(projects).join(', ')}`, 'info');
    return null;
  }
  
  const projectConfig = projects[targetProject];
  log(`使用项目配置: ${targetProject}`, 'info');
  
  // 合并配置：全局配置 + 项目配置（项目配置优先）
  return {
    ...config,
    ...projectConfig,
    // 保留 projects 映射（用于下次解析）
    projects: config.projects
  };
}

function checkPrivateKey(privateKeyPath) {
  if (!privateKeyPath) {
    log('私钥路径未配置', 'error');
    return false;
  }
  const fullPath = path.resolve(privateKeyPath.replace('~', os.homedir()));
  if (!fs.existsSync(fullPath)) {
    log(`私钥文件不存在: ${fullPath}`, 'error');
    return false;
  }
  return true;
}

function checkProjectPath(projectPath) {
  if (!projectPath) {
    log('项目路径未配置', 'error');
    return false;
  }
  const fullPath = path.resolve(projectPath.replace('~', os.homedir()));
  if (!fs.existsSync(fullPath)) {
    log(`项目目录不存在: ${fullPath}`, 'error');
    return false;
  }
  
  const configPath = path.join(fullPath, 'project.config.json');
  if (!fs.existsSync(configPath)) {
    log(`project.config.json 不存在: ${configPath}`, 'warn');
  }
  return true;
}

// 命令行参数解析辅助函数
// 将字符串值转换为合适的类型：true/false → 布尔，数字字符串 → 数字
function parseValue(val) {
  if (val === 'true') return true;
  if (val === 'false') return false;
  if (!isNaN(val) && val !== '') return Number(val);
  return val;
}

// 命令行参数解析
// rawArgs: process.argv.slice(2) 去掉命令名后的剩余参数
// 返回: { appid, version, set, get, project, setting, ... }
function parseArgs(rawArgs) {
  const options = {};
  const setting = {};
  
  for (let i = 0; i < rawArgs.length; i++) {
    const arg = rawArgs[i];
    
    // 处理 --setting.key value 格式
    if (arg.startsWith('--setting.')) {
      const key = arg.replace('--setting.', '');
      const value = rawArgs[i + 1];
      if (value && !value.startsWith('--')) {
        setting[key] = parseValue(value);
        i++;
      } else {
        setting[key] = true;
      }
      continue;
    }
    
    // 处理 --set key=value 或 --set key value 格式
    if (arg === '--set') {
      // 先检查是否是 key=value 格式
      const nextArg = rawArgs[i + 1];
      if (nextArg && nextArg.includes('=')) {
        // --set key=value 格式
        options['set'] = nextArg;
        i++;
      } else {
        // --set key value 格式
        const key = rawArgs[i + 1];
        const value = rawArgs[i + 2];
        if (key && value && !value.startsWith('--')) {
          options['set'] = `${key}=${value}`;
          i += 2;
        } else {
          options['set'] = true;
          i++;
        }
      }
      continue;
    }
    
    // 处理 --get key 格式（key 为空时设为空字符串，方便调用方判断）
    if (arg === '--get') {
      const key = rawArgs[i + 1];
      if (key && !key.startsWith('--')) {
        options['get'] = key;
        i++;
      } else {
        options['get'] = '';
      }
      continue;
    }
    
    // 处理 --project <name> 格式
    if (arg === '--project') {
      const name = rawArgs[i + 1];
      if (name && !name.startsWith('--')) {
        options['project'] = name;
        i++;
      }
      continue;
    }
    
    // 处理 --config-dir <path> 格式（指定配置目录）
    if (arg === '--config-dir') {
      const dir = rawArgs[i + 1];
      if (dir && !dir.startsWith('--')) {
        options['configDir'] = dir;
        cliConfigDir = dir;
        i++;
      }
      continue;
    }
    
    // 处理 --switch <name> 格式（切换默认项目）
    if (arg === '--switch') {
      const name = rawArgs[i + 1];
      if (name && !name.startsWith('--')) {
        options['switch'] = name;
        i++;
      } else {
        options['switch'] = true;
      }
      continue;
    }
    
    // 处理 --list 格式
    if (arg === '--list') {
      options['list'] = true;
      continue;
    }
    
    // 处理 --qrcode-output <path> 格式（preview 二维码输出路径）
    if (arg === '--qrcode-output') {
      const val = rawArgs[i + 1];
      if (val && !val.startsWith('--')) {
        options['qrcodeOutput'] = val;
        i++;
      } else {
        options['qrcodeOutput'] = true;
      }
      continue;
    }

    // 处理 --robot 30 格式
    if (arg.startsWith('--') && !arg.includes('.')) {
      const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const value = rawArgs[i + 1];
      if (value !== undefined && !value.startsWith('--')) {
        options[key] = parseValue(value);
        i++;
      } else {
        options[key] = true;
      }
    }
  }
  
  if (Object.keys(setting).length > 0) {
    options.setting = setting;
  }
  
  return options;
}

function getProjectObject(options) {
  return {
    appid: options.appid || config.appid,
    type: options.type || config.type,
    projectPath: (options.projectPath || config.projectPath).replace('~', os.homedir()),
    privateKeyPath: (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir())
  };
}

function validateRobot(robot) {
  const num = parseInt(robot, 10);
  if (isNaN(num) || num < 1 || num > 30) {
    log(`robot 值无效: ${robot}，应为 1-30`, 'warn');
    return false;
  }
  return true;
}

function ensureDir(dirPath) {
  const fullPath = path.resolve(dirPath.replace('~', os.homedir()));
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
    log(`已创建目录: ${fullPath}`, 'info');
  }
  return fullPath;
}

function mergeSetting(options) {
  return {
    es6: true,
    ...config.setting,
    ...(options.setting || {})
  };
}

function resolvePath(filePath) {
  if (!filePath) return '';
  return path.resolve(filePath.replace('~', os.homedir()));
}

function pushArg(args, flag, value) {
  if (value === undefined || value === null || value === false) return;
  if (value === true) {
    args.push(flag, 'true');
    return;
  }
  const normalized = typeof value === 'string' ? value : String(value);
  if (normalized === '') return;
  args.push(flag, normalized);
}

function appendSettingArgs(args, setting) {
  if (!setting || typeof setting !== 'object') return;
  const mapping = {
    es6: '--enable-es6',
    es7: '--enable-es7',
    minify: '--enable-minify',
    minifyJS: '--enable-minify-js',
    minifyWXML: '--enable-minify-wxml',
    minifyWXSS: '--enable-minify-wxss',
    codeProtect: '--enable-code-protect',
    autoPrefixWXSS: '--enable-auto-prefix-wxss'
  };
  for (const key of Object.keys(mapping)) {
    if (setting[key] !== undefined) {
      pushArg(args, mapping[key], setting[key]);
    }
  }
}

function ensureGlobalMiniprogramCi() {
  const { execSync } = require('child_process');
  try {
    execSync('miniprogram-ci --version', { stdio: 'ignore' });
    log('miniprogram-ci 已全局安装', 'success');
    return true;
  } catch (e) {
    log('miniprogram-ci 未全局安装，正在进行全局安装...', 'info');
    try {
      execSync('npm install -g miniprogram-ci', {
        stdio: 'inherit',
        shell: process.platform === 'win32'
      });
      log('miniprogram-ci 全局安装完成', 'success');
      return true;
    } catch (installError) {
      log(`全局安装失败: ${installError.message}`, 'error');
      return false;
    }
  }
}

function runGlobalMiniprogramCi(args) {
  const { spawnSync } = require('child_process');
  const result = spawnSync('miniprogram-ci', args, {
    stdio: 'inherit',
    shell: process.platform === 'win32'
  });
  if (result.error) {
    log(`调用 miniprogram-ci 失败: ${result.error.message}`, 'error');
    return false;
  }
  if (result.status !== 0) {
    log(`miniprogram-ci 返回非零状态: ${result.status}`, 'error');
    return false;
  }
  return true;
}

// ============== 命令实现 ==============
// 每个命令对应一个 async 函数，接受解析后的 options 对象

// init: 初始化环境（检查/安装全局 miniprogram-ci）
async function cmdInit(options) {
  log(`=== 环境初始化 (v${VERSION}) ===`, 'info');
  return ensureGlobalMiniprogramCi();
}

// config: 查看/修改配置（支持 --get/--set/--list/--project）
async function cmdConfig(options) {
  const projectName = options.project;
  
  // --get 不带参数时显示全局配置（而不是报错）
  if (options.get === '') {
    log('=== 全局配置 ===', 'info');
    if (config.default) {
      log(`默认项目: ${config.default}`, 'info');
    }
    if (config.projects) {
      log('可用项目:', 'info');
      for (const [name, proj] of Object.entries(config.projects)) {
        log(`  ${name}`, 'info');
        log(`    appid: ${proj.appid || '未设置'}`, 'info');
        log(`    privateKeyPath: ${proj.privateKeyPath || '未设置'}`, 'info');
        log(`    projectPath: ${proj.projectPath || '未设置'}`, 'info');
        log(`    type: ${proj.type || 'miniProgram'}`, 'info');
      }
    } else {
      log('无全局配置（可通过 config --set key=value 设置）', 'info');
    }
    log(`输出目录: ${config.outputDir || getDefaultOutputDir()}`, 'info');
    return true;
  }
  
  // 显示当前配置
  if (!options.get && !options.set && !options.list && !options.switch) {
    // 指定了项目但项目不存在 → 报错
    if (projectName && (!config.projects || !config.projects[projectName])) {
      log(`未找到项目 "${projectName}"，可用项目: ${config.projects ? Object.keys(config.projects).join(', ') : '无'}`, 'error');
      return false;
    }
    
    log('=== 当前配置 ===', 'info');
    if (config.default) {
      log(`默认项目: ${config.default}`, 'info');
    }
    if (config.projects) {
      log('可用项目:', 'info');
      for (const [name, proj] of Object.entries(config.projects)) {
        log(`  ${name}`, 'info');
        log(`    appid: ${proj.appid || '未设置'}`, 'info');
        log(`    privateKeyPath: ${proj.privateKeyPath || '未设置'}`, 'info');
        log(`    projectPath: ${proj.projectPath || '未设置'}`, 'info');
      }
    } else {
      log('暂无项目配置', 'info');
      log('用法: config --project <名> --set appid YOUR_APPID', 'info');
    }
    
    log(`输出目录: ${config.outputDir || getDefaultOutputDir()}`, 'info');
    log('', 'info');
    log('用法:', 'info');
    log('  config --list                         列出所有项目', 'info');
    log('  config --set key=value                设置全局配置（持久化）', 'info');
    log('  config --get key                      获取全局配置', 'info');
    log('  config --project <名> --set k=v       设置项目配置（持久化）', 'info');
    log('  config --project <名> --get <key>    获取项目配置', 'info');
    log('  config --switch <名>                 切换默认项目', 'info');
    log('', 'info');
    log('提示: --set 自动持久化到 ~/.wxmini-ci.config.js', 'info');
    log('提示: config --set default <名> 可设置默认项目', 'info');
    return true;
  }
  
  // 列出所有项目
  if (options.list) {
    log('=== 项目列表 ===', 'info');
    if (!config.projects || Object.keys(config.projects).length === 0) {
      log('暂无配置项目', 'info');
    } else {
      for (const [name, proj] of Object.entries(config.projects)) {
        log(`  ${name}`, 'info');
        log(`    appid: ${proj.appid || '未设置'}`, 'info');
        log(`    privateKeyPath: ${proj.privateKeyPath || '未设置'}`, 'info');
        log(`    projectPath: ${proj.projectPath || '未设置'}`, 'info');
        log(`    type: ${proj.type || 'miniProgram'}`, 'info');
      }
    }
    return true;
  }
  
  // 获取配置项
  if (options.get !== undefined) {
    const key = options.get;
    if (!key) {
      log('用法: config --get <key>', 'error');
      log('示例: config --get appid', 'info');
      return false;
    }
    
    let value;
    if (projectName) {
      // 指定了项目名，必须能匹配到
      if (!config.projects || !config.projects[projectName]) {
        log(`未找到项目 "${projectName}"，可用项目: ${config.projects ? Object.keys(config.projects).join(', ') : '无'}`, 'error');
        log('请先使用 config --project <名> --set 添加项目', 'info');
        return false;
      }
      value = config.projects[projectName][key];
      log(`[${projectName}] ${key} = ${JSON.stringify(value)}`, 'success');
    } else {
      // 从全局配置获取
      value = config[key];
      log(`${key} = ${JSON.stringify(value)}`, 'success');
    }
    return true;
  }
  
  // --set 但没有参数（如 `config --set`）
  if (options.set === true) {
    log('用法: config --set <key>=<value>', 'error');
    return false;
  }
  
  // switch 不带参数时报错
  if (options.switch === true) {
    log('用法: config --switch <项目名>', 'error');
    return false;
  }
  
  // switch <项目名> 切换默认项目
  if (options.switch) {
    const targetProject = options.switch;
    if (!config.projects || !config.projects[targetProject]) {
      log(`项目 "${targetProject}" 不存在，可用项目: ${config.projects ? Object.keys(config.projects).join(', ') : '无'}`, 'error');
      return false;
    }
    config.default = targetProject;
    saveUserConfig('default', targetProject);
    log(`已切换默认项目为: ${targetProject}`, 'success');
    return true;
  }
  
  // 设置配置项
  if (options.set && typeof options.set === 'string') {
    const setStr = options.set;
    const eqIndex = setStr.indexOf('=');
    if (eqIndex === -1) {
      log('用法: config --set <key>=<value>', 'error');
      return false;
    }
    
    let key = setStr.substring(0, eqIndex);
    const value = setStr.substring(eqIndex + 1);
    
    // 规范化配置 key：将 CLI 参数名映射为配置名
    // --private-key → privateKeyPath (miniprogram-ci 期望 privateKeyPath)
    // --project-path → projectPath
    if (key === 'privateKey') key = 'privateKeyPath';
    if (key === 'projectPath') key = 'projectPath';
    
    // 尝试解析为 JSON
    let parsedValue = value;
    try {
      parsedValue = JSON.parse(value);
    } catch {}
    
    if (projectName) {
      // 设置指定项目的配置（持久化）
      if (!config.projects) {
        config.projects = {};
      }
      if (!config.projects[projectName]) {
        config.projects[projectName] = {};
      }
      config.projects[projectName][key] = parsedValue;
      saveProjectConfig(projectName, key, parsedValue);
      // 当设置 default=true 时，同步更新顶层 default 指向
      if (key === 'default' && parsedValue === true) {
        config.default = projectName;
        saveUserConfig('default', projectName);
      }
      log(`[${projectName}] 已设置 ${key} = ${JSON.stringify(parsedValue)}`, 'success');
    } else {
      // 设置全局配置（持久化到 ~/.wxmini-ci.config.js）
      config[key] = parsedValue;
      saveUserConfig(key, parsedValue);
      if (key === 'default') {
        log(`已将 "${parsedValue}" 设为默认项目`, 'success');
      } else {
        log(`已设置 ${key} = ${JSON.stringify(parsedValue)}`, 'success');
      }
    }
    return true;
  }
  
  log('用法: config [--project <名>] [--get <key>] [--set <key>=<value>]', 'info');
  return true;
}

// check: 检查配置是否完整（appid/私钥/项目路径）
async function cmdCheck(options) {
  log(`=== 配置检查 (v${VERSION}) ===`, 'info');
  
  const projectPath = (options.projectPath || config.projectPath || '').replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath || '').replace('~', os.homedir());
  const appid = options.appid || config.appid;
  
  let allOk = true;
  
  // 检查 appid
  if (appid) {
    log(`AppID: ${appid}`, 'success');
  } else {
    log('AppID: 未配置', 'warn');
    allOk = false;
  }
  
  // 检查私钥
  if (privateKeyPath) {
    if (checkPrivateKey(privateKeyPath)) {
      log('私钥: 验证通过', 'success');
    } else {
      allOk = false;
    }
  } else {
    log('私钥: 未配置', 'warn');
    allOk = false;
  }
  
  // 检查项目目录
  if (projectPath) {
    if (checkProjectPath(projectPath)) {
      log(`项目: ${projectPath}`, 'success');
    } else {
      allOk = false;
    }
  } else {
    log('项目路径: 未配置', 'warn');
    allOk = false;
  }
  
  // 检查输出目录
  const outputDir = options.outputDir || config.outputDir || getDefaultOutputDir();
  log(`输出目录: ${outputDir}`, 'info');
  
  if (allOk) {
    log('配置检查通过', 'success');
  } else {
    log('配置检查未通过，请补充必要参数', 'error');
    log('', 'info');
    log('必要数据:', 'warn');
    log('  --appid         小程序 appid', 'warn');
    log('  --private-key   私钥文件路径', 'warn');
    log('  --project-path  项目路径', 'warn');
    log('', 'info');
    log('使用 init 命令安装依赖', 'info');
  }
  
  return allOk;
}

// preview: 预览（生成二维码，扫码在手机上看效果）
async function cmdPreview(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }

  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  const outputDir = path.resolve((options.outputDir || config.outputDir || getDefaultOutputDir()).replace('~', os.homedir()));
  const qrcodeOutput = (options.qrcodeOutput && options.qrcodeOutput !== true)
    ? resolvePath(options.qrcodeOutput)
    : path.join(outputDir, `preview-${Date.now()}.png`);
  ensureDir(path.dirname(qrcodeOutput));

  const args = ['preview'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  pushArg(args, '--desc', options.desc || `预览 ${new Date().toLocaleString()}`);
  pushArg(args, '--qrcode-format', options.qrcodeFormat || 'terminal');
  pushArg(args, '--qrcode-output-dest', qrcodeOutput);
  pushArg(args, '--page-path', options.pagePath);
  pushArg(args, '--search-query', options.searchQuery);
  pushArg(args, '--scene', options.scene || 1011);
  if (options.robot) pushArg(args, '-r', options.robot);
  appendSettingArgs(args, mergeSetting(options));

  log('=== 预览 ===');
  return runGlobalMiniprogramCi(args);
}

// upload: 上传代码（提交审核）
async function cmdUpload(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;
  const version = options.version;
  const desc = options.desc || `上传 ${new Date().toLocaleString()}`;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }
  if (!version) {
    log('缺少必要参数: version', 'error');
    return false;
  }
  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  const args = ['upload'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  pushArg(args, '--uv', version);
  pushArg(args, '--desc', desc);
  if (options.robot) pushArg(args, '-r', options.robot);
  if (options.threads) pushArg(args, '--threads', options.threads);
  appendSettingArgs(args, mergeSetting(options));

  log('=== 上传 ===');
  return runGlobalMiniprogramCi(args);
}

// build-npm: 构建 npm（将 node_modules 打包为 miniprogram_npm）
async function cmdBuildNpm(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }

  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  const args = ['pack-npm'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  if (options.ignores) pushArg(args, '--ignores', options.ignores);

  log('=== 构建 NPM ===');
  return runGlobalMiniprogramCi(args);
}

// upload-function: 上传云函数（需要 miniprogram-ci@alpha）
async function cmdUploadFunction(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;

  const env = options.env;
  const name = options.name;
  const funcPath = options.path;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }
  if (!env || !name || !funcPath) {
    log('缺少必要参数: env, name, path', 'error');
    return false;
  }

  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  const args = ['cloud', 'functions', 'upload'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  pushArg(args, '--env', env);
  pushArg(args, '--name', name);
  pushArg(args, '--path', funcPath);
  if (options.remoteNpmInstall) pushArg(args, '--remote-npm-install', options.remoteNpmInstall);

  log('⚠️ 注意: 云函数上传可能需要 miniprogram-ci@alpha 版本', 'warn');
  log('=== 上传云函数 ===');
  return runGlobalMiniprogramCi(args);
}

// upload-storage: 上传云存储（需要 miniprogram-ci@alpha）
async function cmdUploadStorage(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;

  const env = options.env;
  const storagePath = options.path;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }
  if (!env || !storagePath) {
    log('缺少必要参数: env, path', 'error');
    return false;
  }

  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  const args = ['cloud', 'uploadStorage'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  pushArg(args, '--env', env);
  pushArg(args, '--path', storagePath);
  if (options.remotePath) pushArg(args, '--remote-path', options.remotePath);

  log('⚠️ 注意: 云存储上传需要 miniprogram-ci@alpha 版本', 'warn');
  log('=== 上传云存储 ===');
  return runGlobalMiniprogramCi(args);
}

// get-sourcemap: 获取 sourceMap（用于错误定位）
async function cmdGetSourcemap(options) {
  if (!ensureGlobalMiniprogramCi()) {
    return false;
  }

  const projectPath = (options.projectPath || config.projectPath).replace('~', os.homedir());
  const privateKeyPath = (options.privateKeyPath || options.privateKey || config.privateKeyPath).replace('~', os.homedir());
  const appid = options.appid || config.appid;

  const robot = options.robot;
  const output = options.output;

  if (!appid) {
    log('缺少必要参数: appid', 'error');
    return false;
  }
  if (!robot) {
    log('缺少必要参数: robot', 'error');
    return false;
  }
  if (!output) {
    log('缺少必要参数: output', 'error');
    return false;
  }

  if (!checkPrivateKey(privateKeyPath) || !checkProjectPath(projectPath)) {
    return false;
  }

  if (!validateRobot(robot)) {
    return false;
  }

  const outputDir = resolvePath(output);
  ensureDir(outputDir);

  const args = ['get-dev-source-map'];
  pushArg(args, '--pp', projectPath);
  pushArg(args, '--pkp', privateKeyPath);
  pushArg(args, '--appid', appid);
  pushArg(args, '--type', options.type || config.type);
  pushArg(args, '-r', robot);
  pushArg(args, '--source-map-save-path', outputDir);

  log('=== 获取 SourceMap ===');
  return runGlobalMiniprogramCi(args);
}

// ============== 主程序 ==============

function printHelp() {
  console.log(`
wxmini-ci v${VERSION} - 微信小程序 CI 工具
=====================================

使用方法:
  node wx-miniprogram-ci.js <command> [options]

命令:
  init            初始化环境（检查/安装全局 miniprogram-ci）
  config          查看/修改配置
  check           检查配置是否完整
  preview         预览（生成二维码）
  upload          上传代码
  build-npm       构建 npm
  upload-function 上传云函数
  upload-storage  上传云存储
  get-sourcemap   获取 SourceMap

全局选项:
  --config-dir     指定配置目录（默认 ~/.wxmini-ci.config.js）
  --project        从配置文件 projects 映射中选择项目
  --appid          小程序 appid
  --private-key    私钥文件路径
  --project-path   项目路径
  --type           项目类型 (miniProgram/miniGame/miniProgramPlugin/miniGamePlugin)
  --output-dir     输出目录 (默认: ./wx-miniprogram-ci)

preview 特有选项:
  --desc             描述
  --qrcode-format    二维码格式: terminal/base64/image (默认 terminal)
  --qrcode-output    二维码输出路径 (默认 {output-dir}/preview-{timestamp}.png)
  --page-path        预览页面路径
  --search-query     启动参数
  --scene            场景值 (默认 1011)
  --robot            CI 机器人 1-30

upload 特有选项:
  --version          版本号 (必填)
  --desc             描述
  --robot            CI 机器人 1-30
  --threads          编译线程数
  --setting.<key>    编译设置 (如 --setting.es6 true --setting.minify true)

build-npm 特有选项:
  --ignores          排除规则

upload-function 特有选项:
  --env              云环境 ID (必填)
  --name             云函数名称 (必填)
  --path             云函数目录 (必填)
  --remote-npm-install  云端安装依赖

upload-storage 特有选项:
  --env              云环境 ID (必填)
  --path             本地目录 (必填)
  --remote-path       远端路径

get-sourcemap 特有选项:
  --robot            CI 机器人 (必填)
  --output           输出路径 (必填)

配置文件:
  配置文件路径: ~/.wxmini-ci.config.js（可通过 --config-dir 指定其他目录）
  格式: 使用 projects 映射配置（不支持单项目顶层简化写法）
  config --set 会自动持久化到 ~/.wxmini-ci.config.js

示例:
  # 检查环境
  node wx-miniprogram-ci.js check --appid wx7xxx --private-key ./key.pem --project-path ./

  # 预览
  node wx-miniprogram-ci.js preview --appid wx7xxx --project-path ./ -v 1.0.0

  # 上传
  node wx-miniprogram-ci.js upload --appid wx7xxx --project-path ./ -v 1.0.1 --desc "修复bug"

  # 自定义输出目录
  node wx-miniprogram-ci.js preview --appid wx7xxx --project-path ./ --output-dir ~/my-wxmini-output

  # 使用多项目配置
  node wx-miniprogram-ci.js upload --project my-app --version 1.0.0
  `);
}

// 主入口：解析参数 → 加载配置 → 执行命令
async function main() {
  const args = process.argv.slice(2);
  
  // 无参数或 --help 时打印帮助信息
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    return;
  }
  
  const command = args[0];
  
  // 在解析参数之前先检查是否传入 --config-dir，确保 config 文件加载时可正确使用自定义目录
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config-dir' && args[i + 1] && !args[i + 1].startsWith('--')) {
      cliConfigDir = args[i + 1];
      break;
    }
  }
  
  // 1. 加载配置（环境变量 → 配置文件）
  loadConfig();
  
  // 2. 解析命令行选项
  const options = parseArgs(args.slice(1));
  
  // 3. 如果指定了 --project，从 projects 映射中解析配置（项目配置覆盖全局配置）
  // 如果未指定 --project 但有默认项目，也使用默认项目
  // 注意：config 命令跳过自动解析，因为 config --project --set 允许创建不存在的新项目
  if (command !== 'config') {
    const targetProject = options.project || (config.default && config.projects && config.projects[config.default] ? config.default : null);
    if (targetProject && config.projects) {
      const resolved = resolveProjectConfig(targetProject);
      if (!resolved) {
        process.exit(1);
      }
      // 将解析后的配置合并到全局 config（后续命令直接使用 config.xxx）
      Object.assign(config, resolved);
    }
  }
  
  let result = false;
  
  switch (command) {
    case 'init':
      result = await cmdInit(options);
      break;
    case 'config':
      result = await cmdConfig(options);
      break;
    case 'check':
      result = await cmdCheck(options);
      break;
    case 'preview':
      result = await cmdPreview(options);
      break;
    case 'upload':
      result = await cmdUpload(options);
      break;
    case 'build-npm':
      result = await cmdBuildNpm(options);
      break;
    case 'upload-function':
      result = await cmdUploadFunction(options);
      break;
    case 'upload-storage':
      result = await cmdUploadStorage(options);
      break;
    case 'get-sourcemap':
      result = await cmdGetSourcemap(options);
      break;
    default:
      log(`未知命令: ${command}`, 'error');
      printHelp();
  }
  
  process.exit(result ? 0 : 1);
}

main().catch(e => {
  log(`错误: ${e.message}`, 'error');
  process.exit(1);
});
