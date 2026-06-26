/**
 * 奇门遁甲深度解盘模块
 */

const { PALACES, NINE_STARS, EIGHT_DOORS, GOD_INFO, GAN_ELEMENT } = require('./engine.js');

// 五行生克
const WU_XING_SHENG = { '木':'火', '火':'土', '土':'金', '金':'水', '水':'木' };
const WU_XING_KE = { '金':'木', '木':'土', '土':'水', '水':'火', '火':'金' };

// 四季旺衰：monthZhi → { 旺, 相, 休, 囚, 死 }
function getSeasonWangShuai(mZhi) {
  // 寅卯=春, 巳午=夏, 申酉=秋, 亥子=冬, 辰未戌丑=四季
  if ([2,3].includes(mZhi)) return { '木':'旺','火':'相','水':'休','金':'囚','土':'死' };
  if ([5,6].includes(mZhi)) return { '火':'旺','土':'相','木':'休','水':'囚','金':'死' };
  if ([8,9].includes(mZhi)) return { '金':'旺','水':'相','土':'休','火':'囚','木':'死' };
  if ([11,0].includes(mZhi)) return { '水':'旺','木':'相','金':'休','土':'囚','火':'死' };
  // 四季月：辰(4)未(7)戌(10)丑(1)
  return { '土':'旺','金':'相','火':'休','木':'囚','水':'死' };
}

const STATUS_POWER = { '旺':100, '相':80, '休':50, '囚':30, '死':10 };

function getWangShuai(element, mZhi) {
  const table = getSeasonWangShuai(mZhi);
  const status = table[element] || '休';
  return { status, power: STATUS_POWER[status] || 50 };
}

// 用神系统
const YONG_SHEN = {
  general: { name:'综合运势', primary:[{type:'stem',name:'日干'}], desc:'以日干落宫为主' },
  wealth: { name:'求财', primary:[{type:'door',name:'生门'},{type:'stem',name:'戊'}], desc:'生门为财门，戊为财星' },
  career: { name:'事业', primary:[{type:'door',name:'开门'},{type:'star',name:'天心'}], desc:'开门主事业，天心主决策' },
  marriage: { name:'婚姻', primary:[{type:'god',name:'六合'},{type:'door',name:'景门'}], desc:'六合主合和，景门主感情' },
  health: { name:'健康', primary:[{type:'star',name:'天芮'},{type:'door',name:'死门'}], desc:'天芮主疾病，死门主病灶' },
  travel: { name:'出行', primary:[{type:'door',name:'开门'},{type:'god',name:'值符'}], desc:'开门主出入，值符主贵人' },
  lawsuit: { name:'官司', primary:[{type:'door',name:'开门'},{type:'star',name:'天心'}], desc:'开门主官府，天心主法律' },
  exam: { name:'考试', primary:[{type:'star',name:'天辅'},{type:'door',name:'杜门'}], desc:'天辅主文昌，杜门主闭关苦读' },
  lost: { name:'失物', primary:[{type:'god',name:'值符'},{type:'door',name:'景门'}], desc:'值符指方向' },
  missing: { name:'寻人', primary:[{type:'god',name:'六合'},{type:'god',name:'太阴'}], desc:'六合主藏匿方位' },
  weather: { name:'天气', primary:[{type:'star',name:'天蓬'},{type:'star',name:'天冲'}], desc:'天蓬主雨，天冲主风' },
  fengshui: { name:'风水', primary:[{type:'door',name:'生门'},{type:'star',name:'天任'}], desc:'生门主旺气，天任主稳固' },
  invest: { name:'投资', primary:[{type:'door',name:'生门'},{type:'stem',name:'戊'}], desc:'同求财，关注风险' },
};

// 找用神所在宫位
function findYongShenPalace(chartData, ys) {
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    if (ys.type === 'door' && p.door === ys.name) return i;
    if (ys.type === 'star' && p.star === ys.name) return i;
    if (ys.type === 'god' && p.god === ys.name) return i;
    if (ys.type === 'stem') {
      // 日干落宫
      const dayGan = chartData.ganZhi.day[0];
      if (p.heavenStem === dayGan || p.earthStem === dayGan) return i;
    }
  }
  return null;
}

// 五行对应颜色
const ELEMENT_COLOR = { '金':'白色/金色', '木':'绿色/青色', '水':'黑色/蓝色', '火':'红色/紫色', '土':'黄色/棕色' };

