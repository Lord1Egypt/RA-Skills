// 云函数入口文件
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const { limit = 50 } = event;

  try {
    // 查询红包记录
    const result = await db.collection('red_packets')
      .where({
        _openid: wxContext.OPENID
      })
      .orderBy('createTime', 'desc')
      .limit(limit)
      .get();

    console.log('查询成功:', result.data.length);

    return {
      success: true,
      data: result.data,
      message: '查询成功'
    };
  } catch (err) {
    console.error('查询失败:', err);
    return {
      success: false,
      error: err.message,
      message: '查询失败'
    };
  }
};
