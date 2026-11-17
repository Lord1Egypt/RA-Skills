# teaching-modes.md — 四维教学闭环设计（状态机 + SOP + 考核）

> 防止产出"只能旋转看的 3D 玩具"的核心。每个系统必须具备：真实工卡步骤校验、防呆报警、虚拟仪表测量、理论实操评分。

## §1 四维教学闭环结构

| 维度 | 内容 | UI 位置 | 必做程度 |
|---|---|---|---|
| 1. 结构认知与拆解 | 部件树点选 → 3D 聚焦 + 详情卡（名称/材质参数/工程描述）+ 爆炸视图 | 左栏 | 必做 |
| 2. 原理与动态仿真 | 参数滑块驱动动态过程 + 实时 KPI + 曲线图（Canvas 2D） | 右栏 | 原理型必做 |
| 3. 标准 SOP 工卡实操 | 分步骤卡（完成判据 checkFn + 一键演示 autoAct）+ 教学模式按钮 | 左/右栏 | 实操型必做 |
| 4. 故障排故与考核 | 故障注入器 + 仪表测量验证 + 评分扣分 + 评价单弹窗 | 右栏/顶栏 | 考核型必做 |

三种产品形态按需裁剪，但**至少要有 1 + 3 或 1 + 2**：
- **原理仿真型**：1 + 2（+ 轻量 4）——如内燃机（P-V 图/相位盘/波形 + 参数实验）
- **SOP 实操型**：1 + 3 + 4——如 Model Y（模块化工卡 + 万用表验证 + 评分）
- **场景漫游型**：1 + 3 变体（工位制）——如安检（nav-tabs 六大岗位 + 题库考核）

## §2 全局状态机（SimState 模板）

```js
const SimState = {
  // —— 播放控制 ——
  playing: true,
  angleDeg: 45.0,          // 业务主相位（曲轴角/传送带进度/时刻）
  speedFactor: 1.0,
  rpm: 1200,               // 业务主速度参数

  // —— 视图状态 ——
  explode: 0.0,            // 爆炸视图 0..1
  shellOpacity: 0.78,      // 外壳透明度 0..1
  showLabels: true,        // 2D 引线标注
  showVectors: true,       // 力矢量/流向显示
  wireframeMode: false,
  showParticles: true,
  soundEnabled: false,
  autoOrbit: false,

  // —— 拾取状态 ——
  selectedPart: null,
  hoveredPart: null,

  // —— 教学闭环状态 ——
  mode: 'teach',           // 'teach' 教学引导 | 'practice' 自由排故 | 'exam' 考核
  currentModuleIdx: 0,     // 当前实训模块
  score: 100,              // 考核得分（只扣不加）
  safetyViolations: [],    // 违章记录 ['[-20分] 未穿戴绝缘手套接触高压部件', ...]
  operationLogs: [],       // 操作日志（评价单展示最近 8 条）
  elapsedSec: 0,           // 实训计时

  // —— 业务开关（SOP 步骤完成判据位，按需扩展）——
  ppe: { gloves: false, goggles: false, shoes: false, sign: false },
  verifiedZeroVolt: false,
  measuredHvilIn: false,
  // ...
};
```

## §3 实训模块 + SOP 工卡（Model Y 模式全量模板）

```js
const TRAINING_MODULES = [
  {
    num: '模块一',
    title: '高压安全与下电流程',
    subtitle: 'PPE穿戴、断电与验电',
    stdTag: 'GB/T 18384 & 企业SOP',           // 展示的国标/规范号
    knowledgeHtml: `
      <ul>
        <li><strong>Step 1 场地与PPE：</strong>布置警示桩链，穿戴绝缘手套（气密检测合格）、防电弧面屏与绝缘靴。</li>
        <li><strong>Step 2 低压断电：</strong>中控关电 → 拔检修开关 → 断开12V蓄电池负极。</li>
        <li><strong>Step 3 验电：</strong>静置≥5分钟泄放电容，万用表DCV档测 HV+对HV- 确认 0.0V。</li>
      </ul>`,
    faultToLoad: null,
    cameraPreset: 'iso',
    steps: [
      {
        title: '为3D技师穿戴全套PPE并布置围栏',
        desc: '点击底部工具坞依次穿戴：绝缘手套、防电弧面屏、绝缘靴，布置警示桩链。',
        btnText: '一键穿戴PPE并布置围栏',            // 教学模式的辅助按钮
        checkFn: (s) => s.ppe.gloves && s.ppe.goggles && s.ppe.shoes && s.ppe.sign,   // ★ 完成判据
        autoAct: () => { equipAllPPE(); }             // ★ 一键演示（考核模式隐藏）
      },
      {
        title: '万用表 DCV 交叉 0V 验电',
        desc: '万用表选 DCV 档，红表笔接 HV+，黑表笔接 HV-，确认读数 0.0V 后点【记录测量数据】。',
        btnText: '执行验电测量',
        checkFn: (s) => s.verifiedZeroVolt,
        autoAct: () => { performZeroVoltCheck(); }
      }
      // 每模块 3~8 步
    ]
  }
  // 4~6 个模块覆盖完整岗位流程
];
```

