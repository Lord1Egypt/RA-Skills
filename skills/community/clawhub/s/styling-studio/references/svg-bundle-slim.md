<!-- ============================================================
  styling-studio SVG 种子包 · 纤体（B）
  种子数：9 ｜ 所属组：流程样式组 ｜ 载体：SVG 矢量（meta / palette / layer 注释齐全）
  格式：种子 = "seed:" 注释行之后的 <svg>…</svg> 块；原文件名（如 SS-slim-core-01.svg）现仅作种子 ID，
        与「预置 SVG 素材清单」及提示词成品库（wordlib）条目一一对应
  质检：python scripts/styling-studio-check-svg.py references/ （自动切块逐个校验）
  登记：新种子按 SS2 域知识「素材体系规范」生成质检后，将 <svg> 块（含 seed 注释）追加至对应品类包末尾，
        并同步更新 requirements 清单行与 wordlib 条目
  ============================================================ -->
<!-- seed: SS-slim-core-01.svg ｜ B-01 核心训练基础 -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-01 | 名称 平板支撑（核心训练） | 分类 纤体·核心 | 难度 入门 | 标签 居家/核心 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（平板支撑线条图） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="194" cy="136" r="12"/>
    <path d="M176 148 L108 150"/>
    <path d="M176 148 L176 188"/>
    <path d="M176 188 L214 190"/>
    <path d="M108 150 L54 154"/>
    <path d="M54 154 L48 158"/>
  </g>
  <!-- layer: 点缀（身体对齐虚线 + 地面线） -->
  <g id="accent">
    <path d="M50 152 L198 137" fill="none" stroke="#5B7A8E" stroke-width="2.4" opacity="0.45" stroke-dasharray="5 6" stroke-linecap="round"/>
    <path d="M36 200 L224 200" stroke="#5B7A8E" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-posture-01.svg ｜ B-02 体态矫正（圆肩 / 驼背） -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-02 | 名称 靠墙站体态自测（四点接触） | 分类 纤体·体态 | 难度 入门 | 标签 体态矫正 -->
  <!-- palette: c-figure: #5B7A8E | c-wall: #B9C6CE（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（站姿 + 墙体线） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="108" cy="60" r="15"/>
    <path d="M108 76 L108 168"/>
    <path d="M108 92 L96 148"/>
    <path d="M108 92 L120 148"/>
    <path d="M108 168 L102 232 L98 292"/>
    <path d="M108 168 L114 232 L118 292"/>
  </g>
  <!-- layer: 点缀（墙面 + 四点接触标记） -->
  <g id="accent">
    <path d="M168 40 L168 300" stroke="#B9C6CE" stroke-width="4" stroke-linecap="round"/>
    <g fill="#5B7A8E">
      <circle cx="130" cy="60" r="4"/>
      <circle cx="130" cy="104" r="4"/>
      <circle cx="130" cy="168" r="4"/>
      <circle cx="126" cy="290" r="4"/>
    </g>
    <g stroke="#5B7A8E" stroke-width="2" stroke-dasharray="3 4" opacity="0.65">
      <path d="M134 60 L164 60"/>
      <path d="M134 104 L164 104"/>
      <path d="M134 168 L164 168"/>
      <path d="M130 290 L164 290"/>
    </g>
  </g>
