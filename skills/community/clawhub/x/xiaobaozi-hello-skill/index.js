#!/usr/bin/env node

// 小包子 Hello World 技能
// 2026-04-05

const args = process.argv.slice(2);

function parseArgs() {
  const params = {
    name: "World",
    lang: "en"
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--name" && i + 1 < args.length) {
      params.name = args[i + 1];
      i++;
    } else if (args[i] === "--lang" && i + 1 < args.length) {
      params.lang = args[i + 1];
      i++;
    }
  }
  
  return params;
}

function helloWorld(name = "World", lang = "en") {
  const messages = {
    en: `Hello, ${name}!`,
    zh: `你好，${name}！`,
    es: `¡Hola, ${name}!`,
    fr: `Bonjour, ${name}!`,
    ja: `こんにちは、${name}！`,
    ko: `안녕하세요, ${name}！`
  };
  
  return messages[lang] || messages.en;
}

// 主函数
function main() {
  const params = parseArgs();
  const message = helloWorld(params.name, params.lang);
  console.log(message);
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = { helloWorld, parseArgs, main };