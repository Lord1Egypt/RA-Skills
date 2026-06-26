/**
 * 六星占術 v2.0 多语言数据
 * 支持: zh (中文), en (English), ja (日本語)
 * 新增: lucky(幸运元素), compatibility(配对), weakness/strength, fortune rating
 */

const i18n = {
  starTypes: {
    土星: {
      zh: { name:'土星',icon:'🪐',summary:'稳重如山的传统守护者',personality:'稳重踏实，重视传统和安全感。有强烈的责任感和使命感，但有时过于固执。',career:'教育、研究、管理、不动产、农业、历史研究。',love:'忠诚可靠，但不善表达感情。你的爱是沉默而深沉的。',advice:'学会放下控制欲，接受变化。你的稳定性是优势，但不要让它变成枷锁。',lucky:{color:['黄色','棕色'],direction:'中央',number:[5,8],season:'四季交替'},weakness:'过于固执、不善变通、压抑情感',strength:'可靠、持久、有责任心、脚踏实地',polarity_pos:'土星人（正）',polarity_neg:'土星人（负）' },
      en: { name:'Saturn',icon:'🪐',summary:'Steady as a mountain, the traditional guardian',personality:'Steady and grounded, you value tradition and security. Strong sense of responsibility, but can be stubborn.',career:'Education, research, management, real estate, agriculture, history.',love:'Loyal and reliable, but not great at expressing feelings. Your love is silent yet deep.',advice:'Learn to let go of control and embrace change.',lucky:{color:['Yellow','Brown'],direction:'Center',number:[5,8],season:'Seasonal transitions'},weakness:'Too stubborn, inflexible, suppresses emotions',strength:'Reliable, persistent, responsible, grounded',polarity_pos:'Saturn (+)',polarity_neg:'Saturn (-)' },
      ja: { name:'土星',icon:'🪐',summary:'山のように穏やかな伝統の守護者',personality:'穏やかで落ち着きがあり、伝統と安全感を重んじる。強い責任感を持つが、時に頑固すぎる。',career:'教育、研究、管理、不動産、農業、歴史研究。',love:'誠実で頼りになるが、感情表現が苦手。あなたの愛は静かで深い。',advice:'コントロール欲を手放し、変化を受け入れよう。',lucky:{color:['黄色','茶色'],direction:'中央',number:[5,8],season:'四季の変わり目'},weakness:'頑固すぎる、変化に弱い、感情を抑える',strength:'頼りになる、持続力がある、責任感が強い',polarity_pos:'土星人（＋）',polarity_neg:'土星人（－）' },
    },
    金星: {
      zh: { name:'金星',icon:'💫',summary:'锋利如剑的完美主义者',personality:'果断坚毅，追求完美。有很强的执行力和决断力，但容易过于严苛。',career:'金融、法律、医疗、工程、设计、奢侈品行业。',love:'对感情认真专一，但标准太高。学会接受不完美才是真正的完美。',advice:'放松标准，享受过程。完美主义是把双刃剑。',lucky:{color:['白色','金色'],direction:'西方',number:[4,9],season:'秋天'},weakness:'过于严苛、洁癖、不宽容',strength:'精确、果断、有品味、意志坚定',polarity_pos:'金星人（正）',polarity_neg:'金星人（负）' },
      en: { name:'Venus',icon:'💫',summary:'Sharp as a sword, the perfectionist',personality:'Decisive and resolute, you pursue perfection. Strong execution and decision-making, but can be overly critical.',career:'Finance, law, medicine, engineering, design, luxury.',love:'Serious and devoted, but your standards are too high.',advice:'Lower your standards and enjoy the process.',lucky:{color:['White','Gold'],direction:'West',number:[4,9],season:'Autumn'},weakness:'Too critical, perfectionist, unforgiving',strength:'Precise, decisive, refined taste, strong-willed',polarity_pos:'Venus (+)',polarity_neg:'Venus (-)' },
      ja: { name:'金星',icon:'💫',summary:'剣のように鋭い完美主義者',personality:'果断で揺るぎなく、完美主義者。強い実行力と決断力を持つが、時に厳しすぎる。',career:'金融、法律、医療、工学、デザイン。',love:'恋愛に対して真剣で一途だが、基準が高すぎる。',advice:'基準を緩め、プロセスを楽しもう。',lucky:{color:['白','金'],direction:'西',number:[4,9],season:'秋'},weakness:'厳しすぎる、完美主義、不寛容',strength:'正確、果断、品がある、意志が強い',polarity_pos:'金星人（＋）',polarity_neg:'金星人（－）' },
    },
    火星: {
      zh: { name:'火星',icon:'🔴',summary:'燃烧不息的热情行动派',personality:'热情奔放，行动力强。有领袖气质，但容易冲动和急躁。',career:'销售、营销、娱乐、创业、体育、演艺。',love:'恋爱中充满激情，但也容易大起大落。',advice:'控制你的火焰——它能温暖人心，也能烧毁一切。',lucky:{color:['红色','橙色'],direction:'南方',number:[3,7],season:'夏天'},weakness:'冲动、急躁、三分钟热度',strength:'热情、有感染力、行动迅速、勇敢',polarity_pos:'火星人（正）',polarity_neg:'火星人（负）' },
      en: { name:'Mars',icon:'🔴',summary:'Burning with unstoppable passion and action',personality:'Passionate and action-oriented, you have natural leadership. But can be impulsive and impatient.',career:'Sales, marketing, entertainment, entrepreneurship, sports.',love:'Full of passion in romance, but prone to ups and downs.',advice:'Control your fire — it can warm hearts, but also burn everything down.',lucky:{color:['Red','Orange'],direction:'South',number:[3,7],season:'Summer'},weakness:'Impulsive, impatient, short attention span',strength:'Passionate, infectious energy, quick to act, brave',polarity_pos:'Mars (+)',polarity_neg:'Mars (-)' },
      ja: { name:'火星',icon:'🔴',summary:'燃え続ける情熱の行動派',personality:'情熱的で行動力があり、リーダーシップの气质がある。ただし衝動的で短気。',career:'営業、マーケティング、エンタメ、起業、スポーツ。',love:'恋愛では情熱的だが、大きく揺れ动くこともある。',advice:'あなたの炎をコントロールしよう。',lucky:{color:['赤','オレンジ'],direction:'南',number:[3,7],season:'夏'},weakness:'衝動的、短気、飽きっぽい',strength:'情熱的、感染力がある、行動が速い、勇敢',polarity_pos:'火星人（＋）',polarity_neg:'火星人（－）' },
    },
    天王星: {
      zh: { name:'天王星',icon:'🌀',summary:'独立不羁的创新先驱',personality:'独立创新，不走寻常路。有很强的洞察力和创新能力，但容易孤独。',career:'科技、艺术、研究、自由职业、发明、前沿领域。',love:'需要精神上的共鸣，不喜欢束缚。',advice:'拥抱你的独特性，但也要学会与人连接。',lucky:{color:['银色','紫色'],direction:'天顶',number:[1,6],season:'冬春之交'},weakness:'孤独、不合群、过于理想化',strength:'创新、独立、洞察力强、前瞻性',polarity_pos:'天王星人（正）',polarity_neg:'天王星人（负）' },
      en: { name:'Uranus',icon:'🌀',summary:'Independent pioneer of innovation',personality:'Independent and innovative, you forge your own path. Strong insight and creativity, but prone to loneliness.',career:'Tech, arts, research, freelancing, invention, frontier fields.',love:'Needs mental resonance, dislikes束缚.',advice:'Embrace your uniqueness, but also learn to connect with others.',lucky:{color:['Silver','Purple'],direction:'Zenith',number:[1,6],season:'Winter-Spring'},weakness:'Lonely, non-conformist, too idealistic',strength:'Innovative, independent, insightful, forward-thinking',polarity_pos:'Uranus (+)',polarity_neg:'Uranus (-)' },
      ja: { name:'天王星',icon:'🌀',summary:'独立独歩の革新の先駆者',personality:'独立独歩で革新的、普通の道を歩かない。強い洞察力を持つが、孤独になりやすい。',career:'テクノロジー、アート、研究、フリーランス。',love:'精神的な共感を求める束縛を嫌う。',advice:'あなたのユニークさを受け入れよう。人とつながることも学ぼう。',lucky:{color:['シルバー','紫'],direction:'天頂',number:[1,6],season:'冬春の変わり目'},weakness:'孤独、協調性がない、理想主義すぎる',strength:'革新的、独立、洞察力がある、先見性がある',polarity_pos:'天王星人（＋）',polarity_neg:'天王星人（－）' },
    },
    木星: {
      zh: { name:'木星',icon:'🌿',summary:'生机勃勃的社交达人',personality:'乐观开朗，人缘极好。有很强的社交能力和适应力，但容易随波逐流。',career:'公关、教育、服务、媒体、旅游、外交。',love:'桃花运旺盛，但容易三心二意。',advice:'利用你的人脉优势，但不要为了合群而失去自我。',lucky:{color:['绿色','蓝色'],direction:'东方',number:[2,7],season:'春天'},weakness:'随波逐流、优柔寡断、缺乏深度',strength:'社交能力强、乐观、适应力好、有人缘',polarity_pos:'木星人（正）',polarity_neg:'木星人（负）' },
      en: { name:'Jupiter',icon:'🌿',summary:'Vibrant social butterfly with golden charm',personality:'Optimistic and sociable, you are a people magnet. Strong social skills and adaptability.',career:'PR, education, service, media, tourism, diplomacy.',love:'Romantically lucky, but prone to indecision.',advice:'Leverage your social network, but don\'t lose yourself.',lucky:{color:['Green','Blue'],direction:'East',number:[2,7],season:'Spring'},weakness:'Easily influenced, indecisive, lacks depth',strength:'Great social skills, optimistic, adaptable, charming',polarity_pos:'Jupiter (+)',polarity_neg:'Jupiter (-)' },
      ja: { name:'木星',icon:'🌿',summary:'生き生きとした社交の達人',personality:'明るく楽観的で、人缘が極めて良い。強い社交能力を持つが、流されやすい。',career:'PR、教育、サービス、メディア、観光、外交。',love:'恋愛運が盛んだが、気が変わりやすい。',advice:'人脈を活かそう。馴れ合いで自分を失うことのないように。',lucky:{color:['緑','青'],direction:'東',number:[2,7],season:'春'},weakness:'流されやすい、優柔不断、深みがない',strength:'社交性が高い、楽観的、適応力がある',polarity_pos:'木星人（＋）',polarity_neg:'木星人（－）' },
    },
    水星: {
      zh: { name:'水星',icon:'💧',summary:'灵动聪慧的智慧源泉',personality:'聪明机智，思维敏捷。有很强的学习能力和适应力，但容易浮躁。',career:'咨询、IT、贸易、金融、写作、策划。',love:'善于沟通，但容易用理智代替感情。',advice:'你的智慧是天赋，但不要让它成为逃避情感的借口。',lucky:{color:['黑色','深蓝'],direction:'北方',number:[1,6],season:'冬天'},weakness:'浮躁、善变、缺乏毅力',strength:'聪明、灵活、学习能力强、善于沟通',polarity_pos:'水星人（正）',polarity_neg:'水星人（负）' },
      en: { name:'Mercury',icon:'💧',summary:'Quick-witted fountain of wisdom',personality:'Quick-witted and sharp-minded. Strong learning ability and adaptability.',career:'Consulting, IT, trade, finance, writing, planning.',love:'Great communicator, but tends to replace feelings with logic.',advice:'Your wisdom is a gift, but don\'t let it become an excuse to avoid emotions.',lucky:{color:['Black','Dark Blue'],direction:'North',number:[1,6],season:'Winter'},weakness:'Restless, fickle, lacks perseverance',strength:'Smart, flexible, quick learner, great communicator',polarity_pos:'Mercury (+)',polarity_neg:'Mercury (-)' },
      ja: { name:'水星',icon:'💧',summary:'賢く機敏な知恵の源',personality:'聡明機敏で、思考が敏捷。強い学習能力を持つが、浮つきやすい。',career:'コンサルティング、IT、貿易、金融、執筆。',love:'コミュニケーションが得意だが、感情を理性で飲み込みがち。',advice:'あなたの知恵は才能だ。感情逃避の口実にしないこと。',lucky:{color:['黒','紺色'],direction:'北',number:[1,6],season:'冬'},weakness:'浮つきやすい、気が変わりやすい、根気がない',strength:'賢い、柔軟、学習能力が高い',polarity_pos:'水星人（＋）',polarity_neg:'水星人（－）' },
    },
  },

  compatibility: {
    zh: { '土星-金星':'★★★★★ 最佳搭配','土星-木星':'★★★★ 默契','金星-火星':'★★★★ 火热组合','金星-木星':'★★★★ 和谐','金星-水星':'★★★★ 知性组合','火星-天王星':'★★★★ 冒险组合','天王星-水星':'★★★★ 智慧组合','土星-火星':'★★★ 互补','土星-水星':'★★★ 互补','金星-天王星':'★★★ 刺激组合','火星-木星':'★★★ 活力组合','火星-水星':'★★★ 动态组合','天王星-木星':'★★★ 自由组合','木星-木星':'★★★ 快乐组合','木星-水星':'★★★ 活泼组合','水星-水星':'★★★ 知性组合','土星-天王星':'★★ 对极组合' },
    en: { 'Saturn-Venus':'★★★★★ Perfect match','Saturn-Jupiter':'★★★★ Harmony','Venus-Mars':'★★★★ Hot combo','Venus-Jupiter':'★★★★ Harmonious','Venus-Mercury':'★★★★ Intellectual','Mars-Uranus':'★★★★ Adventure','Uranus-Mercury':'★★★★ Wisdom','Saturn-Mars':'★★★ Complementary','Saturn-Mercury':'★★★ Complementary','Venus-Uranus':'★★★ Exciting','Mars-Jupiter':'★★★ Energy','Mars-Mercury':'★★★ Dynamic','Uranus-Jupiter':'★★★ Freedom','Jupiter-Jupiter':'★★★ Happy','Jupiter-Mercury':'★★★ Lively','Mercury-Mercury':'★★★ Intellectual','Saturn-Uranus':'★★ Opposite poles' },
    ja: { '土星-金星':'★★★★★ 最良の組み合わせ','土星-木星':'★★★★ ハーモニー','金星-火星':'★★★★ 熱いコンボ','金星-木星':'★★★★ ハーモニー','金星-水星':'★★★★ 知的コンボ','火星-天王星':'★★★★ 冒険コンボ','天王星-水星':'★★★★ 知恵コンボ','土星-火星':'★★★ 互补','土星-水星':'★★★ 互补','金星-天王星':'★★★ 刺激的','火星-木星':'★★★ エネルギー','火星-水星':'★★★ ダイナミック','天王星-木星':'★★★ 自由','木星-木星':'★★★ ハッピー','木星-水星':'★★★ 活発','水星-水星':'★★★ 知的','土星-天王星':'★★ 対極' },
  },

  cyclePhases: [
    {name:{zh:'種子',en:'Seed',ja:'種子'},roman:'Shushi',desc:{zh:'万物开始萌芽的时期。',en:'All things begin to sprout.',ja:'万物が芽吹き始める時期。'},advice:{zh:'适合开始新事物，要有耐心。',en:'Good time to start, be patient.',ja:'始め的好機。忍耐が必要。'},fortune:{zh:'★★★',en:'★★★',ja:'★★★'}},
    {name:{zh:'緑生',en:'Growth',ja:'緑生'},roman:'Ryokusei',desc:{zh:'一切影响加倍，成长时期。',en:'All influences double, growth period.',ja:'影響が2倍、成長の時期。'},advice:{zh:'乘势而上，不要贪多。',en:'Ride the momentum, don\'t overdo it.',ja:'勢いに乗ろう。欲張らないこと。'},fortune:{zh:'★★★★',en:'★★★★',ja:'★★★★'}},
    {name:{zh:'立花',en:'Bloom',ja:'立花'},roman:'Rikka',desc:{zh:'基本方向确定的重要时期。',en:'Critical period where direction is set.',ja:'方向が決まる重要な時期。'},advice:{zh:'做出关键选择，但要谨慎。',en:'Make key choices, be cautious.',ja:'重要な選択。慎重に。'},fortune:{zh:'★★★★',en:'★★★★',ja:'★★★★'}},
    {name:{zh:'健弱',en:'Fragile',ja:'健弱'},roman:'Kenjaku',desc:{zh:'小杀界——健康运势变差。',en:'Small Sakkai — health fortune declines.',ja:'小殺界——健康運が悪化。'},advice:{zh:'注意身体，不要过度劳累。',en:'Take care of health, don\'t overwork.',ja:'体に気を配り、働きすぎない。'},fortune:{zh:'★★',en:'★★',ja:'★★'}},
    {name:{zh:'達成',en:'Achievement',ja:'達成'},roman:'Tassei',desc:{zh:'目的达成的时期。',en:'Goals are achieved.',ja:'目的が達成される時期。'},advice:{zh:'收获成果，不要骄傲。',en:'Harvest results, stay humble.',ja:'成果を収める。慢心しないこと。'},fortune:{zh:'★★★★★',en:'★★★★★',ja:'★★★★★'}},
    {name:{zh:'乱気',en:'Chaos',ja:'乱気'},roman:'Ranki',desc:{zh:'中杀界——精神容易受打击。',en:'Medium Sakkai — emotionally vulnerable.',ja:'中殺界——精神的にダメージを受けやすい。'},advice:{zh:'保持内心平静，避免冲动。',en:'Keep peace, avoid impulses.',ja:'心を平穏に。衝動を避けよう。'},fortune:{zh:'★★',en:'★★',ja:'★★'}},
    {name:{zh:'再会',en:'Reunion',ja:'再会'},roman:'Saikai',desc:{zh:'第二出发点，适合挽回。',en:'Second starting point, good for recovery.',ja:'第二の出発点。挽回に適する。'},advice:{zh:'重新开始的好时机。',en:'Good time to start fresh.',ja:'やり直し的好機。'},fortune:{zh:'★★★★',en:'★★★★',ja:'★★★★'}},
    {name:{zh:'財成',en:'Wealth',ja:'財成'},roman:'Zaisei',desc:{zh:'财富到来的时期。',en:'Wealth arrives.',ja:'富が入る時期。'},advice:{zh:'把握财运，不要贪心。',en:'Seize opportunity, don\'t be greedy.',ja:'財運を掴もう。貪欲にならないこと。'},fortune:{zh:'★★★★★',en:'★★★★★',ja:'★★★★★'}},
    {name:{zh:'安定',en:'Stability',ja:'安定'},roman:'Antei',desc:{zh:'维持现状，新开始会受苦。',en:'Maintain status quo, new starts will suffer.',ja:'現状維持。新規開始は苦労する。'},advice:{zh:'稳扎稳打，不要冒进。',en:'Stay steady, don\'t rush.',ja:'穩やかに進め。'},fortune:{zh:'★★★',en:'★★★',ja:'★★★'}},
    {name:{zh:'陰影',en:'Shadow',ja:'陰影'},roman:'In\'ei',desc:{zh:'大杀界开始——冬季初期。',en:'Great Sakkai begins — early winter.',ja:'大殺界開始——冬の初期。'},advice:{zh:'收缩战线，养精蓄锐。',en:'Retreat and conserve energy.',ja:'戦線を引き、精力を蓄えよう。'},fortune:{zh:'★',en:'★',ja:'★'}},
    {name:{zh:'停止',en:'Standstill',ja:'停止'},roman:'Teishi',desc:{zh:'大杀界中央——最危险时期。',en:'Great Sakkai center — most dangerous.',ja:'大殺界中間——最も危険。'},advice:{zh:'保持低调，等待黎明。',en:'Keep low profile, wait for dawn.',ja:'控えめに過ごそう。'},fortune:{zh:'★',en:'★',ja:'★'}},
    {name:{zh:'減退',en:'Decline',ja:'減退'},roman:'Gentai',desc:{zh:'大杀界结束——冬季后期。',en:'Great Sakkai ends — late winter.',ja:'大殺界終了——冬の後期。'},advice:{zh:'黎明前的黑暗，坚持住。',en:'Darkest before dawn, hold on.',ja:'夜明け前の暗闘。もう少し。'},fortune:{zh:'★★',en:'★★',ja:'★★'}},
  ],

  shukumei: [
    {name:'静雲星',en:'Still Cloud',desc:{zh:'空想与浪漫，反叛，孤独',en:'Fantasy, romance, rebellion, loneliness',ja:'空想とロマン、反発、孤独'}},
    {name:'光美星',en:'Radiant Beauty',desc:{zh:'想要传达，大方',en:'Want to convey, generous',ja:'伝える、おおらかさ'}},
    {name:'妙雅星',en:'Subtle Elegance',desc:{zh:'守护立场，协调，说服力',en:'Protect position, harmony, persuasion',ja:'立場を守る、協調、説得力'}},
    {name:'白照星',en:'White Light',desc:{zh:'自我，顽固，独立，意志力',en:'Ego, stubbornness, independence, willpower',ja:'自我、頑固、独立、意思'}},
    {name:'香創星',en:'Fragrant Creation',desc:{zh:'继承智慧，知性，传统',en:'Inherit wisdom, intellect, tradition',ja:'知恵を継承、知性、伝統'}},
    {name:'火竹星',en:'Fire Bamboo',desc:{zh:'好奇心，忍耐，改革',en:'Curiosity, endurance, reform',ja:'好奇心、忍耐、改革'}},
    {name:'大木星',en:'Great Tree',desc:{zh:'责任感，名誉，组织力',en:'Duty, honor, organization',ja:'責任感、名誉、組織力'}},
    {name:'風行星',en:'Wind Star',desc:{zh:'动乱期力量，行动力',en:'Power in turbulence, action',ja:'動乱期の力、行動力'}},
    {name:'大善星',en:'Great Goodness',desc:{zh:'大器晚成，家庭，蓄财',en:'Late bloomer, family, wealth',ja:'大器晩成、家庭、蓄財'}},
    {name:'緑水星',en:'Green Water',desc:{zh:'财运，爱情运，义理',en:'Financial luck, love, loyalty',ja:'財運、愛情運、義理'}},
  ],

  oppositeStar: { 土星:'天王星',天王星:'土星',金星:'木星',木星:'金星',火星:'水星',水星:'火星' },

  warnings: {
    zh: { 隱影:'⚠️ 大杀界期间，不宜做重大决定。',停止:'⚠️ 大杀界最危险时期，保持低调。',減退:'⚠️ 大杀界尾声，仍需谨慎。',健弱:'⚠️ 小杀界期间，注意身体健康。',乱気:'⚠️ 中杀界期间，保持内心平静。' },
    en: { 隱影:'⚠️ Great Sakkai — major decisions not recommended.',停止:'⚠️ Most dangerous period, keep low profile.',減退:'⚠️ End of Great Sakkai, still be cautious.',健弱:'⚠️ Small Sakkai, pay attention to health.',乱気:'⚠️ Medium Sakkai, maintain inner peace.' },
    ja: { 隴影:'⚠️ 大殺界中——重大な決定は避けること。',停止:'⚠️ 大殺界で最も危険。控えめに。',減退:'⚠️ 大殺界終盤。まだ注意が必要。',健弱:'⚠️ 小殺界中——健康に注意。',乱気:'⚠️ 中殺界中——心の平穏を保つ。' },
  },

  labels: {
    zh: { title:'六星占術命盘',date:'生日',dayPillar:'日柱',starNumber:'星数',starType:'星型',polarity:'极性',polarityPos:'正极（阳）',polarityNeg:'负极（阴）',reigo:'霊合星人——对极星重叠的特殊命格',personality:'性格特征',career:'事业方向',love:'恋爱婚姻',advice:'人生建议',lucky:'幸运元素',weakness:'弱点',strength:'优势',shukumei:'宿命星',opposite:'对极星',compatibility:'星型配对',cycle:'12年周期·当前阶段',phase:'阶段',yearsOld:'岁',age:'年龄',year:'年份',period:'阶段',fortune:'运势',sakkaiGreat:'大杀界',sakkaiMedium:'中杀界',sakkaiSmall:'小杀界',good:'✅' },
    en: { title:'Six Star Astrology Chart',date:'Birth Date',dayPillar:'Day Pillar',starNumber:'Star Number',starType:'Star Type',polarity:'Polarity',polarityPos:'Positive (+)',polarityNeg:'Negative (-)',reigo:'Reigo Seijin — Special destiny with overlapping polar stars',personality:'Personality',career:'Career',love:'Love & Marriage',advice:'Life Advice',lucky:'Lucky Elements',weakness:'Weakness',strength:'Strengths',shukumei:'Destiny Star',opposite:'Opposite Star',compatibility:'Star Compatibility',cycle:'12-Year Cycle · Current Phase',phase:'Phase',yearsOld:'y',age:'Age',year:'Year',period:'Phase',fortune:'Fortune',sakkaiGreat:'Great Sakkai',sakkaiMedium:'Medium Sakkai',sakkaiSmall:'Small Sakkai',good:'✅' },
    ja: { title:'六星占術 命盤',date:'誕生日',dayPillar:'日柱',starNumber:'星数',starType:'星型',polarity:'極性',polarityPos:'正極（陽）',polarityNeg:'負極（陰）',reigo:'霊合星人——対極星が重なる特殊な命格',personality:'性格特徴',career:'職業方向',love:'恋愛・結婚',advice:'人生アドバイス',lucky:'ラッキーエレメント',weakness:'弱点',strength:'強み',shukumei:'宿命星',opposite:'対極星',compatibility:'星型相性',cycle:'12年周期·現在の段階',phase:'段階',yearsOld:'歳',age:'年齢',year:'年',period:'段階',fortune:'運勢',sakkaiGreat:'大殺界',sakkaiMedium:'中殺界',sakkaiSmall:'小殺界',good:'✅' },
  },
};

module.exports = i18n;
