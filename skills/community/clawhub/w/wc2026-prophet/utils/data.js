/**
 * 世界杯预言家 SKILL 数据模块
 * 包含球队信息、ELO评分、赛程、冠军预测等静态数据
 * 动态比赛结果通过 wx.getStorageSync('wc2026_results') 获取
 */

// ===== 球队数据（含ELO、排名、教练等）=====
var TEAM_STATS = {"MEX":{"n":"墨西哥","f":"🇲🇽","r":15,"c":"CONCACAF","elo":1830,"coach":"Javier Aguirre","h":true,"pl":26},"RSA":{"n":"南非","f":"🇿🇦","r":60,"c":"CAF","elo":1562,"coach":"Hugo Broos","h":false,"pl":26},"KOR":{"n":"韩国","f":"🇰🇷","r":25,"c":"AFC","elo":1742,"coach":"Hong Myung-bo","h":false,"pl":26},"CZE":{"n":"捷克","f":"🇨🇿","r":41,"c":"UEFA","elo":1613,"coach":"Miroslav Koubek","h":false,"pl":26},"CAN":{"n":"加拿大","f":"🇨🇦","r":30,"c":"CONCACAF","elo":1725,"coach":"Jesse Marsch","h":true,"pl":25},"SUI":{"n":"瑞士","f":"🇨🇭","r":19,"c":"UEFA","elo":1807,"coach":"Murat Yakin","h":false,"pl":26},"QAT":{"n":"卡塔尔","f":"🇶🇦","r":53,"c":"AFC","elo":1552,"coach":"Julen Lopetegui","h":false,"pl":26},"BIH":{"n":"波黑","f":"🇧🇦","r":71,"c":"UEFA","elo":1566,"coach":"Sergej Barbarez","h":false,"pl":26},"BRA":{"n":"巴西","f":"🇧🇷","r":6,"c":"CONMEBOL","elo":1994,"coach":"Carlo Ancelotti","h":false,"pl":26},"MAR":{"n":"摩洛哥","f":"🇲🇦","r":8,"c":"CAF","elo":1875,"coach":"Mohamed Ouahbi","h":false,"pl":26},"HAI":{"n":"海地","f":"🇭🇹","r":79,"c":"CONCACAF","elo":1481,"coach":"Sébastien Migné","h":false,"pl":26},"SCO":{"n":"苏格兰","f":"🏴","r":43,"c":"UEFA","elo":1616,"coach":"Steve Clarke","h":false,"pl":26},"USA":{"n":"美国","f":"🇺🇸","r":16,"c":"CONCACAF","elo":1794,"coach":"Mauricio Pochettino","h":true,"pl":26},"PAR":{"n":"巴拉圭","f":"🇵🇾","r":38,"c":"CONMEBOL","elo":1653,"coach":"Gustavo Alfaro","h":false,"pl":26},"AUS":{"n":"澳大利亚","f":"🇦🇺","r":27,"c":"AFC","elo":1769,"coach":"Tony Popovic","h":false,"pl":26},"TUR":{"n":"土耳其","f":"🇹🇷","r":22,"c":"UEFA","elo":1906,"coach":"Vincenzo Montella","h":false,"pl":26},"GER":{"n":"德国","f":"🇩🇪","r":10,"c":"UEFA","elo":1927,"coach":"Julian Nagelsmann","h":false,"pl":26},"CUW":{"n":"库拉索","f":"🇨🇼","r":81,"c":"CONCACAF","elo":1433,"coach":"Dick Advocaat","h":false,"pl":26},"CIV":{"n":"科特迪瓦","f":"🇨🇮","r":39,"c":"CAF","elo":1706,"coach":"Emerse Faé","h":false,"pl":26},"ECU":{"n":"厄瓜多尔","f":"🇪🇨","r":23,"c":"CONMEBOL","elo":1790,"coach":"Sebastián Beccacece","h":false,"pl":26},"NED":{"n":"荷兰","f":"🇳🇱","r":7,"c":"UEFA","elo":1942,"coach":"Ronald Koeman","h":false,"pl":26},"JPN":{"n":"日本","f":"🇯🇵","r":18,"c":"AFC","elo":1851,"coach":"Hajime Moriyasu","h":false,"pl":26},"TUN":{"n":"突尼斯","f":"🇹🇳","r":47,"c":"CAF","elo":1666,"coach":"Sabri Lamouchi","h":false,"pl":26},"SWE":{"n":"瑞典","f":"🇸🇪","r":37,"c":"UEFA","elo":1714,"coach":"Graham Potter","h":false,"pl":26},"BEL":{"n":"比利时","f":"🇧🇪","r":9,"c":"UEFA","elo":1871,"coach":"Rudi Garcia","h":false,"pl":26},"EGY":{"n":"埃及","f":"🇪🇬","r":29,"c":"CAF","elo":1671,"coach":"Hossam Hassan","h":false,"pl":26},"IRN":{"n":"伊朗","f":"🇮🇷","r":21,"c":"AFC","elo":1733,"coach":"Amir Ghalenoei","h":false,"pl":26},"NZL":{"n":"新西兰","f":"🇳🇿","r":88,"c":"OFC","elo":1567,"coach":"Darren Bazeley","h":false,"pl":26},"ESP":{"n":"西班牙","f":"🇪🇸","r":2,"c":"UEFA","elo":2074,"coach":"Luis de la Fuente","h":false,"pl":26},"CPV":{"n":"佛得角","f":"🇨🇻","r":70,"c":"CAF","elo":1576,"coach":"Bubista","h":false,"pl":26},"KSA":{"n":"沙特阿拉伯","f":"🇸🇦","r":58,"c":"AFC","elo":1619,"coach":"Georgios Donis","h":false,"pl":26},"URU":{"n":"乌拉圭","f":"🇺🇾","r":17,"c":"CONMEBOL","elo":1833,"coach":"Marcelo Bielsa","h":false,"pl":26},"FRA":{"n":"法国","f":"🇫🇷","r":1,"c":"UEFA","elo":2040,"coach":"Didier Deschamps","h":false,"pl":26},"SEN":{"n":"塞内加尔","f":"🇸🇳","r":14,"c":"CAF","elo":1830,"coach":"Pape Thiaw","h":false,"pl":26},"NOR":{"n":"挪威","f":"🇳🇴","r":32,"c":"UEFA","elo":1917,"coach":"Ståle Solbakken","h":false,"pl":26},"IRQ":{"n":"伊拉克","f":"🇮🇶","r":56,"c":"AFC","elo":1608,"coach":"Graham Arnold","h":false,"pl":26},"ARG":{"n":"阿根廷","f":"🇦🇷","r":3,"c":"CONMEBOL","elo":2064,"coach":"Lionel Scaloni","h":false,"pl":26},"ALG":{"n":"阿尔及利亚","f":"🇩🇿","r":28,"c":"CAF","elo":1676,"coach":"Vladimir Petković","h":false,"pl":26},"AUT":{"n":"奥地利","f":"🇦🇹","r":24,"c":"UEFA","elo":1830,"coach":"Ralf Rangnick","h":false,"pl":26},"JOR":{"n":"约旦","f":"🇯🇴","r":64,"c":"AFC","elo":1515,"coach":"Jamal Sellami","h":false,"pl":26},"POR":{"n":"葡萄牙","f":"🇵🇹","r":5,"c":"UEFA","elo":1934,"coach":"Roberto Martínez","h":false,"pl":26},"UZB":{"n":"乌兹别克","f":"🇺🇿","r":57,"c":"AFC","elo":1718,"coach":"Fabio Cannavaro","h":false,"pl":26},"COL":{"n":"哥伦比亚","f":"🇨🇴","r":13,"c":"CONMEBOL","elo":1884,"coach":"Néstor Lorenzo","h":false,"pl":26},"COD":{"n":"刚果民主","f":"🇨🇩","r":55,"c":"CAF","elo":1661,"coach":"Sébastien Desabre","h":false,"pl":26},"ENG":{"n":"英格兰","f":"🏴","r":4,"c":"UEFA","elo":1982,"coach":"Thomas Tuchel","h":false,"pl":26},"CRO":{"n":"克罗地亚","f":"🇭🇷","r":11,"c":"UEFA","elo":1878,"coach":"Zlatko Dalić","h":false,"pl":26},"GHA":{"n":"加纳","f":"🇬🇭","r":73,"c":"CAF","elo":1630,"coach":"Carlos Queiroz","h":false,"pl":26},"PAN":{"n":"巴拿马","f":"🇵🇦","r":51,"c":"CONCACAF","elo":1582,"coach":"Thomas Christiansen","h":false,"pl":26}};

