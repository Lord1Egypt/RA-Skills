import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'assets/promo-1600x900.png', 'fixtures/success-output.md', 'fixtures/failure-output.md'];
for (const file of required) if (!existsSync(resolve(root, file))) throw new Error(`缺少文件：${file}`);
const manifest = readFileSync(resolve(root, 'manifest.yaml'), 'utf8');
for (const exact of ['name: video-single-shot-execution-card-cn', 'slug: video-single-shot-execution-card-cn', 'icon: icon-512.png', 'self_test: node scripts/self-test.mjs']) if (!manifest.includes(exact)) throw new Error(`manifest 缺少：${exact}`);
const run = (fixture) => spawnSync(process.execPath, ['scripts/validate-input.mjs', fixture], { cwd: root, encoding: 'utf8' });
const success = run('fixtures/success-input.json');
if (success.status !== 0 || !success.stdout.includes('可制作执行卡')) throw new Error('成功输入未通过真实校验');
const failure = run('fixtures/failure-input.json');
if (failure.status !== 2 || !failure.stdout.includes('人物动作') || !failure.stdout.includes('场地与场地约束')) {
  throw new Error('失败输入未同时识别动作终点/完成标记和场地约束缺失');
}
if (!failure.stdout.includes('人物信息') || !failure.stdout.includes('道具信息')) throw new Error('人物与道具须分别要求提供或明确无需');
const approved = run('fixtures/approved-shot-input.json');
if (approved.status !== 0 || !approved.stdout.includes('可制作执行卡')) throw new Error('新增已批准镜头未通过');
const missingApproval = run('fixtures/missing-approved-shot-input.json');
if (missingApproval.status !== 2 || !missingApproval.stdout.includes('approvedShot') || missingApproval.stdout.includes('可制作执行卡')) throw new Error('其余字段齐全时未拒绝缺少已批准镜头');
const temp = mkdtempSync(resolve(tmpdir(), 'shot-approval-test-'));
try {
  const input = JSON.parse(readFileSync(resolve(root, 'fixtures/approved-shot-input.json'), 'utf8'));
  for (const value of ['', '   ', null, 123, '未确认', '待批准', '待批准：演员从门口走到桌前，放下杯子', '温暖氛围']) {
    const file = resolve(temp, 'case.json');
    writeFileSync(file, JSON.stringify({...input, approvedShot: value}));
    const result = run(file);
    if (result.status !== 2 || !result.stdout.includes('approvedShot')) throw new Error(`批准镜头无效值被通过：${JSON.stringify(value)}`);
  }
  const shortAction = {...input, approvedShot: '已批准：演员举杯喝水。', props: '一个杯子。', actionStart: '演员举起杯子。', actionEnd: '喝完后放下杯子并停1秒。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(shortAction));
  const shortActionResult = run(resolve(temp, 'case.json'));
  if (shortActionResult.status !== 0) throw new Error('简短但可观察的“举杯喝水”已批准镜头应通过完整动作、场地和设备信息校验');
  const staticShot = {...input, approvedShot: '已批准：笔记本静置在桌面正中，固定特写。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(staticShot));
  const staticResult = run(resolve(temp, 'case.json'));
  if (staticResult.status !== 0) throw new Error('明确的静态构图/画面状态应作为具体镜头描述通过');
  const unsupportedObject = {...input, approvedShot: '已批准：红杯特写。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(unsupportedObject));
  const unsupportedResult = run(resolve(temp, 'case.json'));
  if (unsupportedResult.status !== 2 || !unsupportedResult.stdout.includes('approvedShot')) throw new Error('批准镜头与已提供道具矛盾时必须补充确认');
  const naturalAction = {...input, approvedShot: '已批准：演员点头后微笑并保持1秒。', actionStart: '演员看向镜头。', actionEnd: '演员点头后微笑并保持1秒。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(naturalAction));
  const naturalActionResult = run(resolve(temp, 'case.json'));
  if (naturalActionResult.status !== 0) throw new Error('不在封闭动作词表中的自然可观察动作应通过，语义由执行Agent按字段核对');
  const noProps = {...naturalAction, props: '无需道具。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(noProps));
  if (run(resolve(temp, 'case.json')).status !== 0) throw new Error('明确声明无需道具时不应要求补充');
  const noPeople = {...input, approvedShot: '已批准：笔记本静置在桌面正中，固定特写。', people: '无需演员。', actionStart: '笔记本静置在桌面。', actionEnd: '静物保持3秒。'};
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(noPeople));
  if (run(resolve(temp, 'case.json')).status !== 0) throw new Error('明确声明无需人物时不应要求补充');
  const emptyRoom = {
    ...input,
    approvedShot: '已批准：空房间固定全景，保持3秒。',
    people: '无需人物。',
    props: '无需道具。',
    actionStart: '空房间进入固定全景。',
    actionEnd: '空房间固定全景保持3秒。',
  };
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify(emptyRoom));
  if (run(resolve(temp, 'case.json')).status !== 0) throw new Error('人物和道具均明确无需时，已批准的空场静态镜头应通过');
  writeFileSync(resolve(temp, 'case.json'), JSON.stringify({...emptyRoom, approvedShot: ''}));
  const noApprovedShot = run(resolve(temp, 'case.json'));
  if (noApprovedShot.status !== 2 || !noApprovedShot.stdout.includes('approvedShot')) throw new Error('人物与道具均明确无需时，仍必须提供已批准镜头');
} finally { rmSync(temp, {recursive: true, force: true}); }
const successOutput = readFileSync(resolve(root, 'fixtures/success-output.md'), 'utf8');
if (!successOutput.includes('停两秒……一、二，切。') || !successOutput.includes('停留满 2 秒后给出“切”') || /摄影或导演负责/.test(successOutput)) {
  throw new Error('收尾标记须保留 2 秒停留和切口令，且不得臆造口令负责人');
}
const agent = readFileSync(resolve(root, 'agents/openai.yaml'), 'utf8');
for (const key of ['display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large']) {
  const value = agent.match(new RegExp(`^  ${key}: (.+)$`, 'm'))?.[1];
  if (!value?.startsWith('"') || !value.endsWith('"')) throw new Error(`interface.${key} 须为quoted string`);
  const decoded = JSON.parse(value);
  if (key === 'default_prompt' && !decoded.includes('$video-single-shot-execution-card-cn')) throw new Error('default_prompt 缺调用标识');
  if (key.startsWith('icon_') && decoded !== './icon-512.png') throw new Error('图标路径应相对Skill根目录');
  if (key === 'short_description' && (Array.from(decoded).length < 25 || Array.from(decoded).length > 64)) throw new Error('short_description长度不合规');
}
console.log('self-test 通过：实际执行完整/缺料/缺批准输入、7种无效/含糊描述、简短动作与静态构图正例及正式元数据检查。');
