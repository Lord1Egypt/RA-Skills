import { registerSlonAideTools } from './src/tools.js';
import { registerBridgeTools } from './src/bridge.js';

const plugin = {
  id: 'slonaide',
  name: 'SlonAide',
  description: 'SlonAide 录音笔记管理插件',
  register(api) {
    registerSlonAideTools(api);
    registerBridgeTools(api);
  }
};

export default plugin;