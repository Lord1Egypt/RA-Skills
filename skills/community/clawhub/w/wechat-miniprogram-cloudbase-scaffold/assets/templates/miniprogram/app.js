const api = require('./utils/request');
const { ENV_ID } = require('./utils/config');

App({
  globalData: {
    user: null,
    // 当前所在组（组页/广播用），null 表示未选择
    currentGroupId: null,
  },

  onLaunch() {
    if (!wx.cloud) {
      console.error('当前基础库不支持云开发，请使用 2.2.3 以上基础库');
      return;
    }
    // 初始化云开发环境（env ID 在 utils/config.js）
    wx.cloud.init({
      env: ENV_ID,
      traceUser: true,
    });

    api
      .login()
      .then((user) => {
        this.globalData.user = user;
        if (this.loginReadyCallback) this.loginReadyCallback(user);
      })
      .catch((err) => {
        console.error('登录失败', err);
      });
  },
});
