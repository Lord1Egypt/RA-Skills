/**
 * survey-config.js — global Survey 全局配置
 *
 * ============================================================
 * 🎯 最简配置（只需 3 步，5 分钟完成）
 * ============================================================
 *
 * 1. 引入本文件
 * 2. 设置 productName + tasks（见下方最小示例）
 * 3. 引入 survey.js
 *
 * 最小配置示例（复制下面的代码即可）：
 *
 * <script src="survey-config.js"></script>
 * <script>
 *   window.SURVEY_CONFIG = {
 *     productName: '我的产品',
 *     tasks: [
 *       { id: 'T1', label: '完成注册',    detect: 'signup_done'    },
 *       { id: 'T2', label: '完成下单',    detect: 'order_done'    },
 *       { id: 'T3', label: '完成支付',    detect: 'payment_done'  }
 *     ]
 *   };
 * </script>
 * <script src="survey.js"></script>
 *
 * ============================================================
 * 📋 配置速查表
 * ============================================================
 *
 * 字段         | 类型    | 必填 | 说明
 * -------------|---------|------|------
 * productName  | string  | 否   | 产品名称（默认"本产品"）
 * tasks        | array   | 否   | 任务列表（默认 Tideo 3 任务）
 * checkpoints  | array   | 否   | 情境问卷（默认内置 4 个）
 * testVideoUrl | string  | 否   | 测试素材地址（默认 assets/test-video.mov）
 *
 * task 对象格式：
 *   { id: 'T1', label: '任务描述', hint: '提示文字(可选)', detect: 'milestone名称' }
 *
 * checkpoint 对象格式：
 *   { id:'id', trigger:'milestone名', delay:1500, type:'rating'|'sam',
 *     question:'问题', scale:5, labels:['左','右'],
 *     allowComment:true, commentPH:'占位文字' }
 *   或 SAM 型：
 *   { id:'id', trigger:'milestone名', delay:1500, type:'sam',
 *     question:'问题', dims:[{id,label,l:'左',r:'右'}] }
 *
 * ============================================================
 * 完整配置示例
 * ============================================================
 */

window.SURVEY_CONFIG = window.SURVEY_CONFIG || {};

/**
 * ==================== 产品信息 ====================
 */

/** 产品名称（用于问卷中的文案） */
window.SURVEY_CONFIG.productName = window.SURVEY_CONFIG.productName || '本产品';

/** 测试素材下载地址（欢迎页下载按钮指向） */
window.SURVEY_CONFIG.testVideoUrl = window.SURVEY_CONFIG.testVideoUrl || 'assets/test-video.mov';

/** 测试素材文件名（用于下载按钮显示） */
window.SURVEY_CONFIG.testVideoLabel = window.SURVEY_CONFIG.testVideoLabel || 'test-video.mov';

/** 测试素材文件大小（用于下载按钮显示） */
window.SURVEY_CONFIG.testVideoSize = window.SURVEY_CONFIG.testVideoSize || '2.4MB';

/**
 * ==================== 任务定义 ====================
 * 
 * tasks — 任务列表（内部测试模式）
 * 
 * 每个任务对象：
 *   id       — 唯一标识符（字符串）
 *   label    — 任务描述（显示给用户）
 *   hint     — 任务提示（可选，内部模式显示）
 *   detect   — 对应的 milestone 名称（用户完成此任务时触发的 milestone）
 * 
 * detect 字段对应 tracker.js 的 milestone 名称（经 TRACKER_CONFIG.getMilestone 映射后）
 */
window.SURVEY_CONFIG.tasks = window.SURVEY_CONFIG.tasks || null; // null = 使用下方默认值

/** 默认内部测试任务（Tideo 特定） */
window.SURVEY_CONFIG.DEFAULT_TASKS_INTERNAL = [
  { id: 'T1', label: '把一个视频翻译成英文', hint: '用你觉得合适的方式完成', detect: 'mps_complete' },
  { id: 'T2', label: '对翻译结果做一些修改', hint: '比如改条字幕、调个区域', detect: 'finetune_edit' },
  { id: 'T3', label: '把最终结果导出', hint: '下载你满意的版本', detect: 'export' }
];

/** 默认外部用户任务 */
window.SURVEY_CONFIG.DEFAULT_TASKS_USER = [
  { id: 'T1', label: '把这个视频翻译成中文', hint: '', detect: 'mps_complete' },
  { id: 'T2', label: '下载翻译好的视频', hint: '', detect: 'export' }
];

/**
 * ==================== 情境问卷（Checkpoint）====================
 * 
 * checkpoints — 情境嵌入式微问卷配置（内部测试模式）
 * 
 * 每个 checkpoint 对象：
 *   id        — 唯一标识符
 *   trigger   — 触发的 milestone 名称（经映射后）
 *   delay     — 延迟显示时间（ms，默认 1000）
 *   type      — 'rating'（李克特评分）或 'sam'（SAM 情绪模型）
 *   question  — 问题文本
 *   scale     — rating 模式的分值数量（5 或 7）
 *   labels    — rating 模式的两端标签 [左, 右]
 *   allowComment — rating 模式是否显示评论框（布尔）
 *   commentPH   — 评论框 placeholder 文本
 *   dims      — sam 模式的多维度配置 [{id, label, l, r}, ...]
 */
