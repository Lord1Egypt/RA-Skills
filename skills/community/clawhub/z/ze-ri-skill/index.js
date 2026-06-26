/**
 * 择日学 Skill - 核心算法
 * 作者：天工长老
 * 版本：v1.1
 * 创建：2026 年 3 月 29 日
 * 更新：2026 年 3 月 30 日 - 添加神煞系统、时辰吉凶
 */

// 建除十二神计算
function getJianChu(year, month, day) {
  // 简化算法：以月建为基准
  const monthJian = ['建', '除', '满', '平', '定', '执', '破', '危', '成', '收', '开', '闭'];
  
  // 计算月建（简化：正月建寅）
  const lunarMonth = ((month - 1 + 2) % 12); // 调整为农历月
  
  // 计算日建除
  const dayIndex = (day + lunarMonth) % 12;
  
  return monthJian[dayIndex];
}

// 黄道黑道计算（简化版）
function getHuangDao(year, month, day) {
  const huangDao = ['青龙', '明堂', '天刑', '朱雀', '金匮', '天德', '白虎', '玉堂', '天牢', '玄武', '司命', '勾陈'];
  const dayIndex = (year + month + day) % 12;
  return huangDao[dayIndex];
}

// 建除吉凶判断
function getJianChuJiXiong(jianChu) {
  const jiXiong = {
    '建': '吉', '除': '吉', '满': '吉', '平': '平',
    '定': '吉', '执': '吉', '破': '凶', '危': '凶',
    '成': '吉', '收': '吉', '开': '吉', '闭': '凶'
  };
  return jiXiong[jianChu] || '平';
}

// 黄道黑道吉凶判断
function getHuangDaoJiXiong(huangDao) {
  const jiXiong = {
    '青龙': '大吉', '明堂': '吉', '天刑': '凶', '朱雀': '凶',
    '金匮': '吉', '天德': '吉', '白虎': '凶', '玉堂': '吉',
    '天牢': '凶', '玄武': '凶', '司命': '吉', '勾陈': '凶'
  };
  return jiXiong[huangDao] || '平';
}

// 宜忌查询（简化版）
function getYiJi(jianChu, huangDao) {
  const yiMap = {
    '建': ['上任', '出行', '安床'],
    '除': ['扫舍', '求医', '解除'],
    '满': ['祭祀', '祈福', '嫁娶'],
    '平': ['祭祀', '祈福', '修造'],
    '定': ['祭祀', '祈福', '嫁娶'],
    '执': ['祭祀', '祈福', '捕捉'],
    '破': ['破屋', '坏垣', '求医'],
    '危': ['祭祀', '祈福'],
    '成': ['祭祀', '祈福', '嫁娶', '开业'],
    '收': ['祭祀', '祈福', '捕捉', '纳财'],
    '开': ['祭祀', '祈福', '嫁娶', '开业', '出行'],
    '闭': ['祭祀', '祈福', '修造']
  };
  
  const jiMap = {
    '建': ['动土', '开仓'],
    '除': ['余事'],
    '满': ['服药', '栽种'],
    '平': ['嫁娶', '安葬'],
    '定': ['出行', '医疗'],
    '执': ['出行', '搬迁'],
    '破': ['余事'],
    '危': ['登高', '乘船'],
    '成': ['诉讼'],
    '收': ['出行', '安葬'],
    '开': ['动土'],
    '闭': ['嫁娶', '出行', '安葬']
  };
  
  return {
    宜：yiMap[jianChu] || [],
    忌：jiMap[jianChu] || []
  };
}

// 综合择日判断
function zeRi(year, month, day, eventType = 'general') {
  const jianChu = getJianChu(year, month, day);
  const huangDao = getHuangDao(year, month, day);
  const jianChuJiXiong = getJianChuJiXiong(jianChu);
  const huangDaoJiXiong = getHuangDaoJiXiong(huangDao);
  const yiJi = getYiJi(jianChu, huangDao);
  
  // 综合评分
  let score = 50;
  if (jianChuJiXiong === '吉') score += 20;
  if (jianChuJiXiong === '凶') score -= 20;
  if (huangDaoJiXiong.includes('吉')) score += 15;
  if (huangDaoJiXiong.includes('凶')) score -= 15;
  
  let conclusion = '平';
  if (score >= 80) conclusion = '大吉';
  else if (score >= 65) conclusion = '吉';
  else if (score >= 50) conclusion = '平';
  else if (score >= 35) conclusion = '凶';
  else conclusion = '大凶';
  
  return {
    日期：`${year}年${month}月${day}日`,
    建除：jianChu,
    建除吉凶：jianChuJiXiong,
    黄道：huangDao,
    黄道吉凶：huangDaoJiXiong,
    宜：yiJi.宜，
    忌：yiJi.忌，
    综合评分：score,
    综合判断：conclusion
  };
}

