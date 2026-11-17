<!-- ============================================================
  styling-studio SVG 种子包 · 妆容（M）
  种子数：20 ｜ 所属组：穿搭造型组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-makeup-lip-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-makeup-lip-01.svg ｜ M-01 日常清透妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-01 | 名称 唇妆色卡（主唇形 + 三试色） | 分类 妆容 | 难度 入门 | 标签 妆面元素 -->
  <!-- palette: c-lip: #C96A6A | c-t1: #D98C8C | c-t2: #B4453F | c-t3: #8E3B4A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（唇形 + 试色三圆） -->
  <g id="subject">
    <path d="M58 104 C 72 90 88 94 100 101 C 112 94 128 90 142 104 C 134 124 116 134 100 134 C 84 134 66 124 58 104 Z"
          fill="#C96A6A" stroke="#A85252" stroke-width="2"/>
    <path d="M100 101 L100 118" fill="none" stroke="#A85252" stroke-width="1.6" opacity="0.75"/>
    <circle cx="76" cy="158" r="12" fill="#D98C8C"/>
    <circle cx="106" cy="158" r="12" fill="#B4453F"/>
    <circle cx="136" cy="158" r="12" fill="#8E3B4A"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <text x="100" y="42" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#8A5A52">唇色试色 · 由浅至深</text>
  </g>
</svg>
<!-- seed: SS-makeup-work-01.svg ｜ M-02 职场妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-02 | 名称 职场妆 | 分类 妆容·场合 | 难度 入门 | 标签 淡眉淡唇 -->
  <!-- palette: c-a: #3A3A3A | c-b: #A85F4E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（淡唇与标注点） -->
  <g id="accent">
    <path d="M86 134 C 93 129 107 129 114 134 C 107 140 93 140 86 134 Z" fill="#A85F4E" stroke="#A85F4E" stroke-width="2.2" opacity="0.55"/>
    <circle cx="84" cy="81" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="116" cy="81" r="2.6" fill="#A85F4E" opacity="0.6"/>
    <circle cx="100" cy="141" r="2.6" fill="#A85F4E" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-nude-01.svg ｜ M-03 清透裸妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-03 | 名称 清透裸妆 | 分类 妆容·场合 | 难度 入门 | 标签 裸妆 清透 -->
  <!-- palette: c-a: #3A3A3A | c-b: #C9A0A8（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（极淡妆面虚线区与标注点） -->
  <g id="accent" fill="none" stroke="#C9A0A8" stroke-width="2.2" stroke-dasharray="4 4">
    <ellipse cx="100" cy="96" rx="30" ry="12"/>
    <ellipse cx="74" cy="114" rx="15" ry="9" transform="rotate(-12 74 114)"/>
    <ellipse cx="126" cy="114" rx="15" ry="9" transform="rotate(12 126 114)"/>
    <ellipse cx="100" cy="134" rx="18" ry="8"/>
  </g>
  <g fill="#C9A0A8" opacity="0.7">
    <circle cx="100" cy="60" r="2.6"/>
    <circle cx="100" cy="152" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-date-01.svg ｜ M-04 约会妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-04 | 名称 约会妆 | 分类 妆容·场合 | 难度 入门 | 标签 粉腮红 甜感 -->
  <!-- palette: c-a: #3A3A3A | c-b: #E8748C（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（粉腮红区与心形小点） -->
  <g id="accent">
    <ellipse cx="76" cy="116" rx="15" ry="10" transform="rotate(-12 76 116)" fill="#E8748C" opacity="0.38"/>
    <ellipse cx="124" cy="116" rx="15" ry="10" transform="rotate(12 124 116)" fill="#E8748C" opacity="0.38"/>
    <path d="M160 92 C 152 84 150 76 155 74 C 158 72 160 77 160 77 C 160 77 162 72 165 74 C 170 76 168 84 160 92 Z" fill="#E8748C" opacity="0.7"/>
    <circle cx="100" cy="139" r="2.6" fill="#E8748C" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-gala-01.svg ｜ M-05 晚宴妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-05 | 名称 晚宴妆 | 分类 妆容·场合 | 难度 进阶 | 标签 深色眼影 -->
  <!-- palette: c-a: #3A3A3A | c-b: #5A4A6A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（深色眼影区域块与深唇） -->
  <g id="accent">
    <path d="M66 92 C 74 82 90 82 98 92 C 90 99 74 99 66 92 Z" fill="#5A4A6A" opacity="0.5"/>
    <path d="M102 92 C 110 82 126 82 134 92 C 126 99 110 99 102 92 Z" fill="#5A4A6A" opacity="0.5"/>
    <path d="M86 135 C 93 130 107 130 114 135 C 107 142 93 142 86 135 Z" fill="#5A4A6A" opacity="0.6"/>
    <circle cx="100" cy="62" r="2.6" fill="#5A4A6A" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-stage-01.svg ｜ M-06 舞台妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-06 | 名称 舞台妆 | 分类 妆容·场合 | 难度 进阶 | 标签 轮廓夸张 -->
  <!-- palette: c-a: #3A3A3A | c-b: #A85F4E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（轮廓夸张标注线与标记点） -->
  <g id="accent" fill="none" stroke="#A85F4E" stroke-linecap="round">
    <path d="M44 78 C 30 96 30 118 44 138" stroke-width="2.4" stroke-dasharray="5 4"/>
    <path d="M156 78 C 170 96 170 118 156 138" stroke-width="2.4" stroke-dasharray="5 4"/>
    <path d="M62 118 L86 111" stroke-width="3"/>
    <path d="M138 118 L114 111" stroke-width="3"/>
    <path d="M86 135 C 93 130 107 130 114 135 C 107 142 93 142 86 135 Z" stroke-width="2.4"/>
  </g>
  <g fill="#A85F4E" opacity="0.65">
    <circle cx="34" cy="108" r="2.8"/>
    <circle cx="166" cy="108" r="2.8"/>
    <circle cx="100" cy="56" r="2.8"/>
  </g>
