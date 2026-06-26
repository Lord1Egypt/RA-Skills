// iv.ts — /pvp iv 命令：宝可梦 IV 排名查询
// 符合 PvPoke 精确算法：HP floor SP 排序 + 同 SP 按 ATK IV 小优先

import {
  resolveLeague, loadGamemaster, getPokemonBase,
  computeBestIV, parseUserIV, findUserIVInResults,
  computeUserIV, computeIVDiff,
} from './fetcher';
import { getSpeciesCn, SPECIES_CN } from './mapper';

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  master: '大师联盟',
};

interface IVOutput {
  pokemon: string;
  league: string;
  best: { iv: string; cp: number; level: number };
  user: { iv: string; rank: number; cp: number; level: number; diff: { atk: number; def: number; hp: number } } | null;
}

/**
 * 查询宝可梦 IV 排名
 * @param pokemonInput 中文宝可梦名称
 * @param leagueInput  1500 / 2500 / master
 * @param userIVStr    "攻击/防御/生命"（可选）
 * @param speciesId    已知英文 speciesId（可选，用于别名查找）
 * @returns IVOutput 或错误信息
 */
export async function queryIV(
  pokemonInput: string,
  leagueInput: string,
  userIVStr?: string,
): Promise<IVOutput | { error: string }> {
  const leagueKey = resolveLeague(leagueInput);
  if (!leagueKey) {
    return { error: `未知联盟: ${leagueInput}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）` };
  }

  if (leagueKey === 'master') {
    return {
      error: `${getSpeciesCn(pokemonInput) || pokemonInput} - 大师联盟\n最佳 IV：15/15/15（大师联盟默认）\n大师联盟不提供 IV 排名`,
    };
  }

  // 通过 findSpeciesId 找宝可梦
  const speciesIds = findSpeciesId(pokemonInput);
  if (speciesIds.length === 0) {
    return { error: `未找到宝可梦: ${pokemonInput}` };
  }

  const gm = await loadGamemaster();
  if (!gm) {
    return { error: '无法加载 gamemaster 数据' };
  }

  const base = getPokemonBase(gm, speciesIds[0]);
  if (!base) {
    return { error: `gamemaster 中未找到 ${pokemonInput} 的基础数据` };
  }

  const cpLimit = leagueKey === '1500' ? 1500 : 2500;
  const ivResult = computeBestIV(base, cpLimit);

  const name = getSpeciesCn(speciesIds[0]) || speciesIds[0];
  const league = LEAGUE_LABELS[leagueKey] || leagueKey;

  const output: IVOutput = {
    pokemon: name,
    league,
    best: {
      iv: `${ivResult.best.iv[0]}/${ivResult.best.iv[1]}/${ivResult.best.iv[2]}`,
      cp: ivResult.best.cp,
      level: ivResult.best.level,
    },
    user: null,
  };

  if (userIVStr) {
    const parsed = parseUserIV(userIVStr);
    if (!parsed) {
      return { error: `IV 格式错误: ${userIVStr}，正确格式如 1/14/14` };
    }

    // 查找用户 IV 在排名中的位置
    const foundInTop = findUserIVInResults(parsed, ivResult);
    const diff = computeIVDiff(ivResult.best.iv, parsed);

    let record;
    let rank;
    if (foundInTop.record) {
      record = foundInTop.record;
      rank = record.rank;
    } else {
      // 不在前 50 名，单独计算 CP/等级
      record = computeUserIV(base, parsed, cpLimit);
      rank = 9999; // 表示为「未进入前 50」
    }

    output.user = {
      iv: `${parsed[0]}/${parsed[1]}/${parsed[2]}`,
      rank,
      cp: record.cp,
      level: record.level,
      diff,
    };
  }

  return output;
}

/**
 * 格式化 IV 输出
 */
export function formatIVOutput(output: IVOutput | { error: string }): string {
  if ('error' in output) {
    return output.error;
  }

  const o = output;
  const lines: string[] = [];

  lines.push(`宝可梦    ${o.pokemon}`);
  lines.push(`联盟      ${o.league}`);
  lines.push('');

  if (!o.user) {
    // 无用户 IV：只显示最佳
    lines.push('--- 最佳 IV ---');
    lines.push(`最佳 IV    ${o.best.iv}`);
    lines.push(`最佳 CP    ${o.best.cp}`);
    lines.push(`最佳等级   ${o.best.level}`);
  } else {
    // 有用户 IV：显示最佳 + 用户对比
    lines.push('--- 最佳 IV ---');
    lines.push(`最佳 IV    ${o.best.iv}`);
    lines.push(`最佳 CP    ${o.best.cp}`);
    lines.push(`最佳等级   ${o.best.level}`);
    lines.push('');
    lines.push('--- 我的宝可梦 ---');
    lines.push(`我的 IV    ${o.user.iv}`);
    if (o.user.rank < 9999) {
      lines.push(`我的排名   #${o.user.rank}`);
    } else {
      lines.push('我的排名   未进入前 50 名');
    }
    lines.push(`我的 CP    ${o.user.cp}`);
    lines.push(`我的等级   ${o.user.level}`);
    lines.push('');
    lines.push('--- 与最佳 IV 差别 ---');
    lines.push(`攻击       ${formatDiff(o.user.diff.atk)}`);
    lines.push(`防御       ${formatDiff(o.user.diff.def)}`);
    lines.push(`生命       ${formatDiff(o.user.diff.hp)}`);
  }

  return lines.join('\n');
}

