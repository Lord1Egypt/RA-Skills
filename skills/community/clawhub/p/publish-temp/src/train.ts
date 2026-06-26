// train.ts — /pvp 值得练：库存培养排序
// 从 my_pokemon.json 筛选最值得培养的宝可梦

import { loadMyPokemon } from './list';
import { getRankings, resolveLeague, loadGamemaster } from './fetcher';
import { findSpeciesId } from './iv';
import { getSpeciesCn, getMoveCn } from './mapper';
import type { MyPokemon } from './add';
import type { PvPokePokemon } from './types';

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
};

const LEAGUE_ORDER = ['1500', '2500', 'master'];

// 精英招式
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
        const cn = getMoveCn(em);
        if (cn === moveId) return true;
      }
    }
  }
  return false;
}

// 从 rankings 中获取推荐配招
function getRankingMoves(entry: PvPokePokemon): { fast: string; charged: string[] } {
  if (entry.moveset && entry.moveset.length >= 3) {
    return { fast: entry.moveset[0], charged: entry.moveset.slice(1, 3) };
  }
  const fastSorted = [...(entry.moves?.fastMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  const chargedSorted = [...(entry.moves?.chargedMoves || [])].sort((a: any, b: any) => b.uses - a.uses);
  return {
    fast: fastSorted[0]?.moveId || '',
    charged: chargedSorted.slice(0, 2).map((c: any) => c.moveId),
  };
}

// 查找宝可梦在 rankings 中的索引和 entry
function findRankingEntry(rankings: PvPokePokemon[], speciesId: string): { entry: PvPokePokemon; rank: number } | null {
  const idx = rankings.findIndex(e => e.speciesId === speciesId);
  if (idx < 0) return null;
  return { entry: rankings[idx], rank: idx + 1 };
}

/**
 * 获取宝可梦在某个联盟的最佳 IV 排名
 * 返回 IV 排名名次（1-based），如果不在前50返回 999
 */
async function getIVRank(speciesId: string, leagueKey: string): Promise<number> {
  try {
    const gm = await loadGamemaster();
    if (!gm) return 999;

    const { getPokemonBase, computeBestIV } = require('./fetcher');
    const base = getPokemonBase(gm, speciesId);
    if (!base) return 999;

    const cpLimit = leagueKey === '1500' ? 1500 : leagueKey === '2500' ? 2500 : 99999;
    if (cpLimit === 99999) return 999; // 大师联盟无 IV 排名

    const ivResult = computeBestIV(base, cpLimit);
    // ivResult.top50 是已排序的前50
    const top50 = ivResult.top50 || [];
    // 查找用户 IV 在 top50 中的位置
    // 先根据 my_pokemon 中的 IV 来找
    const myPokes = loadMyPokemon();
    const myEntry = myPokes.find(p => p.speciesId === speciesId && p.league === leagueKey);
    if (!myEntry) return 999;

    const userIV: [number, number, number] = myEntry.iv;
    for (let i = 0; i < top50.length; i++) {
      if (top50[i].iv[0] === userIV[0] && top50[i].iv[1] === userIV[1] && top50[i].iv[2] === userIV[2]) {
        return i + 1;
      }
    }

    return 999;
  } catch {
    return 999;
  }
}

interface TrainCandidate {
  speciesId: string;
  name: string;
  league: string;
  pvpokeRank: number;
  pvpokeScore: number;
  ivRank: number;
  built: boolean;
  fastMove: string;
  chargedMoves: string[];
  missingMoves: string[];
  score: number;
  suggestion: string;
}

/**
 * /pvp 值得练 主逻辑
 * @param leagueKey 可选联盟，如 '1500'
 */
export async function buildTrainList(leagueKey?: string): Promise<string> {
  const myPokes = loadMyPokemon();
  if (myPokes.length === 0) {
    return '暂无已记录宝可梦\n先去添加吧：/pvp 添加 <宝可梦> <联盟> <IV> <CP> <等级>';
  }

  // 按联盟过滤
  let filtered: MyPokemon[];
  let leagueKeys: string[];
  if (leagueKey) {
    filtered = myPokes.filter(p => p.league === leagueKey);
    leagueKeys = [leagueKey];
  } else {
    filtered = myPokes;
    leagueKeys = LEAGUE_ORDER.filter(lk => myPokes.some(p => p.league === lk));
  }

  if (filtered.length === 0) {
    const label = leagueKey ? (LEAGUE_LABELS[leagueKey] || leagueKey) : '';
    return `${label ? label + ' ' : ''}暂无已记录宝可梦`;
  }

  // 加载所有联盟的 rankings
  const rankingsMap: Record<string, PvPokePokemon[]> = {};
  for (const lk of leagueKeys) {
    try {
      const ranks = await getRankings(lk);
      if (ranks && ranks.length > 0) rankingsMap[lk] = ranks;
    } catch { /* ignore */ }
  }

  const gm = await loadGamemaster();

  const candidates: TrainCandidate[] = [];

  for (const poke of filtered) {
    const lk = poke.league;
    const rankings = rankingsMap[lk];
    if (!rankings || rankings.length === 0) continue;

    const rankingInfo = findRankingEntry(rankings, poke.speciesId);
    if (!rankingInfo) continue; // 物种不在排名中，跳过

    const entry = rankingInfo.entry;
    const pvpokeRank = rankingInfo.rank;
    const moves = getRankingMoves(entry);

    // 计算 IV 排名
    let ivRank = 999;
    try {
      if (lk !== 'master' && gm) {
        const { getPokemonBase, computeBestIV } = require('./fetcher');
        const base = getPokemonBase(gm, poke.speciesId);
        if (base) {
          const cpLimit = lk === '1500' ? 1500 : 2500;
          const ivResult = computeBestIV(base, cpLimit);
          const top50 = ivResult.top50 || [];
          for (let i = 0; i < top50.length; i++) {
            if (top50[i].iv[0] === poke.iv[0] && top50[i].iv[1] === poke.iv[1] && top50[i].iv[2] === poke.iv[2]) {
              ivRank = i + 1;
              break;
            }
          }
        }
      }
    } catch { /* ignore */ }

    // 配招缺口对比
    const userMoves = new Set(poke.moves.map(m => m.toUpperCase()));
    const missingMoves: string[] = [];
    const allRecMoves = [moves.fast, ...moves.charged];
    for (const recMove of allRecMoves) {
      if (!recMove) continue;
      const recUpper = recMove.toUpperCase();
      // 用户的招式可能是中文，也可能是英文 ID
      const recCn = getMoveCn(recUpper);
      const found =
        userMoves.has(recUpper) ||
        userMoves.has(recCn) ||
        (recCn && userMoves.has(recCn));
      if (!found) {
        missingMoves.push(recCn || recUpper);
      }
    }

    // ⭐ 加权评分（范围 0~100）
    let score = 0;

    // 物种排名分（0~40）：rank #1 = 40, rank #50 = 20, rank #100 = 0, rank > 200 = 0
    const rankScore = Math.max(0, 40 - (pvpokeRank - 1) * 0.4);
    score += rankScore;

    // IV 排名分（0~25）
    if (ivRank <= 50) {
      const ivScore = Math.max(0, 25 - (ivRank - 1) * 0.5);
      score += ivScore;
    }

    // 已培养状态（-15 ~ +15）
    if (!poke.built) {
      score += 15;
    } else {
      score -= 10;
    }

    // 缺配招（0~10）
    score += Math.min(10, missingMoves.length * 3);
    if (missingMoves.some(m => isEliteMove(poke.speciesId, m))) {
      score += 5; // 精英招额外加分
    }

    // 配队需求（0~10）：判断是否在推荐队伍中出现
    // 简化：排名前 30 的给 5 分，前 10 给 10 分
    if (pvpokeRank <= 10) score += 10;
    else if (pvpokeRank <= 30) score += 5;

    // 建议文案
    let suggestion = '';
    if (!poke.built && pvpokeRank <= 10 && ivRank <= 10) suggestion = '⭐ 优先培养';
    else if (!poke.built && (pvpokeRank <= 30 || ivRank <= 30)) suggestion = '推荐培养';
    else if (!poke.built) suggestion = '值得培养';
    else if (missingMoves.length > 0) suggestion = '更新配招';
    else suggestion = '可用 ✓';

    candidates.push({
      speciesId: poke.speciesId,
      name: getSpeciesCn(poke.speciesId) || poke.speciesId,
      league: lk,
      pvpokeRank,
      pvpokeScore: entry.score,
      ivRank,
      built: poke.built,
      fastMove: getMoveCn(moves.fast) || moves.fast,
      chargedMoves: moves.charged.map(m => getMoveCn(m) || m),
      missingMoves,
      score: Math.round(score),
      suggestion,
    });
  }

  // 排序：按分数降序
  candidates.sort((a, b) => b.score - a.score);

  // 输出
  const lines: string[] = [];

  // 按联盟分组输出
  const groups: Record<string, TrainCandidate[]> = {};
  for (const c of candidates) {
    if (!groups[c.league]) groups[c.league] = [];
    groups[c.league].push(c);
  }

  for (const lk of LEAGUE_ORDER) {
    const group = groups[lk];
    if (!group || group.length === 0) continue;

    const label = LEAGUE_LABELS[lk] || lk;
    lines.push(`🔥 值得练 | ${label}`);
    lines.push('');

    let idx = 1;
    for (const c of group) {
      const ivStr = (() => {
        const myPokes = loadMyPokemon();
        const p = myPokes.find(m => m.speciesId === c.speciesId && m.league === c.league);
        if (!p) return '-';
        const ivText = `${p.iv[0]}/${p.iv[1]}/${p.iv[2]}`;
        if (c.league === 'master') return ivText + '（大师联盟默认）';
        return ivText + (c.ivRank <= 50 ? `（#${c.ivRank}）` : '（未入前50）');
      })();

      const ivDetail = c.league !== 'master'
        ? `   IV排名：${c.ivRank <= 50 ? '#' + c.ivRank : '未进入前50'}`
        : '   IV排名：大师联盟默认';

      const builtStr = c.built ? '✅ 已培养' : '⏳ 未培养';

      const movesLines = [];
      movesLines.push(`   推荐配招：`);
      movesLines.push(`   小招：${c.fastMove}`);
      movesLines.push(`   充能1：${c.chargedMoves[0] || '-'}`);
      if (c.chargedMoves.length > 1) {
        movesLines.push(`   充能2：${c.chargedMoves[1] || '-'}`);
      }

      lines.push(`${idx}. ${c.name}`);
      lines.push(`   PvPokeTW：#${c.pvpokeRank}（评分 ${c.pvpokeScore}）`);
      lines.push(`   IV：${ivStr}`);
      lines.push(ivDetail);
      lines.push(`   状态：${builtStr}`);
      for (const ml of movesLines) lines.push(ml);
      if (c.missingMoves.length > 0) {
        lines.push(`   ⚠️ 缺少：${c.missingMoves.join('、')}`);
      }
      lines.push(`   建议：${c.suggestion}`);
      lines.push('');

      idx++;
    }
  }

  return lines.join('\n');
}
