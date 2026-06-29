/**
 * main.js — query_papers Skill 入口
 * 行为由 SKILL.md 驱动；本文件仅提供元信息。
 */
module.exports = {
  name: "query_papers",
  version: "1.0.0",
  description:
    "paper-kb 查询知识库：两阶段检索（目录定位→精读页面），生成带来源链接的中文回答",
  entry: "SKILL.md",
  scripts: {
    listCatalog: "python3 scripts/kb_read.py --open_id <id> --list all",
    readPage: "python3 scripts/kb_read.py --open_id <id> --read <page>",
    logQuery: "python3 scripts/log_query.py --open_id <id> --question <q>",
  },
};
