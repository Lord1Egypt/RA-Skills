<!-- ============================================================
  styling-studio SVG 种子包 · 场景组合卡（K）
  种子数：12 ｜ 所属组：场景组合组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-look-bridal-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-look-bridal-01.svg ｜ K-01 婚礼·新娘全案组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-01 | 名称 婚礼·新娘全案组合卡 | 分类 场景组合 | 难度 进阶 | 标签 婚礼（新娘） -->
  <!-- palette: c-ink: #3A3A3A | c-acc: #B8935A | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">婚礼 · 新娘全案</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">温婉精致 · 暖调 · 全案四件</text>
  </g>
  <!-- layer: 主体（四格单品：甲 / 睫 / 发 / 妆） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F3E6DC" stroke="#C9B8A8" stroke-width="1.4"/>
    <path d="M68 100 C 61 100 60 106 60 112 L60 128 C 60 131 63 134 68 134 C 73 134 76 131 76 128 L76 112 C 76 106 75 100 68 100 Z" fill="none" stroke="#F5F4F2" stroke-width="3.4"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">法式甲 · N-03</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 116 C 160 104 186 104 198 116" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 122 C 162 132 184 132 196 122" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M156 112 C 155 106 156 101 159 98 M166 108 C 165 102 166 97 169 94 M178 108 C 177 102 178 97 181 94 M188 112 C 187 106 188 101 191 98" fill="none" stroke="#2B2320" stroke-width="1.8" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">轻密睫 · E-02</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M50 196 C 50 184 58 178 68 178 C 78 178 86 184 86 196" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M50 196 C 48 208 54 218 60 224" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M86 196 C 88 208 82 218 76 224" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 224 C 64 232 72 232 76 224 C 78 220 70 216 68 212" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 202 C 60 212 65 220 68 224" fill="none" stroke="#3A3A3A" stroke-width="1.6"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">低盘发 · H-08</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 202 C 166 199 171 199 174 202" fill="none" stroke="#C9748A" stroke-width="1.6"/>
    <path d="M176 202 C 179 199 184 199 188 202" fill="none" stroke="#C9748A" stroke-width="1.6"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.4" fill="#E8B4B8" opacity="0.65"/>
    <path d="M158 188 C 164 182 180 182 186 188" fill="none" stroke="#B8935A" stroke-width="1.6" stroke-dasharray="3 3"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">新娘妆 · M-07</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">甲 / 睫 / 发 / 妆 全案四件 · 法式主调、温柔收敛</text>
  </g>
</svg>
<!-- seed: SS-look-guest-01.svg ｜ K-02 婚礼·宾客得体组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-02 | 名称 婚礼·宾客得体组合卡 | 分类 场景组合 | 难度 入门 | 标签 婚礼（宾客） -->
  <!-- palette: c-ink: #3A3A3A | c-acc: #C98F8F | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">婚礼 · 宾客得体</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">低饱和 · 不抢镜 · 上镜友好</text>
  </g>
  <!-- layer: 主体（四格单品：甲 / 睫 / 发 / 妆） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F0DCD1" stroke="#C9B8A8" stroke-width="1.4"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">裸粉纯色 · N-01</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M158 114 C 157 109 158 105 160 102 M170 111 C 169 106 170 102 172 99 M182 111 C 181 106 182 102 184 99 M192 114 C 191 109 192 105 194 102" fill="none" stroke="#2B2320" stroke-width="1.6" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">自然睫 · E-01</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M50 194 C 50 182 58 176 68 176 C 78 176 86 182 86 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M50 194 C 46 206 54 216 48 228 C 44 236 52 242 46 250" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M86 194 C 90 206 82 216 88 228 C 92 236 84 242 90 250" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 200 C 60 214 66 224 68 232" fill="none" stroke="#3A3A3A" stroke-width="1.5"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">大波浪 · H-05</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 171 200 174 203" fill="none" stroke="#C9B8A8" stroke-width="1.5"/>
    <path d="M176 203 C 179 200 184 200 188 203" fill="none" stroke="#C9B8A8" stroke-width="1.5"/>
    <path d="M164 224 C 168 228 176 228 180 224" fill="none" stroke="#D9BFA8" stroke-width="1.6"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">清透裸妆 · M-03</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">避开大面积白与全黑 · 得体不抢新娘镜头</text>
  </g>