// 解盘主函数
function interpret(chartData, gejuData, questionType = 'general') {
  const mZhi = chartData.ganZhi.vals.mZhi;
  const ysConfig = YONG_SHEN[questionType] || YONG_SHEN.general;
  
  // 找用神宫位
  const ysPalaces = [];
  for (const ys of ysConfig.primary) {
    const palace = findYongShenPalace(chartData, ys);
    if (palace) {
      ysPalaces.push({ ...ys, palace, palaceData: chartData.palaces[palace] });
    }
  }
  
  // 分析用神
  let detail = '';
  let summaryParts = [];
  let overallScore = 50;
  
  detail += `📋 问题类型：${ysConfig.name}\n`;
  detail += `📖 用神说明：${ysConfig.desc}\n\n`;
  
  for (const ys of ysPalaces) {
    const p = ys.palaceData;
    const pInfo = PALACES[ys.palace];
    
    // 用神五行旺衰
    let ysElement = '';
    if (ys.type === 'door') {
      const doorInfo = Object.values(EIGHT_DOORS).find(d => d.name === ys.name);
      ysElement = doorInfo ? doorInfo.element : '';
    } else if (ys.type === 'star') {
      const starInfo = Object.values(NINE_STARS).find(s => s.name === ys.name);
      ysElement = starInfo ? starInfo.element : '';
    } else if (ys.type === 'stem') {
      ysElement = GAN_ELEMENT[chartData.ganZhi.day[0]] || '';
    }
    
    const ws = ysElement ? getWangShuai(ysElement, mZhi) : { status:'休', power:50 };
    
    detail += `【用神: ${ys.name}】落${pInfo.name}${ys.palace}宫（${pInfo.dir}）\n`;
    detail += `  五行: ${ysElement}  旺衰: ${ws.status}(${ws.power})\n`;
    detail += `  宫内: ${p.star} + ${p.door} + ${p.god}\n`;
    detail += `  天盘: ${p.heavenStem}  地盘: ${p.earthStem}\n`;
    
    // 得地/失地判断
    if (ysElement && pInfo.element) {
      if (ysElement === pInfo.element) {
        detail += `  ✅ 用神得地（五行同宫），力量增强\n`;
        overallScore += 10;
      } else if (WU_XING_SHENG[pInfo.element] === ysElement) {
        detail += `  ✅ 宫生用神，有助力\n`;
        overallScore += 5;
      } else if (WU_XING_KE[pInfo.element] === ysElement) {
        detail += `  ❌ 宫克用神，用神受制\n`;
        overallScore -= 10;
      } else if (WU_XING_KE[ysElement] === pInfo.element) {
        detail += `  ⚠️ 用神克宫，消耗过大\n`;
        overallScore -= 5;
      }
    }
    
    // 空亡
    if (p.flags.includes('空')) {
      detail += `  ⚠️ 用神落空亡，事难成实\n`;
      overallScore -= 15;
      summaryParts.push('用神落空');
    }
    // 马星
    if (p.flags.includes('马')) {
      detail += `  🐎 用神临马星，事有变动\n`;
      summaryParts.push('临马星');
    }
    
    // 旺衰影响
    if (ws.power >= 80) {
      summaryParts.push(ys.name + '旺相有力');
      overallScore += 10;
    } else if (ws.power <= 30) {
      summaryParts.push(ys.name + '囚死无力');
      overallScore -= 10;
    }
    
    detail += '\n';
  }
  
  // 格局影响
  if (gejuData) {
    overallScore += gejuData.auspicious.length * 3;
    overallScore -= gejuData.inauspicious.length * 3;
    
    if (gejuData.auspicious.length > gejuData.inauspicious.length) {
      summaryParts.push('吉格多于凶格');
    } else if (gejuData.inauspicious.length > gejuData.auspicious.length) {
      summaryParts.push('凶格多于吉格');
    }
    
    // 特殊格局影响
    for (const g of gejuData.inauspicious) {
      if (g.name === '五不遇时') { overallScore -= 8; summaryParts.push('五不遇时'); }
      if (g.name === '值符落空') { overallScore -= 10; summaryParts.push('值符落空'); }
      if (g.name === '值使落空') { overallScore -= 8; summaryParts.push('值使落空'); }
      if (g.name === '天盘伏吟') { overallScore -= 10; summaryParts.push('天盘伏吟'); }
      if (g.name === '天盘反吟') { overallScore -= 10; summaryParts.push('天盘反吟'); }
    }
    for (const g of gejuData.auspicious) {
      if (g.name.includes('天遁') || g.name.includes('地遁') || g.name.includes('人遁')) {
        overallScore += 8;
      }
      if (g.name.includes('奇门遇合')) { overallScore += 3; }
    }
  }
  
  overallScore = Math.max(0, Math.min(100, overallScore));
  
  // 吉方（值符所在宫）
  const zhiFuPalace = chartData.zhiFu.targetPalace;
  const direction = PALACES[zhiFuPalace] ? PALACES[zhiFuPalace].dir : '中央';
  const color = PALACES[zhiFuPalace] ? ELEMENT_COLOR[PALACES[zhiFuPalace].element] || '黄色' : '黄色';
  
  // 吉时（三吉门宫位对应）
  let timing = '';
  if (gejuData && gejuData.sanJiMen) {
    const jiGong = gejuData.sanJiMen;
    timing = '三吉门在' + jiGong.map(g => PALACES[g].name + g + '宫').join('、');
  }
  
  // 生成总结
  let summary = '';
  if (overallScore >= 75) {
    summary = `🟢 ${ysConfig.name}整体大吉（${overallScore}分）。`;
  } else if (overallScore >= 55) {
    summary = `🟡 ${ysConfig.name}整体中吉（${overallScore}分），有利但需留意细节。`;
  } else if (overallScore >= 40) {
    summary = `🟠 ${ysConfig.name}整体平平（${overallScore}分），宜谨慎行事。`;
  } else {
    summary = `🔴 ${ysConfig.name}整体不利（${overallScore}分），建议暂缓或另择时日。`;
  }
  if (summaryParts.length > 0) {
    summary += ' ' + summaryParts.join('，') + '。';
  }
  
  // 建议（按问题类型个性化）
  let advice = '';
  if (overallScore >= 65) {
    const adviceMap = {
      general: `整体趋势向好，把握时机行动。可择${direction}方行事，穿${color}增运。`,
      wealth: `财运看好，宜积极求财。方向${direction}，穿${color}。注意量入为出，不贪大。`,
      career: `事业运旺，适合推进重要项目或求职面试。往${direction}方发展更佳。`,
      marriage: `感情运佳，单身可主动出击，已婚宜增进感情。${direction}方为桃花位。`,
      health: `身体无大碍，但仍需注意保养。规律作息，适量运动。`,
      travel: `出行大吉，往${direction}方向最佳。穿${color}出行平安顺利。`,
      lawsuit: `官司有利，可积极应诉。找贵人相助更佳。`,
      exam: `考运不错，静心复习，正常发挥即可。穿${color}增考运。`,
      invest: `投资时机尚可，可适量入场。注意分散风险，不宜all in。`,
      fengshui: `住宅${direction}方位气场旺盛，可在此方位布局。`,
    };
    advice = adviceMap[questionType] || adviceMap.general;
  } else if (overallScore >= 40) {
    const adviceMap = {
      general: `宜守不宜进，多观察少行动。若必须行事，可往${direction}方，穿${color}。`,
      wealth: `求财宜谨慎，不宜大额投入。小财可得，大财需等。穿${color}稍增财运。`,
      career: `事业暂缓大动作，做好本职工作。不宜跳槽或提出重大方案。`,
      marriage: `感情需耐心经营，不宜急于求成。多沟通少争吵。`,
      health: `注意身体信号，及时检查。饮食清淡，避免劳累。`,
      travel: `出行需谨慎，做好准备再动。避开凶方。`,
      lawsuit: `官司胜负未定，宜调解和解。不宜硬刚。`,
      exam: `考试中等，需更努力复习。保持心态平和。`,
      invest: `投资观望为主，不宜追高。已有仓位可持有但不加仓。`,
      fengshui: `住宅风水一般，可在${direction}方位摆放吉物化解。`,
    };
    advice = adviceMap[questionType] || adviceMap.general;
  } else {
    const adviceMap = {
      general: `建议暂缓此事，另择吉时。若不得已需行动，避开凶方，多加小心。`,
      wealth: `不宜求财，尤其避免大额交易和投机。守住现有资产为上。`,
      career: `事业运低迷，忍耐为主。不宜冒进、跳槽或得罪上司。`,
      marriage: `感情易生变故，控制情绪，避免争吵。给彼此空间。`,
      health: `健康需高度重视，建议尽快体检。注意${direction}方位的风水。`,
      travel: `不宜出行，如必须则避开凶方，做好万全准备。`,
      lawsuit: `官司不利，建议和解退让。硬来损失更大。`,
      exam: `考运不佳，需加倍努力。调整心态，做最坏打算。`,
      invest: `强烈建议不要入场，已有仓位考虑止损。现金为王。`,
      fengshui: `住宅风水有问题，建议请专业人士实地勘查。`,
    };
    advice = adviceMap[questionType] || adviceMap.general;
  }
  
  return {
    summary,
    detail,
    yongShen: ysPalaces,
    score: { overall: overallScore },
    direction,
    color,
    timing,
    advice,
  };
}

module.exports = { interpret, getWangShuai, YONG_SHEN };
