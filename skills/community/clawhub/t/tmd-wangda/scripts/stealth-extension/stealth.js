// stealth.js — 在 document_start 时注入到页面上下文 (MAIN world)
// 对抗各类 anti-devtools / anti-automation 检测

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════
  // 1. 隐藏自动化标志
  // ═══════════════════════════════════════════════════════════════
  try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch(e) {}
  try { Object.defineProperty(window, 'outerWidth',   { get: () => window.innerWidth }); } catch(e) {}
  try { Object.defineProperty(window, 'outerHeight',  { get: () => window.innerHeight }); } catch(e) {}
  try { Object.defineProperty(navigator, 'plugins',   { get: () => [1,2,3,4,5] }); } catch(e) {}
  try { Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN','zh','en'] }); } catch(e) {}

  // ═══════════════════════════════════════════════════════════════
  // 2. Hook performance.now / Date.now：截断时间增量 ≤ 16ms
  //    即使 debugger 语句暂停了几秒，返回的时间差仍然极小
  // ═══════════════════════════════════════════════════════════════
  const _perfNow = performance.now.bind(performance);
  const _dateNow = Date.now.bind(Date);
  let pReal = _perfNow(), pFake = pReal;
  let dReal = _dateNow(), dFake = dReal;

  performance.now = function() {
    const r = _perfNow();
    pFake += Math.min(r - pReal, 16);
    pReal = r;
    return pFake;
  };

  Date.now = function() {
    const r = _dateNow();
    dFake += Math.min(r - dReal, 16);
    dReal = r;
    return dFake;
  };

  // ═══════════════════════════════════════════════════════════════
  // 3. 重写 Function 构造器：剥离 debugger 关键字
  //    对抗 new Function("debugger") 及各种混淆变体
  // ═══════════════════════════════════════════════════════════════
  const _Function = Function;
  const handler = {
    construct(target, args) {
      if (args.length > 0) {
        const last = args.length - 1;
        if (typeof args[last] === 'string') {
          args[last] = args[last].replace(/\bdebugger\b/g, '');
        }
      }
      return Reflect.construct(target, args);
    },
    apply(target, thisArg, args) {
      if (args.length > 0) {
        const last = args.length - 1;
        if (typeof args[last] === 'string') {
          args[last] = args[last].replace(/\bdebugger\b/g, '');
        }
      }
      return Reflect.apply(target, thisArg, args);
    }
  };
  try {
    window.Function = new Proxy(_Function, handler);
    window.Function.prototype = _Function.prototype;
    window.Function.prototype.constructor = window.Function;
  } catch(e) {}

  // ═══════════════════════════════════════════════════════════════
  // 4. 拦截 eval：同样剥离 debugger
  // ═══════════════════════════════════════════════════════════════
  const _eval = window.eval;
  window.eval = function(code) {
    if (typeof code === 'string') {
      code = code.replace(/\bdebugger\b/g, '');
    }
    return _eval.call(this, code);
  };
  window.eval.toString = () => 'function eval() { [native code] }';

  // ═══════════════════════════════════════════════════════════════
  // 5. 拦截 setInterval / setTimeout：过滤包含检测逻辑的回调
  // ═══════════════════════════════════════════════════════════════
  const _setInterval = window.setInterval.bind(window);
  const _setTimeout  = window.setTimeout.bind(window);

  function isSuspicious(fn) {
    try {
      const src = typeof fn === 'function' ? fn.toString() : String(fn);
      // 匹配 debugger、混淆函数名 _0x...、devtools 检测关键字
      return /\bdebugger\b|devtool|eruda|firebug/i.test(src);
    } catch(e) { return false; }
  }

  window.setInterval = function(fn, delay) {
    if (isSuspicious(fn)) return _setInterval(function(){}, 2147483647);
    return _setInterval.apply(null, arguments);
  };
  window.setInterval.toString = () => 'function setInterval() { [native code] }';

  window.setTimeout = function(fn, delay) {
    if (isSuspicious(fn)) return _setTimeout(function(){}, 2147483647);
    return _setTimeout.apply(null, arguments);
  };
  window.setTimeout.toString = () => 'function setTimeout() { [native code] }';

  // ═══════════════════════════════════════════════════════════════
  // 6. 阻止页面跳转到 about:blank 或被 document.write/open 清空
  // ═══════════════════════════════════════════════════════════════
  function isBlank(url) {
    return /^about:/i.test(String(url).trim());
  }

  // location.assign / location.replace
  ['assign', 'replace'].forEach(function(m) {
    const orig = location[m].bind(location);
    try {
      Object.defineProperty(location, m, {
        value: function(u) { return isBlank(u) ? undefined : orig(u); },
        writable: false, configurable: false
      });
    } catch(e) {}
  });

  // location.href setter
  try {
    const hrefDesc = Object.getOwnPropertyDescriptor(window.location, 'href');
    if (hrefDesc && hrefDesc.set) {
      Object.defineProperty(window.location, 'href', {
        get: hrefDesc.get,
        set: function(v) { return isBlank(v) ? undefined : hrefDesc.set.call(window.location, v); }
      });
    }
  } catch(e) {}

  // document.open / document.write
  const _docWrite = document.write.bind(document);
  document.write = function() {
    // 阻止空内容 write（用于清空页面）
    if (arguments.length === 0) return;
    if (arguments.length === 1 && /^\s*$/.test(arguments[0])) return;
    return _docWrite.apply(document, arguments);
  };
  document.write.toString = () => 'function write() { [native code] }';

  document.open = function() { return document; };
  document.open.toString = () => 'function open() { [native code] }';

  // ═══════════════════════════════════════════════════════════════
  // 7. 阻止通过 innerHTML 清空 body
  // ═══════════════════════════════════════════════════════════════
  const _bodyInnerHTMLDesc = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
  if (_bodyInnerHTMLDesc) {
    const _set = _bodyInnerHTMLDesc.set;
    Object.defineProperty(Element.prototype, 'innerHTML', {
      get: _bodyInnerHTMLDesc.get,
      set: function(val) {
        // 如果是 body 或 html 且设置为空，阻止
        if ((this === document.body || this === document.documentElement) && /^\s*$/.test(val)) {
          return;
        }
        return _set.call(this, val);
      },
      configurable: true
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // 8. console 方法保护（某些检测利用 console.log 的 getter）
  // ═══════════════════════════════════════════════════════════════
  const _console = {};
  ['log','warn','error','info','debug','table','trace','dir','group','groupEnd','time','timeEnd','assert','count'].forEach(function(m) {
    if (console[m]) _console[m] = console[m].bind(console);
  });

  // 防止 console 被重写为检测陷阱
  try {
    Object.defineProperty(window, 'console', {
      get: function() { return _console; },
      set: function() { /* 忽略重写 */ },
      configurable: false
    });
  } catch(e) {}

})();