// ===== 分组信息 =====
var GROUPS = {
  A:['MEX','RSA','KOR','CZE'], B:['CAN','SUI','QAT','BIH'],
  C:['BRA','MAR','HAI','SCO'], D:['USA','PAR','AUS','TUR'],
  E:['GER','CUW','CIV','ECU'], F:['NED','JPN','TUN','SWE'],
  G:['BEL','EGY','IRN','NZL'], H:['ESP','CPV','KSA','URU'],
  I:['FRA','SEN','NOR','IRQ'], J:['ARG','ALG','AUT','JOR'],
  K:['POR','UZB','COL','COD'], L:['ENG','CRO','GHA','PAN']
};

// ===== 小组赛赛程（北京时间）=====
var GROUP_SCHEDULE = [
  {d:'2026-06-12',t:'03:00',g:'A',a:'MEX',b:'RSA',v:'墨西哥城阿兹特克',s:'finished',sa:2,sb:0},
  {d:'2026-06-12',t:'10:00',g:'A',a:'KOR',b:'CZE',v:'瓜达拉哈拉',s:'finished',sa:2,sb:1},
  {d:'2026-06-13',t:'03:00',g:'B',a:'CAN',b:'BIH',v:'多伦多',s:'finished',sa:1,sb:1},
  {d:'2026-06-13',t:'09:00',g:'D',a:'USA',b:'PAR',v:'洛杉矶',s:'finished',sa:4,sb:1},
  {d:'2026-06-14',t:'03:00',g:'B',a:'QAT',b:'SUI',v:'旧金山',s:'finished',sa:1,sb:1},
  {d:'2026-06-14',t:'06:00',g:'C',a:'BRA',b:'MAR',v:'纽约新泽西',s:'finished',sa:1,sb:1},
  {d:'2026-06-14',t:'09:00',g:'C',a:'HAI',b:'SCO',v:'波士顿',s:'finished',sa:0,sb:1},
  {d:'2026-06-14',t:'12:00',g:'D',a:'AUS',b:'TUR',v:'温哥华',s:'finished',sa:2,sb:0},
  {d:'2026-06-15',t:'01:00',g:'E',a:'GER',b:'CUW',v:'休斯顿',s:'finished',sa:7,sb:1},
  {d:'2026-06-15',t:'04:00',g:'F',a:'NED',b:'JPN',v:'达拉斯',s:'finished',sa:2,sb:2},
  {d:'2026-06-15',t:'07:00',g:'E',a:'CIV',b:'ECU',v:'费城',s:'finished',sa:1,sb:0},
  {d:'2026-06-15',t:'10:00',g:'F',a:'SWE',b:'TUN',v:'蒙特雷',s:'finished',sa:5,sb:1},
  {d:'2026-06-16',t:'00:00',g:'H',a:'ESP',b:'CPV',v:'亚特兰大',s:'finished',sa:0,sb:0},
  {d:'2026-06-16',t:'03:00',g:'G',a:'BEL',b:'EGY',v:'西雅图',s:'finished',sa:1,sb:1},
  {d:'2026-06-16',t:'06:00',g:'H',a:'KSA',b:'URU',v:'迈阿密',s:'finished',sa:1,sb:1},
  {d:'2026-06-16',t:'09:00',g:'G',a:'IRN',b:'NZL',v:'洛杉矶',s:'finished',sa:2,sb:2},
  {d:'2026-06-17',t:'03:00',g:'I',a:'FRA',b:'SEN',v:'纽约新泽西',s:'finished',sa:3,sb:1},
  {d:'2026-06-17',t:'06:00',g:'I',a:'IRQ',b:'NOR',v:'波士顿',s:'finished',sa:1,sb:4},
  {d:'2026-06-17',t:'09:00',g:'J',a:'ARG',b:'ALG',v:'堪萨斯城',s:'finished',sa:3,sb:0},
  {d:'2026-06-17',t:'12:00',g:'J',a:'AUT',b:'JOR',v:'旧金山',s:'finished',sa:3,sb:1},
  {d:'2026-06-18',t:'01:00',g:'K',a:'POR',b:'COD',v:'休斯顿',s:'finished',sa:1,sb:1},
  {d:'2026-06-18',t:'04:00',g:'L',a:'ENG',b:'CRO',v:'达拉斯',s:'finished',sa:4,sb:2},
  {d:'2026-06-18',t:'07:00',g:'L',a:'GHA',b:'PAN',v:'多伦多',s:'finished',sa:1,sb:0},
  {d:'2026-06-18',t:'10:00',g:'K',a:'UZB',b:'COL',v:'墨西哥城阿兹特克',s:'finished',sa:1,sb:3},
  {d:'2026-06-19',t:'00:00',g:'A',a:'CZE',b:'RSA',v:'亚特兰大',s:'finished',sa:1,sb:1},
  {d:'2026-06-19',t:'03:00',g:'B',a:'SUI',b:'BIH',v:'洛杉矶',s:'finished',sa:4,sb:1},
  {d:'2026-06-19',t:'06:00',g:'B',a:'CAN',b:'QAT',v:'温哥华',s:'finished',sa:6,sb:0},
  {d:'2026-06-19',t:'09:00',g:'A',a:'MEX',b:'KOR',v:'瓜达拉哈拉',s:'finished',sa:1,sb:0},
  {d:'2026-06-20',t:'03:00',g:'D',a:'USA',b:'AUS',v:'西雅图',s:'finished',sa:2,sb:0},
  {d:'2026-06-20',t:'06:00',g:'C',a:'SCO',b:'MAR',v:'波士顿',s:'finished',sa:0,sb:1},
  {d:'2026-06-20',t:'08:30',g:'C',a:'BRA',b:'HAI',v:'费城',s:'finished',sa:3,sb:0},
  {d:'2026-06-20',t:'11:00',g:'D',a:'TUR',b:'PAR',v:'旧金山',s:'finished',sa:0,sb:1},
  {d:'2026-06-21',t:'01:00',g:'F',a:'NED',b:'SWE',v:'休斯顿',s:'finished',sa:5,sb:1},
  {d:'2026-06-21',t:'04:00',g:'E',a:'GER',b:'CIV',v:'多伦多',s:'finished',sa:2,sb:1},
  {d:'2026-06-21',t:'08:00',g:'E',a:'ECU',b:'CUW',v:'堪萨斯城',s:'finished',sa:0,sb:0},
  {d:'2026-06-21',t:'12:00',g:'F',a:'TUN',b:'JPN',v:'蒙特雷',s:'finished',sa:0,sb:4},
  {d:'2026-06-22',t:'00:00',g:'H',a:'ESP',b:'KSA',v:'亚特兰大',s:'finished',sa:4,sb:0},
  {d:'2026-06-22',t:'03:00',g:'G',a:'BEL',b:'IRN',v:'洛杉矶',s:'finished',sa:0,sb:0},
  {d:'2026-06-22',t:'06:00',g:'H',a:'URU',b:'CPV',v:'迈阿密',s:'finished',sa:2,sb:2},
  {d:'2026-06-22',t:'09:00',g:'G',a:'NZL',b:'EGY',v:'温哥华',s:'finished',sa:1,sb:3},
  {d:'2026-06-23',t:'01:00',g:'J',a:'ARG',b:'AUT',v:'达拉斯',s:'finished',sa:2,sb:0},
  {d:'2026-06-23',t:'05:00',g:'I',a:'FRA',b:'IRQ',v:'费城',s:'finished',sa:3,sb:0},
  {d:'2026-06-23',t:'08:00',g:'I',a:'NOR',b:'SEN',v:'纽约新泽西',s:'finished',sa:3,sb:2},
  {d:'2026-06-23',t:'11:00',g:'J',a:'JOR',b:'ALG',v:'旧金山',s:'finished',sa:1,sb:2},
  {d:'2026-06-24',t:'01:00',g:'K',a:'POR',b:'UZB',v:'休斯顿',s:'finished',sa:5,sb:0},
  {d:'2026-06-24',t:'04:00',g:'L',a:'ENG',b:'GHA',v:'温哥华',s:'finished',sa:3,sb:0},
  {d:'2026-06-24',t:'07:00',g:'K',a:'COD',b:'COL',v:'多伦多',s:'finished',sa:1,sb:2},
  {d:'2026-06-24',t:'10:00',g:'L',a:'CRO',b:'PAN',v:'迈阿密',s:'finished',sa:3,sb:1}
];

