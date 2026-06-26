'use strict';

/**
 * Skill: rewrite-question
 * 调用 rewrite_question.py 中的 RewriteQuestionSkill.run()
 *
 * 入参 input:
 *   - query          {string}  用户原始问题（必填）
 *   - history        {Array}   历史对话，每项 { session_id, query, created_at?, response_data? }
 *   - qa_pairs       {Array}   QA 对列表，每项 { id, question, sql }
 *   - gemini_api_url {string}  Gemini REST 地址（可选，env: GEMINI_API_URL）
 *   - gemini_api_key {string}  x-goog-api-key（可选，env: GEMINI_API_KEY）
 *   - gemini_token   {string}  自定义鉴权 token（可选，env: GEMINI_TOKEN）
 *   - llm_timeout    {number}  LLM 超时秒数，默认 120
 *
 * 出参:
 *   - final_query    {string}  送往下一环节的最终问题
 *   - is_rewritten   {boolean} 是否发生重写
 *   - thought        {string}  LLM 推理过程
 *   - confidence     {number}  重写置信度
 *   - matched_sql    {string?} 命中 QA 对时的 SQL
 *   - is_qa_matched  {boolean} 是否命中 QA 对
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 加载 skills/.env（若父进程未注入则自行读取）
(function loadDotEnv() {
  const envFile = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envFile)) return;
  for (const line of fs.readFileSync(envFile, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
})();

// 优先读取 PYTHON_EXECUTABLE，回退到 'python'
const PYTHON_BIN = process.env.PYTHON_EXECUTABLE || 'python';

const PYTHON_RUNNER = `
import asyncio, json, sys
sys.path.insert(0, sys.argv[1])
from rewrite_question import RewriteQuestionSkill, RewriteInput, HistoryRecord, QAPair
from datetime import datetime

data = json.loads(sys.stdin.buffer.read().decode('utf-8'))

skill = RewriteQuestionSkill(
    gemini_api_url=data.get('gemini_api_url', ''),
    gemini_api_key=data.get('gemini_api_key', ''),
    gemini_token=data.get('gemini_token', ''),
    llm_timeout=float(data.get('llm_timeout', 120)),
)

history = [
    HistoryRecord(
        session_id=h.get('session_id', ''),
        query=h.get('query', ''),
        created_at=datetime.fromisoformat(h['created_at']) if h.get('created_at') else datetime.now(),
        response_data=h.get('response_data'),
    )
    for h in data.get('history', [])
]

qa_pairs = [
    QAPair(id=q.get('id', ''), question=q.get('question', ''), sql=q.get('sql', ''))
    for q in data.get('qa_pairs', [])
]

inp = RewriteInput(query=data['query'], history=history, qa_pairs=qa_pairs)
out = asyncio.run(skill.run(inp))

print(json.dumps({
    'final_query':   out.final_query,
    'is_rewritten':  out.is_rewritten,
    'thought':       out.thought,
    'confidence':    out.confidence,
    'matched_sql':   out.matched_sql,
    'is_qa_matched': out.is_qa_matched,
}, ensure_ascii=False))
`;

async function run({ input }) {
  const payload = JSON.stringify({
    query:          input.query,
    history:        input.history        || [],
    qa_pairs:       input.qa_pairs       || [],
    gemini_api_url: input.gemini_api_url || process.env.GEMINI_API_URL || '',
    gemini_api_key: input.gemini_api_key || process.env.GEMINI_API_KEY || '',
    gemini_token:   input.gemini_token   || process.env.GEMINI_TOKEN   || '',
    llm_timeout:    input.llm_timeout    || 120,
  });

  return execPython(PYTHON_RUNNER, payload, __dirname);
}

function execPython(script, stdinData, skillDir) {
  return new Promise((resolve, reject) => {
    const proc = spawn(PYTHON_BIN, ['-c', script, skillDir], {
      env: { ...process.env },
    });

    let stdout = '';
    let stderr = '';

    proc.stdin.write(stdinData, 'utf8');
    proc.stdin.end();

    proc.stdout.on('data', (d) => { stdout += d.toString('utf8'); });
    proc.stderr.on('data', (d) => { stderr += d.toString('utf8'); });
    proc.on('error', (err) => reject(new Error(`[rewrite-question] spawn失败 (${PYTHON_BIN}): ${err.message}`)));

    proc.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`[rewrite-question] Python exit ${code}:\n${stderr}`));
      }
      try {
        resolve(JSON.parse(stdout.trim()));
      } catch (e) {
        reject(new Error(`[rewrite-question] JSON解析失败: ${e.message}\nstdout: ${stdout}\nstderr: ${stderr}`));
      }
    });
  });
}

module.exports = { run };
