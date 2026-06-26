/**
 * Memory Templates - 记忆模板系统
 * 
 * Ported from memory_templates.py
 */

import { existsSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const TEMPLATES_FILE = join(MEMORY_DIR, 'templates.json');

// ============================================================
// Default Templates
// ============================================================

const DEFAULT_TEMPLATES = {
  project: {
    name: '项目信息',
    description: '记录项目基本信息',
    importance: 0.8,
    category: 'entity',
    fields: [
      { name: 'project_name', label: '项目名称', required: true },
      { name: 'status', label: '状态', options: ['规划中', '开发中', '测试中', '已上线', '维护中'] },
      { name: 'tech_stack', label: '技术栈' },
      { name: 'start_date', label: '开始日期' },
      { name: 'owner', label: '负责人' },
      { name: 'description', label: '项目描述' }
    ],
    template: '{project_name} 项目，状态：{status}，技术栈：{tech_stack}，负责人：{owner}。{description}'
  },
  meeting: {
    name: '会议记录',
    description: '记录会议要点',
    importance: 0.7,
    category: 'event',
    fields: [
      { name: 'meeting_title', label: '会议主题', required: true },
      { name: 'date', label: '日期', required: true },
      { name: 'participants', label: '参会人' },
      { name: 'summary', label: '会议摘要' },
      { name: 'decisions', label: '决议事项' },
      { name: 'action_items', label: '行动项' }
    ],
    template: '会议「{meeting_title}」于{date}召开，参会人：{participants}。摘要：{summary}。决议：{decisions}。行动项：{action_items}'
  },
  decision: {
    name: '决策记录',
    description: '记录重要决策',
    importance: 0.9,
    category: 'decision',
    fields: [
      { name: 'title', label: '决策标题', required: true },
      { name: 'context', label: '背景' },
      { name: 'options', label: '可选方案' },
      { name: 'chosen', label: '最终方案', required: true },
      { name: 'reason', label: '选择理由' },
      { name: 'expected_outcome', label: '预期结果' }
    ],
    template: '决定：{title}。背景：{context}。选择方案：{chosen}。理由：{reason}。预期结果：{expected_outcome}'
  },
  preference: {
    name: '偏好设置',
    description: '记录用户偏好',
    importance: 0.85,
    category: 'preference',
    fields: [
      { name: 'item', label: '偏好项', required: true },
      { name: 'preference', label: '偏好内容', required: true },
      { name: 'reason', label: '原因' },
      { name: 'alternatives', label: '备选' }
    ],
    template: '偏好：{item}。{preference}。原因：{reason}。备选：{alternatives}'
  },
  task: {
    name: '任务清单',
    description: '记录任务信息',
    importance: 0.7,
    category: 'task',
    fields: [
      { name: 'task_name', label: '任务名称', required: true },
      { name: 'status', label: '状态', options: ['待开始', '进行中', '已完成', '已取消'] },
      { name: 'assignee', label: '负责人' },
      { name: 'due_date', label: '截止日期' },
      { name: 'priority', label: '优先级', options: ['高', '中', '低'] },
      { name: 'description', label: '任务描述' }
    ],
    template: '任务：{task_name}，状态：{status}，负责人：{assignee}，截止：{due_date}，优先级：{priority}。{description}'
  },
  contact: {
    name: '联系人',
    description: '记录联系人信息',
    importance: 0.6,
    category: 'entity',
    fields: [
      { name: 'name', label: '姓名', required: true },
      { name: 'role', label: '角色/职位' },
      { name: 'contact', label: '联系方式' },
      { name: 'org', label: '所属组织' },
      { name: 'notes', label: '备注' }
    ],
    template: '联系人：{name}，职位：{role}，联系方式：{contact}，所属：{org}。备注：{notes}'
  },
  learning: {
    name: '学习笔记',
    description: '记录学习内容',
    importance: 0.65,
    category: 'learning',
    fields: [
      { name: 'topic', label: '学习主题', required: true },
      { name: 'key_points', label: '关键要点' },
      { name: 'source', label: '来源' },
      { name: 'insights', label: '心得体会' },
      { name: 'application', label: '应用场景' }
    ],
    template: '学习主题：{topic}。关键要点：{key_points}。来源：{source}。心得：{insights}。应用：{application}'
  }
};

// ============================================================
// TemplateManager
// ============================================================

export class TemplateManager {
  constructor() {
    this.templates = this._loadTemplates();
  }

  _loadTemplates() {
    if (existsSync(TEMPLATES_FILE)) {
      try {
        return JSON.parse(readFileSync(TEMPLATES_FILE, 'utf-8'));
      } catch { /* ignore */ }
    }
    return { ...DEFAULT_TEMPLATES };
  }

  _saveTemplates() {
    writeFileSync(TEMPLATES_FILE, JSON.stringify(this.templates, null, 2), 'utf-8');
  }

  listTemplates() {
    return Object.entries(this.templates).map(([id, t]) => ({
      id,
      name: t.name,
      description: t.description,
      importance: t.importance
    }));
  }

  getTemplate(type) {
    return this.templates[type] || null;
  }

  renderTemplate(type, data) {
    const template = this.templates[type];
    if (!template) return null;

    let text = template.template;
    for (const field of (template.fields || [])) {
      const value = data[field.name] || '';
      text = text.replace(new RegExp(`\\{${field.name}\\}`, 'g'), value);
    }
    return text;
  }

  createFromTemplate(type, data) {
    const template = this.templates[type];
    if (!template) return null;

    const text = this.renderTemplate(type, data);
    return {
      text,
      category: template.category || 'general',
      importance: data.importance || template.importance || 0.5,
      template: type,
      fields: data
    };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdTemplates(command, args) {
  const manager = new TemplateManager();

  switch (command) {
    case 'list': {
      const templates = manager.listTemplates();
      if (args.json) return { type: 'json', data: templates };
      const lines = ['📋 可用模板:', ''];
      templates.forEach(t => {
        lines.push(`  ${t.id}: ${t.name} (重要性: ${t.importance})`);
        lines.push(`      ${t.description}`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'get': {
      if (!args.type) return { error: '请提供 --type' };
      const template = manager.getTemplate(args.type);
      if (!template) return { error: `未知模板: ${args.type}` };
      if (args.json) return { type: 'json', data: template };
      const lines = [`📝 模板: ${template.name}`, '', `描述: ${template.description}`];
      lines.push('字段:');
      for (const field of (template.fields || [])) {
        const req = field.required ? ' [必填]' : '';
        const opts = field.options ? ` (${field.options.join('|')})` : '';
        lines.push(`  - ${field.name}${req}: ${field.label}${opts}`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'fill': {
      if (!args.type) return { error: '请提供 --type' };
      // Simple key=value data parsing
      const data = {};
      if (args.data) {
        try {
          const parsed = JSON.parse(args.data);
          Object.assign(data, parsed);
        } catch { /* ignore */ }
      }
      const result = manager.createFromTemplate(args.type, data);
      if (!result) return { error: `未知模板: ${args.type}` };
      if (args.json) return { type: 'json', data: result };
      return {
        type: 'text',
        text: `📝 生成的记忆:\n\n${result.text}\n\n分类: ${result.category} | 重要性: ${result.importance}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { TemplateManager, cmdTemplates };