</svg>
<!-- seed: SS-slim-stretch-01.svg ｜ B-03 拉伸流 -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-03 | 名称 侧向拉伸（拉伸流动作） | 分类 纤体·拉伸 | 难度 入门 | 标签 晨间/舒缓 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（侧弯动作线条图） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="112" cy="72" r="15"/>
    <path d="M116 88 C 112 120 114 148 120 172"/>
    <path d="M114 104 C 98 88 92 64 98 44 C 102 32 110 24 118 20"/>
    <path d="M120 108 C 136 122 146 140 150 160"/>
    <path d="M120 172 C 112 210 106 248 104 292"/>
    <path d="M120 172 C 128 210 134 248 136 292"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M92 292 L116 292 M124 292 L148 292" stroke="#5B7A8E" stroke-width="3" opacity="0.4" stroke-linecap="round"/>
    <path d="M118 20 C 126 16 136 16 142 22" stroke="#5B7A8E" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-morning-01.svg ｜ B-05 晨间激活操 -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-05 | 名称 晨间激活（上举伸展） | 分类 纤体·晨间 | 难度 入门 | 标签 晨间/激活 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（伸展 + 踮脚） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="120" cy="54" r="15"/>
    <path d="M120 70 L120 164"/>
    <path d="M120 88 C 106 70 106 48 118 32"/>
    <path d="M120 88 C 134 70 134 48 122 32"/>
    <path d="M120 164 L112 226 L114 272"/>
    <path d="M120 164 L128 226 L126 272"/>
  </g>
  <!-- layer: 点缀（踮脚表现：脚跟离地 + 地面线） -->
  <g id="accent">
    <path d="M114 272 L108 284 M126 272 L120 284" stroke="#5B7A8E" stroke-width="4" opacity="0.55" stroke-linecap="round"/>
    <path d="M94 296 L150 296" stroke="#5B7A8E" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
    <path d="M166 60 C 172 48 172 36 166 24" fill="none" stroke="#5B7A8E" stroke-width="2.4" opacity="0.4" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-office-01.svg ｜ B-06 办公室拉伸 -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-06 | 名称 办公室拉伸（颈肩侧拉） | 分类 纤体·拉伸 | 难度 入门 | 标签 工位/肩颈 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（颈肩侧拉线条图） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="112" cy="64" r="15"/>
    <path d="M116 80 L120 166"/>
    <path d="M118 96 C 128 74 132 54 122 40"/>
    <path d="M116 98 C 104 124 100 148 102 170"/>
    <path d="M120 166 L114 228 L116 276"/>
    <path d="M120 166 L128 228 L126 276"/>
  </g>
  <!-- layer: 点缀（拉伸方向提示） -->
  <g id="accent">
    <path d="M92 52 C 86 46 84 38 86 30" fill="none" stroke="#5B7A8E" stroke-width="2.4" opacity="0.45" stroke-linecap="round"/>
    <path d="M118 40 L124 36" stroke="#5B7A8E" stroke-width="3.5" opacity="0.5" stroke-linecap="round"/>
    <path d="M96 296 L146 296" stroke="#5B7A8E" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-home-01.svg ｜ B-07 居家无器械训练 -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-07 | 名称 无器械深蹲 | 分类 纤体·居家 | 难度 入门 | 标签 居家/臀腿 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（侧视屈膝下蹲） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="112" cy="124" r="15"/>
    <path d="M106 140 C 100 166 98 190 96 214"/>
    <path d="M108 154 C 130 158 150 160 166 158"/>
    <path d="M110 164 C 132 170 150 172 164 170"/>
    <path d="M96 214 L140 242"/>
    <path d="M140 242 L128 292"/>
    <path d="M128 292 L158 292"/>
    <path d="M100 218 L144 248"/>
    <path d="M144 248 L134 292"/>
    <path d="M134 292 L162 292"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M46 294 L204 294" stroke="#5B7A8E" stroke-width="3" opacity="0.4" stroke-linecap="round"/>
    <path d="M84 220 C 74 242 78 262 92 272" stroke="#5B7A8E" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
    <path d="M180 118 C 190 110 196 98 196 84" stroke="#5B7A8E" stroke-width="3" opacity="0.3" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-cardio-01.svg ｜ B-08 有氧入门（快走 / 跳绳） -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-08 | 名称 跳绳有氧 | 分类 纤体·有氧 | 难度 入门 | 标签 有氧/燃脂 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（跳绳姿态） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="120" cy="78" r="15"/>
    <path d="M120 96 L120 178"/>
    <path d="M120 114 C 98 126 80 144 72 162"/>
    <path d="M120 114 C 142 126 160 144 168 162"/>
    <path d="M64 172 L76 152"/>
    <path d="M176 172 L164 152"/>
    <path d="M120 178 L106 232 L96 258"/>
    <path d="M120 178 L134 232 L144 258"/>
  </g>
  <!-- layer: 点缀 -->
  <g id="accent">
    <path d="M70 162 C 54 280 186 280 170 162" stroke="#5B7A8E" stroke-width="3" opacity="0.4" stroke-linecap="round"/>
    <path d="M56 294 L184 294" stroke="#5B7A8E" stroke-width="3" opacity="0.3" stroke-linecap="round" stroke-dasharray="6 10"/>
    <path d="M208 96 C 214 84 214 70 208 58" stroke="#5B7A8E" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-breath-01.svg ｜ B-09 呼吸训练（腹式） -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-09 | 名称 腹式呼吸训练 | 分类 纤体·呼吸 | 难度 入门 | 标签 呼吸/核心 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（盘坐腹式呼吸） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <circle cx="120" cy="88" r="15"/>
    <path d="M120 106 L120 192"/>
    <path d="M106 120 L134 120" stroke-width="5"/>
    <path d="M120 126 C 102 136 96 152 104 168"/>
    <path d="M120 126 C 138 136 144 152 136 168"/>
    <path d="M120 192 L84 208"/>
    <path d="M120 192 L156 208"/>
    <path d="M84 208 C 108 230 132 230 156 208"/>
  </g>
  <!-- layer: 点缀（腹部呼吸弧线箭头） -->
  <g id="accent">
    <path d="M112 170 C 116 182 124 184 130 180" stroke="#5B7A8E" stroke-width="3" opacity="0.5" stroke-linecap="round"/>
    <path d="M132 168 C 150 164 160 152 162 136" stroke="#5B7A8E" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
    <path d="M162 136 L154 142 M162 136 L164 146" stroke="#5B7A8E" stroke-width="3" opacity="0.45" stroke-linecap="round"/>
    <path d="M138 180 C 158 176 172 164 174 146" stroke="#5B7A8E" stroke-width="3" opacity="0.3" stroke-linecap="round"/>
    <path d="M62 240 L178 240" stroke="#5B7A8E" stroke-width="3" opacity="0.4" stroke-linecap="round"/>
  </g>
