<!-- ============================================================
  styling-studio SVG 种子包 · 饰品（J）
  种子数：21 ｜ 所属组：穿搭造型组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-accessory-earring-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-accessory-earring-01.svg ｜ J-01 耳饰与脸型 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-01 | 名称 耳饰线稿（圆环水滴款） | 分类 饰品·耳饰 | 难度 入门 | 标签 日常/正式 -->
  <!-- palette: c-metal: #B8935A | c-gem: #C9748A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（耳环线稿：挂钩 + 圆环 + 水滴坠） -->
  <g id="subject" fill="none" stroke="#B8935A" stroke-width="3" stroke-linecap="round">
    <path d="M100 38 C 92 38 88 44 88 50"/>
    <circle cx="100" cy="96" r="30"/>
    <path d="M100 132 C 90 144 86 154 92 162 C 98 170 108 170 112 160 C 115 152 108 142 100 132 Z" fill="#C9748A" stroke="#B8935A"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="100" cy="50" r="4" fill="#B8935A"/>
    <circle cx="100" cy="132" r="3.4" fill="#FDFBF8" stroke="#B8935A" stroke-width="1.6"/>
  </g>
</svg>
<!-- seed: SS-access-neckline-01.svg ｜ J-02 项链与领型 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-02 | 名称 项链与领型 | 分类 饰品·项链 | 难度 入门 | 标签 V 领 圆领 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（V 领与圆领线条加对应链型） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M28 58 L48 58 L60 90 L72 58 L92 58" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M50 62 L60 86 L70 62" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M108 58 L128 58" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M158 58 L178 58" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M128 58 C 132 84 154 84 158 58" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M130 62 C 134 80 152 80 156 62" stroke="#B8935A" stroke-width="2.6"/>
  </g>
  <!-- layer: 点缀（链型标记点） -->
  <g id="accent">
    <circle cx="60" cy="86" r="3.4" fill="none" stroke="#B8935A" stroke-width="2.2"/>
    <circle cx="143" cy="82" r="3.4" fill="none" stroke="#B8935A" stroke-width="2.2"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="100" cy="146" r="2.6"/>
    <circle cx="100" cy="162" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-hand-01.svg ｜ J-03 手饰搭配 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-03 | 名称 手饰搭配 | 分类 饰品·手饰 | 难度 入门 | 标签 叠戴 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手腕线条） -->
  <g id="subject" fill="none" stroke="#D9BFA8" stroke-width="4" stroke-linecap="round">
    <path d="M70 42 L70 132"/>
    <path d="M110 42 L110 132"/>
    <path d="M70 132 C 80 146 100 146 110 132"/>
  </g>
  <!-- layer: 点缀（叠戴两环 + 标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <ellipse cx="90" cy="88" rx="27" ry="9" stroke-width="3"/>
    <ellipse cx="90" cy="108" rx="27" ry="9" stroke-width="3"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="90" cy="88" r="2.6"/>
    <circle cx="90" cy="108" r="2.6"/>
    <circle cx="90" cy="162" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-headwear-01.svg ｜ J-04 头饰与场合（婚礼） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-04 | 名称 头饰与场合 | 分类 饰品·头饰 | 难度 进阶 | 标签 场合搭配 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（头部弧线与发线） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M62 132 C 62 68 138 68 138 132" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M66 122 C 70 78 130 78 134 122" stroke="#D9BFA8" stroke-width="2.4" opacity="0.65"/>
  </g>
  <!-- layer: 点缀（珠串与小皇冠线） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-width="2.4" stroke-linecap="round">
    <path d="M74 76 C 88 64 112 64 126 76"/>
    <path d="M78 60 L88 48 L100 60 L112 48 L122 60"/>
  </g>
  <g fill="#B8935A" opacity="0.75">
    <circle cx="80" cy="70" r="2.6"/>
    <circle cx="90" cy="65" r="2.6"/>
    <circle cx="100" cy="63" r="2.6"/>
    <circle cx="110" cy="65" r="2.6"/>
    <circle cx="120" cy="70" r="2.6"/>
  </g>
  <g fill="#B8935A" opacity="0.55">
    <circle cx="100" cy="152" r="2.6"/>
    <circle cx="100" cy="168" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-watchmen-01.svg ｜ J-05 男士手表 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-05 | 名称 男士手表（搭配场景） | 分类 饰品·腕表 | 难度 进阶 | 标签 腕表 袖口 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #4A5A6A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手腕线条与袖口） -->
  <g id="subject" fill="none">
    <rect x="62" y="44" width="60" height="34" rx="4" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.6"/>
    <path d="M72 74 L72 164" stroke="#D9BFA8" stroke-width="4" stroke-linecap="round"/>
    <path d="M112 74 L112 164" stroke="#D9BFA8" stroke-width="4" stroke-linecap="round"/>
    <path d="M72 164 C 82 176 102 176 112 164" stroke="#D9BFA8" stroke-width="4" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀（表带 表盘 指针 + 标记点） -->
  <g id="accent" fill="none" stroke-linecap="round">
    <rect x="68" y="98" width="48" height="30" rx="7" fill="#4A5A6A" opacity="0.22"/>
    <rect x="68" y="98" width="48" height="30" rx="7" stroke="#4A5A6A" stroke-width="2.4"/>
    <circle cx="92" cy="113" r="13" fill="#FDFBF8" stroke="#4A5A6A" stroke-width="2.4"/>
    <path d="M92 113 L92 105" stroke="#4A5A6A" stroke-width="2.2"/>
    <path d="M92 113 L99 117" stroke="#4A5A6A" stroke-width="2.2"/>
  </g>
  <g fill="#4A5A6A" opacity="0.6">
    <circle cx="92" cy="184" r="2.6"/>
    <circle cx="140" cy="184" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-accessory-tie-01.svg ｜ J-06 领带与场合 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-06 | 名称 领带结示意 | 分类 饰品·男士 | 难度 入门 | 标签 男性正式 -->
  <!-- palette: c-tie: #8E3B4A | c-shirt: #FDFBF8 | c-line: #C9B8A8（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（衬衫领 + 领带） -->
  <g id="subject">
    <path d="M74 40 L100 68 L126 40 L118 33 L100 56 L82 33 Z" fill="#FDFBF8" stroke="#C9B8A8" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M89 64 L111 64 L107 80 L93 80 Z" fill="#8E3B4A" stroke="#6E2A38" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M93 80 L107 80 L114 156 L100 172 L86 156 Z" fill="#8E3B4A" stroke="#6E2A38" stroke-width="2.2" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（斜纹 + 结部折痕） -->
  <g id="accent">
    <path d="M96 90 L108 112" stroke="#FFFFFF" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
    <path d="M93 120 L104 141" stroke="#FFFFFF" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
    <path d="M93 72 L107 72" stroke="#6E2A38" stroke-width="1.6" opacity="0.7"/>
  </g>
