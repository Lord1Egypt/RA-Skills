/**
 * 配置加载器 - 从 config.yaml 读取，支持环境变量覆盖
 *
 * 环境变量优先级 > config.yaml
 *   WECOM_BOT_ID     → wecom.bot_id
 *   WECOM_BOT_SECRET → wecom.bot_secret
 *   AGENT_ENDPOINT   → agent.endpoint
 *   MONITOR_HEARTBEAT_INTERVAL → monitor.heartbeat_interval
 *   MONITOR_NOTIFY_CHATID      → monitor.notify_chatid
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const CONFIG_PATH = process.env.CONFIG_YAML_PATH
  ? path.resolve(process.env.CONFIG_YAML_PATH)
  : path.join(__dirname, 'config.yaml');

let _config = null;

function loadConfig() {
  if (_config) return _config;

  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  _config = yaml.load(raw);

  // 环境变量覆盖
  if (process.env.WECOM_BOT_ID)     _config.wecom.bot_id = process.env.WECOM_BOT_ID;
  if (process.env.WECOM_BOT_SECRET) _config.wecom.bot_secret = process.env.WECOM_BOT_SECRET;
  if (process.env.AGENT_ENDPOINT)   _config.agent.endpoint = process.env.AGENT_ENDPOINT;

  // 监控配置环境变量覆盖
  if (process.env.MONITOR_HEARTBEAT_INTERVAL) {
    _config.monitor = _config.monitor || {};
    _config.monitor.heartbeat_interval = parseInt(process.env.MONITOR_HEARTBEAT_INTERVAL);
  }
  if (process.env.MONITOR_NOTIFY_CHATID) {
    _config.monitor = _config.monitor || {};
    _config.monitor.notify_chatid = process.env.MONITOR_NOTIFY_CHATID;
  }

  // 云端转换 API 配置（环境变量优先）
  if (process.env.CONVERTER_API_BASE) {
    _config.converter = _config.converter || {};
    _config.converter.api_base = process.env.CONVERTER_API_BASE;
  }
  if (process.env.CONVERTER_API_KEY) {
    _config.converter = _config.converter || {};
    _config.converter.api_key = process.env.CONVERTER_API_KEY;
  }

  // 把 converter 配置注入环境变量（供 msg-converter 读取）
  if (_config.converter) {
    if (_config.converter.api_base) process.env.CONVERTER_API_BASE = _config.converter.api_base;
    if (_config.converter.api_key)  process.env.CONVERTER_API_KEY  = _config.converter.api_key;
  }

  return _config;
}

function validateConfig(config) {
  const errors = [];
  const c = config || loadConfig();

  if (!c.wecom || !c.wecom.bot_id || c.wecom.bot_id.includes('你的'))
    errors.push('wecom.bot_id 未填写');
  if (!c.wecom || !c.wecom.bot_secret || c.wecom.bot_secret.includes('你的'))
    errors.push('wecom.bot_secret 未填写');
  if (!c.agent || !c.agent.endpoint)
    errors.push('agent.endpoint 未填写（Agent 端点 URL，Connector 将消息转发到该端点）');

  // P2P 验证（仅当启用时）
  if (c.p2p && c.p2p.enabled) {
    if (!c.p2p.signaling_server)
      errors.push('p2p.signaling_server 未填写（P2P 已启用但未指定配对服务器地址）');
  }

  return errors;
}

module.exports = { loadConfig, validateConfig };
