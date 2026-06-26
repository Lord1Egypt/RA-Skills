#!/usr/bin/env node
/**
 * openclaw mg - Multi-gateway Configuration Wizard (完整版)
 * 多网关配置向导 - 完整复制 main 配置 + 自动飞书配置引导
 */

const readline = require('readline');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

const log = {
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✅${colors.reset} ${msg}`),
  warn: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}❌${colors.reset} ${msg}`),
  step: (msg) => console.log(`\n${colors.cyan}━━━ ${msg} ━━━${colors.reset}\n`)
};

const API_KEY = 'sk-sp-319b5ed947404131b3b12e5211592b46';

// ========== 日志文件 ==========
let logFile = null;

function setupLogging(gatewayName) {
  const { execSync } = require('child_process');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  logFile = `/tmp/openclaw-mg-${gatewayName}-${timestamp}.log`;
  console.log(`📝 操作日志：${logFile}\n`);
  return logFile;
}

function logToFile(msg) {
  if (logFile) {
    try {
      const { execSync } = require('child_process');
      execSync(`echo "[${new Date().toISOString()}] ${msg}" >> ${logFile} 2>/dev/null || true`);
    } catch (e) {}
  }
}

// ========== 前置检查 ==========
function checkPrerequisites(baseDir) {
  console.log(`${colors.cyan}🔍 检查前置条件...${colors.reset}\n`);
  
  // 检查必要文件
  const requiredFiles = [
    { path: path.join(baseDir, 'openclaw-main.json'), name: 'main 配置文件' }
  ];
  
  for (const { path: filePath, name } of requiredFiles) {
    if (!fs.existsSync(filePath)) {
      log.error(`缺少必要文件：${name}`);
      console.log(`  路径：${filePath}`);
      return false;
    }
    log.success(`${name} 存在`);
  }
  
  // 检查必要目录
  const requiredDirs = [
    path.join(baseDir, 'agents'),
    path.join(baseDir, 'agents', 'main', 'agent') // main 的 agent 目录必须存在
  ];
  
  for (const dir of requiredDirs) {
    if (!fs.existsSync(dir)) {
      log.error(`缺少必要目录：${dir}`);
      return false;
    }
  }
  log.success('必要目录存在');
  
  // 检测存在的 workspace
  const possibleWorkspaces = [];
  try {
    const dirs = fs.readdirSync(baseDir);
    for (const dir of dirs) {
      if (dir.startsWith('workspace-') && dir !== 'workspace') {
        possibleWorkspaces.push(dir);
      }
    }
  } catch (e) {
    log.error(`读取目录失败：${e.message}`);
    return false;
  }
  
  if (possibleWorkspaces.length === 0) {
    log.error('没有找到任何 workspace');
    return false;
  }
  
  log.success(`检测到存在的 workspace: ${possibleWorkspaces.join(', ')}`);
  
  // 检查是否有 models.json 模板（只检查 main）
  let hasModels = false;
  
  const mainAgentSubDir = path.join(baseDir, 'agents', 'main', 'agent');
  const mainDir = path.join(baseDir, 'agents', 'main');
  
  // 搜索路径：main/agent 和 main
  const searchPaths = [
    { path: path.join(mainAgentSubDir, 'models.json'), name: 'main/agent/models.json' },
    { path: path.join(mainDir, 'models.json'), name: 'main/models.json' }
  ];
  
  for (const { path: modelsPath, name } of searchPaths) {
    if (fs.existsSync(modelsPath)) {
      log.success(`${name} 存在（将使用作为模板）`);
      hasModels = true;
      break;
    }
  }
  
  if (!hasModels) {
    log.error('找不到 models.json 模板');
    log.error('搜索路径:');
    searchPaths.forEach(({ path: p, name }) => {
      log.error(`  - ${name}: ${p}`);
    });
    return false;
  }
  
  console.log('');
  return true;
}

// ========== 配置备份 ==========
function backupConfig(configPath) {
  if (fs.existsSync(configPath)) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = `${configPath}.backup.${timestamp}`;
    fs.copyFileSync(configPath, backupPath);
    log.warn(`已备份旧配置：${backupPath}`);
    return backupPath;
  }
  return null;
}

// ========== 改进的 IP 获取 ==========
function getServerIP() {
  const { execSync } = require('child_process');
  
  const sources = [
    'curl -s ifconfig.me',
    'curl -s api.ipify.org',
    'curl -s icanhazip.com',
    'hostname -I 2>/dev/null | awk \'{print $1}\'',
    'hostname 2>/dev/null'
  ];
  
  for (const cmd of sources) {
    try {
      const ip = execSync(cmd, { encoding: 'utf8', timeout: 5000 }).trim();
      if (ip && ip.length > 0 && !ip.includes('error')) {
        return ip;
      }
    } catch (e) {
      // 尝试下一个源
    }
  }
  
  return 'YOUR_SERVER_IP';
}

// ========== 回滚机制 ==========
let createdResources = {
  configPath: null,
  agentDir: null,
  workspaceDir: null,
  serviceFile: null
};

function rollback() {
  console.log(`\n${colors.yellow}⚠️  创建失败，正在回滚...${colors.reset}`);
  
  try {
    if (createdResources.serviceFile && fs.existsSync(createdResources.serviceFile)) {
      execSync(`systemctl --user stop ${path.basename(createdResources.serviceFile, '.service')} 2>/dev/null || true`);
      execSync(`systemctl --user disable ${path.basename(createdResources.serviceFile, '.service')} 2>/dev/null || true`);
      fs.unlinkSync(createdResources.serviceFile);
      log.info(`已删除服务文件：${createdResources.serviceFile}`);
    }
    
    if (createdResources.workspaceDir && fs.existsSync(createdResources.workspaceDir)) {
      execSync(`rm -rf ${createdResources.workspaceDir}`);
      log.info(`已删除 workspace: ${createdResources.workspaceDir}`);
    }
    
    if (createdResources.agentDir && fs.existsSync(createdResources.agentDir)) {
      execSync(`rm -rf ${createdResources.agentDir}`);
      log.info(`已删除 agent 目录：${createdResources.agentDir}`);
    }
    
    if (createdResources.configPath && fs.existsSync(createdResources.configPath)) {
      fs.unlinkSync(createdResources.configPath);
      log.info(`已删除配置文件：${createdResources.configPath}`);
    }
    
    log.success('回滚完成');
  } catch (e) {
    log.error(`回滚失败：${e.message}`);
    log.error('请手动清理残留文件');
  }
}

// 设置错误处理
process.on('uncaughtException', (err) => {
  log.error(`未捕获的错误：${err.message}`);
  if (createdResources.configPath) {
    rollback();
  }
  process.exit(1);
});

