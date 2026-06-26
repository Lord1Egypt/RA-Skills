# Evaluation Suite - OpenClaw 评估体系

**版本**: 0.1.0  
**功能**: RAG评估 + 推理评估 + 幻觉检测

## 功能特性

- **RAG 评估**: 检索质量、答案相关性、上下文准确性
- **推理评估**: 逻辑推理能力测试
- **幻觉检测**: 检测 AI 生成内容中的幻觉
- **批量评估**: 支持批量测试用例评估
- **统一接口**: 一致的评估 API

## 安装

```bash
cd skills/evaluation-suite
npm install
```

## 快速开始

```javascript
import { Evaluator } from './src/evaluator.js';

// 创建评估器
const evaluator = new Evaluator({
  rag: { threshold: 0.7 },
  reasoning: { threshold: 0.8 },
  hallucination: { threshold: 0.5 }
});

// RAG 评估
const ragResult = await evaluator.evaluate('rag', {
  query: '什么是 OpenClaw?',
  retrievedDocs: ['OpenClaw 是一个 AI 助手框架...'],
  generatedAnswer: 'OpenClaw 是一个 AI 助手框架'
});

console.log('RAG Score:', ragResult.score);

// 幻觉检测
const hallucinationResult = await evaluator.evaluate('hallucination', {
  context: 'OpenClaw 是一个框架',
  generatedText: 'OpenClaw 是一个编程语言'
});

console.log('Hallucination:', hallucinationResult.isHallucination);
```

## API 参考

### Evaluator

#### 构造函数
```javascript
new Evaluator(config)
```

**参数**:
- `config.rag.threshold` - RAG 评估阈值 (默认: 0.7)
- `config.reasoning.threshold` - 推理评估阈值 (默认: 0.8)
- `config.hallucination.threshold` - 幻觉检测阈值 (默认: 0.5)

#### evaluate(type, params)
运行评估

```javascript
// RAG 评估
await evaluator.evaluate('rag', {
  query: '问题',
  retrievedDocs: ['文档1', '文档2'],
  generatedAnswer: '生成的答案'
});

// 推理评估
await evaluator.evaluate('reasoning', {
  problem: '推理问题',
  solution: '解决方案',
  expectedAnswer: '期望答案'
});

// 幻觉检测
await evaluator.evaluate('hallucination', {
  context: '上下文',
  generatedText: '生成的文本'
});
```

#### batchEvaluate(type, testCases)
批量评估

```javascript
const results = await evaluator.batchEvaluate('rag', [
  { query: 'Q1', retrievedDocs: [...], generatedAnswer: 'A1' },
  { query: 'Q2', retrievedDocs: [...], generatedAnswer: 'A2' }
]);
```

### RAGEvaluator

#### evaluate(params)
评估 RAG 质量

```javascript
import RAGEvaluator from './src/rag-eval.js';

const evaluator = new RAGEvaluator({ threshold: 0.7 });
const result = await evaluator.evaluate({
  query: '问题',
  retrievedDocs: ['文档1', '文档2'],
  generatedAnswer: '答案'
});

// 返回: { score, relevanceScore, contextScore, passed }
```

### ReasoningEvaluator

#### evaluate(params)
评估推理能力

```javascript
import ReasoningEvaluator from './src/reasoning-eval.js';

const evaluator = new ReasoningEvaluator({ threshold: 0.8 });
const result = await evaluator.evaluate({
  problem: '逻辑问题',
  solution: '解决步骤',
  expectedAnswer: '期望答案'
});

// 返回: { score, logicScore, completenessScore, passed }
```

### HallucinationDetector

#### detect(params)
检测幻觉

```javascript
import HallucinationDetector from './src/hallucination-detector.js';

const detector = new HallucinationDetector({ threshold: 0.5 });
const result = await detector.detect({
  context: '原始上下文',
  generatedText: '生成的文本'
});

// 返回: { isHallucination, score, indicators }
```

## 测试

```bash
npm test
```

## License

MIT
