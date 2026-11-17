const { cloud, db, _ } = require('./db');
const { MILESTONES, todayStr } = require('./services/streak');
const { recomputeStats, getStats } = require('./services/stats');

// ============ 视图函数：把 DB 内部字段转成对外 API 字段（camelCase DB → snake_case API） ============
function userView(u) {
  if (!u) return null;
  return { id: u._id, nickname: u.nickname, avatar_url: u.avatarUrl, created_at: u.createdAt };
}
function checkinView(c) {
  return {
    id: c._id,
    user_id: c.openid,
    group_id: c.groupId,
    date: c.date,
    skipped: c.skipped,
    note: c.note,
    created_at: c.createdAt,
  };
}
async function groupView(g) {
  if (!g) return null;
  const cnt = await db.collection('group_memberships').where({ groupId: g._id }).count();
  return {
    id: g._id,
    name: g.name,
    type: g.type,
    created_by: g.createdBy,
    created_at: g.createdAt,
    member_count: cnt.total,
  };
}

// ============ handlers ============
async function me(ctx) {
  let u = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data[0];
  if (!u) {
    // 兜底幂等建号：页面可能在 login 云函数建号前就请求 me，这里补建，消除「用户不存在」竞争
    try {
      const add = await db.collection('users').add({
        data: { openid: ctx.OPENID, nickname: '微信用户', avatarUrl: '', createdAt: new Date().toISOString() },
      });
      const pub = (await db.collection('groups').where({ type: 'public' }).get()).data;
      for (const g of pub) {
        await db.collection('group_memberships').add({ data: { openid: ctx.OPENID, groupId: g._id, role: 'member' } });
      }
      u = (await db.collection('users').doc(add._id).get()).data;
    } catch (e) {
      // 并发下 login 可能已建号，重查一次兜底
      u = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data[0];
    }
  }
  if (!u) return { error: '用户不存在' };
  const stats = await getStats(ctx.OPENID);
  const c = (await db.collection('checkins').where({ openid: ctx.OPENID, date: todayStr() }).get()).data;
  const r = (await db.collection('reminders').where({ openid: ctx.OPENID }).get()).data;
  const rem = r.length ? r[0] : { time: '20:00', enabled: 0 };
  return {
    user: userView(u),
    stats: {
      current_streak: stats.current_streak,
      longest_streak: stats.longest_streak,
      total_days: stats.total_days,
    },
    todayCheckin: c.length ? checkinView(c[0]) : null,
    reminder: { time: rem.time, enabled: rem.enabled },
  };
}

async function updateMe(ctx) {
  const set = {};
  if (ctx.body.nickname) set.nickname = String(ctx.body.nickname).slice(0, 30);
  if (ctx.body.avatarUrl) set.avatarUrl = String(ctx.body.avatarUrl);
  if (Object.keys(set).length) {
    const u = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data;
    if (u.length) await db.collection('users').doc(u[0]._id).update({ data: set });
  }
  const u2 = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data[0];
  return { user: userView(u2) };
}

async function setReminder(ctx) {
  const { time = '20:00', enabled = true } = ctx.body || {};
  if (!/^\d{2}:\d{2}$/.test(time)) return { error: 'time 格式应为 HH:MM' };
  const r = (await db.collection('reminders').where({ openid: ctx.OPENID }).get()).data;
  const data = { time, enabled: enabled ? 1 : 0 };
  if (r.length) await db.collection('reminders').doc(r[0]._id).update({ data });
  else await db.collection('reminders').add({ data: { openid: ctx.OPENID, ...data } });
  return { ok: true };
}

// 订阅授权一次，额度 +1（前端 requestSubscribeMessage 成功后调用）
async function subscribeGrant(ctx) {
  const g = (await db.collection('subscribe_grants').where({ openid: ctx.OPENID }).get()).data;
  if (g.length) await db.collection('subscribe_grants').doc(g[0]._id).update({ data: { remain: _.inc(1) } });
  else await db.collection('subscribe_grants').add({ data: { openid: ctx.OPENID, remain: 1 } });
  const g2 = (await db.collection('subscribe_grants').where({ openid: ctx.OPENID }).get()).data[0];
  return { ok: true, remain: g2.remain };
}

async function listGroups(ctx) {
  const pub = (await db.collection('groups').where({ type: 'public' }).orderBy('createdAt', 'asc').get()).data;
  const publicGroups = [];
  for (const g of pub) publicGroups.push(await groupView(g));

  const myMem = (await db.collection('group_memberships').where({ openid: ctx.OPENID }).get()).data;
  const myGroups = [];
  for (const m of myMem) {
    const g = (await db.collection('groups').doc(m.groupId).get()).data;
    if (g) {
      const gv = await groupView(g);
      gv.role = m.role;
      myGroups.push(gv);
    }
  }
  return { publicGroups, myGroups };
}

