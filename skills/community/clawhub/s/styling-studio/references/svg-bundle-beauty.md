<!-- ============================================================
  styling-studio SVG 种子包 · 美容（S）
  种子数：13 ｜ 所属组：流程样式组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-skin-routine-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-skin-routine-01.svg ｜ S-01 清洁流程（含步骤卡） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-01 | 名称 护肤步骤流程卡（五步） | 分类 美容·流程 | 难度 入门 | 标签 日常护理 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（五步流程） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <circle cx="70" cy="32" r="13"/>
    <circle cx="70" cy="68" r="13"/>
    <circle cx="70" cy="104" r="13"/>
    <circle cx="70" cy="140" r="13"/>
    <circle cx="70" cy="176" r="13"/>
    <path d="M70 45 L70 55"/>
    <path d="M70 81 L70 91"/>
    <path d="M70 117 L70 127"/>
    <path d="M70 153 L70 163"/>
  </g>
  <!-- layer: 点缀（步骤序列线 + 图标） -->
  <g id="accent" stroke="#7A8E96" stroke-width="2" opacity="0.35" stroke-linecap="round">
    <path d="M92 32 L150 32"/>
    <path d="M92 68 L136 68"/>
    <path d="M92 104 L144 104"/>
    <path d="M92 140 L130 140"/>
    <path d="M92 176 L146 176"/>
  </g>
  <g id="icons" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M70 25 C 67 30 66 32.5 66 34.5 C 66 37 67.8 38.5 70 38.5 C 72.2 38.5 74 37 74 34.5 C 74 32.5 73 30 70 25 Z"/>
    <circle cx="67" cy="67" r="2.2"/>
    <circle cx="73" cy="71" r="2.6"/>
    <rect x="66" y="98" width="8" height="11" rx="2"/>
    <path d="M70 95 L70 98"/>
    <circle cx="70" cy="140" r="5.5"/>
    <path d="M66 140 C 68 136.5 72 136.5 74 140"/>
    <circle cx="70" cy="176" r="4"/>
    <path d="M70 169 L70 170.5 M70 181.5 L70 183 M63 176 L64.5 176 M75.5 176 L77 176"/>
  </g>
</svg>
<!-- seed: SS-skin-hydrate-01.svg ｜ S-02 补水护理 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-02 | 名称 补水护理 | 分类 美容·补水 | 难度 入门 | 标签 保湿/干燥 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M84 58 C 108 58 116 78 116 100 C 116 124 102 142 84 142 C 66 142 52 124 52 100 C 52 78 60 58 84 58 Z"/>
    <path d="M68 96 C 71 92 76 92 79 96"/>
    <path d="M90 96 C 93 92 98 92 101 96"/>
    <path d="M76 118 C 82 122 88 122 92 118"/>
  </g>
  <!-- layer: 点缀（水滴组） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M146 72 C 143 78 142 82 142 86 C 142 89 144 92 146 92 C 148 92 150 89 150 86 C 150 82 149 78 146 72 Z"/>
    <path d="M160 106 C 156 114 155 118 155 122 C 155 126 157 129 160 129 C 163 129 165 126 165 122 C 165 118 164 114 160 106 Z"/>
    <path d="M142 136 C 139 142 138 145 138 148 C 138 151 140 154 142 154 C 144 154 146 151 146 148 C 146 145 145 142 142 136 Z"/>
  </g>
