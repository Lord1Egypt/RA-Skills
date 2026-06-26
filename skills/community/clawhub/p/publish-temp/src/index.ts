// index.ts — OpenClaw 命令入口（/pvp 培养 + 配队）v1.1
// 数据源：PvPokeTW（见 https://pvpoketw.com/）

import { parseCommand, queryPokemon } from './query';
import { queryIV, formatIVOutput } from './iv';
import { handleAdd } from './add';
import { handleList } from './list';
import { handleEvaluate } from './evaluate';
import { buildTeam } from './team';
import { buildTrainList } from './train';
import { buildOrderList } from './buildOrder';
import { findMissing } from './missing';
import { getSpeciesCn, getMoveCn } from './mapper';
import { QueryResult } from './types';

interface OpenClawContext {
  args: string[];
  reply: (text: string) => void;
}

const TYPE_CN: Record<string, string> = {
  Normal: '一般', Fire: '火', Water: '水', Electric: '电', Grass: '草',
  Ice: '冰', Fighting: '格斗', Poison: '毒', Ground: '地面', Flying: '飞行',
  Psychic: '超能力', Bug: '虫', Rock: '岩石', Ghost: '幽灵', Dragon: '龙',
  Dark: '恶', Steel: '钢', Fairy: '妖精',
};

function toTypeCn(typeEn: string): string {
  // 首字母大写后查表，兼容 "fighting" 和 "Fighting"
  const normalized = typeEn.charAt(0).toUpperCase() + typeEn.slice(1).toLowerCase();
  return TYPE_CN[normalized] || typeEn;
}

function resolveLeagueCmd(input: string): string | null {
  const map: Record<string, string> = {
    '1500': '1500', '超级': '1500', '超级联盟': '1500',
    '2500': '2500', '高级': '2500', '高级联盟': '2500',
    'master': 'master', '大师': 'master', '大师联盟': 'master', '无限制': 'master',
  };
  return map[input.trim()] || null;
}

/** 格式化查询结果为可读文本 */
function formatResult(result: QueryResult): string {
  // 属性中文化
  const typeCn = (result.types || [])
    .filter(t => t && t !== 'none' && t !== 'None')
    .map(toTypeCn);

  // 招式显示 — 多行格式
  const fastMove = result.recommendedMoves.length >= 1 ? result.recommendedMoves[0] : (result.fastMoves?.[0] || '');
  const chargedMoves = result.recommendedMoves.length >= 3
    ? [result.recommendedMoves[1], result.recommendedMoves[2]]
    : result.chargeMoves?.slice(0, 2) || [];
  const movesDisplay = fastMove
    ? `：\n  小招：${fastMove}\n  充能招1：${chargedMoves[0] || '-'}\n  充能招2：${chargedMoves[1] || '-'}`
    : (result.fastMoves.concat(result.chargeMoves).join(' / '));

  // 表格布局（不使用 markdown 表格，用对齐格式）
  const rows: string[] = [];
  const pad = (label: string, val: string) => `${label}    ${val}`;

  rows.push('┌──────────┬──────────────────────────────┐');
  rows.push(pad('宝可梦', result.pokemon));
  rows.push(pad('联盟', result.league));
  rows.push(pad('排名', `#${result.rank}`));
  rows.push(pad('评分', `${result.score}`));
  rows.push(pad('属性', typeCn.join(' / ')));
  rows.push(pad('CP', result.cp > 0 ? `${result.cp}` : '-'));
  rows.push(pad('等级', result.level > 0 ? `${result.level}` : '-'));
  rows.push(`推荐配招${movesDisplay}`);
  if (result.bestIV) {
    rows.push(pad('最佳IV', result.bestIV.iv.join('/')));
    rows.push(pad('最佳CP', `${result.bestIV.cp}`));
    rows.push(pad('最佳等级', `${result.bestIV.level}`));
  }
  if (result.userIV) {
    rows.push(pad('---', ''));
    rows.push(pad('我的IV', result.userIV.iv));
    if (result.userIV.record) {
      rows.push(pad('我的CP', `${result.userIV.record.cp}`));
      rows.push(pad('我的等级', `${result.userIV.record.level}`));
    }
    if (result.userIV.inTop50) {
      rows.push(pad('我的排名', `#${result.userIV.record!.rank}`));
    } else {
      rows.push(pad('我的排名', '未进入前50'));
    }
  }
  rows.push('');
  rows.push(pad('来源', result.source));
  rows.push(pad('更新时间', result.fetchedAt));

  return rows.join('\n');
}

/**
 * OpenClaw 命令处理器
 */