</svg>
<!-- seed: SS-makeup-bride-01.svg ｜ M-07 新娘妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-07 | 名称 新娘妆 | 分类 妆容·场合 | 难度 进阶 | 标签 花冠 柔色 -->
  <!-- palette: c-a: #3A3A3A | c-b: #D8A0B0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（花冠线条与柔色标注点） -->
  <g id="accent" fill="none" stroke="#D8A0B0">
    <path d="M62 60 C 80 40 120 40 138 60" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="72" cy="58" r="6" stroke-width="2.2"/>
    <circle cx="88" cy="48" r="6" stroke-width="2.2"/>
    <circle cx="100" cy="44" r="6" stroke-width="2.2"/>
    <circle cx="112" cy="48" r="6" stroke-width="2.2"/>
    <circle cx="128" cy="58" r="6" stroke-width="2.2"/>
  </g>
  <g fill="#D8A0B0" opacity="0.7">
    <circle cx="72" cy="58" r="2"/>
    <circle cx="88" cy="48" r="2"/>
    <circle cx="100" cy="44" r="2"/>
    <circle cx="112" cy="48" r="2"/>
    <circle cx="128" cy="58" r="2"/>
  </g>
</svg>
<!-- seed: SS-makeup-menbow-01.svg ｜ M-08 男士眉部修整 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-08 | 名称 男士眉部修整 | 分类 妆容·男士 | 难度 入门 | 标签 眉形 修型 -->
  <!-- palette: c-a: #3A3A3A | c-b: #6B7A8A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（眉形线条） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="5" stroke-linecap="round">
    <path d="M34 100 C 50 84 78 84 94 100"/>
    <path d="M106 100 C 122 84 150 84 166 100"/>
  </g>
  <!-- layer: 点缀（修型虚线框与标记点） -->
  <g id="accent" fill="none" stroke="#6B7A8A" stroke-width="2.2" stroke-dasharray="5 4">
    <rect x="28" y="74" width="72" height="36" rx="6"/>
    <rect x="100" y="74" width="72" height="36" rx="6"/>
  </g>
  <g fill="#6B7A8A" opacity="0.6">
    <circle cx="64" cy="140" r="2.8"/>
    <circle cx="136" cy="140" r="2.8"/>
    <circle cx="100" cy="140" r="2.8"/>
  </g>