</svg>
<!-- seed: SS-skin-soothe-01.svg ｜ S-03 舒缓手法 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-03 | 名称 舒缓手法 | 分类 美容·舒缓 | 难度 入门 | 标签 敏感/按压 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部弧线） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M86 54 C 112 54 122 76 122 100 C 122 126 106 146 86 146"/>
    <path d="M86 54 C 60 54 50 76 50 100 C 50 126 66 146 86 146"/>
    <path d="M70 96 C 73 92 78 92 81 96"/>
    <path d="M94 96 C 97 92 102 92 105 96"/>
  </g>
  <!-- layer: 点缀（柔和手掌线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M118 152 C 132 148 144 158 144 170 C 144 180 135 186 122 186 C 110 186 102 180 102 170 C 102 160 108 154 118 152 Z"/>
    <path d="M112 152 L108 140 M120 148 L120 136 M129 150 L133 138 M137 156 L143 146"/>
    <path d="M48 92 C 40 88 34 92 34 100" stroke="#7A8E96" stroke-width="2.6" opacity="0.4"/>
    <path d="M44 112 C 36 110 30 116 32 124" stroke="#7A8E96" stroke-width="2.6" opacity="0.3"/>
  </g>
</svg>
<!-- seed: SS-skin-facial-01.svg ｜ S-04 面部按摩基础 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-04 | 名称 面部按摩方向示意 | 分类 美容·手法 | 难度 进阶 | 标签 居家护理 -->
  <!-- palette: c-line: #7A8E96 | c-face: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓） -->
  <g id="subject" fill="none" stroke="#3A3A3A" stroke-width="2.8">
    <ellipse cx="100" cy="102" rx="46" ry="58"/>
    <path d="M78 88 C 84 84 90 84 95 88" stroke-width="2.2"/>
    <path d="M105 88 C 110 84 116 84 122 88" stroke-width="2.2"/>
    <path d="M96 122 C 100 126 104 126 108 122" stroke-width="2.2"/>
  </g>
  <!-- layer: 点缀（向外按摩方向箭头 ×4） -->
  <g id="accent" fill="none" stroke="#7A8E96" stroke-width="3" stroke-linecap="round">
    <path d="M100 76 C 100 64 100 56 100 46"/>
    <path d="M96 52 L100 44 L104 52" stroke-width="2.6"/>
    <path d="M76 104 C 64 106 56 108 48 112"/>
    <path d="M54 106 L46 112 L55 117" stroke-width="2.6"/>
    <path d="M124 104 C 136 106 144 108 152 112"/>
    <path d="M146 106 L154 112 L145 117" stroke-width="2.6"/>
    <path d="M100 134 C 100 146 100 154 100 162"/>
    <path d="M96 156 L100 164 L104 156" stroke-width="2.6"/>
  </g>
</svg>
<!-- seed: SS-skin-cleanse-01.svg ｜ S-06 卸妆规范 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-06 | 名称 卸妆规范 | 分类 美容·卸妆 | 难度 入门 | 标签 清洁/卸妆 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（化妆棉圆片） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <circle cx="76" cy="94" r="36"/>
    <circle cx="76" cy="94" r="24" opacity="0.5" stroke-width="2"/>
    <path d="M62 94 C 68 88 84 88 90 94" opacity="0.6" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（水滴＋脸部弧线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M140 52 C 137 58 136 62 136 66 C 136 69 138 72 140 72 C 142 72 144 69 144 66 C 144 62 143 58 140 52 Z"/>
    <path d="M156 82 C 152 90 151 94 151 98 C 151 102 153 105 156 105 C 159 105 161 102 161 98 C 161 94 160 90 156 82 Z"/>
    <path d="M132 132 C 150 138 162 152 166 170" stroke="#7A8E96" stroke-width="2.6"/>
    <path d="M146 126 C 164 132 176 146 180 164" stroke="#7A8E96" stroke-width="2.6" opacity="0.45"/>
  </g>
</svg>
<!-- seed: SS-skin-tone-01.svg ｜ S-07 二次清洁（温和） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-07 | 名称 二次清洁 | 分类 美容·二次清洁 | 难度 入门 | 标签 爽肤/棉片 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部弧线） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M112 48 C 88 58 74 80 74 106 C 74 132 88 154 112 164"/>
    <path d="M124 56 C 102 66 90 86 90 108 C 90 130 102 150 124 160" opacity="0.45" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（棉片＋滑过示意线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <circle cx="146" cy="66" r="16"/>
    <path d="M136 66 C 140 62 152 62 156 66" opacity="0.7"/>
    <path d="M56 96 C 82 78 118 76 150 90" stroke="#7A8E96" stroke-width="2.4" opacity="0.7"/>
    <path d="M150 90 L140 86 M150 90 L144 99"/>
  </g>