export async function handlePvp(context: OpenClawContext): Promise<void> {
  const args = context.args;

  // /pvp 评估我的 <联盟>
  if (args.length >= 2 && args[0].toLowerCase() === '评估' && args[1].toLowerCase() === '我的') {
    const evalArgs = args.slice(2);
    const text = await handleEvaluate(evalArgs);
    context.reply(text);
    return;
  }

  // /pvp 我的 [联盟]
  if (args.length >= 1 && args[0].toLowerCase() === '我的') {
    const listArgs = args.slice(1);
    const text = handleList(listArgs);
    context.reply(text);
    return;
  }

  // /pvp 添加 <宝可梦> <联盟> <IV> <CP> <等级>
  if (args.length >= 1 && args[0].toLowerCase() === '添加') {
    const addArgs = args.slice(1);
    const text = await handleAdd(addArgs);
    context.reply(text);
    return;
  }

  // /pvp iv <宝可梦> <联盟> [?攻击/防御/生命]
  if (args.length >= 1 && args[0].toLowerCase() === 'iv') {
    const ivArgs = args.slice(1);
    if (ivArgs.length < 2) {
      context.reply('用法：/pvp iv <宝可梦> <联盟> [攻击/防御/生命]\n示例：/pvp iv 胖嘟嘟 1500\n      /pvp iv 胖嘟嘟 1500 1/14/14');
      return;
    }
    const pokemon = ivArgs[0];
    const league = ivArgs[1];
    const userIV = ivArgs.length >= 3 ? ivArgs[2] : undefined;

    const result = await queryIV(pokemon, league, userIV);
    const text = formatIVOutput(result);
    context.reply(text);
    return;
  }

  // /pvp 值得练 [联盟]
  if (args.length >= 1 && args[0].toLowerCase() === '值得练') {
    const trainArgs = args.slice(1);
    if (trainArgs.length >= 1 && trainArgs[0].trim() !== '') {
      const leagueKey = resolveLeagueCmd(trainArgs[0]);
      if (!leagueKey) {
        context.reply(`未知联盟: ${trainArgs[0]}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`);
        return;
      }
      const text = await buildTrainList(leagueKey);
      context.reply(text);
      return;
    }
    const text = await buildTrainList();
    context.reply(text);
    return;
  }

  // /pvp 培养顺序 [联盟]
  if (args.length >= 1 && args[0].toLowerCase() === '培养顺序') {
    const orderArgs = args.slice(1);
    if (orderArgs.length >= 1 && orderArgs[0].trim() !== '') {
      const leagueKey = resolveLeagueCmd(orderArgs[0]);
      if (!leagueKey) {
        context.reply(`未知联盟: ${orderArgs[0]}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`);
        return;
      }
      const text = await buildOrderList(leagueKey);
      context.reply(text);
      return;
    }
    const text = await buildOrderList();
    context.reply(text);
    return;
  }

  // /pvp 缺什么 [联盟]
  if (args.length >= 1 && args[0].toLowerCase() === '缺什么') {
    const missingArgs = args.slice(1);
    if (missingArgs.length >= 1 && missingArgs[0].trim() !== '') {
      const leagueKey = resolveLeagueCmd(missingArgs[0]);
      if (!leagueKey) {
        context.reply(`未知联盟: ${missingArgs[0]}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`);
        return;
      }
      const text = await findMissing(leagueKey);
      context.reply(text);
      return;
    }
    const text = await findMissing();
    context.reply(text);
    return;
  }

  // /pvp 配队 <联盟> [?核心宝可梦]
  if (args.length >= 1 && args[0].toLowerCase() === '配队') {
    const teamArgs = args.slice(1);
    if (teamArgs.length < 1) {
      context.reply('用法：/pvp 配队 <联盟> [核心宝可梦]\n示例：/pvp 配队 1500\n      /pvp 配队 1500 胖嘟嘟\n      /pvp 配队 master 固拉多');
      return;
    }
    const leagueInput = teamArgs[0];
    const leagueKey = resolveLeagueCmd(leagueInput);
    if (!leagueKey) {
      context.reply(`未知联盟: ${leagueInput}，支持 1500（超级联盟）/ 2500（高级联盟）/ master（大师联盟）`);
      return;
    }
    const coreInput = teamArgs.length >= 2 ? teamArgs.slice(1).join(' ') : undefined;
    const text = await buildTeam(leagueKey, coreInput);
    context.reply(text);
    return;
  }

  // 原有 /pvp 培养 逻辑
  const parsed = parseCommand(args);

  if (!parsed.valid) {
    let msg = parsed.error || '参数错误';
    if (parsed.suggestions && parsed.suggestions.length > 0) {
      msg += `\n可用联盟：${parsed.suggestions.join('、')}`;
    }
    context.reply(msg);
    return;
  }

  const result = await queryPokemon(parsed.pokemon, parsed.league, parsed.userIV);

  if ('error' in result) {
    context.reply(result.error);
    return;
  }

  const text = formatResult(result);
  context.reply(text);
}

// 命令行测试入口
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === '--test') {
    const testCases: [string, string, string?][] = [
      ['大舌舔', '1500'],
      ['弃世猴', '1500'],
      ['胖嘟嘟', '1500'],
      ['玛力露丽', '1500'],
      ['未知宝可梦', '1500'],
    ];

    (async () => {
      for (const [pokemon, league, userIV] of testCases) {
        const ivSuffix = userIV ? ` ${userIV}` : '';
        console.log(`\n>>> /pvp 培养 ${pokemon} ${league}${ivSuffix}`);
        const parsed = parseCommand([pokemon, league, ...(userIV ? [userIV] : [])]);
        if (!parsed.valid) {
          console.log(`错误: ${parsed.error}`);
          if (parsed.suggestions) console.log(`建议: ${parsed.suggestions.join(', ')}`);
          continue;
        }
        const result = await queryPokemon(parsed.pokemon, parsed.league, parsed.userIV);
        if ('error' in result) {
          console.log(`错误: ${result.error}`);
        } else {
          console.log(formatResult(result));
        }
        console.log('---');
      }
    })();
  } else if (args.length >= 2) {
    (async () => {
      const parsed = parseCommand(args);
      if (!parsed.valid) {
        console.log(parsed.error);
        if (parsed.suggestions) console.log(`可用联盟：${parsed.suggestions.join('、')}`);
        return;
      }
      const result = await queryPokemon(parsed.pokemon, parsed.league, parsed.userIV);
      if ('error' in result) {
        console.log(result.error);
      } else {
        console.log(formatResult(result));
      }
    })();
  } else {
    console.log('用法: node dist/index.js --test');
    console.log('       node dist/index.js <宝可梦> <联盟> [攻击/防御/HP]');
  }
}
