import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'fixtures/success-page.json', 'fixtures/failure-page.json'];
for (const file of required) if (!fs.existsSync(path.join(root, file))) throw new Error(`Missing ${file}`);
const skill = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
const manifest = fs.readFileSync(path.join(root, 'manifest.yaml'), 'utf8');
const agent = fs.readFileSync(path.join(root, 'agents/openai.yaml'), 'utf8');
if (!skill.includes('name: youtube-playlist-watch-plan-free')) throw new Error('SKILL name mismatch');
if (!manifest.includes('name: youtube-playlist-watch-plan-free') || !manifest.includes('slug: youtube-playlist-watch-plan-free')) throw new Error('manifest identity mismatch');
if (!manifest.includes('self_test: node scripts/self-test.mjs')) throw new Error('self_test command missing');
for (const file of ['icon-512.png', 'assets/icon-small.png']) if (!fs.existsSync(path.join(root, file))) throw new Error(`Icon reference missing: ${file}`);
const invocation = '$youtube-playlist-watch-plan-free';
if (!agent.includes('allow_implicit_invocation: false') || !agent.includes('short_description:') || !agent.includes(invocation)) throw new Error('agent policy/interface/default prompt invalid');
if (!manifest.includes('allow_implicit_invocation: false') || !manifest.includes(invocation)) throw new Error('manifest policy/interface/default prompt invalid');
const success = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/success-page.json')));
const failure = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/failure-page.json')));
if (success.visible_items.length > 10 || !success.visible_items.every(x => x.duration && x.source)) throw new Error('success fixture invalid');
if (!failure.stop_reason || failure.visible_items[1].duration !== null) throw new Error('failure fixture must demonstrate unknown duration');
const seconds = (value) => {
  const match = /^(\d{1,2}):(\d{2})$/.exec(value ?? '');
  if (!match || Number(match[2]) >= 60) throw new Error(`Invalid duration: ${value}`);
  return Number(match[1]) * 60 + Number(match[2]);
};
const formatDuration = (value) => `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
const verifyBatches = (fixture, expected) => {
  const assigned = expected.daily_batches.flatMap((batch) => batch.positions);
  const visibleByPosition = new Map(fixture.visible_items.map((item) => [item.position, item]));
  if (new Set(assigned).size !== assigned.length) throw new Error('a video was assigned more than once');
  for (const batch of expected.daily_batches) {
    const batchSeconds = batch.positions.reduce((sum, position) => {
      const item = visibleByPosition.get(position);
      if (!item?.duration) throw new Error(`batch includes an item without a visible duration: ${position}`);
      return sum + seconds(item.duration);
    }, 0);
    if (batchSeconds > fixture.daily_minutes * 60) throw new Error(`daily batch ${batch.day} exceeds budget`);
    if (formatDuration(batchSeconds) !== batch.planned_duration) throw new Error(`daily batch ${batch.day} duration mismatch`);
    if (formatDuration(fixture.daily_minutes * 60 - batchSeconds) !== batch.remaining_minutes) throw new Error(`daily batch ${batch.day} remaining time mismatch`);
  }
};
const successExpected = success.expected_business_output;
if (successExpected?.budget_status !== 'complete_from_visible_items') throw new Error('success output must declare a complete visible-item budget');
if (formatDuration(success.visible_items.reduce((sum, item) => sum + seconds(item.duration), 0)) !== '36:04' || successExpected.known_total_duration !== '36:04') throw new Error('success total must be 36:04');
verifyBatches(success, successExpected);
if (JSON.stringify(successExpected.daily_batches.map((batch) => batch.positions)) !== JSON.stringify([[1, 2], [3]])) throw new Error('success daily allocation must be [[1,2],[3]] at 30 minutes per day');
const failureExpected = failure.expected_business_output;
if (failureExpected?.budget_status !== 'incomplete_due_to_missing_duration' || failureExpected.known_total_duration !== '12:34') throw new Error('failure output must report only the known 12:34 duration');
if (failureExpected.complete_budget !== null || !Array.isArray(failureExpected.pending_confirmation) || failureExpected.pending_confirmation[0]?.position !== 2) throw new Error('failure output must leave item 2 pending and omit a complete budget');
verifyBatches(failure, failureExpected);
const png = fs.readFileSync(path.join(root, 'icon-512.png'));
if (png.readUInt32BE(16) !== 512 || png.readUInt32BE(20) !== 512) throw new Error('icon is not 512x512');
console.log('PASS: repository structure, identity, icons, and offline success/failure fixtures are valid.');
