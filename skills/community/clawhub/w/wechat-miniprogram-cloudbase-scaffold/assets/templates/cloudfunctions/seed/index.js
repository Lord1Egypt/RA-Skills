const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

const DEFAULT_GROUPS = ['默认公开组'];

// ⚠️ 集合清单必须与代码实际用到的集合一一核对（漏一个会报 collection not exists）
const ALL_COLLECTIONS = [
  'users',
  'groups',
  'group_memberships',
  'checkins',
  'reminders',
  'subscribe_grants',
  'group_events',
];

// 幂等建集合：先 add 占位再删（首次 add 会自动创建集合）
async function ensureCollection(name) {
  try {
    const r = await db.collection(name).add({ data: { _init: true } });
    await db.collection(name).doc(r._id).remove();
  } catch (e) {
    // 集合已存在则忽略
  }
}

// 幂等预置种子数据（手动触发一次即可：DevTools 右键「测试」或 tcb fn invoke seed）
exports.main = async () => {
  for (const c of ALL_COLLECTIONS) await ensureCollection(c);

  const cnt = (await db.collection('groups').count()).total;
  if (cnt > 0) return { skipped: true, count: cnt };
  for (const name of DEFAULT_GROUPS) {
    await db.collection('groups').add({
      data: { name, type: 'public', createdBy: 'system', createdAt: new Date().toISOString() },
    });
  }
  const n = (await db.collection('groups').count()).total;
  return { seeded: true, count: n };
};
