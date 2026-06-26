const fs = require('fs');
const path = require('path');

// ========== 加载配置 / Load Config ==========
const CONFIG_FILE = './config.json';

let config = {
  feishu: {
    app_id: process.env.FEISHU_APP_ID || 'YOUR_APP_ID',
    app_secret: process.env.FEISHU_APP_SECRET || 'YOUR_APP_SECRET',
    user_id: process.env.FEISHU_USER_ID || 'YOUR_USER_OPEN_ID'
  },
  qclaw: {
    health_url: process.env.QCLAW_HEALTH_URL || 'http://127.0.0.1:28789/health'
  },
  watchdog: {
    check_interval_ms: parseInt(process.env.CHECK_INTERVAL_MS) || 180000,
    restart_delay_ms: parseInt(process.env.RESTART_DELAY_MS) || 10000,
    max_retries: parseInt(process.env.MAX_RETRIES) || 3
  },
  logs: {
    main_log: process.env.LOG_FILE || './watchdog.log',
    command_log: process.env.CMD_FILE || './commands.log'
  }
};

// 尝试读取配置文件 / Try to read config file
try {
  if (fs.existsSync(CONFIG_FILE)) {
    const fileConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    config = {
      feishu: { ...config.feishu, ...fileConfig.feishu },
      qclaw: { ...config.qclaw, ...fileConfig.qclaw },
      watchdog: { ...config.watchdog, ...fileConfig.watchdog },
      logs: { ...config.logs, ...fileConfig.logs }
    };
    console.log(`配置文件已加载: ${CONFIG_FILE}`);
  } else {
    console.log(`配置文件不存在，使用默认配置或环境变量`);
    console.log(`Config file not found, using default config or environment variables`);
    console.log(`提示: 运行 ./init-config.sh 创建配置文件`);
    console.log(`Tip: Run ./init-config.sh to create config file`);
  }
} catch (e) {
  console.error(`加载配置文件失败: ${e.message}`);
}

// 使用配置 / Use config
const FEISHU_APP_ID = config.feishu.app_id;
const FEISHU_APP_SECRET = config.feishu.app_secret;
const USER_ID = config.feishu.user_id;
const QCLAW_HEALTH_URL = config.qclaw.health_url;
const CHECK_INTERVAL = config.watchdog.check_interval_ms;
const RESTART_DELAY = config.watchdog.restart_delay_ms;
const MAX_RETRIES = config.watchdog.max_retries;
const LOG_FILE = config.logs.main_log;
const CMD_FILE = config.logs.command_log;

// ========== Lark SDK ==========
const { Client, WSClient, AppType, EventDispatcher, LoggerLevel } = require('@larksuiteoapi/node-sdk');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// 指令映射 / Command mapping
const COMMANDS = {
  '状态': 'status', 'status': 'status',
  '重启': 'restart', 'restart': 'restart',
  '启动': 'start', 'start': 'start',
  '退出': 'quit', 'quit': 'quit',
  '帮助': 'help', 'help': 'help',
  '配置': 'config', 'config': 'config'
};

// 日志函数 / Log functions
function log(message) {
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const line = `[${timestamp}] ${message}`;
  console.log(line);
  
  try {
    fs.appendFileSync(LOG_FILE, line + '\n');
  } catch (e) {
    // 忽略写入错误
  }
}

// 记录命令到专门文件 / Log commands to separate file
function logCommand(type, text, result) {
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const line = `[${timestamp}] [${type}] "${text}" -> ${result}`;
  
  try {
    fs.appendFileSync(CMD_FILE, line + '\n');
  } catch (e) {
    // 忽略写入错误
  }
}

class Watchdog {
  constructor() {
    this.client = null;
    this.wsClient = null;
    this.eventDispatcher = null;
  }

  // 构建卡片消息 / Build card message
  buildCard(title, content, tagColor = 'blue') {
    return {
      config: { wide_screen_mode: true },
      header: {
        title: { tag: 'plain_text', content: title },
        template: tagColor
      },
      elements: [
        { tag: 'div', text: { tag: 'lark_md', content: content } }
      ]
    };
  }

  // 发送消息 / Send message
  async sendMessage(card, tagColor = 'blue') {
    try {
      const result = await this.client.im.message.create({
        params: { receive_id_type: 'open_id' },
        data: {
          receive_id: USER_ID,
          msg_type: 'interactive',
          content: JSON.stringify(card)
        }
      });
      
      if (result.code !== 0) {
        log(`发送消息失败: ${JSON.stringify(result)}`);
      }
    } catch (e) {
      log(`发送消息异常: ${e.message}`);
    }
  }

