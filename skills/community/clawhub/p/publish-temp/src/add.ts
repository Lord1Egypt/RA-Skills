// add.ts — /pvp 添加：录入我的宝可梦到 data/my_pokemon.json

import * as fs from 'fs';
import * as path from 'path';
import { findSpeciesId } from './iv';
import { getSpeciesCn } from './mapper';

const DATA_DIR = path.resolve(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'my_pokemon.json');

export interface MyPokemon {
  name: string;                    // 中文名
  speciesId: string;               // PvPoke 英文 ID
  league: string;                  // "1500" / "2500" / "master"
  iv: [number, number, number];    // [攻IV, 防IV, 血IV]
  cp: number;                      // 当前 CP
  level: number;                   // 当前等级（支持小数）
  moves: string[];                 // 招式列表（可选）
  built: boolean;                  // 是否已培养
  note: string;                    // 备注
  createdAt: string;               // ISO 8601
  updatedAt: string;               // ISO 8601
}

interface AddPokemonInput {
  pokemon: string;                 // 用户输入的中文名
  league: string;                  // 联盟
  iv: [number, number, number];    // IV
  cp: number;                      // CP
  level: number;                   // 等级
  moves?: string[];                // 招式（可选）
  built?: boolean;                 // 是否已培养
  note?: string;                   // 备注
}

/** 解析 IV 字符串 "a/d/h" → [a,d,h] */
export function parseAddIV(input: string): [number, number, number] | null {
  const parts = input.trim().split('/');
  if (parts.length !== 3) return null;
  const a = parseInt(parts[0], 10);
  const d = parseInt(parts[1], 10);
  const s = parseInt(parts[2], 10);
  if (isNaN(a) || isNaN(d) || isNaN(s)) return null;
  if (a < 0 || a > 15 || d < 0 || d > 15 || s < 0 || s > 15) return null;
  return [a, d, s];
}

/** 校验等级（支持小数） */
function validateLevel(input: string): number | null {
  const lv = parseFloat(input);
  if (isNaN(lv)) return null;
  if (lv < 1 || lv > 51) return null;
  return lv;
}

/** 校验 CP */
function validateCP(input: string): number | null {
  const cp = parseInt(input, 10);
  if (isNaN(cp)) return null;
  if (cp < 10) return null;
  return cp;
}

/** 校验联盟 */
function validateLeague(input: string): string | null {
  const map: Record<string, string> = {
    '1500' : '1500', '超级' : '1500', '超级联盟' : '1500',
    '2500' : '2500', '高级' : '2500', '高级联盟' : '2500',
    'master' : 'master', '大师' : 'master', '大师联盟' : 'master', '无限制' : 'master',
    '484' : '484', '小小' : '484', '小小杯' : '484', '幼童' : '484',
  };
  return map[input.trim()] || null;
}

