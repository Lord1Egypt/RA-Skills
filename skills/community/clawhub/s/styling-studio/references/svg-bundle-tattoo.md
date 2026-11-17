<!-- ============================================================
  styling-studio SVG 种子包 · 纹身（T）
  种子数：34 ｜ 所属组：图案款式组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-tattoo-rose-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-tattoo-rose-01.svg ｜ T-01 Oldschool 经典图案（玫瑰/锚） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-01 | 名称 经典玫瑰（线稿版） | 分类 Oldschool | 难度 进阶 | 标签 小臂/肩背 -->
  <!-- palette: c-ink: #2B2B2B | c-rose: #C2554F | c-leaf: #6E8B5A（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（一笔螺旋玫瑰 + 茎叶） -->
  <g clip-path="url(#tattoo)">
    <path d="M122 118 C 110 126 96 121 96 108 C 96 95 110 88 123 91 C 138 94 144 110 137 123 C 129 137 110 141 97 132 C 83 122 83 103 96 92"
          fill="none" stroke="#C2554F" stroke-width="5.5" stroke-linecap="round"/>
    <path d="M104 136 C 100 158 96 174 88 190" fill="none" stroke="#2B2B2B" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M99 152 C 84 144 70 148 64 160 C 75 170 92 166 99 152 Z" fill="#6E8B5A" stroke="#2B2B2B" stroke-width="2.5"/>
    <path d="M97 170 C 110 162 124 166 129 178 C 118 187 102 183 97 170 Z" fill="#6E8B5A" stroke="#2B2B2B" stroke-width="2.5"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M150 88 L156 94 M156 88 L150 94" stroke="#2B2B2B" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="160" cy="78" r="2.5" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-anchor-01.svg ｜ T-01b 经典锚（Oldschool 变体） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-01b | 名称 经典锚（Oldschool 变体） | 分类 纹身·Oldschool | 难度 进阶 | 标签 小臂/小腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（锚形） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round">
    <circle cx="120" cy="56" r="10"/>
    <path d="M92 88 L148 88" stroke="#C2554F" stroke-width="6"/>
    <path d="M120 66 L120 166"/>
    <path d="M120 166 C 96 166 78 150 72 126"/>
    <path d="M120 166 C 144 166 162 150 168 126"/>
  </g>
  <!-- layer: 点缀（爪尖 + 绳圈） -->
  <g id="accent">
    <path d="M72 126 L64 116 L80 120 Z" fill="#2B2B2B"/>
    <path d="M168 126 L176 116 L160 120 Z" fill="#2B2B2B"/>
    <path d="M120 46 C 102 38 88 48 92 62" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <path d="M134 40 L140 46 M140 40 L134 46" stroke="#2B2B2B" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-tattoo-neotrad-01.svg ｜ T-02 新传统动物/花卉 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-02 | 名称 新传统（鹰与花） | 分类 新传统 | 难度 专业 | 标签 大臂/后背 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（粗线鹰头侧影 + 红花朵 + 绿叶） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M104 156 C 90 122 96 84 126 70 C 150 58 178 64 188 84 C 192 94 188 102 180 104 C 168 102 156 96 146 100 C 136 104 130 114 132 128 C 134 142 126 152 112 158"
          fill="none" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M188 84 C 202 90 210 102 206 114 C 202 124 190 124 182 118" fill="#2B2B2B"/>
    <circle cx="150" cy="96" r="4.5" fill="#2B2B2B"/>
    <circle cx="78" cy="182" r="15" fill="#C2554F" stroke="#2B2B2B" stroke-width="3"/>
    <circle cx="78" cy="182" r="4.5" fill="#FAF7F2" stroke="#2B2B2B" stroke-width="2.5"/>
    <path d="M96 172 C 110 164 126 166 132 176 C 120 186 104 183 96 172 Z" fill="#6E8B5A" stroke="#2B2B2B" stroke-width="2.5"/>
    <path d="M62 166 C 48 160 34 164 30 174 C 42 182 58 178 62 166 Z" fill="#6E8B5A" stroke="#2B2B2B" stroke-width="2.5"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="164" cy="140" r="3" fill="#C2554F"/>
    <circle cx="176" cy="150" r="2" fill="#2B2B2B"/>
    <circle cx="60" cy="204" r="2.5" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-line-flower-01.svg ｜ T-03 极简线条花卉 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-03 | 名称 极简线条花卉 | 分类 极简线条 | 难度 进阶 | 标签 手腕/耳后 -->
  <!-- palette: c-ink: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（单支线描小花） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="2.6" stroke-linecap="round">
    <path d="M120 96 L120 196"/>
    <ellipse cx="120" cy="80" rx="10" ry="20"/>
    <ellipse cx="120" cy="80" rx="10" ry="20" transform="rotate(72 120 96)"/>
    <ellipse cx="120" cy="80" rx="10" ry="20" transform="rotate(144 120 96)"/>
    <ellipse cx="120" cy="80" rx="10" ry="20" transform="rotate(216 120 96)"/>
    <ellipse cx="120" cy="80" rx="10" ry="20" transform="rotate(288 120 96)"/>
    <circle cx="120" cy="96" r="6.5"/>
    <path d="M120 146 C 104 138 90 142 84 154 C 96 164 112 160 120 146 Z"/>
    <path d="M120 168 C 136 160 150 164 156 176 C 144 186 128 182 120 168 Z"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="120" cy="206" r="3" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-mandala-01.svg ｜ T-04 几何 / 曼陀罗 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-04 | 名称 几何曼陀罗 | 分类 几何 | 难度 进阶 | 标签 小臂/胸口 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（八瓣放射 + 圈层） -->
  <g clip-path="url(#tattoo)">
    <circle cx="120" cy="120" r="30" fill="none" stroke="#2B2B2B" stroke-width="3"/>
    <circle cx="120" cy="120" r="9" fill="none" stroke="#2B2B2B" stroke-width="3"/>
    <circle cx="120" cy="120" r="62" fill="none" stroke="#2B2B2B" stroke-width="2.2"/>
    <circle cx="120" cy="120" r="88" fill="none" stroke="#2B2B2B" stroke-width="1.6" stroke-dasharray="4 6"/>
    <g fill="none" stroke="#2B2B2B" stroke-width="2.6">
      <ellipse cx="120" cy="72" rx="9" ry="20"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(45 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(90 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(135 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(180 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(225 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(270 120 120)"/>
      <ellipse cx="120" cy="72" rx="9" ry="20" transform="rotate(315 120 120)"/>
    </g>
    <g fill="#A8843C">
      <circle cx="120" cy="46" r="3.4"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(45 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(90 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(135 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(180 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(225 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(270 120 120)"/>
      <circle cx="120" cy="46" r="3.4" transform="rotate(315 120 120)"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
</svg>
<!-- seed: SS-tattoo-realistic-01.svg ｜ T-05 黑灰写实 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-05 | 名称 黑灰写实玫瑰 | 分类 写实 | 难度 专业 | 标签 小臂/大腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #8E8E8E（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（灰阶层次块层叠出玫瑰立体） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M120 56 C 152 56 176 80 176 116 C 176 154 150 180 120 180 C 90 180 64 154 64 116 C 64 80 88 56 120 56 Z" fill="#C4C4C4"/>
    <path d="M120 66 C 146 66 166 88 166 116 C 166 148 144 170 120 170 C 96 170 74 148 74 116 C 74 88 94 66 120 66 Z" fill="#9A9A9A"/>
    <path d="M120 78 C 140 78 154 96 154 116 C 154 140 138 158 120 158 C 102 158 86 140 86 116 C 86 96 100 78 120 78 Z" fill="#707070"/>
    <path d="M120 90 C 134 90 142 102 142 116 C 142 132 132 146 120 146 C 108 146 98 132 98 116 C 98 102 106 90 120 90 Z" fill="#4A4A4A"/>
    <path d="M120 100 C 128 100 132 108 132 116 C 132 126 127 134 120 134 C 113 134 108 126 108 116 C 108 108 112 100 120 100 Z" fill="#2B2B2B"/>
    <g fill="none" stroke="#E8E8E8" stroke-width="1.6" opacity="0.6">
      <path d="M120 66 C 108 84 100 100 100 118"/>
      <path d="M120 66 C 132 84 140 100 140 118"/>
      <path d="M74 116 C 92 108 108 106 120 106"/>
      <path d="M166 116 C 148 108 132 106 120 106"/>
    </g>
    <path d="M120 180 C 120 198 118 206 114 214" fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>
    <path d="M116 198 C 104 192 92 196 88 206 C 100 212 114 208 116 198 Z" fill="#4A4A4A" stroke="#2B2B2B" stroke-width="1.8"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="172" cy="72" r="2.6" fill="#9A9A9A"/>
    <circle cx="66" cy="162" r="2.2" fill="#707070"/>
    <circle cx="160" cy="186" r="2" fill="#4A4A4A"/>
  </g>
</svg>
<!-- seed: SS-tattoo-watercolor-01.svg ｜ T-06 水彩花鸟 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-06 | 名称 水彩花鸟 | 分类 水彩 | 难度 进阶 | 标签 肩头/小腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #5B8FB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（无轮廓水彩色块组成花与鸟剪影） -->
  <g id="subject" clip-path="url(#tattoo)">
    <ellipse cx="120" cy="118" rx="74" ry="54" fill="#9BB7D4" opacity="0.28"/>
    <path d="M156 76 C 176 62 200 66 210 80 C 196 78 184 82 176 92 C 186 98 200 104 208 114 C 188 110 170 102 158 92 C 152 102 140 108 126 106 C 138 98 148 88 152 78 Z" fill="#5B8FB9" opacity="0.6"/>
    <g fill="#C2554F" opacity="0.5">
      <circle cx="82" cy="156" r="26"/>
      <circle cx="60" cy="176" r="20"/>
      <circle cx="100" cy="176" r="19"/>
      <circle cx="76" cy="192" r="17"/>
    </g>
    <circle cx="82" cy="170" r="12" fill="#E0A0A0" opacity="0.6"/>
    <g fill="#6E8B5A" opacity="0.45">
      <ellipse cx="108" cy="200" rx="22" ry="9" transform="rotate(-20 108 200)"/>
      <ellipse cx="124" cy="212" rx="18" ry="8" transform="rotate(-10 124 212)"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="150" cy="130" r="4" fill="#5B8FB9" opacity="0.55"/>
    <circle cx="166" cy="146" r="3" fill="#C2554F" opacity="0.55"/>
    <circle cx="52" cy="140" r="3.5" fill="#5B8FB9" opacity="0.55"/>
    <circle cx="46" cy="206" r="3" fill="#C2554F" opacity="0.55"/>
  </g>
</svg>
<!-- seed: SS-tattoo-script-01.svg ｜ T-07 字体 / 脚本 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-07 | 名称 字体/脚本装饰 | 分类 字体/脚本 | 难度 进阶 | 标签 锁骨/手腕（字体可替换） -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（手写感文字 + 装饰线；文字内容与字体可替换） -->
  <g clip-path="url(#tattoo)">
    <text x="120" y="128" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-style="italic" fill="#2B2B2B">Stay Wild</text>
    <path d="M64 148 C 90 156 150 156 176 148" fill="none" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M76 160 C 100 166 140 166 164 160" fill="none" stroke="#A8843C" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" fill="#A8843C">
    <path d="M84 96 L87 103 L94 104 L89 109 L90 116 L84 112 L78 116 L79 109 L74 104 L81 103 Z"/>
    <circle cx="160" cy="100" r="3"/>
  </g>
</svg>
<!-- seed: SS-tattoo-dotwork-01.svg ｜ T-08 点刺（Dotwork） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-08 | 名称 点刺（Dotwork） | 分类 黑工/点刺 | 难度 进阶 | 标签 小臂/脊柱 -->
  <!-- palette: c-ink: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（同心点阵） -->
  <g clip-path="url(#tattoo)" fill="#2B2B2B">
    <circle cx="120" cy="120" r="6"/>
    <g>
      <circle cx="120" cy="102" r="3.4"/>
      <circle cx="120" cy="102" r="3.4" transform="rotate(60 120 120)"/>
      <circle cx="120" cy="102" r="3.4" transform="rotate(120 120 120)"/>
      <circle cx="120" cy="102" r="3.4" transform="rotate(180 120 120)"/>
      <circle cx="120" cy="102" r="3.4" transform="rotate(240 120 120)"/>
      <circle cx="120" cy="102" r="3.4" transform="rotate(300 120 120)"/>
    </g>
    <g opacity="0.92">
      <circle cx="120" cy="80" r="2.8"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(36 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(72 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(108 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(144 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(180 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(216 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(252 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(288 120 120)"/>
      <circle cx="120" cy="80" r="2.8" transform="rotate(324 120 120)"/>
    </g>
    <g opacity="0.8">
      <circle cx="120" cy="58" r="2.2"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(22.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(45 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(67.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(90 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(112.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(135 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(157.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(180 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(202.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(225 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(247.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(270 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(292.5 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(315 120 120)"/>
      <circle cx="120" cy="58" r="2.2" transform="rotate(337.5 120 120)"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
</svg>
<!-- seed: SS-tattoo-mountain-01.svg ｜ T-09 国风题材 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-09 | 名称 国风山水（线稿） | 分类 纹身·国风 | 难度 专业 | 标签 小臂/大臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（远山 + 月） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
    <path d="M52 164 L100 96 L148 164"/>
    <path d="M108 164 L136 124 L170 164"/>
    <circle cx="178" cy="66" r="15" stroke-width="2.6"/>
  </g>
  <!-- layer: 点缀（云线 + 水纹） -->
  <g id="accent" fill="none" stroke="#2B2B2B" stroke-width="2.2" stroke-linecap="round">
    <path d="M56 100 Q 66 92 76 100 Q 86 92 96 100"/>
    <path d="M62 186 Q 74 180 86 186 Q 98 192 110 186 Q 122 180 134 186 Q 146 192 158 186"/>
    <path d="M74 200 Q 86 194 98 200 Q 110 206 122 200 Q 134 194 146 200"/>
    <circle cx="70" cy="70" r="2.4" fill="#A8843C" stroke="none"/>
  </g>
</svg>
<!-- seed: SS-tattoo-wave-01.svg ｜ T-11 日式（锦鲤 / 波浪） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-11 | 名称 日式波浪（线稿） | 分类 纹身·日式 | 难度 专业 | 标签 半甲/背部 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #4A7BA6（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（层叠浪弧） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round">
    <path d="M40 158 C 70 118 120 106 160 122 C 190 134 200 154 196 170"/>
    <path d="M48 174 C 76 142 120 130 156 142 C 182 152 192 166 190 178"/>
    <path d="M60 190 C 84 166 118 154 148 162 C 172 170 182 180 184 190"/>
  </g>
  <!-- layer: 点缀（浪头卷 + 浪花 + 装饰） -->
  <g id="accent" fill="none" stroke="#2B2B2B" stroke-width="2.6" stroke-linecap="round">
    <path d="M160 122 C 172 106 192 106 198 120 C 202 132 192 140 184 134"/>
    <path d="M150 114 C 154 106 162 104 166 108"/>
    <path d="M186 148 C 194 142 202 144 204 152"/>
  </g>
  <g fill="#4A7BA6" opacity="0.75">
    <circle cx="176" cy="120" r="3"/>
    <circle cx="192" cy="132" r="2.5"/>
    <circle cx="166" cy="108" r="2.5"/>
  </g>
</svg>
<!-- seed: SS-tattoo-chicano-01.svg ｜ T-12 Chicano（字体+宗教意象） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-12 | 名称 Chicano 字体 | 分类 字体 | 难度 进阶 | 标签 胸口/小臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（斜体 serif 手写短词 + 小玫瑰花线） -->
  <g id="subject" clip-path="url(#tattoo)">
    <text x="120" y="126" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-style="italic" font-size="30" letter-spacing="2" fill="#2B2B2B">MI VIDA</text>
    <path d="M74 140 C 96 150 144 150 166 140" fill="none" stroke="#2B2B2B" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M120 176 C 108 180 100 174 102 165 C 104 156 116 154 122 161 C 128 169 123 180 111 182 C 100 184 90 177 89 166" fill="none" stroke="#C2554F" stroke-width="3" stroke-linecap="round"/>
    <path d="M128 160 C 138 155 148 157 152 164" fill="none" stroke="#2B2B2B" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M140 158 C 144 151 153 151 158 156 C 153 161 144 162 140 158 Z" fill="#6E8B5A" stroke="#2B2B2B" stroke-width="1.6"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M62 100 L68 106 M68 100 L62 106" stroke="#2B2B2B" stroke-width="2" stroke-linecap="round"/>
    <circle cx="180" cy="108" r="2.5" fill="#C2554F"/>
  </g>
</svg>
<!-- seed: SS-tattoo-trashpolka-01.svg ｜ T-13 Trash Polka（红黑抽象） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-13 | 名称 Trash Polka 拼贴 | 分类 抽象 | 难度 专业 | 标签 大臂/小腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（黑几何块 + 红色泼溅点 + 细斜线） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M52 64 L150 54 L160 96 L64 106 Z" fill="#2B2B2B"/>
    <path d="M56 152 L146 142 L152 186 L62 196 Z" fill="#2B2B2B"/>
    <g fill="#C2554F">
      <circle cx="168" cy="86" r="7"/>
      <circle cx="184" cy="100" r="3.5"/>
      <circle cx="156" cy="106" r="2.6"/>
      <circle cx="176" cy="72" r="2.2"/>
      <circle cx="196" cy="84" r="2"/>
    </g>
    <g stroke="#2B2B2B" stroke-width="1.4" opacity="0.6">
      <path d="M40 210 L150 100"/>
      <path d="M52 220 L174 96"/>
      <path d="M70 226 L196 104"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="96" cy="40" r="2.6" fill="#C2554F"/>
    <circle cx="120" cy="34" r="1.8" fill="#C2554F"/>
    <circle cx="150" cy="216" r="2.4" fill="#C2554F"/>
    <circle cx="176" cy="200" r="1.8" fill="#C2554F"/>
  </g>
</svg>
<!-- seed: SS-tattoo-tribal-01.svg ｜ T-14 部落 / 波利尼西亚 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-14 | 名称 部落图腾 | 分类 图腾 | 难度 进阶 | 标签 小臂/腰侧 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（黑色对称几何图腾：钩形 + 尖角） -->
  <g id="subject" clip-path="url(#tattoo)">
    <g fill="#2B2B2B">
      <path d="M118 56 C 92 56 74 74 74 100 C 74 120 86 136 104 142 C 92 128 88 112 94 98 C 100 84 108 78 118 78 Z"/>
      <path d="M118 150 L86 150 C 70 150 58 162 58 178 C 58 194 70 206 86 206 L118 206 L118 190 L88 190 C 80 190 74 185 74 178 C 74 171 80 166 88 166 L118 166 Z"/>
      <path d="M118 118 L88 118 L102 132 Z"/>
    </g>
    <g fill="#2B2B2B" transform="translate(240,0) scale(-1,1)">
      <path d="M118 56 C 92 56 74 74 74 100 C 74 120 86 136 104 142 C 92 128 88 112 94 98 C 100 84 108 78 118 78 Z"/>
      <path d="M118 150 L86 150 C 70 150 58 162 58 178 C 58 194 70 206 86 206 L118 206 L118 190 L88 190 C 80 190 74 185 74 178 C 74 171 80 166 88 166 L118 166 Z"/>
      <path d="M118 118 L88 118 L102 132 Z"/>
    </g>
    <path d="M120 62 L120 200" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="120" cy="88" r="4" fill="#2B2B2B"/>
    <circle cx="120" cy="140" r="4" fill="#2B2B2B"/>
    <circle cx="120" cy="216" r="3" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-constellation-01.svg ｜ T-15 星座符号（小图） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-15 | 名称 星座符号（七连星） | 分类 纹身·小图 | 难度 入门 | 标签 手腕/耳后 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（星点连线） -->
  <g clip-path="url(#tattoo)">
    <path d="M70 158 L96 138 L122 132 L148 122 L168 106 L174 84 L192 70" fill="none" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round"/>
    <g fill="#2B2B2B">
      <circle cx="96" cy="138" r="3"/>
      <circle cx="122" cy="132" r="3"/>
      <circle cx="148" cy="122" r="3"/>
      <circle cx="168" cy="106" r="3"/>
      <circle cx="174" cy="84" r="3"/>
    </g>
  </g>
  <!-- layer: 点缀（双大星 + 散点） -->
  <g id="accent" fill="#A8843C">
    <path d="M70 144 L73 155 L84 158 L73 161 L70 172 L67 161 L56 158 L67 155 Z"/>
    <path d="M192 56 L195 67 L206 70 L195 73 L192 84 L189 73 L178 70 L189 67 Z"/>
    <circle cx="58" cy="94" r="2.5"/>
    <circle cx="204" cy="148" r="2.5"/>
    <circle cx="88" cy="196" r="2.2"/>
    <circle cx="160" cy="182" r="2.2"/>
  </g>
</svg>
<!-- seed: SS-tattoo-animal-01.svg ｜ T-16 动物剪影（小图） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-16 | 名称 动物剪影（猫与月） | 分类 剪影 | 难度 进阶 | 标签 手腕/脚踝 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（坐姿猫剪影 + 小月牙） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M120 82 C 132 82 138 88 140 98 L 146 70 L 156 96 C 164 104 168 118 166 136 C 164 160 156 182 150 200 L 146 200 L 144 180 C 136 186 104 186 96 180 L 94 200 L 90 200 C 84 182 76 160 74 136 C 72 118 76 104 84 96 L 94 70 L 100 98 C 102 88 108 82 120 82 Z" fill="#2B2B2B"/>
    <path d="M150 200 C 172 198 182 180 178 162" fill="none" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/>
    <path d="M74 54 A 24 24 0 1 0 74 102 A 17 17 0 1 1 74 54 Z" fill="#2B2B2B"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="176" cy="60" r="3" fill="#2B2B2B"/>
    <circle cx="196" cy="82" r="2" fill="#2B2B2B"/>
    <circle cx="164" cy="44" r="2" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-sakura-01.svg ｜ T-17 樱花 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-17 | 名称 樱花（线稿） | 分类 纹身·花卉 | 难度 进阶 | 标签 锁骨/手腕 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #E8A0B4（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（五瓣樱花） -->
  <g clip-path="url(#tattoo)">
    <g fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round">
      <path d="M120 76 C 110 90 108 108 116 122 C 118 125 122 125 124 122 C 132 108 130 90 120 76 Z"/>
      <path d="M120 88 L115 78 M120 88 L125 78"/>
      <path d="M120 76 C 110 90 108 108 116 122 C 118 125 122 125 124 122 C 132 108 130 90 120 76 Z" transform="rotate(72 120 120)"/>
      <path d="M120 88 L115 78 M120 88 L125 78" transform="rotate(72 120 120)"/>
      <path d="M120 76 C 110 90 108 108 116 122 C 118 125 122 125 124 122 C 132 108 130 90 120 76 Z" transform="rotate(144 120 120)"/>
      <path d="M120 88 L115 78 M120 88 L125 78" transform="rotate(144 120 120)"/>
      <path d="M120 76 C 110 90 108 108 116 122 C 118 125 122 125 124 122 C 132 108 130 90 120 76 Z" transform="rotate(216 120 120)"/>
      <path d="M120 88 L115 78 M120 88 L125 78" transform="rotate(216 120 120)"/>
      <path d="M120 76 C 110 90 108 108 116 122 C 118 125 122 125 124 122 C 132 108 130 90 120 76 Z" transform="rotate(288 120 120)"/>
      <path d="M120 88 L115 78 M120 88 L125 78" transform="rotate(288 120 120)"/>
      <circle cx="120" cy="120" r="6"/>
    </g>
  </g>
  <!-- layer: 点缀（花蕊 + 落瓣） -->
  <g id="accent">
    <g fill="#2B2B2B">
      <circle cx="120" cy="112" r="1.6"/>
      <circle cx="128" cy="116" r="1.6"/>
      <circle cx="125" cy="125" r="1.6"/>
      <circle cx="115" cy="125" r="1.6"/>
      <circle cx="112" cy="116" r="1.6"/>
    </g>
    <path d="M176 178 C 172 184 172 192 176 197 C 180 192 180 184 176 178 Z" fill="none" stroke="#E8A0B4" stroke-width="2.2"/>
    <path d="M64 168 C 60 174 60 182 64 187 C 68 182 68 174 64 168 Z" fill="none" stroke="#E8A0B4" stroke-width="2.2"/>
  </g>
</svg>
<!-- seed: SS-tattoo-peony-01.svg ｜ T-18 牡丹 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-18 | 名称 牡丹（线稿） | 分类 纹身·国风花卉 | 难度 专业 | 标签 大臂/肩背 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（多层牡丹） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="2.6" stroke-linejoin="round">
    <ellipse cx="120" cy="76" rx="26" ry="16"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(45 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(90 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(135 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(180 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(225 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(270 120 112)"/>
    <ellipse cx="120" cy="76" rx="26" ry="16" transform="rotate(315 120 112)"/>
    <ellipse cx="120" cy="94" rx="15" ry="10"/>
    <ellipse cx="120" cy="94" rx="15" ry="10" transform="rotate(72 120 112)"/>
    <ellipse cx="120" cy="94" rx="15" ry="10" transform="rotate(144 120 112)"/>
    <ellipse cx="120" cy="94" rx="15" ry="10" transform="rotate(216 120 112)"/>
    <ellipse cx="120" cy="94" rx="15" ry="10" transform="rotate(288 120 112)"/>
    <circle cx="120" cy="112" r="7"/>
    <path d="M120 145 C 116 168 110 186 100 200" stroke-width="3"/>
    <path d="M112 170 C 98 162 84 166 78 178 C 90 188 106 184 112 170 Z" stroke-width="2.4"/>
    <path d="M126 178 C 140 170 154 174 160 186 C 148 196 132 192 126 178 Z" stroke-width="2.4"/>
  </g>
  <!-- layer: 点缀（花蕊点） -->
  <g id="accent" fill="#C2554F">
    <circle cx="120" cy="108" r="1.8"/>
    <circle cx="126" cy="112" r="1.8"/>
    <circle cx="116" cy="117" r="1.8"/>
    <circle cx="120" cy="202" r="2.4" opacity="0.8"/>
  </g>
</svg>
<!-- seed: SS-tattoo-brush-01.svg ｜ T-19 抽象笔刷 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-19 | 名称 抽象笔刷 | 分类 抽象 | 难度 进阶 | 标签 小臂/肩头 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（两道粗细渐变的笔刷墨迹） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M46 196 C 76 150 112 108 152 84 C 164 77 176 74 184 78 C 186 88 180 96 168 102 C 132 122 100 158 74 200 C 66 202 56 200 46 196 Z" fill="#2B2B2B"/>
    <path d="M66 66 C 92 76 120 96 142 124 C 158 144 168 166 170 188 C 162 190 154 188 148 182 C 144 158 132 134 112 114 C 92 94 74 82 62 76 C 58 72 60 68 66 66 Z" fill="#2B2B2B" opacity="0.82"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="188" cy="190" r="4" fill="#2B2B2B"/>
    <circle cx="196" cy="176" r="2.4" fill="#2B2B2B"/>
    <circle cx="48" cy="60" r="3" fill="#2B2B2B"/>
    <circle cx="40" cy="74" r="2" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-chain-01.svg ｜ T-20 链条 / 锁链元素 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-20 | 名称 链条元素 | 分类 元素 | 难度 入门 | 标签 手腕/脚踝 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（五个交错咬合椭圆链环） -->
  <g id="subject" clip-path="url(#tattoo)">
    <g fill="none" stroke="#2B2B2B" stroke-width="6">
      <ellipse cx="62" cy="178" rx="23" ry="13" transform="rotate(45 62 178)"/>
      <ellipse cx="91" cy="149" rx="23" ry="13" transform="rotate(45 91 149)"/>
      <ellipse cx="120" cy="120" rx="23" ry="13" transform="rotate(45 120 120)"/>
      <ellipse cx="149" cy="91" rx="23" ry="13" transform="rotate(45 149 91)"/>
      <ellipse cx="178" cy="62" rx="23" ry="13" transform="rotate(45 178 62)"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="62" cy="178" r="2.6" fill="#2B2B2B" opacity="0.55"/>
    <circle cx="120" cy="120" r="2.6" fill="#2B2B2B" opacity="0.55"/>
    <circle cx="178" cy="62" r="2.6" fill="#2B2B2B" opacity="0.55"/>
  </g>
</svg>
<!-- seed: SS-tattoo-snake-dagger-01.svg ｜ T-21 蛇与匕首（经典组合） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-21 | 名称 蛇与匕首 | 分类 元素 | 难度 专业 | 标签 小臂/大腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（竖直匕首 + S 形缠绕蛇身） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M120 40 L128 78 L126 168 L114 168 L112 78 Z" fill="none" stroke="#2B2B2B" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M120 46 L120 164" stroke="#2B2B2B" stroke-width="1.4"/>
    <path d="M92 168 L148 168" stroke="#2B2B2B" stroke-width="6" stroke-linecap="round"/>
    <path d="M112 168 L112 210 L128 210 L128 168" fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>
    <path d="M120 210 L120 218" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>
    <path d="M70 84 C 100 74 140 96 150 120 C 158 140 140 156 118 160 C 96 164 76 156 68 140 C 60 124 72 108 92 106 C 112 104 128 114 130 128 C 132 140 122 150 110 150"
          fill="none" stroke="#2B2B2B" stroke-width="6" stroke-linecap="round"/>
    <circle cx="108" cy="150" r="7" fill="#2B2B2B"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M102 148 L92 145 M102 152 L92 155" stroke="#C2554F" stroke-width="2" stroke-linecap="round"/>
    <circle cx="150" cy="52" r="2.4" fill="#2B2B2B"/>
    <circle cx="176" cy="120" r="2" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-pet-01.svg ｜ T-22 宠物主题 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-22 | 名称 宠物主题（爪印与狗头） | 分类 主题 | 难度 入门 | 标签 手腕/小臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（狗头简线 + 实心爪印） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M98 66 L90 44 L112 56 C 122 51 134 51 144 56 L164 44 L158 66 C 168 74 174 88 170 102 C 164 118 146 128 120 128 C 94 128 76 118 70 102 C 66 88 72 74 82 66 Z"
          fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>
    <circle cx="104" cy="86" r="3.4" fill="#2B2B2B"/>
    <circle cx="136" cy="86" r="3.4" fill="#2B2B2B"/>
    <ellipse cx="120" cy="106" rx="6" ry="4.6" fill="#2B2B2B"/>
    <g fill="#2B2B2B">
      <ellipse cx="120" cy="182" rx="22" ry="18"/>
      <ellipse cx="94" cy="158" rx="8" ry="10"/>
      <ellipse cx="112" cy="148" rx="8" ry="10"/>
      <ellipse cx="132" cy="150" rx="8" ry="10"/>
      <ellipse cx="150" cy="162" rx="7" ry="9"/>
    </g>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M172 180 C 166 174 172 168 176 172 C 180 168 186 174 180 180 L176 186 Z" fill="#C2554F"/>
    <circle cx="60" cy="190" r="2.4" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-planet-01.svg ｜ T-23 星空 / 行星 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-23 | 名称 星空 / 行星 | 分类 纹身·题材 | 难度 进阶 | 标签 小臂/后背 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #4A7BA6（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（行星 + 光环） -->
  <g clip-path="url(#tattoo)" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round">
    <circle cx="120" cy="118" r="36"/>
    <ellipse cx="120" cy="118" rx="60" ry="15" transform="rotate(-16 120 118)" stroke-width="2.4"/>
    <path d="M96 96 C 108 104 108 132 96 142" stroke-width="2"/>
    <path d="M144 100 C 134 110 134 128 144 136" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（星点 + 轨道弧） -->
  <g id="accent">
    <path d="M52 60 A 88 88 0 0 1 190 178" fill="none" stroke="#4A7BA6" stroke-width="1.6" stroke-dasharray="3 6" opacity="0.8"/>
    <path d="M180 62 L183 70 L191 72 L184 77 L185 85 L178 80 L171 85 L172 77 L165 72 L173 70 Z" fill="#4A7BA6" opacity="0.9"/>
    <circle cx="58" cy="170" r="2.4" fill="#2B2B2B"/>
    <circle cx="76" cy="190" r="2" fill="#2B2B2B"/>
    <circle cx="196" cy="120" r="2" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-monogram-01.svg ｜ T-24 字母组合（Monogram） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-24 | 名称 字母组合（A 与 M） | 分类 字体 | 难度 进阶 | 标签 锁骨/手腕 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（圆形外框内 A 与 M 交叠字母） -->
  <g id="subject" clip-path="url(#tattoo)">
    <circle cx="120" cy="120" r="84" fill="none" stroke="#2B2B2B" stroke-width="3"/>
    <circle cx="120" cy="120" r="76" fill="none" stroke="#2B2B2B" stroke-width="1.2"/>
    <text x="120" y="152" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="96" font-weight="bold" fill="#2B2B2B" transform="translate(-14,0)">A</text>
    <text x="120" y="152" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="96" font-weight="bold" fill="none" stroke="#2B2B2B" stroke-width="2.2" transform="translate(14,0)">M</text>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M120 22 L122 30 L130 32 L122 34 L120 42 L118 34 L110 32 L118 30 Z" fill="#A8843C"/>
    <path d="M120 198 L122 206 L130 208 L122 210 L120 218 L118 210 L110 208 L118 206 Z" fill="#A8843C"/>
    <circle cx="44" cy="120" r="3" fill="#A8843C"/>
    <circle cx="196" cy="120" r="3" fill="#A8843C"/>
  </g>
</svg>
<!-- seed: SS-tattoo-rings-01.svg ｜ T-25 对戒纹身（双人） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-25 | 名称 对戒纹身 | 分类 主题 | 难度 入门 | 标签 手指/手腕 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（两个交叠戒指环 + 中心小心形） -->
  <g id="subject" clip-path="url(#tattoo)">
    <circle cx="98" cy="130" r="40" fill="none" stroke="#2B2B2B" stroke-width="7"/>
    <circle cx="142" cy="130" r="40" fill="none" stroke="#2B2B2B" stroke-width="7"/>
    <path d="M98 90 L106 78 L98 66 L90 78 Z" fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>
    <path d="M120 144 C 110 134 104 129 104 121 C 104 115 110 112 115 115 C 117 117 119 119 120 122 C 121 119 123 117 125 115 C 130 112 136 115 136 121 C 136 129 130 134 120 144 Z" fill="#C2554F"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <circle cx="98" cy="58" r="2.6" fill="#2B2B2B"/>
    <circle cx="142" cy="58" r="2.6" fill="#2B2B2B"/>
    <circle cx="120" cy="196" r="2.4" fill="#C2554F"/>
  </g>
</svg>
<!-- seed: SS-tattoo-date-01.svg ｜ T-26 纪念日期 / 数字 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-26 | 名称 纪念日期 | 分类 字体 | 难度 入门 | 标签 手腕/前臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（日期竖排 serif 数字） -->
  <g id="subject" clip-path="url(#tattoo)">
    <text x="120" y="120" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="30" letter-spacing="2" fill="#2B2B2B" transform="rotate(-90 120 120)">1990.05.20</text>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M120 30 L122 38 L130 40 L122 42 L120 50 L118 42 L110 40 L118 38 Z" fill="#2B2B2B"/>
    <path d="M120 190 L122 198 L130 200 L122 202 L120 210 L118 202 L110 200 L118 198 Z" fill="#2B2B2B"/>
    <circle cx="120" cy="22" r="2.4" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-family-01.svg ｜ T-27 亲子主题 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-27 | 名称 亲子主题（大手牵小手） | 分类 主题 | 难度 进阶 | 标签 小臂/肩头 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（大手牵小手线稿 + 上方小心形） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M100 120 C 98 106 104 96 114 92 C 124 89 134 94 136 104 C 138 114 132 124 120 128 C 112 130 104 128 100 120 Z" fill="none" stroke="#2B2B2B" stroke-width="3.4"/>
    <path d="M110 94 L110 80 M120 92 L122 78 M130 98 L134 86" stroke="#2B2B2B" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M78 200 C 74 180 80 162 96 152 C 108 144 124 142 138 148 C 150 153 156 164 154 176 C 152 190 138 200 120 202 C 104 204 86 204 78 200 Z" fill="none" stroke="#2B2B2B" stroke-width="4"/>
    <path d="M96 152 L94 132 M112 148 L112 128 M128 148 L130 128 M142 152 L146 134" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M120 60 C 112 50 104 46 104 38 C 104 32 110 29 115 32 C 117 34 119 36 120 39 C 121 36 123 34 125 32 C 130 29 136 32 136 38 C 136 46 128 50 120 60 Z" fill="#C2554F"/>
    <circle cx="168" cy="170" r="2.4" fill="#2B2B2B"/>
    <circle cx="64" cy="150" r="2.4" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-scene-01.svg ｜ T-28 生活场景简笔 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-28 | 名称 生活场景（家与树） | 分类 场景 | 难度 进阶 | 标签 小臂/后背 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #2B2B2B（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（小房子 + 树 + 太阳简笔线） -->
  <g id="subject" clip-path="url(#tattoo)">
    <circle cx="64" cy="66" r="18" fill="none" stroke="#2B2B2B" stroke-width="3.5"/>
    <g stroke="#2B2B2B" stroke-width="3" stroke-linecap="round">
      <path d="M64 40 L64 32 M64 100 L64 92 M38 66 L30 66 M98 66 L90 66 M46 48 L40 42 M82 84 L88 90 M82 48 L88 42"/>
    </g>
    <path d="M60 168 L200 168" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <path d="M104 168 L104 120 L140 92 L176 120 L176 168 Z" fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>
    <path d="M96 122 L140 88 L184 122" fill="none" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="130" y="136" width="22" height="32" fill="none" stroke="#2B2B2B" stroke-width="3"/>
    <circle cx="146" cy="152" r="1.8" fill="#2B2B2B"/>
    <rect x="112" y="132" width="14" height="14" fill="none" stroke="#2B2B2B" stroke-width="2.4"/>
    <path d="M192 168 L192 132" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>
    <circle cx="192" cy="114" r="20" fill="none" stroke="#2B2B2B" stroke-width="3.5"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <path d="M52 108 C 56 104 60 104 64 108" fill="none" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M64 108 C 68 104 72 104 76 108" fill="none" stroke="#2B2B2B" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M74 178 L66 186 M86 180 L80 190 M176 180 L184 188" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-tattoo-calligraphy-01.svg ｜ T-29 汉字 / 书法 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-29 | 名称 汉字 / 书法（示例"静"） | 分类 纹身·字体 | 难度 专业 | 标签 手腕/锁骨（字体版权注意） -->
  <!-- palette: c-ink: #2B2B2B | c-seal: #C2554F（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（书法字） -->
  <g clip-path="url(#tattoo)">
    <text x="120" y="146" text-anchor="middle" font-family="KaiTi, STKaiti, 'Songti SC', serif" font-size="76" fill="#2B2B2B">静</text>
  </g>
  <!-- layer: 点缀（印章 + 墨点） -->
  <g id="accent">
    <rect x="160" y="164" width="26" height="26" rx="3" fill="none" stroke="#C2554F" stroke-width="2.6"/>
    <rect x="166" y="170" width="14" height="14" rx="1.5" fill="#C2554F" opacity="0.55"/>
    <circle cx="66" cy="88" r="2.6" fill="#2B2B2B" opacity="0.7"/>
    <circle cx="58" cy="176" r="2" fill="#2B2B2B" opacity="0.5"/>
  </g>
</svg>
<!-- seed: SS-tattoo-ridge-01.svg ｜ T-30 半甲几何山脉 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-30 | 名称 半甲几何山脉 | 分类 几何 | 难度 专业 | 标签 半甲/大臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #989898（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g id="base" clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（三层几何山峰层叠 + 小太阳） -->
  <g id="subject" clip-path="url(#tattoo)">
    <path d="M10 214 L54 132 L92 178 L124 118 L170 200 L230 200 L230 230 L10 230 Z" fill="#C6C6C6"/>
    <path d="M10 222 L48 160 L86 200 L120 146 L166 218 L10 218 Z" fill="#989898"/>
    <path d="M10 228 L58 188 L104 224 L148 180 L196 228 L10 228 Z" fill="#6A6A6A"/>
    <circle cx="180" cy="86" r="18" fill="none" stroke="#2B2B2B" stroke-width="3"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" clip-path="url(#tattoo)">
    <g stroke="#2B2B2B" stroke-width="2.2" stroke-linecap="round">
      <path d="M180 58 L180 50 M180 122 L180 114 M152 86 L144 86 M216 86 L208 86"/>
    </g>
    <circle cx="60" cy="70" r="2.4" fill="#2B2B2B"/>
    <circle cx="92" cy="58" r="1.8" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-swallow-01.svg ｜ T-31 燕子 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-31 | 名称 燕子（Oldschool 经典元素） | 分类 纹身·经典元素 | 难度 进阶 | 标签 锁骨/小臂 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #4A7BA6（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（展翅燕子） -->
  <g clip-path="url(#tattoo)">
    <path d="M120 106 C 112 112 108 122 108 132 C 108 146 112 156 120 164 C 128 156 132 146 132 132 C 132 122 128 112 120 106 Z" fill="#2B2B2B"/>
    <circle cx="120" cy="98" r="11" fill="#2B2B2B"/>
    <path d="M109 96 L96 100 L109 104 Z" fill="#2B2B2B"/>
    <path d="M110 126 C 90 112 66 110 46 122 C 72 130 94 136 110 140 Z" fill="#2B2B2B"/>
    <path d="M130 126 C 150 112 174 110 194 122 C 168 130 146 136 130 140 Z" fill="#2B2B2B"/>
    <path d="M112 156 L100 190 L114 172 Z" fill="#2B2B2B"/>
    <path d="M128 156 L140 190 L126 172 Z" fill="#2B2B2B"/>
  </g>
  <!-- layer: 点缀（腹部羽纹 + 眼点） -->
  <g id="accent">
    <path d="M114 138 C 117 142 123 142 126 138" fill="none" stroke="#FAF7F2" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M115 148 C 117 151 123 151 125 148" fill="none" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="123" cy="96" r="2.2" fill="#FAF7F2"/>
    <path d="M162 76 L168 82 M168 76 L162 82" stroke="#4A7BA6" stroke-width="2.4" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-tattoo-snake-01.svg ｜ T-32 蛇（盘绕） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-32 | 名称 蛇（盘绕 S 形） | 分类 纹身·经典元素 | 难度 进阶 | 标签 小臂/大腿 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #6E8B5A（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（S 形蛇身） -->
  <g clip-path="url(#tattoo)">
    <path d="M146 196 C 118 202 96 184 100 158 C 104 132 136 128 138 104 C 140 80 118 64 94 70"
          fill="none" stroke="#2B2B2B" stroke-width="10" stroke-linecap="round"/>
    <ellipse cx="88" cy="66" rx="13" ry="9" fill="#2B2B2B" transform="rotate(-34 88 66)"/>
    <path d="M77 60 L62 52 M77 60 L60 62" fill="none" stroke="#2B2B2B" stroke-width="2.6" stroke-linecap="round"/>
    <circle cx="90" cy="62" r="2" fill="#FAF7F2"/>
  </g>
  <!-- layer: 点缀（鳞纹 + 尾梢） -->
  <g id="accent">
    <g fill="none" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round" opacity="0.9">
      <path d="M138 150 C 132 146 132 140 138 136"/>
      <path d="M127 150 C 121 146 121 140 127 136"/>
      <path d="M141 108 C 135 104 135 98 141 94"/>
      <path d="M130 108 C 124 104 124 98 130 94"/>
      <path d="M112 84 C 108 88 102 88 100 84"/>
    </g>
    <path d="M150 198 L162 206 L146 206 Z" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-dagger-01.svg ｜ T-33 匕首 -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-33 | 名称 匕首（经典元素） | 分类 纹身·经典元素 | 难度 进阶 | 标签 小臂（可配玫瑰组合） -->
  <!-- palette: c-ink: #2B2B2B | c-steel: #C7CEDA（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（匕首） -->
  <g clip-path="url(#tattoo)">
    <path d="M120 42 L130 146 L120 164 L110 146 Z" fill="#C7CEDA" stroke="#2B2B2B" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M120 52 L120 150" stroke="#2B2B2B" stroke-width="2"/>
    <rect x="92" y="154" width="56" height="9" rx="3" fill="#2B2B2B"/>
    <path d="M112 163 L128 163 L125 194 L115 194 Z" fill="#B07040" stroke="#2B2B2B" stroke-width="3" stroke-linejoin="round"/>
    <path d="M114 172 L126 172 M114 180 L126 180" stroke="#2B2B2B" stroke-width="2.2"/>
    <circle cx="120" cy="202" r="7.5" fill="#B07040" stroke="#2B2B2B" stroke-width="3"/>
  </g>
  <!-- layer: 点缀（刃光 + 装饰点） -->
  <g id="accent">
    <path d="M124 58 L124 132" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>
    <circle cx="86" cy="88" r="2.6" fill="#2B2B2B"/>
    <circle cx="156" cy="112" r="2.2" fill="#2B2B2B"/>
  </g>
</svg>
<!-- seed: SS-tattoo-dragon-01.svg ｜ T-34 龙（简笔盘龙 · 东方） -->
<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 T-34 | 名称 龙（简笔盘龙·东方） | 分类 纹身·东方 | 难度 专业 | 标签 大臂/背部 -->
  <!-- palette: c-ink: #2B2B2B | c-accent: #A8843C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="tattoo"><rect x="10" y="10" width="220" height="220" rx="18"/></clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#tattoo)">
    <rect x="10" y="10" width="220" height="220" fill="#FAF7F2"/>
  </g>
  <!-- layer: 主体（盘龙身 + 头） -->
  <g clip-path="url(#tattoo)">
    <path d="M60 190 C 92 182 96 152 122 142 C 150 132 152 104 136 88 C 120 72 96 78 92 98"
          fill="none" stroke="#2B2B2B" stroke-width="9" stroke-linecap="round"/>
    <path d="M88 100 C 84 92 86 82 94 78" fill="none" stroke="#2B2B2B" stroke-width="9" stroke-linecap="round"/>
    <path d="M82 84 L68 70 M92 76 L86 60" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round"/>
    <path d="M80 104 C 68 110 60 118 56 130" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <circle cx="92" cy="88" r="2.4" fill="#A8843C"/>
  </g>
  <!-- layer: 点缀（爪 + 尾鳍 + 鳞点） -->
  <g id="accent">
    <path d="M108 146 C 102 152 100 158 102 164 M112 148 C 110 154 110 160 112 166 M116 150 C 118 156 120 160 124 162" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <path d="M136 126 C 144 128 150 134 152 142 M136 122 C 146 120 152 122 158 128" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <path d="M54 194 L66 204 L50 206 Z" fill="#2B2B2B"/>
    <g fill="#A8843C" opacity="0.85">
      <circle cx="108" cy="152" r="2.2"/>
      <circle cx="128" cy="134" r="2.2"/>
      <circle cx="138" cy="108" r="2.2"/>
      <circle cx="122" cy="82" r="2.2"/>
    </g>
  </g>
</svg>
