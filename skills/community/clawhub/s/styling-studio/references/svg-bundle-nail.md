<!-- ============================================================
  styling-studio SVG 种子包 · 美甲（N）
  种子数：44 ｜ 所属组：图案款式组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-nail-solid-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-nail-solid-01.svg ｜ N-01 纯色单色款（短方圆） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-01 | 名称 纯色单色款（短方圆） | 分类 简约风格 | 难度 入门 | 标签 日常/职场 -->
  <!-- palette: c-base: #F0D9C8 | c-gloss: #FFF6EF | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="baseGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8EDE3"/>
      <stop offset="100%" stop-color="#EFD4C2"/>
    </linearGradient>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#baseGrad)"/>
  </g>
  <!-- layer: 主体（柔光高光） -->
  <g clip-path="url(#nail)">
    <ellipse cx="86" cy="70" rx="22" ry="34" fill="#FFF6EF" opacity="0.55"/>
    <ellipse cx="128" cy="150" rx="12" ry="20" fill="#FFF6EF" opacity="0.25"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-ombre-01.svg ｜ N-02 裸透渐变 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-02 | 名称 裸透渐变 | 分类 特效工艺 | 难度 入门 | 标签 日常/通勤 -->
  <!-- palette: c-from: #EFD3C6 | c-to: #FDF6F1 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="ombre" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EFD3C6"/>
      <stop offset="55%" stop-color="#F7E8E0"/>
      <stop offset="100%" stop-color="#FDF6F1" stop-opacity="0.5"/>
    </linearGradient>
  </defs>
  <!-- layer: 底（裸粉到透白线性渐变） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FDF6F1"/>
    <rect x="40" y="16" width="120" height="210" fill="url(#ombre)"/>
  </g>
  <!-- layer: 主体（柔光过渡） -->
  <g clip-path="url(#nail)">
    <ellipse cx="86" cy="70" rx="18" ry="30" fill="#FFFFFF" opacity="0.35"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="128" cy="62" r="3" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="136" cy="74" r="2" fill="#FFFFFF" opacity="0.5"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-french-01.svg ｜ N-03 经典法式（白边） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-03 | 名称 经典法式（白边） | 分类 简约风格 | 难度 入门 | 标签 婚礼/职场 -->
  <!-- palette: c-base: #F0D9C8 | c-tip: #FFF8F2 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="baseGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8EDE3"/>
      <stop offset="100%" stop-color="#F0D9C8"/>
    </linearGradient>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#baseGrad)"/>
  </g>
  <!-- layer: 主体（指尖月牙边） -->
  <g clip-path="url(#nail)" id="tip">
    <path d="M40 75 Q100 95 160 75 L160 16 L40 16 Z" fill="#FFF8F2"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-french-02.svg ｜ N-04 彩色法式/斜法式 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-04 | 名称 斜法式 | 分类 简约风格 | 难度 入门 | 标签 日常/约会 -->
  <!-- palette: c-base: #F0D9C8 | c-tip: #FFF8F2 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="baseGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8EDE3"/>
      <stop offset="100%" stop-color="#EFD4C2"/>
    </linearGradient>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#baseGrad)"/>
  </g>
  <!-- layer: 主体（斜向月牙边） -->
  <g clip-path="url(#nail)" id="tip">
    <path d="M40 52 Q100 78 160 116 L160 16 L40 16 Z" fill="#FFF8F2"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M40 55 Q100 81 160 119" fill="none" stroke="#E3C9B4" stroke-width="1.2" opacity="0.8"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-liner-01.svg ｜ N-05 极细线条描边 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-05 | 名称 极细线条描边 | 分类 简约风格 | 难度 入门 | 标签 日常 -->
  <!-- palette: c-base: #F8EFE7 | c-line: #A88B76 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F8EFE7"/>
  </g>
  <!-- layer: 主体（内圈细线） -->
  <g id="subject">
    <path d="M100 28 C 63 28 52 58 52 100 L52 166 C 52 196 74 212 100 212 C 126 212 148 196 148 166 L148 100 C 148 58 137 28 100 28 Z" fill="none" stroke="#A88B76" stroke-width="2.4"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="100" cy="196" r="3" fill="#A88B76"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-dot-01.svg ｜ N-06 波点 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-06 | 名称 波点 | 分类 几何图形 | 难度 入门 | 标签 日常/约会 -->
  <!-- palette: c-base: #FBEDE4 | c-dot: #FFFFFF | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nailDot">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nailDot)">
    <rect x="40" y="16" width="120" height="210" fill="#FBEDE4"/>
  </g>
  <!-- layer: 主体（波点阵） -->
  <g clip-path="url(#nailDot)" fill="#FFFFFF">
    <circle cx="62" cy="50" r="9"/><circle cx="100" cy="40" r="9"/><circle cx="138" cy="50" r="9"/>
    <circle cx="80" cy="84" r="9"/><circle cx="118" cy="84" r="9"/>
    <circle cx="62" cy="118" r="9"/><circle cx="100" cy="108" r="9"/><circle cx="138" cy="118" r="9"/>
    <circle cx="80" cy="152" r="9"/><circle cx="118" cy="152" r="9"/>
    <circle cx="62" cy="186" r="9"/><circle cx="100" cy="176" r="9"/><circle cx="138" cy="186" r="9"/>
    <circle cx="80" cy="214" r="9"/><circle cx="118" cy="214" r="9"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-stripe-01.svg ｜ N-07 条纹 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-07 | 名称 条纹 | 分类 几何图形 | 难度 入门 | 标签 日常 -->
  <!-- palette: c-base: #FBEDE4 | c-stripe: #C9748A | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBEDE4"/>
  </g>
  <!-- layer: 主体（斜条纹 ×4） -->
  <g clip-path="url(#nail)" fill="#C9748A">
    <path d="M40 62 L160 22 L160 44 L40 84 Z"/>
    <path d="M40 110 L160 70 L160 92 L40 132 Z"/>
    <path d="M40 158 L160 118 L160 140 L40 180 Z"/>
    <path d="M40 206 L160 166 L160 188 L40 228 Z"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-checker-01.svg ｜ N-08 棋盘格 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-08 | 名称 棋盘格 | 分类 几何图形 | 难度 入门 | 标签 日常/派对 -->
  <!-- palette: c-base: #FAF6F2 | c-cell: #2B2B2B | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <pattern id="checker" width="30" height="30" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="30" height="30" fill="#FAF6F2"/>
      <rect x="0" y="0" width="15" height="15" fill="#2B2B2B"/>
      <rect x="15" y="15" width="15" height="15" fill="#2B2B2B"/>
    </pattern>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FAF6F2"/>
  </g>
  <!-- layer: 主体（棋盘格） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#checker)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-geo-01.svg ｜ N-09 几何色块拼接 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-09 | 名称 几何色块拼接 | 分类 几何图形 | 难度 进阶 | 标签 职场/派对 -->
  <!-- palette: c-base: #FBEDE4 | c-block1: #D9A38F | c-block2: #8E6E5E | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBEDE4"/>
  </g>
  <!-- layer: 主体（三角色块拼接） -->
  <g clip-path="url(#nail)">
    <path d="M40 226 L160 226 L160 40 Z" fill="#D9A38F"/>
    <path d="M40 16 L122 16 L40 100 Z" fill="#8E6E5E"/>
    <path d="M122 16 L160 40 L124 72 Z" fill="#F0D9C8" opacity="0.9"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="70" cy="150" r="4" fill="#FBEDE4"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-zigzag-01.svg ｜ N-10 折线/闪电锐角 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-10 | 名称 折线/闪电锐角 | 分类 几何图形 | 难度 进阶 | 标签 派对/个性 -->
  <!-- palette: c-base: #F8EFE7 | c-bolt: #D9A648 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F8EFE7"/>
  </g>
  <!-- layer: 主体（闪电折线） -->
  <g clip-path="url(#nail)">
    <path d="M82 48 L128 92 L102 104 L136 168 L90 128 L114 116 L82 48 Z" fill="#D9A648"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M118 186 L128 194 L118 202 L108 194 Z" fill="#D9A648" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-daisy-01.svg ｜ N-11 手绘小雏菊 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-11 | 名称 手绘小雏菊 | 分类 花卉植物 | 难度 进阶 | 标签 日常/约会 -->
  <!-- palette: c-base: #FBF3EA | c-petal: #FFFDF8 | c-core: #F2C14E | c-leaf: #A8BD84 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBF3EA"/>
  </g>
  <!-- layer: 主体（主花 + 小伴花） -->
  <g clip-path="url(#nail)">
    <g>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8"/>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8" transform="rotate(60 100 100)"/>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8" transform="rotate(120 100 100)"/>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8" transform="rotate(180 100 100)"/>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8" transform="rotate(240 100 100)"/>
      <ellipse cx="100" cy="74" rx="9" ry="17" fill="#FFFDF8" transform="rotate(300 100 100)"/>
      <circle cx="100" cy="100" r="12" fill="#F2C14E"/>
    </g>
    <g opacity="0.9">
      <ellipse cx="66" cy="162" rx="5.5" ry="10" fill="#FFFDF8"/>
      <ellipse cx="66" cy="162" rx="5.5" ry="10" fill="#FFFDF8" transform="rotate(72 66 178)"/>
      <ellipse cx="66" cy="162" rx="5.5" ry="10" fill="#FFFDF8" transform="rotate(144 66 178)"/>
      <ellipse cx="66" cy="162" rx="5.5" ry="10" fill="#FFFDF8" transform="rotate(216 66 178)"/>
      <ellipse cx="66" cy="162" rx="5.5" ry="10" fill="#FFFDF8" transform="rotate(288 66 178)"/>
      <circle cx="66" cy="178" r="7" fill="#F2C14E"/>
    </g>
    <path d="M112 178 C 120 186 132 188 140 184" fill="none" stroke="#A8BD84" stroke-width="3"/>
    <ellipse cx="126" cy="180" rx="9" ry="5" fill="#A8BD84" transform="rotate(18 126 180)"/>
    <ellipse cx="138" cy="186" rx="8" ry="4.5" fill="#A8BD84" transform="rotate(30 138 186)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="140" cy="70" r="3" fill="#F2C14E" opacity="0.8"/>
    <circle cx="150" cy="82" r="2" fill="#F2C14E" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-vine-01.svg ｜ N-12 藤蔓线条 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-12 | 名称 藤蔓线条 | 分类 花卉植物 | 难度 进阶 | 标签 日常/婚礼 -->
  <!-- palette: c-base: #F7F1E8 | c-vine: #8FA36F | c-leaf: #A8BD84 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F7F1E8"/>
  </g>
  <!-- layer: 主体（藤蔓主线 + 叶片） -->
  <g clip-path="url(#nail)">
    <path d="M100 34 C 74 76 126 110 100 150 C 84 176 110 196 100 218" fill="none" stroke="#8FA36F" stroke-width="3"/>
    <ellipse cx="84" cy="66" rx="7" ry="12" fill="#A8BD84" transform="rotate(-38 84 66)"/>
    <ellipse cx="118" cy="92" rx="7" ry="12" fill="#A8BD84" transform="rotate(38 118 92)"/>
    <ellipse cx="82" cy="122" rx="7" ry="12" fill="#A8BD84" transform="rotate(-42 82 122)"/>
    <ellipse cx="118" cy="152" rx="7" ry="12" fill="#A8BD84" transform="rotate(40 118 152)"/>
    <ellipse cx="86" cy="184" rx="6" ry="10" fill="#A8BD84" transform="rotate(-34 86 184)"/>
    <circle cx="100" cy="34" r="4" fill="#8FA36F"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="132" cy="62" r="3" fill="#D9A648" opacity="0.75"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-dryflower-01.svg ｜ N-13 干花压花风 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-13 | 名称 干花压花风 | 分类 花卉植物 | 难度 入门 | 标签 森系/日常 -->
  <!-- palette: c-base: #EFE6D8 | c-petal: #D9C3C7 | c-core: #BFA46B | c-branch: #A89B84 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <g id="dryflower">
      <ellipse cx="0" cy="-11" rx="6" ry="11" fill="#D9C3C7" opacity="0.92"/>
      <ellipse cx="0" cy="-11" rx="6" ry="11" fill="#D9C3C7" opacity="0.92" transform="rotate(72)"/>
      <ellipse cx="0" cy="-11" rx="6" ry="11" fill="#D9C3C7" opacity="0.92" transform="rotate(144)"/>
      <ellipse cx="0" cy="-11" rx="6" ry="11" fill="#D9C3C7" opacity="0.92" transform="rotate(216)"/>
      <ellipse cx="0" cy="-11" rx="6" ry="11" fill="#D9C3C7" opacity="0.92" transform="rotate(288)"/>
      <circle cx="0" cy="0" r="5" fill="#BFA46B"/>
    </g>
  </defs>
  <!-- layer: 底（米色） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#EFE6D8"/>
  </g>
  <!-- layer: 主体（三朵干花 + 细枝） -->
  <g clip-path="url(#nail)">
    <path d="M78 176 C 92 158 100 140 104 118" fill="none" stroke="#A89B84" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M104 118 C 112 132 122 146 130 158" fill="none" stroke="#A89B84" stroke-width="1.6" stroke-linecap="round"/>
    <ellipse cx="94" cy="150" rx="9" ry="4" fill="#C7BBA1" transform="rotate(-40 94 150)"/>
    <ellipse cx="114" cy="138" rx="8" ry="3.6" fill="#C7BBA1" transform="rotate(35 114 138)"/>
    <use href="#dryflower" transform="translate(104 104) scale(1.15)"/>
    <use href="#dryflower" transform="translate(76 168) scale(0.85)"/>
    <use href="#dryflower" transform="translate(132 162) scale(0.8)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="120" cy="88" r="2" fill="#BFA46B" opacity="0.7"/>
    <circle cx="66" cy="140" r="1.6" fill="#BFA46B" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-handpaint-flower-01.svg ｜ N-14 玫瑰/牡丹手绘 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-14 | 名称 手绘主花 | 分类 花卉植物 | 难度 进阶 | 标签 约会/婚礼 -->
  <!-- palette: c-base: #FBF2EC | c-deep: #C0564F | c-mid: #DA8378 | c-light: #EFB3A6 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（暖白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBF2EC"/>
  </g>
  <!-- layer: 主体（手绘玫瑰：同心弧线花瓣） -->
  <g clip-path="url(#nail)" fill="none" stroke-linecap="round">
    <circle cx="100" cy="108" r="44" fill="#EFB3A6" opacity="0.75" stroke="none"/>
    <path d="M100 108 C 118 104 126 90 116 78 C 104 66 84 72 82 90 C 80 108 96 118 110 112" stroke="#C0564F" stroke-width="2.4"/>
    <path d="M100 108 C 90 96 96 82 108 82 C 122 82 128 96 118 105 C 110 112 96 110 92 100" stroke="#DA8378" stroke-width="2.2"/>
    <path d="M100 108 C 108 102 108 92 100 90 C 92 88 86 96 90 103" stroke="#C0564F" stroke-width="2"/>
    <path d="M100 108 C 104 105 104 100 100 99" stroke="#DA8378" stroke-width="2"/>
    <path d="M70 132 C 78 148 92 158 108 158" stroke="#A8BD84" stroke-width="3"/>
    <ellipse cx="74" cy="150" rx="11" ry="5.5" fill="#A8BD84" opacity="0.9" stroke="none" transform="rotate(28 74 150)"/>
    <ellipse cx="126" cy="146" rx="10" ry="5" fill="#A8BD84" opacity="0.9" stroke="none" transform="rotate(-24 126 146)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="122" cy="82" r="3" fill="#C0564F" opacity="0.65"/>
    <circle cx="78" cy="90" r="2.4" fill="#DA8378" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-leaf-01.svg ｜ N-15 植物剪影 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-15 | 名称 植物剪影 | 分类 花卉植物 | 难度 进阶 | 标签 日常 -->
  <!-- palette: c-base: #F6EFE6 | c-silhouette: #6E5748 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F6EFE6"/>
  </g>
  <!-- layer: 主体（叶片剪影） -->
  <g clip-path="url(#nail)" fill="#6E5748">
    <path d="M104 60 C 78 88 76 138 102 168 C 128 138 126 88 104 60 Z"/>
    <path d="M78 132 C 62 148 60 176 76 194 C 92 178 94 150 78 132 Z" opacity="0.85"/>
    <path d="M124 106 C 138 118 140 142 128 158 C 114 146 112 122 124 106 Z" opacity="0.85"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M104 172 L104 206" stroke="#6E5748" stroke-width="3"/>
    <circle cx="104" cy="210" r="3.5" fill="#6E5748"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-heart-01.svg ｜ N-16 心形 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-16 | 名称 心形 | 分类 甜美卡通 | 难度 入门 | 标签 情人节/约会 -->
  <!-- palette: c-base: #FCEEF1 | c-heart: #E8748C | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FCEEF1"/>
  </g>
  <!-- layer: 主体（主心形） -->
  <g clip-path="url(#nail)">
    <path d="M100 96 C 84 72 52 80 52 110 C 52 140 88 160 100 178 C 112 160 148 140 148 110 C 148 80 116 72 100 96 Z" fill="#E8748C"/>
    <ellipse cx="78" cy="100" rx="8" ry="6" fill="#FFF6F8" opacity="0.75" transform="rotate(-24 78 100)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" fill="#E8748C">
    <path d="M132 62 C 128 56 118 58 118 65 C 118 72 127 77 132 81 C 137 77 146 72 146 65 C 146 58 136 56 132 62 Z" opacity="0.8"/>
    <circle cx="68" cy="62" r="4" opacity="0.7"/>
    <circle cx="76" cy="200" r="3.5" opacity="0.65"/>
    <circle cx="128" cy="204" r="3" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-cartoon-01.svg ｜ N-17 卡通形象简笔 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-17 | 名称 卡通形象简笔（兔脸） | 分类 甜美卡通 | 难度 入门 | 标签 日常/学生 -->
  <!-- palette: c-base: #FBF2EC | c-fur: #FFF9F5 | c-detail: #D8BFAE | c-blush: #F5C6C0 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBF2EC"/>
  </g>
  <!-- layer: 主体（兔脸） -->
  <g clip-path="url(#nail)">
    <ellipse cx="84" cy="82" rx="10" ry="26" fill="#FFF9F5" stroke="#D8BFAE" stroke-width="2" transform="rotate(-10 84 82)"/>
    <ellipse cx="84" cy="84" rx="4.5" ry="16" fill="#F5C6C0" transform="rotate(-10 84 84)"/>
    <ellipse cx="116" cy="82" rx="10" ry="26" fill="#FFF9F5" stroke="#D8BFAE" stroke-width="2" transform="rotate(10 116 82)"/>
    <ellipse cx="116" cy="84" rx="4.5" ry="16" fill="#F5C6C0" transform="rotate(10 116 84)"/>
    <circle cx="100" cy="136" r="36" fill="#FFF9F5" stroke="#D8BFAE" stroke-width="2"/>
    <circle cx="87" cy="130" r="3.6" fill="#4A4A4A"/>
    <circle cx="113" cy="130" r="3.6" fill="#4A4A4A"/>
    <ellipse cx="100" cy="142" rx="4" ry="3" fill="#E8A0B4"/>
    <path d="M94 150 Q100 155 106 150" fill="none" stroke="#4A4A4A" stroke-width="2" stroke-linecap="round"/>
    <circle cx="72" cy="146" r="6" fill="#F5C6C0" opacity="0.6"/>
    <circle cx="128" cy="146" r="6" fill="#F5C6C0" opacity="0.6"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="70" cy="192" r="3" fill="#D8BFAE" opacity="0.7"/>
    <circle cx="130" cy="196" r="2.6" fill="#D8BFAE" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-candy-01.svg ｜ N-18 糖果色撞色 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-18 | 名称 糖果色撞色 | 分类 甜美卡通 | 难度 入门 | 标签 派对/学生 -->
  <!-- palette: c-pink: #F5A8C0 | c-yellow: #F6D96A | c-blue: #9CC7E8 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FDF9F6"/>
  </g>
  <!-- layer: 主体（三色斜撞） -->
  <g clip-path="url(#nail)">
    <path d="M40 16 H112 L68 226 H40 Z" fill="#F5A8C0"/>
    <path d="M112 16 H148 L104 226 H68 Z" fill="#F6D96A"/>
    <path d="M148 16 H160 V226 H104 Z" fill="#9CC7E8"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="88" cy="70" r="3" fill="#FFFFFF" opacity="0.8"/>
    <circle cx="120" cy="150" r="3" fill="#FFFFFF" opacity="0.8"/>
    <circle cx="150" cy="100" r="2.6" fill="#FFFFFF" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-paw-01.svg ｜ N-19 猫爪/爪印 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-19 | 名称 猫爪/爪印 | 分类 甜美卡通 | 难度 入门 | 标签 日常 -->
  <!-- palette: c-base: #FCEEE6 | c-paw: #E8A0B4 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FCEEE6"/>
  </g>
  <!-- layer: 主体（爪印） -->
  <g clip-path="url(#nail)" fill="#E8A0B4">
    <ellipse cx="76" cy="112" rx="8" ry="10" transform="rotate(-18 76 112)"/>
    <ellipse cx="94" cy="98" rx="8" ry="10" transform="rotate(-6 94 98)"/>
    <ellipse cx="113" cy="98" rx="8" ry="10" transform="rotate(6 113 98)"/>
    <ellipse cx="131" cy="112" rx="8" ry="10" transform="rotate(18 131 112)"/>
    <path d="M103 128 C 87 128 78 142 82 156 C 85 167 94 171 103 166 C 112 171 121 167 124 156 C 128 142 119 128 103 128 Z"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="70" cy="176" r="3.2" fill="#E8A0B4" opacity="0.65"/>
    <circle cx="130" cy="182" r="2.8" fill="#E8A0B4" opacity="0.55"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-star-01.svg ｜ N-20 星月元素 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-20 | 名称 星月元素 | 分类 甜美卡通 | 难度 入门 | 标签 约会/夜间派对 -->
  <!-- palette: c-base: #F3EFF9 | c-gold: #E5B84B | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F3EFF9"/>
  </g>
  <!-- layer: 主体（主星 + 月牙） -->
  <g clip-path="url(#nail)">
    <path d="M92 78 L102 106.2 L131.9 107 L108.2 125.3 L116.7 154 L92 137 L67.3 154 L75.8 125.3 L52.1 107 L82 106.2 Z" fill="#E5B84B"/>
    <path d="M148 92 A 17 17 0 1 0 148 126 A 13 13 0 1 1 148 92 Z" fill="#E5B84B"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" fill="#E5B84B">
    <path d="M76 186 L79 193 L86 194 L81 199 L82 206 L76 202 L70 206 L71 199 L66 194 L73 193 Z" opacity="0.85"/>
    <circle cx="132" cy="176" r="3.4" opacity="0.8"/>
    <circle cx="142" cy="192" r="2.6" opacity="0.65"/>
    <circle cx="62" cy="62" r="2.8" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-ink-01.svg ｜ N-21 水墨写意风 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-21 | 名称 水墨写意 | 分类 艺术手绘 | 难度 进阶 | 标签 国风/日常 -->
  <!-- palette: c-base: #F4F1EA | c-ink: #2E3438 | c-ink2: #5C666B | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（米白宣纸感） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F4F1EA"/>
  </g>
  <!-- layer: 主体（水墨曲线笔触，粗细渐变） -->
  <g clip-path="url(#nail)" fill="none" stroke-linecap="round">
    <path d="M58 66 C 84 84 116 96 148 92" stroke="#2E3438" stroke-width="7" opacity="0.9"/>
    <path d="M50 108 C 82 120 120 128 152 122" stroke="#2E3438" stroke-width="4.2" opacity="0.82"/>
    <path d="M62 158 C 88 172 116 178 144 172" stroke="#5C666B" stroke-width="2.6" opacity="0.72"/>
    <path d="M150 92 C 156 96 158 102 154 108" stroke="#2E3438" stroke-width="2.4" opacity="0.7"/>
    <circle cx="150" cy="120" r="3.4" fill="#2E3438" opacity="0.55" stroke="none"/>
    <circle cx="140" cy="150" r="2.2" fill="#5C666B" opacity="0.5" stroke="none"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="70" cy="86" r="1.6" fill="#2E3438" opacity="0.4"/>
    <circle cx="96" cy="132" r="1.4" fill="#2E3438" opacity="0.35"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-oil-01.svg ｜ N-22 油画笔触 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-22 | 名称 油画笔触 | 分类 艺术手绘 | 难度 进阶 | 标签 艺术/日常 -->
  <!-- palette: c-base: #F3EFE8 | c-a: #B7A79A | c-b: #9FAE9C | c-c: #C9A9A0 | c-d: #8E9BB0 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（米灰） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F3EFE8"/>
  </g>
  <!-- layer: 主体（莫兰迪厚涂色块拼贴） -->
  <g clip-path="url(#nail)">
    <rect x="54" y="46" width="46" height="52" rx="10" fill="#B7A79A"/>
    <rect x="106" y="62" width="40" height="46" rx="10" fill="#C9A9A0"/>
    <rect x="60" y="108" width="44" height="48" rx="10" fill="#9FAE9C"/>
    <rect x="110" y="118" width="36" height="54" rx="10" fill="#8E9BB0"/>
    <rect x="70" y="164" width="54" height="34" rx="12" fill="#B7A79A" opacity="0.85"/>
    <path d="M66 60 C 76 66 88 66 96 62" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
    <path d="M120 128 C 128 134 138 134 144 130" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.3" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <rect x="126" y="176" width="14" height="14" rx="4" fill="#C9A9A0" opacity="0.7"/>
    <circle cx="150" cy="96" r="3" fill="#9FAE9C" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-abstract-01.svg ｜ N-23 抽象色流 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-23 | 名称 抽象色流 | 分类 艺术手绘 | 难度 进阶 | 标签 潮酷/日常 -->
  <!-- palette: c-base: #F6F4F1 | c-blue: #6C7BC4 | c-purple: #9B7FC1 | c-pink: #E1A0B6 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（浅灰白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F6F4F1"/>
  </g>
  <!-- layer: 主体（蓝紫粉三色流动曲线带交错） -->
  <g clip-path="url(#nail)" fill="none" stroke-linecap="round">
    <path d="M36 72 C 76 38 110 108 164 66" stroke="#6C7BC4" stroke-width="16" opacity="0.78"/>
    <path d="M36 118 C 80 84 104 156 164 112" stroke="#9B7FC1" stroke-width="15" opacity="0.72"/>
    <path d="M36 166 C 78 140 108 196 164 158" stroke="#E1A0B6" stroke-width="14" opacity="0.75"/>
    <path d="M52 62 C 84 44 108 96 150 62" stroke="#FFFFFF" stroke-width="3" opacity="0.3"/>
    <path d="M56 164 C 86 146 108 184 148 158" stroke="#FFFFFF" stroke-width="3" opacity="0.28"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="120" cy="90" r="3.2" fill="#6C7BC4" opacity="0.7"/>
    <circle cx="78" cy="140" r="2.6" fill="#9B7FC1" opacity="0.7"/>
    <circle cx="132" cy="176" r="2.4" fill="#E1A0B6" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-filigree-01.svg ｜ N-24 细密艺术花纹 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-24 | 名称 细密艺术花纹 | 分类 艺术手绘 | 难度 进阶 | 标签 婚礼/宴会 -->
  <!-- palette: c-base: #F7F2EA | c-gold: #C6A15B | c-gold2: #DFC486 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（象牙白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F7F2EA"/>
  </g>
  <!-- layer: 主体（金色细线同心弧 + 小卷草，对称布局） -->
  <g clip-path="url(#nail)" fill="none" stroke-linecap="round">
    <path d="M100 74 A 34 34 0 0 1 100 142" stroke="#C6A15B" stroke-width="1.6"/>
    <path d="M100 74 A 34 34 0 0 0 100 142" stroke="#C6A15B" stroke-width="1.6"/>
    <path d="M100 86 A 22 22 0 0 1 100 130" stroke="#DFC486" stroke-width="1.4"/>
    <path d="M100 86 A 22 22 0 0 0 100 130" stroke="#DFC486" stroke-width="1.4"/>
    <path d="M100 100 A 8 8 0 0 1 100 116" stroke="#C6A15B" stroke-width="1.4"/>
    <path d="M100 100 A 8 8 0 0 0 100 116" stroke="#C6A15B" stroke-width="1.4"/>
    <path d="M66 108 C 58 100 58 88 66 82 C 74 88 74 100 66 108" stroke="#C6A15B" stroke-width="1.3"/>
    <path d="M134 108 C 142 100 142 88 134 82 C 126 88 126 100 134 108" stroke="#C6A15B" stroke-width="1.3"/>
    <path d="M66 82 C 60 76 52 76 48 82" stroke="#DFC486" stroke-width="1.2"/>
    <path d="M134 82 C 140 76 148 76 152 82" stroke="#DFC486" stroke-width="1.2"/>
  </g>
  <!-- layer: 点缀（点阵） -->
  <g id="accent" fill="#C6A15B">
    <circle cx="100" cy="68" r="2.2"/>
    <circle cx="100" cy="148" r="2.2"/>
    <circle cx="46" cy="112" r="1.8" fill="#DFC486"/>
    <circle cx="154" cy="112" r="1.8" fill="#DFC486"/>
    <circle cx="100" cy="160" r="1.6" fill="#DFC486"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-portrait-01.svg ｜ N-25 主题人像手绘 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-25 | 名称 主题人像手绘 | 分类 艺术手绘 | 难度 进阶 | 标签 个性/艺术 -->
  <!-- palette: c-base: #F6F1EA | c-line: #2B2B2B | c-hair: #4A4A4A | c-accent: #C98B7E | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（暖白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F6F1EA"/>
  </g>
  <!-- layer: 主体（女性侧脸简约线稿） -->
  <g clip-path="url(#nail)" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M84 66 C 104 60 122 72 122 92 C 122 104 116 112 108 118 C 104 121 104 126 108 130 C 112 134 110 140 104 142 L104 150 C 112 152 118 158 118 166"/>
    <path d="M84 66 C 68 72 60 90 62 108 C 63 120 60 132 56 142"/>
    <path d="M108 118 C 116 116 122 112 126 106"/>
    <path d="M104 142 C 98 146 92 148 86 148"/>
    <path d="M96 96 C 100 94 106 94 110 96" stroke-width="1.8"/>
    <path d="M74 88 C 82 80 96 78 104 82" stroke="#4A4A4A" stroke-width="2.4"/>
    <path d="M78 70 C 90 62 110 64 118 76" stroke="#4A4A4A" stroke-width="2.4"/>
    <circle cx="98" cy="102" r="1.2" fill="#2B2B2B" stroke="none"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="120" cy="86" r="3" fill="#C98B7E" opacity="0.6"/>
    <path d="M66 160 C 82 166 104 166 122 160" fill="none" stroke="#C98B7E" stroke-width="2" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-catseye-01.svg ｜ N-26 猫眼（磁吸） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-26 | 名称 猫眼（磁吸） | 分类 特效工艺 | 难度 进阶 | 标签 派对/日常 -->
  <!-- palette: c-base: #1E3B33 | c-deep: #14261F | c-glow: #D8B25C | c-hi: #F3E0A6 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="cateye" x1="0.2" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#F3E0A6" stop-opacity="0"/>
      <stop offset="45%" stop-color="#F3E0A6" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#D8B25C" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#D8B25C" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- layer: 底（深墨绿） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#1E3B33"/>
    <ellipse cx="70" cy="190" rx="60" ry="70" fill="#14261F" opacity="0.55"/>
  </g>
  <!-- layer: 主体（中央斜向金色光带） -->
  <g clip-path="url(#nail)">
    <ellipse cx="100" cy="120" rx="82" ry="20" fill="url(#cateye)" transform="rotate(-38 100 120)"/>
    <ellipse cx="100" cy="120" rx="70" ry="7" fill="#F3E0A6" opacity="0.5" transform="rotate(-38 100 120)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" fill="#F3E0A6">
    <circle cx="72" cy="86" r="1.8" opacity="0.75"/>
    <circle cx="128" cy="156" r="1.6" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-smoke-01.svg ｜ N-27 渐变晕染 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-27 | 名称 渐变晕染 | 分类 特效工艺 | 难度 入门 | 标签 日常/通勤 -->
  <!-- palette: c-base: #FBFAF8 | c-a: #E7B6C4 | c-b: #B9C7E0 | c-c: #D8C7A6 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBFAF8"/>
  </g>
  <!-- layer: 主体（三层低透明度色雾叠加） -->
  <g clip-path="url(#nail)">
    <circle cx="76" cy="82" r="46" fill="#E7B6C4" opacity="0.5"/>
    <circle cx="132" cy="128" r="52" fill="#B9C7E0" opacity="0.42"/>
    <circle cx="86" cy="182" r="44" fill="#D8C7A6" opacity="0.4"/>
    <circle cx="120" cy="74" r="30" fill="#E7B6C4" opacity="0.3"/>
    <circle cx="66" cy="140" r="26" fill="#B9C7E0" opacity="0.3"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="124" cy="96" r="3" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="82" cy="118" r="2.4" fill="#FFFFFF" opacity="0.6"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-mirror-01.svg ｜ N-28 镜面/金属光泽 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-28 | 名称 镜面/金属光泽 | 分类 特效工艺 | 难度 进阶 | 标签 派对/潮酷 -->
  <!-- palette: c-from: #B9BEC6 | c-mid: #DDE1E6 | c-to: #9AA0A9 | c-hi: #FFFFFF | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="mirror" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B9BEC6"/>
      <stop offset="45%" stop-color="#DDE1E6"/>
      <stop offset="100%" stop-color="#9AA0A9"/>
    </linearGradient>
  </defs>
  <!-- layer: 底（银灰渐变） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#mirror)"/>
  </g>
  <!-- layer: 主体（斜向高光条） -->
  <g clip-path="url(#nail)">
    <rect x="72" y="8" width="14" height="230" fill="#FFFFFF" opacity="0.6" transform="rotate(-24 100 120)"/>
    <rect x="104" y="8" width="6" height="230" fill="#FFFFFF" opacity="0.4" transform="rotate(-24 100 120)"/>
    <rect x="40" y="8" width="10" height="230" fill="#6E747C" opacity="0.18" transform="rotate(-24 100 120)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="120" cy="70" r="2.6" fill="#FFFFFF" opacity="0.85"/>
    <circle cx="86" cy="180" r="2" fill="#FFFFFF" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-3d-01.svg ｜ N-29 立体雕花 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-29 | 名称 立体雕花 | 分类 特效工艺 | 难度 进阶 | 标签 婚礼/宴会 -->
  <!-- palette: c-base: #F1E7E0 | c-petal: #FFFFFF | c-shade: #C9A9A0 | c-core: #E0B979 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（藕粉） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F1E7E0"/>
  </g>
  <!-- layer: 主体（立体小花：阴影线在花瓣下方表现凸起） -->
  <g clip-path="url(#nail)">
    <ellipse cx="102" cy="130" rx="26" ry="10" fill="#C9A9A0" opacity="0.5"/>
    <g>
      <ellipse cx="100" cy="96" rx="11" ry="20" fill="#FFFFFF"/>
      <ellipse cx="100" cy="96" rx="11" ry="20" fill="#FFFFFF" transform="rotate(72 100 120)"/>
      <ellipse cx="100" cy="96" rx="11" ry="20" fill="#FFFFFF" transform="rotate(144 100 120)"/>
      <ellipse cx="100" cy="96" rx="11" ry="20" fill="#FFFFFF" transform="rotate(216 100 120)"/>
      <ellipse cx="100" cy="96" rx="11" ry="20" fill="#FFFFFF" transform="rotate(288 100 120)"/>
    </g>
    <path d="M86 132 C 92 126 96 122 100 120" fill="none" stroke="#C9A9A0" stroke-width="1.6" opacity="0.8"/>
    <path d="M114 132 C 108 126 104 122 100 120" fill="none" stroke="#C9A9A0" stroke-width="1.6" opacity="0.8"/>
    <circle cx="100" cy="120" r="9" fill="#E0B979"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="128" cy="176" r="4" fill="#FFFFFF" opacity="0.9"/>
    <circle cx="72" cy="172" r="3" fill="#FFFFFF" opacity="0.85"/>
    <circle cx="134" cy="88" r="3" fill="#FFFFFF" opacity="0.8"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-marble-01.svg ｜ N-30 大理石/琥珀纹 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-30 | 名称 大理石/琥珀纹 | 分类 特效工艺 | 难度 进阶 | 标签 高级/日常 -->
  <!-- palette: c-base: #F4EFE6 | c-vein: #9AA0A2 | c-vein2: #C3C7C6 | c-gold: #C9A85E | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（奶白） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F4EFE6"/>
  </g>
  <!-- layer: 主体（灰色裂纹曲线） -->
  <g clip-path="url(#nail)" fill="none" stroke-linecap="round">
    <path d="M44 70 C 70 78 82 62 104 74 C 126 86 140 70 158 80" stroke="#9AA0A2" stroke-width="2" opacity="0.8"/>
    <path d="M46 108 C 74 100 86 124 110 118 C 132 112 144 128 160 120" stroke="#C3C7C6" stroke-width="2.4" opacity="0.75"/>
    <path d="M50 156 C 76 164 90 146 114 156 C 134 164 146 154 158 160" stroke="#9AA0A2" stroke-width="1.8" opacity="0.7"/>
    <path d="M96 62 C 92 84 100 100 96 122" stroke="#C3C7C6" stroke-width="1.4" opacity="0.6"/>
    <path d="M124 74 C 132 96 120 116 128 138" stroke="#C3C7C6" stroke-width="1.4" opacity="0.55"/>
  </g>
  <!-- layer: 点缀（金色细线） -->
  <g id="accent" fill="none" stroke="#C9A85E" stroke-linecap="round">
    <path d="M62 190 C 82 184 100 192 122 186 C 138 182 150 188 160 184" stroke-width="1.4" opacity="0.85"/>
    <path d="M70 44 C 84 40 96 48 112 44" stroke-width="1.2" opacity="0.7"/>
    <circle cx="140" cy="60" r="2" fill="#C9A85E" stroke="none" opacity="0.8"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-newyear-01.svg ｜ N-31 新年红金 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-31 | 名称 新年红金 | 分类 节庆主题 | 难度 入门 | 标签 新年/节庆 -->
  <!-- palette: c-red: #C0392B | c-gold: #E5B84B | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#C0392B"/>
  </g>
  <!-- layer: 主体（金色钱纹） -->
  <g clip-path="url(#nail)" fill="none" stroke="#E5B84B" stroke-width="2.6" stroke-linejoin="round">
    <path d="M100 52 L124 84 L100 116 L76 84 Z"/>
    <path d="M100 84 L110 84 M100 84 L100 98"/>
    <path d="M100 140 L118 164 L100 188 L82 164 Z" stroke-width="2.2"/>
  </g>
  <!-- layer: 点缀（金点） -->
  <g id="accent" fill="#E5B84B">
    <circle cx="62" cy="60" r="3"/>
    <circle cx="140" cy="70" r="2.6"/>
    <circle cx="58" cy="180" r="2.6"/>
    <circle cx="142" cy="196" r="3"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-christmas-01.svg ｜ N-32 圣诞主题 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-32 | 名称 圣诞主题 | 分类 节庆主题 | 难度 入门 | 标签 圣诞/节庆 -->
  <!-- palette: c-green: #2E5E4E | c-white: #FDFBF8 | c-gold: #E5B84B | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#2E5E4E"/>
  </g>
  <!-- layer: 主体（圣诞树） -->
  <g clip-path="url(#nail)">
    <path d="M100 66 L124 102 L76 102 Z" fill="#FDFBF8"/>
    <path d="M100 92 L132 138 L68 138 Z" fill="#FDFBF8"/>
    <rect x="94" y="138" width="12" height="14" fill="#B07040"/>
    <path d="M100 46 L104 56 L114 58 L106 66 L108 76 L100 70 L92 76 L94 66 L86 58 L96 56 Z" fill="#E5B84B"/>
  </g>
  <!-- layer: 点缀（雪花点） -->
  <g id="accent" fill="#FDFBF8">
    <circle cx="62" cy="70" r="2.6" opacity="0.9"/>
    <circle cx="138" cy="86" r="2.2" opacity="0.85"/>
    <circle cx="58" cy="150" r="2.6" opacity="0.9"/>
    <circle cx="144" cy="164" r="2.2" opacity="0.85"/>
    <circle cx="100" cy="186" r="2.6" opacity="0.9"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-valentine-01.svg ｜ N-33 情人节限定 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-33 | 名称 情人节限定 | 分类 节庆主题 | 难度 入门 | 标签 情人节/约会 -->
  <!-- palette: c-base: #FBE4EC | c-heart: #D9536F | c-deep: #B93A56 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBE4EC"/>
  </g>
  <!-- layer: 主体（主爱心） -->
  <g clip-path="url(#nail)">
    <path d="M100 108 C 88 90 62 96 62 120 C 62 142 88 158 100 172 C 112 158 138 142 138 120 C 138 96 112 90 100 108 Z" fill="#D9536F"/>
    <path d="M132 62 C 127 54 114 57 114 66 C 114 76 126 82 132 88 C 138 82 150 76 150 66 C 150 57 137 54 132 62 Z" fill="#D9536F" opacity="0.85"/>
  </g>
  <!-- layer: 点缀（小爱心 + 点） -->
  <g id="accent" fill="#B93A56">
    <circle cx="70" cy="70" r="3" opacity="0.7"/>
    <circle cx="66" cy="186" r="2.6" opacity="0.65"/>
    <circle cx="138" cy="192" r="3" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-bride-01.svg ｜ N-34 新娘甲（婚礼限定） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-34 | 名称 新娘甲（婚礼限定） | 分类 节庆主题 | 难度 进阶 | 标签 婚礼（新娘） -->
  <!-- palette: c-base: #FBF7F2 | c-pearl: #F2EAE0 | c-gold: #C9B8A8 | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBF7F2"/>
  </g>
  <!-- layer: 主体（珍珠 + 蕾丝线） -->
  <g clip-path="url(#nail)">
    <circle cx="100" cy="84" r="11" fill="#F2EAE0" stroke="#D9CCBC" stroke-width="1.5"/>
    <circle cx="96" cy="80" r="3.4" fill="#FFFFFF" opacity="0.9"/>
    <circle cx="76" cy="130" r="7" fill="#F2EAE0" stroke="#D9CCBC" stroke-width="1.4"/>
    <circle cx="124" cy="130" r="7" fill="#F2EAE0" stroke="#D9CCBC" stroke-width="1.4"/>
    <path d="M58 168 Q 68 160 78 168 Q 88 176 98 168 Q 108 160 118 168 Q 128 176 138 168" fill="none" stroke="#C9B8A8" stroke-width="2" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀（小钻） -->
  <g id="accent" fill="#C9B8A8">
    <path d="M100 148 L105 154 L100 160 L95 154 Z" opacity="0.85"/>
    <circle cx="64" cy="74" r="2.4" opacity="0.7"/>
    <circle cx="136" cy="74" r="2.4" opacity="0.7"/>
    <circle cx="100" cy="196" r="2.6" opacity="0.75"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-halloween-01.svg ｜ N-35 万圣节主题 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-35 | 名称 万圣节主题 | 分类 节庆主题 | 难度 入门 | 标签 万圣节/派对 -->
  <!-- palette: c-base: #3A2A3C | c-pumpkin: #E8863A | c-dark: #2A1E2C | c-edge: #E8CDB9（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#3A2A3C"/>
  </g>
  <!-- layer: 主体（南瓜灯） -->
  <g clip-path="url(#nail)">
    <rect x="96" y="86" width="8" height="10" fill="#7A9A5C"/>
    <ellipse cx="100" cy="132" rx="34" ry="28" fill="#E8863A"/>
    <path d="M88 102 C 86 132 86 156 90 158 M112 102 C 114 132 114 156 110 158" fill="none" stroke="#C96A28" stroke-width="2" opacity="0.8"/>
    <path d="M84 124 L94 136 L74 136 Z" fill="#2A1E2C"/>
    <path d="M116 124 L106 136 L126 136 Z" fill="#2A1E2C"/>
    <path d="M82 148 Q 88 142 94 148 Q 100 142 106 148 Q 112 142 118 148" fill="none" stroke="#2A1E2C" stroke-width="2.6" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀（星光点） -->
  <g id="accent" fill="#E8863A">
    <circle cx="64" cy="68" r="2.6" opacity="0.8"/>
    <circle cx="138" cy="76" r="2.2" opacity="0.7"/>
    <circle cx="100" cy="190" r="2.6" opacity="0.75"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-sheer-01.svg ｜ N-36 透明护甲 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-36 | 名称 透明护甲 | 分类 中性男性向 | 难度 入门 | 标签 男性日常/职业受限 -->
  <!-- palette: c-base: #FDFAF7 | c-gloss: #FFFFFF | c-edge: #E5D8CC（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FDFAF7" opacity="0.92"/>
    <rect x="40" y="16" width="120" height="210" fill="none"/>
  </g>
  <!-- layer: 主体（自然高光） -->
  <g clip-path="url(#nail)">
    <ellipse cx="84" cy="76" rx="16" ry="30" fill="#FFFFFF" opacity="0.6"/>
    <path d="M118 60 L140 108" stroke="#FFFFFF" stroke-width="8" opacity="0.35" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E5D8CC" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-minimal-01.svg ｜ N-37 极简黑灰线条 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-37 | 名称 极简黑灰线条 | 分类 中性男性向 | 难度 入门 | 标签 男性日常 -->
  <!-- palette: c-base: #F2F0EE | c-ink: #3A3A3A | c-gray: #8A8A8A | c-edge: #DCD6D0（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F2F0EE"/>
  </g>
  <!-- layer: 主体（极简线条组） -->
  <g clip-path="url(#nail)">
    <path d="M56 92 L144 72" stroke="#3A3A3A" stroke-width="5" stroke-linecap="round"/>
    <path d="M56 132 L144 112" stroke="#3A3A3A" stroke-width="5" stroke-linecap="round" opacity="0.85"/>
    <path d="M56 168 L112 154" stroke="#8A8A8A" stroke-width="3" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="128" cy="192" r="4.5" fill="#3A3A3A"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#DCD6D0" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-matte-01.svg ｜ N-38 哑光纯色（短平） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-38 | 名称 哑光纯色（短平） | 分类 中性男性向 | 难度 入门 | 标签 男性职场 -->
  <!-- palette: c-base: #4A4A4F | c-edge: #3A3A3E（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底（哑光平涂，无高光） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#4A4A4F"/>
  </g>
  <!-- layer: 主体（顶部极淡磨砂过渡） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="26" fill="#55555B" opacity="0.5"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#3A3A3E" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-dotgeo-01.svg ｜ N-39 单点几何点缀 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-39 | 名称 单点几何点缀 | 分类 中性男性向 | 难度 入门 | 标签 男性约会/派对 -->
  <!-- palette: c-base: #F4F1EC | c-dot: #2F3A44 | c-edge: #DCD6D0（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F4F1EC"/>
  </g>
  <!-- layer: 主体（单点几何） -->
  <g clip-path="url(#nail)">
    <circle cx="100" cy="162" r="11" fill="#2F3A44"/>
    <path d="M100 128 L108 142 L92 142 Z" fill="#2F3A44" opacity="0.75"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="100" cy="188" r="3" fill="#2F3A44" opacity="0.5"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#DCD6D0" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-bow-01.svg ｜ N-40 蝴蝶结 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-40 | 名称 蝴蝶结 | 分类 甜美卡通 | 难度 入门 | 标签 约会/派对 -->
  <!-- palette: c-base: #FBE9EF | c-bow: #E899AE | c-deep: #D87F98（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#FBE9EF"/>
  </g>
  <!-- layer: 主体（蝴蝶结） -->
  <g clip-path="url(#nail)">
    <ellipse cx="79" cy="110" rx="17" ry="13" fill="#E899AE" stroke="#D87F98" stroke-width="2" transform="rotate(-16 79 110)"/>
    <ellipse cx="121" cy="110" rx="17" ry="13" fill="#E899AE" stroke="#D87F98" stroke-width="2" transform="rotate(16 121 110)"/>
    <circle cx="100" cy="112" r="7.5" fill="#E899AE" stroke="#D87F98" stroke-width="2"/>
    <path d="M100 119 C 96 134 91 146 83 156" fill="none" stroke="#D87F98" stroke-width="3.2" stroke-linecap="round"/>
    <path d="M100 119 C 104 134 109 146 117 156" fill="none" stroke="#D87F98" stroke-width="3.2" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <circle cx="66" cy="176" r="3" fill="#D87F98" opacity="0.65"/>
    <circle cx="136" cy="184" r="2.6" fill="#D87F98" opacity="0.55"/>
    <path d="M130 66 L134 72 L140 73 L135 78 L136 84 L130 81 L124 84 L125 78 L120 73 L126 72 Z" fill="#E899AE" opacity="0.7"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-cloud-01.svg ｜ N-41 祥云纹（国风） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-41 | 名称 祥云纹 | 分类 艺术手绘（国风） | 难度 进阶 | 标签 新中式/节庆 -->
  <!-- palette: c-base: #F6F4EC | c-cloud: #E3D5B8 | c-line: #B8A88C（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#F6F4EC"/>
  </g>
  <!-- layer: 主体（祥云） -->
  <g clip-path="url(#nail)">
    <path d="M64 138 C 58 124 68 112 82 114 C 84 102 100 96 108 106 C 114 96 130 96 134 108 C 146 106 154 116 150 128 C 160 132 160 144 150 148 L72 150 C 62 148 58 144 64 138 Z" fill="#E3D5B8" stroke="#B8A88C" stroke-width="2"/>
    <path d="M82 130 C 84 122 94 120 98 126" fill="none" stroke="#B8A88C" stroke-width="2" stroke-linecap="round"/>
    <path d="M108 122 C 110 114 120 112 124 118" fill="none" stroke="#B8A88C" stroke-width="2" stroke-linecap="round"/>
  </g>
  <!-- layer: 点缀（小云朵 + 云尾） -->
  <g id="accent">
    <path d="M92 176 C 90 168 98 162 106 166 C 110 160 120 162 120 170 C 128 170 130 178 124 182 L98 182 C 93 182 90 179 92 176 Z" fill="#EDE2C8" stroke="#C9BBA0" stroke-width="1.8"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-leopard-01.svg ｜ N-42 豹纹 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-42 | 名称 豹纹 | 分类 几何图形（时尚纹理） | 难度 进阶 | 标签 个性/秋冬 -->
  <!-- palette: c-base: #E8C9A8 | c-ring: #8E5A3B | c-inner: #F2E2D0（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#E8C9A8"/>
  </g>
  <!-- layer: 主体（豹纹斑，环形） -->
  <g clip-path="url(#nail)" stroke="#8E5A3B" stroke-width="4" fill="#F2E2D0">
    <ellipse cx="72" cy="72" rx="12" ry="9" transform="rotate(-18 72 72)"/>
    <ellipse cx="116" cy="62" rx="10" ry="8" transform="rotate(24 116 62)"/>
    <ellipse cx="146" cy="94" rx="11" ry="8" transform="rotate(-30 146 94)"/>
    <ellipse cx="86" cy="112" rx="12" ry="9" transform="rotate(12 86 112)"/>
    <ellipse cx="128" cy="122" rx="10" ry="8" transform="rotate(-14 128 122)"/>
    <ellipse cx="62" cy="152" rx="11" ry="8" transform="rotate(28 62 152)"/>
    <ellipse cx="104" cy="156" rx="12" ry="9" transform="rotate(-20 104 156)"/>
    <ellipse cx="142" cy="158" rx="9" ry="7" transform="rotate(16 142 158)"/>
    <ellipse cx="80" cy="196" rx="11" ry="8" transform="rotate(-24 80 196)"/>
    <ellipse cx="126" cy="200" rx="10" ry="8" transform="rotate(20 126 200)"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent" fill="#8E5A3B" opacity="0.55">
    <circle cx="100" cy="88" r="2.6"/>
    <circle cx="52" cy="106" r="2.2"/>
    <circle cx="156" cy="128" r="2.2"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-gradient-01.svg ｜ N-43 渐变底 -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-43 | 名称 渐变底（珊瑚粉系） | 分类 特效工艺 | 难度 入门 | 标签 日常/婚礼 -->
  <!-- palette: c-from: #F08A7D | c-to: #F8D3DC | c-gloss: #FFFFFF（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
    <linearGradient id="ombre" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="#F08A7D"/>
      <stop offset="100%" stop-color="#F8D3DC"/>
    </linearGradient>
  </defs>
  <!-- layer: 底（渐变） -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="url(#ombre)"/>
  </g>
  <!-- layer: 主体（柔光过渡） -->
  <g clip-path="url(#nail)">
    <ellipse cx="88" cy="72" rx="20" ry="32" fill="#FFFFFF" opacity="0.28"/>
    <ellipse cx="126" cy="170" rx="26" ry="40" fill="#FFFFFF" opacity="0.14"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent"></g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
