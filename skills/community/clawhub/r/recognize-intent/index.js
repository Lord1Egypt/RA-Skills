'use strict';

/**
 * Skill: recognize-intent
 * 调用 recognize_intent.py 中的 RecognizeIntentSkill.run()
 *
 * 入参 input:
 *   - query           {string}  重写后的用户问题（必填；也接受 rewritten_query 别名）
 *   - memory_id       {string}  会话记忆 ID（可选）
 *   - indicators      {Array}   指标别名列表，每项 { indicator_code, indicator_name, indicator_alias?, similarity_score? }
 *   - metric_configs  {Array}   指标维度配置，每项 { indicator_code, indicator_metadata, aggregation, metric_info }
 *   - gemini_api_url  {string}  Gemini REST 地址（可选，env: GEMINI_API_URL）
 *   - gemini_api_key  {string}  x-goog-api-key（可选，env: GEMINI_API_KEY）
 *   - gemini_token    {string}  自定义鉴权 token（可选，env: GEMINI_TOKEN）
 *   - llm_timeout     {number}  LLM 超时秒数，默认 120
 *
 * 出参:
 *   - intent / indicator_metric / success / message 等
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 加载 skills/.env
(function loadDotEnv() {
  const envFile = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envFile)) return;
  for (const line of fs.readFileSync(envFile, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
})();

const PYTHON_BIN = process.env.PYTHON_EXECUTABLE || 'python';

const PYTHON_RUNNER = `
import asyncio, json, sys
sys.path.insert(0, sys.argv[1])
from recognize_intent import RecognizeIntentSkill, IntentInput

data = json.loads(sys.stdin.buffer.read().decode('utf-8'))

class MockIndicatorSearcher:
    def __init__(self, indicators):
        self._list = indicators or []
    def search_by_text(self, name, top_k=3):
        hits = [i for i in self._list
                if name.lower() in i.get('indicator_name', '').lower()
                or name.lower() in i.get('indicator_alias', '').lower()]
        if not hits:
            hits = sorted(self._list, key=lambda x: x.get('similarity_score', 0), reverse=True)
        return [{**h, 'similarity_score': h.get('similarity_score', 0.9)} for h in hits[:top_k]]
    def search_all_alias(self):
        return '\\u3001'.join(i.get('indicator_name', '') for i in self._list)

class MockMetricConfigLoader:
    def __init__(self, configs):
        self._configs = configs or []
    def search_by_text(self, code):
        matched = [c for c in self._configs if c.get('indicator_code') == code]
        return matched if matched else self._configs[:1]

skill = RecognizeIntentSkill(
    gemini_api_url=data.get('gemini_api_url', ''),
    gemini_api_key=data.get('gemini_api_key', ''),
    gemini_token=data.get('gemini_token', ''),
    indicator_searcher=MockIndicatorSearcher(data.get('indicators', [])),
    metric_config_loader=MockMetricConfigLoader(data.get('metric_configs', [])),
    llm_timeout=float(data.get('llm_timeout', 120)),
)

query = data.get('query') or data.get('rewritten_query', '')
inp = IntentInput(query=query, memory_id=data.get('memory_id', ''))
out = asyncio.run(skill.run(inp))

print(json.dumps({
    'intent':                  out.intent,
    'indicator_metric':        out.indicator_metric,
    'l1_concepts':             out.l1_concepts,
    'vector_candidates':       out.vector_candidates,
    'candidates':              out.candidates,
    'indicator_metric_groups': out.indicator_metric_groups,
    'mode':                    out.mode,
    'success':                 out.success,
    'message':                 out.message,
    'result_data':             out.result_data,
}, ensure_ascii=False))
`;

async function run({ input }) {
  const payload = JSON.stringify({
    query:           input.query          || input.rewritten_query || '',
    memory_id:       input.memory_id      || '',
    indicators:      input.indicators     || [],
    metric_configs:  input.metric_configs || [],
    gemini_api_url:  input.gemini_api_url || process.env.GEMINI_API_URL || '',
    gemini_api_key:  input.gemini_api_key || process.env.GEMINI_API_KEY || '',
    gemini_token:    input.gemini_token   || process.env.GEMINI_TOKEN   || '',
    llm_timeout:     input.llm_timeout    || 120,
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
    proc.on('error', (err) => reject(new Error(`[recognize-intent] spawn失败 (${PYTHON_BIN}): ${err.message}`)));

    proc.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`[recognize-intent] Python exit ${code}:\n${stderr}`));
      }
      try {
        resolve(JSON.parse(stdout.trim()));
      } catch (e) {
        reject(new Error(`[recognize-intent] JSON解析失败: ${e.message}\nstdout: ${stdout}\nstderr: ${stderr}`));
      }
    });
  });
}

module.exports = { run };