</svg>
<!-- seed: SS-look-work-01.svg ｜ K-03 职场·通勤日常组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-03 | 名称 职场·通勤日常组合卡 | 分类 场景组合 | 难度 入门 | 标签 职场/通勤 -->
  <!-- palette: c-ink: #3A3A3A | c-acc: #8A93A6 | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">职场 · 通勤日常</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">干净利落 · 低维护 · 提气色</text>
  </g>
  <!-- layer: 主体（四格单品：甲 / 睫 / 发 / 妆） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F1EAE2" stroke="#C9B8A8" stroke-width="1.4"/>
    <path d="M62 112 L74 112 M62 120 L74 120 M62 128 L70 128" stroke="#3A3A3A" stroke-width="1.4" stroke-linecap="round"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">细线条 · N-05</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M160 114 C 159 110 160 106 162 103 M172 111 C 171 107 172 103 174 100 M184 111 C 183 107 184 103 186 100" fill="none" stroke="#2B2320" stroke-width="1.6" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">自然睫 · E-01</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M52 192 C 52 180 59 174 68 174 C 77 174 84 180 84 192" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M52 192 C 50 214 52 234 54 246" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M84 192 C 86 214 84 234 82 246" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 198 C 60 214 63 228 64 240" fill="none" stroke="#3A3A3A" stroke-width="1.5"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">锁骨发 · H-15</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 170 200 173 203" fill="none" stroke="#5A4A3E" stroke-width="1.5"/>
    <path d="M176 203 C 179 200 183 200 186 203" fill="none" stroke="#5A4A3E" stroke-width="1.5"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.2" fill="#D98C8C" opacity="0.7"/>
    <circle cx="152" cy="218" r="2" fill="#E8B4B8" opacity="0.6"/>
    <circle cx="192" cy="218" r="2" fill="#E8B4B8" opacity="0.6"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">职场妆 · M-02</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">三件套原则：低维护、耐看、每天可复制</text>
  </g>
</svg>
<!-- seed: SS-look-interview-01.svg ｜ K-04 面试·正式场合组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-04 | 名称 面试·正式场合组合卡 | 分类 场景组合 | 难度 入门 | 标签 面试 -->
  <!-- palette: c-ink: #3A3A3A | c-acc: #4A5568 | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">面试 · 正式场合</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">干净利落 · 不露痕迹 · 专业感</text>
  </g>
  <!-- layer: 主体（四格单品：甲 / 睫 / 发 / 穿搭） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#EDE4DA" stroke="#C9B8A8" stroke-width="1.4"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">纯色裸色 · N-01</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M162 113 C 161 110 162 107 163 105 M174 111 C 173 108 174 105 175 103 M186 113 C 185 110 186 107 187 105" fill="none" stroke="#2B2320" stroke-width="1.4" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">无痕超轻睫 · E-14</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M52 194 C 52 180 59 174 68 174 C 77 174 84 180 84 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M52 194 C 50 210 52 224 54 236" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M84 194 C 86 210 84 224 82 236" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M62 200 C 62 212 64 222 64 230" fill="none" stroke="#3A3A3A" stroke-width="1.5"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">波波头 · H-14</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M156 186 L164 182 L172 189 L180 182 L188 186 L187 202 L177 206 L168 240 L159 206 L149 202 Z" fill="#F4F6F8" stroke="#C9D2DA" stroke-width="1.5" stroke-linejoin="round"/>
    <path d="M164 182 L172 189 L180 182" fill="none" stroke="#C9D2DA" stroke-width="1.3"/>
    <path d="M158 208 L186 208" stroke="#4A5568" stroke-width="1.8"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">衬衫 · O-18</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">"被看到能力、而非装扮" · 一切从简</text>
  </g>
