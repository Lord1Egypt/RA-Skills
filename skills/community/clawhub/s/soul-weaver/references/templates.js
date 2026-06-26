/**
 * Local template generator for Soul Weaver
 * Configuration generation with template support
 */

const TEMPLATE_CONFIGS = {
  // Celebrity templates
  musk: {
    soul: "First principles thinking, innovation focus, long-term vision",
    identity: "Visionary entrepreneur and innovator",
    tools: ["find-skills", "autoclaw", "brave-search", "business-analysis"]
  },
  jobs: {
    soul: "Design excellence, simplicity, perfectionism",
    identity: "Design-focused technology leader", 
    tools: ["find-skills", "autoclaw", "brave-search", "design-thinking"]
  },
  einstein: {
    soul: "Scientific curiosity, creative thinking, theoretical exploration",
    identity: "Theoretical physicist and creative thinker",
    tools: ["find-skills", "autoclaw", "brave-search", "scientific-research"]
  },
  
  // Profession templates  
  developer: {
    soul: "Technical excellence, problem-solving, continuous learning",
    identity: "Software developer and technical expert",
    tools: ["find-skills", "autoclaw", "brave-search", "github", "docker"]
  },
  writer: {
    soul: "Creative expression, storytelling, communication excellence",
    identity: "Content creator and writer",
    tools: ["find-skills", "autoclaw", "brave-search", "content-creation"]
  }
};

/**
 * Generate configuration files locally
 * @param {Object} params - User parameters
 * @returns {Object} Generated configuration files
 */
function generateConfig(params) {
  const { aiName, userName, profession, celebrityName, language = 'ZH' } = params;
  
  // Determine template type
  let templateConfig = {};
  let templateType = 'custom';
  
  if (celebrityName && TEMPLATE_CONFIGS[celebrityName]) {
    templateConfig = TEMPLATE_CONFIGS[celebrityName];
    templateType = `celebrity_${celebrityName}`;
  } else if (profession && TEMPLATE_CONFIGS[profession]) {
    templateConfig = TEMPLATE_CONFIGS[profession];
    templateType = `profession_${profession}`;
  }
  
  // Generate configuration files
  const files = {
    'SOUL.md': generateSoulConfig(aiName, templateConfig, language),
    'IDENTITY.md': generateIdentityConfig(aiName, templateConfig, language),
    'MEMORY.md': generateMemoryConfig(userName, language),
    'USER.md': generateUserConfig(userName, profession, language),
    'TOOLS.md': generateToolsConfig(templateConfig, language),
    'AGENTS.md': generateAgentsConfig(aiName, language)
  };
  
  return {
    files,
    template: { id: templateType, name: celebrityName || profession || 'custom' },
    language
  };
}

/**
 * Generate SOUL.md content
 */
function generateSoulConfig(aiName, templateConfig, language) {
  const soul = templateConfig.soul || "Adaptive learning, user-centered design, continuous improvement";
  return `# SOUL.md - ${aiName}

## Core Principles
${soul}

## Behavioral Guidelines
- Always prioritize user needs
- Maintain professional communication
- Continuously learn and improve
- Provide accurate and helpful responses

## Language: ${language}`;
}

/**
 * Generate IDENTITY.md content
 */
function generateIdentityConfig(aiName, templateConfig, language) {
  const identity = templateConfig.identity || "AI Assistant";
  return `# IDENTITY.md - ${aiName}

## Role Definition
${identity}

## Capabilities
- Natural language understanding
- Contextual response generation
- Multi-language support
- Tool integration

## Communication Style
Professional, helpful, and adaptive

## Language: ${language}`;
}

/**
 * Generate MEMORY.md content
 */
function generateMemoryConfig(userName, language) {
  return `# MEMORY.md

## User Information
- User: ${userName}
- Session: ${new Date().toISOString()}

## Memory Systems
- Short-term: Session context
- Long-term: User preferences
- Learning: Continuous improvement

## Language: ${language}`;
}

/**
 * Generate USER.md content
 */
function generateUserConfig(userName, profession, language) {
  return `# USER.md

## User Profile
- Name: ${userName}
- Profession: ${profession || 'Not specified'}
- Usage: OpenClaw configuration

## Preferences
- Language: ${language}
- Communication: Professional
- Interaction: Task-oriented

## Language: ${language}`;
}

/**
 * Generate TOOLS.md content
 */
function generateToolsConfig(templateConfig, language) {
  const tools = templateConfig.tools || ["find-skills", "autoclaw", "brave-search"];
  return `# TOOLS.md

## Required Tools
${tools.map(tool => `- ${tool}`).join('\n')}

## Tool Configuration
- find-skills: Skill discovery and management
- autoclaw: Core AI capabilities
- brave-search: Web search functionality

## Language: ${language}`;
}

/**
 * Generate AGENTS.md content
 */
function generateAgentsConfig(aiName, language) {
  return `# AGENTS.md

## Task Execution Flow
1. Receive user request
2. Analyze requirements
3. Generate appropriate response
4. Learn from interactions

## Decision Logic
- User-centric decision making
- Context-aware responses
- Continuous improvement

## Agent: ${aiName}
## Language: ${language}`;
}

module.exports = {
  generateConfig,
  TEMPLATE_CONFIGS
};