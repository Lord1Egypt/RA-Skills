import { createClient } from "redis";
import OpenAI from "openai";

const REDIS_URL = process.env.REDIS_URL;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const SIMILARITY_THRESHOLD = parseFloat(process.env.SEMANTIC_CACHE_THRESHOLD || "0.80");
const CACHE_TTL = parseInt(process.env.SEMANTIC_CACHE_TTL || "86400");
const INDEX_NAME = "idx:semantic_cache";
const KEY_PREFIX = "cache:";
const VECTOR_DIM = 1536;

if (!REDIS_URL) {
  console.error("Error: REDIS_URL environment variable is required");
  process.exit(1);
}
if (!OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY environment variable is required");
  process.exit(1);
}

const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

let redisClient = null;

async function getRedis() {
  if (redisClient && redisClient.isOpen) return redisClient;
  redisClient = createClient({ url: REDIS_URL });
  redisClient.on("error", (err) => console.error("Redis error:", err));
  await redisClient.connect();
  return redisClient;
}

async function embed(text) {
  const response = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
  });
  return response.data[0].embedding;
}

function float32Buffer(arr) {
  return Buffer.from(new Float32Array(arr).buffer);
}

async function ensureIndex() {
  const redis = await getRedis();
  try {
    await redis.ft.info(INDEX_NAME);
  } catch {
    await redis.ft.create(
      INDEX_NAME,
      {
        query_text: { type: "TEXT" },
        response_text: { type: "TEXT" },
        embedding: {
          type: "VECTOR",
          ALGORITHM: "HNSW",
          TYPE: "FLOAT32",
          DIM: VECTOR_DIM,
          DISTANCE_METRIC: "COSINE",
        },
        created_at: { type: "NUMERIC" },
        hit_count: { type: "NUMERIC" },
        model: { type: "TAG" },
      },
      {
        ON: "HASH",
        PREFIX: KEY_PREFIX,
      }
    );
    console.log("Created vector search index:", INDEX_NAME);
  }
}