// ===== 淘汰赛赛程 =====
var KO_SCHEDULE = [
  {d:'2026-06-29',t:'03:00',r:'1/16决赛',a:'A2',b:'B2',v:'洛杉矶',s:'upcoming'},
  {d:'2026-06-29',t:'09:00',r:'1/16决赛',a:'C1',b:'F2',v:'休斯顿',s:'upcoming'},
  {d:'2026-06-30',t:'03:00',r:'1/16决赛',a:'E1',b:'T1',v:'波士顿',s:'upcoming'},
  {d:'2026-06-30',t:'06:00',r:'1/16决赛',a:'F1',b:'C2',v:'蒙特雷',s:'upcoming'},
  {d:'2026-06-30',t:'09:00',r:'1/16决赛',a:'I1',b:'T2',v:'纽约新泽西',s:'upcoming'},
  {d:'2026-07-01',t:'03:00',r:'1/16决赛',a:'E2',b:'I2',v:'达拉斯',s:'upcoming'},
  {d:'2026-07-01',t:'06:00',r:'1/16决赛',a:'A1',b:'T3',v:'墨西哥城阿兹特克',s:'upcoming'},
  {d:'2026-07-01',t:'09:00',r:'1/16决赛',a:'L1',b:'T4',v:'亚特兰大',s:'upcoming'},
  {d:'2026-07-02',t:'03:00',r:'1/16决赛',a:'D1',b:'T5',v:'旧金山',s:'upcoming'},
  {d:'2026-07-02',t:'06:00',r:'1/16决赛',a:'G1',b:'T6',v:'西雅图',s:'upcoming'},
  {d:'2026-07-02',t:'09:00',r:'1/16决赛',a:'K2',b:'L2',v:'多伦多',s:'upcoming'},
  {d:'2026-07-03',t:'03:00',r:'1/16决赛',a:'H1',b:'J2',v:'洛杉矶',s:'upcoming'},
  {d:'2026-07-03',t:'06:00',r:'1/16决赛',a:'B1',b:'T7',v:'温哥华',s:'upcoming'},
  {d:'2026-07-03',t:'09:00',r:'1/16决赛',a:'J1',b:'H2',v:'迈阿密',s:'upcoming'},
  {d:'2026-07-04',t:'03:00',r:'1/16决赛',a:'K1',b:'T8',v:'堪萨斯城',s:'upcoming'},
  {d:'2026-07-04',t:'06:00',r:'1/16决赛',a:'D2',b:'G2',v:'达拉斯',s:'upcoming'},
  {d:'2026-07-05',t:'03:00',r:'1/8决赛',a:'W1',b:'W2',v:'费城',s:'upcoming'},
  {d:'2026-07-06',t:'03:00',r:'1/8决赛',a:'W3',b:'W4',v:'纽约新泽西',s:'upcoming'},
  {d:'2026-07-06',t:'09:00',r:'1/8决赛',a:'W5',b:'W6',v:'达拉斯',s:'upcoming'},
  {d:'2026-07-07',t:'03:00',r:'1/8决赛',a:'W7',b:'W8',v:'亚特兰大',s:'upcoming'},
  {d:'2026-07-07',t:'09:00',r:'1/8决赛',a:'W9',b:'W10',v:'西雅图',s:'upcoming'},
  {d:'2026-07-08',t:'03:00',r:'1/8决赛',a:'W11',b:'W12',v:'多伦多',s:'upcoming'},
  {d:'2026-07-08',t:'09:00',r:'1/8决赛',a:'W13',b:'W14',v:'温哥华',s:'upcoming'},
  {d:'2026-07-09',t:'03:00',r:'1/8决赛',a:'W15',b:'W16',v:'迈阿密',s:'upcoming'},
  {d:'2026-07-10',t:'03:00',r:'1/4决赛',a:'W17',b:'W18',v:'波士顿',s:'upcoming'},
  {d:'2026-07-11',t:'03:00',r:'1/4决赛',a:'W19',b:'W20',v:'洛杉矶',s:'upcoming'},
  {d:'2026-07-11',t:'09:00',r:'1/4决赛',a:'W21',b:'W22',v:'迈阿密',s:'upcoming'},
  {d:'2026-07-12',t:'03:00',r:'1/4决赛',a:'W23',b:'W24',v:'堪萨斯城',s:'upcoming'},
  {d:'2026-07-15',t:'03:00',r:'半决赛',a:'W25',b:'W26',v:'达拉斯',s:'upcoming'},
  {d:'2026-07-16',t:'03:00',r:'半决赛',a:'W27',b:'W28',v:'亚特兰大',s:'upcoming'},
  {d:'2026-07-19',t:'03:00',r:'季军赛',a:'L29',b:'L30',v:'迈阿密',s:'upcoming'},
  {d:'2026-07-20',t:'03:00',r:'决赛',a:'W29',b:'W30',v:'纽约新泽西',s:'upcoming'}
];

