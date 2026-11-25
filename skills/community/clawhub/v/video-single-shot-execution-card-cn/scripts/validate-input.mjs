import { readFileSync } from 'node:fs';

const file = process.argv[2];
if (!file) throw new Error('用法：node scripts/validate-input.mjs <input.json>');
const input = JSON.parse(readFileSync(file, 'utf8'));
const text = (value) => typeof value === 'string' ? value.trim() : '';
const hasActionStart = Boolean(text(input.actionStart));
const hasActionEnd = Boolean(text(input.actionEnd));
const location = text(input.location);
const locationConstraint = text(input.locationConstraint);
const people = text(input.people);
const props = text(input.props);
const explicitlyNone = (value, subject) => new RegExp(`^(?:无|无需|不需要|不使用)(?:${subject})?[。.!！]*$`, 'u').test(value);
const isPlaceholder = (value) => /^(?:未确认|未批准|待批准|待审批|待确认|待审核|(?:温暖|轻松|治愈|高级|浪漫)?氛围|(?:温暖|轻松|治愈|高级|浪漫)氛围感)(?:\s*[:：].*)?[。！!]*$/u.test(value);
// “室内”“室外”等只说明类型，不构成可执行的场地约束。允许单独字段，
// 或在场地描述中给出范围、限制或安全条件等可检查的要求。
const hasEmbeddedLocationConstraint = /(范围|尺寸|距离|限制|保持|避开|清空|封闭|可用|不得|只能|禁止|安全|障碍)/u.test(location);
const missing = [];
const approvedShot = text(input.approvedShot);
// Approval is a non-negotiable input for every execution card. In particular,
// do not let an empty-scene shot (both people and props explicitly unnecessary)
// bypass this requirement merely because it has no grounding anchors.
if (!approvedShot || isPlaceholder(approvedShot)) {
  missing.push('一条已批准且能与人物/道具输入对应的具体实拍镜头（approvedShot）');
}
// Deterministic boundary: require a concrete subject/item in the approved
// shot that is grounded in the supplied people/props. Do not try to infer
// natural-language action semantics from a closed verb list; the agent must
// compare the approved shot with actionStart/actionEnd before drafting.
const anchors = [
  explicitlyNone(people, '人物|演员') ? '' : people,
  explicitlyNone(props, '道具') ? '' : props,
]
  .flatMap((value) => value.match(/[\p{Script=Han}]{2,}/gu) ?? [])
  .map((term) => term.replace(/^(?:一名|一位|一个|一只|一本|一张|一把|两名|两位|两个|两只|两本|两张|两把)/u, ''))
  .filter((term) => term.length >= 2 && !/^(人物|道具|物品|东西|产品|商品)$/u.test(term));
const grounded = anchors.some((term) => approvedShot.includes(term) || (term.endsWith('子') && approvedShot.includes(term.slice(0, -1))));
const hasDeclaredSubject = anchors.length > 0;
if (hasDeclaredSubject && !grounded) {
  missing.push('一条已批准且能与人物/道具输入对应的具体实拍镜头（approvedShot）');
}
if (!hasActionStart || !hasActionEnd) missing.push('人物动作的起点与终点/完成标记');
if (!location || !(locationConstraint || hasEmbeddedLocationConstraint)) missing.push('场地与场地约束');
if (!people && !explicitlyNone(people, '人物|演员')) missing.push('人物信息（或明确写无需人物/演员）');
if (!props && !explicitlyNone(props, '道具')) missing.push('道具信息（或明确写无需道具）');
if (!text(input.equipment)) missing.push('现有设备');
if (!text(input.delivery)) missing.push('交付要求');
if (missing.length) {
  console.log(`缺项：${missing.join('；')}`);
  process.exitCode = 2;
} else {
  console.log('输入可制作执行卡：已批准镜头、关键动作、场地、设备与交付要求齐全。');
}