</svg>
<!-- seed: SS-look-date-01.svg ｜ K-05 约会·初次见面组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-05 | 名称 约会·初次见面组合卡 | 分类 场景组合 | 难度 入门 | 标签 约会 -->
  <!-- palette: c-ink: #3A3A3A | c-acc: #E899AE | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">约会 · 初次见面</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">清新甜美 · 亲和力 · 拍照友好</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#FDF9F2" stroke="#C9B8A8" stroke-width="1.4"/>
    <circle cx="68" cy="116" r="4" fill="#F6D96A"/>
    <path d="M68 108 C 66 111 65 112.5 65 113.5 M63 118.5 C 65 120 67 120.5 68 120.5 M73 118.5 C 71 120 69 120.5 68 120.5" fill="none" stroke="#FBF6EA" stroke-width="1.6" stroke-linecap="round"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">小雏菊 · N-11</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 120 C 160 108 186 108 198 120" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 126 C 162 136 184 136 196 126" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M158 114 C 157 108 158 103 161 99 M168 111 C 167 104 168 99 171 95 M178 111 C 177 104 178 99 181 95 M188 113 C 187 106 188 101 192 97 M196 116 C 195 110 196 105 200 102" fill="none" stroke="#2B2320" stroke-width="1.7" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">飞扬睫 · E-10</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M52 194 C 52 180 59 174 68 174 C 77 174 84 180 84 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M52 194 C 48 208 56 220 52 232 C 50 240 58 246 56 252" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M84 194 C 88 208 80 220 84 232 C 86 240 78 246 80 252" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M60 200 C 60 214 65 226 68 234" fill="none" stroke="#3A3A3A" stroke-width="1.5"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">蛋卷头 · H-19</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 170 200 173 203" fill="none" stroke="#8A5A4A" stroke-width="1.5"/>
    <path d="M176 203 C 179 200 183 200 186 203" fill="none" stroke="#8A5A4A" stroke-width="1.5"/>
    <ellipse cx="158" cy="218" rx="5" ry="3" fill="#F0A8B8" opacity="0.7"/>
    <ellipse cx="186" cy="218" rx="5" ry="3" fill="#F0A8B8" opacity="0.7"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.4" fill="#E8708C" opacity="0.75"/>
    <path d="M190 194 C 194 196 196 199 196 202" fill="none" stroke="#E899AE" stroke-width="1.4"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">约会妆 · M-04</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">甜美但不过度 · 自然光下最上镜</text>
  </g>
</svg>
<!-- seed: SS-look-party-01.svg ｜ K-06 派对·夜场闪耀组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-06 | 名称 派对·夜场闪耀组合卡 | 分类 场景组合 | 难度 进阶 | 标签 派对/夜场 -->
  <!-- palette: c-ink: #3A3A3A | c-gold: #E5B84B | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">派对 · 夜场闪耀</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">存在感 · 低光环境友好 · 出片</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F3EFF9" stroke="#C9B8A8" stroke-width="1.4"/>
    <path d="M68 104 L70.5 111 L78 111.5 L72 116 L74 123 L68 118.5 L62 123 L64 116 L58 111.5 L65.5 111 Z" fill="#E5B84B"/>
    <path d="M76 124 C 77.5 121.5 81 121.5 82 124.5 C 83 127.5 79.5 129.5 77 131 C 74.5 129.5 71 127.5 72 124.5 C 73 121.5 76 121.5 77.5 124 Z" fill="#E5B84B" opacity="0.85" transform="translate(0 -1)"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">星月元素 · N-20</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M156 113 C 155 106 156 100 159 96 M165 110 C 164 102 165 96 168 91 M175 109 C 174 97 175 88 179 82 M185 110 C 184 102 185 96 188 91 M193 114 C 192 106 193 100 196 96" fill="none" stroke="#2B2320" stroke-width="1.8" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">芭比睫 · E-12</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M50 194 C 50 182 58 176 68 176 C 78 176 86 182 86 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M50 194 C 46 206 54 216 48 228 C 44 236 52 242 46 250" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M86 194 C 90 206 82 216 88 228 C 92 236 84 242 90 250" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 200 C 60 214 66 224 68 232" fill="none" stroke="#3A3A3A" stroke-width="1.5"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">大波浪 · H-05</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M160 201 C 165 197 171 197 174 200" fill="none" stroke="#5A4A6A" stroke-width="1.5"/>
    <path d="M176 200 C 179 197 185 197 190 201" fill="none" stroke="#5A4A6A" stroke-width="1.5"/>
    <path d="M162 205 C 166 210 176 210 182 205" fill="none" stroke="#5A4A6A" stroke-width="1.4" opacity="0.7"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.4" fill="#8E3B4A" opacity="0.8"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">晚宴妆 · M-05</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">金 / 星光点缀提亮 · 低光下显存在感</text>
  </g>