// ===== 冠军预测数据 =====
var CHAMPION_PREDICTION = {
  champion: [
    {rank:1,code:'ESP',name:'西班牙',flag:'🇪🇸',stars:5,pct:23.7,reason:'Cup26最高23.7%，铁律全部通过，亚马尔+佩德里双核'},
    {rank:2,code:'ARG',name:'阿根廷',flag:'🇦🇷',stars:5,pct:20.3,reason:'Cup26第二20.3%，卫冕冠军，梅西最后一届世界杯'},
    {rank:3,code:'FRA',name:'法国',flag:'🇫🇷',stars:4,pct:15.8,reason:'Cup26第三15.8%，阵容深度最强，姆巴佩世界最佳'},
    {rank:4,code:'GER',name:'德国',flag:'🇩🇪',stars:3,pct:3.6,reason:'铁律通过，维尔茨+穆西亚拉双核，但ELO偏低'},
    {rank:5,code:'COL',name:'哥伦比亚',flag:'🇨🇴',stars:3,pct:1.8,reason:'铁律通过，迪亚兹领衔，但整体实力略逊'}
  ],
  top5Total: 65.2,
  otherPredictions: [
    {label:'最可能决赛',value:'🇪🇸 西班牙 vs 🇦🇷 阿根廷'},
    {label:'最佳射手热门',value:'姆巴佩、劳塔罗、哈兰德、孙兴慜'},
    {label:'最大黑马',value:'🇲🇦 摩洛哥、🇯🇵 日本'},
    {label:'东道主表现',value:'美国/墨西哥至少进16强'},
    {label:'小组赛冷门',value:'至少1支赔率前8球队出局'}
  ],
  ironLaws: [
    {law:'本土教练定律',desc:'22届世界杯冠军均由本土教练执教，排除巴西/葡萄牙/英格兰/美国/乌拉圭'},
    {law:'五大联赛定律',desc:'非五大联赛所在国从未夺冠，排除荷兰/比利时/克罗地亚等'},
    {law:'大洲垄断定律',desc:'亚洲/非洲/北美球队从未进入决赛，排除全部亚非北美队'}
  ]
};

