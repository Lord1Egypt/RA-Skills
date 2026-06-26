/**
 * Viking URI 系统 - 统一资源标识符
 * 借鉴 OpenViking 的文件系统范式
 */

/**
 * Viking URI 格式: viking://{scope}/{path}
 * 
 * Scopes:
 * - resources: 独立资源（文档、代码等）
 * - user: 用户级数据（profile、memories）
 * - agent: Agent 级数据（skills、memories）
 * - session: Session 级数据（messages、tools）
 * - queue: 处理队列
 * - temp: 临时文件
 */

const VALID_SCOPES = ['resources', 'user', 'agent', 'session', 'queue', 'temp'];

export class VikingURI {
  constructor(uriString) {
    if (typeof uriString === 'string') {
      this.parse(uriString);
    } else if (typeof uriString === 'object') {
      this.scope = uriString.scope;
      this.path = uriString.path || '';
    }
  }
  
  /**
   * 解析 URI 字符串
   */
  parse(uriString) {
    const match = uriString.match(/^viking:\/\/([^\/]+)\/?(.*)$/);
    
    if (!match) {
      throw new Error(`Invalid Viking URI: ${uriString}`);
    }
    
    this.scope = match[1];
    this.path = match[2] || '';
    
    if (!VALID_SCOPES.includes(this.scope)) {
      throw new Error(`Invalid scope: ${this.scope}. Valid scopes: ${VALID_SCOPES.join(', ')}`);
    }
  }
  
  /**
   * 获取完整 URI
   */
  get uri() {
    return `viking://${this.scope}/${this.path}`;
  }
  
  /**
   * 获取完整路径（包含 scope）
   */
  get fullPath() {
    return `${this.scope}/${this.path}`;
  }
  
  /**
   * 获取父目录 URI
   */
  get parent() {
    if (!this.path || this.path === '') {
      return null;
    }
    
    const parts = this.path.split('/').filter(p => p);
    parts.pop();
    
    return new VikingURI({
      scope: this.scope,
      path: parts.join('/')
    });
  }
  
  /**
   * 获取文件名或目录名
   */
  get name() {
    const parts = this.path.split('/').filter(p => p);
    return parts[parts.length - 1] || '';
  }
  
  /**
   * 获取扩展名
   */
  get extension() {
    const name = this.name;
    const idx = name.lastIndexOf('.');
    return idx >= 0 ? name.substring(idx) : '';
  }
  
  /**
   * 是否是目录（以 / 结尾或没有扩展名）
   */
  get isDirectory() {
    if (this.path.endsWith('/')) return true;
    if (!this.name) return true;
    return !this.extension;
  }
  
  /**
   * 是否是文件
   */
  get isFile() {
    return !this.isDirectory;
  }
  
  /**
   * 拼接路径
   */
  join(...parts) {
    const newPath = [this.path, ...parts]
      .filter(p => p)
      .join('/')
      .replace(/\/+/g, '/');
    
    return new VikingURI({
      scope: this.scope,
      path: newPath
    });
  }
  
  /**
   * 检查是否是子路径
   */
  isChildOf(parentUri) {
    const parent = typeof parentUri === 'string' ? new VikingURI(parentUri) : parentUri;
    
    if (this.scope !== parent.scope) return false;
    
    const thisParts = this.path.split('/').filter(p => p);
    const parentParts = parent.path.split('/').filter(p => p);
    
    if (thisParts.length <= parentParts.length) return false;
    
    for (let i = 0; i < parentParts.length; i++) {
      if (thisParts[i] !== parentParts[i]) return false;
    }
    
    return true;
  }
  
  /**
   * 获取相对路径
   */
  relativeTo(baseUri) {
    const base = typeof baseUri === 'string' ? new VikingURI(baseUri) : baseUri;
    
    if (this.scope !== base.scope) {
      throw new Error('Cannot get relative path across different scopes');
    }
    
    const thisParts = this.path.split('/').filter(p => p);
    const baseParts = base.path.split('/').filter(p => p);
    
    // 找到公共前缀
    let i = 0;
    while (i < thisParts.length && i < baseParts.length && thisParts[i] === baseParts[i]) {
      i++;
    }
    
    // 构建相对路径
    const upLevels = baseParts.length - i;
    const downParts = thisParts.slice(i);
    
    const relativeParts = [];
    for (let j = 0; j < upLevels; j++) {
      relativeParts.push('..');
    }
    relativeParts.push(...downParts);
    
    return relativeParts.join('/') || '.';
  }
  
  /**
   * 转换为字符串
   */
  toString() {
    return this.uri;
  }
  
  /**
   * 转换为 JSON
   */
  toJSON() {
    return this.uri;
  }
}

/**
 * URI 工厂函数
 */
export function createURI(scope, path = '') {
  return new VikingURI({ scope, path });
}

/**
 * 常用 URI 常量
 */
