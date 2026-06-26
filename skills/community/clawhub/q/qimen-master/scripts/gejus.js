/**
 * 奇门遁甲格局识别模块
 * 识别吉格、凶格、天干组合
 */

const { PALACES, NINE_STARS, EIGHT_DOORS, GOD_INFO, GAN_ELEMENT } = require('./engine.js');

// ========== 十天干克应（天地盘干组合） ==========
const STEM_COMBOS = {
  // 甲(戊)加X
  '戊戊':{ name:'伏吟', type:'平', desc:'事情迟缓不动' },
  '戊乙':{ name:'青龙和会', type:'吉', desc:'门户光辉，百事顺遂' },
  '戊丙':{ name:'飞鸟跌穴', type:'吉', desc:'百事大吉，谋望有成' },
  '戊丁':{ name:'青龙转光', type:'吉', desc:'官讼皆吉，出入皆利' },
  '戊己':{ name:'贵人入狱', type:'凶', desc:'公私皆不利' },
  '戊庚':{ name:'值符飞宫', type:'凶', desc:'上司有灾，吉事成凶' },
  '戊辛':{ name:'青龙折足', type:'凶', desc:'吉门被伤，求谋有阻' },
  '戊壬':{ name:'青龙入天牢', type:'凶', desc:'公私不利，官司牢狱' },
  '戊癸':{ name:'青龙华盖', type:'平', desc:'贵人有阻，暗中有助' },
  // 乙加X
  '乙乙':{ name:'日奇伏吟', type:'平', desc:'不宜谋事' },
  '乙戊':{ name:'利见中人', type:'吉', desc:'利见贵人' },
  '乙丙':{ name:'奇仪顺遂', type:'吉', desc:'谋事皆宜' },
  '乙丁':{ name:'奇仪相佐', type:'吉', desc:'最利文书' },
  '乙己':{ name:'日奇入墓', type:'凶', desc:'被人诬陷，门户破败' },
  '乙庚':{ name:'日奇被刑', type:'凶', desc:'失道被伤，争讼不利' },
  '乙辛':{ name:'青龙逃走', type:'凶', desc:'奴仆背主，六畜有灾' },
  '乙壬':{ name:'日奇入地', type:'平', desc:'尊卑悖逆，阴人害事' },
  '乙癸':{ name:'华盖逢星', type:'平', desc:'遁迹修道为吉' },
  // 丙加X
  '丙丙':{ name:'月奇伏吟', type:'平', desc:'文书阻碍' },
  '丙戊':{ name:'鸟跌穴', type:'吉', desc:'事从心想' },
  '丙乙':{ name:'日月并行', type:'吉', desc:'公谋私谋皆大吉' },
  '丙丁':{ name:'月奇朱雀', type:'吉', desc:'贵人文书皆吉' },
  '丙己':{ name:'火悖入刑', type:'凶', desc:'游魂入墓' },
  '丙庚':{ name:'荧入太白', type:'凶', desc:'贼来害我，被人欺凌' },
  '丙辛':{ name:'谋事能成', type:'吉', desc:'利于谋事' },
  '丙壬':{ name:'火入天罗', type:'凶', desc:'为客不利' },
  '丙癸':{ name:'华盖悖师', type:'凶', desc:'文书口舌是非' },
  // 丁加X
  '丁丁':{ name:'星奇伏吟', type:'平', desc:'文书不行' },
  '丁戊':{ name:'青龙转光', type:'吉', desc:'贵人财帛有喜' },
  '丁乙':{ name:'人遁吉格', type:'吉', desc:'贵人加临，百事皆吉' },
  '丁丙':{ name:'星月相会', type:'吉', desc:'贵人星助，文书有成' },
  '丁己':{ name:'火入勾陈', type:'凶', desc:'奸私仇冤，事多不明' },
  '丁庚':{ name:'文星入狱', type:'凶', desc:'文书口舌，行人不归' },
  '丁辛':{ name:'朱雀入狱', type:'凶', desc:'罪人得刑' },
  '丁壬':{ name:'五离不遇', type:'凶', desc:'文书逢鬼，口舌破财' },
  '丁癸':{ name:'朱雀投江', type:'凶', desc:'文书口舌，词讼不利' },
  // 己加X
  '己己':{ name:'地户伏吟', type:'凶', desc:'百事不遂' },
  '己戊':{ name:'犬遇青龙', type:'平', desc:'门户不正' },
  '己乙':{ name:'墓神不明', type:'凶', desc:'地户逢星，阴人害事' },
  '己丙':{ name:'火悖地户', type:'凶', desc:'文书不行' },
  '己丁':{ name:'朱雀入墓', type:'凶', desc:'文书词讼先损后益' },
  '己庚':{ name:'刑格', type:'凶', desc:'求人无益，行事有阻' },
  '己辛':{ name:'入狱自刑', type:'凶', desc:'奴仆欺主，官讼不利' },
  '己壬':{ name:'地入天牢', type:'凶', desc:'关梁不通' },
  '己癸':{ name:'地刑玄武', type:'凶', desc:'阴谋贼害，词讼不利' },
  // 庚加X
  '庚庚':{ name:'太白伏吟', type:'凶', desc:'诸事不利' },
  '庚戊':{ name:'上格', type:'凶', desc:'值符被伤，上司有灾' },
  '庚乙':{ name:'太白逢星', type:'凶', desc:'退吉进凶，谋事不成' },
  '庚丙':{ name:'太白入荧', type:'凶', desc:'贼去害人，被人告发' },
  '庚丁':{ name:'亭亭之格', type:'凶', desc:'因私匿成讼，损财招非' },
  '庚己':{ name:'刑格返名', type:'凶', desc:'上格多灾' },
  '庚辛':{ name:'白虎干格', type:'凶', desc:'官讼惊恐' },
  '庚壬':{ name:'小格', type:'凶', desc:'诸事不利' },
  '庚癸':{ name:'大格', type:'凶', desc:'行人不归，诸事不利' },
  // 辛加X
  '辛辛':{ name:'伏吟天庭', type:'凶', desc:'公废私就' },
  '辛戊':{ name:'困龙被伤', type:'凶', desc:'谋事有阻' },
  '辛乙':{ name:'白虎猖狂', type:'凶', desc:'被人欺凌，灾害重重' },
  '辛丙':{ name:'谋事有成', type:'吉', desc:'有小人阻但终成' },
  '辛丁':{ name:'狱神得奇', type:'平', desc:'经商安稳' },
  '辛己':{ name:'入墓自刑', type:'凶', desc:'奴仆被害' },
  '辛庚':{ name:'白虎出力', type:'凶', desc:'刀兵相见，主有血光' },
  '辛壬':{ name:'凶蛇入狱', type:'凶', desc:'两男争女，讼狱不息' },
  '辛癸':{ name:'天牢华盖', type:'凶', desc:'日月失明' },
  // 壬加X
  '壬壬':{ name:'天牢伏吟', type:'凶', desc:'公私皆不利' },
  '壬戊':{ name:'蛇入龙穴', type:'吉', desc:'男吉女凶' },
  '壬乙':{ name:'玉女游龙', type:'吉', desc:'有情有义' },
  '壬丙':{ name:'水蛇入火', type:'凶', desc:'官灾刑禁' },
  '壬丁':{ name:'蛇夭矫', type:'凶', desc:'文书词讼，贼来害己' },
  '壬己':{ name:'入地化柱', type:'凶', desc:'凡阴不利' },
  '壬庚':{ name:'小格', type:'凶', desc:'诸事不利' },
  '壬辛':{ name:'凶蛇入狱', type:'凶', desc:'两男争女' },
  '壬癸':{ name:'天网四张', type:'凶', desc:'行人失伴' },
  // 癸加X
  '癸癸':{ name:'华盖伏吟', type:'凶', desc:'阴人害事' },
  '癸戊':{ name:'天乙合局', type:'吉', desc:'利见贵人' },
  '癸乙':{ name:'华盖逢星', type:'平', desc:'贵人暗中相助' },
  '癸丙':{ name:'华盖悖师', type:'凶', desc:'是非口舌' },
  '癸丁':{ name:'螣蛇夭矫', type:'凶', desc:'文书官讼，贼盗不宁' },
  '癸己':{ name:'华盖地户', type:'凶', desc:'阴人害事' },
  '癸庚':{ name:'大格', type:'凶', desc:'行人不归' },
  '癸辛':{ name:'网盖天牢', type:'凶', desc:'主有官讼' },
  '癸壬':{ name:'天网四张', type:'凶', desc:'行人失伴，主落水灾' },
};

