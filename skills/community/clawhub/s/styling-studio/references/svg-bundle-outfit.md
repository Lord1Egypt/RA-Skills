<!-- ============================================================
  styling-studio SVG 种子包 · 服装（O）
  种子数：21 ｜ 所属组：穿搭造型组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-outfit-dress-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-outfit-dress-01.svg ｜ O-01 场合穿搭法（女） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-01 | 名称 连衣裙剪影（A 字无袖款） | 分类 服装·女装 | 难度 入门 | 标签 场合穿搭 -->
  <!-- palette: c-dress: #C87F6E | c-line: #A85F4E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（裙装剪影） -->
  <g id="subject">
    <path d="M84 44 L100 38 L116 44 L128 54 L114 112 L142 206 C 112 218 88 218 58 206 L86 112 L72 54 Z"
          fill="#C87F6E" stroke="#A85F4E" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="M86 112 C 96 118 104 118 114 112" fill="none" stroke="#A85F4E" stroke-width="2"/>
    <path d="M74 54 L86 112" fill="none" stroke="#A85F4E" stroke-width="1.4" opacity="0.6"/>
    <path d="M126 54 L114 112" fill="none" stroke="#A85F4E" stroke-width="1.4" opacity="0.6"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M62 196 C 88 206 112 206 138 196" fill="none" stroke="#A85F4E" stroke-width="1.4" opacity="0.5"/>
  </g>
</svg>
<!-- seed: SS-outfit-silhouette-01.svg ｜ O-02 廓形修饰（女） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-02 | 名称 三种廓形对比（A / H / X） | 分类 服装·廓形 | 难度 入门 | 标签 体型修饰 -->
  <!-- palette: c-line: #A85F4E | c-fill: #F3E0DA（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三种廓形剪影） -->
  <g id="subject">
    <path d="M40 62 L60 62 L74 160 L26 160 Z" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M86 62 L114 62 L114 160 L86 160 Z" fill="none" stroke="#A85F4E" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M144 62 L162 62 L156 108 L168 160 L138 160 L150 108 Z" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（基线 + 标签点） -->
  <g id="accent">
    <path d="M24 168 L176 168" stroke="#A85F4E" stroke-width="2" opacity="0.45" stroke-linecap="round"/>
    <circle cx="50" cy="176" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="100" cy="176" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="153" cy="176" r="2.6" fill="#A85F4E" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-colors-01.svg ｜ O-03 色彩搭配法（诊断联动） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-03 | 名称 色彩组合卡（暖调组 / 冷调组） | 分类 服装·色彩 | 难度 入门 | 标签 诊断联动 -->
  <!-- palette: 暖调组 #C8A184/#B07040/#F1E6D8；冷调组 #9BB3CC/#A79ABF/#EDEFF2 -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFDFB" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（两组配色三圆：主 / 辅 / 点缀） -->
  <g id="subject">
    <circle cx="56" cy="70" r="22" fill="#C8A184"/>
    <circle cx="100" cy="70" r="22" fill="#B07040"/>
    <circle cx="144" cy="70" r="22" fill="#F1E6D8" stroke="#E6D6C6" stroke-width="1.5"/>
    <circle cx="56" cy="142" r="22" fill="#9BB3CC"/>
    <circle cx="100" cy="142" r="22" fill="#A79ABF"/>
    <circle cx="144" cy="142" r="22" fill="#EDEFF2" stroke="#D8DDE4" stroke-width="1.5"/>
  </g>
  <!-- layer: 点缀（分组标注线） -->
  <g id="accent" stroke-linecap="round">
    <path d="M36 100 L164 100" stroke="#EADFD3" stroke-width="1.6" stroke-dasharray="4 5"/>
    <path d="M36 34 L164 34" stroke="#C8A184" stroke-width="2.4" opacity="0.55"/>
    <path d="M36 178 L164 178" stroke="#9BB3CC" stroke-width="2.4" opacity="0.55"/>
  </g>
