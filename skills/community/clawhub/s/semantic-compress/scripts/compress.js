/**
 * semantic-compress - 语义压缩，在保留全部关键信息的前提下大幅减少token消耗
 */

const fs = require('fs');
const path = require('path');

// 压缩提示词
const COMPRESSION_PROMPT = `
你是一个语义压缩专家。你的任务是压缩给定文本，在**保留全部关键信息和逻辑完整性**的前提下，去除所有冗余废话，大幅减少token数量。

## 严格遵守压缩规则：

1. ✅ 必须保留：所有核心论点、结论、决策、数据、关键事实、逻辑关系
2. ✅ 必须删除：所有客套话、重复说明、过程性废话、修饰性铺垫、语气词、重复确认
3. ✅ 保持逻辑连贯：压缩后仍然是完整可理解的文本
4. ✅ 能合并就合并：用简洁的一句话代替分散的多句话
5. ❌ 不准丢失任何关键信息！不准做摘要总结！只删废话，不删信息
6. ❌ 不准添加新内容！只压缩，不扩展

## 分层压缩规则（如果是对话历史）：
- 最近的3轮对话：完整保留
- 更早的对话：只保留结论和关键信息，过程性问答删除

## 输出格式：
直接输出压缩后的文本，不要加任何说明。

---

请压缩以下文本：
`;

function semanticCompress(text, options = {}) {
  const defaultOptions = {
    targetCompression: 0.5,
    preserveAccuracy: true,
    model: null
  };
  const config = { ...defaultOptions, ...options };
  
  const fullPrompt = COMPRESSION_PROMPT + '\n' + text;
  return {
    prompt: fullPrompt,
    originalLength: text.length,
    originalTokens: Math.ceil(text.length / 4), // 粗略估算
    config: config
  };
}

function compressFromFile(inputPath, outputPath = null) {
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }
  
  const text = fs.readFileSync(inputPath, 'utf-8');
  const result = semanticCompress(text);
  
  if (outputPath) {
    fs.writeFileSync(outputPath, result.prompt, 'utf-8');
    console.log(`Compressed prompt written to: ${outputPath}`);
    console.log(`Original length: ${result.originalLength} chars (~${result.originalTokens} tokens)`);
  } else {
    console.log(result.prompt);
  }
  
  return result;
}

// 如果从命令行运行
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: node compress.js <input-file> [output-file]');
    console.log('Example: node compress.js conversation.txt compressed.txt');
    process.exit(1);
  }
  
  compressFromFile(args[0], args[1] || null);
}

module.exports = {
  semanticCompress,
  compressFromFile,
  COMPRESSION_PROMPT
};