// ========== 格局识别 ==========

/**
 * 识别所有格局
 */
function identifyGejus(chartData) {
  const auspicious = [];
  const inauspicious = [];
  const stemCombos = {};
  
  // 1. 天干组合
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    const key = p.heavenStem + p.earthStem;
    const combo = STEM_COMBOS[key];
    stemCombos[i] = {
      heaven: p.heavenStem,
      earth: p.earthStem,
      name: combo ? combo.name : '未知',
      type: combo ? combo.type : '平',
      desc: combo ? combo.desc : '',
    };
  }
  
  // 2. 吉格识别
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    
    // 龙回首：天盘戊落在地盘戊上（甲回本位）
    if (p.heavenStem === '戊' && p.earthStem === '戊' && i !== 5) {
      // 这其实是伏吟的一种特殊情况
    }
    
    // 鸟跌穴：天盘丙落在地盘戊上
    if (p.heavenStem === '丙' && p.earthStem === '戊') {
      auspicious.push({ name:'鸟跌穴', palace:i, desc:'丙奇加甲子戊，百事大吉' });
    }
    
    // 三奇得使
    if (p.heavenStem === '乙' && p.door === '开门') {
      auspicious.push({ name:'三奇得使(乙奇开门)', palace:i, desc:'日奇得使，百事可为' });
    }
    if (p.heavenStem === '丙' && p.door === '休门') {
      auspicious.push({ name:'三奇得使(丙奇休门)', palace:i, desc:'月奇得使，贵人来助' });
    }
    if (p.heavenStem === '丁' && p.door === '生门') {
      auspicious.push({ name:'三奇得使(丁奇生门)', palace:i, desc:'星奇得使，财利大吉' });
    }
    
    // 玉女守门：丁奇+开门+太阴
    if (p.heavenStem === '丁' && p.door === '开门' && p.god === '太阴') {
      auspicious.push({ name:'玉女守门', palace:i, desc:'阴贵相助，暗中有益' });
    }
    
    // 三奇贵人升殿
    if (['乙','丙','丁'].includes(p.heavenStem)) {
      const stemEl = GAN_ELEMENT[p.heavenStem];
      const palaceEl = PALACES[i].element;
      // 三奇落在生旺之地
      if ((stemEl === '木' && palaceEl === '木') ||
          (stemEl === '火' && palaceEl === '火') ||
          (stemEl === '木' && palaceEl === '水')) { // 水生木
        auspicious.push({ name:'三奇贵人升殿', palace:i, desc:p.heavenStem + '奇得地旺相' });
      }
    }
    
    // 九遁
    // 天遁：天盘丙+地盘戊+生门（或天盘丁+地盘癸+生门）
    if (p.heavenStem === '丙' && p.earthStem === '戊' && p.door === '生门') {
      auspicious.push({ name:'天遁', palace:i, desc:'天地人三盘合一，大吉' });
    }
    // 地遁：天盘乙+地盘己+开门
    if (p.heavenStem === '乙' && p.earthStem === '己' && p.door === '开门') {
      auspicious.push({ name:'地遁', palace:i, desc:'利于隐匿、埋藏' });
    }
    // 人遁：天盘丁+地盘乙+休门+太阴
    if (p.heavenStem === '丁' && p.earthStem === '乙' && p.door === '休门' && p.god === '太阴') {
      auspicious.push({ name:'人遁', palace:i, desc:'利于求人、交际' });
    }
    // 神遁：天盘丙+地盘戊+九天（或生门+九天）
    if (p.heavenStem === '丙' && p.earthStem === '戊' && p.god === '九天') {
      auspicious.push({ name:'神遁', palace:i, desc:'利于祈福、求神' });
    }
    // 鬼遁：天盘丁+地盘癸+九地（或生门+九地）
    if (p.heavenStem === '丁' && p.earthStem === '癸' && p.god === '九地') {
      auspicious.push({ name:'鬼遁', palace:i, desc:'利于阴事、暗中行事' });
    }
    // 龙遁：天盘乙+休门+六合（卦为坎/震）
    if (p.heavenStem === '乙' && p.door === '休门' && p.god === '六合') {
      auspicious.push({ name:'龙遁', palace:i, desc:'利于求财、交易' });
    }
    // 虎遁：天盘辛+生门+太阴（或开门+太阴）
    if (p.heavenStem === '辛' && p.door === '生门' && p.god === '太阴') {
      auspicious.push({ name:'虎遁', palace:i, desc:'利于行猎、捕获' });
    }
    // 风遁：天盘乙+开门+九天（巽宫）
    if (p.heavenStem === '乙' && p.door === '开门' && p.god === '九天') {
      auspicious.push({ name:'风遁', palace:i, desc:'利于出行、行军' });
    }
    // 云遁：天盘乙+开门+九地（坤宫/艮宫）
    if (p.heavenStem === '乙' && p.door === '开门' && p.god === '九地') {
      auspicious.push({ name:'云遁', palace:i, desc:'利于隐藏、潜伏' });
    }
    
    // 吉门+吉星+吉神 = 大吉
    const doorInfo = Object.values(EIGHT_DOORS).find(d => d.name === p.door);
    const starInfo = Object.values(NINE_STARS).find(s => s.name === p.star);
    const godInfo = GOD_INFO[p.god];
    if (doorInfo && doorInfo.type === '吉' && starInfo && starInfo.type === '吉' && godInfo && godInfo.type === '吉') {
      auspicious.push({ name:'三吉会合', palace:i, desc:p.star + '+' + p.door + '+' + p.god + '，大吉之象' });
    }
  }
  
  // 3. 凶格识别
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    
    // 伏吟：天盘干=地盘干
    if (p.heavenStem === p.earthStem) {
      inauspicious.push({ name:'伏吟', palace:i, desc:'事情迟缓不动，凡事宜守不宜进' });
    }
    
    // 反吟：天盘干与地盘干相冲（甲庚冲、乙辛冲、丙壬冲、丁癸冲、戊甲冲→戊庚？）
    const chongPairs = {'戊':'壬','壬':'戊','己':'癸','癸':'己','庚':'甲','辛':'乙','乙':'辛','丙':'庚','丁':'辛'};
    // 简化：五行相冲
    if (GAN_ELEMENT[p.heavenStem] && GAN_ELEMENT[p.earthStem]) {
      const hEl = GAN_ELEMENT[p.heavenStem];
      const eEl = GAN_ELEMENT[p.earthStem];
      if ((hEl === '金' && eEl === '木') || (hEl === '木' && eEl === '金') ||
          (hEl === '水' && eEl === '火') || (hEl === '火' && eEl === '水')) {
        inauspicious.push({ name:'反吟', palace:i, desc:'天地盘干相冲克，事情反复' });
      }
    }
    
    // 三奇入墓
    // 乙奇入墓：乙在坤2宫（未为乙墓）
    if (p.heavenStem === '乙' && i === 2) {
      inauspicious.push({ name:'三奇入墓(乙)', palace:i, desc:'日奇入墓，不能发挥作用' });
    }
    // 丙奇入墓：丙在乾6宫（戌为丙墓）
    if (p.heavenStem === '丙' && i === 6) {
      inauspicious.push({ name:'三奇入墓(丙)', palace:i, desc:'月奇入墓，贵人无力' });
    }
    // 丁奇入墓：丁在艮8宫？[待验证]  一般认为丁墓在丑→艮8宫不完全对
    // 传统：丁(火)墓在戌→乾6宫
    if (p.heavenStem === '丁' && i === 6) {
      inauspicious.push({ name:'三奇入墓(丁)', palace:i, desc:'星奇入墓，事情暗中受阻' });
    }
    
    // 门迫：门克宫（门不在本宫才算）
    const doorInfo = Object.values(EIGHT_DOORS).find(d => d.name === p.door);
    if (doorInfo && i !== 5) {
      const doorEl = doorInfo.element;
      const palaceEl = PALACES[i].element;
      const keMap = { '金':'木', '木':'土', '土':'水', '水':'火', '火':'金' };
      // 门在本宫不算迫
      const DOOR_ORIG = {'休门':1,'死门':2,'伤门':3,'杜门':4,'开门':6,'惊门':7,'生门':8,'景门':9};
      if (keMap[doorEl] === palaceEl && DOOR_ORIG[p.door] !== i) {
        inauspicious.push({ name:'门迫', palace:i, desc:p.door + '(' + doorEl + ')克' + PALACES[i].name + '宫(' + palaceEl + ')，门受宫制约' });
      }
    }
    
    // 大格：庚加癸
    if (p.heavenStem === '庚' && p.earthStem === '癸') {
      inauspicious.push({ name:'大格', palace:i, desc:'行人不归，诸事不利' });
    }
    // 小格：庚加壬
    if (p.heavenStem === '庚' && p.earthStem === '壬') {
      inauspicious.push({ name:'小格', palace:i, desc:'诸事不利' });
    }
    
    // 荧入太白：丙加庚
    if (p.heavenStem === '丙' && p.earthStem === '庚') {
      inauspicious.push({ name:'荧入太白', palace:i, desc:'贼来害我' });
    }
    // 太白入荧：庚加丙
    if (p.heavenStem === '庚' && p.earthStem === '丙') {
      inauspicious.push({ name:'太白入荧', palace:i, desc:'贼去害人' });
    }
    
    // 青龙逃走：乙加辛
    if (p.heavenStem === '乙' && p.earthStem === '辛') {
      inauspicious.push({ name:'青龙逃走', palace:i, desc:'奴仆背主' });
    }
    // 白虎猖狂：辛加乙
    if (p.heavenStem === '辛' && p.earthStem === '乙') {
      inauspicious.push({ name:'白虎猖狂', palace:i, desc:'被人欺凌' });
    }
    
    // 朱雀投江：丁加癸
    if (p.heavenStem === '丁' && p.earthStem === '癸') {
      inauspicious.push({ name:'朱雀投江', palace:i, desc:'文书词讼不利' });
    }
    // 螣蛇夭矫：癸加丁
    if (p.heavenStem === '癸' && p.earthStem === '丁') {
      inauspicious.push({ name:'螣蛇夭矫', palace:i, desc:'文书官讼' });
    }
    
    // 三凶门+凶星+凶神
    const starInfo = Object.values(NINE_STARS).find(s => s.name === p.star);
    const godInfo = GOD_INFO[p.god];
    if (doorInfo && doorInfo.type === '凶' && starInfo && starInfo.type === '凶' && godInfo && godInfo.type === '凶') {
      inauspicious.push({ name:'三凶会合', palace:i, desc:p.star + '+' + p.door + '+' + p.god + '，大凶之象' });
    }
  }
  
  // 4. 全局格局
  // 五不遇时：时干克日干
  const hGanEl = GAN_ELEMENT[chartData.ganZhi.hour[0]];
  const dGanEl = GAN_ELEMENT[chartData.ganZhi.day[0]];
  const keMap2 = { '金':'木', '木':'土', '土':'水', '水':'火', '火':'金' };
  if (keMap2[hGanEl] === dGanEl) {
    inauspicious.push({ name:'五不遇时', palace:0, desc:'时干克日干，诸事不利' });
  }
  
  // 值符落空
  const zhiFuPalace = chartData.zhiFu.targetPalace;
  if (chartData.kongWang.palaces.includes(zhiFuPalace)) {
    inauspicious.push({ name:'值符落空', palace:zhiFuPalace, desc:'领导不力、靠山全无' });
  }
  
  // 值使落空
  const zhiShiPalace = chartData.zhiShi.targetPalace;
  if (chartData.kongWang.palaces.includes(zhiShiPalace)) {
    inauspicious.push({ name:'值使落空', palace:zhiShiPalace, desc:'执行力缺失，计划落空' });
  }
  
  // 全局伏吟：值符星回原宫
  if (chartData.zhiFu.origPalace === chartData.zhiFu.targetPalace) {
    inauspicious.push({ name:'天盘伏吟', palace:0, desc:'九星不动，主事滞不前、进退两难' });
  }
  
  // 全局反吟：值符星到对冲宫
  const CHONG_PALACE = {1:9, 9:1, 2:8, 8:2, 3:7, 7:3, 4:6, 6:4};
  if (CHONG_PALACE[chartData.zhiFu.origPalace] === chartData.zhiFu.targetPalace) {
    inauspicious.push({ name:'天盘反吟', palace:0, desc:'九星对冲，主反复无常、出尔反尔' });
  }
  
  // 门伏吟：值使门回原宫
  if (chartData.zhiShi.origPalace === chartData.zhiShi.targetPalace) {
    inauspicious.push({ name:'门伏吟', palace:0, desc:'八门不动，人事停滞' });
  }
  
  // 门反吟：值使门到对冲宫
  if (CHONG_PALACE[chartData.zhiShi.origPalace] === chartData.zhiShi.targetPalace) {
    inauspicious.push({ name:'门反吟', palace:0, desc:'八门对冲，人事反复' });
  }
  
  // 奇门遇合（天地盘六合）
  const LIU_HE = {'甲':'己','己':'甲','乙':'庚','庚':'乙','丙':'辛','辛':'丙','丁':'壬','壬':'丁','戊':'癸','癸':'戊'};
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    if (LIU_HE[p.heavenStem] === p.earthStem) {
      auspicious.push({ name:'奇门遇合', palace:i, desc:p.heavenStem + '与' + p.earthStem + '六合，主和合有助' });
    }
  }
  
  // 时干入墓
  const hourGan = chartData.ganZhi.hour[0];
  const STEM_TOMB = {'甲':2,'乙':2,'丙':6,'丁':6,'戊':6,'己':6,'庚':8,'辛':8,'壬':4,'癸':4};
  const hourTombPalace = STEM_TOMB[hourGan];
  // 找时干在天盘的宫位
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    if (chartData.palaces[i].heavenStem === hourGan && i === hourTombPalace) {
      inauspicious.push({ name:'时干入墓', palace:i, desc:hourGan + '落' + i + '宫入墓，做事不明朗' });
      break;
    }
  }
  
  // 刑格（庚加戊）
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    const p = chartData.palaces[i];
    if (p.heavenStem === '庚' && p.earthStem === '戊') {
      inauspicious.push({ name:'刑格(上格)', palace:i, desc:'庚克甲(戊)，上级施压、官灾' });
    }
  }
  
  // 天三门：开休生三吉门所在宫位
  const sanJiMen = [];
  for (let i = 1; i <= 9; i++) {
    if (i === 5) continue;
    if (['开门','休门','生门'].includes(chartData.palaces[i].door)) {
      sanJiMen.push(i);
    }
  }
  
  // 5. 综合评分
  const score = calculateScore(auspicious, inauspicious, stemCombos);
  
  return { auspicious, inauspicious, stemCombos, score, sanJiMen };
}

/**
 * 综合评分
 */
function calculateScore(auspicious, inauspicious, stemCombos) {
  let score = 50; // 基准分
  
  // 吉格加分
  score += auspicious.length * 5;
  
  // 凶格减分
  score -= inauspicious.length * 5;
  
  // 天干组合
  for (const [p, combo] of Object.entries(stemCombos)) {
    if (combo.type === '吉') score += 3;
    if (combo.type === '凶') score -= 3;
  }
  
  return Math.max(0, Math.min(100, Math.round(score)));
}

module.exports = { identifyGejus, STEM_COMBOS };