</svg>
<!-- seed: SS-access-cufflink-01.svg ｜ J-07 袖扣 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-07 | 名称 袖扣 | 分类 饰品·袖扣 | 难度 入门 | 标签 正装细节 -->
  <!-- palette: c-a: #B8935A | c-b: #E6ECF1（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（衬衫袖口矩形） -->
  <g id="subject">
    <rect x="54" y="64" width="92" height="72" rx="6" fill="#E6ECF1" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M100 64 L100 136" fill="none" stroke="#B8935A" stroke-width="2" opacity="0.45"/>
  </g>
  <!-- layer: 点缀（袖扣圆点与连杆） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <circle cx="76" cy="90" r="10" stroke-width="3"/>
    <circle cx="76" cy="114" r="10" stroke-width="3"/>
    <path d="M76 100 L76 104" stroke-width="2.6"/>
    <circle cx="76" cy="90" r="3.4" fill="#B8935A"/>
  </g>
  <g fill="#B8935A" opacity="0.55">
    <circle cx="140" cy="82" r="2.6"/>
    <circle cx="140" cy="118" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-belt-01.svg ｜ J-08 皮带搭配 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-08 | 名称 皮带搭配 | 分类 饰品·皮带 | 难度 入门 | 标签 腰线 金属扣 -->
  <!-- palette: c-a: #8A6B4E | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（腰部线条与皮带） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M60 74 C 60 60 140 60 140 74" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M60 130 C 60 146 140 146 140 130" stroke="#D9BFA8" stroke-width="4"/>
    <rect x="56" y="92" width="88" height="24" rx="4" fill="#8A6B4E" stroke="#8A6B4E" stroke-width="2.4"/>
  </g>
  <!-- layer: 点缀（金属扣与标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <rect x="86" y="88" width="28" height="32" rx="4" stroke-width="3"/>
    <path d="M100 88 L100 120" stroke-width="2.4"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="100" cy="166" r="2.6"/>
    <circle cx="100" cy="52" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-earlite-01.svg ｜ J-09 耳饰 · 日常轻量 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-09 | 名称 耳饰轻量 | 分类 饰品·耳饰 | 难度 入门 | 标签 日常轻量 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（耳朵弧线） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M106 56 C 84 58 80 90 94 102 C 104 110 102 120 94 126" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M100 76 C 90 78 90 92 98 98" stroke="#D9BFA8" stroke-width="2.6" opacity="0.75"/>
  </g>
  <!-- layer: 点缀（细链小坠与标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <path d="M94 126 C 94 140 90 150 86 158" stroke-width="2.2"/>
    <circle cx="86" cy="164" r="5" stroke-width="2.2"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="86" cy="164" r="1.8"/>
    <circle cx="140" cy="120" r="2.6"/>
    <circle cx="140" cy="136" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-earbold-01.svg ｜ J-10 耳饰 · 正式存在感 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-10 | 名称 耳饰正式 | 分类 饰品·耳饰 | 难度 进阶 | 标签 正式 大圆环 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（耳朵弧线） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M110 52 C 86 54 82 88 96 102 C 106 112 104 122 96 128" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M104 72 C 94 74 94 90 102 96" stroke="#D9BFA8" stroke-width="2.6" opacity="0.75"/>
  </g>
  <!-- layer: 点缀（大圆环与珍珠 + 标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <circle cx="96" cy="152" r="26" stroke-width="3"/>
    <circle cx="96" cy="178" r="6" fill="#EFE6DA" stroke-width="2.2"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="150" cy="112" r="2.6"/>
    <circle cx="150" cy="128" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-accessory-necklace-01.svg ｜ J-11 项链 · 长短层次 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-11 | 名称 项链长度示意（短 / 中 / 长） | 分类 饰品·项链 | 难度 入门 | 标签 领型搭配 -->
  <!-- palette: c-metal: #B8935A | c-skin: #D9BFA8（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（颈肩线条 + 三条项链） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M80 52 C 80 42 120 42 120 52" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M62 92 C 74 76 86 68 100 68" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M138 92 C 126 76 114 68 100 68" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M86 74 C 92 84 108 84 114 74" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M83 71 C 90 96 110 96 117 71" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M80 68 C 88 118 112 118 120 68" stroke="#B8935A" stroke-width="2.6"/>
  </g>
  <!-- layer: 点缀（长链吊坠 + 长度标注点） -->
  <g id="accent">
    <circle cx="100" cy="112" r="5" fill="none" stroke="#B8935A" stroke-width="2.2"/>
    <circle cx="100" cy="78" r="2.2" fill="#B8935A" opacity="0.6"/>
    <circle cx="100" cy="96" r="2.2" fill="#B8935A" opacity="0.6"/>
    <circle cx="100" cy="118" r="2.2" fill="#B8935A" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-access-ringshape-01.svg ｜ J-12 戒指 · 手型搭配 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-12 | 名称 戒指与手型 | 分类 饰品·戒指 | 难度 入门 | 标签 圈位 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手指线条） -->
  <g id="subject" fill="none" stroke="#D9BFA8" stroke-width="3.2">
    <rect x="58" y="58" width="22" height="104" rx="11"/>
    <rect x="88" y="48" width="22" height="120" rx="11"/>
    <rect x="118" y="58" width="22" height="104" rx="11"/>
  </g>
  <!-- layer: 点缀（戒指圈位与标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <rect x="86" y="92" width="26" height="16" rx="8" stroke-width="3"/>
    <circle cx="99" cy="86" r="5" stroke-width="2.4"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="99" cy="86" r="1.8"/>
    <circle cx="158" cy="120" r="2.6"/>
    <circle cx="158" cy="136" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-bracelet-01.svg ｜ J-13 手链 / 腕饰 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-13 | 名称 手链腕饰 | 分类 饰品·手链 | 难度 入门 | 标签 珠串 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手腕线条） -->
  <g id="subject" fill="none" stroke="#D9BFA8" stroke-width="4" stroke-linecap="round">
    <path d="M70 40 L70 150"/>
    <path d="M110 40 L110 150"/>
    <path d="M70 150 C 80 164 100 164 110 150"/>
  </g>
  <!-- layer: 点缀（珠串手链与标记点） -->
  <g id="accent">
    <ellipse cx="90" cy="110" rx="26" ry="11" fill="none" stroke="#B8935A" stroke-width="2.2" opacity="0.55"/>
    <g fill="#B8935A">
      <circle cx="64" cy="110" r="4"/>
      <circle cx="72" cy="119" r="4"/>
      <circle cx="84" cy="121" r="4"/>
      <circle cx="96" cy="121" r="4"/>
      <circle cx="108" cy="119" r="4"/>
      <circle cx="116" cy="110" r="4"/>
      <circle cx="108" cy="101" r="4"/>
      <circle cx="96" cy="99" r="4"/>
      <circle cx="84" cy="99" r="4"/>
      <circle cx="72" cy="101" r="4"/>
    </g>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="90" cy="62" r="2.6"/>
    <circle cx="90" cy="176" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-hairpin-01.svg ｜ J-14 发饰 · 日常与婚礼 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-14 | 名称 发饰 | 分类 饰品·发饰 | 难度 入门 | 标签 蝴蝶结 发夹 -->
  <!-- palette: c-a: #D9BFA8 | c-b: #7C5C8A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（发丝线条） -->
  <g id="subject" fill="none" stroke="#D9BFA8" stroke-width="3.4" stroke-linecap="round">
    <path d="M36 84 C 66 48 134 48 164 84"/>
    <path d="M42 104 C 70 72 130 72 158 104"/>
    <path d="M50 124 C 74 98 126 98 150 124"/>
  </g>
  <!-- layer: 点缀（蝴蝶结发夹与标记点） -->
  <g id="accent">
    <path d="M138 58 L114 44 L114 72 Z" fill="#7C5C8A" opacity="0.85"/>
    <path d="M138 58 L162 44 L162 72 Z" fill="#7C5C8A" opacity="0.85"/>
    <circle cx="138" cy="58" r="6" fill="#7C5C8A"/>
  </g>
  <g fill="#7C5C8A" opacity="0.55">
    <circle cx="138" cy="150" r="2.6"/>
    <circle cx="138" cy="166" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-accessory-bags-01.svg ｜ J-15 包袋选型（按场合） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-15 | 名称 包袋选型（三种场合款） | 分类 饰品·包袋 | 难度 入门 | 标签 全场合 -->
  <!-- palette: c-tote: #B07040 | c-clutch: #8E3B4A | c-back: #4A5568（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（托特 / 手拿 / 双肩） -->
  <g id="subject" stroke-linejoin="round" stroke-width="2.4">
    <path d="M36 88 L74 88 L80 150 L30 150 Z" fill="#B07040" stroke="#8E5A32"/>
    <path d="M44 88 C 44 70 66 70 66 88" fill="none" stroke="#8E5A32"/>
    <path d="M98 116 L138 116 C 141 116 142 118 142 121 L142 139 C 142 142 141 144 138 144 L98 144 C 95 144 94 142 94 139 L94 121 C 94 118 95 116 98 116 Z" fill="#8E3B4A" stroke="#6E2A38"/>
    <path d="M112 116 L112 144" stroke="#6E2A38" stroke-width="2" opacity="0.6"/>
    <path d="M154 100 H188 V150 H154 Z" fill="#4A5568" stroke="#3A4250"/>
    <path d="M154 100 C 154 86 188 86 188 100" fill="none" stroke="#3A4250"/>
    <path d="M162 104 C 158 118 158 134 162 146 M180 104 C 184 118 184 134 180 146" fill="none" stroke="#3A4250" stroke-width="1.8" opacity="0.7"/>
  </g>
  <!-- layer: 点缀（场合点） -->
  <g id="accent">
    <circle cx="55" cy="164" r="2.8" fill="#B07040"/>
    <circle cx="118" cy="164" r="2.8" fill="#8E3B4A"/>
    <circle cx="171" cy="164" r="2.8" fill="#4A5568"/>
    <path d="M30 172 L180 172" stroke="#A85F4E" stroke-width="1.6" opacity="0.35" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-accessory-scarf-01.svg ｜ J-16 丝巾用法 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-16 | 名称 方形丝巾（对角折与结） | 分类 饰品·丝巾 | 难度 入门 | 标签 职场/度假 -->
  <!-- palette: c-silk: #C9748A | c-fold: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（方巾菱形 + 折痕） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M100 34 L166 100 L100 166 L34 100 Z" stroke="#C9748A" stroke-width="3.2" stroke-linejoin="round"/>
    <path d="M100 34 L100 166" stroke="#C9748A" stroke-width="1.8" opacity="0.5" stroke-dasharray="4 5"/>
    <path d="M34 100 L166 100" stroke="#C9748A" stroke-width="1.8" opacity="0.5" stroke-dasharray="4 5"/>
  </g>
  <!-- layer: 点缀（系结示意 + 垂角） -->
  <g id="accent">
    <circle cx="100" cy="34" r="7" fill="none" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M92 30 C 88 22 94 16 100 20 C 106 16 112 22 108 30" fill="none" stroke="#B8935A" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M100 41 C 96 52 92 60 90 68 M100 41 C 104 52 108 60 110 68" fill="none" stroke="#C9748A" stroke-width="2.2" stroke-linecap="round" opacity="0.75"/>
  </g>