</svg>
<!-- seed: SS-makeup-menskin-01.svg ｜ M-09 男士肤色均匀 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-09 | 名称 男士肤色均匀 | 分类 妆容·男士 | 难度 入门 | 标签 匀色 素色 -->
  <!-- palette: c-a: #3A3A3A | c-b: #E3C9B0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（男士面部线稿与均匀肤色色块） -->
  <g id="subject">
    <path d="M100 46 C 74 46 62 66 62 96 C 62 118 72 140 88 150 C 94 154 106 154 112 150 C 128 140 138 118 138 96 C 138 66 126 46 100 46 Z" fill="#E3C9B0" stroke="#3A3A3A" stroke-width="2.6" stroke-linejoin="round"/>
    <g fill="none" stroke="#3A3A3A" stroke-width="2.4" stroke-linecap="round">
      <path d="M74 86 C 82 82 90 82 96 86"/>
      <path d="M104 86 C 110 82 118 82 126 86"/>
      <path d="M76 100 C 83 96 89 96 96 100"/>
      <path d="M104 100 C 111 96 117 96 124 100"/>
      <path d="M100 108 L100 122"/>
      <path d="M94 134 C 98 138 102 138 106 134"/>
    </g>
  </g>
  <!-- layer: 点缀（匀色标记点） -->
  <g id="accent" fill="none" stroke="#E3C9B0" stroke-width="2.2" stroke-dasharray="4 4">
    <ellipse cx="76" cy="112" rx="13" ry="9" transform="rotate(-12 76 112)"/>
    <ellipse cx="124" cy="112" rx="13" ry="9" transform="rotate(12 124 112)"/>
  </g>
  <g fill="#3A3A3A" opacity="0.55">
    <circle cx="100" cy="164" r="2.6"/>
    <circle cx="100" cy="178" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-elements-01.svg ｜ M-10 妆面元素速查 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-10 | 名称 妆面元素速查（四区标注） | 分类 妆容·元素 | 难度 入门 | 标签 全场合 -->
  <!-- palette: c-line: #3A3A3A | c-mark: #C9748A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸轮廓 + 四区虚线标记） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.4">
    <ellipse cx="92" cy="102" rx="42" ry="54"/>
    <path d="M74 84 C 80 80 86 80 90 84" stroke-width="2.6" stroke="#C9748A"/>
    <path d="M94 84 C 98 80 104 80 110 84" stroke-width="2.6" stroke="#C9748A"/>
    <ellipse cx="82" cy="96" rx="7" ry="4" stroke="#C9748A" stroke-width="1.8" stroke-dasharray="3 3"/>
    <ellipse cx="102" cy="96" rx="7" ry="4" stroke="#C9748A" stroke-width="1.8" stroke-dasharray="3 3"/>
    <circle cx="68" cy="112" r="9" stroke="#C9748A" stroke-width="1.8" stroke-dasharray="3 3"/>
    <ellipse cx="92" cy="130" rx="10" ry="5" stroke="#C9748A" stroke-width="1.8" stroke-dasharray="3 3"/>
  </g>
  <!-- layer: 点缀（引线与标点） -->
  <g id="accent" fill="none" stroke="#C9748A" stroke-width="1.6" stroke-linecap="round">
    <path d="M110 84 L150 72"/>
    <path d="M102 96 L152 96"/>
    <path d="M77 112 L150 120"/>
    <path d="M102 130 L152 144"/>
  </g>
  <g fill="#C9748A">
    <circle cx="155" cy="70" r="3.6"/>
    <circle cx="157" cy="96" r="3.6"/>
    <circle cx="155" cy="121" r="3.6"/>
    <circle cx="157" cy="146" r="3.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-base-01.svg ｜ M-11 底妆选色（诊断联动） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-11 | 名称 底妆选色卡（三肤色 + 贴合对比） | 分类 妆容·底妆 | 难度 入门 | 标签 诊断联动 -->
  <!-- palette: c-s1: #F2D8C4 | c-s2: #E2BC9C | c-s3: #C89B72 | c-line: #D9BFA8（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三档肤色圆 + 内环） -->
  <g id="subject">
    <circle cx="52" cy="70" r="26" fill="#F2D8C4"/>
    <circle cx="100" cy="70" r="26" fill="#E2BC9C"/>
    <circle cx="148" cy="70" r="26" fill="#C89B72"/>
    <circle cx="52" cy="70" r="12" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
    <circle cx="100" cy="70" r="12" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
    <circle cx="148" cy="70" r="12" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
  </g>
  <!-- layer: 点缀（贴合对比区 + 对勾） -->
  <g id="accent">
    <rect x="36" y="118" width="128" height="44" rx="10" fill="none" stroke="#D9BFA8" stroke-width="2"/>
    <ellipse cx="72" cy="140" rx="20" ry="12" fill="#E2BC9C"/>
    <ellipse cx="128" cy="140" rx="20" ry="12" fill="#F6E3D6" opacity="0.9"/>
    <path d="M92 140 L98 146 L112 130" fill="none" stroke="#7A9A6B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>
