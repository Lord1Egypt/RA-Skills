const vm = require("vm");

function stripScriptTags(jsLike) {
  return String(jsLike)
    .replace(/<script[^>]*>/gi, "")
    .replace(/<\/script>/gi, "")
    .trim();
}

/**
 * 执行“跳转解密脚本”，捕获其写入的最终 URL。
 * 兼容：location.href / window.href 的 setter、以及 bracket 访问。
 */
function decodeRedirectUrlFromJs(jsLike) {
  const jsContent = stripScriptTags(jsLike);
  if (!jsContent) return null;

  const wrapperCode = `
let capturedUrl = null;

let _locationObj = {};
Object.defineProperty(_locationObj, 'href', {
  set(value) { if (!capturedUrl && value) capturedUrl = value; },
  configurable: true
});
_locationObj.assign = function(value) { if (!capturedUrl && value) capturedUrl = value; };
_locationObj.replace = function(value) { if (!capturedUrl && value) capturedUrl = value; };

Object.defineProperty(globalThis, 'location', {
  get() { return _locationObj; },
  set(value) { if (!capturedUrl && value) capturedUrl = value; _locationObj = value; },
  configurable: true
});

const window = {};
Object.defineProperty(window, 'href', {
  set(value) { if (!capturedUrl && value) capturedUrl = value; },
  configurable: true
});
window.location = globalThis.location;

${jsContent}

capturedUrl;
`;

  const sandbox = {};
  const context = vm.createContext(sandbox, {
    name: "decode-redirect-sandbox",
    origin: "file:///",
  });
  try {
    const captured = vm.runInContext(wrapperCode, context, {
      timeout: 8000,
      displayErrors: false,
      breakOnSigint: true,
    });
    return typeof captured === "string" && captured.trim() ? captured.trim() : null;
  } catch {
    return null;
  }
}

module.exports = { decodeRedirectUrlFromJs };

