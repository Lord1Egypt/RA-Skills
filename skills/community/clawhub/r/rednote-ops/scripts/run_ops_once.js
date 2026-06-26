const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const profilePath = path.join(process.cwd(), 'data/xiaohongshu/profile.json');
const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const topic = process.argv[2] || 'AI 工作流';
const angle = process.argv[3] || '大多数人学 AI 的方向一开始就错了';
const outDir = process.argv[4] || '/tmp/openclaw/uploads/xhs_ops_run';

function shortenTitle(input, max = 20) {
  const s = String(input || '').replace(/[\n\r]+/g, ' ').trim();
  if ([...s].length <= max) return s;

  const rules = [
    [/大多数人还没意识到/g, '很多人没意识到'],
    [/真正淘汰的是/g, '真正淘汰的'],
    [/会提问的人很多，但会把AI接进工作的人还不多/g, '会提问不等于会用AI'],
    [/会用AI的人变多了，但真正拉开差距的人还很少/g, 'AI拉开差距的是工作流'],
    [/你以为大家都在学AI，其实真正赚钱的人在搭流程/g, '赚钱的人都在搭AI流程'],
    [/大多数人学 AI 的方向一开始就错了/g, '大多数人学AI方向错了'],
    [/很多人只盯模型参数，却没看见Anthropic真正重视的是harness/g, 'Anthropic更重视harness'],
    [/Anthropic/gi, 'Anthropic'],
    [/OpenAI/gi, 'OpenAI'],
    [/harness engineering/gi, 'harness'],
    [/computer use/gi, 'computer use']
  ];

  let out = s;
  for (const [pattern, replacement] of rules) out = out.replace(pattern, replacement);
  out = out.replace(/[｜|].*$/, '').trim();
  if ([...out].length > max) out = [...out].slice(0, max).join('');
  return out;
}

fs.mkdirSync(outDir, { recursive: true });

const opsScriptDir = __dirname;
const studio = spawnSync('node', [
  path.join(opsScriptDir, 'build_xhs_post.js'),
  '--topic', topic,
  '--angle', angle,
  '--pages', String(profile.defaultPages || 2),
  '--out', outDir
], { stdio: 'inherit' });
if (studio.status !== 0) process.exit(studio.status || 1);

const post = JSON.parse(fs.readFileSync(path.join(outDir, 'post.json'), 'utf8'));
const publish = spawnSync('node', [
  path.join(opsScriptDir, 'xhs_independent_publish.js'),
  '--asset-dir', path.join(outDir, 'png'),
  '--title', shortenTitle(post.title, 20),
  '--body', post.body
], { stdio: 'inherit' });
if (publish.status !== 0) process.exit(publish.status || 1);

console.log('XHS_OPS_ONCE_DONE');
