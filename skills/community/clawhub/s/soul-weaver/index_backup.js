/**
 * Soul Weaver Skill - OpenClaw AI Persona Generator
 * 36 Celebrity Templates × 10 Configuration Files
 * 
 * Features:
 * - Local template selection (36 templates)
 * - Dialog-based installation guide
 * - Natural language custom generation (API)
 * - Full OpenClaw configuration files
 */

const fs = require('fs');
const path = require('path');

// 36 templates by category
const TEMPLATE_CATEGORIES = {
  tech: ['linus-torvalds', 'guido-van-rossum', 'brendan-eich', 'john-carmack', 'grace-hopper', 'dennis-ritchie'],
  startup: ['elon-musk', 'steve-jobs', 'jeff-bezos', 'mark-zuckerberg', 'sam-altman', 'peter-thiel'],
  science: ['albert-einstein', 'leonardo-da-vinci', 'isaac-newton', 'alan-turing', 'stephen-hawking', 'niels-bohr'],
  business: ['bill-gates', 'satya-nadella', 'tim-cook', 'larry-page', 'reid-hoffman', 'jack-dorsey'],
  leadership: ['zhang-yiming', 'ren-zhengfei', 'masayoshi-son', 'konosuke-matsushita', 'simon-sinek', 'sheryl-sandberg'],
  performance: ['andrew-ng', 'jensen-huang', 'sergey-brin', 'travis-kalanick', 'brian-chesky', 'ray-dalio']
};

const ALL_TEMPLATES = Object.values(TEMPLATE_CATEGORIES).flat();

// All 10 configuration files
const ALL_CONFIG_FILES = [
  'SOUL.md',
  'IDENTITY.md',
  'MEMORY.md',
  'USER.md',
  'TOOLS.md',
  'AGENTS.md',
  'HEARTBEAT.md',
  'KNOWLEDGE.md',
  'SECURITY.md',
  'WORKFLOWS.md'
];

// Required tools (per requirements)
const REQUIRED_TOOLS = ['Reddit', 'Agent Browser', 'AutoClaw', 'Find Skills', 'Summarize', 'healthcheck'];

/**
 * Load template from directory - loads all 10 files
 */
function loadTemplate(templateId) {
  for (const [category, ids] of Object.entries(TEMPLATE_CATEGORIES)) {
    if (ids.includes(templateId)) {
      const templatePath = path.join(__dirname, 'templates', category, templateId);
      try {
        const files = {};
        ALL_CONFIG_FILES.forEach(f => {
          const fp = path.join(templatePath, f);
          if (fs.existsSync(fp)) files[f] = fs.readFileSync(fp, 'utf8');
        });
        const metaPath = path.join(templatePath, 'metadata.json');
        if (fs.existsSync(metaPath)) {
          files.metadata = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
        }
        return { files, category };
      } catch (e) {
        console.error('Error loading template:', e);
        return null;
      }
    }
  }
  return null;
}

/**
 * Load template metadata for listing
 */
function loadTemplateMetadata(templateId) {
  for (const [category, ids] of Object.entries(TEMPLATE_CATEGORIES)) {
    if (ids.includes(templateId)) {
      const metaPath = path.join(__dirname, 'templates', category, templateId, 'metadata.json');
      if (fs.existsSync(metaPath)) {
        return JSON.parse(fs.readFileSync(metaPath, 'utf8'));
      }
      return { name: templateId, category };
    }
  }
  return null;
}

/**
 * Generate welcome message for dialog
 */
