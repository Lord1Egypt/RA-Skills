const { ENV_ID } = require('./config');

// 统一通过微信云开发调用云函数，OPENID 由平台在云函数侧保证，无需 token
function callApi(path, method, data) {
  // 兼容前端把 query 写在 path 里的写法（如 /api/checkins?month=2026-08）
  let pathname = path;
  const query = {};
  const qi = path.indexOf('?');
  if (qi >= 0) {
    pathname = path.slice(0, qi);
    path.slice(qi + 1).split('&').forEach((pair) => {
      const idx = pair.indexOf('=');
      const k = decodeURIComponent(pair.slice(0, idx < 0 ? undefined : idx));
      const v = idx < 0 ? '' : decodeURIComponent(pair.slice(idx + 1));
      if (k) query[k] = v;
    });
  }

  return new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'api',
      data: { path: pathname, method, body: data || {}, query },
      success: (res) => {
        const result = res.result || {};
        if (result && result.error) {
          wx.showToast({ title: result.error, icon: 'none' });
          return reject(new Error(result.error));
        }
        resolve(result);
      },
      fail: (err) => {
        // 关键：打印完整错误对象，便于排障（别只打 errMsg）
        console.error('[callApi fail]', pathname, method, err);
        const msg = (err && (err.errMsg || err.message)) || '网络异常';
        wx.showToast({ title: '调用失败:' + msg, icon: 'none' });
        reject(err);
      },
    });
  });
}

// 登录：调用云函数 login，平台侧直接拿到真实 OPENID，无需 wx.login code 换 token
function login() {
  return new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'login',
      success: (res) => {
        const result = res.result || {};
        if (result && result.error) return reject(new Error(result.error));
        resolve(result.user);
      },
      fail: reject,
    });
  });
}

const api = {
  login,
  get: (path) => callApi(path, 'GET'),
  post: (path, data) => callApi(path, 'POST', data),
  put: (path, data) => callApi(path, 'PUT', data),
};

module.exports = api;
