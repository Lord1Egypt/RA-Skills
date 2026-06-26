App({
  globalData: {
    userInfo: null,
    redPacketList: []
  },
  
  onLaunch() {
    // 初始化云开发环境
    wx.cloud.init({
      env: 'card-native-2gvohkdhd8a64b2d',
      traceUser: true
    });
    
    // 获取用户信息
    this.getUserInfo();
  },
  
  getUserInfo() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        this.globalData.userInfo = res.userInfo;
        console.log('用户信息:', res.userInfo);
      }
    });
  }
})
