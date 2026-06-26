const axios = require("axios");
const getTrendingKeywords = require("./trending");
const generatePost = require("./generator");
const rankHashtags = require("./hashtagRanker");
const generateCoverPrompt = require("./coverPrompt");
const buildStrategy = require("./strategy");

const SKILLPAY_ID = "66d32381-4e78-4593-9309-63576e85a8b7";
const PRICE_USDT = 0.05;

async function chargeSkillPay(input) {
  const skillPayKey = process.env.SKILLPAY_KEY;
  if (!skillPayKey) {
    throw new Error("Missing SKILLPAY_KEY");
  }

  const endpoint = process.env.SKILLPAY_ENDPOINT || "https://api.skillpay.me/v1/charges";

  const payload = {
    skillId: SKILLPAY_ID,
    amount: PRICE_USDT,
    currency: "USDT",
    unit: "call",
    input: {
      topic: String(input.topic || "").slice(0, 120)
    },
    timestamp: new Date().toISOString()
  };

  await axios.post(endpoint, payload, {
    headers: {
      Authorization: `Bearer ${skillPayKey}`,
      "Content-Type": "application/json"
    },
    timeout: 10000
  });
}

module.exports = async function run(input) {
  const topic = (input && input.topic ? String(input.topic) : "").trim();
  if (!topic) {
    throw new Error("Missing required input: topic");
  }

  // Enforce paid usage: billing must succeed before generation.
  await chargeSkillPay({ topic });

  const trending = await getTrendingKeywords(topic);
  const keywords = Array.isArray(trending.keywords) ? trending.keywords : [];

  const post = await generatePost(topic, keywords);
  const title = String(post.title || "").trim();
  const content = String(post.content || "").trim();

  const hashtags = await rankHashtags(topic, keywords, title, content);
  const coverPrompt = await generateCoverPrompt(topic, title, hashtags);
  const strategy = await buildStrategy(topic, hashtags);

  return {
    title,
    content,
    hashtags,
    coverPrompt,
    strategy
  };
};
