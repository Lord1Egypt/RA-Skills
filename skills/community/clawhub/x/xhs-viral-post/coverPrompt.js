module.exports = async function generateCoverPrompt(topic, title, hashtags) {
  const t = String(topic || "").trim() || "lifestyle";
  const h = String(title || "").trim() || "xiaohongshu viral note";
  const tags = (Array.isArray(hashtags) ? hashtags : []).slice(0, 3).join(" ");

  return [
    "Xiaohongshu cover, 4:5 vertical, clean bright style,",
    `theme: ${t},`,
    `headline mood: ${h},`,
    `elements: ${tags || "cozy props, daily life details"},`,
    "natural daylight, close-up product + lifestyle scene,",
    "high contrast subject, minimal background clutter,",
    "premium social media editorial photography, ultra-detailed, no watermark"
  ].join(" ");
};