function formatDiff(val: number): string {
  if (val === 0) return '0';
  if (val > 0) return `+${val}`;
  return `${val}`;
}

/** 简化版 findSpeciesId —— 与 query.ts 保持一致逻辑 */
export function findSpeciesId(userInput: string): string[] {
  const input = userInput.trim();
  const fs = require('fs');
  const path = require('path');
  const ALIAS_PATH = path.resolve(__dirname, '..', 'data', 'pokemon_alias.json');

  let aliases: Record<string, any> = {};
  try {
    if (fs.existsSync(ALIAS_PATH)) {
      aliases = JSON.parse(fs.readFileSync(ALIAS_PATH, 'utf-8'));
    }
  } catch { /* ignore */ }

  // 繁简归一化 — 在最前面定义，供后续所有阶段使用
  const simpMap: Record<string, string> = {
    '棄': '弃', '戰': '战', '體': '体', '靈': '灵', '鬥': '斗', '無': '无',
    '關': '关', '對': '对', '擊': '击', '龍': '龙', '惡': '恶', '鋼': '钢',
    '蟲': '虫', '雲': '云', '魚': '鱼', '鳥': '鸟', '龜': '龟', '雞': '鸡',
    '鴨': '鸭', '鵝': '鹅', '鷹': '鹰', '鶴': '鹤', '麗': '丽', '飛': '飞',
    '驚': '惊', '彈': '弹', '電': '电', '塵': '尘', '頭': '头', '聲': '声',
    '響': '响', '劍': '剑', '獸': '兽', '愛': '爱', '偽': '伪', '鴉': '鸦',
    '鬱': '郁', '癒': '愈', '曆': '历', '鳳': '凤', '貓': '猫', '獅': '狮',
    '獨': '独', '學': '学', '儀': '仪', '擔': '担', '勁': '劲', '葉': '叶',
    '圓': '圆', '圖': '图', '號': '号', '門': '门', '種': '种', '驗': '验',
    '變': '变', '隱': '隐', '發': '发', '導': '导', '內': '内', '殼': '壳',
    '單': '单', '開': '开',
  };
  const simplify = (s: string) => s.replace(/[棄戰體靈鬥無關對擊龍惡鋼蟲雲魚鳥龜雞鴨鵝鷹鶴麗飛驚彈電塵頭聲響劍獸愛偽鴉鬱癒曆鳳貓獅獨學儀擔勁葉圓圖號門種驗變隱發導內殼單開]/g,
    (m: string) => simpMap[m] || m
  );

  // 构建中文→英文反向映射（从 SPECIES_CN）
  function buildCnToEn(): Record<string, string> {
    const map: Record<string, string> = {};
    for (const [en, cn] of Object.entries(SPECIES_CN)) {
      map[cn] = en;
    }
    return map;
  }
  const cnToEn = buildCnToEn();

  // 辅助：中文→英文转换（如果已知是中文则转，否则原样返回）
  function toEn(sid: string): string {
    const en = cnToEn[sid];
    if (en) return en;
    const en2 = cnToEn[simplify(sid)];
    if (en2) return en2;
    return sid;
  }

  // 收集 knownIds
  const knownIds = new Set<string>();
  ['1500', '2500', 'master'].forEach((lk) => {
    try {
      const cacheFile = path.resolve(__dirname, '..', 'cache', `rankings-${lk === 'master' ? 'master' : lk}.json`);
      if (fs.existsSync(cacheFile)) {
        const data = JSON.parse(fs.readFileSync(cacheFile, 'utf-8')) as any[];
        data.forEach((p: any) => knownIds.add(p.speciesId));
      }
    } catch { /* */ }
  });

  // 直接匹配 knownIds
  const lower = input.toLowerCase();
  for (const sid of knownIds) {
    if (sid.toLowerCase() === lower) {
      return [toEn(sid)];
    }
  }

  // 别名映射 — 直接返回映射值（不校验 knownIds，因为别名指向 PvPoke 英文 ID）
  for (const [cn, sid] of Object.entries(aliases)) {
    if (cn === input) {
      const targetIds = typeof sid === 'string' ? [sid] : (Array.isArray(sid) ? sid : [sid]);
      return targetIds;
    }
  }

  // 前缀匹配
  for (const sid of knownIds) {
    if (sid.toLowerCase().startsWith(lower) || lower.startsWith(sid.toLowerCase())) return [toEn(sid)];
  }

  // 繁简归一化
  const simpInput = simplify(input);
  for (const sid of knownIds) {
    if (simplify(sid) === simpInput) return [toEn(sid)];
  }

  // 通过 getSpeciesCn 反向查找（knownIds 中的英文 ID → 中文名）
  for (const sid of knownIds) {
    const cn = getSpeciesCn(sid);
    if (cn === input) return [sid]; // sid 是英文，直接返回
  }
  // 中文名包含匹配
  for (const sid of knownIds) {
    const cn = getSpeciesCn(sid);
    if (cn.includes(input) || input.includes(cn)) return [sid]; // sid 是英文，直接返回
  }

  return [];
}