window.SURVEY_CONFIG.checkpoints = window.SURVEY_CONFIG.checkpoints || null; // null = 使用默认值

/** 默认内部测试 Checkpoint */
window.SURVEY_CONFIG.DEFAULT_CP_INTERNAL = [
  {
    id: 'upload_ease',
    trigger: 'upload_done',
    delay: 1500,
    type: 'rating',
    question: '刚才找到上传入口顺利吗？',
    scale: 5,
    labels: ['很困难', '有点绕', '还行', '比较顺', '一下就找到了'],
    allowComment: true,
    commentPH: '在哪卡住过？（可选）'
  },
  {
    id: 'wait_sam',
    trigger: 'processing_wait_30s',
    delay: 500,
    type: 'sam',
    question: '等 AI 处理的这段时间感觉怎样？',
    dims: [
      { id: 'arousal', label: '紧张程度', l: '很放松', r: '很焦虑' },
      { id: 'valence', label: '心情', l: '不太好', r: '挺好的' }
    ]
  },
  {
    id: 'result_sam',
    trigger: 'result_viewed',
    delay: 3000,
    type: 'sam',
    question: '看到 AI 处理的结果，感觉如何？',
    dims: [
      { id: 'valence', label: '满意程度', l: '不满意', r: '很满意' },
      { id: 'dominance', label: '掌控感', l: '不知道怎么调', r: '我知道怎么改' }
    ]
  },
  {
    id: 'finetune_ease',
    trigger: 'step_edited',
    delay: 1500,
    type: 'rating',
    question: '刚才修改结果的操作顺利吗？',
    scale: 5,
    labels: ['完全不会', '有点绕', '还行', '比较顺', '很容易'],
    allowComment: true,
    commentPH: '哪个操作让你卡住了？（可选）'
  }
];

/** 默认外部用户 Checkpoint */
window.SURVEY_CONFIG.DEFAULT_CP_USER = [
  {
    id: 'upload_ease',
    trigger: 'upload_done',
    delay: 2000,
    type: 'rating',
    question: '上传视频顺利吗？',
    scale: 5,
    labels: ['很困难', '有点绕', '还行', '比较顺', '一下就找到了'],
    allowComment: false
  },
  {
    id: 'result_quality',
    trigger: 'result_viewed',
    delay: 3000,
    type: 'rating',
    question: '翻译的效果你满意吗？',
    scale: 5,
    labels: ['很不满意', '不太行', '一般', '还不错', '很满意'],
    allowComment: true,
    commentPH: '哪里满意/不满意？'
  }
];

/**
 * ==================== 欢迎页文案 ====================
 */
window.SURVEY_CONFIG.welcomeInternal = window.SURVEY_CONFIG.welcomeInternal || {
  title: '感谢参与可用性测试',
  subtitle: '{productName} 是一个 AI 视频翻译工具，可以自动将视频翻译成其他语言。我们希望通过你的真实操作体验，发现产品的易用性问题。',
  note: '请像第一次使用一个新产品一样自然操作。没有对错之分，你遇到的任何困惑都是我们需要改进的地方。过程中会在关键节点弹出简短问卷，请如实作答。',
  estimatedTime: '5-8 分钟'
};

window.SURVEY_CONFIG.welcomeUser = window.SURVEY_CONFIG.welcomeUser || {
  title: '感谢参与体验测试',
  subtitle: '请使用 {productName} 将一段视频翻译成中文，并下载翻译后的结果。',
  note: '请像平时使用新产品一样自然操作。过程中会弹出几个简短问题，请如实作答。',
  estimatedTime: '5-8 分钟'
};

/**
 * ==================== 总结问卷文案 ====================
 */

/** NPS 问题中的产品名称（默认使用 productName） */
window.SURVEY_CONFIG.npsQuestionProduct = window.SURVEY_CONFIG.npsQuestionProduct || null;

/** 总结问卷开放题 — 最困惑的地方（默认文案） */
window.SURVEY_CONFIG.openQuestion1 = window.SURVEY_CONFIG.openQuestion1 || '使用过程中最困惑/卡住的地方是什么？';

/** 总结问卷开放题 — 最有价值的地方（默认文案） */
window.SURVEY_CONFIG.openQuestion2 = window.SURVEY_CONFIG.openQuestion2 || '你觉得 {productName} 最有价值的功能是什么？';

/**
 * ==================== 工具函数 ====================
 */

/**
 * 获取最终使用的 tasks 数组
 * 优先级：用户配置 > 默认值
 */
window.SURVEY_CONFIG.getTasks = function(isInternal) {
  if (this.tasks && this.tasks.length) return this.tasks;
  return isInternal ? this.DEFAULT_TASKS_INTERNAL : this.DEFAULT_TASKS_USER;
};

/**
 * 获取最终使用的 checkpoints 数组
 * 优先级：用户配置 > 默认值
 */
window.SURVEY_CONFIG.getCheckpoints = function(isInternal) {
  if (this.checkpoints && this.checkpoints.length) return this.checkpoints;
  return isInternal ? this.DEFAULT_CP_INTERNAL : this.DEFAULT_CP_USER;
};

/**
 * 替换文案中的 {productName} 占位符
 */
window.SURVEY_CONFIG.interpolate = function(str) {
  if (!str) return '';
  return str.replace(/\{productName\}/g, this.productName || '本产品');
};