</svg>
<!-- seed: SS-look-neochinese-01.svg ｜ K-07 新中式·雅集组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-07 | 名称 新中式·雅集组合卡 | 分类 场景组合 | 难度 进阶 | 标签 新中式/雅集 -->
  <!-- palette: c-ink: #3A3A3A | c-jade: #8FA88F | c-gold: #C9B8A8 | c-soft: #F6F4EC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFCF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">新中式 · 雅集</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">东方雅致 · 低饱和 · 器质感</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#F7F5ED" stroke="#E3DBC8"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F6F4EC" stroke="#B8A88C" stroke-width="1.4"/>
    <path d="M60 118 C 58 113 61 109 65 110 C 66 106 71 105 73 108 C 75 105 80 106 80 110 C 84 110 85 114 82 116 L61 117 Z" fill="#E3D5B8" stroke="#B8A88C" stroke-width="1"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">祥云纹 · N-41</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#F7F5ED" stroke="#E3DBC8"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M162 113 C 161 109 162 106 164 103 M174 111 C 173 107 174 104 176 101 M186 113 C 185 109 186 106 188 103" fill="none" stroke="#2B2320" stroke-width="1.5" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">自然睫 · E-01</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#F7F5ED" stroke="#E3DBC8"/>
    <path d="M50 196 C 50 184 58 178 68 178 C 78 178 86 184 86 196" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M50 196 C 48 208 54 218 60 224" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M86 196 C 88 208 82 218 76 224" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 224 C 64 232 72 232 76 224 C 78 220 70 216 68 212" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M60 202 C 60 212 65 220 68 224" fill="none" stroke="#3A3A3A" stroke-width="1.6"/>
    <path d="M80 208 L86 204" stroke="#C9B8A8" stroke-width="2.2" stroke-linecap="round"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">低盘发 · H-08</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#F7F5ED" stroke="#E3DBC8"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 170 200 173 203" fill="none" stroke="#8A7A6A" stroke-width="1.4"/>
    <path d="M176 203 C 179 200 183 200 186 203" fill="none" stroke="#8A7A6A" stroke-width="1.4"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.2" fill="#C98F8F" opacity="0.6"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">清透裸妆 · M-03</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F0EDE2"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">玉色 / 金调点题 · 一处主元素即可</text>
  </g>
</svg>
<!-- seed: SS-look-student-01.svg ｜ K-08 学生·日常清新组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-08 | 名称 学生·日常清新组合卡 | 分类 场景组合 | 难度 入门 | 标签 学生/日常 -->
  <!-- palette: c-ink: #3A3A3A | c-candy: #F5A8C0 | c-soft: #FBF7F2（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">学生 · 日常清新</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">活泼耐用 · 低维护 · 校内友好</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#FDF9F6" stroke="#C9B8A8" stroke-width="1.4"/>
    <path d="M57 100 L70 96 L57 112 Z" fill="#F5A8C0"/>
    <path d="M79 118 L66 138 L79 130 Z" fill="#F6D96A" opacity="0.9"/>
    <path d="M57 126 L66 120 L57 138 Z" fill="#9CC7E8" opacity="0.9"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">糖果撞色 · N-18</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M148 118 C 160 106 186 106 198 118" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M150 124 C 162 134 184 134 196 124" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M162 113 C 161 109 162 106 164 103 M174 111 C 173 107 174 104 176 101 M186 113 C 185 109 186 106 188 103" fill="none" stroke="#2B2320" stroke-width="1.5" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">自然睫 · E-01</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <path d="M52 194 C 52 180 59 174 68 174 C 77 174 84 180 84 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M76 186 C 82 184 86 188 86 194 C 86 200 82 206 78 210" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M76 186 C 70 190 68 196 70 202" fill="none" stroke="#6E5748" stroke-width="2"/>
    <path d="M56 200 C 55 214 60 228 62 240" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M62 200 C 62 214 66 228 68 240" fill="none" stroke="#3A3A3A" stroke-width="1.4"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">半扎发 · H-26</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FBF7F2" stroke="#EADFD3"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 170 200 173 203" fill="none" stroke="#8A7A6A" stroke-width="1.4"/>
    <path d="M176 203 C 179 200 183 200 186 203" fill="none" stroke="#8A7A6A" stroke-width="1.4"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.2" fill="#E8A8B0" opacity="0.6"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">清透裸妆 · M-03</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F5EDE3"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">一点亮色提精神 · 短甲更利落</text>
  </g>