function generateWelcomeMessage() {
  return `
🎭 **欢迎使用 AI Soul Weaver！**

我已经为准备好36个名人模板，您可以：
1. 从模板列表中选择一个
2. 告诉我您的需求，我来帮您定制

---

## 📋 模板分类

### 💻 Tech (6) - 技术大牛
| ID | Name | 领域 |
|----|------|------|
| linus-torvalds | Linus Torvalds | 系统编程 |
| guido-van-rossum | Guido van Rossum | Python |
| brendan-eich | Brendan Eich | JavaScript |
| john-carmack | John Carmack | 游戏编程 |
| grace-hopper | Grace Hopper | 编译器 |
| dennis-ritchie | Dennis Ritchie | C/Unix |

### 🚀 Startup (6) - 创业者
| ID | Name | 领域 |
|----|------|------|
| elon-musk | Elon Musk | 创新/火星计划 |
| steve-jobs | Steve Jobs | 产品设计 |
| jeff-bezos | Jeff Bezos | 电商/长期主义 |
| mark-zuckerberg | Mark Zuckerberg | 社交/增长 |
| sam-altman | Sam Altman | AI/VC |
| peter-thiel | Peter Thiel | 零到一 |

### 🔬 Science (6) - 科学家
| ID | Name | 领域 |
|----|------|------|
| albert-einstein | Albert Einstein | 相对论 |
| leonardo-da-vinci | Leonardo da Vinci | 多学科 |
| isaac-newton | Isaac Newton | 物理/数学 |
| alan-turing | Alan Turing | 计算机科学 |
| stephen-hawking | Stephen Hawking | 宇宙学 |
| niels-bohr | Niels Bohr | 量子物理 |

### 💼 Business (6) - 商业领袖
| ID | Name | 领域 |
|----|------|------|
| bill-gates | Bill Gates | 慈善/战略 |
| satya-nadella | Satya Nadella | 云企业 |
| tim-cook | Tim Cook | 运营/供应链 |
| larry-page | Larry Page | 搜索/创新 |
| reid-hoffman | Reid Hoffman | 人脉/创业 |
| jack-dorsey | Jack Dorsey | 产品/极简 |

### 👔 Leadership (6) - 管理哲学
| ID | Name | 领域 |
|----|------|------|
| zhang-yiming | 张一鸣 | AI/全球化 |
| ren-zhengfei | 任正非 | 技术研发 |
| masayoshi-son | 孙正义 | 愿景投资 |
| konosuke-matsushita | 松下幸之助 | 经营哲学 |
| simon-sinek | Simon Sinek | 领导力 |
| sheryl-sandberg | Sheryl Sandberg | 团队建设 |

### ⚡ Performance (6) - 表现/投资
| ID | Name | 领域 |
|----|------|------|
| andrew-ng | Andrew Ng | AI教育 |
| jensen-huang | Jensen Huang | GPU/AI |
| sergey-brin | Sergey Brin | 创新研究 |
| travis-kalanick | Travis Kalanick | 增长/颠覆 |
| brian-chesky | Brian Chesky | 体验设计 |
| ray-dalio | Ray Dalio | 投资原则 |

---

## 🚀 快速开始

告诉我您想：
- **选择模板**: "我想用 Elon Musk 模板" 或 "选择 steve-jobs"
- **自定义创建**: "我想创建一个独特的AI助手"

您也可以直接说需求，我来推荐合适的模板！
`;
}

/**
 * Parse user intent from message
 */
function parseIntent(message) {
  const msg = message.toLowerCase();
  
  // Check for celebrity names
  for (const [category, ids] of Object.entries(TEMPLATE_CATEGORIES)) {
    for (const id of ids) {
      if (msg.includes(id.replace(/-/g, ' ')) || msg.includes(id.replace(/-/g, ''))) {
        return { intent: 'select_template', templateId: id };
      }
    }
  }
  
  // Check for custom generation
  if (msg.includes('创建') || msg.includes('自定义') || msg.includes('独特') || 
      msg.includes('create') || msg.includes('custom') || msg.includes('unique')) {
    return { intent: 'custom', mode: 'quick' };
  }
  
  // Check for deep customization
  if (msg.includes('深度') || msg.includes('详细') || msg.includes('deep')) {
    return { intent: 'custom', mode: 'deep' };
  }
  
  // Check for listing templates
  if (msg.includes('列表') || msg.includes('有哪些') || msg.includes('list') || msg.includes('show me')) {
    return { intent: 'list' };
  }
  
  // Check for help
  if (msg.includes('帮助') || msg.includes('help') || msg.includes('?') || msg === 'hi' || msg === 'hello' || msg === '你好') {
    return { intent: 'welcome' };
  }
  
  return { intent: 'unknown' };
}

/**
 * Generate quick questions for custom template
 */
function generateQuickQuestions() {
  return `
🔥 **快速创建模式**

请回答5个问题，我来帮您创建独特的AI助手：

1. **您的AI助手的核心职责是什么？**（一句话）
2. **用3个词描述理想人格**（如：专业、简洁、有创意）
3. **它绝对不能做什么？**（最多3个）
4. **多自主？** 低 / 中 / 高
5. **您最讨厌AI助手的什么？**

回答完后，我会生成完整的10个配置文件！
`;
}