<!-- seed: SS-nail-elegant-01.svg ｜ N-44 熟龄优雅款（低饱和 / 细边） -->
<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 N-44 | 名称 熟龄优雅款（低饱和 / 细边） | 分类 简约风格 | 难度 入门 | 标签 熟龄/职场 -->
  <!-- palette: c-base: #E8DCD2 | c-edge: #C9B8A8 | c-accent: #B8935A（运行时按诊断色系替换） -->
  <defs>
    <clipPath id="nail">
      <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z"/>
    </clipPath>
  </defs>
  <!-- layer: 底 -->
  <g clip-path="url(#nail)">
    <rect x="40" y="16" width="120" height="210" fill="#E8DCD2"/>
  </g>
  <!-- layer: 主体（内缩细边） -->
  <g clip-path="url(#nail)">
    <path d="M100 28 C 60 28 50 58 50 100 L50 170 C 50 202 72 216 100 216 C 128 216 150 202 150 170 L150 100 C 150 58 140 28 100 28 Z"
          fill="none" stroke="#C9B8A8" stroke-width="1.6"/>
  </g>
  <!-- layer: 点缀（金箔小点） -->
  <g id="accent">
    <rect x="86" y="106" width="5" height="5" fill="#B8935A" opacity="0.85" transform="rotate(20 88 108)"/>
    <rect x="108" y="128" width="4" height="4" fill="#B8935A" opacity="0.7" transform="rotate(-14 110 130)"/>
  </g>
  <!-- 甲片轮廓 -->
  <path d="M100 16 C 52 16 40 52 40 100 L40 172 C 40 208 66 226 100 226 C 134 226 160 208 160 172 L160 100 C 160 52 148 16 100 16 Z" fill="none" stroke="#E8CDB9" stroke-width="2"/>
</svg>