</svg>
<!-- seed: SS-look-men-business-01.svg ｜ K-09 男士·商务组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-09 | 名称 男士·商务组合卡 | 分类 场景组合 | 难度 入门 | 标签 男性商务 -->
  <!-- palette: c-ink: #3A3A3A | c-steel: #4A5568 | c-soft: #F6F6F4（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FCFCFA" stroke="#E2E2DE" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">男士 · 商务</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">整洁克制 · 低存在感 · 可信赖</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <path d="M68 100 C 61 100 59 106 59 113 L59 126 C 59 131 63 134 68 134 C 73 134 77 131 77 126 L77 113 C 77 106 75 100 68 100 Z" fill="#4A4A4F"/>
    <path d="M59 104 L77 104" stroke="#55555B" stroke-width="2"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">哑光纯色 · N-38</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <path d="M148 120 C 158 112 186 112 198 120" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M152 126 C 162 132 184 132 196 126" fill="none" stroke="#3A3A3A" stroke-width="2"/>
    <path d="M164 115 C 163 112 164 110 165 108 M174 114 C 173 111 174 109 175 107 M184 115 C 183 112 184 110 185 108" fill="none" stroke="#2B2320" stroke-width="1.3" stroke-linecap="round"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">男性自然睫 · E-07</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <path d="M54 190 C 54 178 60 172 68 172 C 76 172 82 178 82 190 C 82 196 81 202 79 208" fill="none" stroke="#5A4A3E" stroke-width="2.4"/>
    <path d="M62 176 C 66 173 70 173 74 176" fill="none" stroke="#5A4A3E" stroke-width="1.6"/>
    <path d="M54 190 C 54 196 55 202 57 208" fill="none" stroke="#5A4A3E" stroke-width="2.2"/>
    <path d="M60 196 C 60 210 64 222 66 232" fill="none" stroke="#3A3A3A" stroke-width="1.4"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">男发短层次 · H-10</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <ellipse cx="172" cy="212" rx="25" ry="29" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M163 204 C 166 202 169 202 172 204" fill="none" stroke="#5A4A3E" stroke-width="1.3"/>
    <path d="M172 204 C 175 202 178 202 181 204" fill="none" stroke="#5A4A3E" stroke-width="1.3"/>
    <path d="M164 224 C 168 227 176 227 180 224" fill="none" stroke="#C9B8A8" stroke-width="1.3"/>
    <path d="M160 190 C 166 186 178 186 184 190" fill="none" stroke="#C9D2DA" stroke-width="1.2" stroke-dasharray="3 3"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">男士底妆 · M-19</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#EFEFEC"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">"看起来没做、其实都做了" · 细节即专业</text>
  </g>
