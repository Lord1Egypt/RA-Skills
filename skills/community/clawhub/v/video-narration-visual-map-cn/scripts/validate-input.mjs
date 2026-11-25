#!/usr/bin/env node
import fs from 'node:fs';

const [inputPath] = process.argv.slice(2);
if (!inputPath) throw new Error('用法: node scripts/validate-input.mjs <input.json>');
const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const missing = [];
if (!Array.isArray(input.narration) || input.narration.length === 0) missing.push('已批准旁白');
if (!Array.isArray(input.shots) || input.shots.length === 0) missing.push('带编号的候选镜头/素材内容说明');

if (missing.length) {
  console.log(JSON.stringify({
    status: 'needs_input',
    request: `请补充${missing.join('和')}；没有镜头说明时不会完成句画对照或编造证据。`
  }, null, 2));
  process.exitCode = 2;
} else {
  const clean = (value) => String(value ?? '').normalize('NFKC').replace(/[\s，。、“”"'：:；;（）()]/gu, '');
  const hasExactClaim = (shot, claim) => Array.isArray(shot.visible_claims)
    && shot.visible_claims.some((visible) => clean(visible) === clean(claim));
  const hasExactEvidence = (shot, item) => Array.isArray(shot.visible_evidence)
    && shot.visible_evidence.some((visible) => clean(visible) === clean(item));
  const shots = new Map(input.shots.filter((shot) => shot && typeof shot.id === 'string').map((shot) => [shot.id, shot]));
  const rows = input.narration.map((line) => {
    // `visible_claims` is deliberately an explicit, full-claim annotation.  Do
    // not infer support from a shared noun in prose: a visible download button
    // is not evidence that a poster has already been downloaded.
    const lineClaims = Array.isArray(line.claims) ? line.claims.filter((claim) => typeof claim === 'string' && claim.trim()) : [];
    const linkedIds = Array.isArray(line.shot_ids) ? line.shot_ids.filter((id) => typeof id === 'string') : input.shots.map((shot) => shot.id);
    const candidates = linkedIds.map((id) => shots.get(id)).filter(Boolean);
    const missingLink = linkedIds.filter((id) => !shots.has(id));
    if (linkedIds.length === 0) {
      return { narration_id: line.id, shot_ids: [], status: '有声无画', visible_evidence: '没有关联的既有镜头', reason: '这句旁白没有可对应的画面；需补一条实际镜头或素材。' };
    }
    if (lineClaims.length === 0) {
      return { narration_id: line.id, shot_ids: candidates.map((shot) => shot.id), status: '需补素材', visible_evidence: candidates.map((shot) => shot.description || shot.visual || '').filter(Boolean).join('；'), reason: '未给这句旁白标出可核对的具体主张，无法确认镜头是否证明了动作或结果。' };
    }
    // Coverage is the union of this line's candidate shots.  This lets S1
    // establish a title and S2 establish a person without demanding that
    // either single shot contain every requirement.
    const supported = lineClaims.filter((claim) => candidates.some((shot) => hasExactClaim(shot, claim)));
    const evidence = Array.isArray(line.required_evidence) ? line.required_evidence.filter(Boolean) : [];
    const missingEvidence = evidence.filter((item) => !candidates.some((shot) =>
      hasExactEvidence(shot, item)
    ));
    const selected = candidates.filter((shot) => {
      const claimsShown = lineClaims.some((claim) => hasExactClaim(shot, claim));
      const evidenceShown = evidence.some((item) => hasExactEvidence(shot, item));
      return claimsShown || evidenceShown;
    });
    const selectedIds = selected.map((shot) => shot.id);
    const visibleEvidence = (selected.length ? selected : candidates).map((shot) => shot.description || shot.visual || '').filter(Boolean).join('；');
    let status;
    let reason;
    if (missingLink.length) {
      status = '需补素材';
      reason = `关联镜头编号不存在：${missingLink.join('、')}。`;
    } else if (supported.length === lineClaims.length && missingEvidence.length === 0) {
      status = '已支撑';
      reason = '关联镜头明确标出了旁白主张和所需证据。';
    } else if (supported.length === 0 && candidates.length > 0) {
      status = '画不支撑话';
      reason = `现有关联镜头没有标出这句旁白的主张：${lineClaims.join('、')}。`;
    } else {
      status = '需补素材';
      const gaps = [...lineClaims.filter((claim) => !supported.includes(claim)), ...missingEvidence];
      reason = `已有镜头只支持部分内容；仍需补充：${[...new Set(gaps)].join('、')}。`;
    }
    return { narration_id: line.id, shot_ids: selectedIds.length ? selectedIds : candidates.map((shot) => shot.id), status, visible_evidence: visibleEvidence || '没有可核对为已呈现的证据', reason };
  });

  const globalEvidence = Array.isArray(input.required_evidence) ? input.required_evidence.filter(Boolean) : [];
  const evidenceCoverage = globalEvidence.map((item) => ({
    evidence: item,
    shot_ids: input.shots.filter((shot) => hasExactEvidence(shot, item)).map((shot) => shot.id),
  }));
  const missingGlobalEvidence = evidenceCoverage.filter((item) => item.shot_ids.length === 0).map((item) => item.evidence);
  const result = { status: 'mapped', rows, evidence_coverage: evidenceCoverage, missing_materials: missingGlobalEvidence };
  console.log(JSON.stringify(result, null, 2));
}