</svg>
<!-- seed: SS-outfit-mix-01.svg ｜ O-04 胶囊衣橱组合 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-04 | 名称 胶囊衣橱组合 | 分类 服装·搭配 | 难度 入门 | 标签 胶囊衣橱 -->
  <!-- palette: c-a: #A85F4E | c-b: #F3E0DA（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三套上装加下装色块组合横向并排） -->
  <g id="subject">
    <rect x="30" y="54" width="40" height="52" rx="4" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.4"/>
    <path d="M34 110 L66 110 L76 198 L24 198 Z" fill="#A85F4E" stroke="#A85F4E" stroke-width="2.4" stroke-linejoin="round" opacity="0.82"/>
    <rect x="80" y="54" width="40" height="52" rx="4" fill="#A85F4E" stroke="#A85F4E" stroke-width="2.4" opacity="0.82"/>
    <rect x="82" y="110" width="36" height="88" rx="4" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.4"/>
    <rect x="130" y="54" width="40" height="52" rx="4" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.4"/>
    <path d="M134 110 L166 110 L158 198 L142 198 Z" fill="#A85F4E" stroke="#A85F4E" stroke-width="2.4" stroke-linejoin="round" opacity="0.82"/>
  </g>
  <!-- layer: 点缀（基准线 + 组标记点） -->
  <g id="accent">
    <path d="M24 212 L176 212" stroke="#A85F4E" stroke-width="2" opacity="0.4" stroke-linecap="round"/>
    <circle cx="50" cy="220" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="100" cy="220" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="150" cy="220" r="2.6" fill="#A85F4E" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-men-01.svg ｜ O-05 男装场合法 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-05 | 名称 男装场合法 | 分类 服装·男装 | 难度 入门 | 标签 职场搭配 -->
  <!-- palette: c-a: #4A5A6A | c-b: #E4E8EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（左西装右休闲两件剪影对比） -->
  <g id="subject">
    <path d="M36 56 L72 56 L78 120 L30 120 Z" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="M54 58 L46 96" fill="none" stroke="#4A5A6A" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M54 58 L62 96" fill="none" stroke="#4A5A6A" stroke-width="2.2" stroke-linecap="round"/>
    <rect x="34" y="120" width="17" height="82" rx="2" fill="#4A5A6A" opacity="0.85"/>
    <rect x="55" y="120" width="17" height="82" rx="2" fill="#4A5A6A" opacity="0.85"/>
    <rect x="112" y="66" width="36" height="54" rx="4" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.4"/>
    <rect x="102" y="72" width="12" height="26" rx="3" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.2"/>
    <rect x="146" y="72" width="12" height="26" rx="3" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.2"/>
    <rect x="114" y="120" width="16" height="82" rx="2" fill="#4A5A6A" opacity="0.85"/>
    <rect x="132" y="120" width="16" height="82" rx="2" fill="#4A5A6A" opacity="0.85"/>
  </g>
  <!-- layer: 点缀（分区线 + 标记点） -->
  <g id="accent">
    <path d="M100 44 L100 214" fill="none" stroke="#4A5A6A" stroke-width="1.6" opacity="0.3" stroke-dasharray="5 5" stroke-linecap="round"/>
    <circle cx="54" cy="220" r="2.6" fill="#4A5A6A" opacity="0.6"/>
    <circle cx="130" cy="220" r="2.6" fill="#4A5A6A" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-menshape-01.svg ｜ O-06 男装廓形 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-06 | 名称 男装廓形 | 分类 服装·廓形 | 难度 进阶 | 标签 廓形修饰 -->
  <!-- palette: c-a: #4A5A6A | c-b: #E4E8EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（左 H 型轮廓 右 X 型轮廓） -->
  <g id="subject">
    <path d="M40 58 L76 58 L76 196 L40 196 Z" fill="none" stroke="#4A5A6A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M116 58 L160 58 L146 120 L160 196 L116 196 L130 120 Z" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（腰线标注 + 基准线） -->
  <g id="accent" fill="none" stroke="#4A5A6A" stroke-width="2" stroke-linecap="round">
    <path d="M36 126 L80 126" opacity="0.4" stroke-dasharray="6 5"/>
    <path d="M112 120 L164 120" opacity="0.4" stroke-dasharray="6 5"/>
  </g>
  <g fill="#4A5A6A" opacity="0.6">
    <circle cx="58" cy="212" r="2.6"/>
    <circle cx="138" cy="212" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-pear-01.svg ｜ O-07 梨形身材穿搭 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-07 | 名称 梨形穿搭 | 分类 服装·体型修饰 | 难度 入门 | 标签 梨形 A 字 -->
  <!-- palette: c-a: #7C5C8A | c-b: #F1E8F0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（上浅色块加下深 A 字裙剪影） -->
  <g id="subject">
    <path d="M76 56 L124 56 L124 106 L76 106 Z" fill="#F1E8F0" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M76 106 L124 106 L158 200 L42 200 Z" fill="#7C5C8A" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round" opacity="0.85"/>
  </g>
  <!-- layer: 点缀（腰线标注 + 色阶标记点） -->
  <g id="accent" fill="none" stroke="#7C5C8A" stroke-width="2" stroke-linecap="round">
    <path d="M70 106 L130 106" opacity="0.55" stroke-dasharray="6 5"/>
  </g>
  <g fill="#7C5C8A" opacity="0.6">
    <circle cx="100" cy="82" r="2.6"/>
    <circle cx="100" cy="152" r="2.6"/>
    <circle cx="100" cy="212" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-apple-01.svg ｜ O-08 苹果形穿搭 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-08 | 名称 苹果形穿搭 | 分类 服装·体型修饰 | 难度 入门 | 标签 苹果形 V 领 -->
  <!-- palette: c-a: #8A6B4E | c-b: #F2E7DA（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（V 领上装加高腰顺色下装） -->
  <g id="subject">
    <path d="M62 56 L138 56 L138 118 L62 118 Z" fill="#F2E7DA" stroke="#8A6B4E" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M86 56 L100 86 L114 56" fill="none" stroke="#8A6B4E" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M62 118 L138 118 L130 202 L70 202 Z" fill="#8A6B4E" stroke="#8A6B4E" stroke-width="2.6" stroke-linejoin="round" opacity="0.82"/>
  </g>
  <!-- layer: 点缀（高腰线标注 + 标记点） -->
  <g id="accent" fill="none" stroke="#8A6B4E" stroke-width="2" stroke-linecap="round">
    <path d="M56 118 L144 118" opacity="0.55" stroke-dasharray="6 5"/>
  </g>
  <g fill="#8A6B4E" opacity="0.6">
    <circle cx="100" cy="48" r="2.6"/>
    <circle cx="100" cy="118" r="2.6"/>
    <circle cx="100" cy="210" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-hourglass-01.svg ｜ O-09 沙漏形穿搭 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-09 | 名称 沙漏形穿搭 | 分类 服装·体型修饰 | 难度 进阶 | 标签 沙漏形 收腰 -->
  <!-- palette: c-a: #7C5C8A | c-b: #F1E8F0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（收腰连衣裙剪影） -->
  <g id="subject">
    <path d="M62 52 L138 52 L116 122 L146 202 L54 202 L84 122 Z" fill="#F1E8F0" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（腰线标注 + 标记点） -->
  <g id="accent" fill="none" stroke="#7C5C8A" stroke-width="2.4" stroke-linecap="round">
    <path d="M76 122 L124 122" opacity="0.7" stroke-dasharray="5 4"/>
    <path d="M70 122 L62 122" opacity="0.7"/>
    <path d="M130 122 L138 122" opacity="0.7"/>
  </g>
  <g fill="#7C5C8A" opacity="0.65">
    <circle cx="100" cy="122" r="3"/>
    <circle cx="100" cy="44" r="2.6"/>
    <circle cx="100" cy="214" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-petite-01.svg ｜ O-10 小个子比例技巧 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-10 | 名称 小个子比例 | 分类 服装·体型修饰 | 难度 入门 | 标签 小个子 高腰 -->
  <!-- palette: c-a: #6B7A8A | c-b: #E6ECF1（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（顺色上下装形成纵向延伸） -->
  <g id="subject">
    <path d="M72 58 L128 58 L128 116 L72 116 Z" fill="#E6ECF1" stroke="#6B7A8A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M72 116 L128 116 L134 204 L66 204 Z" fill="#E6ECF1" stroke="#6B7A8A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（高腰线 + 纵向延伸箭头） -->
  <g id="accent" fill="none" stroke="#6B7A8A" stroke-width="2.2" stroke-linecap="round">
    <path d="M66 116 L134 116" opacity="0.55" stroke-dasharray="6 5"/>
    <path d="M100 70 L100 194" opacity="0.7" stroke-dasharray="4 5"/>
    <path d="M94 76 L100 68 L106 76" opacity="0.7"/>
    <path d="M94 188 L100 196 L106 188" opacity="0.7"/>
  </g>
  <g fill="#6B7A8A" opacity="0.6">
    <circle cx="100" cy="50" r="2.6"/>
    <circle cx="100" cy="116" r="3"/>
    <circle cx="100" cy="212" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-tall-01.svg ｜ O-11 高个穿搭 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-11 | 名称 高个穿搭 | 分类 服装·体型修饰 | 难度 入门 | 标签 高个 长线条 -->
  <!-- palette: c-a: #8A6B4E | c-b: #F2E7DA（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（长线条大衣剪影） -->
  <g id="subject">
    <path d="M54 50 L146 50 L152 206 L48 206 Z" fill="#F2E7DA" stroke="#8A6B4E" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M84 52 L100 88 L116 52" fill="none" stroke="#8A6B4E" stroke-width="2.6" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀（门襟长线 + 标记点） -->
  <g id="accent" fill="none" stroke="#8A6B4E" stroke-width="2" stroke-linecap="round">
    <path d="M100 88 L100 202" opacity="0.5" stroke-dasharray="6 5"/>
  </g>
  <g fill="#8A6B4E" opacity="0.6">
    <circle cx="100" cy="42" r="2.6"/>
    <circle cx="100" cy="120" r="2.6"/>
    <circle cx="100" cy="214" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-blazer-01.svg ｜ O-12 西装场合法（女） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-12 | 名称 西装场合法（女） | 分类 服装·正式 | 难度 进阶 | 标签 职场西装 -->
  <!-- palette: c-a: #4A5A6A | c-b: #E4E8EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（女西装外套剪影） -->
  <g id="subject">
    <path d="M42 56 L158 56 L152 176 L48 176 Z" fill="#E4E8EC" stroke="#4A5A6A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M78 58 L100 104 L122 58" fill="none" stroke="#4A5A6A" stroke-width="2.6" stroke-linecap="round"/>
    <circle cx="100" cy="128" r="3.4" fill="none" stroke="#4A5A6A" stroke-width="2.2"/>
  </g>
  <!-- layer: 点缀（口袋巾线 + 腰线标注） -->
  <g id="accent" fill="none" stroke="#4A5A6A" stroke-width="2.2" stroke-linecap="round">
    <path d="M60 112 L60 128 L78 128" opacity="0.8"/>
    <path d="M60 112 L74 112" opacity="0.8"/>
    <path d="M64 116 L64 126 L74 126 Z" opacity="0.8"/>
    <path d="M56 152 L144 152" opacity="0.4" stroke-dasharray="6 5"/>
  </g>
  <g fill="#4A5A6A" opacity="0.6">
    <circle cx="100" cy="194" r="2.6"/>
    <circle cx="54" cy="194" r="2.6"/>
    <circle cx="146" cy="194" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-dressy-01.svg ｜ O-13 连衣裙选型 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-13 | 名称 连衣裙选型 | 分类 服装·裙装 | 难度 入门 | 标签 裙型对比 -->
  <!-- palette: c-a: #7C5C8A | c-b: #F1E8F0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（A 字 直筒 鱼尾三款裙型小剪影） -->
  <g id="subject">
    <path d="M34 62 L66 62 L82 190 L18 190 Z" fill="#F1E8F0" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M86 62 L114 62 L114 190 L86 190 Z" fill="none" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M136 62 L164 62 L162 132 L178 190 L122 190 L138 132 Z" fill="#F1E8F0" stroke="#7C5C8A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（基准线 + 标记点） -->
  <g id="accent">
    <path d="M18 202 L182 202" stroke="#7C5C8A" stroke-width="2" opacity="0.4" stroke-linecap="round"/>
    <circle cx="50" cy="212" r="2.6" fill="#7C5C8A" opacity="0.6"/>
    <circle cx="100" cy="212" r="2.6" fill="#7C5C8A" opacity="0.6"/>
    <circle cx="150" cy="212" r="2.6" fill="#7C5C8A" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-layer-01.svg ｜ O-14 冬季叠穿 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-14 | 名称 叠穿层次示意（三层领口） | 分类 服装·叠穿 | 难度 进阶 | 标签 冬季/层次感 -->
  <!-- palette: c-layer1: #B07040 | c-layer2: #C8A184 | c-layer3: #8E6E5E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三层领口由内到外） -->
  <g id="subject" fill="none" stroke-linecap="round">
    <path d="M86 66 L100 84 L114 66" stroke="#B07040" stroke-width="3"/>
    <path d="M74 62 C 84 50 116 50 126 62" stroke="#C8A184" stroke-width="3.6"/>
    <path d="M58 54 C 70 40 130 40 142 54" stroke="#8E6E5E" stroke-width="4.2"/>
    <path d="M62 58 L88 78 M138 58 L112 78" stroke="#8E6E5E" stroke-width="3.4"/>
  </g>
  <!-- layer: 点缀（衣身延伸线 + 层次标注） -->
  <g id="accent" fill="none" stroke-linecap="round">
    <path d="M86 66 C 82 100 78 132 74 158" stroke="#B07040" stroke-width="2.4" opacity="0.7"/>
    <path d="M114 66 C 118 100 122 132 126 158" stroke="#B07040" stroke-width="2.4" opacity="0.7"/>
    <path d="M80 92 C 76 120 72 142 68 160" stroke="#C8A184" stroke-width="2.4" opacity="0.7"/>
    <path d="M120 92 C 124 120 128 142 132 160" stroke="#C8A184" stroke-width="2.4" opacity="0.7"/>
    <path d="M74 152 L134 152" stroke="#8E6E5E" stroke-width="2" opacity="0.4"/>
  </g>
