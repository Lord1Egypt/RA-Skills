function hash(text) {
  let h = 0;
  for (let i = 0; i < text.length; i += 1) {
    h = (h * 31 + text.charCodeAt(i)) >>> 0;
  }
  return h;
}

module.exports = async function buildStrategy(topic, hashtags) {
  const basis = `${topic || ""}|${(hashtags || []).join("|")}`;
  const n = hash(basis);

  const bestTimes = ["07:40", "12:15", "18:30", "20:10", "21:40"];
  const audiences = [
    "18-24 学生党 / 刚毕业人群",
    "22-30 一二线通勤女生",
    "20-35 关注性价比与颜值的人群",
    "新手博主与轻内容创作者",
    "关注生活方式与效率提升用户"
  ];
  const hooks = [
    "开头先说你踩过的坑，拉近真实感。",
    "正文最后加一句“要不要我出对比版？”提高评论率。",
    "把最实用一步提前说，提升完读率。",
    "用“我自己试了7天”的口吻提高可信度。",
    "结尾引导“先收藏，周末照着做”提高收藏率。"
  ];

  return {
    bestTime: bestTimes[n % bestTimes.length],
    audience: audiences[n % audiences.length],
    hook: hooks[n % hooks.length]
  };
};
