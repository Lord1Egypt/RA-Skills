const { assertChoice, assertIntegerRange } = require("./keyword");

function assertSearchOptions(searchType, limit) {
  searchType = assertChoice(
    searchType,
    [1, 2, 3, 4, 5, 6, 7],
    "搜索类型 search-type",
  );
  limit = assertIntegerRange(limit, 1, 10000, "搜索数量 limit");
  return [searchType, limit];
}

module.exports = { assertSearchOptions };