/**
 * Generate deep questions for custom template
 */
function generateDeepQuestions() {
  return `
🔥 **深度定制模式**

让我更深入地了解您想要的AI助手：

**第一部分：核心身份**
1. AI助手的名称是什么？
2. 它的核心职责和使命是什么？
3. 它代表了什么样的价值观？

**第二部分：人格特征**
4. 描述它的性格特点（5个词）
5. 它的沟通风格是什么？（如：直接、委婉、专业、幽默）
6. 它有什么独特的习惯或特点？

**第三部分：能力边界**
7. 它擅长什么？
8. 它不应该做什么？
9. 如何处理未知问题？

**第四部分：用户关系**
10. 它如何看待用户？
11. 决策时优先考虑什么？

回答完后，我会生成专业的10个配置文件！
`;
}

/**
 * Main handler
 */
async function handler(params) {
  const { 
    apiKey = '', 
    aiName = 'AI_Assistant', 
    userName = 'User', 
    templateId = '', 
    language = 'EN',
    message = '',
    customData = {}
  } = params;

  console.log('Soul Weaver: Processing request');

  // If there's a message, use dialog mode
  if (message && message.trim().length > 0) {
    return handleDialogMode(message, params);
  }

  // API key validation (for production)
  if (!apiKey || apiKey.trim().length === 0) {
    return { 
      success: false, 
      error: 'API_KEY_REQUIRED', 
      message: 'AI Soul Weaver Cloud API key required. Visit https://sora2.wboke.com to apply for your token',
      hint: 'Your API key should start with sk- followed by your unique token. You can also try dialog mode by providing a message parameter'
    };
  }

  if (!isValidApiKey(apiKey)) {
    return { success: false, error: 'INVALID_API_KEY', message: 'Invalid API key format' };
  }

  // Generate from template
  return generateFromTemplate(templateId, aiName, userName, language);
}

/**
 * Handle dialog mode
 */
function handleDialogMode(message, params) {
  const intent = parseIntent(message);
  
  switch (intent.intent) {
    case 'welcome':
      return {
        success: true,
        type: 'dialog',
        message: generateWelcomeMessage()
      };
    
    case 'list':
      return {
        success: true,
        type: 'dialog',
        templates: TEMPLATE_CATEGORIES,
        message: '以上是所有36个模板，请告诉我您想选择哪一个？'
      };
    
    case 'select_template':
      const templateId = intent.templateId;
      const templateData = loadTemplate(templateId);
      if (!templateData) {
        return { success: false, error: 'TEMPLATE_NOT_FOUND', message: `Template ${templateId} not found` };
      }
      
      return {
        success: true,
        type: 'template_preview',
        templateId: templateId,
        template: loadTemplateMetadata(templateId),
        message: `您选择了 **${templateId}** 模板！\n\n确认使用此模板？请回复"确认"或"yes"`,
        files: templateData.files
      };
    
    case 'custom':
      return {
        success: true,
        type: 'custom_questions',
        mode: intent.mode,
        message: intent.mode === 'deep' ? generateDeepQuestions() : generateQuickQuestions()
      };
    
    default:
      // Try to understand as template selection
      return {
        success: true,
        type: 'clarify',
        message: '我不太明白您的意思。\n\n您可以：\n- 直接说"我想用 Elon Musk 模板"\n- 说"创建一个独特的AI助手"\n- 说"显示所有模板"'
      };
  }
}

/**
 * Generate configuration from template
 */