</svg>
<!-- seed: SS-outfit-summer-01.svg ｜ O-15 夏季清凉搭配 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-15 | 名称 夏季清凉搭配 | 分类 服装·搭配 | 难度 入门 | 标签 夏季 短袖 -->
  <!-- palette: c-a: #6B8A7A | c-b: #E7F1EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（短袖上装加半裙组合剪影） -->
  <g id="subject">
    <rect x="66" y="58" width="68" height="56" rx="4" fill="#E7F1EC" stroke="#6B8A7A" stroke-width="2.6"/>
    <rect x="50" y="66" width="16" height="34" rx="4" fill="#E7F1EC" stroke="#6B8A7A" stroke-width="2.2"/>
    <rect x="134" y="66" width="16" height="34" rx="4" fill="#E7F1EC" stroke="#6B8A7A" stroke-width="2.2"/>
    <path d="M70 114 L130 114 L148 194 L52 194 Z" fill="#6B8A7A" stroke="#6B8A7A" stroke-width="2.6" stroke-linejoin="round" opacity="0.82"/>
  </g>
  <!-- layer: 点缀（腰线 + 标记点） -->
  <g id="accent" fill="none" stroke="#6B8A7A" stroke-width="2" stroke-linecap="round">
    <path d="M64 114 L136 114" opacity="0.55" stroke-dasharray="6 5"/>
  </g>
  <g fill="#6B8A7A" opacity="0.6">
    <circle cx="100" cy="50" r="2.6"/>
    <circle cx="100" cy="114" r="2.6"/>
    <circle cx="100" cy="204" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-capsule-01.svg ｜ O-16 通勤胶囊衣橱（20 件） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-16 | 名称 胶囊衣橱构成卡（四类单品） | 分类 服装·衣橱 | 难度 入门 | 标签 通勤/极简 -->
  <!-- palette: c-line: #A85F4E | c-fill: #F3E0DA（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（2×2 分类格） -->
  <g id="subject" fill="none" stroke="#A85F4E" stroke-width="2" opacity="0.85">
    <path d="M40 58 L160 58 M40 118 L160 118 M40 178 L160 178"/>
    <path d="M40 58 L40 178 M100 58 L100 178 M160 58 L160 178"/>
  </g>
  <!-- layer: 点缀（四类单品简笔） -->
  <g id="accent" fill="#F3E0DA" stroke="#A85F4E" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">
    <path d="M52 74 L62 68 L78 68 L88 74 L83 82 L83 106 L57 106 L57 82 Z"/>
    <path d="M112 68 L128 68 L132 106 L124 106 L120 88 L116 106 L108 106 Z"/>
    <path d="M52 128 L60 124 L70 124 L80 128 L76 136 L76 172 L56 172 L56 136 Z"/>
    <path d="M62 128 L62 172" fill="none"/>
    <path d="M108 136 L152 136 L156 172 L104 172 Z" fill="#F3E0DA"/>
    <path d="M116 136 C 116 124 144 124 144 136" fill="none"/>
  </g>