export const URI_TEMPLATES = {
  // Resources
  RESOURCES_ROOT: 'viking://resources/',
  RESOURCE_PROJECT: (project) => `viking://resources/${project}/`,
  RESOURCE_FILE: (project, path) => `viking://resources/${project}/${path}`,
  
  // User
  USER_ROOT: (userId) => `viking://user/${userId}/`,
  USER_PROFILE: (userId) => `viking://user/${userId}/profile.md`,
  USER_MEMORIES: (userId) => `viking://user/${userId}/memories/`,
  USER_PREFERENCES: (userId) => `viking://user/${userId}/memories/preferences/`,
  USER_ENTITIES: (userId) => `viking://user/${userId}/memories/entities/`,
  USER_EVENTS: (userId) => `viking://user/${userId}/memories/events/`,
  
  // Agent
  AGENT_ROOT: (agentId) => `viking://agent/${agentId}/`,
  AGENT_SKILLS: (agentId) => `viking://agent/${agentId}/skills/`,
  AGENT_SKILL: (agentId, skillName) => `viking://agent/${agentId}/skills/${skillName}/`,
  AGENT_MEMORIES: (agentId) => `viking://agent/${agentId}/memories/`,
  AGENT_CASES: (agentId) => `viking://agent/${agentId}/memories/cases/`,
  AGENT_PATTERNS: (agentId) => `viking://agent/${agentId}/memories/patterns/`,
  AGENT_TOOLS: (agentId) => `viking://agent/${agentId}/memories/tools/`,
  AGENT_SKILLS_MEM: (agentId) => `viking://agent/${agentId}/memories/skills/`,
  
  // Session
  SESSION_ROOT: (sessionId) => `viking://session/${sessionId}/`,
  SESSION_MESSAGES: (sessionId) => `viking://session/${sessionId}/messages.jsonl`,
  SESSION_TOOLS: (sessionId) => `viking://session/${sessionId}/tools/`,
  SESSION_HISTORY: (sessionId) => `viking://session/${sessionId}/history/`,
  SESSION_ARCHIVE: (sessionId, archiveNum) => `viking://session/${sessionId}/history/archive_${String(archiveNum).padStart(3, '0')}/`,
  
  // Queue
  QUEUE_ROOT: 'viking://queue/',
  QUEUE_TASK: (taskId) => `viking://queue/${taskId}`,
  
  // Temp
  TEMP_ROOT: 'viking://temp/',
  TEMP_DIR: (tempId) => `viking://temp/${tempId}/`
};

/**
 * URI 解析工具
 */
export class URIParser {
  /**
   * 解析用户记忆 URI
   */
  static parseUserMemoryUri(uri) {
    const vikingUri = new VikingURI(uri);
    
    if (vikingUri.scope !== 'user') {
      throw new Error('Not a user URI');
    }
    
    const parts = vikingUri.path.split('/').filter(p => p);
    
    // viking://user/{user_id}/memories/{category}/{memory_id}
    if (parts.length >= 4 && parts[1] === 'memories') {
      return {
        userId: parts[0],
        category: parts[2],
        memoryId: parts.slice(3).join('/')
      };
    }
    
    // viking://user/{user_id}/profile.md
    if (parts.length === 2 && parts[1] === 'profile.md') {
      return {
        userId: parts[0],
        category: 'profile',
        memoryId: 'profile'
      };
    }
    
    throw new Error(`Invalid user memory URI: ${uri}`);
  }
  
  /**
   * 解析 Agent 记忆 URI
   */
  static parseAgentMemoryUri(uri) {
    const vikingUri = new VikingURI(uri);
    
    if (vikingUri.scope !== 'agent') {
      throw new Error('Not an agent URI');
    }
    
    const parts = vikingUri.path.split('/').filter(p => p);
    
    // viking://agent/{agent_id}/memories/{category}/{memory_id}
    if (parts.length >= 4 && parts[1] === 'memories') {
      return {
        agentId: parts[0],
        category: parts[2],
        memoryId: parts.slice(3).join('/')
      };
    }
    
    // viking://agent/{agent_id}/skills/{skill_name}
    if (parts.length >= 3 && parts[1] === 'skills') {
      return {
        agentId: parts[0],
        category: 'skills',
        memoryId: parts.slice(2).join('/')
      };
    }
    
    throw new Error(`Invalid agent memory URI: ${uri}`);
  }
  
  /**
   * 解析 Session URI
   */
  static parseSessionUri(uri) {
    const vikingUri = new VikingURI(uri);
    
    if (vikingUri.scope !== 'session') {
      throw new Error('Not a session URI');
    }
    
    const parts = vikingUri.path.split('/').filter(p => p);
    
    // viking://session/{session_id}/...
    if (parts.length >= 1) {
      return {
        sessionId: parts[0],
        resource: parts.slice(1).join('/')
      };
    }
    
    throw new Error(`Invalid session URI: ${uri}`);
  }
  
  /**
   * 解析资源 URI
   */
  static parseResourceUri(uri) {
    const vikingUri = new VikingURI(uri);
    
    if (vikingUri.scope !== 'resources') {
      throw new Error('Not a resource URI');
    }
    
    const parts = vikingUri.path.split('/').filter(p => p);
    
    // viking://resources/{project}/{path}
    if (parts.length >= 1) {
      return {
        project: parts[0],
        path: parts.slice(1).join('/')
      };
    }
    
    throw new Error(`Invalid resource URI: ${uri}`);
  }
}

export default VikingURI;