</svg>
<!-- seed: SS-skin-mask-01.svg ｜ S-08 面膜使用规范（含示意） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-08 | 名称 面膜使用示意 | 分类 美容·护理 | 难度 入门 | 标签 居家护理 -->
  <!-- palette: c-face: #D9BFA8 | c-mask: #EAF2E6 | c-line: #A8BD84（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FCFDFB" stroke="#E2EAE4" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸轮廓 + 面膜贴片） -->
  <g id="subject">
    <ellipse cx="100" cy="102" rx="46" ry="56" fill="none" stroke="#D9BFA8" stroke-width="2.5"/>
    <ellipse cx="100" cy="102" rx="41" ry="51" fill="#EAF2E6" stroke="#A8BD84" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（眼 / 鼻 / 嘴留孔 + 边缘虚线） -->
  <g id="accent">
    <ellipse cx="82" cy="88" rx="9" ry="5.5" fill="#FCFDFB" stroke="#A8BD84" stroke-width="1.6"/>
    <ellipse cx="118" cy="88" rx="9" ry="5.5" fill="#FCFDFB" stroke="#A8BD84" stroke-width="1.6"/>
    <ellipse cx="100" cy="132" rx="10" ry="5" fill="#FCFDFB" stroke="#A8BD84" stroke-width="1.6"/>
    <path d="M100 96 L100 114" fill="none" stroke="#A8BD84" stroke-width="1.6" stroke-linecap="round"/>
    <ellipse cx="100" cy="102" rx="44" ry="54" fill="none" stroke="#A8BD84" stroke-width="1.4" stroke-dasharray="4 5" opacity="0.7"/>
  </g>
</svg>
<!-- seed: SS-skin-eye-01.svg ｜ S-09 眼周护理手法 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-09 | 名称 眼周护理 | 分类 美容·眼周 | 难度 入门 | 标签 眼周/细纹 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（眼睛） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M50 100 C 66 80 94 80 110 100 C 94 120 66 120 50 100 Z"/>
    <circle cx="80" cy="100" r="12" stroke-width="2.4"/>
    <circle cx="80" cy="100" r="5" fill="#7A8E96" stroke="none"/>
  </g>
  <!-- layer: 点缀（环绕箭头圈） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M120 62 C 148 72 160 98 154 126"/>
    <path d="M154 126 L145 120 M154 126 L146 134"/>
    <path d="M42 140 C 22 132 12 110 16 86"/>
    <path d="M16 86 L20 96 M16 86 L26 94"/>
  </g>
</svg>
<!-- seed: SS-skin-neck-01.svg ｜ S-10 颈部护理 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-10 | 名称 颈部护理 | 分类 美容·颈部 | 难度 入门 | 标签 颈纹/提拉 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（颈部线条） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M70 44 C 60 76 60 108 70 132"/>
    <path d="M126 44 C 136 76 136 108 126 132"/>
    <path d="M60 132 C 82 148 114 148 136 132"/>
    <path d="M40 172 C 70 152 126 152 156 172"/>
  </g>
  <!-- layer: 点缀（向上箭头） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M100 100 L100 48"/>
    <path d="M86 62 L100 46 L114 62"/>
    <path d="M74 108 C 84 112 92 116 100 122" stroke="#7A8E96" stroke-width="2.2" opacity="0.45"/>
    <path d="M124 108 C 116 112 108 116 100 122" stroke="#7A8E96" stroke-width="2.2" opacity="0.45"/>
  </g>
