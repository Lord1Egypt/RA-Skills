<!-- ============================================================
  styling-studio SVG 种子包 · 祛痘（A）
  种子数：8 ｜ 所属组：流程样式组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-acne-cleanse-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-acne-cleanse-01.svg ｜ A-01 温和清洁流程 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-01 | 名称 温和清洁 | 分类 祛痘·清洁 | 难度 入门 | 标签 泡沫/清洁 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（手掌轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M64 130 C 64 120 72 114 84 114 L106 114 C 118 114 126 120 126 130 L126 152 C 126 168 112 178 95 178 C 78 178 64 168 64 152 Z"/>
    <path d="M74 114 L74 96"/>
    <path d="M90 114 L90 90"/>
    <path d="M106 114 L106 94"/>
    <path d="M118 116 L122 100"/>
    <path d="M64 132 C 48 130 40 140 44 150"/>
  </g>
  <!-- layer: 点缀（泡沫泡泡组） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <circle cx="128" cy="72" r="11"/>
    <circle cx="149" cy="96" r="8"/>
    <circle cx="118" cy="54" r="6"/>
    <circle cx="146" cy="54" r="4.5"/>
    <circle cx="160" cy="76" r="5"/>
    <circle cx="140" cy="86" r="3.5"/>
  </g>
</svg>
<!-- seed: SS-acne-oil-01.svg ｜ A-02 控油护理要点 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-02 | 名称 控油护理 | 分类 祛痘·控油 | 难度 入门 | 标签 出油/清爽 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓＋T区线） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M92 54 C 114 54 122 74 122 96 C 122 120 110 140 92 140 C 74 140 62 120 62 96 C 62 74 70 54 92 54 Z"/>
    <path d="M92 66 L92 116" opacity="0.4" stroke-width="2"/>
    <path d="M76 84 L108 84" opacity="0.4" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（油滴＋划除斜线） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M146 62 C 142 70 141 74 141 78 C 141 82 143 85 146 85 C 149 85 151 82 151 78 C 151 74 150 70 146 62 Z"/>
    <path d="M160 104 C 157 110 156 113 156 116 C 156 119 158 122 160 122 C 162 122 164 119 164 116 C 164 113 163 110 160 104 Z"/>
    <path d="M132 96 L172 152" stroke-width="2.6"/>
    <path d="M142 90 L178 136" stroke-width="2.6" opacity="0.55"/>
  </g>
</svg>
<!-- seed: SS-acne-soothe-01.svg ｜ A-03 舒缓护理 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-03 | 名称 舒缓护理 | 分类 祛痘·舒缓 | 难度 入门 | 标签 泛红/芦荟 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（芦荟叶形） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M88 164 C 74 130 76 86 92 42 C 108 86 110 130 96 164 Z"/>
    <path d="M92 156 L92 56" opacity="0.5" stroke-width="2"/>
    <path d="M84 118 C 88 122 96 122 100 118" opacity="0.5" stroke-width="2"/>
    <path d="M82 92 C 87 97 97 97 102 92" opacity="0.5" stroke-width="2"/>
  </g>
  <!-- layer: 点缀（脸部弧线＋水珠） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M136 62 C 160 70 172 92 168 116 C 164 140 144 154 122 152" stroke="#7A8E96" stroke-width="2.6"/>
    <path d="M150 74 C 168 84 176 104 172 126" stroke="#7A8E96" stroke-width="2.4" opacity="0.4"/>
    <path d="M146 100 C 143 106 142 109 142 112 C 142 115 144 118 146 118 C 148 118 150 115 150 112 C 150 109 149 106 146 100 Z"/>
  </g>
</svg>
<!-- seed: SS-acne-routine-01.svg ｜ A-05 早晚清洁节奏 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-05 | 名称 早晚清洁流程图标 | 分类 祛痘·清洁 | 难度 入门 | 标签 日常护理 -->
  <!-- palette: c-step: #6E8B9E | c-line: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（三步徽章：水滴 → 泡沫 → 完成） -->
  <g id="subject" fill="none" stroke="#6E8B9E" stroke-width="3" stroke-linecap="round">
    <circle cx="48" cy="100" r="24"/>
    <circle cx="100" cy="100" r="24"/>
    <circle cx="152" cy="100" r="24"/>
    <path d="M72 100 L76 100 M124 100 L128 100" stroke-width="2.6"/>
    <path d="M74 96 L79 100 L74 104" stroke-width="2.2"/>
    <path d="M126 96 L131 100 L126 104" stroke-width="2.2"/>
  </g>
  <!-- layer: 点缀（步骤图标） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2.6" stroke-linecap="round">
    <path d="M48 88 C 42 96 40 100 40 105 C 40 111 44 114 48 114 C 52 114 56 111 56 105 C 56 100 54 96 48 88 Z"/>
    <circle cx="94" cy="104" r="4"/>
    <circle cx="104" cy="98" r="3"/>
    <circle cx="106" cy="108" r="3.4"/>
    <path d="M142 100 L149 107 L162 92"/>
  </g>