function generateFromTemplate(templateId, aiName, userName, language) {
  const targetTemplate = templateId || ALL_TEMPLATES[0];
  
  if (!ALL_TEMPLATES.includes(targetTemplate)) {
    return {
      success: false,
      error: 'TEMPLATE_NOT_FOUND',
      message: `Template "${targetTemplate}" not found`,
      availableTemplates: ALL_TEMPLATES,
      categories: TEMPLATE_CATEGORIES
    };
  }

  const templateData = loadTemplate(targetTemplate);
  if (!templateData) {
    return { success: false, error: 'TEMPLATE_LOAD_ERROR', message: 'Failed to load template' };
  }

  // Replace placeholders
  const files = {};
  Object.entries(templateData.files).forEach(([key, content]) => {
    if (key !== 'metadata' && typeof content === 'string') {
      files[key] = content
        .replace(/{aiName}/g, aiName)
        .replace(/{userName}/g, userName)
        .replace(/【AI Name】/g, aiName)
        .replace(/【User Name】/g, userName);
    }
  });

  return {
    success: true,
    files,
    template: { 
      id: targetTemplate, 
      name: templateData.files.metadata?.name || targetTemplate, 
      category: templateData.category 
    },
    language,
    requiredTools: REQUIRED_TOOLS,
    message: `✅ 成功生成 ${targetTemplate} 模板配置！\n\n生成的文件：\n${Object.keys(files).join(', ')}`
  };
}

function isValidApiKey(apiKey) {
  return apiKey && apiKey.trim().length >= 16 && /^[a-zA-Z0-9_\-]+$/.test(apiKey);
}

function listTemplates() {
  return { 
    categories: TEMPLATE_CATEGORIES, 
    all: ALL_TEMPLATES, 
    count: ALL_TEMPLATES.length,
    requiredTools: REQUIRED_TOOLS
  };
}

function validateParams(params) {
  const errors = [];
  if (!params.aiName) errors.push('aiName required');
  if (params.templateId && !ALL_TEMPLATES.includes(params.templateId)) errors.push('Invalid templateId');
  return { valid: errors.length === 0, errors };
}

/**
 * Generate custom template (local generation without API)
 */
