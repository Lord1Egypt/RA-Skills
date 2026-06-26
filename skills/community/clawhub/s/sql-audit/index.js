'use strict';

/**
 * Skill: sql-audit
 * 调用 sql_audit.py 中的 SQLAuditSkill.run()
 *
 * 数据库连接说明（三选一）：
 *   1. mock_rows  — 预设行数据，跳过真实数据库（测试用）
 *   2. db_dsn     — StarRocks/MySQL DSN: mysql://user:pass@host:port/dbname（需 pymysql）
 *   3. env DB_DSN — 同上格式（在 skills/.env 中配置）
 *
 * 入参 input:
 *   - query             {string}   用户原始问题（必填）
 *   - sql               {string?}  待执行 SQL（与 sql_candidates 二选一）
 *   - sql_candidates    {Array?}   多候选 SQL，每项 { sql, context, index }
 *   - indicator_metric  {*}        指标维度信息
 *   - vector_candidates {object}   向量候选
 *   - retry_count       {number}   当前重试次数，默认 0
 *   - connection_id     {number}   连接 ID，默认 0
 *   - memory_id         {string}   会话记忆 ID
 *   - mock_rows         {Array?}   预设返回行（mock 模式）
 *   - db_dsn            {string?}  真实数据库 DSN（优先级高于 mock_rows）
 *   - gemini_api_url / gemini_api_key / gemini_token（兜底候选生成用，可选）
 *   - llm_timeout       {number}   LLM 超时秒数，默认 120
 *
 * 出参:
 *   - success / sql / data / row_count / error_msg / new_indicator_metrics / need_retry / retry_count
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
from sql_audit import SQLAuditSkill, SQLAuditInput

data = json.loads(sys.stdin.buffer.read().decode('utf-8'))

def make_db_runner(data):
    import os
    dsn = data.get('db_dsn') or os.environ.get('DB_DSN', '')
    if dsn:
        try:
            import pymysql, re
            m = re.match(r'[a-z]+://([^:]+):([^@]*)@([^:/]+):?(\\d*)/(\\S*)', dsn)
            if m:
                user, pwd, host, port_s, dbname = m.groups()
                port = int(port_s) if port_s else 9030
                class RealDBRunner:
                    def run_sql(self, sql):
                        conn = pymysql.connect(host=host, port=port, database=dbname,
                                               user=user, password=pwd, charset='utf8mb4')
                        try:
                            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                                cur.execute(sql.rstrip(';'))
                                return list(cur.fetchmany(50))
                        finally:
                            conn.close()
                return RealDBRunner()
        except Exception as e:
            sys.stderr.write(f'[sql-audit] DB连接失败，降级为mock: {e}\\n')
    rows = data.get('mock_rows') or []
    class MockDBRunner:
        def run_sql(self, _sql): return rows
    return MockDBRunner()

skill = SQLAuditSkill(
    db_service=make_db_runner(data),
    gemini_api_url=data.get('gemini_api_url', ''),
    gemini_api_key=data.get('gemini_api_key', ''),
    gemini_token=data.get('gemini_token', ''),
    llm_timeout=float(data.get('llm_timeout', 120)),
)

inp = SQLAuditInput(
    query=data['query'],
    sql=data.get('sql'),
    sql_candidates=data.get('sql_candidates'),
    indicator_metric=data.get('indicator_metric'),
    vector_candidates=data.get('vector_candidates', {}),
    retry_count=int(data.get('retry_count', 0)),
    connection_id=int(data.get('connection_id', 0)),
    memory_id=data.get('memory_id', ''),
)

out = asyncio.run(skill.run(inp))

print(json.dumps({
    'success':               out.success,
    'sql':                   out.sql,
    'data':                  out.data,
    'row_count':             out.row_count,
    'error_msg':             out.error_msg,
    'new_indicator_metrics': out.new_indicator_metrics,
    'need_retry':            out.need_retry,
    'retry_count':           out.retry_count,
}, ensure_ascii=False))
`;

async function run({ input }) {
  const payload = JSON.stringify({
    query:             input.query             || '',
    sql:               input.sql               || null,
    sql_candidates:    input.sql_candidates    || null,
    indicator_metric:  input.indicator_metric  || null,
    vector_candidates: input.vector_candidates || {},
    retry_count:       input.retry_count       || 0,
    connection_id:     input.connection_id     || 0,
    memory_id:         input.memory_id         || '',
    mock_rows:         input.mock_rows         || null,
    db_dsn:            input.db_dsn            || process.env.DB_DSN            || '',
    gemini_api_url:    input.gemini_api_url    || process.env.GEMINI_API_URL    || '',
    gemini_api_key:    input.gemini_api_key    || process.env.GEMINI_API_KEY    || '',
    gemini_token:      input.gemini_token      || process.env.GEMINI_TOKEN      || '',
    llm_timeout:       input.llm_timeout       || 120,
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
    proc.on('error', (err) => reject(new Error(`[sql-audit] spawn失败 (${PYTHON_BIN}): ${err.message}`)));

    proc.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`[sql-audit] Python exit ${code}:\n${stderr}`));
      }
      try {
        resolve(JSON.parse(stdout.trim()));
      } catch (e) {
        reject(new Error(`[sql-audit] JSON解析失败: ${e.message}\nstdout: ${stdout}\nstderr: ${stderr}`));
      }
    });
  });
}

module.exports = { run };
