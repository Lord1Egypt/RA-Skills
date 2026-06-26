const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = require('@modelcontextprotocol/sdk/client/stdio.js');
const path = require('path');
const fs = require('fs');

/**
 * 加载配置（优先 config.local.json，其次环境变量）
 * 环境变量优先级：X_VARIFLIGHT_KEY（官方）> VARIFLIGHT_API_KEY（兼容备用）
 */
function loadApiKey() {
  const localConfig = path.join(__dirname, '../../config.local.json');
  if (fs.existsSync(localConfig)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(localConfig, 'utf8'));
      if (cfg.apiKey) return cfg.apiKey;
    } catch (_) {}
  }
  const envKey = process.env.X_VARIFLIGHT_KEY || process.env.VARIFLIGHT_API_KEY;
  if (envKey) return envKey;
  throw new Error(
    'API Key 未配置。请在 config.local.json 中设置 "apiKey"，\n' +
    '或设置环境变量 X_VARIFLIGHT_KEY。\n' +
    '前往 https://ai.variflight.com/keys 获取 Key。'
  );
}

class VariflightClient {
  constructor() {
    this.apiKey = loadApiKey();
    this.client = null;
    this.transport = null;
    this.isConnected = false;
  }

  async connect() {
    if (this.isConnected) return;

    this.transport = new StdioClientTransport({
      command: 'npx',
      args: ['-y', '@variflight-ai/variflight-mcp'],
      env: {
        ...process.env,
        X_VARIFLIGHT_KEY: this.apiKey,
        VARIFLIGHT_API_KEY: this.apiKey  // 兼容备用
      }
    });

    this.client = new Client({
      name: 'variflight-skill',
      version: '1.0.0'
    });

    await this.client.connect(this.transport);
    this.isConnected = true;
  }

  async disconnect() {
    if (this.client) {
      try { await this.client.close(); } catch (_) {}
      this.client = null;
    }
    if (this.transport) {
      try { await this.transport.close(); } catch (_) {}
      this.transport = null;
    }
    this.isConnected = false;
  }

  /**
   * 调用 MCP 工具，返回解析后的数据
   */
  async callTool(name, args) {
    await this.connect();
    const result = await this.client.callTool({ name, arguments: args });
    if (result && result.content && Array.isArray(result.content)) {
      const text = result.content.find(c => c.type === 'text');
      if (text && text.text) {
        // 检查是否错误字符串
        if (text.text.startsWith('Error:')) {
          throw new Error(text.text.replace(/^Error:\s*/, ''));
        }
        try { return JSON.parse(text.text); } catch (_) { return text.text; }
      }
    }
    return result;
  }

  // ======== 业务封装 ========

  /** 按航班号+日期查询（info / comfort / track 命令核心） */
  async searchFlightsByNumber(fnum, date, dep, arr) {
    const args = { fnum: fnum.toUpperCase(), date };
    if (dep) args.dep = dep.toUpperCase();
    if (arr) args.arr = arr.toUpperCase();
    return this.callTool('searchFlightsByNumber', args);
  }

  /** 按出发/到达机场查询（search 命令核心） */
  async searchFlightsByDepArr(dep, arr, date) {
    const args = { date };
    if (dep) args.dep = dep.toUpperCase();
    if (arr) args.arr = arr.toUpperCase();
    return this.callTool('searchFlightsByDepArr', args);
  }

  /** 中转方案查询（transfer 命令核心） */
  async getFlightTransferInfo(depCity, arrCity, depdate) {
    return this.callTool('getFlightTransferInfo', {
      depcity: depCity.toUpperCase(),
      arrcity: arrCity.toUpperCase(),
      depdate
    });
  }

  /** 飞行幸福指数（comfort 命令核心） */
  async flightHappinessIndex(fnum, date, dep, arr) {
    const args = { fnum: fnum.toUpperCase(), date };
    if (dep) args.dep = dep.toUpperCase();
    if (arr) args.arr = arr.toUpperCase();
    return this.callTool('flightHappinessIndex', args);
  }

  /** 飞机实时位置（track 命令使用，需要注册号 anum） */
  async getRealtimeLocationByAnum(anum) {
    return this.callTool('getRealtimeLocationByAnum', { anum });
  }

  /** 机场天气（weather 命令核心） */
  async getFutureWeatherByAirport(airport) {
    return this.callTool('getFutureWeatherByAirport', { airport: airport.toUpperCase() });
  }

  /** 最低票价搜索（search 命令附加） */
  async searchFlightItineraries(depCity, arrCity, depDate) {
    return this.callTool('searchFlightItineraries', {
      depCityCode: depCity.toUpperCase(),
      arrCityCode: arrCity.toUpperCase(),
      depDate
    });
  }

  /** 获取今日日期 */
  async getTodayDate() {
    const r = await this.callTool('getTodayDate', {});
    return typeof r === 'string' ? r : new Date().toISOString().slice(0, 10);
  }
}

module.exports = { VariflightClient };
