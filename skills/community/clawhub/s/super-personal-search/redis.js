const { createClient } = require('redis');

let client;
let connected = false;

function getRedisClient() {
  if (client) {
    return client;
  }

  const redisUrl = process.env.REDIS_URL;
  if (!redisUrl) {
    throw new Error('REDIS_URL is required in environment variables.');
  }

  client = createClient({
    url: redisUrl,
  });

  client.on('error', (error) => {
    console.error('Redis client error:', error);
  });

  return client;
}

async function ensureRedisConnected() {
  const redisClient = getRedisClient();

  if (!connected) {
    await redisClient.connect();
    connected = true;
  }

  return redisClient;
}

async function saveConnection(id, data) {
  const redisClient = await ensureRedisConnected();
  await redisClient.set(`connection:${id}`, JSON.stringify(data));
}

async function getConnection(id) {
  const redisClient = await ensureRedisConnected();
  const raw = await redisClient.get(`connection:${id}`);
  return raw ? JSON.parse(raw) : null;
}

async function getAllConnections() {
  const redisClient = await ensureRedisConnected();
  const keys = await redisClient.keys('connection:*');

  if (keys.length === 0) {
    return [];
  }

  const values = await redisClient.mGet(keys);
  return values.filter(Boolean).map((value) => JSON.parse(value));
}

async function saveQueryContext(sessionId, context) {
  const redisClient = await ensureRedisConnected();
  const key = `query-context:${sessionId}`;

  await redisClient.set(key, JSON.stringify(context), {
    EX: 60 * 30,
  });
}

async function getQueryContext(sessionId) {
  const redisClient = await ensureRedisConnected();
  const raw = await redisClient.get(`query-context:${sessionId}`);
  return raw ? JSON.parse(raw) : null;
}

module.exports = {
  ensureRedisConnected,
  saveConnection,
  getConnection,
  getAllConnections,
  saveQueryContext,
  getQueryContext,
};