</svg>
<!-- seed: SS-access-brooch-01.svg ｜ J-17 男士 · 胸针 / 口袋巾 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-17 | 名称 胸针口袋巾 | 分类 饰品·胸饰 | 难度 进阶 | 标签 胸针 口袋巾 -->
  <!-- palette: c-a: #4A5A6A | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（西装胸前线条） -->
  <g id="subject" fill="none" stroke="#4A5A6A" stroke-width="2.6" stroke-linecap="round">
    <path d="M56 50 L84 92 L62 134"/>
    <path d="M104 50 L104 158"/>
    <path d="M112 116 L160 116"/>
  </g>
  <!-- layer: 点缀（胸针与口袋巾三角 + 标记点） -->
  <g id="accent" fill="none" stroke="#B8935A" stroke-linecap="round">
    <path d="M120 115 L140 88 L160 115 Z" stroke-width="2.4"/>
    <circle cx="74" cy="104" r="7" stroke-width="2.6"/>
    <circle cx="74" cy="92" r="3" stroke-width="2"/>
    <circle cx="74" cy="116" r="3" stroke-width="2"/>
    <circle cx="62" cy="104" r="3" stroke-width="2"/>
    <circle cx="86" cy="104" r="3" stroke-width="2"/>
  </g>
  <g fill="#B8935A" opacity="0.55">
    <circle cx="168" cy="150" r="2.6"/>
    <circle cx="168" cy="166" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-access-beltwatch-01.svg ｜ J-18 男士 · 皮带与腕表协调 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-18 | 名称 皮带腕表协调 | 分类 饰品·配饰 | 难度 进阶 | 标签 同色系 -->
  <!-- palette: c-a: #8A6B4E | c-b: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（腰部皮带与手腕线条） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M22 84 C 40 72 76 72 94 84" stroke="#D9BFA8" stroke-width="3.4"/>
    <rect x="20" y="92" width="76" height="20" rx="4" fill="#8A6B4E" stroke="#8A6B4E" stroke-width="2.2"/>
    <path d="M120 70 L120 158" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M156 70 L156 158" stroke="#D9BFA8" stroke-width="4"/>
    <path d="M120 158 C 130 170 146 170 156 158" stroke="#D9BFA8" stroke-width="4"/>
  </g>
  <!-- layer: 点缀（表带圆盘与金属扣 同色系连线） -->
  <g id="accent" fill="none" stroke-linecap="round">
    <rect x="126" y="100" width="44" height="22" rx="6" fill="#8A6B4E" opacity="0.28"/>
    <rect x="126" y="100" width="44" height="22" rx="6" stroke="#8A6B4E" stroke-width="2.4"/>
    <circle cx="148" cy="111" r="11" fill="#FDFBF8" stroke="#8A6B4E" stroke-width="2.4"/>
    <rect x="44" y="88" width="24" height="28" rx="4" stroke="#B8935A" stroke-width="2.6"/>
    <path d="M92 108 L120 108" stroke="#B8935A" stroke-width="2" stroke-dasharray="4 4"/>
  </g>
  <g fill="#B8935A" opacity="0.6">
    <circle cx="56" cy="132" r="3"/>
    <circle cx="148" cy="132" r="3"/>
  </g>
