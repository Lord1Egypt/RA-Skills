const HOT_CATEGORIES = [
  "realtimehot",
  "fun",
  "social",
  "sportnav",
  "lifenav",
  "gamenav",
  "technologynav",
];

function assertHotCategory(category) {
  const value = String(category ?? "").trim();
  if (!HOT_CATEGORIES.includes(value)) {
    throw new Error(
      `热搜类目 ${category} 无效, 允许: ${HOT_CATEGORIES.join(", ")}`,
    );
  }
  return value;
}

module.exports = { HOT_CATEGORIES, assertHotCategory };