// 择日推荐（给定月份推荐吉日）
function tuiJianJiRi(year, month, eventType = '嫁娶', limit = 5) {
  const daysInMonth = new Date(year, month, 0).getDate();
  const jiRiList = [];
  
  for (let day = 1; day <= daysInMonth; day++) {
    const result = zeRi(year, month, day);
    if (result.综合评分 >= 65) {
      if (eventType === '嫁娶' && result.宜.includes('嫁娶')) {
        jiRiList.push({ ...result, 日：day });
      } else if (eventType === '开业' && result.宜.includes('开业')) {
        jiRiList.push({ ...result, 日：day });
      } else if (eventType === 'general') {
        jiRiList.push({ ...result, 日：day });
      }
    }
  }
  
  return jiRiList.slice(0, limit);
}

// ========== v1.1 新增：神煞系统 ==========

// 常用神煞计算（简化版）
function getShenSha(year, month, day) {
  const shenSha = [];
  const dayGan = (year + month + day) % 10; // 简化日干
  const dayZhi = (year + month + day) % 12; // 简化日支
  
  // 天德贵人
  if ([1, 3, 5, 7, 9, 11].includes(month)) shenSha.push('天德');
  
  // 月德贵人
  if ([2, 6, 10].includes(month)) shenSha.push('月德');
  
  // 天赦日（春戊寅、夏甲午、秋戊申、冬甲子）
  if ((month === 3 && day === 15) || (month === 6 && day === 21) || 
      (month === 9 && day === 27) || (month === 12 && day === 3)) {
    shenSha.push('天赦');
  }
  
  // 三合日
  const sanHe = {
    1: [5, 9], 2: [6, 10], 3: [7, 11], 4: [8, 12],
    5: [9, 1], 6: [10, 2], 7: [11, 3], 8: [12, 4],
    9: [1, 5], 10: [2, 6], 11: [3, 7], 12: [4, 8]
  };
  if (sanHe[month] && sanHe[month].includes(day % 12 || 12)) {
    shenSha.push('三合');
  }
  
  // 岁破
  if (month === ((year % 12) + 6) % 12 || month === ((year % 12) + 6) % 12 + 6) {
    shenSha.push('岁破');
  }
  
  // 月破
  if (day === ((month + 6) % 12) || day === ((month + 6) % 12) + 12) {
    shenSha.push('月破');
  }
  
  return shenSha.length > 0 ? shenSha : ['无特殊神煞'];
}

// 神煞吉凶判断
function getShenShaJiXiong(shenSha) {
  const jiShen = ['天德', '月德', '天赦', '三合', '六合'];
  const xiongShen = ['岁破', '月破', '四离', '四绝', '往亡'];
  
  let jiCount = 0;
  let xiongCount = 0;
  
  shenSha.forEach(ss => {
    if (jiShen.includes(ss)) jiCount++;
    if (xiongShen.includes(ss)) xiongCount++;
  });
  
  return { jiShen: jiCount, xiongShen: xiongCount };
}

// 时辰吉凶（简化版）
function getShiChenJiXiong(hour) {
  const shiChen = [
    { name: '子时', time: '23:00-01:00' },
    { name: '丑时', time: '01:00-03:00' },
    { name: '寅时', time: '03:00-05:00' },
    { name: '卯时', time: '05:00-07:00' },
    { name: '辰时', time: '07:00-09:00' },
    { name: '巳时', time: '09:00-11:00' },
    { name: '午时', time: '11:00-13:00' },
    { name: '未时', time: '13:00-15:00' },
    { name: '申时', time: '15:00-17:00' },
    { name: '酉时', time: '17:00-19:00' },
    { name: '戌时', time: '19:00-21:00' },
    { name: '亥时', time: '21:00-23:00' }
  ];
  
  const shiChenIndex = Math.floor(hour / 2) % 12;
  const jiXiong = ['吉', '凶', '吉', '吉', '凶', '吉', '凶', '吉', '吉', '凶', '吉', '凶'];
  
  return {
    时辰：shiChen[shiChenIndex].name,
    时间：shiChen[shiChenIndex].time,
    吉凶：jiXiong[shiChenIndex]
  };
}

// 导出
module.exports = {
  zeRi,
  tuiJianJiRi,
  getJianChu,
  getHuangDao,
  getJianChuJiXiong,
  getHuangDaoJiXiong,
  // v1.1 新增
  getShenSha,
  getShenShaJiXiong,
  getShiChenJiXiong
};