<!-- seed: SS-makeup-brow-01.svg ｜ M-12 眉形设计（脸型联动） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-12 | 名称 眉形三型（平眉 / 标准眉 / 挑眉） | 分类 妆容·眉形 | 难度 入门 | 标签 脸型联动 -->
  <!-- palette: c-line: #5A4A3E | c-accent: #B07040（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三条眉形线） -->
  <g id="subject" fill="none" stroke="#5A4A3E" stroke-linecap="round">
    <path d="M38 62 C 58 54 80 54 96 62" stroke-width="5"/>
    <path d="M104 62 C 116 58 128 58 138 62" stroke-width="4"/>
    <path d="M38 118 C 58 106 80 104 96 112" stroke-width="5"/>
    <path d="M104 112 C 116 106 128 106 138 112" stroke-width="4"/>
    <path d="M38 174 C 58 154 78 148 96 156" stroke-width="5"/>
    <path d="M104 156 C 116 148 128 146 138 152" stroke-width="4"/>
  </g>
  <!-- layer: 点缀（眉峰标注点） -->
  <g id="accent" fill="#B07040">
    <circle cx="70" cy="55" r="2.6" opacity="0.7"/>
    <circle cx="70" cy="106" r="2.6" opacity="0.7"/>
    <circle cx="70" cy="152" r="2.6" opacity="0.7"/>
  </g>
</svg>
<!-- seed: SS-makeup-eye-01.svg ｜ M-13 眼妆 · 自然放大 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-13 | 名称 眼妆范围示意（眼影区 + 眼线） | 分类 妆容·眼妆 | 难度 入门 | 标签 自然放大 -->
  <!-- palette: c-line: #3A3A3A | c-shadow: #C3A8D9 | c-liner: #2B2320（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（眼影范围 + 眼形） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="3" stroke-linecap="round">
    <path d="M44 116 C 72 92 128 92 156 116"/>
    <path d="M50 116 C 78 136 122 136 150 116"/>
    <circle cx="100" cy="112" r="13" stroke-width="2.5"/>
    <circle cx="100" cy="112" r="5.5" fill="#3A3A3A" stroke="none"/>
    <circle cx="105" cy="107" r="2.4" fill="#FFFFFF" stroke="none"/>
  </g>
  <!-- layer: 点缀（眼影范围虚线 + 眼线加粗） -->
  <g id="accent">
    <path d="M48 102 C 70 72 130 72 152 102" fill="none" stroke="#C3A8D9" stroke-width="2.2" stroke-dasharray="5 4"/>
    <path d="M58 106 C 76 86 124 86 142 106" fill="none" stroke="#C3A8D9" stroke-width="2" stroke-dasharray="3 4" opacity="0.8"/>
    <path d="M46 114 C 74 92 126 92 154 114" fill="none" stroke="#2B2320" stroke-width="4" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-makeup-eye-stage-01.svg ｜ M-14 眼妆 · 舞台放大 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-14 | 名称 舞台眼妆放大 | 分类 妆容·眼妆 | 难度 进阶 | 标签 眼部特写 浓眼影 -->
  <!-- palette: c-a: #3A3A3A | c-b: #5A4A6A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（眼部特写线稿） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-linecap="round">
    <path d="M44 112 C 68 88 116 88 140 112 C 116 132 68 132 44 112 Z" stroke-width="2.8" stroke-linejoin="round"/>
    <circle cx="90" cy="111" r="16" stroke-width="2.4"/>
    <circle cx="90" cy="111" r="7" fill="#3A3A3A" stroke="none"/>
    <path d="M46 78 C 70 62 114 62 138 78" stroke-width="4"/>
    <path d="M138 108 L150 102" stroke-width="2.2"/>
    <path d="M140 114 L153 112" stroke-width="2.2"/>
  </g>
  <!-- layer: 点缀（浓眼影大区域虚线与标记点） -->
  <g id="accent">
    <path d="M42 104 C 66 74 118 74 142 104 C 118 86 66 86 42 104 Z" fill="#5A4A6A" opacity="0.22" stroke="#5A4A6A" stroke-width="2.4" stroke-dasharray="5 4" stroke-linejoin="round"/>
    <circle cx="100" cy="158" r="2.8" fill="#5A4A6A" opacity="0.65"/>
    <circle cx="100" cy="174" r="2.8" fill="#5A4A6A" opacity="0.65"/>
  </g>
