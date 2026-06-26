// missing.ts — /pvp 缺什么：找出当前缺少的关键宝可梦

import { loadMyPokemon } from './list';
import { getRankings } from './fetcher';
import { getSpeciesCn, getMoveCn } from './mapper';
import type { PvPokePokemon } from './types';

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
};

const LEAGUE_ORDER = ['1500', '2500', 'master'];

function getRankingMoves(entry: PvPokePokemon): { fast: string; charged: string[] } {
  if (entry.moveset && entry.moveset.length >= 3) {
    // moveset 可能是 display name（如 "Gigaton Hammer*"），需要翻译
    const raw: string[] = entry.moveset;
    const clean = raw.map(m => m.replace(/\*$/, ''));
    return { fast: getMoveCn(clean[0]) || clean[0], charged: clean.slice(1, 3).map(m => getMoveCn(m) || m) };
  }
  const fastSorted = [...(entry.moves?.fastMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  const chargedSorted = [...(entry.moves?.chargedMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  return {
    fast: getMoveCn(fastSorted[0]?.moveId || '') || fastSorted[0]?.moveId || '',
    charged: chargedSorted.slice(0, 2).map((c: any) => getMoveCn(c.moveId) || c.moveId),
  };
}

function loadEliteMoves(): Record<string, string[]> {
  try {
    const path = require('path');
    const fs = require('fs');
    const elitePath = path.resolve(__dirname, '..', 'data', 'elite_moves.json');
    if (fs.existsSync(elitePath)) {
      return JSON.parse(fs.readFileSync(elitePath, 'utf-8'));
    }
  } catch { /* ignore */ }
  return {};
}

function isEliteMove(speciesId: string, moveId: string): boolean {
  const elite = loadEliteMoves();
  const lookups = [speciesId];
  if (speciesId.endsWith('_shadow')) {
    lookups.push(speciesId.slice(0, -7));
  }
  for (const sid of lookups) {
    const moves = elite[sid];
    if (Array.isArray(moves)) {
      for (const em of moves) {
        if (em === moveId) return true;
      }
    }
  }
  return false;
}

interface MissingEntry {
  speciesId: string;
  name: string;
  rank: number;
  score: number;
  fastMove: string;
  chargedMoves: string[];
  needsElite: boolean;
}

/**
 * /pvp 缺什么 主逻辑
 * @param leagueKey 可选联盟
 */
export async function findMissing(leagueKey?: string): Promise<string> {
  const myPokes = loadMyPokemon();
  const leagueKeys = leagueKey ? [leagueKey] : [...LEAGUE_ORDER];

  const lines: string[] = [];
  let anyOutput = false;

  for (const lk of leagueKeys) {
    const rankings = await getRankings(lk);
    if (!rankings || rankings.length === 0) continue;

    const label = LEAGUE_LABELS[lk] || lk;

    // 已有宝可梦的 speciesId 集合
    const ownedIds = new Set(
      myPokes
        .filter(p => p.league === lk)
        .map(p => p.speciesId.toLowerCase())
    );

    const ownedNames: string[] = [];
    const missingList: MissingEntry[] = [];

    // 检查排名前 50
    for (let i = 0; i < Math.min(50, rankings.length); i++) {
      const entry = rankings[i];
      const sid = entry.speciesId.toLowerCase();

      if (ownedIds.has(sid)) {
        ownedNames.push(getSpeciesCn(entry.speciesId) || entry.speciesId);
        continue;
      }

      const moves = getRankingMoves(entry);
      const needsElite =
        isEliteMove(entry.speciesId, moves.fast) ||
        moves.charged.some(m => isEliteMove(entry.speciesId, m));

      missingList.push({
        speciesId: entry.speciesId,
        name: getSpeciesCn(entry.speciesId) || entry.speciesId,
        rank: i + 1,
        score: entry.score,
        fastMove: getMoveCn(moves.fast) || moves.fast,
        chargedMoves: moves.charged.map(m => getMoveCn(m) || m),
        needsElite,
      });
    }

    if (ownedNames.length === 0 && missingList.length === 0) {
      // 这个联盟没有任何数据，跳过
      continue;
    }

    anyOutput = true;
    lines.push(`📦 ${label} 缺少核心`);
    lines.push('');

    // 已有
    lines.push('已有：');
    if (ownedNames.length > 0) {
      for (const n of ownedNames) {
        lines.push(`✅ ${n}`);
      }
    } else {
      lines.push('（暂无）');
    }
    lines.push('');

    // 缺少
    lines.push('缺少：');
    const topMissing = missingList.slice(0, 5);
    for (const m of topMissing) {
      const eliteMark = m.needsElite ? '（需精英招式）' : '';
      lines.push(`❌ ${m.name}（PvPokeTW #${m.rank}）${eliteMark}`);
      lines.push(`  推荐配招：`);
      lines.push(`  小招：${m.fastMove}`);
      lines.push(`  充能1：${m.chargedMoves[0] || '-'}`);
      if (m.chargedMoves.length > 1) {
        lines.push(`  充能2：${m.chargedMoves[1] || '-'}`);
      }
      lines.push('');
    }

    // 下一步建议
    if (topMissing.length > 0) {
      const first = topMissing[0];
      const extra =
        first.needsElite ? '（需准备精英招式）' : '（星尘+糖果即可）';
      lines.push(`下一步建议：优先补 ${first.name} ${extra}`);
    }

    if (leagueKeys.length > 1) {
      lines.push('');
    }
  }

  if (!anyOutput) {
    return '暂无数据，请先拉取排名数据\n或使用 /pvp 添加 录入你的宝可梦';
  }

  // 最后一行多余分隔去掉
  let result = lines.join('\n');
  if (result.endsWith('\n\n')) {
    result = result.trimEnd();
  }

  return result;
}
