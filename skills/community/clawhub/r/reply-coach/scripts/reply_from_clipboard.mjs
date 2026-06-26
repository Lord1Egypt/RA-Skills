import { execSync } from "node:child_process";

function safeRun(cmd) {
  try {
    return execSync(cmd, { encoding: "utf8" }).trim();
  } catch (err) {
    return "";
  }
}

const text = safeRun("pbpaste");

if (!text) {
  console.error("剪贴板里没有可读取的文本。请先复制聊天内容，再使用这个 skill。");
  process.exit(1);
}

console.log("===CHAT_TEXT_BEGIN===");
console.log(text);
console.log("===CHAT_TEXT_END===");