</svg>
<!-- seed: SS-makeup-blush-01.svg ｜ M-15 腮红位置学 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-15 | 名称 腮红位置示意（三区 + 方向） | 分类 妆容·腮红 | 难度 入门 | 标签 位置学 -->
  <!-- palette: c-face: #3A3A3A | c-blush: #E8748C（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸轮廓 + 左脸三处腮红区） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <ellipse cx="74" cy="122" rx="13" ry="8" stroke="#E8748C" stroke-width="2.2" stroke-dasharray="4 4" transform="rotate(-14 74 122)"/>
    <ellipse cx="76" cy="102" rx="14" ry="7" stroke="#E8748C" stroke-width="2.2" stroke-dasharray="4 4" transform="rotate(-8 76 102)"/>
    <ellipse cx="70" cy="84" rx="11" ry="7" stroke="#E8748C" stroke-width="2.2" stroke-dasharray="4 4" transform="rotate(-26 70 84)"/>
  </g>
  <!-- layer: 点缀（右脸方向箭头 + 标注点） -->
  <g id="accent" fill="none" stroke="#E8748C" stroke-width="2.4" stroke-linecap="round">
    <path d="M118 122 C 126 112 128 100 126 90"/>
    <path d="M120 96 L126 86 L131 95"/>
  </g>
  <g fill="#E8748C" opacity="0.65">
    <circle cx="156" cy="70" r="2.4"/>
    <circle cx="156" cy="84" r="2.4"/>
    <circle cx="156" cy="98" r="2.4"/>
  </g>
</svg>
<!-- seed: SS-makeup-lipline-01.svg ｜ M-16 唇形修饰 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-16 | 名称 唇形修饰 | 分类 妆容·唇妆 | 难度 进阶 | 标签 唇线 描边 -->
  <!-- palette: c-a: #3A3A3A | c-b: #C05A6E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（唇形） -->
  <g id="subject">
    <path d="M58 104 C 74 88 90 96 100 102 C 110 96 126 88 142 104 C 126 122 110 130 100 132 C 90 130 74 122 58 104 Z" fill="#C05A6E" fill-opacity="0.35" stroke="#3A3A3A" stroke-width="2.6" stroke-linejoin="round"/>
  </g>
  <!-- layer: 点缀（唇线描边对比虚线与标记点） -->
  <g id="accent" fill="none" stroke="#C05A6E" stroke-width="2.4" stroke-dasharray="5 4" stroke-linejoin="round">
    <path d="M54 102 C 72 82 90 90 100 96 C 110 90 128 82 146 102 C 128 128 110 136 100 138 C 90 136 72 128 54 102 Z"/>
  </g>
  <g fill="#C05A6E" opacity="0.65">
    <circle cx="100" cy="62" r="2.8"/>
    <circle cx="100" cy="156" r="2.8"/>
    <circle cx="100" cy="172" r="2.8"/>
  </g>
</svg>
<!-- seed: SS-makeup-contour-01.svg ｜ M-17 修容入门 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-17 | 名称 修容入门 | 分类 妆容·修容 | 难度 入门 | 标签 阴影区 下颌 -->
  <!-- palette: c-a: #3A3A3A | c-b: #B08A6E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <ellipse cx="100" cy="103" rx="46" ry="58"/>
    <path d="M72 84 C 80 79 90 79 96 84"/>
    <path d="M104 84 C 110 79 120 79 128 84"/>
    <path d="M74 98 C 81 94 89 94 96 98"/>
    <path d="M104 98 C 111 94 119 94 126 98"/>
    <path d="M100 106 L100 120"/>
    <path d="M95 122 C 99 126 101 126 105 122"/>
  </g>
  <!-- layer: 点缀（两侧与下颌阴影区域标注） -->
  <g id="accent" fill="none" stroke="#B08A6E" stroke-width="2.4" stroke-dasharray="5 4" stroke-linecap="round">
    <path d="M58 90 C 50 110 54 128 68 142"/>
    <path d="M142 90 C 150 110 146 128 132 142"/>
    <path d="M72 138 C 84 152 116 152 128 138"/>
  </g>
  <g fill="#B08A6E" opacity="0.65">
    <circle cx="46" cy="88" r="2.8"/>
    <circle cx="154" cy="88" r="2.8"/>
    <circle cx="100" cy="162" r="2.8"/>
  </g>