/** 从文件加载宝可梦列表 */
function loadMyPokemon(): MyPokemon[] {
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

/** 保存到文件 */
function saveMyPokemon(list: MyPokemon[]): void {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  fs.writeFileSync(DATA_FILE, JSON.stringify(list, null, 2), 'utf-8');
}

/**
 * 添加宝可梦
 * 同一 speciesId + league + iv 视为重复 → 覆盖 CP/level/updatedAt
 * 否则新增
 */
export function addPokemon(input: AddPokemonInput): {
  success: boolean;
  message: string;
  pokemon: MyPokemon;
  isUpdate: boolean;
} {
  const now = new Date().toISOString();

  const entry: MyPokemon = {
    name: getSpeciesCn(input.pokemon) || input.pokemon,
    speciesId: input.pokemon,  // 已经是由 findSpeciesId 转换后的 speciesId
    league: input.league,
    iv: input.iv,
    cp: input.cp,
    level: input.level,
    moves: input.moves || [],
    built: input.built || false,
    note: input.note || '',
    createdAt: now,
    updatedAt: now,
  };

  const list = loadMyPokemon();

  // 查找重复：同 speciesId + league + iv（三个条件都匹配）
  const existingIdx = list.findIndex(
    (p) => p.speciesId === entry.speciesId
        && p.league === entry.league
        && p.iv[0] === entry.iv[0]
        && p.iv[1] === entry.iv[1]
        && p.iv[2] === entry.iv[2]
  );

  let isUpdate = false;
  if (existingIdx >= 0) {
    // 覆盖已有
    const existing = list[existingIdx];
    existing.cp = entry.cp;
    existing.level = entry.level;
    if (entry.moves.length > 0) existing.moves = entry.moves;
    existing.note = entry.note || existing.note;
    existing.updatedAt = now;
    entry.createdAt = existing.createdAt;
    isUpdate = true;
    list[existingIdx] = existing;
  } else {
    list.push(entry);
  }

  saveMyPokemon(list);

  return {
    success: true,
    message: isUpdate
      ? `已更新 ${entry.name} (${entry.league})`
      : `已添加 ${entry.name} (${entry.league})`,
    pokemon: existingIdx >= 0 ? list[existingIdx] : entry,
    isUpdate,
  };
}

/**
 * /pvp 添加 命令入口
 * 参数：[宝可梦, 联盟, IV, CP, 等级]
 */
export async function handleAdd(args: string[]): Promise<string> {
  if (args.length < 5) {
    return '用法：/pvp 添加 <宝可梦> <联盟> <攻击/防御/生命> <CP> <等级> [招式1/招式2/招式3]\n示例：/pvp 添加 胖嘟嘟 1500 1/14/14 1498 24.5\n      /pvp 添加 土龙弟弟 1500 0/14/12 1157 27 咬住/岩崩';
  }

  const pokemonInput = args[0];
  const leagueInput = args[1];
  const ivInput = args[2];
  const cpInput = args[3];
  const levelInput = args[4];

  // 校验联盟
  const league = validateLeague(leagueInput);
  if (!league) {
    return `未知联盟: ${leagueInput}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`;
  }

  // 校验 IV
  const iv = parseAddIV(ivInput);
  if (!iv) {
    return `IV 格式错误: ${ivInput}，正确格式如 1/14/14`;
  }

  // 校验 CP
  const cp = validateCP(cpInput);
  if (!cp) {
    return `CP 格式错误: ${cpInput}`;
  }

  // 校验 CP 上限
  const cpLimit = league === '1500' ? 1500 : league === '2500' ? 2500 : league === '484' ? 484 : 99999;
  if (cp > cpLimit) {
    return `CP ${cp} 超出 ${league === 'master' ? '大师' : league === '1500' ? '超级' : '高级'}联盟上限 (${cpLimit})`;
  }

  // 校验等级
  const level = validateLevel(levelInput);
  if (!level) {
    return `等级格式错误: ${levelInput}，有效范围 1~51`;
  }

  // 查找 speciesId（复用 iv.ts 中的 findSpeciesId）
  const speciesIds = findSpeciesId(pokemonInput);
  if (speciesIds.length === 0) {
    return `未找到宝可梦: ${pokemonInput}`;
  }

  const speciesId = speciesIds[0];

  // 解析配招（可选参数，args[5] 以后是招式，用 / 分隔）
  const movesInput = args.slice(5).join('');
  const moves = movesInput ? movesInput.split('/').filter(m => m.trim().length > 0).map(m => m.trim()) : [];

  // 添加
  const result = addPokemon({
    pokemon: speciesId,
    league,
    iv,
    cp,
    level,
    moves,
  });

  // 读取最新文件内容用于输出
  const fileContent = loadMyPokemon();

  const lines: string[] = [];
  lines.push(`✅ ${result.message}`);
  const movesLine = moves.length > 0 ? ` 招式: ${moves.join('/')}` : '';
  lines.push(`   IV: ${iv[0]}/${iv[1]}/${iv[2]}  CP: ${cp}  Lv: ${level}${movesLine ? ' ｜' + movesLine : ''}`);
  lines.push('');
  lines.push(`data/my_pokemon.json 当前 ${fileContent.length} 条记录:`);
  for (const p of fileContent) {
    const builtMark = p.built ? '✅' : '⏳';
    const m = p.moves.length > 0 ? ` 招式: ${p.moves.join('/')}` : '';
    lines.push(`   ${builtMark} ${p.name} (${p.league}) IV=${p.iv[0]}/${p.iv[1]}/${p.iv[2]} CP=${p.cp} Lv=${p.level}${m ? ' ｜' + m : ''}`);
  }

  return lines.join('\n');
}
