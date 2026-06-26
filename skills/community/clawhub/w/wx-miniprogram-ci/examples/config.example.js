/**
 * wxmini-ci 配置文件示例
 *
 * 使用方式：
 * 1. 将此文件复制到项目根目录，重命名为 wxmini-ci.config.js
 * 2. 或复制到 ~/.wxmini-ci.config.js 作为全局配置
 * 3. 命令行参数会覆盖配置文件中的设置
 *
 * 配置优先级（从高到低）：
 * 1. 命令行参数
 * 2. 环境变量 (WXMINI_*)
 * 3. 配置文件 projects 映射中的指定项目
 * 4. 顶层配置
 * 5. 默认值
 */

const path = require('path');
const os = require('os');

module.exports = {
  // 默认项目（可选，不指定时使用 default 或第一个项目）
  default: 'project-a',
  
  // 多项目配置
  projects: {
    'project-a': {
      appid: 'YOUR_APPID',
      privateKeyPath: '~/.credentials/private.YOUR_APPID.key',
      projectPath: '/path/to/project-a',
      type: 'miniProgram'
    },
    'project-b': {
      appid: 'YOUR_APPID_B',
      privateKeyPath: '~/.credentials/private.YOUR_APPID_B.key',
      projectPath: '/path/to/project-b',
      type: 'miniProgram'
    }
  },
  
  // 编译设置（可选）
  setting: {
    es6: true,              // ES6 -> ES5
    es7: true,              // 增强编译
    minify: true,           // 压缩代码
    // minifyJS: true,      // 压缩 JS
    // minifyWXML: true,    // 压缩 WXML
    // minifyWXSS: true,    // 压缩 WXSS
    // codeProtect: true,   // 代码保护
    // autoPrefixWXSS: true // 样式自动补全
  }
};
