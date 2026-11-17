const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();
const _ = db.command;

// 订阅消息模板 ID（必须与 miniprogram/utils/config.js 的 SUBSCRIBE_TEMPLATE_ID 一致）
const TEMPLATE_ID = '__TEMPLATE_ID__';

// 每日由 config.json 定时触发器唤起：给开启提醒且订阅额度充足的人推送提醒
exports.main = async () => {
  const reminders = (await db.collection('reminders').where({ enabled: 1 }).get()).data;
  let pushed = 0;
  let skipped = 0;

  for (const r of reminders) {
    const g = (await db.collection('subscribe_grants').where({ openid: r.openid }).get()).data;
    const remain = g.length ? g[0].remain : 0;
    if (remain <= 0) {
      skipped++;
      continue;
    }
    try {
      await cloud.openapi.subscribeMessage.send({
        touser: r.openid,
        templateId: TEMPLATE_ID,
        page: '/pages/index/index',
        // ⚠️ 字段名（thing1/time2 等）必须与你 MP 后台申请的模板关键词严格一一对应，
        //    请在后台「订阅消息-我的模板」里核对关键词顺序后修改此处
        data: {
          thing1: { value: '今天还没打卡哦' },
          time2: { value: r.time || '20:00' },
        },
      });
      await db.collection('subscribe_grants').where({ openid: r.openid }).update({ data: { remain: _.inc(-1) } });
      pushed++;
    } catch (e) {
      console.error('push fail', r.openid, e);
      skipped++;
    }
  }
  return { pushed, skipped };
};
