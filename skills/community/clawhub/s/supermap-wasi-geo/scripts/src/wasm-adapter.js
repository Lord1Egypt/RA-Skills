/**
 * Node.js 环境适配器
 * 模拟浏览器环境所需的 API，使 UGCWasmAll.js 能在 Node.js 中运行
 */

const path = require('path');

// 标记环境是否已初始化
let envInitialized = false;

/**
 * 初始化浏览器环境模拟
 */
function initBrowserEnv() {
  if (envInitialized) return;
  envInitialized = true;

  // 模拟完整的 document 对象
  if (typeof global.document === 'undefined') {
    global.document = {
      currentScript: {
        src: __filename,
        ownerDocument: {}
      },
      createElement: (tag) => {
        if (tag === 'script') {
          return {
            src: '',
            onload: null,
            onerror: null,
            readyState: 'complete'
          };
        }
        return {};
      },
      getElementById: () => null,
      getElementsByTagName: (tag) => {
        if (tag === 'script') return [{ src: __filename }];
        if (tag === 'head') return [{}];
        return [];
      },
      head: {},
      body: {},
      documentElement: {},
      createEvent: () => ({ initEvent: () => {} }),
      dispatchEvent: () => true
    };
  }

  // 模拟 self 对象（Worker 环境）
  if (typeof global.self === 'undefined') {
    global.self = global;
  }

  // 模拟 window 对象
  if (typeof global.window === 'undefined') {
    global.window = global;
  }

  // 模拟 XMLHttpRequest
  if (typeof global.XMLHttpRequest === 'undefined') {
    global.XMLHttpRequest = function() {
      this.open = () => {};
      this.send = () => {
        this.readyState = 4;
        this.status = 200;
        if (this.onload) this.onload({ target: { response: new ArrayBuffer(0) } });
      };
      this.setRequestHeader = () => {};
      this.getAllResponseHeaders = () => '';
      this.getResponseHeader = () => null;
      this.abort = () => {};
    };
  }
}

// 加载 WASM 模块
let wasmInstance = null;
let initPromise = null;

/**
 * 初始化 WASM 模块
 * @returns {Promise<Object>} 初始化后的 Module 对象
 */
async function initWasm() {
  // 如果已经初始化，直接返回
  if (wasmInstance && wasmInstance.HEAP8) {
    return wasmInstance;
  }

  // 如果正在初始化，返回同一个 Promise
  if (initPromise) {
    return initPromise;
  }

  initPromise = (async () => {
    try {
      // 初始化浏览器环境
      initBrowserEnv();

      // 加载模块
      const ugcModule = require('../wasm/UGCWasmAll.js');

      // WASM 模块需要异步初始化
      // 等待 HEAP8 可用（表示 WASM 已加载完成）
      await new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 50; // 最多等待 5 秒
        
        const check = () => {
          attempts++;
          if (ugcModule.HEAP8) {
            resolve();
          } else if (attempts >= maxAttempts) {
            reject(new Error('WASM 模块初始化超时'));
          } else {
            setTimeout(check, 100);
          }
        };
        check();
      });

      wasmInstance = ugcModule;

      // 验证模块是否正确加载
      if (!wasmInstance.HEAP8 || typeof wasmInstance._malloc !== 'function') {
        throw new Error('WASM 模块加载失败：缺少必要的导出函数');
      }

      return wasmInstance;
    } catch (error) {
      initPromise = null;
      throw error;
    }
  })();

  return initPromise;
}

/**
 * 获取已初始化的 WASM 模块实例
 * @returns {Object|null} Module 对象或 null
 */
function getWasmInstance() {
  return wasmInstance;
}

/**
 * 检查模块是否已初始化
 * @returns {boolean}
 */
function isInitialized() {
  return wasmInstance !== null;
}

module.exports = {
  initWasm,
  getWasmInstance,
  isInitialized
};
