#!/usr/bin/env node
/**
 * Story Relay - 故事接龙
 * 多人协作创作，AI智能续写，支持图文生成
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = '/root/.openclaw/workspace';
const RELAY_DIR = path.join(WORKSPACE, 'story-relay');
const STORIES_DIR = path.join(RELAY_DIR, 'stories');
const CONFIG_FILE = path.join(RELAY_DIR, 'config.json');

// 默认配置
const DEFAULT_CONFIG = {
  defaultStyle: '悬疑',
  maxChapters: 100,
  autoSave: true
};

// 故事风格定义
const STORY_STYLES = {
  '悬疑': {
    emoji: '🎭',
    description: '紧张刺激，悬念迭起',
    keywords: ['神秘', '悬疑', '推理', '惊悚', '秘密']
  },
  '温馨': {
    emoji: '🌟',
    description: '治愈温暖，轻松愉快',
    keywords: ['温暖', '治愈', '快乐', '幸福', '感动']
  },
  '热血': {
    emoji: '⚔️',
    description: '冒险战斗，热血沸腾',
    keywords: ['热血', '战斗', '冒险', '挑战', '胜利']
  },
  '搞笑': {
    emoji: '😄',
    description: '轻松幽默，有趣好玩',
    keywords: ['搞笑', '幽默', '有趣', '好玩', '笑点']
  },
  '奇幻': {
    emoji: '🏰',
    description: '魔法奇幻，异世界',
    keywords: ['魔法', '奇幻', '异世界', '冒险', '传说']
  },
  '科幻': {
    emoji: '🚀',
    description: '未来科技，太空冒险',
    keywords: ['科幻', '未来', '科技', '太空', 'AI']
  },
  '浪漫': {
    emoji: '💕',
    description: '爱情故事，浪漫唯美',
    keywords: ['爱情', '浪漫', '喜欢', '心动', '表白']
  },
  '现实': {
    emoji: '🎭',
    description: '现实主义，贴近生活',
    keywords: ['现实', '生活', '工作', '家庭', '朋友']
  }
};

/**
 * 确保目录存在
 */
