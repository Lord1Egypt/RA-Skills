const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

// 登录：平台侧直接拿到真实 OPENID，无需 wx.login code 换 token、无需 mock
// 幂等建号：查不到就建，并把新用户自动加入所有公开组（避免「组里没人」）
exports.main = async () => {
  const { OPENID } = cloud.getWXContext();
  let u = (await db.collection('users').where({ openid: OPENID }).get()).data;
  if (!u.length) {
    const add = await db.collection('users').add({
      data: { openid: OPENID, nickname: '微信用户', avatarUrl: '', createdAt: new Date().toISOString() },
    });
    const pub = (await db.collection('groups').where({ type: 'public' }).get()).data;
    for (const g of pub) {
      await db.collection('group_memberships').add({ data: { openid: OPENID, groupId: g._id, role: 'member' } });
    }
    u = (await db.collection('users').doc(add._id).get()).data;
  } else {
    u = u[0];
  }
  return {
    user: { id: u._id, nickname: u.nickname, avatar_url: u.avatarUrl, created_at: u.createdAt },
  };
};