</svg>
<!-- seed: SS-accessory-watch-01.svg ｜ J-19 男士腕表（经典圆盘） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-19 | 名称 男士腕表（经典圆盘） | 分类 饰品·男士 | 难度 入门 | 标签 男性正式/日常 -->
  <!-- palette: c-metal: #B8935A | c-band: #6E5748 | c-face: #FDFBF6（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（表带 + 表盘） -->
  <g id="subject">
    <path d="M84 76 C 76 48 124 48 116 76 L116 82 L84 82 Z" fill="#6E5748"/>
    <path d="M84 124 C 76 152 124 152 116 124 L116 118 L84 118 Z" fill="#6E5748"/>
    <circle cx="100" cy="100" r="30" fill="#B8935A"/>
    <circle cx="100" cy="100" r="24" fill="#FDFBF6" stroke="#B8935A" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（刻度与指针 + 表冠） -->
  <g id="accent">
    <path d="M100 80 L100 86 M120 100 L114 100 M100 120 L100 114 M80 100 L86 100" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M100 100 L100 86 M100 100 L111 106" stroke="#2B2B2B" stroke-width="2.6" stroke-linecap="round"/>
    <circle cx="100" cy="100" r="2.4" fill="#B8935A"/>
    <rect x="130" y="96" width="7" height="8" rx="2" fill="#B8935A"/>
  </g>
