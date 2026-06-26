const fs = require("fs").promises;
const path = require("path");
const { getEnvByName } = require("./wenjuan_env");

const ID_RE = /^[a-zA-Z0-9_-]{8,64}$/;

function validateId(value, fieldName = "id") {
  const v = String(value || "").trim();
  if (!ID_RE.test(v)) {
    throw new Error(`${fieldName} 格式非法`);
  }
  return v;
}

function validateQuestionList(questions) {
  if (!Array.isArray(questions)) {
    throw new Error("question_list 必须是数组");
  }
  if (questions.length === 0) {
    throw new Error("question_list 不能为空");
  }
  if (questions.length > 300) {
    throw new Error("question_list 题目数量不能超过 300");
  }
  questions.forEach((q, i) => {
    if (!q || typeof q !== "object") {
      throw new Error(`第 ${i + 1} 题结构非法`);
    }
    const title = String(q.title || "").trim();
    if (!title) {
      throw new Error(`第 ${i + 1} 题缺少 title`);
    }
    if (title.length > 1000) {
      throw new Error(`第 ${i + 1} 题 title 过长`);
    }
  });
}

async function ensurePrivateDir(dir) {
  const abs = path.resolve(String(dir));
  await fs.mkdir(abs, { recursive: true, mode: 0o700 });
  await fs.chmod(abs, 0o700);
  return abs;
}

async function writeSecretFile(filePath, content) {
  const abs = path.resolve(String(filePath));
  await ensurePrivateDir(path.dirname(abs));
  await fs.writeFile(abs, content, { encoding: "utf-8", mode: 0o600 });
  await fs.chmod(abs, 0o600);
  return abs;
}

function getRequiredEnv(name) {
  const v = getEnvByName(name);
  if (v == null || String(v).trim() === "") {
    throw new Error(`缺少环境变量 ${name}`);
  }
  return String(v).trim();
}

module.exports = {
  validateId,
  validateQuestionList,
  ensurePrivateDir,
  writeSecretFile,
  getRequiredEnv,
};