**SOP 步骤卡渲染 + 三模式切换**：

```js
function renderSopSteps() {
  const mod = TRAINING_MODULES[SimState.currentModuleIdx];
  const container = document.getElementById('sopStepContainer');
  let firstIncompleteFound = false;
  container.innerHTML = mod.steps.map((s, idx) => {
    const done = s.checkFn(SimState);                    // ★ 每次重渲染实时校验
    let stateClass = '', statusLabel = '待操作';
    if (done) { stateClass = 'completed'; statusLabel = '✓ 已完成'; }
    else if (!firstIncompleteFound) { stateClass = 'current'; statusLabel = '▶ 当前步骤'; firstIncompleteFound = true; }

    const showAutoBtn = SimState.mode !== 'exam' && !done;   // ★ 考核模式隐藏一键按钮
    return `
      <div class="step-item ${stateClass}">
        <div class="step-top">
          <span class="step-badge">步骤 ${idx + 1} / ${mod.steps.length}</span>
          <span style="color:${done ? '#34d399' : '#38bdf8'};">${statusLabel}</span>
        </div>
        <div class="step-title">${s.title}</div>
        <div class="step-desc">${s.desc}</div>
        ${showAutoBtn ? `<button class="step-action-btn" onclick="runStepAutoAction(${idx})">⚡ ${s.btnText}</button>` : ''}
      </div>`;
  }).join('');
}

// 步骤完成后自动触发重渲染：在所有改变状态的操作函数末尾调用 renderSopSteps()
function runStepAutoAction(stepIdx) {
  const step = TRAINING_MODULES[SimState.currentModuleIdx].steps[stepIdx];
  if (step && step.autoAct) { step.autoAct(); renderSopSteps(); }
}
```

## §4 安全互锁与扣分（防呆报警核心）

**一票否决式安全红线**——危险操作前检查前置条件，不满足即扣分 + 弹窗 + 报警音：

```js
function deductScore(points, reason) {
  SimState.score = Math.max(0, SimState.score - points);
  SimState.safetyViolations.push(`[-${points}分] ${reason}`);
  document.getElementById('scoreVal').textContent = SimState.score;
  logAction(`⚠️ 扣分提醒 (-${points}分)：${reason}`);
}

function triggerSafetyViolation(msg, points) {
  deductScore(points, msg);
  playSynthSound('alarm');
  openModal({
    danger: true,
    title: '⚡ 安全红线告警（违反 GB/T XXXXX 规范）',
    body: `
      <div style="padding:12px;background:rgba(239,68,68,0.18);border:1px solid #ef4444;border-radius:8px;">
        <strong style="color:#fca5a5;">${msg}</strong>
      </div>
      <p><strong>岗位安全考核一票否决规范：</strong></p>
      <ul>${SAFETY_RULES.map(r => `<li>${r}</li>`).join('')}</ul>`
  });
}

// 用法示例：接触高压部件前检查手套
function touchHvComponent() {
  if (!SimState.ppe.gloves) {
    triggerSafetyViolation('未穿戴1000V绝缘手套接触橙色高压线束！', 30);
    return;
  }
  // ……正常操作
}
```

## §5 虚拟仪器矩阵 + 遥测条（**P1 必需，缺项不得交付**）

> irb_6700 高分验证：仪器矩阵是"内容完善度"的最大感知来源。以下四件套**全部必须实现**：
> ① 万用表 4 模式 ② 双通道示波器 ③ 五维能力雷达 ④ 底部遥测条。

### 5.1 万用表 4 模式（testPoints 数据驱动）

读数直接来自部件的 `testPoints`（正常/故障双值，契约见 domain-data.md §1），
故障注入切换到该部件的 Fault 值，LOTO 断电时电压/电流读 0：