  // 回复消息 / Reply message
  async replyMessage(messageId, card, tagColor = 'blue') {
    try {
      log(`回复消息到: ${messageId}`);
      const result = await this.client.im.message.reply({
        path: { message_id: messageId },
        data: {
          content: JSON.stringify(card),
          msg_type: 'interactive'
        }
      });
      
      log(`回复结果: code=${result.code}, msg=${result.msg}`);
      if (result.code !== 0) {
        log(`回复失败详情: ${JSON.stringify(result)}`);
      }
    } catch (e) {
      log(`回复异常: ${e.message}`);
    }
  }

  // 检查 QClaw 状态 / Check QClaw status
  async checkQclawStatus() {
    log('开始检查 QClaw 状态...');
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(QCLAW_HEALTH_URL, { 
        signal: controller.signal 
      });
      clearTimeout(timeoutId);
      
      log(`  Gateway 响应状态码: ${response.status}`);
      
      if (response.status === 200) {
        const data = await response.json();
        log(`  Gateway 返回数据: ${JSON.stringify(data)}`);
        
        if (data.status === 'live' || data.status === 'healthy' || data.status === 'ok') {
          log('  判断: Gateway 正常');
          return { status: 'running', detail: `Gateway 正常 (status=${data.status})` };
        } else {
          log(`  判断: Gateway 状态异常 (status=${data.status})`);
          return { status: 'unhealthy', detail: `Gateway 状态异常: ${JSON.stringify(data)}` };
        }
      }
      
      return { status: 'no_response', detail: `HTTP ${response.status}` };
    } catch (e) {
      log(`  Gateway 连接失败: ${e.message}`);
    }
    
