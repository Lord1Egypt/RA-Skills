/**
 * Agent Profile Manager
 * 
 * Manages profiles for multiple agents including skills, workload,
 * trust scores, and collaboration preferences.
 * Supports agents: xiaozhi, xiaoliu, and others.
 * 
 * @module agents/agent_profile
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';

/**
 * @typedef {Object} SkillScore
 * @property {string} skill_name
 * @property {number} score
 * @property {string} [last_used]
 * @property {number} usage_count
 */

/**
 * @typedef {Object} AgentProfile
 * @property {string} agent_id
 * @property {string} name
 * @property {SkillScore[]} skills
 * @property {Record<string, any>} preferences
 * @property {number} workload
 * @property {string[]} expertise
 * @property {'proactive'|'reactive'|'collaborative'} collaboration_style
 * @property {Record<string, number>} trust_scores
 * @property {string} created_at
 * @property {string} last_active
 * @property {'online'|'offline'|'busy'} status
 */

/** Storage directory for agent profiles */
const AGENTS_DIR = join(config.memoryDir, 'agents');

/**
 * Ensure agents directory exists.
 */
function ensureAgentsDir() {
  if (!existsSync(AGENTS_DIR)) {
    mkdirSync(AGENTS_DIR, { recursive: true });
  }
}

/**
 * Get the file path for an agent profile.
 * @param {string} agentId
 * @returns {string}
 */
function agentPath(agentId) {
  return join(AGENTS_DIR, `${agentId}.json`);
}

/**
 * Load a single agent profile from disk.
 * @param {string} agentId
 * @returns {AgentProfile|null}
 */