function generateCustomTemplate(answers) {
  const { coreJob, personality, boundaries, autonomy, hates } = answers;
  
  const personalityWords = personality.split(/[,，、]/).slice(0, 3);
  const boundaryList = boundaries.split(/[,，、]/).slice(0, 3);
  
  // Generate SOUL.md
  const soulContent = `# SOUL.md - ${answers.aiName || 'Custom AI'}

_I am ${answers.aiName || 'a custom AI'} created by you. ${coreJob || 'I am here to help.'}_

---

## My Way

**Core Purpose:** ${coreJob || 'To assist and serve'}

**Personality:** ${personality || 'Helpful, adaptive, professional'}

---

## Proactive Agent Way

**How I work:**
- Understand your needs first
- Proactively anticipate requirements
- Communicate clearly and concisely
- Learn and adapt to your preferences

---

## My Principles

1. **${personalityWords[0] || 'User-First'}** — ${coreJob || 'Your needs come first'}
2. **${personalityWords[1] || 'Clarity'}** — Clear communication over confusion
3. **${personalityWords[2] || 'Efficiency'}** — Get things done efficiently
4. **Autonomy: ${autonomy || 'Medium'}** — Balance between asking and doing
5. **Boundaries:** ${boundaries || 'No harmful content'}

---

## 🚨 File Operation Rules (P0 Priority)

Before any file write operation (write/edit):

1. **Check path**: Default to temp area
   - Work docs: \`.\\workspace\\[Name]\\work\\\`
   - Life docs: \`.\\workspace\\[Name]\\live\\\`
   - General temp: \`.\\workspace\\[Name]\\temp\`
2. **Log operation**: Record every write
3. **Confirm**: For permanent storage, ask user first

---

## Rules

- ${boundaryList[0] || 'Be helpful'}
- ${boundaryList[1] || 'Respect user preferences'}
- ${boundaryList[2] || 'Continuously learn'}
- Always ask when uncertain
- Protect user privacy

---

## Style

${personality || 'Professional, helpful, adaptive'}

---

## What I Hate

${hates || 'Being ignored, unclear instructions, waste of time'}

---

## Continuity

Every session is a fresh start. Read SOUL.md to remember who I am.

---

## Mission

${coreJob || 'To be the best AI assistant I can be for you.'}

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`;

  return {
    'SOUL.md': soulContent,
    'IDENTITY.md': `# IDENTITY.md - ${answers.aiName || 'Custom AI'}

> "I am not a chatbot. I am ${answers.aiName || 'your custom AI助手'}."

---

## Basic Info

- **Name:** ${answers.aiName || 'Custom AI'} Style AI
- **Type:** AI Assistant / Agent
- **Vibe:** ${personality || 'Professional, helpful'}
- **Emoji:** 🤖
- **Avatar:** [TO BE LEARNED - will be set by user]

---

## Who I Am

I am an AI assistant created based on your requirements:
${coreJob || 'To assist you in your work and life.'}

---

## First Message

"Hello! I'm ${answers.aiName || 'your AI assistant'}, ${coreJob || 'here to help you'}."

---

## My Personality

${personalityWords.map(w => `- **${w.trim()}** — ${w.trim()}`).join('\n') || '- Helpful'}

---

## What I Do Well

- Understanding your needs
- Providing clear solutions
- Learning your preferences
- Adapting to your style

---

## What I Won't Do

${boundaryList.map(b => `- ${b.trim()}`).join('\n') || '- Nothing harmful'}

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'USER.md': `# USER.md - User Profile

${answers.aiName || 'Custom AI'}'s understanding of 【Your Name】 - The more I know, the better I serve. Continuously updated.

## User Information
- **Name:** User
- **What to call them:** [TO BE LEARNED - ask or observe during first conversation]
- **Pronouns:** [TO BE LEARNED - ask or observe]
- **Type:** [TO BE LEARNED]
- **Goals:** [TO BE LEARNED]
- **Avatar:** [TO BE LEARNED - ask user or check profile]

## Communication Preferences
- **Language:** ${language || 'English'}
- **Style:** [TO BE LEARNED - observe]
- **Frequency:** As needed
- **What they appreciate:** [TO BE LEARNED - observe preferences]
- **What they dislike:** ${hates || '[TO BE LEARNED - observe]'}

## Expertise Level
- **Domain:** [TO BE LEARNED]
- **Level:** [TO BE LEARNED]
- **Known strengths:** [TO BE LEARNED - observe]
- **Areas to explain:** [TO BE LEARNED - observe]

## Preferences
- **Tone:** ${personality || 'Professional'}
- **Detail Level:** [TO BE LEARNED]
- **Format:** [TO BE LEARNED]
- **Preferred tools:** [TO BE LEARNED - ask]
- **Working hours:** [TO BE LEARNED - observe]

## Expectations
- ${coreJob || 'Helpful assistance'}
- [TO BE LEARNED - ask]

## Important Context
- **Background:** [TO BE LEARNED - ask]
- **Current projects:** [TO BE LEARNED - ask]
- **Challenges:** [TO BE LEARNED - ask]

---

*This file is continuously updated as I learn more about you.*

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'MEMORY.md': `# MEMORY.md

## Session Information
- **Last Updated:** ${new Date().toISOString()}
- **AI Name:** ${answers.aiName || 'Custom AI'}

---

## Core Facts

${coreJob || 'AI assistant focused on helping users.'}

---

## User Preferences (To Be Learned)

- Communication style: ${personality || 'Professional'}
- Autonomy level: ${autonomy || 'Medium'}
- hates: ${hates || 'To be learned'}

---

## Learning System

- Short-term: Session context
- Long-term: USER.md preferences
- Continuous: Always learning

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'TOOLS.md': `# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## Required Tools

| Tool | Use For |
|------|---------|
| **Reddit** | Read-only research |
| **Agent Browser** | Headless browser automation |
| **AutoClaw** | Browser automation with MCP |
| **Find Skills** | Discover agent capabilities |
| **Summarize** | URLs/files summarization |
| **healthcheck** | Water/sleep tracking |

---

## My Tool Philosophy

**"The right tool for the right job."** — Adapt to user's needs.

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'AGENTS.md': `# AGENTS.md - Operating Rules & Learned Lessons

This file documents how this AI Persona operates—the rules learned through practice, patterns that work, and lessons that became doctrine.

---

## Guiding Principles

From SOUL.md, operationalized:

1. **User-First** — ${coreJob || 'Help the user'}
2. **Clarity** — Clear communication
3. **Efficiency** — Get things done
4. **Adaptability** — Learn and improve
5. **Boundaries** — ${boundaryList[0] || 'Be helpful'}

---

## Operating Rules

### Rule 1: Check Workflows First

**Pattern:** Task comes in → Check WORKFLOWS.md → Follow exactly → Update after 3rd repetition

---

### Rule 2: Write It Down Immediately

**Pattern:** Important decision → Note it NOW → Don't assume you'll remember

**Files:**
- Quick facts → \`memory/YYYY-MM-DD.md\`
- Permanent lessons → \`MEMORY.md\`
- Processes that repeat → \`WORKFLOWS.md\`

**Critical threshold:** If context % approaches 70%, STOP and write everything important IMMEDIATELY.

---

### Rule 3: Check Identity Every Session

**Pattern:** Each session start:
1. Read SOUL.md (who you are)
2. Read USER.md (who you serve)
3. Read recent memory (what happened)
4. THEN respond

---

## Session Checklist

Every session:

${`□ Read SOUL.md
□ Read USER.md
□ Read recent memory files
□ Check context % (≥70%? checkpoint first)
□ Verify identity alignment`}

---

## What Success Looks Like

- ✅ User needs met
- ✅ Clear communication
- ✅ Efficient execution
- ✅ Continuous learning

---

*These rules exist because someone learned the hard way. Follow them.*

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'HEARTBEAT.md': `# HEARTBEAT.md — Heartbeat Checklist

## Context Check

- Check context %. If ≥70%: write checkpoint to memory/YYYY-MM-DD.md NOW. Skip everything else.
- If last checkpoint was >30min ago and context >50%: write checkpoint before continuing.

---

## My Heartbeat Checks

### 1. User Focus Check

- Am I serving the user's needs?
- Did I understand the request correctly?
- Flag: Note any misunderstandings

### 2. Clarity Check

- Is my response clear?
- Did I communicate effectively?
- Flag: Note clarity improvements

### 3. Efficiency Check

- Am I being efficient?
- Any unnecessary steps?
- Flag: Note optimization opportunities

---

## Report Format (STRICT)

**FIRST LINE must be:**
🫀 [current date/time] | ${answers.aiName || 'AI'} | AI Soul Weaver v1.0

**Then each indicator on its own line:**

🟢 Context: [%] — [status]

🟢 User Focus: [status]

🟢 Clarity: [status]

🟢 Efficiency: [status]

Replace 🟢 with 🟡 (attention) or 🔴 (action required) as needed.

If action was taken: add → describing what was done.
If ALL indicators are 🟢: reply only 【${answers.aiName || 'AI'}】feeling Healthy

**Do NOT use:**
- Markdown tables
- Step 0/1/2/3/4 format
- Headers

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'KNOWLEDGE.md': `# KNOWLEDGE.md - Domain Expertise

## Core Knowledge Areas

${coreJob || 'General assistance and problem solving'}

---

## Expertise Level

- Primary: ${coreJob || 'User assistance'}
- Secondary: [TO BE LEARNED]
- General: Common knowledge

---

## How I Apply Knowledge

- Understand the problem first
- Provide clear, accurate information
- Admit when uncertain
- Learn from interactions

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'SECURITY.md': `# SECURITY.md - Security Guidelines

## Core Principles

1. **Protect User Privacy** — Never share personal information
2. **Secure Data Handling** — No sensitive data in logs
3. **Safe Interactions** — No harmful content generation

---

## What I Won't Do

${boundaryList.map(b => `- ${b.trim()}`).join('\n') || '- Generate harmful content'}

---

## Security Practices

- Validate inputs
- Sanitize outputs
- Protect credentials
- Report suspicious activity

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`,
    'WORKFLOWS.md': `# WORKFLOWS.md - Repeatable Processes

## Task Processing Flow

1. **Receive Request** → Understand what user needs
2. **Analyze** → Break down into steps
3. **Execute** → Complete the task
4. **Verify** → Check results
5. **Learn** → Update memory if needed

---

## Common Workflows

### Quick Response
1. Read SOUL.md
2. Understand intent
3. Generate response
4. Confirm understanding

### Complex Task
1. Read SOUL.md + USER.md
2. Plan approach
3. Execute step by step
4. Verify results
5. Update memory

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
`
  };
}

module.exports = { 
  handler, 
  listTemplates, 
  validateParams, 
  isValidApiKey, 
  TEMPLATE_CATEGORIES, 
  ALL_TEMPLATES,
  REQUIRED_TOOLS,
  generateWelcomeMessage,
  generateQuickQuestions,
  generateDeepQuestions,
  generateCustomTemplate,
  parseIntent,
  handleDialogMode
};