// ===== 辅助函数 =====

function getTeam(code) {
  var t = TEAM_STATS[code];
  if (!t) return null;
  return { code: code, name: t.n, flag: t.f, rank: t.r, conf: t.c, elo: t.elo, coach: t.coach, host: !!t.h, squadSize: t.pl };
}

function getTeamName(code) {
  var t = TEAM_STATS[code];
  return t ? t.n : code;
}

function getTeamFlag(code) {
  var t = TEAM_STATS[code];
  return t ? t.f : '🏳️';
}

function getTeamElo(code) {
  var t = TEAM_STATS[code];
  return t ? t.elo : 1600;
}

function getStoredResults() {
  try {
    var data = wx.getStorageSync('wc2026_results');
    if (data) { if (typeof data === 'string') return JSON.parse(data); return data; }
  } catch(e) {}
  return [];
}

function getMergedSchedule() {
  var results = getStoredResults();
  var merged = GROUP_SCHEDULE.map(function(m) {
    var match = { date: m.d, time: m.t, group: m.g, venue: m.v, teamA: m.a, teamB: m.b,
      teamAName: getTeamName(m.a), teamBName: getTeamName(m.b), teamAFlag: getTeamFlag(m.a), teamBFlag: getTeamFlag(m.b),
      status: m.s };
    if (m.sa !== undefined) { match.scoreA = m.sa; match.scoreB = m.sb; }
    // 从storage结果覆盖
    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      if (r.date === m.d && (r.teamA === m.a || r.a === m.a) && (r.teamB === m.b || r.b === m.b)) {
        match.scoreA = r.scoreA; match.scoreB = r.scoreB; match.status = 'finished';
        if (r.penWinner) { match.penWinner = r.penWinner; match.penScoreA = r.penScoreA; match.penScoreB = r.penScoreB; }
        break;
      }
    }
    return match;
  });
  KO_SCHEDULE.forEach(function(m) {
    var match = { date: m.d, time: m.t, round: m.r, venue: m.v, teamA: m.a, teamB: m.b,
      teamAName: m.a, teamBName: m.b, teamAFlag: getTeamFlag(m.a), teamBFlag: getTeamFlag(m.b), status: m.s };
    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      if (r.date === m.d && (r.teamA === m.a || r.a === m.a) && (r.teamB === m.b || r.b === m.b)) {
        match.scoreA = r.scoreA; match.scoreB = r.scoreB; match.status = 'finished';
        if (r.penWinner) { match.penWinner = r.penWinner; match.penScoreA = r.penScoreA; match.penScoreB = r.penScoreB; }
        break;
      }
    }
    merged.push(match);
  });
  return merged;
}