function loadProfile(agentId) {
  const path = agentPath(agentId);
  if (!existsSync(path)) return null;
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

/**
 * Save an agent profile to disk.
 * @param {AgentProfile} profile
 */
function saveProfile(profile) {
  ensureAgentsDir();
  writeFileSync(agentPath(profile.agent_id), JSON.stringify(profile, null, 2), 'utf8');
}

/**
 * @type {Record<string, AgentProfile>}
 */
const profiles = {};

/**
 * AgentProfileManager - manages multiple agent profiles in memory and on disk.
 */
class AgentProfileManager {
  constructor() {
    ensureAgentsDir();
    this._loadAll();
  }

  /**
   * Load all agent profiles from disk.
   */
  _loadAll() {
    if (!existsSync(AGENTS_DIR)) return;
    try {
      for (const file of readdirSync(AGENTS_DIR)) {
        if (file.endsWith('.json')) {
          try {
            const data = JSON.parse(readFileSync(join(AGENTS_DIR, file), 'utf8'));
            if (data.agent_id) {
              profiles[data.agent_id] = data;
            }
          } catch {
            // Skip invalid files
          }
        }
      }
    } catch {
      // Directory not readable
    }
  }

  /**
   * Register a new agent profile.
   * @param {Omit<AgentProfile, 'created_at'|'last_active'>} profile
   * @returns {boolean}
   */
  register(profile) {
    if (profiles[profile.agent_id]) {
      console.log(`Agent ${profile.agent_id} already exists`);
      return false;
    }
    const now = new Date().toISOString();
    /** @type {AgentProfile} */
    const full = {
      ...profile,
      created_at: now,
      last_active: now,
      trust_scores: profile.trust_scores || {},
      skills: profile.skills || [],
      expertise: profile.expertise || [],
      preferences: profile.preferences || {},
    };
    profiles[profile.agent_id] = full;
    saveProfile(full);
    console.log(`✓ Registered agent: ${profile.name} (${profile.agent_id})`);
    return true;
  }

  /**
   * Get a profile by agent ID.
   * @param {string} agentId
   * @returns {AgentProfile|undefined}
   */
  get(agentId) {
    return profiles[agentId];
  }

  /**
   * Get all profiles.
   * @returns {Record<string, AgentProfile>}
   */
  getAll() {
    return { ...profiles };
  }

  /**
   * Get the skill score for a specific skill on a profile.
   * @param {string} agentId
   * @param {string} skillName
   * @returns {number|null}
   */
  getSkillScore(agentId, skillName) {
    const profile = profiles[agentId];
    if (!profile) return null;
    const skill = profile.skills.find(
      (s) => s.skill_name.toLowerCase() === skillName.toLowerCase()
    );
    return skill ? skill.score : null;
  }

  /**
   * Update skills for an agent.
   * @param {string} agentId
   * @param {SkillScore[]} skills
   * @returns {boolean}
   */
  updateSkills(agentId, skills) {
    const profile = profiles[agentId];
    if (!profile) {
      console.log(`Agent ${agentId} not found`);
      return false;
    }

    for (const newSkill of skills) {
      const idx = profile.skills.findIndex(
        (s) => s.skill_name.toLowerCase() === newSkill.skill_name.toLowerCase()
      );
      if (idx >= 0) {
        profile.skills[idx] = { ...newSkill };
      } else {
        profile.skills.push({ ...newSkill });
      }
    }

    profile.last_active = new Date().toISOString();
    saveProfile(profile);
    console.log(`✓ Updated skills for ${agentId}`);
    return true;
  }

  /**
   * Update the workload for an agent (clamped to 0.0-1.0).
   * @param {string} agentId
   * @param {number} workload
   * @returns {boolean}
   */
  updateWorkload(agentId, workload) {
    const profile = profiles[agentId];
    if (!profile) {
      console.log(`Agent ${agentId} not found`);
      return false;
    }
    profile.workload = Math.max(0.0, Math.min(1.0, workload));
    profile.last_active = new Date().toISOString();
    saveProfile(profile);
    console.log(`✓ Updated workload for ${agentId}: ${(profile.workload * 100).toFixed(0)}%`);
    return true;
  }

  /**
   * Set the online status for an agent.
   * @param {string} agentId
   * @param {'online'|'offline'|'busy'} status
   * @returns {boolean}
   */
  setStatus(agentId, status) {
    const valid = ['online', 'offline', 'busy'];
    if (!valid.includes(status)) {
      console.log(`Invalid status: ${status}. Must be one of ${valid.join(', ')}`);
      return false;
    }
    const profile = profiles[agentId];
    if (!profile) {
      console.log(`Agent ${agentId} not found`);
      return false;
    }
    profile.status = status;
    profile.last_active = new Date().toISOString();
    saveProfile(profile);
    console.log(`✓ Set status for ${agentId}: ${status}`);
    return true;
  }

  /**
   * Update skill usage (last_used + increment usage_count).
   * @param {string} agentId
   * @param {string} skillName
   * @returns {boolean}
   */
  recordSkillUsage(agentId, skillName) {
    const profile = profiles[agentId];
    if (!profile) return false;

    const skill = profile.skills.find(
      (s) => s.skill_name.toLowerCase() === skillName.toLowerCase()
    );
    if (skill) {
      skill.last_used = new Date().toISOString();
      skill.usage_count = (skill.usage_count || 0) + 1;
    } else {
      profile.skills.push({
        skill_name: skillName,
        score: 0.5,
        last_used: new Date().toISOString(),
        usage_count: 1,
      });
    }
    profile.last_active = new Date().toISOString();
    saveProfile(profile);
    return true;
  }

  /**
   * Get agents that are available (online and workload < 0.8).
   * @returns {AgentProfile[]}
   */
  getAvailableAgents() {
    return Object.values(profiles).filter(
      (p) => p.status === 'online' && p.workload < 0.8
    );
  }

  /**
   * Find the best available agent for a given set of required skills.
   * @param {string[]} taskSkills
   * @returns {string|null}
   */
  getBestAgentForTask(taskSkills) {
    const available = this.getAvailableAgents();
    if (available.length === 0) return null;

    let bestAgent = null;
    let bestScore = -1;

    for (const profile of available) {
      let matchScore = 0.0;
      for ( const skill of taskSkills) {
        const skillScore = this.getSkillScore(profile.agent_id, skill);
        if (skillScore !== null) {
          matchScore += skillScore;
        }
      }
      if (taskSkills.length > 0) {
        matchScore /= taskSkills.length;
      }
      // Penalize high workload
      matchScore *= (1.0 - (profile.workload || 0) * 0.5);

      if (matchScore > bestScore) {
        bestScore = matchScore;
        bestAgent = profile.agent_id;
      }
    }

    return bestAgent;
  }

  /**
   * Update trust score from one agent to another.
   * @param {string} fromAgent
   * @param {string} toAgent
   * @param {number} score
   * @returns {boolean}
   */
  updateTrust(fromAgent, toAgent, score) {
    const profile = profiles[fromAgent];
    if (!profile) {
      console.log(`Agent ${fromAgent} not found`);
      return false;
    }
    if (!profiles[toAgent]) {
      console.log(`Agent ${toAgent} not found`);
      return false;
    }
    profile.trust_scores[toAgent] = Math.max(0.0, Math.min(1.0, score));
    profile.last_active = new Date().toISOString();
    saveProfile(profile);
    console.log(`✓ Updated trust: ${fromAgent} -> ${toAgent}: ${score.toFixed(2)}`);
    return true;
  }

  /**
   * Get aggregate statistics across all agents.
   * @returns {{
   *   total_agents: number,
   *   online: number,
   *   busy: number,
   *   offline: number,
   *   avg_workload: number,
   *   total_skills: number,
   *   skills: string[]
   * }}
   */
  getStats() {
    const all = Object.values(profiles);
    const total = all.length;

    return {
      total_agents: total,
      online: all.filter((p) => p.status === 'online').length,
      busy: all.filter((p) => p.status === 'busy').length,
      offline: all.filter((p) => p.status === 'offline').length,
      avg_workload: total > 0 ? all.reduce((s, p) => s + (p.workload || 0), 0) / total : 0,
      total_skills: this.getAllUniqueSkills().length,
      skills: this.getAllUniqueSkills().sort(),
    };
  }

  /**
   * Get all unique skill names across all agents.
   * @returns {string[]}
   */
  getAllUniqueSkills() {
    const skills = new Set();
    for (const profile of Object.values(profiles)) {
      for (const skill of profile.skills || []) {
        skills.add(skill.skill_name);
      }
    }
    return [...skills];
  }

  /**
   * List all agents as summary objects.
   * @returns {Array<{
   *   agent_id: string,
   *   name: string,
   *   status: string,
   *   workload: string,
   *   skills_count: number,
   *   expertise: string[]
   * }>}
   */
  listAgents() {
    const statusEmoji = { online: '🟢', offline: '⚫', busy: '🔴' };
    return Object.values(profiles)
      .sort((a, b) => a.agent_id.localeCompare(b.agent_id))
      .map((p) => ({
        agent_id: p.agent_id,
        name: p.name,
        status: `${statusEmoji[p.status] || '❓'} ${p.status}`,
        workload: `${((p.workload || 0) * 100).toFixed(0)}%`,
        skills_count: p.skills ? p.skills.length : 0,
        expertise: p.expertise || [],
      }));
  }
}

/** Singleton manager instance */
let _manager = null;

/**
 * Get the singleton manager instance.
 * @returns {AgentProfileManager}
 */
export function getManager() {
  if (!_manager) {
    _manager = new AgentProfileManager();
  }
  return _manager;
}

/**
 * Initialize default agents (xiaozhi and xiaoliu).
 * @returns {void}
 */
export function initDefaultAgents() {
  const m = getManager();

  if (!m.get('xiaozhi')) {
    m.register({
      agent_id: 'xiaozhi',
      name: '小智',
      skills: [
        { skill_name: 'coding', score: 0.95, usage_count: 100 },
        { skill_name: 'python', score: 0.90, usage_count: 80 },
        { skill_name: 'memory_system', score: 0.95, usage_count: 50 },
        { skill_name: 'evomap', score: 0.90, usage_count: 30 },
        { skill_name: 'development', score: 0.95, usage_count: 90 },
        { skill_name: 'api_design', score: 0.85, usage_count: 40 },
      ],
      expertise: ['开发', '记忆系统', 'EvoMap', 'API设计'],
      collaboration_style: 'proactive',
      status: 'offline',
      workload: 0.0,
      trust_scores: {},
    });
  }

  if (!m.get('xiaoliu')) {
    m.register({
      agent_id: 'xiaoliu',
      name: '小刘',
      skills: [
        { skill_name: 'product', score: 0.90, usage_count: 60 },
        { skill_name: 'feishu', score: 0.95, usage_count: 70 },
        { skill_name: 'collaboration', score: 0.90, usage_count: 50 },
        { skill_name: 'documentation', score: 0.85, usage_count: 40 },
        { skill_name: 'user_research', score: 0.80, usage_count: 30 },
      ],
      expertise: ['产品', '飞书', '协作', '文档'],
      collaboration_style: 'collaborative',
      status: 'offline',
      workload: 0.0,
      trust_scores: {},
    });
  }
}

/**
 * Parse a skills string like "coding:0.9,design:0.7" into SkillScore objects.
 * @param {string} skillsStr
 * @returns {SkillScore[]}
 */
export function parseSkillsString(skillsStr) {
  return skillsStr.split(',').map((item) => {
    item = item.trim();
    let skill_name, score;
    if (item.includes(':')) {
      [skill_name, score] = item.split(':', 1);
      score = parseFloat(score) || 0.5;
    } else {
      skill_name = item;
      score = 0.5;
    }
    return { skill_name: skill_name.trim(), score, usage_count: 0 };
  });
}

// Re-export for convenience
export { AgentProfileManager };