</svg>
<!-- seed: SS-look-men-casual-01.svg ｜ K-10 男士·休闲周末组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-10 | 名称 男士·休闲周末组合卡 | 分类 场景组合 | 难度 入门 | 标签 男性休闲 -->
  <!-- palette: c-ink: #3A3A3A | c-steel: #4A5568 | c-soft: #F6F6F4（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FCFCFA" stroke="#E2E2DE" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">男士 · 休闲周末</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">松弛随性 · 一点个性 · 舒适优先</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <path d="M68 98 C 61 98 59 104 59 112 L59 126 C 59 131 63 134 68 134 C 73 134 77 131 77 126 L77 112 C 77 104 75 98 68 98 Z" fill="#F2F0EE" stroke="#C9C6C0" stroke-width="1.4"/>
    <circle cx="68" cy="120" r="4" fill="#2F3A44"/>
    <path d="M68 108 L71 112 L68 115 L65 112 Z" fill="#2F3A44" opacity="0.75"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">单点几何 · N-39</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <path d="M54 190 C 54 178 60 172 68 172 C 76 172 82 178 82 190" fill="none" stroke="#5A4A3E" stroke-width="2.4"/>
    <path d="M54 190 C 55 182 60 177 68 175" fill="none" stroke="#5A4A3E" stroke-width="1.6"/>
    <path d="M68 175 C 76 177 81 182 82 190" fill="none" stroke="#5A4A3E" stroke-width="1.6"/>
    <path d="M62 195 C 62 208 65 220 66 230" fill="none" stroke="#3A3A3A" stroke-width="1.4"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">男发碎盖 · H-29</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <ellipse cx="68" cy="210" rx="25" ry="29" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M59 204 C 62 202 65 202 68 204" fill="none" stroke="#5A4A3E" stroke-width="1.3"/>
    <path d="M68 204 C 71 202 74 202 77 204" fill="none" stroke="#5A4A3E" stroke-width="1.3"/>
    <path d="M60 220 C 64 223 72 223 76 220" fill="none" stroke="#C9B8A8" stroke-width="1.3"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">男士肤色 · M-09</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#F7F7F5" stroke="#E0E0DB"/>
    <circle cx="172" cy="206" r="16" fill="none" stroke="#B8935A" stroke-width="2"/>
    <path d="M166 178 C 162 172 182 172 178 178" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M166 234 C 162 240 182 240 178 234" fill="none" stroke="#6E5748" stroke-width="2.4"/>
    <path d="M172 206 L172 196 M172 206 L180 210" stroke="#3A3A3A" stroke-width="1.6" stroke-linecap="round"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">腕表 · J-19</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#EFEFEC"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">腕表是"唯一配饰"原则的完美答案</text>
  </g>
</svg>
<!-- seed: SS-look-autumn-01.svg ｜ K-11 秋冬·暖调约会组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-11 | 名称 秋冬·暖调约会组合卡 | 分类 场景组合 | 难度 进阶 | 标签 秋冬/约会 -->
  <!-- palette: c-ink: #3A3A3A | c-warm: #C8A184 | c-soft: #FAF6F1（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFBF8" stroke="#EADFD3" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">秋冬 · 暖调约会</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">暖棕调 · 层次感 · 拥抱感</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#FAF6F1" stroke="#E8DCCC"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F2C8B8" stroke="#C9A88C" stroke-width="1.4"/>
    <path d="M57 118 L79 118" stroke="#E8A98C" stroke-width="6" opacity="0.6"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">渐变底 · N-43</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#FAF6F1" stroke="#E8DCCC"/>
    <path d="M52 190 C 52 178 60 172 68 172 C 76 172 84 178 84 190" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M58 180 Q 64 176 68 180 Q 72 176 78 180" fill="none" stroke="#6E5748" stroke-width="1.6"/>
    <path d="M52 190 C 48 202 56 212 52 224 C 50 232 58 238 56 244" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M84 190 C 88 202 80 212 84 224 C 86 232 78 238 80 244" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">羊毛卷 · H-18</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#FAF6F1" stroke="#E8DCCC"/>
    <path d="M56 186 L62 182 L74 182 L80 186" fill="none" stroke="#C8A184" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M56 196 L58 192 L78 192 L80 196" fill="none" stroke="#8E6E5E" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M54 208 L56 204 L80 204 L82 208" fill="none" stroke="#B07040" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M58 214 L58 238 M78 214 L78 238" fill="none" stroke="#B07040" stroke-width="2"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">叠穿层次 · O-14</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#FAF6F1" stroke="#E8DCCC"/>
    <ellipse cx="172" cy="212" rx="26" ry="31" fill="none" stroke="#3A3A3A" stroke-width="1.8"/>
    <path d="M162 203 C 166 200 170 200 173 203" fill="none" stroke="#8A5A4A" stroke-width="1.5"/>
    <path d="M176 203 C 179 200 183 200 186 203" fill="none" stroke="#8A5A4A" stroke-width="1.5"/>
    <ellipse cx="158" cy="218" rx="5" ry="3" fill="#E8A8A0" opacity="0.7"/>
    <ellipse cx="186" cy="218" rx="5" ry="3" fill="#E8A8A0" opacity="0.7"/>
    <ellipse cx="172" cy="224" rx="7" ry="3.4" fill="#C96A6A" opacity="0.8"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">约会妆 · M-04</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#F3EBE0"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">焦糖 / 奶茶色系打底 · 暖光下更显气色</text>
  </g>