</svg>
<!-- seed: SS-slim-check-01.svg ｜ B-10 体态自测（靠墙站） -->
<svg viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <!-- meta: 编号 B-10 | 名称 靠墙体态自测 | 分类 纤体·体态 | 难度 入门 | 标签 体态/自测 -->
  <!-- palette: c-figure: #5B7A8E（运行时按诊断色系替换） -->
  <defs></defs>
  <!-- layer: 底 -->
  <g id="base">
    <rect x="8" y="8" width="224" height="304" rx="14" fill="#FAFBFD" stroke="#DFE6EC" stroke-width="1.5"/>
  </g>
  <!-- layer: 主体（靠墙侧视站姿＋墙面线） -->
  <g id="subject" fill="none" stroke="#5B7A8E" stroke-width="6" stroke-linecap="round">
    <path d="M64 40 L64 292" stroke-width="4"/>
    <circle cx="92" cy="82" r="15"/>
    <path d="M96 98 C 96 138 96 176 96 216"/>
    <path d="M98 116 C 90 142 86 168 86 192"/>
    <path d="M100 122 C 94 148 90 172 90 194"/>
    <path d="M96 216 L94 254 L92 292"/>
    <path d="M100 220 L104 256 L106 292"/>
    <path d="M92 292 L114 292"/>
  </g>
  <!-- layer: 点缀（四个体态标记点） -->
  <g id="accent">
    <circle cx="78" cy="82" r="4.5" stroke="#5B7A8E" stroke-width="3" opacity="0.55" fill="none"/>
    <circle cx="78" cy="116" r="4.5" stroke="#5B7A8E" stroke-width="3" opacity="0.55" fill="none"/>
    <circle cx="78" cy="216" r="4.5" stroke="#5B7A8E" stroke-width="3" opacity="0.55" fill="none"/>
    <circle cx="78" cy="288" r="4.5" stroke="#5B7A8E" stroke-width="3" opacity="0.55" fill="none"/>
    <path d="M64 82 L72 82 M64 116 L72 116 M64 216 L72 216 M64 288 L72 288" stroke="#5B7A8E" stroke-width="2" opacity="0.4" stroke-linecap="round"/>
  </g>
</svg>
