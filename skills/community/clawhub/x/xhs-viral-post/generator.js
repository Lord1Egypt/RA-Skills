const OpenAI = require("openai");

function parseJsonMaybe(text) {
  const raw = String(text || "").trim();
  if (!raw) {
    throw new Error("OpenAI returned empty response");
  }

  try {
    return JSON.parse(raw);
  } catch (_) {
    const m = raw.match(/\{[\s\S]*\}/);
    if (!m) {
      throw new Error("OpenAI response is not valid JSON");
    }
    return JSON.parse(m[0]);
  }
}

module.exports = async function generatePost(topic, keywords) {
  const cleanTopic = String(topic || "").trim();
  if (!cleanTopic) {
    throw new Error("Missing required input: topic");
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error("Missing OPENAI_API_KEY");
  }

  const client = new OpenAI({ apiKey });
  const kw = (Array.isArray(keywords) ? keywords : []).slice(0, 8).join("、");

  const prompt = [
    "你是资深小红书博主，擅长真实种草和高收藏笔记。",
    `主题：${cleanTopic}`,
    `可参考趋势词：${kw || "无"}`,
    "请只输出 JSON，字段必须是 title 和 content。",
    "写作硬性要求：",
    "1) title 16-24 字，避免夸张绝对化词（如最强、100%）。",
    "2) content 220-360 字，口语化，像真人分享。",
    "3) 结构包含：场景痛点 -> 具体做法(3步以内) -> 真实体感结果 -> 互动提问。",
    "4) 不写医疗/金融承诺，不写违规引流词。",
    "5) 适度加入 1-2 个 emoji，但不要堆砌。"
  ].join("\n");

  const response = await client.responses.create({
    model: "gpt-4o",
    input: prompt,
    max_output_tokens: 900
  });

  const parsed = parseJsonMaybe(response.output_text);
  const title = String(parsed.title || "").trim();
  const content = String(parsed.content || "").trim();

  if (!title || !content) {
    throw new Error("Generated post is missing title or content");
  }

  return { title, content };
};