</svg>
<!-- seed: SS-outfit-wedding-01.svg ｜ O-17 婚礼着装（分角色） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-17 | 名称 婚礼着装（分角色·三剪影） | 分类 服装·场合法 | 难度 入门 | 标签 婚礼 -->
  <!-- palette: c-bride: #F2EAE0 | c-guest: #C98F8F | c-elder: #8A93A6（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（新娘 / 宾客 / 长辈 三剪影） -->
  <g id="subject" stroke-linejoin="round" stroke-width="2.4">
    <path d="M56 58 L68 58 L66 96 L86 188 L38 188 L58 96 Z" fill="#F2EAE0" stroke="#D9CCBC"/>
    <path d="M104 58 L116 58 L114 96 L130 172 L90 172 L106 96 Z" fill="#C98F8F" stroke="#A87070"/>
    <path d="M150 58 L162 58 L162 96 L170 172 L142 172 L142 96 Z" fill="#8A93A6" stroke="#6E778A"/>
    <path d="M150 96 L162 96" stroke="#6E778A"/>
  </g>
  <!-- layer: 点缀（基准线 + 角色点） -->
  <g id="accent">
    <path d="M30 196 L170 196" stroke="#A85F4E" stroke-width="2" opacity="0.45" stroke-linecap="round"/>
    <circle cx="62" cy="206" r="2.6" fill="#D9CCBC"/>
    <circle cx="110" cy="206" r="2.6" fill="#C98F8F"/>
    <circle cx="156" cy="206" r="2.6" fill="#8A93A6"/>
  </g>