</svg>
<!-- seed: SS-makeup-set-01.svg ｜ M-18 定妆与补妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-18 | 名称 定妆与补妆 | 分类 妆容·底妆 | 难度 入门 | 标签 定妆 粉扑 -->
  <!-- palette: c-a: #3A3A3A | c-b: #A8B8C8（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（面部线稿与五官） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.4" stroke-linecap="round" opacity="0.85">
    <ellipse cx="86" cy="100" rx="42" ry="54"/>
    <path d="M60 82 C 68 77 76 77 82 82"/>
    <path d="M90 82 C 96 77 104 77 112 82"/>
    <path d="M62 96 C 69 92 76 92 82 96"/>
    <path d="M90 96 C 97 92 104 92 111 96"/>
    <path d="M86 104 L86 118"/>
    <path d="M88 130 C 92 134 96 134 100 130"/>
  </g>
  <!-- layer: 点缀（粉扑圆形与小喷雾点） -->
  <g id="accent">
    <circle cx="146" cy="146" r="22" fill="#A8B8C8" opacity="0.3" stroke="#A8B8C8" stroke-width="2.6"/>
    <circle cx="146" cy="146" r="14" fill="none" stroke="#A8B8C8" stroke-width="2.2" stroke-dasharray="5 4"/>
  </g>
  <g fill="#A8B8C8">
    <circle cx="42" cy="52" r="2.6" opacity="0.75"/>
    <circle cx="54" cy="42" r="2.2" opacity="0.6"/>
    <circle cx="34" cy="66" r="2.2" opacity="0.6"/>
    <circle cx="60" cy="34" r="2" opacity="0.5"/>
  </g>
</svg>
<!-- seed: SS-makeup-menbase-01.svg ｜ M-19 男士 · 自然底妆 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-19 | 名称 男士自然底妆 | 分类 妆容·男士 | 难度 入门 | 标签 薄底 自然 -->
  <!-- palette: c-a: #3A3A3A | c-b: #E3C9B0（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFFBF9" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（男士面部线稿与薄底匀色示意） -->
  <g id="subject">
    <path d="M100 46 C 74 46 62 66 62 96 C 62 118 72 140 88 150 C 94 154 106 154 112 150 C 128 140 138 118 138 96 C 138 66 126 46 100 46 Z" fill="#E3C9B0" fill-opacity="0.55" stroke="#3A3A3A" stroke-width="2.6" stroke-linejoin="round"/>
    <g fill="none" stroke="#3A3A3A" stroke-width="2.4" stroke-linecap="round">
      <path d="M74 86 C 82 82 90 82 96 86"/>
      <path d="M104 86 C 110 82 118 82 126 86"/>
      <path d="M76 100 C 83 96 89 96 96 100"/>
      <path d="M104 100 C 111 96 117 96 124 100"/>
      <path d="M100 108 L100 122"/>
      <path d="M94 134 C 98 138 102 138 106 134"/>
    </g>
  </g>
  <!-- layer: 点缀（薄底匀色虚线标记） -->
  <g id="accent" fill="none" stroke="#E3C9B0" stroke-width="2.4" stroke-dasharray="5 4">
    <path d="M74 62 C 86 54 114 54 126 62"/>
    <ellipse cx="100" cy="104" rx="34" ry="42"/>
  </g>
  <g fill="#3A3A3A" opacity="0.55">
    <circle cx="100" cy="164" r="2.6"/>
    <circle cx="100" cy="178" r="2.6"/>
  </g>
</svg>
<!-- seed: SS-makeup-prep-01.svg ｜ M-20 妆前皮肤准备 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 M-20 | 名称 妆前皮肤准备（三步） | 分类 妆容·打底 | 难度 入门 | 标签 全场合 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三步徽章） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <circle cx="52" cy="100" r="24"/>
    <circle cx="100" cy="100" r="24"/>
    <circle cx="148" cy="100" r="24"/>
    <path d="M76 100 L78 100 M124 100 L126 100" stroke-width="2.4"/>
    <path d="M78 96 L82 100 L78 104" stroke-width="2"/>
    <path d="M126 96 L130 100 L126 104" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（清洁滴 / 保湿 / 防护盾） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2.2" stroke-linecap="round">
    <path d="M52 88 C 46 96 44 100 44 104 C 44 109 47.5 112 52 112 C 56.5 112 60 109 60 104 C 60 100 58 96 52 88 Z"/>
    <circle cx="96" cy="106" r="4"/>
    <circle cx="104" cy="98" r="3"/>
    <path d="M148 90 L156 94 L156 104 C 156 111 148 116 148 116 C 148 116 140 111 140 104 L140 94 Z"/>
    <path d="M143 103 L147 107 L154 98"/>
  </g>
</svg>