// ========== 端口检测函数 ==========
function getOccupiedPorts() {
  const { execSync } = require('child_process');
  const occupied = [];
  
  try {
    // 从 systemd 服务获取
    const services = execSync('systemctl --user list-units 2>/dev/null | grep "openclaw-gateway.*\\.service" | awk \'{print $1}\'', { encoding: 'utf8' });
    const serviceList = services.trim().split('\n').filter(s => s.trim());
    
    for (const service of serviceList) {
      try {
        // 获取完整的环境变量行
        const envLine = execSync(`systemctl --user show ${service.trim()} 2>/dev/null | grep "OPENCLAW_CONFIG_PATH="`, { encoding: 'utf8' }).trim();
        // 从环境变量行中提取配置路径
        const match = envLine.match(/OPENCLAW_CONFIG_PATH=([^\s]+)/);
        const configPath = match ? match[1] : null;
        
        if (configPath && fs.existsSync(configPath)) {
          const config = fs.readFileSync(configPath, 'utf8');
          const portMatch = config.match(/"port":\s*(\d+)/);
          if (portMatch) {
            occupied.push({ port: portMatch[1], service: service.trim() });
          }
        }
      } catch (e) {
        // 忽略单个服务的错误
      }
    }
  } catch (e) {
    // 忽略 systemd 错误
  }
  
  return occupied;
}

function suggestAvailablePort(startPort = 19900, endPort = 29999) {
  const { execSync } = require('child_process');
  
  for (let port = startPort; port <= endPort; port++) {
    try {
      // 检查端口是否被监听
      const netstat = execSync(`ss -tlnp 2>/dev/null | grep ":${port} " || netstat -tlnp 2>/dev/null | grep ":${port} " || true`, { encoding: 'utf8' });
      const isListening = netstat.trim().length > 0;
      
      // 检查配置文件是否使用该端口
      const configCheck = execSync(`grep -r "\"port": ${port}" ~/.openclaw/openclaw-*.json 2>/dev/null | grep -v "openclaw.json" || true`, { encoding: 'utf8' });
      const isConfigured = configCheck.trim().length > 0;
      
      if (!isListening && !isConfigured) {
        return port;
      }
    } catch (e) {
      // 如果检查失败，假设端口可用
      return port;
    }
  }
  
  return endPort + 1;
}