</svg>
<!-- seed: SS-outfit-interview-01.svg ｜ O-18 面试穿搭 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-18 | 名称 面试穿搭（衬衫 + 西裤组合） | 分类 服装·场合法 | 难度 入门 | 标签 面试/职场 -->
  <!-- palette: c-shirt: #F4F6F8 | c-pants: #4A5568 | c-line: #3A4250（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（衬衫 + 西裤） -->
  <g id="subject" stroke-linejoin="round">
    <path d="M72 52 L88 46 L100 58 L112 46 L128 52 L128 100 L72 100 Z" fill="#F4F6F8" stroke="#C9D2DA" stroke-width="2.4"/>
    <path d="M88 46 L100 58 L112 46" fill="none" stroke="#C9D2DA" stroke-width="2"/>
    <path d="M78 104 L122 104 L128 178 L104 178 L100 132 L96 178 L72 178 Z" fill="#4A5568" stroke="#3A4250" stroke-width="2.4"/>
    <path d="M100 104 L100 132" stroke="#3A4250" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（腰带线 + 基准线） -->
  <g id="accent">
    <path d="M78 108 L122 108" stroke="#2E3745" stroke-width="3" opacity="0.8"/>
    <path d="M30 196 L170 196" stroke="#A85F4E" stroke-width="2" opacity="0.4" stroke-linecap="round"/>
    <circle cx="100" cy="214" r="2.6" fill="#4A5568" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-lapel-01.svg ｜ O-19 男装 · 西装领型 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-19 | 名称 西装领型 | 分类 服装·细节 | 难度 进阶 | 标签 平驳 戗驳 青果 -->
  <!-- palette: c-a: #4A5A6A | c-b: #E4E8EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三种领型线条对比） -->
  <g id="subject" fill="none" stroke="#4A5A6A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M58 58 L100 74 L142 58"/>
    <path d="M100 74 L84 60"/>
    <path d="M100 74 L88 54"/>
    <path d="M58 116 L100 132 L142 116"/>
    <path d="M100 132 L80 108"/>
    <path d="M100 132 L90 102"/>
    <path d="M58 174 L100 190 L142 174"/>
    <path d="M100 190 C 90 172 84 162 80 150"/>
    <path d="M100 190 C 110 172 116 162 120 150"/>
  </g>
  <!-- layer: 点缀（领型标记点） -->
  <g fill="#4A5A6A" opacity="0.6">
    <circle cx="168" cy="66" r="2.8"/>
    <circle cx="168" cy="124" r="2.8"/>
    <circle cx="168" cy="182" r="2.8"/>
  </g>
