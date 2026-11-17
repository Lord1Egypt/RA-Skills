// verify_js.js — node 端对拍执行器：node verify_js.js <data_dir> <cases.json>
"use strict";
const fs = require("fs");
const path = require("path");
const engine = require(path.join(__dirname, "engine.js"));

const dataDir = process.argv[2];
const cases = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const data = {
  questions: JSON.parse(fs.readFileSync(path.join(dataDir, "questions.json"), "utf8")),
  papers: JSON.parse(fs.readFileSync(path.join(dataDir, "papers.json"), "utf8")),
  meta: JSON.parse(fs.readFileSync(path.join(dataDir, "meta.json"), "utf8")),
  attrs: JSON.parse(fs.readFileSync(path.join(dataDir, "attrs.json"), "utf8")),
  tiers: JSON.parse(fs.readFileSync(path.join(dataDir, "tiers.json"), "utf8")),
};
const out = cases.map(function (c) {
  const r = engine.compute(data, c.letters, c.paper, c.config || "alt");
  return { talisman: r.talisman, dao: r.dao };
});
process.stdout.write(JSON.stringify(out));
