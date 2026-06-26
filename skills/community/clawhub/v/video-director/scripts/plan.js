#!/usr/bin/env node
/**
 * Video Director - 画面规划脚本
 * 输入：主题 + 要点
 * 输出：标准JSON格式的分镜数据
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  fps: 30,
  width: 1080,
  height: 1920,
  charsPerSecond: 4.5
};

const log = (msg) => console.log('[' + new Date().toLocaleTimeString() + '] ' + msg);

const nounVisualMap = {
  'AI': { emoji: '🤖', type: 'emoji' },
  '机器人': { emoji: '🤖', type: 'emoji' },
  '技能': { emoji: '⚡', type: 'emoji' },
  '目标': { emoji: '🎯', type: 'emoji' },
  '手机': { emoji: '📱', type: 'emoji' },
  '视频': { emoji: '🎬', type: 'emoji' },
  '工具': { emoji: '🔧', type: 'emoji' },
  '学习': { emoji: '📖', type: 'emoji' },
  '赚钱': { emoji: '💰', type: 'emoji' },
  '时间': { emoji: '⏰', type: 'emoji' },
  '数据': { emoji: '📊', type: 'emoji' },
  '设计': { emoji: '🎨', type: 'emoji' },
  '代码': { emoji: '💻', type: 'emoji' },
  '程序员': { emoji: '👨‍💻', type: 'emoji' },
  '创意': { emoji: '💡', type: 'emoji' },
  '成功': { emoji: '✅', type: 'emoji' },
  '升级': { emoji: '🚀', type: 'emoji' },
  '用户': { emoji: '👤', type: 'emoji' },
  '人物': { emoji: '👤', type: 'emoji' },
  '系统': { emoji: '⚙️', type: 'emoji' },
  '功能': { emoji: '⚡', type: 'emoji' },
  '平台': { emoji: '🌐', type: 'emoji' },
  '应用': { emoji: '📱', type: 'emoji' },
  '软件': { emoji: '💿', type: 'emoji' },
  '网络': { emoji: '🌐', type: 'emoji' },
  '安全': { emoji: '🔒', type: 'emoji' },
  '速度': { emoji: '⚡', type: 'emoji' },
  '效率': { emoji: '📈', type: 'emoji' },
  '问题': { emoji: '❓', type: 'emoji' },
  '解决': { emoji: '✅', type: 'emoji' },
  '开始': { emoji: '🚀', type: 'emoji' },
  '结束': { emoji: '🏁', type: 'emoji' },
  '重点': { emoji: '📌', type: 'emoji' },
  '注意': { emoji: '⚠️', type: 'emoji' },
  '提示': { emoji: '💡', type: 'emoji' },
  '示例': { emoji: '📝', type: 'emoji' },
  '步骤': { emoji: '1️⃣', type: 'emoji' },
  '方法': { emoji: '📋', type: 'emoji' },
  '技巧': { emoji: '🎯', type: 'emoji' },
  '优势': { emoji: '⭐', type: 'emoji' },
  '缺点': { emoji: '❌', type: 'emoji' },
  '对比': { emoji: '⚖️', type: 'emoji' },
  '选择': { emoji: '✓', type: 'emoji' },
  '推荐': { emoji: '👍', type: 'emoji' },
  '必看': { emoji: '👀', type: 'emoji' },
  '干货': { emoji: '💎', type: 'emoji' },
  '教程': { emoji: '📚', type: 'emoji' },
  '案例': { emoji: '📁', type: 'emoji' },
  '实战': { emoji: '⚔️', type: 'emoji' },
  '项目': { emoji: '📁', type: 'emoji' },
  '开发': { emoji: '💻', type: 'emoji' },
  '测试': { emoji: '🧪', type: 'emoji' },
  '部署': { emoji: '🚀', type: 'emoji' },
  '优化': { emoji: '⚡', type: 'emoji' },
  '性能': { emoji: '📊', type: 'emoji' },
  '架构': { emoji: '🏗️', type: 'emoji' },
  '框架': { emoji: '🔧', type: 'emoji' },
  '库': { emoji: '📦', type: 'emoji' },
  'API': { emoji: '🔌', type: 'emoji' },
  '接口': { emoji: '🔌', type: 'emoji' },
  '数据库': { emoji: '🗄️', type: 'emoji' },
  '服务器': { emoji: '🖥️', type: 'emoji' },
  '客户端': { emoji: '💻', type: 'emoji' },
  '前端': { emoji: '🎨', type: 'emoji' },
  '后端': { emoji: '⚙️', type: 'emoji' },
  '全栈': { emoji: '🔄', type: 'emoji' },
  '算法': { emoji: '🧮', type: 'emoji' },
  '模型': { emoji: '🤖', type: 'emoji' },
  '训练': { emoji: '🏋️', type: 'emoji' },
  '预测': { emoji: '🔮', type: 'emoji' },
  '分析': { emoji: '📊', type: 'emoji' },
  '可视化': { emoji: '📈', type: 'emoji' },
  '报告': { emoji: '📄', type: 'emoji' },
  '文档': { emoji: '📄', type: 'emoji' },
  '配置': { emoji: '⚙️', type: 'emoji' },
  '环境': { emoji: '🌍', type: 'emoji' },
  '版本': { emoji: '📌', type: 'emoji' },
  '更新': { emoji: '🔄', type: 'emoji' },
  '发布': { emoji: '🚀', type: 'emoji' },
  '维护': { emoji: '🔧', type: 'emoji' },
  '监控': { emoji: '👁️', type: 'emoji' },
  '日志': { emoji: '📝', type: 'emoji' },
  '错误': { emoji: '❌', type: 'emoji' },
  '调试': { emoji: '🔍', type: 'emoji' },
  '修复': { emoji: '🔧', type: 'emoji' },
  '重构': { emoji: '🔄', type: 'emoji' },
  '质量': { emoji: '⭐', type: 'emoji' },
  '规范': { emoji: '📋', type: 'emoji' },
  '最佳实践': { emoji: '✨', type: 'emoji' },
  '模式': { emoji: '🎨', type: 'emoji' },
  '原则': { emoji: '📐', type: 'emoji' },
  '经验': { emoji: '💡', type: 'emoji' },
  '建议': { emoji: '💬', type: 'emoji' },
  '总结': { emoji: '📝', type: 'emoji' },
  '回顾': { emoji: '🔍', type: 'emoji' },
  '展望': { emoji: '🔮', type: 'emoji' },
  '趋势': { emoji: '📈', type: 'emoji' },
  '未来': { emoji: '🚀', type: 'emoji' },
  '创新': { emoji: '💡', type: 'emoji' },
  '突破': { emoji: '🎯', type: 'emoji' },
  '机会': { emoji: '🌟', type: 'emoji' },
  '挑战': { emoji: '💪', type: 'emoji' },
  '团队': { emoji: '👥', type: 'emoji' },
  '协作': { emoji: '🤝', type: 'emoji' },
  '沟通': { emoji: '💬', type: 'emoji' },
  '管理': { emoji: '📋', type: 'emoji' },
  '流程': { emoji: '🔄', type: 'emoji' },
  '成本': { emoji: '💰', type: 'emoji' },
  '收益': { emoji: '📈', type: 'emoji' },
  '投资': { emoji: '💵', type: 'emoji' },
  '回报': { emoji: '💎', type: 'emoji' },
  '增长': { emoji: '📈', type: 'emoji' },
  '规模': { emoji: '📊', type: 'emoji' },
  '扩展': { emoji: '🔄', type: 'emoji' },
  '集成': { emoji: '🔗', type: 'emoji' },
  '兼容': { emoji: '✅', type: 'emoji' },
  '稳定': { emoji: '⚖️', type: 'emoji' },
  '可靠': { emoji: '🛡️', type: 'emoji' },
  '隐私': { emoji: '🔐', type: 'emoji' },
  '权限': { emoji: '🔑', type: 'emoji' },
  '认证': { emoji: '🎫', type: 'emoji' },
  '授权': { emoji: '✅', type: 'emoji' },
  '加密': { emoji: '🔒', type: 'emoji' },
  '解密': { emoji: '🔓', type: 'emoji' },
  '备份': { emoji: '💾', type: 'emoji' },
  '恢复': { emoji: '🔄', type: 'emoji' },
  '迁移': { emoji: '🚚', type: 'emoji' },
  '降级': { emoji: '⬇️', type: 'emoji' },
  '回滚': { emoji: '⬅️', type: 'emoji' },
  '快照': { emoji: '📸', type: 'emoji' },
  '镜像': { emoji: '🪞', type: 'emoji' },
  '容器': { emoji: '📦', type: 'emoji' },
  '虚拟化': { emoji: '🖥️', type: 'emoji' },
  '云': { emoji: '☁️', type: 'emoji' },
  '边缘': { emoji: '🌐', type: 'emoji' },
  '分布式': { emoji: '🌐', type: 'emoji' },
  '微服务': { emoji: '🔧', type: 'emoji' },
  '服务': { emoji: '🛠️', type: 'emoji' },
  '网关': { emoji: '🚪', type: 'emoji' },
  '负载均衡': { emoji: '⚖️', type: 'emoji' },
  '缓存': { emoji: '⚡', type: 'emoji' },
  '队列': { emoji: '📝', type: 'emoji' },
  '消息': { emoji: '💬', type: 'emoji' },
  '事件': { emoji: '⚡', type: 'emoji' },
  '触发': { emoji: '🎯', type: 'emoji' },
  '调度': { emoji: '📅', type: 'emoji' },
  '定时': { emoji: '⏰', type: 'emoji' },
  '异步': { emoji: '🔄', type: 'emoji' },
  '同步': { emoji: '🔗', type: 'emoji' },
  '并发': { emoji: '⚡', type: 'emoji' },
  '并行': { emoji: '🔀', type: 'emoji' },
  '串行': { emoji: '➡️', type: 'emoji' },
  '批处理': { emoji: '📦', type: 'emoji' },
  '流处理': { emoji: '🌊', type: 'emoji' },
  '实时': { emoji: '⚡', type: 'emoji' },
  '离线': { emoji: '💾', type: 'emoji' },
  '在线': { emoji: '🌐', type: 'emoji' },
  '本地': { emoji: '💻', type: 'emoji' },
  '远程': { emoji: '🌐', type: 'emoji' },
  '跨平台': { emoji: '🔄', type: 'emoji' },
  '多语言': { emoji: '🌍', type: 'emoji' },
  '国际化': { emoji: '🌐', type: 'emoji' },
  '本地化': { emoji: '📍', type: 'emoji' },
  '适配': { emoji: '🔧', type: 'emoji' },
  '兼容性': { emoji: '✅', type: 'emoji' },
  '可扩展': { emoji: '📈', type: 'emoji' },
  '可维护': { emoji: '🔧', type: 'emoji' },
  '可测试': { emoji: '🧪', type: 'emoji' },
  '可观测': { emoji: '👁️', type: 'emoji' },
  '可追溯': { emoji: '🔍', type: 'emoji' },
  '可恢复': { emoji: '🔄', type: 'emoji' },
  '可配置': { emoji: '⚙️', type: 'emoji' },
  '可定制': { emoji: '🎨', type: 'emoji' },
  '可插拔': { emoji: '🔌', type: 'emoji' },
  '可替换': { emoji: '🔄', type: 'emoji' },
  '可升级': { emoji: '⬆️', type: 'emoji' },
  '可迁移': { emoji: '🚚', type: 'emoji' },
  '可移植': { emoji: '📦', type: 'emoji' },
  '可重用': { emoji: '♻️', type: 'emoji' },
  '可组合': { emoji: '🧩', type: 'emoji' },
  '可编排': { emoji: '🎭', type: 'emoji' },
  '可自动化': { emoji: '🤖', type: 'emoji' },
  '可编程': { emoji: '💻', type: 'emoji' },
  '可脚本化': { emoji: '📜', type: 'emoji' },
  '可批量化': { emoji: '📦', type: 'emoji' },
  '可规模化': { emoji: '📈', type: 'emoji' },
  '可商业化': { emoji: '💰', type: 'emoji' },
  '可产品化': { emoji: '🎁', type: 'emoji' },
  '可服务化': { emoji: '🛠️', type: 'emoji' },
  '可平台化': { emoji: '🏗️', type: 'emoji' },
  '可生态化': { emoji: '🌐', type: 'emoji' },
  '可社区化': { emoji: '👥', type: 'emoji' },
  '可开放化': { emoji: '🔓', type: 'emoji' },
  '可共享化': { emoji: '🤝', type: 'emoji' },
  '可协同化': { emoji: '👥', type: 'emoji' },
  '可智能化': { emoji: '🤖', type: 'emoji' },
  '可数字化': { emoji: '🔢', type: 'emoji' },
  '可网络化': { emoji: '🌐', type: 'emoji' },
  '可移动化': { emoji: '📱', type: 'emoji' },
  '可云端化': { emoji: '☁️', type: 'emoji' },
  '可边缘化': { emoji: '🌐', type: 'emoji' },
  '可容器化': { emoji: '📦', type: 'emoji' },
  '可虚拟化': { emoji: '🖥️', type: 'emoji' },
  '可微服务化': { emoji: '🔧', type: 'emoji' },
  '可Serverless化': { emoji: '☁️', type: 'emoji' },
  '可FaaS化': { emoji: '⚡', type: 'emoji' },
  '可BaaS化': { emoji: '🔧', type: 'emoji' },
  '可SaaS化': { emoji: '🌐', type: 'emoji' },
  '可PaaS化': { emoji: '🏗️', type: 'emoji' },
  '可IaaS化': { emoji: '🖥️', type: 'emoji' },
  '可CaaS化': { emoji: '📦', type: 'emoji' },
  '可MaaS化': { emoji: '🤖', type: 'emoji' },
  '可DaaS化': { emoji: '🗄️', type: 'emoji' },
  '可AI化': { emoji: '🤖', type: 'emoji' },
  '可ML化': { emoji: '🧠', type: 'emoji' },
  '可DL化': { emoji: '🔮', type: 'emoji' },
  '可NLP化': { emoji: '💬', type: 'emoji' },
  '可CV化': { emoji: '👁️', type: 'emoji' },
  '可ASR化': { emoji: '🎤', type: 'emoji' },
  '可TTS化': { emoji: '🔊', type: 'emoji' },
  '可OCR化': { emoji: '📝', type: 'emoji' },
  '可RPA化': { emoji: '🤖', type: 'emoji' },
  '可IoT化': { emoji: '🌐', type: 'emoji' },
  '可区块链化': { emoji: '🔗', type: 'emoji' },
  '可AR化': { emoji: '👓', type: 'emoji' },
  '可VR化': { emoji: '🎮', type: 'emoji' },
  '可MR化': { emoji: '🌐', type: 'emoji' },
  '可XR化': { emoji: '🌐', type: 'emoji' },
  '可5G化': { emoji: '📡', type: 'emoji' },
  '可6G化': { emoji: '📡', type: 'emoji' },
  '可WiFi化': { emoji: '📶', type: 'emoji' },
  '可蓝牙化': { emoji: '📶', type: 'emoji' },
  '可NFC化': { emoji: '📱', type: 'emoji' },
  '可RFID化': { emoji: '📡', type: 'emoji' },
  '可GPS化': { emoji: '📍', type: 'emoji' },
  '可GIS化': { emoji: '🗺️', type: 'emoji' },
  '可LBS化': { emoji: '📍', type: 'emoji' },
  '可IM化': { emoji: '💬', type: 'emoji' },
  '可RTC化': { emoji: '📹', type: 'emoji' },
  '可直播化': { emoji: '📺', type: 'emoji' },
  '可点播化': { emoji: '🎬', type: 'emoji' },
  '可短视频化': { emoji: '📱', type: 'emoji' },
  '可长视频化': { emoji: '🎬', type: 'emoji' },
  '可音频化': { emoji: '🎵', type: 'emoji' },
  '可图片化': { emoji: '🖼️', type: 'emoji' },
  '可文本化': { emoji: '📝', type: 'emoji' },
  '可富媒体化': { emoji: '🎨', type: 'emoji' },
  '可互动化': { emoji: '🎮', type: 'emoji' },
  '可游戏化': { emoji: '🎮', type: 'emoji' },
  '可社交化': { emoji: '👥', type: 'emoji' },
  '可电商化': { emoji: '🛒', type: 'emoji' },
  '可金融化': { emoji: '💰', type: 'emoji' },
  '可教育化': { emoji: '📚', type: 'emoji' },
  '可医疗化': { emoji: '🏥', type: 'emoji' },
  '可出行化': { emoji: '🚗', type: 'emoji' },
  '可物流化': { emoji: '📦', type: 'emoji' },
  '可制造化': { emoji: '🏭', type: 'emoji' },
  '可农业化': { emoji: '🌾', type: 'emoji' },
  '可能源化': { emoji: '⚡', type: 'emoji' },
  '可环保化': { emoji: '🌱', type: 'emoji' },
  '可公益化': { emoji: '❤️', type: 'emoji' },
  '可政府化': { emoji: '🏛️', type: 'emoji' },
  '可企业化': { emoji: '🏢', type: 'emoji' },
  '可个人化': { emoji: '👤', type: 'emoji' },
  '可家庭化': { emoji: '🏠', type: 'emoji' },
  '可社区化': { emoji: '🏘️', type: 'emoji' },
  '可城市化': { emoji: '🏙️', type: 'emoji' },
  '可乡村化': { emoji: '🌾', type: 'emoji' },
  '可全球化': { emoji: '🌍', type: 'emoji' },
  '可个性化': { emoji: '👤', type: 'emoji' },
  '可定制化': { emoji: '🎨', type: 'emoji' },
  '可差异化': { emoji: '🎯', type: 'emoji' },
  '可专业化': { emoji: '🎓', type: 'emoji' },
  '可标准化': { emoji: '📋', type: 'emoji' },
  '可规范化': { emoji: '📐', type: 'emoji' },
  '可流程化': { emoji: '🔄', type: 'emoji' },
  'clawhub': { emoji: '🔧', type: 'emoji' },
  'OpenClaw': { emoji: '🤖', type: 'emoji' }
};

const materialKeywords = {
  'AI': { prompt: '一个逼真的AI机器人头像，表情严肃，深色背景，科技感，数字艺术风格，高质量', aspect: '1:1' },
  '机器人': { prompt: '一个逼真的AI机器人头像，表情严肃，深色背景，科技感，数字艺术风格，高质量', aspect: '1:1' },
  '牛顿': { prompt: '牛顿画像，严肃的科学家，深色背景，古典风格', aspect: '1:1' },
  '苹果': { prompt: '一个红苹果，干净背景，简洁风格', aspect: '1:1' },
  '苹果树': { prompt: '苹果树，挂在树枝上的红苹果，阳光照射，田园风格', aspect: '16:9' },
  '树': { prompt: '一棵大树，阳光照射，田园风格', aspect: '16:9' },
  '思考': { prompt: '人物托腮思考，发光灯泡想法冒出，深色背景，创意思维', aspect: '1:1' },
  '万有引力': { prompt: '行星围绕太阳运转，轨道线，深色背景，宇宙感，科学可视化', aspect: '16:9' },
  '引力': { prompt: '物体相互吸引的示意图，磁场线效果，深色背景，科学图示', aspect: '16:9' },
  '定律': { prompt: '物理公式和图表，科学感，深色背景，教育风格', aspect: '16:9' },
  '发现': { prompt: '科学家发现真理，灵光一闪，发光灯泡，深色背景', aspect: '1:1' },
  '宇宙': { prompt: '浩瀚宇宙星空，银河系，行星运转，深色背景，科幻风格', aspect: '16:9' },
  '地球': { prompt: '蓝色地球，悬浮在宇宙中，云层和陆地可见，深色背景', aspect: '1:1' },
  '技能': { prompt: '技能树或技能图标，能力升级概念，深色背景，发光效果', aspect: '1:1' },
  'clawhub': { prompt: '网站图标，工具和插件，深色背景，科技感', aspect: '1:1' },
  '数据': { prompt: '数据流动画，数字矩阵，深色背景，科技感', aspect: '16:9' },
  '设计': { prompt: '设计师工作场景，创意设计，深色背景', aspect: '16:9' },
  '程序员': { prompt: '程序员编程场景，代码屏幕，深色背景', aspect: '16:9' },
  '代码': { prompt: '代码屏幕，编程界面，深色背景，科技感', aspect: '16:9' },
  '赚钱': { prompt: '金币增长图表，财富增长，深色背景', aspect: '16:9' },
  '时间': { prompt: '沙漏时钟，时间流逝，深色背景', aspect: '1:1' },
  '升级': { prompt: '技能树图标，能力升级，发光效果，深色背景', aspect: '1:1' },
  '取代': { prompt: '人类vsAI对比图，科技对比，深色背景', aspect: '16:9' },
  '裁员': { prompt: '空荡办公室，商务场景，深色背景', aspect: '16:9' },
  '实习生': { prompt: '年轻人使用AI工作，现代办公，深色背景', aspect: '16:9' }
};

const defaultBg = { 
  prompt: '抽象科技背景，深蓝色调，发光线条和网格，数据流效果，科幻数字艺术风格', 
  aspect: '9:16' 
};

function extractNouns(text) {
  const nouns = [];
  for (const [keyword, visual] of Object.entries(nounVisualMap)) {
    if (text.includes(keyword)) {
      nouns.push({ keyword, ...visual });
    }
  }
  return nouns.slice(0, 3);
}

function extractMaterials(text) {
  const materials = [];
  for (const [keyword, material] of Object.entries(materialKeywords)) {
    if (text.includes(keyword)) {
      materials.push({ keyword, ...material });
    }
  }
  return materials.slice(0, 2);
}

function estimateDuration(text) {
  const charCount = text.length;
  return Math.max(2, Math.ceil(charCount / CONFIG.charsPerSecond));
}

function planScenes(topic, points, options = {}) {
  log('开始画面规划...');
  
  const scenes = [];
  let currentTime = 0;
  
  scenes.push({
    id: 0,
    type: '开场',
    timeStart: 0,
    timeEnd: 2,
    duration: 2,
    title: topic,
    script: topic,
    visual: {
      layout: 'center-explosion',
      elements: [
        { 
          type: '背景', 
          desc: '科技背景', 
          prompt: defaultBg.prompt, 
          aspect: defaultBg.aspect, 
          anim: 'fadeIn', 
          delay: 0, 
          duration: 30 
        },
        { 
          type: 'emoji', 
          value: '🤖', 
          anim: 'popIn', 
          delay: 15, 
          duration: 15 
        },
        { 
          type: '文字', 
          value: topic, 
          anim: 'fadeSlideUp', 
          delay: 30, 
          duration: 40,
          style: {
            fontSize: 72,
            color: '#FFD700',
            fontWeight: '900'
          }
        }
      ]
    }
  });
  currentTime = 2;
  
  points.forEach((point, i) => {
    const script = point.text || '';
    const title = point.title || script.substring(0, 20);
    const emoji = point.emoji || '📌';
    const sceneId = i + 1;
    
    const elements = [];
    const usedKeywords = [];
    
    const materials = extractMaterials(script);
    materials.forEach(mat => {
      if (!usedKeywords.includes(mat.keyword)) {
        elements.push({
          type: '素材',
          desc: mat.keyword,
          prompt: mat.prompt,
          aspect: mat.aspect,
          anim: 'fadeIn',
          delay: 20,
          duration: 45
        });
        usedKeywords.push(mat.keyword);
      }
    });
    
    elements.push({ 
      type: 'emoji', 
      value: emoji, 
      anim: 'popIn', 
      delay: 10, 
      duration: 15 
    });
    
    elements.push({ 
      type: '文字', 
      value: title, 
      anim: 'fadeSlideUp', 
      delay: 25, 
      duration: 40,
      style: {
        fontSize: 56,
        color: 'white',
        fontWeight: '900'
      }
    });
    
    if (point.description) {
      elements.push({ 
        type: '描述', 
        value: point.description, 
        anim: 'fadeSlideUp', 
        delay: 45, 
        duration: 40,
        style: {
          fontSize: 36,
          color: '#9ca3af'
        }
      });
    }
    
    if (!elements.find(e => e.type === '素材')) {
      elements.unshift({ 
        type: '背景', 
        desc: '科技背景', 
        prompt: defaultBg.prompt, 
        aspect: defaultBg.aspect, 
        anim: 'fadeIn', 
        delay: 0, 
        duration: 30 
      });
    }
    
    const nouns = extractNouns(script);
    nouns.forEach(noun => {
      if (!usedKeywords.includes(noun.keyword)) {
        elements.push({
          type: 'noun-visual',
          keyword: noun.keyword,
          emoji: noun.emoji,
          anim: 'popIn',
          delay: 35,
          duration: 20
        });
        usedKeywords.push(noun.keyword);
      }
    });
    
    const sceneDuration = estimateDuration(script);
    scenes.push({
      id: sceneId,
      type: i === 0 ? '核心观点' : '要点' + (i + 1),
      timeStart: currentTime,
      timeEnd: currentTime + sceneDuration,
      duration: sceneDuration,
      title: title,
      script: script,
      visual: { 
        layout: i % 2 === 0 ? 'left-text-right-image' : 'right-text-left-image',
        elements: elements 
      }
    });
    currentTime += sceneDuration;
  });
  
  scenes.push({
    id: scenes.length,
    type: '结尾',
    timeStart: currentTime,
    timeEnd: currentTime + 3,
    duration: 3,
    title: options.ending?.endingTitle || '开始使用',
    script: options.ending?.endingText || '更多信息，请访问 clawhub.ai',
    visual: {
      layout: 'center-focus',
      elements: [
        { type: 'emoji', value: '🔧', anim: 'popIn', delay: 10, duration: 15 },
        { 
          type: '文字', 
          value: options.ending?.endingText || 'clawhub.ai', 
          anim: 'fadeSlideUp', 
          delay: 25, 
          duration: 40,
          style: {
            fontSize: 64,
            color: '#FFD700',
            fontWeight: '900'
          }
        },
        { 
          type: '描述', 
          value: options.ending?.endingDesc || '解锁你的第一个AI技能', 
          anim: 'fadeSlideUp', 
          delay: 45, 
          duration: 40,
          style: {
            fontSize: 36,
            color: '#9ca3af'
          }
        }
      ]
    }
  });
  
  scenes.forEach((s, si) => {
    s.visual.elements.forEach(e => {
      if (e.type === '素材' || e.type === '背景') {
        e.filename = 's' + String(si).padStart(2, '0') + '_' + e.desc.replace(/\s/g, '_') + '.png';
      }
    });
  });
  
  const totalDuration = scenes[scenes.length - 1].timeEnd;
  log('生成了 ' + scenes.length + ' 个场景，总时长: ' + totalDuration + '秒');
  
  return { 
    topic,
    scenes, 
    totalDuration,
    config: CONFIG
  };
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法: node plan.js "主题" \'[{"text":"口播文案","emoji":"💡","title":"标题"}]\'');
    console.log('   或: node plan.js input.json -o output.json');
    process.exit(1);
  }
  
  let topic, points, outputFile, inputData;
  
  if (args[0].endsWith('.json') && fs.existsSync(args[0])) {
    inputData = JSON.parse(fs.readFileSync(args[0], 'utf-8'));
    topic = inputData.topic;
    points = inputData.points;
    outputFile = args[2] || 'storyboard.json';
  } else {
    topic = args[0];
    points = args[1] ? JSON.parse(args[1]) : [];
    outputFile = args[3] || null;
  }
  
  const storyboard = planScenes(topic, points, { ending: inputData?.ending });
  
  if (outputFile) {
    fs.writeFileSync(outputFile, JSON.stringify(storyboard, null, 2));
    log('分镜数据已保存到: ' + outputFile);
  } else {
    console.log(JSON.stringify(storyboard, null, 2));
  }
}

if (require.main === module) {
  main();
}

module.exports = { planScenes };
