import { existsSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const root = new URL('..', import.meta.url);
const file = (name) => readFileSync(new URL(name, root), 'utf8');
const need = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'fixtures/success-visible-subtitles.json', 'fixtures/failure-no-subtitles.json', 'icon-512.png'];
for (const name of need) if (!existsSync(new URL(name, root))) throw new Error(`missing ${name}`);
const skill = file('SKILL.md');
const manifest = file('manifest.yaml');
const agent = file('agents/openai.yaml');
if (!skill.startsWith('---\nname: youtube-transcript-study-notes-free\n')) throw new Error('SKILL frontmatter name mismatch');
for (const value of ['name: youtube-transcript-study-notes-free', 'slug: youtube-transcript-study-notes-free', 'icon: icon-512.png', 'repository: https://github.com/xxjrq/youtube-transcript-study-notes-free']) if (!manifest.includes(value)) throw new Error(`manifest missing ${value}`);
if (!agent.includes('allow_implicit_invocation: true')) throw new Error('agent policy mismatch');
for (const name of ['fixtures/success-visible-subtitles.json', 'fixtures/failure-no-subtitles.json']) {
  const sample = JSON.parse(file(name));
  if (sample.fixture_type !== 'offline visible-page material simulation') throw new Error(`${name} is not marked offline`);
  for (const field of ['source_url', 'requested_language', 'learning_goal']) {
    if (typeof sample[field] !== 'string' || !sample[field].trim()) throw new Error(`${name} missing required ${field}`);
  }
}
const success = JSON.parse(file('fixtures/success-visible-subtitles.json'));
if (success.visible_subtitle_language !== success.requested_language) throw new Error('success fixture language does not match request');
if (success.expected_notes.limitations.length !== 0) throw new Error('success fixture must not report limitations');
const failure = JSON.parse(file('fixtures/failure-no-subtitles.json'));
if (failure.visible_subtitle_state !== 'absent') throw new Error('failure fixture must model absent subtitles');
const png = execFileSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', new URL('icon-512.png', root).pathname], { encoding: 'utf8' });
if (!/pixelWidth: 512/.test(png) || !/pixelHeight: 512/.test(png)) throw new Error('icon must be 512x512');
console.log('self-test passed: metadata, offline fixtures, and 512px icon verified');
