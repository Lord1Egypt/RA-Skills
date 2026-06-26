const axios = require("axios");

const FALLBACK = [
  "真实测评",
  "平替",
  "不踩雷",
  "学生党",
  "上班族",
  "新手友好",
  "高性价比",
  "懒人方法"
];

function uniq(items) {
  return Array.from(new Set(items.map((x) => String(x || "").trim()).filter(Boolean)));
}

async function fetchDatamuse(topic) {
  const res = await axios.get("https://api.datamuse.com/words", {
    params: { ml: topic, max: 12 },
    timeout: 5000
  });

  if (!Array.isArray(res.data)) {
    return [];
  }

  return uniq(res.data.map((x) => x.word));
}

module.exports = async function getTrendingKeywords(topic) {
  const cleanTopic = String(topic || "").trim();

  try {
    if (cleanTopic) {
      const apiWords = await fetchDatamuse(cleanTopic);
      if (apiWords.length >= 5) {
        return { keywords: apiWords };
      }
    }
  } catch (_) {
    // Network failures fallback to simulated keywords.
  }

  return {
    keywords: uniq([cleanTopic, ...FALLBACK, "爆款", "收藏", "种草清单"]).slice(0, 12)
  };
};