</svg>
<!-- seed: SS-acne-hydrate-01.svg ｜ A-06 清爽保湿（非油厚） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-06 | 名称 清爽保湿 | 分类 祛痘·保湿 | 难度 入门 | 标签 清爽/水油平衡 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M138 66 C 158 66 166 84 166 104 C 166 126 154 144 138 144 C 122 144 110 126 110 104 C 110 84 118 66 138 66 Z"/>
    <path d="M128 102 C 131 98 136 98 139 102"/>
    <path d="M146 102 C 149 98 154 98 157 102"/>
    <path d="M132 122 C 136 126 142 126 146 122"/>
  </g>
  <!-- layer: 点缀（水滴组） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <path d="M62 48 C 56 60 54 66 54 72 C 54 78 57 82 62 82 C 67 82 70 78 70 72 C 70 66 68 60 62 48 Z"/>
    <path d="M54 106 C 50 114 49 118 49 122 C 49 126 51 129 54 129 C 57 129 59 126 59 122 C 59 118 58 114 54 106 Z"/>
    <path d="M74 136 C 71 142 70 145 70 148 C 70 151 72 154 74 154 C 76 154 78 151 78 148 C 78 145 77 142 74 136 Z"/>
  </g>
</svg>
<!-- seed: SS-acne-sun-01.svg ｜ A-08 防晒与痘印防护 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-08 | 名称 防晒防护 | 分类 祛痘·防晒 | 难度 入门 | 标签 防晒/痘印 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（盾形） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M132 58 L176 72 C 176 110 158 140 132 152 C 106 140 88 110 88 72 Z"/>
    <path d="M110 104 L126 120 L158 86"/>
  </g>
  <!-- layer: 点缀（小太阳） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <circle cx="52" cy="62" r="17"/>
    <path d="M52 34 L52 24"/>
    <path d="M52 100 L52 90"/>
    <path d="M24 62 L14 62"/>
    <path d="M90 62 L80 62"/>
    <path d="M32 42 L25 35"/>
    <path d="M72 42 L79 35"/>
    <path d="M32 82 L25 89"/>
    <path d="M72 82 L79 89"/>
    <path d="M30 128 C 44 136 60 138 74 134" stroke="#7A8E96" stroke-width="2.2" opacity="0.4"/>
  </g>
</svg>
<!-- seed: SS-acne-cover-01.svg ｜ A-11 温和遮盖建议 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-11 | 名称 温和遮盖 | 分类 祛痘·遮盖 | 难度 入门 | 标签 遮盖/粉扑 -->
  <!-- palette: c-line: #7A8E96 | c-icon: #3A3A3A（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FAFCFD" stroke="#DDE7EA" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（脸部轮廓） -->
  <g id="subject" fill="none" stroke="#7A8E96" stroke-width="2.6" stroke-linecap="round">
    <path d="M80 56 C 102 56 110 76 110 98 C 110 122 98 142 80 142 C 62 142 50 122 50 98 C 50 76 58 56 80 56 Z"/>
    <path d="M68 94 C 71 90 76 90 79 94"/>
    <path d="M90 94 C 93 90 98 90 101 94"/>
    <path d="M70 118 C 76 122 86 122 92 118"/>
  </g>
  <!-- layer: 点缀（粉扑＋遮盖点阵） -->
  <g id="accent" fill="none" stroke="#3A3A3A" stroke-width="2" stroke-linecap="round">
    <circle cx="148" cy="92" r="22"/>
    <path d="M130 108 C 138 118 158 118 166 108"/>
    <path d="M148 92 L164 76"/>
    <circle cx="72" cy="104" r="3" stroke-width="1.6"/>
    <circle cx="88" cy="108" r="3" stroke-width="1.6"/>
    <circle cx="80" cy="84" r="3" stroke-width="1.6"/>
    <path d="M120 130 C 136 138 152 140 168 136" stroke="#7A8E96" stroke-width="2.2" opacity="0.4"/>
  </g>
</svg>
<!-- seed: SS-acne-selfcheck-01.svg ｜ A-12 就医信号清单（含自查卡） -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 A-12 | 名称 就医信号自查卡（四信号） | 分类 祛痘·提示 | 难度 入门 | 标签 合规提示 -->
  <!-- palette: c-line: #D98C6A | c-ink: #A85F48（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="184" height="184" rx="14" fill="#FFF9F5" stroke="#F0DCD2" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（卡片外框 + 四信号图标） -->
  <g id="subject" fill="none" stroke="#D98C6A" stroke-width="2.4" stroke-linecap="round">
    <rect x="20" y="34" width="160" height="132" rx="12"/>
    <circle cx="44" cy="78" r="14"/>
    <circle cx="82" cy="78" r="14"/>
    <circle cx="118" cy="78" r="14"/>
    <circle cx="156" cy="78" r="14"/>
  </g>
  <!-- layer: 点缀（信号符号 + 提示条） -->
  <g id="accent">
    <g fill="none" stroke="#A85F48" stroke-width="2" stroke-linecap="round">
      <circle cx="47" cy="74" r="2"/>
      <circle cx="41" cy="80" r="2.4"/>
      <circle cx="49" cy="82" r="2.2"/>
      <path d="M76 72 L80 80 L84 72 L88 84"/>
      <path d="M118 86 L118 70 M112 76 L118 70 L124 76"/>
      <path d="M150 84 A 7.5 7.5 0 1 1 157 76"/>
      <path d="M157 72 L157 77 L152 77"/>
    </g>
    <rect x="40" y="112" width="120" height="16" rx="8" fill="#D98C6A" opacity="0.18"/>
    <path d="M56 120 L104 120 M114 120 L144 120" stroke="#A85F48" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>
    <path d="M100 138 L100 150 M94 145 L100 152 L106 145" fill="none" stroke="#A85F48" stroke-width="2.4" stroke-linecap="round"/>
  </g>
</svg>