function getUpcomingMatches(count) {
  count = count || 5;
  var all = getMergedSchedule();
  var now = new Date();
  var upcoming = [];
  for (var i = 0; i < all.length; i++) {
    var m = all[i];
    if (m.status === 'finished' || m.status === 'live') continue;
    var mt = new Date(m.date + 'T' + m.time + ':00+08:00').getTime();
    if (mt > now.getTime()) { upcoming.push(m); if (upcoming.length >= count) break; }
  }
  return upcoming;
}

function getRecentResults(count) {
  count = count || 5;
  var all = getMergedSchedule();
  var finished = all.filter(function(m) { return m.status === 'finished'; });
  finished.sort(function(a, b) { return new Date(b.date + 'T' + b.time) - new Date(a.date + 'T' + a.time); });
  return finished.slice(0, count);
}

function getGroupStandings(group) {
  var teams = GROUPS[group] || [];
  var standings = teams.map(function(code) {
    return { code: code, name: getTeamName(code), flag: getTeamFlag(code), played: 0, win: 0, draw: 0, lose: 0, gf: 0, ga: 0, gd: 0, pts: 0 };
  });
  var all = getMergedSchedule();
  all.forEach(function(m) {
    if (m.group !== group || m.status !== 'finished' || m.scoreA === undefined) return;
    var aIdx = teams.indexOf(m.teamA); var bIdx = teams.indexOf(m.teamB);
    if (aIdx < 0 || bIdx < 0) return;
    var a = standings[aIdx]; var b = standings[bIdx];
    a.played++; b.played++; a.gf += m.scoreA; a.ga += m.scoreB; b.gf += m.scoreB; b.ga += m.scoreA;
    if (m.scoreA > m.scoreB) { a.win++; a.pts += 3; b.lose++; }
    else if (m.scoreA < m.scoreB) { b.win++; b.pts += 3; a.lose++; }
    else { a.draw++; b.draw++; a.pts++; b.pts++; }
  });
  standings.forEach(function(s) { s.gd = s.gf - s.ga; });
  standings.sort(function(a, b) { if (b.pts !== a.pts) return b.pts - a.pts; if (b.gd !== a.gd) return b.gd - a.gd; return b.gf - a.gf; });
  return standings;
}