```js
function updateDmmDisplay() {
  const comp = SIM_CONFIG.components.find(c => c.id === state.probeRed) || SIM_CONFIG.components[0];
  const tp = comp.testPoints;
  const activeFault = SIM_CONFIG.faults.find(f => f.id === state.activeFaultId);
  const isFaultedComp = activeFault && activeFault.targetComp === comp.id;

  let val = 0, unit = 'V DC', isAbnormal = false;
  const jitter = Math.sin(state.simTime * 5.3) * 0.02;   // 实时微抖，防"死板"

  if (state.dmmMode === 'V') {
    if (state.powerOff && comp.id !== 'comp_harness') val = 0.00;   // LOTO 断电读零（编码器电池回路除外）
    else { val = (isFaultedComp ? tp.vFault : tp.vNorm) + jitter;
           if (isFaultedComp && Math.abs(tp.vFault - tp.vNorm) > 1.0) isAbnormal = true; }
    unit = 'V DC';
  } else if (state.dmmMode === 'OHM') {
    val = (isFaultedComp ? tp.ohmFault : tp.ohmNorm) + jitter * 0.5;
    if (isFaultedComp && Math.abs(tp.ohmFault - tp.ohmNorm) > 5.0) isAbnormal = true;
    unit = 'Ω';
  } else if (state.dmmMode === 'MOHM') {
    val = isFaultedComp ? tp.mohmFault : tp.mohmNorm;
    if (isFaultedComp && tp.mohmFault < 10.0) isAbnormal = true;
    unit = 'MΩ (500V)';
  } else if (state.dmmMode === 'AMP') {
    if (state.powerOff) val = 0.00;
    else { val = (isFaultedComp ? tp.ampFault : tp.ampNorm) + Math.sin(state.simTime * 4.0) * 0.35;
           if (isFaultedComp && Math.abs(tp.ampFault - tp.ampNorm) > 3.0) isAbnormal = true; }
    unit = 'A RMS';
  }
  const lcd = document.getElementById('dmm-lcd');
  lcd.className = 'dmm-lcd' + (isAbnormal ? ' fault-lcd' : '');   // 异常红显
  document.getElementById('dmm-val-text').textContent = val >= 100 ? val.toFixed(1) : val.toFixed(2);
  document.getElementById('dmm-unit-text').textContent = unit;
}
```

- **表笔选择**：红表笔 `sel-probe-red` = 全部部件（`SIM_CONFIG.components.map` 生成 options）；
  黑表笔 `sel-probe-black` = 参考点（PE 保护地 / DC-Bus 0V / 编码器屏蔽壳，按设备改）。
- **档位按钮组**：`data-dmm="V|OHM|MOHM|AMP"` ≥3 个（audit 检测）。
- 选中部件即红表笔搭接（selectComponent 同步 probeRed），左栏点部件 ↔ 万用表联动。

### 5.2 双通道示波器 + 五维能力雷达（同一 canvas 切换）

```js
// 波形采样在 updateRobotKinematics/stepSimulation 里 push，>90 样本 shift
state.waveHistoryA.push(wA); state.waveHistoryB.push(wB);

// 五维能力：机械拆装/运动学标定(或原理识读)/电气测量/SOP安全/故障排故
// SOP 完成 +3~+4，答对 quiz +8，答错/违章 -5~-6（下限 40）
const skills = [86, 84, 82, 88, 80];   // 初始基准分
```

雷达图 Canvas 2D：五边形网格 3 圈（0.35/0.7/1.0）+ 数据多边形半透明填充 + 轴向标签（`600 10px` 字体）。

### 5.3 底部遥测条（telemetry strip，**P1 必需**）

底部横条 4–6 项实时指标，每项有 `id="tele-xxx"`（audit 检测前缀 `tele-`），故障态变色：

```html
<footer class="telemetry-strip">
  <div class="tele-metrics">
    <div class="tele-item">工况模式:<span id="tele-cond">圆弧焊接轨迹</span></div>
    <div class="tele-item">TCP空间坐标:<span id="tele-tcp">X:+1120 Y:+420 Z:+680 mm</span></div>
    <div class="tele-item">二轴伺服相电流:<span id="tele-curr">11.4 A</span></div>
    <div class="tele-item">直流母线电压:<span id="tele-bus">540.0 V</span></div>
    <div class="tele-item">重复定位误差:<span id="tele-err">±0.020 mm</span></div>
  </div>
  <div style="color:#64748b; font-size:11px;">左键旋转 · 右键平移 · 滚轮缩放 · 点击3D标签定位</div>
</footer>
```

主循环每 6 帧刷新（`uiTick % 6 === 0`），故障激活时给对应 span 加 `.danger` class 红显：
```js
const currEl = document.getElementById('tele-curr');
currEl.textContent = `${curr.toFixed(1)} A`;
currEl.className = isBrakeFault ? 'danger' : '';
```