</svg>
<!-- seed: SS-outfit-casual-01.svg ｜ O-20 男装 · 休闲组合 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-20 | 名称 男装休闲组合 | 分类 服装·搭配 | 难度 入门 | 标签 休闲 三层 -->
  <!-- palette: c-a: #6B7A8A | c-b: #E6ECF1（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（开衫外套 加 T 恤 加休闲裤三层示意） -->
  <g id="subject">
    <path d="M54 54 L86 54 L82 194 L56 194 Z" fill="#6B7A8A" stroke="#6B7A8A" stroke-width="2.4" stroke-linejoin="round" opacity="0.45"/>
    <path d="M114 54 L146 54 L144 194 L118 194 Z" fill="#6B7A8A" stroke="#6B7A8A" stroke-width="2.4" stroke-linejoin="round" opacity="0.45"/>
    <rect x="74" y="60" width="52" height="58" rx="4" fill="#E6ECF1" stroke="#6B7A8A" stroke-width="2.6"/>
    <rect x="76" y="120" width="20" height="76" rx="3" fill="#E6ECF1" stroke="#6B7A8A" stroke-width="2.4"/>
    <rect x="104" y="120" width="20" height="76" rx="3" fill="#E6ECF1" stroke="#6B7A8A" stroke-width="2.4"/>
  </g>
  <!-- layer: 点缀（中轴层序线 + 标记点） -->
  <g id="accent" fill="none" stroke="#6B7A8A" stroke-width="2" stroke-linecap="round">
    <path d="M100 48 L100 206" opacity="0.35" stroke-dasharray="6 5"/>
  </g>
  <g fill="#6B7A8A" opacity="0.6">
    <circle cx="100" cy="44" r="2.6"/>
    <circle cx="100" cy="112" r="2.6"/>
    <circle cx="100" cy="212" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-outfit-suit-01.svg ｜ O-21 西装剪影（翻领款） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 O-21 | 名称 西装剪影（翻领款） | 分类 服装·场合法 | 难度 入门 | 标签 职场/正式（男女通用） -->
  <!-- palette: c-suit: #5A6B7E | c-line: #48576A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="224" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（西装轮廓） -->
  <g id="subject">
    <path d="M72 62 L88 48 L100 62 L112 48 L128 62 L134 80 L124 90 L124 178 L76 178 L76 90 L66 80 Z"
          fill="#5A6B7E" stroke="#48576A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（翻领 + 扣子 + 口袋） -->
  <g id="accent">
    <path d="M88 48 L97 94 L103 94 L112 48" fill="none" stroke="#48576A" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="M88 48 L82 68 M112 48 L118 68" fill="none" stroke="#48576A" stroke-width="2.2"/>
    <circle cx="100" cy="120" r="2.6" fill="#C7CEDA"/>
    <circle cx="100" cy="138" r="2.6" fill="#C7CEDA"/>
    <path d="M82 154 L92 154" stroke="#48576A" stroke-width="2.2" stroke-linecap="round"/>
  </g>
</svg>