function calcWinProb(eloA, eloB) {
  var diff = eloA - eloB;
  return Math.round((1 / (1 + Math.pow(10, -diff / 400))) * 100);
}

function calcGoalExpect(eloA, eloB) {
  var diff = eloA - eloB;
  return { goalA: Math.max(0.3, Math.min(3.5, 1.35 + diff / 350)), goalB: Math.max(0.3, Math.min(3.5, 1.35 - diff / 350)) };
}

function predictMatch(teamA, teamB) {
  var eloA = getTeamElo(teamA); var eloB = getTeamElo(teamB);
  var winProb = calcWinProb(eloA, eloB);
  var goals = calcGoalExpect(eloA, eloB);
  var scoreA = Math.round(goals.goalA); var scoreB = Math.round(goals.goalB);
  if (scoreA === scoreB) { if (winProb > 55) scoreA++; else if (winProb < 45) scoreB++; }
  return { teamA: teamA, teamB: teamB, teamAName: getTeamName(teamA), teamBName: getTeamName(teamB),
    teamAFlag: getTeamFlag(teamA), teamBFlag: getTeamFlag(teamB), eloA: eloA, eloB: eloB, eloDiff: eloA - eloB,
    winProbA: winProb, drawProb: Math.round(100 - Math.abs(2 * winProb - 100) * 0.6), winProbB: 100 - winProb,
    predictedScore: scoreA + ':' + scoreB, expectedGoals: { teamA: goals.goalA.toFixed(1), teamB: goals.goalB.toFixed(1) } };
}

module.exports = {
  TEAM_STATS: TEAM_STATS, GROUPS: GROUPS, GROUP_SCHEDULE: GROUP_SCHEDULE, KO_SCHEDULE: KO_SCHEDULE,
  CHAMPION_PREDICTION: CHAMPION_PREDICTION,
  getTeam: getTeam, getTeamName: getTeamName, getTeamFlag: getTeamFlag, getTeamElo: getTeamElo,
  getStoredResults: getStoredResults, getMergedSchedule: getMergedSchedule,
  getUpcomingMatches: getUpcomingMatches, getRecentResults: getRecentResults,
  getGroupStandings: getGroupStandings, calcWinProb: calcWinProb, calcGoalExpect: calcGoalExpect, predictMatch: predictMatch
};