</svg>
<!-- seed: SS-skin-hand-01.svg ｜ S-11 手部护理（手膜） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-11 | 名称 手部护理手膜 | 分类 美容·手部 | 难度 入门 | 标签 手部/手膜 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手掌轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M62 92 C 62 80 70 72 82 72 L112 72 C 124 72 132 80 132 92 L132 130 C 132 152 116 168 96 168 C 76 168 62 152 62 130 Z"/>
    <path d="M72 72 L72 50"/>
    <path d="M88 72 L88 42"/>
    <path d="M104 72 L104 44"/>
    <path d="M118 74 L122 54"/>
    <path d="M62 100 C 46 100 38 112 42 124"/>
  </g>
  <!-- layer: 点缀（手膜象征线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M58 148 C 76 158 118 158 138 148"/>
    <path d="M56 136 C 60 132 66 130 72 130" opacity="0.6"/>
    <path d="M136 136 C 132 132 126 130 120 130" opacity="0.6"/>
  </g>
</svg>
<!-- seed: SS-skin-scalp-01.svg ｜ S-12 头皮放松按摩 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-12 | 名称 头皮放松按摩 | 分类 美容·头皮 | 难度 入门 | 标签 头皮/减压 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（头部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M100 40 C 134 40 158 64 158 98 C 158 132 134 156 100 156 C 66 156 42 132 42 98 C 42 64 66 40 100 40 Z"/>
    <path d="M58 84 C 72 56 106 48 132 60"/>
  </g>
  <!-- layer: 点缀（指腹按压点阵） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <circle cx="80" cy="78" r="5"/>
    <circle cx="100" cy="68" r="5"/>
    <circle cx="120" cy="78" r="5"/>
    <circle cx="70" cy="100" r="5"/>
    <circle cx="130" cy="100" r="5"/>
    <circle cx="86" cy="116" r="5"/>
    <circle cx="114" cy="116" r="5"/>
  </g>
</svg>
<!-- seed: SS-skin-steam-01.svg ｜ S-13 居家蒸面 / 热敷 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-13 | 名称 蒸面热敷 | 分类 美容·蒸面 | 难度 入门 | 标签 热敷/毛孔 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M100 78 C 122 78 130 96 130 116 C 130 138 118 154 100 154 C 82 154 70 138 70 116 C 70 96 78 78 100 78 Z"/>
    <path d="M86 112 C 89 108 94 108 97 112"/>
    <path d="M104 112 C 107 108 112 108 115 112"/>
    <path d="M90 134 C 96 138 104 138 110 134"/>
  </g>
  <!-- layer: 点缀（蒸汽曲线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M76 66 C 68 54 84 46 76 34 C 70 26 78 20 84 16"/>
    <path d="M100 62 C 92 50 108 42 100 30 C 94 22 102 16 108 12"/>
    <path d="M124 66 C 116 54 132 46 124 34 C 118 26 126 20 132 16"/>
  </g>
</svg>
<!-- seed: SS-skin-rescue-01.svg ｜ S-15 熬夜急救护理（补水向） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 S-15 | 名称 熬夜急救 | 分类 美容·急救 | 难度 入门 | 标签 熬夜/急救 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（月牙＋脸部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M74 36 A 50 50 0 1 0 74 140"/>
    <path d="M74 36 A 38 38 0 1 1 74 140"/>
    <path d="M154 106 C 166 106 172 116 172 128 C 172 142 164 152 152 152 C 140 152 132 142 132 128 C 132 116 142 106 154 106 Z"/>
  </g>
  <!-- layer: 点缀（水滴） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M112 84 C 108 92 107 96 107 100 C 107 104 109 107 112 107 C 115 107 117 104 117 100 C 117 96 116 92 112 84 Z"/>
    <path d="M126 118 C 123 124 122 127 122 130 C 122 133 124 136 126 136 C 128 136 130 133 130 130 C 130 127 129 124 126 118 Z"/>
    <path d="M20 150 C 34 158 52 162 70 160" stroke="#7A8E96" stroke-width="2.2" opacity="0.4"/>
  </g>
</svg>