async function main() {
  console.log(`
${colors.cyan}╔══════════════════════════════════════════════════════════╗
║     OpenClaw Multi-Gateway Wizard - 多网关配置向导        ║
║                  (完整配置版)                             ║
╚══════════════════════════════════════════════════════════╝${colors.reset}
  `);

  try {
    const baseDir = path.join(process.env.HOME, '.openclaw');
    
    // ========== 前置检查 ==========
    if (!checkPrerequisites(baseDir)) {
      log.error('前置检查失败，请修复后重试');
      process.exit(1);
    }
    
    // ========== 步骤 1: 配置网关信息 ==========
    log.step('步骤 1/11: 配置网关信息');
    
    // 显示已占用端口
    console.log(`${colors.cyan}📊 当前已占用的网关端口：${colors.reset}`);
    const occupied = getOccupiedPorts();
    if (occupied.length > 0) {
      occupied.forEach(({ port, service }) => {
        console.log(`  ${colors.green}✓${colors.reset} 端口 ${port} - ${service}`);
      });
    } else {
      console.log('  暂无已占用的网关端口');
    }
    console.log('');
    
    const gatewayName = await question('网关名称：') || 'agent-a';
    const gatewayDesc = await question(`网关描述/用途 [${gatewayName} 机器人]: `) || `${gatewayName} 机器人`;
    
    // 随机推荐可用端口
    const suggestedPort = suggestAvailablePort(19900, 19999);
    
    console.log(`${colors.green}✅ 推荐端口：${suggestedPort}${colors.reset}`);
    console.log('');
    
    const gatewayPort = await question(`网关端口 [${suggestedPort}]: `) || suggestedPort;
    
    const workspaceName = `workspace-${gatewayName}`;
    const configPath = path.join(baseDir, `openclaw-${gatewayName}.json`);
    const agentDir = path.join(baseDir, 'agents', gatewayName);
    const workspaceDir = path.join(baseDir, workspaceName);
    
    console.log(`\n${colors.yellow}配置摘要:${colors.reset}`);
    console.log(`  网关名称：  ${gatewayName}`);
    console.log(`  用途描述：  ${gatewayDesc}`);
    console.log(`  监听端口：  ${gatewayPort}`);
    console.log(`  Workspace:  ${workspaceName}`);
    console.log(`  配置文件：  ${configPath}`);
    
    const confirm = await question(`\n确认配置？[Y/n]: `);
    if (confirm.toLowerCase() === 'n') {
      log.info('已取消');
      process.exit(0);
    }
    
    // 设置日志
    setupLogging(gatewayName);
    logToFile(`开始创建网关：${gatewayName}, 端口：${gatewayPort}`);
    
    // 备份旧配置（如果存在）
    backupConfig(configPath);
    
    // ========== 步骤 2: 选择并复制配置 ==========
    log.step('步骤 2/11: 选择配置来源');
    
    // 动态检测存在的配置文件
    const possibleConfigs = [];
    const configPattern = /^openclaw-(.+)\.json$/;
    
    try {
      const files = fs.readdirSync(baseDir);
      for (const file of files) {
        const match = file.match(configPattern);
        if (match && file !== 'openclaw.json') {
          const name = match[1];
          possibleConfigs.push({
            name: name,
            path: path.join(baseDir, file),
            label: file
          });
        }
      }
    } catch (e) {
      log.error(`读取配置目录失败：${e.message}`);
      process.exit(1);
    }
    
    const existingConfigs = possibleConfigs;
    
    if (existingConfigs.length === 0) {
      log.error('没有找到任何配置文件');
      process.exit(1);
    }
    
    // 如果只有一个配置，直接使用
    let sourceConfig;
    if (existingConfigs.length === 1) {
      sourceConfig = existingConfigs[0];
      log.info(`检测到唯一配置：${sourceConfig.label}`);
    } else {
      // 多个配置，让用户选择
      console.log('\n检测到以下配置文件：');
      existingConfigs.forEach((cfg, index) => {
        console.log(`  ${index + 1}) ${cfg.label}`);
      });
      
      const choice = await question(`\n请选择配置来源 [1-${existingConfigs.length}]: `);
      const choiceIndex = parseInt(choice) - 1;
      if (choiceIndex < 0 || choiceIndex >= existingConfigs.length) {
        log.error('无效选择');
        process.exit(1);
      }
      sourceConfig = existingConfigs[choiceIndex];
    }
    
    console.log(`\n  来源配置：${sourceConfig.label}`);
    
    // 备份原配置（如果已存在）
    if (fs.existsSync(configPath)) {
      fs.copyFileSync(configPath, `${configPath}.bak`);
      log.info('已备份原配置');
    }
    
    // 复制配置
    const sourceLines = fs.readFileSync(sourceConfig.path, 'utf8').split('\n').length;
    fs.copyFileSync(sourceConfig.path, configPath);
    const newLines = fs.readFileSync(configPath, 'utf8').split('\n').length;
    
    console.log(`  ${sourceConfig.name} 配置：${sourceLines} 行`);
    console.log(`  ${gatewayName} 配置：${newLines} 行`);
    
    if (newLines < sourceLines) {
      log.error(`配置不完整！${sourceConfig.name} 有 ${sourceLines} 行，但新配置只有 ${newLines} 行`);
      // 回滚备份
      if (fs.existsSync(`${configPath}.bak`)) {
        fs.copyFileSync(`${configPath}.bak`, configPath);
        log.info('已恢复原配置');
      }
      process.exit(1);
    }
    
    // 验证配置有效性
    try {
      JSON.parse(fs.readFileSync(configPath, 'utf8'));
      log.success('配置文件验证通过');
    } catch (e) {
      log.error(`配置文件无效：${e.message}`);
      // 回滚备份
      if (fs.existsSync(`${configPath}.bak`)) {
        fs.copyFileSync(`${configPath}.bak`, configPath);
        log.info('已恢复原配置');
      }
      process.exit(1);
    }
    
    log.success(`已完整复制 ${sourceConfig.name} 配置（${newLines} 行）`);
    
    // 保存配置来源，后续步骤使用（技能/记忆同步）
    global.sourceAgentName = sourceConfig.name;
    
    // 预计算 workspace 路径，后续步骤复用
    const srcWorkspace = path.join(baseDir, `workspace-${sourceConfig.name}`);
    
    // ========== 步骤 3: 替换关键配置项 ==========
    log.step('步骤 3/11: 替换关键配置');
    
    let configContent = fs.readFileSync(configPath, 'utf8');
    
    // 替换 workspace（完整路径）- 动态检测源配置
    const oldWorkspaceMatch = configContent.match(/"workspace":\s*"([^"]+)"/);
    const oldWorkspace = oldWorkspaceMatch ? oldWorkspaceMatch[1] : 'xxx';
    configContent = configContent.replace(
      /"workspace":\s*"[^"]+"/g,
      `"workspace": "/home/admin/.openclaw/workspace-${gatewayName}"`
    );
    console.log(`  ✓ workspace: ${oldWorkspace} → workspace-${gatewayName}`);
    
    // 替换端口 - 动态检测源配置
    const oldPortMatch = configContent.match(/"port":\s*(\d+)/);
    const oldPort = oldPortMatch ? oldPortMatch[1] : 'xxx';
    configContent = configContent.replace(/"port":\s*\d+/g, `"port": ${gatewayPort}`);
    console.log(`  ✓ 端口：${oldPort} → ${gatewayPort}`);
    
    // 替换 UI basePath - 动态检测源配置
    const oldBasePathMatch = configContent.match(/"basePath":\s*"([^"]+)"/);
    const oldBasePath = oldBasePathMatch ? oldBasePathMatch[1] : 'xxx-ui';
    configContent = configContent.replace(/"basePath":\s*"[^"]+"/g, `"basePath": "${gatewayName}-ui"`);
    console.log(`  ✓ UI basePath: ${oldBasePath} → ${gatewayName}-ui`);
    
    // 替换 token - 动态检测源配置
    const oldTokenMatch = configContent.match(/"token":\s*"([^"]+)"/);
    const oldToken = oldTokenMatch ? oldTokenMatch[1] : 'xxx-token';
    const token = `${gatewayName}-token-${gatewayDesc}-${gatewayPort}`;
    configContent = configContent.replace(/"token":\s*"[^"]+"/g, `"token": "${token}"`);
    console.log(`  ✓ Token: ${oldToken} → ${token}`);
    
    // 替换 allowedOrigins - 动态检测源配置
    const serverIp = getServerIP();
    const oldAllowedOriginsMatch = configContent.match(/"allowedOrigins":\s*\[([^\]]+)\]/);
    const oldAllowedOrigins = oldAllowedOriginsMatch ? oldAllowedOriginsMatch[0] : '"allowedOrigins": ["xxx"]';
    configContent = configContent.replace(
      /"allowedOrigins":\s*\[[^\]]+\]/g,
      `"allowedOrigins": ["http://${serverIp}:${gatewayPort}"]`
    );
    console.log(`  ✓ allowedOrigins: 已更新`);
    logToFile(`服务器 IP: ${serverIp}`);
    
    fs.writeFileSync(configPath, configContent);
    log.success('关键配置已替换');
    
    // ========== 步骤 3.1: 添加/替换 agents.list ==========
    log.step('步骤 3.1/11: 配置 agents.list');
    
    configContent = fs.readFileSync(configPath, 'utf8');
    
    // 检查是否已有 agents.list
    if (configContent.includes('"list": [')) {
      // 已有 list，替换其中的配置
      configContent = configContent.replace(
        /"id":\s*"[^"]+",/g,
        `"id": "${gatewayName}",`
      );
      configContent = configContent.replace(
        /"name":\s*"[^"]*",\n\s*"agentDir":/g,
        `"name": "${gatewayDesc}",\n        "agentDir":`
      );
      configContent = configContent.replace(
        /"agentDir":\s*"[^"]+"/g,
        `"agentDir": "/home/admin/.openclaw/agents/${gatewayName}"`
      );
      configContent = configContent.replace(
        /"workspace":\s*"[^"]+",\n\s*\}/g,
        `"workspace": "/home/admin/.openclaw/workspace-${gatewayName}",\n      }`
      );
      console.log(`  ✓ agents.list: 已更新 (${gatewayName})`);
    } else {
      // 没有 list，使用模板添加
      const agentsListTemplate = `"agents": {\n    "list": [\n      {\n        "id": "${gatewayName}",\n        "name": "${gatewayDesc}",\n        "agentDir": "/home/admin/.openclaw/agents/${gatewayName}",\n        "workspace": "/home/admin/.openclaw/workspace-${gatewayName}"\n      }\n    ],\n    "defaults":`;
      
      configContent = configContent.replace(
        /"agents":\s*{\s*"defaults":/,
        agentsListTemplate
      );
      console.log(`  ✓ agents.list: 已添加 (${gatewayName})`);
    }
    
    fs.writeFileSync(configPath, configContent);
    log.success('agents.list 配置完成');
    
    // ========== 步骤 3.2: 全面检查并替换所有名称 ==========
    log.step('步骤 3.2/11: 全面检查并替换名称');
    
    configContent = fs.readFileSync(configPath, 'utf8');
    let modified = false;
    
    // 替换所有可能的 agent 名称引用
    const replacements = [
      // 替换 agent ID
      { pattern: /"id":\s*"[^"]+"/g, replacement: `"id": "${gatewayName}"`, desc: 'agent ID' },
      // 替换 agent 名称
      { pattern: /"name":\s*"[^"]+"/g, replacement: `"name": "${gatewayDesc}"`, desc: 'agent 名称' },
      // 替换 agentDir
      { pattern: /"agentDir":\s*"[^"]+"/g, replacement: `"agentDir": "/home/admin/.openclaw/agents/${gatewayName}"`, desc: 'agentDir' },
      // 替换 workspace
      { pattern: /"workspace":\s*"[^"]+"/g, replacement: `"workspace": "/home/admin/.openclaw/workspace-${gatewayName}"`, desc: 'workspace' },
      // 替换 UI basePath
      { pattern: /"basePath":\s*"[^"]+"/g, replacement: `"basePath": "${gatewayName}-ui"`, desc: 'UI basePath' },
      // 替换 token 中的名称
      { pattern: /"token":\s*"[^"]+"/g, replacement: `"token": "${gatewayName}-token-${gatewayDesc}-${gatewayPort}"`, desc: 'token' },
    ];
    
    for (const { pattern, replacement, desc } of replacements) {
      const matches = configContent.match(pattern);
      if (matches && matches.length > 0) {
        configContent = configContent.replace(pattern, replacement);
        console.log(`  ✓ 已替换 ${desc}: ${matches.length} 处`);
        modified = true;
      }
    }
    
    if (!modified) {
      console.log(`  ✓ 所有名称已正确配置`);
    }
    
    fs.writeFileSync(configPath, configContent);
    log.success('名称检查完成');
    
    // ========== 步骤 3.5: 飞书配置修改提示 ==========
    console.log(`\n${colors.yellow}⚠️  飞书应用配置确认${colors.reset}`);
    console.log(`${colors.gray}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log('当前配置复制了 main 的飞书应用，需要确认：\n');
    console.log('  1) 使用新的飞书应用（推荐，每个网关独立）');
    console.log('  2) 使用和 main 相同的应用（共用应用）');
    console.log('  3) 跳过飞书配置（不绑定任何渠道，纯本地使用）\n');
    
    const feishuChoice = await question('请选择 [1/2/3]: ');
    if (feishuChoice === '1') {
      console.log('\n请在飞书开发者后台创建新应用，然后输入配置:');
      const newAppId = await question('新 App ID (cli_xxx): ');
      const newAppSecret = await question('新 App Secret: ');
      
      if (newAppId && newAppSecret) {
        // 重新读取并修改配置
        configContent = fs.readFileSync(configPath, 'utf8');
        configContent = configContent.replace(/"appId":\s*"[^"]*"/, `"appId": "${newAppId}"`);
        configContent = configContent.replace(/"appSecret":\s*"[^"]*"/, `"appSecret": "${newAppSecret}"`);
        fs.writeFileSync(configPath, configContent);
        log.success(`已更新飞书配置：${newAppId}`);
      }
    } else if (feishuChoice === '2') {
      log.info('使用和 main 相同的飞书应用');
    } else if (feishuChoice === '3') {
      log.info('跳过飞书配置 - 网关将不绑定任何渠道（纯本地使用）');
      log.info('后续如需绑定渠道，可手动修改配置文件或运行 openclaw channels login');
      // 标记跳过后续飞书配置步骤
      global.skipFeishuConfig = true;
    }
    
    // ========== 步骤 4: 复制 agents 配置（包含 API Key） ==========
    log.step('步骤 4/11: 复制 agents 配置');
    
    // 动态检测存在的 agent 目录
    const possibleAgents = [];
    try {
      const agentDirs = fs.readdirSync(path.join(baseDir, 'agents'));
      for (const dir of agentDirs) {
        const agentDir = path.join(baseDir, 'agents', dir);
        const agentSubDir = path.join(agentDir, 'agent');
        if (fs.existsSync(agentSubDir) || fs.existsSync(agentDir)) {
          possibleAgents.push(dir);
        }
      }
    } catch (e) {
      log.error(`读取 agent 目录失败：${e.message}`);
      process.exit(1);
    }
    
    log.info(`检测到存在的 agent: ${possibleAgents.length > 0 ? possibleAgents.join(', ') : '无'}`);
    
    // 构建搜索路径列表（动态）
    const searchDirs = [];
    for (const agent of possibleAgents) {
      const agentSubDir = path.join(baseDir, 'agents', agent, 'agent');
      const agentDir = path.join(baseDir, 'agents', agent);
      if (fs.existsSync(agentSubDir)) searchDirs.push({ path: agentSubDir, name: `${agent}/agent` });
      if (fs.existsSync(agentDir)) searchDirs.push({ path: agentDir, name: agent });
    }
    
    // 如果没有检测到任何 agent，使用 main 作为后备
    if (searchDirs.length === 0) {
      const mainAgentSubDir = path.join(baseDir, 'agents', 'main', 'agent');
      const mainDir = path.join(baseDir, 'agents', 'main');
      if (fs.existsSync(mainAgentSubDir)) searchDirs.push({ path: mainAgentSubDir, name: 'main/agent' });
      if (fs.existsSync(mainDir)) searchDirs.push({ path: mainDir, name: 'main' });
    }
    
    if (!fs.existsSync(agentDir)) fs.mkdirSync(agentDir, { recursive: true });
    if (!fs.existsSync(path.join(agentDir, 'agent'))) fs.mkdirSync(path.join(agentDir, 'agent'), { recursive: true });
    
    // ========== 复制 agent 子目录内容 ==========
    // 使用动态检测的目录列表
    const dstAgentSubDir = path.join(agentDir, 'agent');
    let agentFilesCopied = false;
    
    // 按优先级尝试从检测到的目录复制
    for (const { path: srcDir, name } of searchDirs) {
      if (agentFilesCopied) break;
      
      try {
        const files = fs.readdirSync(srcDir);
        if (files.length > 0) {
          files.forEach(file => {
            const src = path.join(srcDir, file);
            const dst = path.join(dstAgentSubDir, file);
            if (fs.statSync(src).isFile() && file !== 'models.json') {
              fs.copyFileSync(src, dst);
            }
          });
          log.success(`已复制 agent 配置（从 ${name}）`);
          agentFilesCopied = true;
        }
      } catch (e) {
        log.warn(`从 ${name} 复制失败：${e.message}`);
      }
    }
    
    if (!agentFilesCopied) {
      log.error('没有找到可复制的 agent 配置');
      process.exit(1);
    }
    
    // ========== 复制 models.json（动态搜索） ==========
    const dstModels = path.join(agentDir, 'models.json');
    let modelsCopied = false;
    
    // 使用动态检测的目录列表搜索 models.json
    for (const { path: srcDir, name } of searchDirs) {
      const modelsPath = path.join(srcDir, 'models.json');
      if (fs.existsSync(modelsPath)) {
        let modelsContent = fs.readFileSync(modelsPath, 'utf8');
        modelsContent = modelsContent.replace(/\$api-key/g, API_KEY);
        fs.writeFileSync(dstModels, modelsContent);
        log.success(`已复制 models.json (从 ${name}, API Key 已修复)`);
        modelsCopied = true;
        break;
      }
    }
    
    if (!modelsCopied) {
      log.error('无法复制 models.json（所有搜索路径都没有）');
      log.error('搜索路径:');
      searchPaths.forEach(({ path: p, name }) => {
        log.error(`  - ${name}: ${p}`);
      });
      process.exit(1);
    }
    
    // ========== 步骤 5: 创建目录结构 ==========
    log.step('步骤 5/11: 创建目录结构');
    
    const dirsToCreate = [
      path.join(workspaceDir, 'memory'),
      path.join(workspaceDir, 'skills'),
      path.join(agentDir, 'sessions')
    ];
    
    dirsToCreate.forEach(dir => {
      try {
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
          log.success(`创建目录：${dir}`);
        } else {
          log.info(`目录已存在：${dir}`);
        }
      } catch (e) {
        log.error(`创建目录失败：${dir} - ${e.message}`);
        process.exit(1);
      }
    });
    
    // 从选择的配置来源复制基础文件
    ['AGENTS.md', 'SOUL.md', 'TOOLS.md'].forEach(file => {
      const src = path.join(srcWorkspace, file);
      const dst = path.join(workspaceDir, file);
      if (fs.existsSync(src)) {
        try {
          fs.copyFileSync(src, dst);
          log.success(`复制文件：${file} (从 ${global.sourceAgentName})`);
        } catch (e) {
          log.warn(`复制 ${file} 失败：${e.message}`);
        }
      }
    });
    
    log.success('目录结构已创建');
    
    // ========== 步骤 6: 选择是否复制技能 ==========
    log.step('步骤 6/11: 选择技能同步');
    
    const srcSkillsDir = path.join(baseDir, `workspace-${global.sourceAgentName || 'main'}`, 'skills');
    const dstSkills = path.join(workspaceDir, 'skills');
    
    // 列出可用技能
    const availableSkills = [];
    if (fs.existsSync(srcSkillsDir)) {
      fs.readdirSync(srcSkillsDir).forEach(skill => {
        const src = path.join(srcSkillsDir, skill);
        if (fs.statSync(src).isDirectory()) {
          availableSkills.push(skill);
        }
      });
    }
    
    console.log(`发现 ${availableSkills.length} 个可用技能（从 ${global.sourceAgentName}）：\n`);
    availableSkills.forEach((skill, i) => {
      console.log(`  [${String(i+1).padStart(2)}] ${skill}`);
    });
    console.log(`  [ a] 全选`);
    console.log(`  [ n] 不复制（全新开始）`);
    console.log(`  [ b] 只复制基础技能 (self-improving-agent, proactive-agent)`);
    console.log('\n提示：输入多个数字用逗号分隔，如：1,3,5');
    
    const skillInput = await question('\n请选择要同步的技能：') || 'b';
    
    if (!fs.existsSync(dstSkills)) fs.mkdirSync(dstSkills, { recursive: true });
    
    let skillsToCopy = [];
    
    if (skillInput.toLowerCase() === 'n') {
      console.log('  选择：不复制技能（全新开始）');
      log.success('技能目录已创建，可以后续手动添加');
    } else if (skillInput.toLowerCase() === 'a') {
      console.log('  选择：完整复制所有技能');
      skillsToCopy = availableSkills;
    } else if (skillInput.toLowerCase() === 'b') {
      console.log('  选择：只复制基础技能');
      skillsToCopy = ['self-improving-agent', 'proactive-agent'].filter(s => availableSkills.includes(s));
    } else {
      // 解析选择的数字
      const indices = skillInput.split(',').map(s => parseInt(s.trim()) - 1).filter(n => !isNaN(n) && n >= 0 && n < availableSkills.length);
      skillsToCopy = indices.map(i => availableSkills[i]);
      console.log(`  选择：复制 ${skillsToCopy.length} 个技能`);
    }
    
    // 执行复制
    let copiedCount = 0;
    skillsToCopy.forEach(skill => {
      const src = path.join(srcSkillsDir, skill);
      const dst = path.join(dstSkills, skill);
      if (fs.existsSync(src)) {
        if (fs.existsSync(dst)) fs.rmSync(dst, { recursive: true, force: true });
        fs.cpSync(src, dst, { recursive: true });
        log.success(`同步技能：${skill}`);
        copiedCount++;
      }
    });
    if (copiedCount > 0) log.success(`共同步 ${copiedCount} 个技能`);
    
    // ========== 步骤 7: 选择是否复制记忆 ==========
    log.step('步骤 7/11: 选择记忆同步');
    
    const srcMemory = path.join(srcWorkspace, 'memory');
    const dstMemory = path.join(workspaceDir, 'memory');
    
    // 列出可用记忆文件
    const memoryFiles = [];
    if (fs.existsSync(srcMemory)) {
      fs.readdirSync(srcMemory).forEach(file => {
        if (file.endsWith('.md')) {
          memoryFiles.push(file);
        }
      });
    }
    
    if (memoryFiles.length > 0) {
      console.log(`发现 ${memoryFiles.length} 个记忆文件（从 ${global.sourceAgentName}）：\n`);
      memoryFiles.forEach((file, i) => {
        console.log(`  [${String(i+1).padStart(2)}] ${file}`);
      });
      console.log(`  [ a] 全选`);
      console.log(`  [ n] 不复制（全新开始）`);
      
      const memoryInput = await question('\n请选择要同步的记忆文件：') || 'n';
      
      if (!fs.existsSync(dstMemory)) fs.mkdirSync(dstMemory, { recursive: true });
      
      let memoriesToCopy = [];
      
      if (memoryInput.toLowerCase() === 'n') {
        console.log('  选择：不复制记忆文件（全新开始）');
        log.success('记忆目录已创建，可以后续手动添加');
      } else if (memoryInput.toLowerCase() === 'a') {
        console.log('  选择：复制所有记忆文件');
        memoriesToCopy = memoryFiles;
      } else {
        // 解析选择的数字
        const indices = memoryInput.split(',').map(s => parseInt(s.trim()) - 1).filter(n => !isNaN(n) && n >= 0 && n < memoryFiles.length);
        memoriesToCopy = indices.map(i => memoryFiles[i]);
        console.log(`  选择：复制 ${memoriesToCopy.length} 个记忆文件`);
      }
      
      // 执行复制
      let copiedCount = 0;
      memoriesToCopy.forEach(file => {
        const src = path.join(srcMemory, file);
        const dst = path.join(dstMemory, file);
        fs.copyFileSync(src, dst);
        log.success(`复制记忆：${file}`);
        copiedCount++;
      });
      if (copiedCount > 0) log.success(`已复制 ${copiedCount} 个记忆文件`);
    } else {
      console.log('  没有找到记忆文件');
      if (!fs.existsSync(dstMemory)) fs.mkdirSync(dstMemory, { recursive: true });
      log.success('记忆目录已创建');
    }
    
    // ========== 步骤 8: 创建 systemd 服务 ==========
    log.step('步骤 8/11: 创建 systemd 服务');
    
    const systemdDir = path.join(process.env.HOME, '.config', 'systemd', 'user');
    if (!fs.existsSync(systemdDir)) fs.mkdirSync(systemdDir, { recursive: true });
    
    const serviceFile = path.join(systemdDir, `openclaw-gateway-${gatewayName}.service`);
    fs.writeFileSync(serviceFile, `[Unit]
Description=OpenClaw Gateway - ${gatewayDesc}
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /opt/openclaw/dist/index.js gateway
Restart=on-failure
RestartSec=10
Environment=HOME=${process.env.HOME}
Environment=TMPDIR=/tmp/openclaw-${gatewayName}
Environment=OPENCLAW_SERVICE_MARKER=openclaw-${gatewayName}
Environment=OPENCLAW_SERVICE_KIND=gateway
Environment=OPENCLAW_CONFIG_PATH=${configPath}
Environment=OPENCLAW_AGENT_DIR=${agentDir}/agent
Environment=PI_CODING_AGENT_DIR=${agentDir}/agent

[Install]
WantedBy=default.target
`);
    
    log.success(`创建服务文件：${serviceFile}`);
    
    // ========== 配置内存限制 ==========
    log.step('配置内存限制');
    
    try {
      // 从选择的配置来源读取内存限制（如果存在）
      const memoryLimitConf = path.join(srcWorkspace, '.openclaw', 'memory-limit.conf');
      
      let gatewayCount = 1;
      let memPerGateway = 600; // 默认 600MB
      let totalMemMB = 0; // 初始化
      
      if (fs.existsSync(memoryLimitConf)) {
        // 从配置文件读取
        const memoryConfig = fs.readFileSync(memoryLimitConf, 'utf8');
        const countMatch = memoryConfig.match(/GATEWAY_COUNT=(\d+)/);
        const memMatch = memoryConfig.match(/MEMORY_PER_GATEWAY=(\d+)/);
        if (countMatch) gatewayCount = parseInt(countMatch[1]);
        if (memMatch) memPerGateway = parseInt(memMatch[1]);
        log.info(`从配置读取：${gatewayCount}个网关，${memPerGateway}MB/网关`);
      } else {
        // 自动计算
        const memInfo = fs.readFileSync('/proc/meminfo', 'utf8');
        const totalMemMatch = memInfo.match(/MemTotal:\s*(\d+)/);
        const totalMemKB = totalMemMatch ? parseInt(totalMemMatch[1]) : 4000000;
        totalMemMB = Math.floor(totalMemKB / 1024);
        
        // 统计现有网关数量
        try {
          const services = execSync('ls ~/.config/systemd/user/openclaw-gateway-*.service 2>/dev/null || true', { encoding: 'utf8' });
          gatewayCount = services.trim().split('\n').filter(s => s.trim()).length + 1; // +1 表示新网关
        } catch (e) {
          gatewayCount = 1;
        }
        
        // 计算每个网关的内存（系统内存的 70% / 网关数量）
        const availableMem = Math.floor(totalMemMB * 70 / 100);
        memPerGateway = Math.floor(availableMem / gatewayCount);
        if (memPerGateway < 400) memPerGateway = 400; // 最少 400MB
        if (memPerGateway > 800) memPerGateway = 800; // 最多 800MB
        
        log.info(`自动计算：系统 ${totalMemMB}MB, ${gatewayCount}个网关，${memPerGateway}MB/网关`);
      }
      if (gatewayCount < 1) gatewayCount = 1;
      
      // 计算内存限制
      const memoryHigh = Math.floor(memPerGateway * 80 / 100);
      const memorySwap = Math.floor(memPerGateway * 50 / 100);
      
      // 创建内存限制配置
      const serviceDropInDir = path.join(systemdDir, `${gatewayName}.service.d`);
      if (!fs.existsSync(serviceDropInDir)) fs.mkdirSync(serviceDropInDir, { recursive: true });
      
      const memoryLimitConfig = `[Service]
MemoryHigh=${memoryHigh}M
MemoryMax=${memPerGateway}M
MemorySwapMax=${memorySwap}M
`;
      
      const memoryLimitFile = path.join(serviceDropInDir, 'memory-limit.conf');
      fs.writeFileSync(memoryLimitFile, memoryLimitConfig);
      
      if (totalMemMB > 0) {
        log.success(`配置内存限制：MemoryMax=${memPerGateway}M (系统 ${totalMemMB}MB, ${gatewayCount}个网关)`);
      } else {
        log.success(`配置内存限制：MemoryMax=${memPerGateway}M`);
      }
      log.info(`MemoryHigh=${memoryHigh}M (软限制)`);
      log.info(`MemorySwapMax=${memorySwap}M`);
      
      // 重新加载 systemd
      execSync('systemctl --user daemon-reload', { stdio: 'pipe' });
      log.success('systemd 已重新加载');
      
    } catch (e) {
      log.warn(`内存限制配置失败：${e.message}`);
      log.warn('可以稍后手动配置：bash setup-gateway-memory-limits.sh');
      
      // 至少重新加载 systemd
      execSync('systemctl --user daemon-reload', { stdio: 'pipe' });
      log.success('systemd 已重新加载');
    }
    
    // ========== 步骤 9: 启动网关 ==========
    log.step('步骤 9/11: 启动网关');
    
    const enableService = await question('是否现在启用并启动服务？[Y/n]: ');
    if (enableService.toLowerCase() !== 'n') {
      execSync(`systemctl --user enable openclaw-gateway-${gatewayName}.service`, { stdio: 'pipe' });
      log.success('启用服务');
      execSync(`systemctl --user start openclaw-gateway-${gatewayName}.service`, { stdio: 'pipe' });
      log.success('启动服务');
      
      // 动态等待网关启动（轮询检查，最多 30 秒）
      console.log('  ⏳ 等待网关启动...');
      let gatewayStarted = false;
      const maxAttempts = 30;
      
      for (let i = 1; i <= maxAttempts; i++) {
        try {
          const status = execSync(`systemctl --user is-active openclaw-gateway-${gatewayName}.service`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
          if (status === 'active') {
            log.success(`网关状态：active (运行中) - 尝试 ${i}/${maxAttempts}`);
            gatewayStarted = true;
            break;
          }
        } catch (e) {
          // 继续等待
        }
        
        if (i < maxAttempts) {
          process.stdout.write(`\r     等待中... (${i}/${maxAttempts})`);
          await new Promise(r => setTimeout(r, 1000));
        }
      }
      process.stdout.write('\r                                  \r');
      
      if (!gatewayStarted) {
        log.warn('网关未在规定时间内启动');
        log.warn(`检查 systemd 日志：journalctl --user -u openclaw-gateway-${gatewayName}.service -n 30`);
        log.warn(`检查应用日志：tail -n 30 /tmp/openclaw/openclaw-${gatewayName}.log`);
        
        // 显示最近的错误日志
        try {
          console.log('\n最近日志片段:');
          execSync(`tail -n 20 /tmp/openclaw/openclaw-${gatewayName}.log 2>/dev/null | grep -i error || echo '暂无错误日志'`, { stdio: 'inherit' });
        } catch (e) {
          // 忽略
        }
      }
      
      // 检查端口监听（多等 5 秒，给应用初始化时间）
      console.log('  ⏳ 等待端口监听...');
      await new Promise(r => setTimeout(r, 5000));
      
      let portListening = false;
      const maxPortAttempts = 10;
      
      for (let i = 1; i <= maxPortAttempts; i++) {
        try {
          // 尝试多种检测方法
          const ssCheck = execSync(`ss -tlnp 2>/dev/null | grep ":${gatewayPort} " || true`, { encoding: 'utf8' });
          const netstatCheck = execSync(`netstat -tlnp 2>/dev/null | grep ":${gatewayPort} " || true`, { encoding: 'utf8' });
          
          if (ssCheck.trim() || netstatCheck.trim()) {
            log.success(`端口 ${gatewayPort} 正在监听 (尝试 ${i}/${maxPortAttempts})`);
            portListening = true;
            break;
          }
        } catch (e) {
          // 继续尝试
        }
        
        if (i < maxPortAttempts) {
          process.stdout.write(`\r     等待端口监听... (${i}/${maxPortAttempts})`);
          await new Promise(r => setTimeout(r, 1000));
        }
      }
      process.stdout.write('\r                                  \r');
      
      if (!portListening) {
        log.warn(`端口 ${gatewayPort} 未监听`);
        log.warn('可能原因：网关启动失败或正在初始化');
        log.warn(`查看日志：journalctl --user -u openclaw-gateway-${gatewayName}.service -n 30`);
        log.warn(`或查看：tail -f /tmp/openclaw/openclaw-${gatewayName}.log`);
      }
    }
    
    // ========== 步骤 9.5: 检查 dmPolicy 配置 ==========
    log.step('步骤 9.5/11: 检查配对模式配置');
    
    // 读取配置中的 dmPolicy
    let dmPolicy = 'open'; // 默认
    try {
      const configContent = fs.readFileSync(configPath, 'utf8');
      const dmPolicyMatch = configContent.match(/"dmPolicy":\s*"([^"]+)"/);
      if (dmPolicyMatch) {
        dmPolicy = dmPolicyMatch[1];
      }
    } catch (e) {
      log.warn('无法读取 dmPolicy 配置，默认为 open');
    }
    
    console.log(`\n${colors.cyan}配对模式检测：${colors.reset}`);
    if (dmPolicy === 'pairing') {
      console.log(`  ${colors.yellow}⚠${colors.reset} 当前配置：dmPolicy = "pairing" (需要配对)`);
      console.log(`  ${colors.gray}说明：用户首次给机器人发消息时，会收到一个 6 位数配对码${colors.reset}`);
    } else {
      console.log(`  ${colors.green}✅${colors.reset} 当前配置：dmPolicy = "open" (无需配对)`);
      console.log(`  ${colors.gray}说明：用户可以直接给机器人发消息，无需配对${colors.reset}`);
    }
    console.log('');
    
    // ========== 步骤 9.5: 生成飞书配置清单 ==========
    if (!global.skipFeishuConfig) {
      log.step('步骤 9.5/11: 生成飞书配置清单');
      
      const checklistPath = path.join(workspaceDir, 'feishu-checklist.md');
    const checklistContent = `# 飞书配置检查清单 - ${gatewayDesc}

## 应用信息
- **应用名称**: ${gatewayDesc}
- **App ID**: (待填写)
- **App Secret**: (待填写)

## 1. 权限配置
请在飞书开发者后台「权限管理」页面添加以下权限：

### 必需权限
- [ ] contact:contact.base:readonly - 读取用户基本信息
- [ ] im:message - 发送和接收消息
- [ ] im:message.receive - 接收消息
- [ ] im:message.send - 发送消息
- [ ] im:chat - 访问群聊信息
- [ ] im:chat.p2p - 访问私聊会话
- [ ] cardkit:card:write - 创建卡片消息
- [ ] websocket - 使用长连接
- [ ] event:im.message.receive_v1 - 接收消息事件
- [ ] bot:chat - 机器人访问聊天

### 可选权限（根据需求）
- [ ] aily:file:read - 读取文件
- [ ] aily:file:write - 写入文件
- [ ] contact:user.employee_id:readonly - 读取员工 ID

## 2. 事件订阅
- [ ] 订阅方式：使用长连接接收事件/回调
- [ ] 添加事件：im.message.receive_v1
- [ ] 保存配置

## 3. 验证步骤
- [ ] 在飞书中给机器人发消息
- [ ] 机器人能够正常回复
- [ ] 如果 dmPolicy=pairing，完成配对授权

## 4. 本地配置
- **配置文件**: ${configPath}
- **端口**: ${gatewayPort}
- **服务名称**: openclaw-gateway-${gatewayName}.service

## 管理命令
\`\`\`bash
# 查看状态
systemctl --user status openclaw-gateway-${gatewayName}.service

# 查看日志
journalctl --user -u openclaw-gateway-${gatewayName}.service -f

# 重启网关
systemctl --user restart openclaw-gateway-${gatewayName}.service

# 查看实时日志
tail -f /tmp/openclaw/openclaw-${gatewayName}.log
\`\`\`

---
**生成时间**: ${new Date().toISOString()}
`;
    
    fs.writeFileSync(checklistPath, checklistContent);
    log.success(`生成飞书配置清单：${checklistPath}`);
    console.log(`\n${colors.cyan}提示：${colors.reset}可以打印此清单，在飞书后台逐项配置\n`);
    
    } else {
      log.info('已跳过飞书配置清单生成（用户选择纯本地使用）');
    }
    
    // ========== 步骤 10: 飞书配置引导 ==========
    if (!global.skipFeishuConfig) {
      log.step('步骤 10/11: 飞书配置引导');
    
    console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log(`${colors.yellow}📋 现在需要导入飞书应用权限${colors.reset}`);
    console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
    console.log('请在飞书开发者后台「权限管理」页面，直接导入以下配置：\n');
    console.log(`${colors.gray}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log(colors.yellow + JSON.stringify({
      scopes: {
        tenant: [
          "aily:file:read",
          "aily:file:write",
          "application:application.app_message_stats.overview:readonly",
          "application:application:self_manage",
          "application:bot.menu:write",
          "contact:user.employee_id:readonly",
          "corehr:file:download",
          "event:ip_list",
          "im:chat.access_event.bot_p2p_chat:read",
          "im:chat.members:bot_access",
          "im:message",
          "im:message.group_at_msg:readonly",
          "im:message.p2p_msg:readonly",
          "im:message:readonly",
          "im:message:send_as_bot",
          "im:resource"
        ],
        user: ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
      }
    }, null, 2) + colors.reset);
    console.log(`${colors.gray}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
    console.log('操作步骤：');
    console.log('  1. 访问飞书开发者后台');
    console.log('  2. 进入应用 → 权限管理');
    console.log('  3. 点击「批量导入」或手动添加上述权限');
    console.log('  4. 点击「申请权限」');
    console.log('  5. 等待审核通过（通常几分钟）\n');
    
    await question('✅ 权限已导入后，按回车继续...');
    log.success('权限已导入');
    
    // 等待长连接 - 智能检测（总共 15 秒）
    console.log('\n🔗 正在等待飞书长连接自动建立...\n');
    let connected = false;
    const checkLogPath = `/tmp/openclaw/openclaw-${gatewayName}.log`;
    const maxAttempts = 15;  // 最多 15 次
    const intervalMs = 1000;  // 每次间隔 1 秒
    
    for (let i = 1; i <= maxAttempts; i++) {
      try {
        // 检查日志中的连接成功标志
        const logContent = execSync(`tail -100 ${checkLogPath} 2>/dev/null || true`, { encoding: 'utf8' });
        
        // 多个连接成功标志（按优先级排序）
        const connectedSigns = [
          // 最高优先级：能收到消息，说明长连接肯定建立了
          'feishu[default]: received message',
          'feishu[default]: dispatching to agent',
          // 其次：WebSocket 已启动
          'WebSocket client started',
          'ws client ready',
          'event-dispatch is ready',
          '[feishu] feishu[default]: WebSocket'
        ];
        
        // 检查是否有错误
        const errorSigns = ['WebSocket closed', 'connection failed', 'auth failed', 'permission denied', 'Access denied'];
        const hasError = errorSigns.some(sign => logContent.includes(sign));
        
        // 检查是否连接成功（任意一个标志即可）
        const hasConnected = connectedSigns.some(sign => logContent.includes(sign));
        
        if (hasConnected && !hasError) {
          log.success('飞书长连接已建立！');
          connected = true;
          break;
        }
        
        if (hasError) {
          log.warn('检测到权限错误，请确认权限已开通');
          // 继续等待，因为权限可能刚开通还在生效中
        }
      } catch(e) {
        // 日志文件可能还不存在
      }
      
      if (i < maxAttempts) {
        process.stdout.write(`\r   ⏳ 等待中... (${i}/${maxAttempts})`);
        await new Promise(r => setTimeout(r, intervalMs));
      }
    }
    process.stdout.write('\r                              \r');
    
    if (connected) {
      log.success('验证通过：飞书长连接正常');
    } else {
      log.warn('飞书长连接尚未建立');
      log.warn('请检查：1) 权限是否已开通  2) App ID/Secret 是否正确');
      log.warn(`查看日志：tail -f ${checkLogPath}`);
    }
    
    } else {
      log.info('已跳过飞书配置引导（用户选择纯本地使用）');
    }
    
    // ========== 步骤 11: 添加接收消息事件 ==========
    if (!global.skipFeishuConfig) {
      log.step('步骤 11/11: 添加接收消息事件');
    
    console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log(`${colors.yellow}📋 现在需要添加接收消息事件${colors.reset}`);
    console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
    console.log('请在飞书开发者后台「事件订阅」页面：\n');
    console.log('  1. 进入应用 → 事件订阅');
    console.log('  2. 确保订阅方式选择：「使用长连接接收事件/回调」');
    console.log('  3. 点击「添加事件」');
    console.log('  4. 搜索并添加：im.message.receive_v1');
    console.log('  5. 点击「保存」\n');
    
    await question('✅ 事件已添加后，按回车继续...');
    log.success('已确认事件订阅配置');
    
    } else {
      log.info('已跳过事件订阅配置（用户选择纯本地使用）');
    }
    
    // ========== 总结 ==========
    console.log(`\n${colors.green}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
    console.log(`${colors.green}🎉 恭喜！${gatewayDesc} 配置完成！${colors.reset}`);
    console.log(`${colors.green}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
    
    console.log('配置摘要：');
    console.log(`  Agent 名称：${gatewayName}`);
    console.log(`  网关名称：${gatewayDesc}`);
    console.log(`  端口：${gatewayPort}`);
    console.log('');
    console.log('✅ 已完成：');
    console.log('  ✓ 配置复制（完整复制 main）');
    console.log('  ✓ API Key 修复');
    console.log('  ✓ systemd 服务创建');
    if (!global.skipFeishuConfig) {
      console.log('  ✓ 飞书权限导入');
      console.log('  ✓ 长连接建立');
      console.log('  ✓ 接收消息事件添加');
    } else {
      console.log('  ○ 飞书配置（已跳过，纯本地使用）');
    }
    console.log('');
    console.log('管理命令：');
    console.log(`  查看状态：systemctl --user status openclaw-gateway-${gatewayName}.service`);
    console.log(`  查看日志：journalctl --user -u openclaw-gateway-${gatewayName}.service -f`);
    console.log(`  重启网关：systemctl --user restart openclaw-gateway-${gatewayName}.service`);
    console.log('');
    
    // ========== 步骤 12: 配对码授权（根据 dmPolicy 决定） ==========
    // 如果跳过了飞书配置，则跳过配对测试
    if (!global.skipFeishuConfig && dmPolicy === 'pairing') {
      // 需要配对模式
      console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
      console.log(`${colors.yellow}📬 现在进行配对授权${colors.reset}`);
      console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
      console.log(`${colors.yellow}⚠${colors.reset} 当前配置为 ${colors.bold}pairing${colors.reset} 模式，需要配对才能接收消息。\n`);
      console.log('操作步骤：');
      console.log('  1. 在飞书中给机器人发送任意消息');
      console.log('  2. 机器人会回复一个配对码（6 位数字）');
      console.log('  3. 将配对码输入到这里\n');
      
      const needPairing = await question('是否需要现在配对？[Y/n]: ');
      if (needPairing.toLowerCase() !== 'n') {
        console.log('\n请前往飞书给机器人发消息，然后输入配对码...');
        const pairingCode = await question('配对码（6 位数字）: ');
        
        if (pairingCode && pairingCode.length >= 4) {
          console.log('\n正在提交配对码...');
          
          // 调用 openclaw pairing 命令
          try {
            const result = execSync(`openclaw pairing ${pairingCode.trim()} --agent ${gatewayName}`, { 
              encoding: 'utf8',
              stdio: 'pipe'
            });
            log.success('配对成功！');
            console.log(result);
          } catch (e) {
            log.warn('配对命令执行失败，请手动配对');
            log.warn(`手动配对：openclaw pairing ${pairingCode.trim()} --agent ${gatewayName}`);
          }
        } else {
          log.info('跳过配对');
        }
        
        console.log('\n配对后测试：');
        console.log(`  在飞书中给机器人发消息，应该能正常对话了！\n`);
      } else {
        log.info('跳过配对（稍后需要时可手动执行：openclaw pairing <配对码> --agent ' + gatewayName + ')');
      }
    } else {
      // open 模式，无需配对
      console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
      console.log(`${colors.green}✅ 无需配对${colors.reset}`);
      console.log(`${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);
      console.log(`${colors.green}✓${colors.reset} 当前配置为 ${colors.bold}open${colors.reset} 模式，无需配对即可使用。\n`);
      
      // open 模式下不显示测试提示，直接显示下一步
    }
    
    console.log('');
    console.log('下一步：');
    if (global.skipFeishuConfig) {
      console.log('  ℹ️  飞书配置已跳过（纯本地使用）');
      console.log('  如需绑定渠道，可手动修改配置文件或运行 openclaw channels login');
      console.log('');
      console.log('管理命令：');
      console.log(`  查看状态：systemctl --user status openclaw-gateway-${gatewayName}.service`);
      console.log(`  查看日志：journalctl --user -u openclaw-gateway-${gatewayName}.service -f`);
    } else {
      console.log('  1. 在飞书上给机器人发消息');
      console.log('  2. 开始正常使用！');
    }
    console.log('');
    
  } catch (error) {
    log.error(`配置出错：${error.message}`);
    process.exit(1);
  } finally {
    rl.close();
  }
}

main();