async function createGroup(ctx) {
  const { name, type = 'public' } = ctx.body || {};
  if (!name || !String(name).trim()) return { error: '组名不能为空' };
  if (!['public', 'private'].includes(type)) return { error: 'type 只能是 public / private' };
  const add = await db.collection('groups').add({
    data: { name: String(name).trim(), type, createdBy: ctx.OPENID, createdAt: new Date().toISOString() },
  });
  await db.collection('group_memberships').add({ data: { openid: ctx.OPENID, groupId: add._id, role: 'owner' } });
  const g = (await db.collection('groups').doc(add._id).get()).data;
  return { group: await groupView(g) };
}

async function joinGroup(ctx, id) {
  const g = (await db.collection('groups').doc(id).get()).data;
  if (!g) return { error: '组不存在' };
  const existing = (await db.collection('group_memberships').where({ openid: ctx.OPENID, groupId: id }).get()).data;
  if (existing.length) return { error: '已经在组里了' };
  await db.collection('group_memberships').add({ data: { openid: ctx.OPENID, groupId: id, role: 'member' } });
  return { ok: true };
}

async function createCheckin(ctx) {
  const { skipped = false, note = null, groupId = null } = ctx.body || {};
  const today = todayStr();
  const existing = (await db.collection('checkins').where({ openid: ctx.OPENID, date: today }).get()).data;
  if (existing.length) return { error: '今天已经打过卡了', checkin: checkinView(existing[0]) };

  const add = await db.collection('checkins').add({
    data: {
      openid: ctx.OPENID,
      groupId: groupId || null,
      date: today,
      skipped: skipped ? 1 : 0,
      note,
      createdAt: new Date().toISOString(),
    },
  });
  const c = (await db.collection('checkins').doc(add._id).get()).data;
  const stats = await recomputeStats(ctx.OPENID);

  // 里程碑：恰好达到 7/21/100 时广播庆祝（按需扩展）
  let milestone = null;
  if (!skipped && MILESTONES.includes(stats.currentStreak)) {
    milestone = stats.currentStreak;
    const mem = (await db.collection('group_memberships').where({ openid: ctx.OPENID }).get()).data;
    for (const m of mem) {
      await db.collection('group_events').add({
        data: {
          groupId: m.groupId,
          openid: ctx.OPENID,
          type: 'milestone',
          payload: JSON.stringify({ streak: milestone }),
          createdAt: new Date().toISOString(),
        },
      });
    }
  }
  return {
    ok: true,
    skipped,
    checkin: checkinView(c),
    currentStreak: stats.currentStreak,
    longestStreak: stats.longestStreak,
    totalDays: stats.totalDays,
    milestone,
  };
}

async function listCheckins(ctx) {
  const month = /^\d{4}-\d{2}$/.test(ctx.query.month || '') ? ctx.query.month : todayStr().slice(0, 7);
  const rows = (await db.collection('checkins')
    .where({ openid: ctx.OPENID, date: db.RegExp({ regexp: `^${month}` }) })
    .orderBy('date', 'asc')
    .get()).data;
  const checkins = rows.map((c) => ({ date: c.date, skipped: c.skipped, note: c.note }));
  return { month, checkins };
}

// ============ 路由：单函数 REST 分发 ============
exports.main = async (event) => {
  const { OPENID } = cloud.getWXContext();
  const { path = '', method = 'GET', body = {}, query = {} } = event;
  const ctx = { OPENID, body, query };

  try {
    if (path === '/api/users/me') {
      if (method === 'GET') return await me(ctx);
      if (method === 'PUT') return await updateMe(ctx);
    }
    if (path === '/api/users/me/reminder' && method === 'PUT') return await setReminder(ctx);
    if (path === '/api/users/me/subscribe-grant' && method === 'POST') return await subscribeGrant(ctx);

    if (path === '/api/groups') {
      if (method === 'GET') return await listGroups(ctx);
      if (method === 'POST') return await createGroup(ctx);
    }
    let m;
    if ((m = path.match(/^\/api\/groups\/([^/]+)\/join$/)) && method === 'POST') return await joinGroup(ctx, m[1]);

    if (path === '/api/checkins') {
      if (method === 'POST') return await createCheckin(ctx);
      if (method === 'GET') return await listCheckins(ctx);
    }

    return { error: '接口不存在', path, method };
  } catch (e) {
    console.error(e);
    return { error: e.message || '服务器错误' };
  }
};