    // 检查进程 / Check process
    log('  Gateway 无响应，检查 QClaw 进程...');
    try {
      const { stdout } = await execPromise('pgrep -f QClaw');
      const pids = stdout.trim().split('\n').filter(p => p);
      log(`  判断: QClaw 进程存在 (PID: ${pids.join(', ')})，但 Gateway 无响应`);
      return { status: 'no_response', detail: `QClaw 进程在运行 (PID: ${pids.join(', ')}) 但 Gateway 无响应` };
    } catch (e) {
      log('  判断: QClaw 进程不存在');
      return { status: 'stopped', detail: 'QClaw 未运行' };
    }
  }

  // 启动 QClaw / Start QClaw
  async startQclaw() {
    try {
      await execPromise('open -a QClaw');
      return '已启动 QClaw';
    } catch (e) {
      return `启动失败: ${e.message}`;
    }
  }

  // 重启 QClaw / Restart QClaw
  async restartQclaw() {
    try {
      await execPromise('osascript -e \'tell application "QClaw" to quit\'');
      await new Promise(r => setTimeout(r, 3000));
      await execPromise('pkill -f QClaw').catch(() => {});
      await new Promise(r => setTimeout(r, 2000));
      await execPromise('open -a QClaw');
      return '已重启 QClaw';
    } catch (e) {
      return `重启失败: ${e.message}`;
    }
  }

  // 退出 QClaw / Quit QClaw
  async quitQclaw() {
    try {
      await execPromise('osascript -e \'tell application "QClaw" to quit\'');
      return '已退出 QClaw';
    } catch (e) {
      return `退出失败: ${e.message}`;
    }
  }

  // 确保 QClaw 可用 / Ensure QClaw is available
  async ensureQclawAvailable() {
    for (let i = 0; i < MAX_RETRIES; i++) {
      const { status, detail } = await this.checkQclawStatus();
      
      if (status === 'running') {
        return { success: true, message: 'QClaw 正常运行' };
      }
      
      log(`QClaw 不可用 (${status}): ${detail}, 尝试修复... (${i + 1}/${MAX_RETRIES})`);
      
      const result = status === 'stopped' 
        ? await this.startQclaw() 
        : await this.restartQclaw();
      
      log(`执行操作: ${result}`);
      await new Promise(r => setTimeout(r, RESTART_DELAY / 1000));
      
      const check = await this.checkQclawStatus();
      if (check.status === 'running') {
        return { success: true, message: `修复成功: ${result}` };
      }
    }
    
    return { success: false, message: `修复失败，已尝试 ${MAX_RETRIES} 次` };
  }

  // 处理用户指令 / Handle user commands
  async handleCommand(text, messageId) {
    const cmd = COMMANDS[text.toLowerCase()] || 'unknown';
    log(`处理指令: ${text} -> ${cmd}`);
    logCommand('指令', text, cmd);
    
    switch (cmd) {
      case 'status': {
        const { status, detail } = await this.checkQclawStatus();
        logCommand('状态查询', text, status);
        const statusConfig = {
          running: ['🟢 运行正常', 'green'],
          unhealthy: ['🟡 状态异常', 'orange'],
          no_response: ['🔴 无响应', 'red'],
          stopped: ['⚫ 已停止', 'gray']
        };
        const [title, color] = statusConfig[status] || ['❓ 未知状态', 'blue'];
        const card = this.buildCard(
          `QClaw 状态 - ${title}`,
          `**状态**: ${status}\n**详情**: ${detail}`,
          color
        );
        await this.replyMessage(messageId, card, color);
        break;
      }
      
      case 'restart': {
        logCommand('重启', text, '开始');
        await this.replyMessage(messageId, this.buildCard('🔄 正在重启 QClaw...', '请稍候', 'blue'), 'blue');
        const { success, message } = await this.ensureQclawAvailable();
        logCommand('重启', text, success ? '成功' : '失败');
        const color = success ? 'green' : 'red';
        const title = success ? '✅ 重启成功' : '❌ 重启失败';
        const card = this.buildCard(title, message, color);
        await this.replyMessage(messageId, card, color);
        break;
      }
      
      case 'start': {
        const { status } = await this.checkQclawStatus();
        logCommand('启动', text, status);
        if (status === 'running') {
          const card = this.buildCard('✅ 已在运行', 'QClaw 已经在运行中，无需启动', 'green');
          await this.replyMessage(messageId, card, 'green');
        } else {
          await this.replyMessage(messageId, this.buildCard('▶️ 正在启动 QClaw...', '请稍候', 'blue'), 'blue');
          const result = await this.startQclaw();
          await new Promise(r => setTimeout(r, RESTART_DELAY));
          const check = await this.checkQclawStatus();
          const success = check.status === 'running';
          logCommand('启动', text, success ? '成功' : '失败');
          const color = success ? 'green' : 'red';
          const title = success ? '✅ 启动成功' : '❌ 启动失败';
          const card = this.buildCard(title, `${result}\n\n**当前状态**: ${check.status}`, color);
          await this.replyMessage(messageId, card, color);
        }
        break;
      }
      
      case 'quit': {
        const result = await this.quitQclaw();
        logCommand('退出', text, result);
        const card = this.buildCard('⏹️ 已退出', result, 'gray');
        await this.replyMessage(messageId, card, 'gray');
        break;
      }
      
      case 'config': {
        logCommand('配置', text, '显示');
        const interval = Math.round(CHECK_INTERVAL / 60000);
        const card = this.buildCard(
          '⚙️ 当前配置',
          `**巡检间隔**: ${interval} 分钟\n**重启延迟**: ${RESTART_DELAY / 1000} 秒\n**最大重试**: ${MAX_RETRIES} 次\n\n配置文件: config.json\n更新配置后重启生效`,
          'blue'
        );
        await this.replyMessage(messageId, card, 'blue');
        break;
      }
      
      case 'help': {
        logCommand('帮助', text, '显示');
        const card = this.buildCard(
          '🐕 看门狗指令',
          `• **状态/status** - 检查 QClaw 状态
• **重启/restart** - 确保 QClaw 可用
• **启动/start** - 启动 QClaw
• **退出/quit** - 退出 QClaw
• **配置/config** - 显示当前配置
• **帮助/help** - 显示此帮助

自动监控：每${Math.round(CHECK_INTERVAL / 60000)}分钟检查一次，异常自动修复`,
          'blue'
        );
        await this.replyMessage(messageId, card, 'blue');
        break;
      }
      
      default: {
        const card = this.buildCard('❓ 未知指令', '发送「帮助」查看可用指令', 'orange');
        await this.replyMessage(messageId, card, 'orange');
      }
    }
  }

  // 自动监控 / Auto monitor
  autoMonitor() {
    this.monitorLoop().catch(e => {
      log(`监控循环错误: ${e.message}`);
    });
  }

  async monitorLoop() {
    await new Promise(r => setTimeout(r, 10000));
    
    while (true) {
      try {
        log('='.repeat(50));
        log('执行自动检查...');
        
        const { status, detail } = await this.checkQclawStatus();
        log(`检查结果: status=${status}, detail=${detail}`);
        
        if (status === 'running') {
          log('判断: QClaw 正常，无需操作');
          logCommand('巡检', '自动', '正常');
          const card = this.buildCard(
            '🟢 QClaw 巡检正常',
            `**状态**: 运行正常\n**详情**: ${detail}\n**时间**: ${new Date().toLocaleTimeString()}`,
            'green'
          );
          await this.sendMessage(card, 'green');
        } else {
          log(`判断: QClaw 异常 (${status})，开始自动修复...`);
          logCommand('巡检', '自动', `异常-${status}`);
          
          const card = this.buildCard(
            '🔴 QClaw 异常检测',
            `**状态**: ${status}\n**详情**: ${detail}\n**时间**: ${new Date().toLocaleTimeString()}\n\n🔄 正在自动修复...`,
            'red'
          );
          await this.sendMessage(card, 'red');
          
          const { success, message } = await this.ensureQclawAvailable();
          
          if (success) {
            log(`修复成功: ${message}`);
            logCommand('自动修复', '自动', '成功');
            const card = this.buildCard(
              '🟢 QClaw 修复成功',
              `**原状态**: ${status}\n**修复结果**: ${message}\n**时间**: ${new Date().toLocaleTimeString()}`,
              'green'
            );
            await this.sendMessage(card, 'green');
          } else {
            log(`修复失败: ${message}`);
            logCommand('自动修复', '自动', '失败');
            const card = this.buildCard(
              '🔴 QClaw 修复失败',
              `**状态**: ${status}\n**详情**: ${detail}\n**修复结果**: ${message}\n**时间**: ${new Date().toLocaleTimeString()}\n\n⚠️ 请手动检查！`,
              'red'
            );
            await this.sendMessage(card, 'red');
          }
        }
      } catch (e) {
        log(`自动监控异常: ${e.message}`);
        logCommand('错误', '自动', e.message);
        const card = this.buildCard(
          '🔴 看门狗异常',
          `监控脚本出错: ${e.message}\n**时间**: ${new Date().toLocaleTimeString()}`,
          'red'
        );
        await this.sendMessage(card, 'red');
      }
      
      log(`等待 ${CHECK_INTERVAL / 1000} 秒后进行下次检查...`);
      await new Promise(r => setTimeout(r, CHECK_INTERVAL));
    }
  }

  // 启动看门狗 / Start watchdog
  async start() {
    log('='.repeat(50));
    log('看门狗启动...');
    log(`检查间隔: ${CHECK_INTERVAL / 1000} 秒`);
    
    // 创建 HTTP 客户端
    this.client = new Client({
      appId: FEISHU_APP_ID,
      appSecret: FEISHU_APP_SECRET,
      appType: AppType.SelfBuild
    });
    
    // 创建事件分发器
    this.eventDispatcher = new EventDispatcher({});
    
    // 注册消息事件处理器
    this.eventDispatcher.register({
      'im.message.receive_v1': async (data) => {
        log(`收到消息事件`);
        
        try {
          const message = data.message || {};
          
          log(`消息类型: ${message.message_type}`);
          log(`消息内容: ${message.content}`);
          
          if (message.message_type === 'text') {
            const content = JSON.parse(message.content);
            const text = content.text?.trim() || '';
            const messageId = message.message_id;
            
            log(`收到指令: "${text}"`);
            await this.handleCommand(text, messageId);
          }
        } catch (e) {
          log(`处理消息失败: ${e.message}`);
        }
      }
    });
    
    // 创建 WebSocket 客户端
    this.wsClient = new WSClient({
      appId: FEISHU_APP_ID,
      appSecret: FEISHU_APP_SECRET,
      appType: AppType.SelfBuild,
      loggerLevel: LoggerLevel.info
    });
    
    // 发送启动通知
    const card = this.buildCard(
      '🐕 看门狗已启动',
      `**检查间隔**: ${Math.round(CHECK_INTERVAL / 60000)} 分钟\n**自动修复**: 已启用\n**启动时间**: ${new Date().toLocaleString()}\n\n发送「帮助」查看可用指令`,
      'blue'
    );
    await this.sendMessage(card, 'blue');
    
    // 启动 WebSocket
    log('连接 WebSocket...');
    this.wsClient.start({ eventDispatcher: this.eventDispatcher });
    log('WebSocket 已启动');
    
    // 启动自动监控
    this.autoMonitor();
  }
}

// 启动看门狗
const watchdog = new Watchdog();
watchdog.start().catch(e => {
  log(`致命错误: ${e.message}`);
  console.error(e);
  process.exit(1);
});