**设备适配**：机械臂=TCP 坐标/伺服电流/母线电压/定位误差；车辆=车速/SOC/电机温度/挡位；
动力机械=转速/油温/排温/负载率；航空器=空速/高度/航向/推力。

### 5.4 场景型设备的端子枚举读数公式表（无 testPoints 时适用）

对于安检/空港/客舱等场景型设备，保留端子枚举公式表写法：

```js
const METER_MODES = { dcv: 'DCV 电压档', acv: 'ACV 电压档', ohm: 'Ω 电阻档', diode: '二极管档' };

const PROBE_POINTS = [
  { id: 'HV_PLUS',  label: 'Penthouse HV+',  pos: [0.42, 0.28, -0.3] },
  { id: 'HV_MINUS', label: 'Penthouse HV-',  pos: [0.42, 0.28, -0.1] },
  { id: 'HVIL_IN',  label: 'HVIL 输入端',    pos: [1.28, 0.1, -0.1] },
  // …按业务列出所有可测端子，pos 供 3D 表笔尖端吸附
];

function updateMultimeterReading() {
  const s = SimState;
  let reading = 'OL';   // 默认过载
  const key = `${s.probeRed}|${s.probeBlack}|${s.meterMode}|${s.activeFault || 'NONE'}`;

  // ★ 读数公式表：穷举 (红笔, 黑笔, 档位, 故障态) → 真实读数
  if (s.meterMode === 'dcv' && s.probeRed === 'HV_PLUS' && s.probeBlack === 'HV_MINUS') {
    reading = s.systemLive ? '407.3 V' : '0.0 V';
    if (s.activeFault === 'HVIL_OPEN') reading = '0.0 V';
  }
  if (s.meterMode === 'ohm' && s.probeRed === 'RES_R' && s.probeBlack === 'RES_S') {
    reading = s.activeFault === 'RES_OPEN' ? 'OL ∞' : '10.2 Ω';
  }
  // …
  document.getElementById('meterDisplay').textContent = reading;

  // 测量结果联动 SOP 校验位
  if (reading === '0.0 V' && s.meterMode === 'dcv') s.verifiedZeroVolt = true;
}

// 点击 3D 端子或端子列表 → 表笔自动搭接 + 3D 技师走过去 + 表笔尖端吸附到端子 pos
function connectProbe(pointId, which) {
  SimState[which] = pointId;
  const pt = PROBE_POINTS.find(p => p.id === pointId);
  SimState.techTargetPos = [pt.pos[0] + 0.5, pt.pos[2] + 0.35];   // 技师移到端子附近（包围盒外）
  updateMultimeterReading();
  renderSopSteps();
}
```

**示波器波形**（Canvas 2D，参照样本画三相正弦/PWM）：

```js
function drawScope(ctx, viewW, viewH, signals) {
  ctx.clearRect(0, 0, viewW, viewH);
  const colors = ['#38bdf8', '#f59e0b', '#34d399'];
  signals.forEach((sig, idx) => {
    ctx.beginPath();
    for (let x = 0; x < viewW; x += 2) {
      const y = viewH * 0.5 + sig.amp * Math.sin(x * sig.freq + animTick * sig.speed + idx * (Math.PI * 2 / signals.length)) * (viewH * 0.4);
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.strokeStyle = colors[idx];
    ctx.lineWidth = 1.6;
    ctx.stroke();
  });
}
```

## §6 故障注入器（排故训练核心）

```js
const FAULT_LIBRARY = [
  {
    id: 'HVIL_OPEN',
    name: '高压互锁回路断路（HVIL 退针）',
    symptom: '上电READY失败，仪表提示"电力系统故障"',
    effects: { systemLive: false, hvilOutVoltage: 0 },
    truth: '万用表DCV测 HVIL_IN=9.6V 而 HVIL_OUT=0.0V → 判断互锁回路中断'
  },
  {
    id: 'RES_OPEN',
    name: '电机旋变信号线圈断路',
    symptom: '起步抖动限功率',
    effects: { resSShort: true },
    truth: '万用表Ω档：R1-R2=10.2Ω正常，S1-S3=OL∞ → 正弦线圈断路'
  }
  // 6~10 个典型故障
];

function injectFault(faultId) {
  SimState.activeFault = faultId;
  const f = FAULT_LIBRARY.find(x => x.id === faultId);
  if (f) {
    Object.assign(SimState, f.effects);       // 应用物理效果
    logAction(`🔧 已注入故障：【${f.name}】${f.symptom}`);
    updateMultimeterReading();                // 所有仪表立即联动
    renderObdPanel();
    renderSopSteps();
  }
}

function clearFault() {
  SimState.activeFault = null;
  const f0 = {};   // 恢复默认
  // …重置 effects 字段
  logAction('✅ 已清除全部故障，系统恢复正常。');
  updateMultimeterReading();
}
```

