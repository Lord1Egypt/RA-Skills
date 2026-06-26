function hash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function cleanToken(t) {
  const v = String(t || "").replace(/^#+/, "").trim();
  if (!v) return "";
  if (v.length > 18) return "";
  return `#${v}`;
}

module.exports = async function rankHashtags(topic, keywords, title, content) {
  const pool = [topic, ...(keywords || []), title, content]
    .map((x) => String(x || "").trim())
    .filter(Boolean)
    .flatMap((x) => x.split(/[\s,，。.!！？、\n]+/))
    .map(cleanToken)
    .filter(Boolean);

  const seed = [
    ...pool,
    "#小红书笔记",
    "#真实分享",
    "#种草",
    "#好物推荐",
    "#生活方式",
    "#自媒体运营"
  ];

  const uniq = Array.from(new Set(seed));

  return uniq
    .map((tag) => ({
      tag,
      score: 50 + (hash(`${tag}|${topic}`) % 51)
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map((x) => x.tag);
};
