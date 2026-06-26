const https = require('https');
const fs = require('fs');

const API_KEY = process.env.ARK_API_KEY;
const BASE_URL = process.env.ARK_BASE_URL || 'ark.cn-beijing.volces.com';
const API_PATH = '/api/v3/chat/completions';
const MODEL = process.env.ARK_MODEL || 'doubao-1.5-pro-32k-250115';

if (!API_KEY) {
  console.error('[question_generator] 错误: ARK_API_KEY 环境变量未设置');
  process.exit(1);
}

// Truncate content if too long (API limit ~32k tokens)
function truncateContent(content, maxChars = 6000) {
  if (content.length <= maxChars) return content;
  return content.substring(0, maxChars) + '\n\n[内容已截断...]';
}

function callAI(messages) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      messages,
      temperature: 0.7,
      max_tokens: 3000
    });

    const options = {
      hostname: BASE_URL,
      path: '/api/v3/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) return reject(new Error(parsed.error.message || 'API Error'));
          resolve(parsed.choices[0].message.content);
        } catch (e) {
          reject(new Error('Failed to parse AI response: ' + data.substring(0, 200)));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

const SYSTEM_PROMPT = `你是一个专业的题目生成专家。根据提供的教材或课程内容，生成高质量的测试题目。

要求：
1. 生成 **10道选择题**（每题4个选项 A/B/C/D），涵盖内容的核心知识点
2. 难度要适中，区分度好
3. 严格按照以下JSON格式返回，不要添加任何解释或说明：

[
  {
    "question": "题目内容（完整描述题干）",
    "options": ["A. 选项A内容", "B. 选项B内容", "C. 选项C内容", "D. 选项D内容"],
    "correctAnswer": "A"  // 正确选项字母
  }
]

重要：
- 只返回纯JSON数组，不要有markdown代码块标记
- 每道题的选项要清晰、正确
- 正确答案要合理，不要有歧义
- 题目内容要准确基于原文`;

async function generateQuestions(content) {
  const truncated = truncateContent(content);
  
  const userMessage = `请根据以下教材内容生成10道选择题：\n\n${truncated}`;

  const reply = await callAI([
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'user', content: userMessage }
  ]);

  // Try to extract JSON from the response
  let jsonStr = reply.trim();
  
  // Remove markdown code block if present
  if (jsonStr.startsWith('```')) {
    jsonStr = jsonStr.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }

  try {
    const questions = JSON.parse(jsonStr);
    if (!Array.isArray(questions) || questions.length === 0) {
      throw new Error('Invalid question format');
    }
    // Validate each question
    for (const q of questions) {
      if (!q.question || !q.options || !q.correctAnswer) {
        throw new Error('Question missing required fields');
      }
      if (q.options.length !== 4) {
        throw new Error('Each question must have exactly 4 options');
      }
    }
    return questions;
  } catch (err) {
    console.error('JSON parse error:', err.message);
    console.error('Raw reply:', jsonStr.substring(0, 500));
    throw new Error('AI返回格式错误，请重试: ' + err.message);
  }
}

module.exports = { generateQuestions };