## §7 考核评价单（交付标配）

```js
function openScoreReportModal() {
  const completedCount = TRAINING_MODULES.reduce((acc, m) =>
    acc + m.steps.filter(s => s.checkFn(SimState)).length, 0);
  const totalSteps = TRAINING_MODULES.reduce((acc, m) => acc + m.steps.length, 0);
  const violationsHtml = SimState.safetyViolations.length === 0
    ? '<li style="color:#34d399;">零违章记录：严格遵守安全操作规范</li>'
    : SimState.safetyViolations.map(v => `<li style="color:#fca5a5;">${v}</li>`).join('');

  openModal({
    title: '📊 虚拟仿真实训考核评价单',
    body: `
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px;">
        <div class="report-card"><div>综合实训得分</div><div class="big">${SimState.score} 分</div></div>
        <div class="report-card"><div>工序完成进度</div><div class="big">${completedCount} / ${totalSteps}</div></div>
        <div class="report-card"><div>实训用时</div><div class="big" id="timerVal">00:00</div></div>
      </div>
      <h4>一、安全与岗位规范记录：</h4><ul>${violationsHtml}</ul>
      <h4>二、最近实操测量与诊断日志：</h4>
      <div style="max-height:130px;overflow-y:auto;font-family:monospace;font-size:11px;">
        ${SimState.operationLogs.slice(-8).reverse().map(l => `<div>${l}</div>`).join('')}
      </div>`
  });
}

// 计时器
setInterval(() => {
  SimState.elapsedSec++;
  const m = String(Math.floor(SimState.elapsedSec / 60)).padStart(2, '0');
  const s = String(SimState.elapsedSec % 60).padStart(2, '0');
  const el = document.getElementById('timerVal');
  if (el) el.textContent = `${m}:${s}`;
}, 1000);

// 操作日志（单行滚动显示在底部或顶部）
function logAction(text) {
  const ts = new Date().toTimeString().split(' ')[0];
  SimState.operationLogs.push(`[${ts}] ${text}`);
  const ticker = document.getElementById('systemLogTicker');
  if (ticker) ticker.textContent = `[${ts}] ${text}`;
}
```

## §8 场景型题库考核（安检模式变体）

场景型项目（安检/验证/判图）用"情境题 + 选项 + 解析"：

```js
const EXAM_BANK = [
  {
    q: '旅客出示居民身份证已过有效期（2026.01.01 到期，今日 2026.10.15），人证票相符。应如何处置？',
    options: ['正常放行', '拒绝乘机并指引办理临时乘机证明', '罚款后放行', '要求出示社保卡'],
    answer: 1,
    explanation: '【考核解析】已过有效期的身份证属无效乘机证件，不得放行！应指引旅客通过"民航临时乘机证明"小程序或机场公安制证点办理。'
  }
  // 10~20 题
];

function answerExam(qIdx, optIdx) {
  const q = EXAM_BANK[qIdx];
  const fb = document.getElementById('examFeedback');
  if (optIdx === q.answer) {
    fb.innerHTML = `✅ <strong>正确。</strong>${q.explanation}`;
    playSynthSound('beep');
  } else {
    fb.innerHTML = `❌ <strong>错误。</strong>${q.explanation}`;
    deductScore(10, '理论题答错：' + q.q.slice(0, 20) + '…');
  }
}
```

## §9 领域 SOP 素材速查（写文案时参考，禁止编造规程）

| 领域 | 规范依据 | 典型红线（一票否决） |
|---|---|---|
| 新能源车维修 | GB/T 18384、特斯拉 Toolbox SOP | 未戴绝缘手套碰橙色高压线；未验电拆高压部件 |
| 民航机务 | AMM 手册、CCAR-66 | 未挂安全牌操作；工具遗留舱内 |
| 民航安检 | CCAR-329、安检五级教材 | 漏检违禁品放行；未复检报警部位 |
| 客舱乘务 | CCAR-121、各航司客舱手册 | 滑梯误放；起降未调暗灯光 |
| 内燃机 | GB/T 1147 | 运转中打开水箱盖；无防护接触传动件 |
| 无人机 | CAAC 实名登记、禁飞区规定 | 禁飞区起飞；超视距无监护 |

> 文案必须使用行业标准术语（如"预位/解除预位""验电""互锁回路"），禁止口语化改写规程原文。不确定的规程表述先 WebSearch 核实。