async function store(query, response, model = "unknown") {
  const redis = await getRedis();
  await ensureIndex();

  const vector = await embed(query);
  const key = `${KEY_PREFIX}${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

  await redis.hSet(key, {
    query_text: query,
    response_text: response,
    embedding: float32Buffer(vector),
    created_at: Date.now(),
    hit_count: 0,
    model,
  });

  if (CACHE_TTL > 0) {
    await redis.expire(key, CACHE_TTL);
  }

  console.log(`Cached: "${query.substring(0, 60)}..." -> ${key}`);
  return key;
}

async function lookup(query) {
  const redis = await getRedis();
  await ensureIndex();

  const vector = await embed(query);
  const startTime = Date.now();

  const results = await redis.ft.search(INDEX_NAME, `*=>[KNN 1 @embedding $BLOB AS score]`, {
    PARAMS: { BLOB: float32Buffer(vector) },
    SORTBY: "score",
    LIMIT: { from: 0, size: 1 },
    RETURN: ["query_text", "response_text", "score", "hit_count", "model", "created_at"],
    DIALECT: 2,
  });

  const lookupMs = Date.now() - startTime;

  if (results.total === 0) {
    return { hit: false, lookupMs };
  }

  const doc = results.documents[0];
  const similarity = 1 - parseFloat(doc.value.score);

  if (similarity < SIMILARITY_THRESHOLD) {
    return {
      hit: false,
      lookupMs,
      closestSimilarity: similarity,
      closestQuery: doc.value.query_text,
    };
  }

  // Increment hit count
  await redis.hIncrBy(doc.id, "hit_count", 1);

  return {
    hit: true,
    response: doc.value.response_text,
    similarity,
    originalQuery: doc.value.query_text,
    model: doc.value.model,
    hitCount: parseInt(doc.value.hit_count) + 1,
    lookupMs,
  };
}

async function query(question) {
  const cached = await lookup(question);

  if (cached.hit) {
    console.log(`\nCache HIT (${cached.similarity.toFixed(3)} similarity, ${cached.lookupMs}ms)`);
    console.log(`Original query: "${cached.originalQuery}"`);
    console.log(`Hit count: ${cached.hitCount}`);
    console.log(`\nResponse:\n${cached.response}`);
    return cached;
  }

  console.log(`\nCache MISS (${cached.lookupMs}ms lookup)`);
  if (cached.closestSimilarity) {
    console.log(`Closest match: "${cached.closestQuery}" (${cached.closestSimilarity.toFixed(3)} similarity, below ${SIMILARITY_THRESHOLD} threshold)`);
  }

  console.log("Calling OpenAI...");
  const startTime = Date.now();
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: question }],
    max_tokens: 1000,
  });

  const response = completion.choices[0].message.content;
  const apiMs = Date.now() - startTime;
  const tokens = completion.usage?.total_tokens || 0;

  await store(question, response, "gpt-4o-mini");

  console.log(`API response (${apiMs}ms, ${tokens} tokens):`);
  console.log(`\nResponse:\n${response}`);

  return { hit: false, response, apiMs, tokens };
}

async function stats() {
  const redis = await getRedis();
  await ensureIndex();

  const info = await redis.ft.info(INDEX_NAME);
  const keys = await redis.keys(`${KEY_PREFIX}*`);

  let totalHits = 0;
  let oldestEntry = Infinity;
  let newestEntry = 0;

  for (const key of keys) {
    const hitCount = await redis.hGet(key, "hit_count");
    const createdAt = await redis.hGet(key, "created_at");
    totalHits += parseInt(hitCount || "0");
    const ts = parseInt(createdAt || "0");
    if (ts < oldestEntry) oldestEntry = ts;
    if (ts > newestEntry) newestEntry = ts;
  }

  console.log("\nSemantic Cache Stats");
  console.log("====================");
  console.log(`Cached entries: ${keys.length}`);
  console.log(`Total cache hits: ${totalHits}`);
  console.log(`Index docs: ${info.numDocs}`);
  console.log(`Similarity threshold: ${SIMILARITY_THRESHOLD}`);
  console.log(`TTL: ${CACHE_TTL}s`);
  if (keys.length > 0) {
    console.log(`Oldest entry: ${new Date(oldestEntry).toISOString()}`);
    console.log(`Newest entry: ${new Date(newestEntry).toISOString()}`);
  }

  return { entries: keys.length, totalHits };
}

async function clear() {
  const redis = await getRedis();
  const keys = await redis.keys(`${KEY_PREFIX}*`);
  if (keys.length > 0) {
    await redis.del(keys);
  }
  try {
    await redis.ft.dropIndex(INDEX_NAME);
  } catch {}
  console.log(`Cleared ${keys.length} cached entries and dropped index`);
}

async function test() {
  console.log("Running semantic cache test...\n");

  // Store
  console.log("1. Storing: 'What is the capital of France?'");
  await store("What is the capital of France?", "The capital of France is Paris.", "test");

  // Exact match
  console.log("\n2. Looking up: 'What is the capital of France?' (exact)");
  const exact = await lookup("What is the capital of France?");
  console.log(`   Hit: ${exact.hit}, Similarity: ${exact.similarity?.toFixed(3)}, Time: ${exact.lookupMs}ms`);

  // Semantic match
  console.log("\n3. Looking up: 'What's France's capital city?' (semantic)");
  const semantic = await lookup("What's France's capital city?");
  console.log(`   Hit: ${semantic.hit}, Similarity: ${semantic.similarity?.toFixed(3)}, Time: ${semantic.lookupMs}ms`);

  // Different question
  console.log("\n4. Looking up: 'How do I make pasta?' (different)");
  const different = await lookup("How do I make pasta?");
  console.log(`   Hit: ${different.hit}, Closest similarity: ${different.closestSimilarity?.toFixed(3)}, Time: ${different.lookupMs}ms`);

  // Stats
  await stats();

  // Cleanup
  await clear();
  console.log("\nTest complete!");

  const redis = await getRedis();
  await redis.quit();
}

// CLI
const [command, ...args] = process.argv.slice(2);

switch (command) {
  case "store":
    await store(args[0], args[1], args[2]);
    (await getRedis()).quit();
    break;
  case "lookup":
    await lookup(args[0]);
    (await getRedis()).quit();
    break;
  case "query":
    await query(args.join(" "));
    (await getRedis()).quit();
    break;
  case "stats":
    await stats();
    (await getRedis()).quit();
    break;
  case "clear":
    await clear();
    (await getRedis()).quit();
    break;
  case "test":
    await test();
    break;
  default:
    console.log("Usage: node cache.js <store|lookup|query|stats|clear|test> [args]");
    console.log("");
    console.log("Commands:");
    console.log("  store <query> <response> [model]  Cache a query-response pair");
    console.log("  lookup <query>                    Check cache for similar query");
    console.log("  query <question>                  Check cache, call LLM on miss, cache result");
    console.log("  stats                             Show cache statistics");
    console.log("  clear                             Clear all cached entries");
    console.log("  test                              Run end-to-end test");
}