</svg>
<!-- seed: SS-look-vacation-01.svg ｜ K-12 度假·清新出游组合卡 -->
<svg viewBox="0 0 240 300" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 K-12 | 名称 度假·清新出游组合卡 | 分类 场景组合 | 难度 入门 | 标签 度假/旅行 -->
  <!-- palette: c-ink: #3A3A3A | c-fresh: #9CC7E8 | c-soft: #FAFBFC（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="284" rx="14" fill="#FDFCF8" stroke="#E2E8E2" stroke-width="1.5"/>
  </g>
  <!-- layer: 标题 -->
  <g id="title">
    <text x="24" y="42" font-family="sans-serif" font-size="16" fill="#3A3A3A">度假 · 清新出游</text>
    <text x="24" y="60" font-family="sans-serif" font-size="10.5" fill="#8A7868">清透 · 会呼吸 · 防晒友好</text>
  </g>
  <!-- layer: 主体（四格单品） -->
  <g id="subject">
    <rect x="20" y="72" width="96" height="88" rx="10" fill="#F6FAFC" stroke="#D8E4EA"/>
    <path d="M68 96 C 59 96 57 103 57 112 L57 128 C 57 134 62 138 68 138 C 74 138 79 134 79 128 L79 112 C 79 103 77 96 68 96 Z" fill="#F6EFE6" stroke="#C9B8A8" stroke-width="1.4"/>
    <path d="M68 100 C 61 100 60 106 60 112 L60 128 C 60 131 63 134 68 134 C 73 134 76 131 76 128 L76 112 C 76 106 75 100 68 100 Z" fill="none" stroke="#FFFFFF" stroke-width="3.2"/>
    <text x="26" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">法式甲 · N-03</text>
    <rect x="124" y="72" width="96" height="88" rx="10" fill="#F6FAFC" stroke="#D8E4EA"/>
    <path d="M52 194 C 52 182 60 176 68 176 C 76 176 84 182 84 194" fill="none" stroke="#6E5748" stroke-width="2.6"/>
    <path d="M74 188 C 80 186 84 190 84 196 C 84 202 80 208 76 212" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M56 200 C 55 212 60 224 62 234" fill="none" stroke="#6E5748" stroke-width="2.2"/>
    <path d="M62 202 C 62 216 66 228 68 236" fill="none" stroke="#3A3A3A" stroke-width="1.4"/>
    <text x="130" y="154" font-family="sans-serif" font-size="8.5" fill="#8A7868">半扎发 · H-26</text>
    <rect x="20" y="168" width="96" height="88" rx="10" fill="#F6FAFC" stroke="#D8E4EA"/>
    <path d="M58 186 L74 186 L62 196 L74 206 L58 206" fill="none" stroke="#9CC7E8" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M60 212 L68 230 L76 212" fill="none" stroke="#F0D8C8" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="M58 236 L78 236" stroke="#C9B8A8" stroke-width="2" stroke-linecap="round"/>
    <text x="26" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">夏季搭配 · O-15</text>
    <rect x="124" y="168" width="96" height="88" rx="10" fill="#F6FAFC" stroke="#D8E4EA"/>
    <path d="M172 190 L192 210 L172 230 L152 210 Z" fill="#F5E0E4" stroke="#E0AEB8" stroke-width="1.6"/>
    <path d="M172 190 L172 230 M152 210 L192 210" stroke="#E0AEB8" stroke-width="1" stroke-dasharray="3 3"/>
    <circle cx="172" cy="190" r="4" fill="none" stroke="#C9748A" stroke-width="1.8"/>
    <text x="130" y="250" font-family="sans-serif" font-size="8.5" fill="#8A7868">丝巾 · J-16</text>
  </g>
  <!-- layer: 点缀（要点条） -->
  <g id="accent">
    <rect x="20" y="268" width="200" height="18" rx="9" fill="#EDF3F6"/>
    <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#8A7868">清透底妆 + 防晒 · 丝巾一点跳色提亮</text>
  </g>
</svg>