</svg>
<!-- seed: SS-accessory-ring-01.svg ｜ J-20 戒指（宝石款） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-20 | 名称 戒指（宝石款） | 分类 饰品·手饰 | 难度 入门 | 标签 日常/婚礼 -->
  <!-- palette: c-metal: #B8935A | c-gem: #C9748A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（戒圈 + 宝石） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <circle cx="100" cy="118" r="30" stroke="#B8935A" stroke-width="5"/>
    <circle cx="100" cy="118" r="21" stroke="#B8935A" stroke-width="2" opacity="0.6"/>
    <path d="M100 58 L113 74 L100 90 L87 74 Z" fill="#C9748A" stroke="#A85252" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M87 74 L113 74" stroke="#A85252" stroke-width="1.6" opacity="0.7"/>
    <path d="M90 70 L96 64" stroke="#FFFFFF" stroke-width="2.4" opacity="0.85"/>
  </g>
  <!-- layer: 点缀（戒托小弧 + 光点） -->
  <g id="accent">
    <path d="M92 88 C 96 92 104 92 108 88" fill="none" stroke="#B8935A" stroke-width="2.6" stroke-linecap="round"/>
    <circle cx="140" cy="88" r="2.4" fill="#B8935A" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-accessory-bag-01.svg ｜ J-21 手提包（选型简图） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 J-21 | 名称 手提包（选型简图） | 分类 饰品·包袋 | 难度 入门 | 标签 场合搭配 -->
  <!-- palette: c-bag: #8E6E5E | c-line: #6E5748 | c-buckle: #B8935A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（包身 + 提手） -->
  <g id="subject">
    <path d="M78 106 C 78 74 122 74 122 106" fill="none" stroke="#6E5748" stroke-width="5" stroke-linecap="round"/>
    <path d="M62 104 L138 104 L146 178 L54 178 Z" fill="#8E6E5E" stroke="#6E5748" stroke-width="3" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（扣件 + 缝线） -->
  <g id="accent">
    <rect x="90" y="98" width="20" height="14" rx="4" fill="#B8935A"/>
    <circle cx="100" cy="105" r="2.6" fill="#FDFBF8"/>
    <path d="M62 118 L138 118" stroke="#6E5748" stroke-width="1.6" opacity="0.5" stroke-dasharray="4 4"/>
  </g>
</svg>