function ensureDirectories() {
  [RELAY_DIR, STORIES_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

/**
 * 加载配置
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2));
    return DEFAULT_CONFIG;
  }
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (e) {
    console.error('Failed to load config:', e);
    return DEFAULT_CONFIG;
  }
}

/**
 * 生成故事ID
 */
function generateStoryId() {
  const random = Math.random().toString(36).substring(2, 6).toUpperCase();
  return `STORY-${random}`;
}

/**
 * 获取当前活动故事ID
 */
function getCurrentStoryId() {
  const currentFile = path.join(RELAY_DIR, 'current.json');
  if (!fs.existsSync(currentFile)) {
    return null;
  }
  try {
    const data = JSON.parse(fs.readFileSync(currentFile, 'utf-8'));
    return data.currentStoryId;
  } catch (e) {
    return null;
  }
}

/**
 * 设置当前活动故事
 */
function setCurrentStoryId(storyId) {
  const currentFile = path.join(RELAY_DIR, 'current.json');
  const data = { currentStoryId: storyId };
  fs.writeFileSync(currentFile, JSON.stringify(data, null, 2));
}

/**
 * 创建新故事
 */
function createStory(theme, config) {
  ensureDirectories();

  const storyId = generateStoryId();
  const style = config.defaultStyle;

  const story = {
    id: storyId,
    title: theme,
    theme: theme,
    style: style,
    status: 'in_progress',
    createdAt: Date.now(),
    updatedAt: Date.now(),
    chapters: [],
    characters: [],
    settings: []
  };

  // 保存故事
  const storyFile = path.join(STORIES_DIR, `${storyId}.json`);
  fs.writeFileSync(storyFile, JSON.stringify(story, null, 2));

  // 设置为当前故事
  setCurrentStoryId(storyId);

  return story;
}

/**
 * 获取故事
 */
function getStory(storyId) {
  const storyFile = path.join(STORIES_DIR, `${storyId}.json`);
  if (!fs.existsSync(storyFile)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(storyFile, 'utf-8'));
  } catch (e) {
    return null;
  }
}

/**
 * 保存故事
 */
function saveStory(story) {
  const storyFile = path.join(STORIES_DIR, `${story.id}.json`);
  story.updatedAt = Date.now();
  fs.writeFileSync(storyFile, JSON.stringify(story, null, 2));
}

/**
 * 获取所有故事
 */
function getAllStories() {
  ensureDirectories();
  const files = fs.readdirSync(STORIES_DIR);
  const stories = [];

  files.forEach(file => {
    if (file.endsWith('.json')) {
      const storyId = file.replace('.json', '');
      const story = getStory(storyId);
      if (story) {
        stories.push(story);
      }
    }
  });

  return stories.sort((a, b) => b.updatedAt - a.updatedAt);
}

/**
 * 添加章节
 */
function addChapter(story, content, author) {
  const chapter = {
    id: story.chapters.length + 1,
    author: author,
    content: content,
    timestamp: Date.now()
  };

  story.chapters.push(chapter);
  return chapter;
}

/**
 * 格式化故事内容
 */
function formatStoryContent(story) {
  let content = '';

  story.chapters.forEach(chapter => {
    content += `📖 第${chapter.id}章\n\n`;
    content += `${chapter.content}\n\n`;
    content += `👤 作者: ${chapter.author}\n`;
    content += `⏰ ${new Date(chapter.timestamp).toLocaleString('zh-CN')}\n\n`;
    content += '---\n\n';
  });

  return content;
}

/**
 * AI生成开头
 */
function generateOpening(theme, style) {
  const styleInfo = STORY_STYLES[style] || STORY_STYLES['悬疑'];

  // 简单的模板生成
  const templates = {
    '科幻': [
      `2077年，新东京。霓虹灯在雨夜中闪烁，照亮了这座不夜城。\n\n${theme}的故事从这里开始...`,
      `在遥远的未来，人类已经征服了星际旅行。\n\n${theme}的冒险即将展开...`,
      `量子计算机的诞生改变了整个世界。\n\n${theme}的序幕拉开...`
    ],
    '奇幻': [
      `在遥远的艾瑞西亚大陆，魔法与科技共存。\n\n${theme}的传说开始了...`,
      `一个普通的少年，偶然获得了一本古老的魔法书。\n\n${theme}的故事从此改变...`,
      `异世界的召唤之光照亮了夜空。\n\n${theme}的冒险即将启程...`
    ],
    '悬疑': [
      `那是一个月黑风高的夜晚。\n\n${theme}的谜团浮现...`,
      `所有人都以为那是一场意外，但真相远比想象中复杂。\n\n${theme}的真相被隐藏...`,
      `一封神秘的信件改变了一切。\n\n${theme}的秘密开始解开...`
    ],
    '温馨': [
      `阳光透过窗户洒进房间，温暖而明亮。\n\n${theme}的美好故事开始了...`,
      `小镇的清晨，总是那么宁静美好。\n\n${theme}的温暖故事展开...`,
      `那是一个普通的周末，却因为一次相遇而变得不平凡。\n\n${theme}的温馨时光...`
    ],
    '热血': [
      `战斗的号角已经吹响！\n\n${theme}的热血冒险启程！`,
      `少年发誓要成为最强的战士。\n\n${theme}的挑战之路开始...`,
      `敌人压境，英雄们集结起来！\n\n${theme}的战斗即将爆发...`
    ],
    '搞笑': [
      `本来想好好当个普通人，结果...\n\n${theme}的搞笑日常开始了！`,
      `一不小心就闹了个大笑话。\n\n${theme}的有趣故事展开...`,
      `生活总是充满了意外和惊喜。\n\n${theme}的欢乐时刻...`
    ],
    '浪漫': [
      `那是一个樱花飘落的春天。\n\n${theme}的浪漫故事开始...`,
      `一次偶然的相遇，改变了两个人的命运。\n\n${theme}的爱情故事...`,
      `月光下，心跳的声音清晰可闻。\n\n${theme}的浪漫时刻...`
    ],
    '现实': [
      `这是一段关于${theme}的真实故事。\n\n生活总是这样，平凡而又不平凡...`,
      `在那家咖啡馆里，每天都会发生不同的故事。\n\n${theme}的生活片段...`,
      `工作和生活的平衡，是现代人永恒的话题。\n\n${theme}的现实写照...`
    ]
  };

  const styleTemplates = templates[style] || templates['悬疑'];
  const template = styleTemplates[Math.floor(Math.random() * styleTemplates.length)];

  return template;
}

/**
 * AI续写故事
 */
function generateContinuation(story) {
  const lastChapter = story.chapters[story.chapters.length - 1];
  const styleInfo = STORY_STYLES[story.style] || STORY_STYLES['悬疑'];

  // 简单的续写逻辑（实际应该调用AI）
  const continuationTemplates = [
    `突然，${lastChapter.content.slice(-20)}...\n\n这改变了一切。`,
    `正当一切看似平静时，意外发生了。\n\n${styleInfo.keywords[Math.floor(Math.random() * styleInfo.keywords.length)]}的故事继续...`,
    `一个新的角色出现了，打破了沉默。\n\n"你好，"他/她说道。`,
    `在这个关键时刻，主角面临着重要的选择。\n\n${styleInfo.keywords[Math.floor(Math.random() * styleInfo.keywords.length)]}...`,
    `夜幕降临，更多的秘密浮出水面。\n\n${styleInfo.keywords[Math.floor(Math.random() * styleInfo.keywords.length)]}的真相...`
  ];

  const template = continuationTemplates[Math.floor(Math.random() * continuationTemplates.length)];

  return template;
}

/**
 * 主函数
 */
function main(args) {
  const config = loadConfig();
  ensureDirectories();

  const command = args[0];

  switch (command) {
    case 'start':
    case '开始': {
      const theme = args.slice(1).join(' ');
      if (!theme) {
        console.log('❌ 请提供故事主题');
        console.log('用法: node index.js start <主题>');
        return;
      }

      console.log(`🎨 正在创建故事：${theme}`);
      console.log(`   风格：${config.defaultStyle}`);

      const story = createStory(theme, config);

      console.log(`\n✅ 故事已创建：${story.id}`);
      console.log(`\n📖 第一章：${story.title}`);

      // 生成开头
      const opening = generateOpening(theme, config.defaultStyle);
      console.log(`\n${opening}`);

      // 添加第一章
      addChapter(story, opening, 'AI');
      saveStory(story);

      console.log(`\n👉 轮到你了！输入"续写：[内容]"或者"继续故事"让AI续写`);
      break;
    }

    case 'continue':
    case '继续': {
      const currentStoryId = getCurrentStoryId();
      if (!currentStoryId) {
        console.log('❌ 没有当前故事，请先用"开始故事"创建一个');
        return;
      }

      const story = getStory(currentStoryId);
      if (!story) {
        console.log('❌ 故事不存在');
        return;
      }

      console.log(`📖 正在续写故事：${story.title}`);

      const continuation = generateContinuation(story);
      const chapter = addChapter(story, continuation, 'AI');
      saveStory(story);

      console.log(`\n📖 第${chapter.id}章\n\n`);
      console.log(`${continuation}\n\n`);
      console.log(`👉 输入"续写：[内容]"继续创作`);
      break;
    }

    case 'write':
    case '续写': {
      const currentStoryId = getCurrentStoryId();
      if (!currentStoryId) {
        console.log('❌ 没有当前故事，请先用"开始故事"创建一个');
        return;
      }

      const story = getStory(currentStoryId);
      if (!story) {
        console.log('❌ 故事不存在');
        return;
      }

      const content = args.slice(1).join(' ');
      if (!content) {
        console.log('❌ 请提供续写内容');
        console.log('用法: node index.js write <内容>');
        return;
      }

      const chapter = addChapter(story, content, 'user');
      saveStory(story);

      console.log(`\n✅ 第${chapter.id}章已添加！\n`);
      console.log(`📖 故事：${story.title}\n`);
      console.log(`📝 你的内容：\n\n${content}\n`);
      console.log(`👉 输入"继续故事"让AI续写`);
      break;
    }

    case 'view':
    case '查看': {
      const currentStoryId = getCurrentStoryId();
      if (!currentStoryId) {
        console.log('❌ 没有当前故事');
        return;
      }

      const story = getStory(currentStoryId);
      if (!story) {
        console.log('❌ 故事不存在');
        return;
      }

      console.log(`\n📚 故事：${story.title}`);
      console.log(`📖 ID：${story.id}`);
      console.log(`🎨 风格：${story.style}`);
      console.log(`📊 状态：${story.status}`);
      console.log(`📝 章节：${story.chapters.length}章`);
      console.log(`⏰ 更新：${new Date(story.updatedAt).toLocaleString('zh-CN')}`);
      console.log('\n---\n');

      console.log(formatStoryContent(story));
      break;
    }

    case 'list':
    case '列表': {
      const stories = getAllStories();

      if (stories.length === 0) {
        console.log('📚 还没有故事，输入"开始故事：[主题]"创建第一个！');
        return;
      }

      console.log(`\n📚 故事列表（共${stories.length}个）\n`);

      stories.forEach((story, index) => {
        const styleInfo = STORY_STYLES[story.style] || STORY_STYLES['悬疑'];
        const isCurrent = story.id === getCurrentStoryId() ? '👈 当前' : '';

        console.log(`${index + 1}. ${story.title}`);
        console.log(`   📖 ID: ${story.id} ${isCurrent}`);
        console.log(`   🎨 风格: ${styleInfo.emoji} ${story.style}`);
        console.log(`   📝 章节: ${story.chapters.length}章`);
        console.log(`   📊 状态: ${story.status}`);
        console.log(`   ⏰ 更新: ${new Date(story.updatedAt).toLocaleString('zh-CN')}`);
        console.log('');
      });
      break;
    }

    case 'switch':
    case '切换': {
      const storyId = args[1];
      if (!storyId) {
        console.log('❌ 请提供故事ID');
        console.log('用法: node index.js switch <故事ID>');
        return;
      }

      const story = getStory(storyId);
      if (!story) {
        console.log('❌ 故事不存在');
        console.log('💡 使用"故事列表"查看所有故事');
        return;
      }

      setCurrentStoryId(storyId);
      console.log(`\n✅ 已切换到故事：${story.title}`);
      console.log(`📖 ID: ${storyId}`);
      break;
    }

    case 'complete':
    case '完成': {
      const currentStoryId = getCurrentStoryId();
      if (!currentStoryId) {
        console.log('❌ 没有当前故事');
        return;
      }

      const story = getStory(currentStoryId);
      if (!story) {
        console.log('❌ 故事不存在');
        return;
      }

      story.status = 'completed';
      saveStory(story);

      console.log(`\n✅ 故事已完成！\n`);
      console.log(`📚 ${story.title}`);
      console.log(`📝 共${story.chapters.length}章`);
      console.log(`\n完整故事：\n\n${formatStoryContent(story)}`);
      break;
    }

    case 'delete':
    case '删除': {
      const storyId = args[1];
      if (!storyId) {
        console.log('❌ 请提供故事ID');
        console.log('用法: node index.js delete <故事ID>');
        return;
      }

      const storyFile = path.join(STORIES_DIR, `${storyId}.json`);
      if (!fs.existsSync(storyFile)) {
        console.log('❌ 故事不存在');
        return;
      }

      fs.unlinkSync(storyFile);
      console.log(`\n✅ 故事已删除：${storyId}`);

      // 如果删除的是当前故事，清除当前标记
      if (getCurrentStoryId() === storyId) {
        setCurrentStoryId(null);
        console.log('📝 已清除当前故事标记');
      }
      break;
    }

    case 'set-style':
    case '设置风格': {
      const style = args[1];
      if (!style) {
        console.log('❌ 请提供风格');
        console.log('可用风格:', Object.keys(STORY_STYLES).join(', '));
        console.log('用法: node index.js set-style <风格>');
        return;
      }

      if (!STORY_STYLES[style]) {
        console.log(`❌ 不支持的风格：${style}`);
        console.log('可用风格:', Object.keys(STORY_STYLES).join(', '));
        return;
      }

      config.defaultStyle = style;
      fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));

      const styleInfo = STORY_STYLES[style];
      console.log(`\n✅ 默认风格已设置：${style}`);
      console.log(`🎨 ${styleInfo.emoji} ${styleInfo.description}`);
      break;
    }

    default:
      console.log('📚 故事接龙 - Story Relay\n');
      console.log('命令列表:');
      console.log('  start <主题>        - 开始新故事');
      console.log('  continue            - AI续写故事');
      console.log('  write <内容>         - 续写内容');
      console.log('  view                - 查看当前故事');
      console.log('  list                - 列出所有故事');
      console.log('  switch <ID>         - 切换故事');
      console.log('  complete            - 完成故事');
      console.log('  delete <ID>         - 删除故事');
      console.log('  set-style <风格>     - 设置默认风格');
      console.log('\n可用风格:', Object.keys(STORY_STYLES).join(', '));
      console.log('\n示例:');
      console.log('  node index.js start 科幻冒险');
      console.log('  node index.js write 主角发现了秘密');
      console.log('  node index.js continue');
  }
}

// 运行
main(process.argv.slice(2));
