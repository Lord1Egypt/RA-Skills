// list.ts — /pvp 我的：列出我的宝可梦

import * as fs from 'fs';
import * as path from 'path';
import { MyPokemon } from './add';

const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'my_pokemon.json');

/** 从文件加载宝可梦列表 */
export function loadMyPokemon(): MyPokemon[] {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw) as MyPokemon[];
    }
  } catch {
    // 文件损坏则重置
  }
  return [];
}

/** 验证联盟 */
function resolveLeague(input: string): string | null {
  const map: Record<string, string> = {
    '1500' : '1500', '超级' : '1500', '超级联盟' : '1500',
    '2500' : '2500', '高级' : '2500', '高级联盟' : '2500',
    'master' : 'master', '大师' : 'master', '大师联盟' : 'master', '无限制' : 'master',
    '484' : '484', '小小' : '484', '小小杯' : '484', '幼童' : '484',
  };
  return map[input.trim()] || null;
}

const LEAGUE_LABELS: Record<string, string> = {
  '1500': '超级联盟',
  '2500': '高级联盟',
  'master': '大师联盟',
  '484': '小小杯',
};

/**
 * /pvp 我的 命令入口
 * args: [] 或 [联盟]
 */
export function handleList(args: string[]): string {
  const all = loadMyPokemon();

  if (all.length === 0) {
    return '暂无已记录宝可梦\n使用 /pvp 添加 录入你的宝可梦';
  }

  let filtered = all;
  let filterLabel = '';

  if (args.length > 0 && args[0].trim() !== '') {
    const league = resolveLeague(args[0]);
    if (!league) {
      return `未知联盟: ${args[0]}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`;
    }
    filtered = all.filter(p => p.league === league);
    filterLabel = LEAGUE_LABELS[league] || league;

    if (filtered.length === 0) {
      return `暂无 ${filterLabel} 的已记录宝可梦`;
    }
  }

  // 按联盟分组排序（超级 → 高级 → 大师）
  const leagueOrder = ['484', '1500', '2500', 'master'];
  const grouped: Record<string, MyPokemon[]> = { '1500': [], '2500': [], 'master': [] };
  for (const p of filtered) {
    if (!grouped[p.league]) grouped[p.league] = [];
    grouped[p.league].push(p);
  }

  const lines: string[] = [];
  let firstGroup = true;

  for (const lk of leagueOrder) {
    const group = grouped[lk];
    if (!group || group.length === 0) continue;

    const label = LEAGUE_LABELS[lk] || lk;
    const builtCount = group.filter(p => p.built).length;
    const pendingCount = group.length - builtCount;

    // 组标题 + 统计
    if (!firstGroup) lines.push('');
    lines.push(`📦 ${label} 库存  (共 ${group.length} 只  ✅已培养 ${builtCount}  ⏳待培养 ${pendingCount})`);
    lines.push('');

    for (const p of group) {
      const ivStr = `${p.iv[0]}/${p.iv[1]}/${p.iv[2]}`;
      const builtStr = p.built ? '✅ 已培养' : '⏳ 未培养';
      const noteStr = p.note ? `\n备注：${p.note}` : '';

      lines.push(`📘 ${p.name}｜${label}`);
      lines.push(`   IV：${ivStr}`);
      lines.push(`   CP：${p.cp} ｜ Lv${p.level}`);
      lines.push(`   状态：${builtStr}${noteStr}`);
    }

    firstGroup = false;
  }

  return lines.join('\n');
}
