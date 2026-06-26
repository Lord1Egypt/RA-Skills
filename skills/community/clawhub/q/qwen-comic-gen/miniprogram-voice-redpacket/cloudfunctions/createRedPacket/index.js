// 云函数入口文件
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const { recipient, amount, message } = event;

  try {
    // 创建红包记录
    const result = await db.collection('red_packets').add({
      data: {
        _openid: wxContext.OPENID,
        recipient: recipient,
        amount: parseInt(amount),
        message: message,
        status: 'sent',
        createTime: db.serverDate()
      }
    });

    console.log('创建成功:', result);

    return {
      success: true,
      data: result,
      message: '红包创建成功'
    };
  } catch (err) {
    console.error('创建失败:', err);
    return {
      success: false,
      error: err.message,
      message: '红包创建失败'
    };
  }
};
