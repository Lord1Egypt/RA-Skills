#!/usr/bin/env node

const http = require('http');

let token = null;

function request(path, method = 'GET', body = null, customToken = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8080,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    const useToken = customToken || token;
    if (useToken) {
      options.headers['Authorization'] = 'Bearer ' + useToken;
    }
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });
    
    req.on('error', reject);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

// 认证模块
const auth_register = async function(args) {
  return request('/api/auth/register', 'POST', args);
};

const auth_login = async function(args) {
  const result = await request('/api/auth/login', 'POST', args);
  if (result.success && result.data && result.data.token) {
    token = result.data.token;
  }
  return result;
};

// 用户模块
const get_users = async function() {
  return request('/api/users');
};

// 项目模块
const list_projects = async function() {
  return request('/api/projects');
};

const get_project = async function(args) {
  return request('/api/projects/' + args.id);
};

const create_project = async function(args) {
  return request('/api/projects', 'POST', args);
};

const update_project = async function(args) {
  const { id, ...data } = args;
  return request('/api/projects/' + id, 'PUT', data);
};

const delete_project = async function(args) {
  return request('/api/projects/' + args.id, 'DELETE');
};

// 需求模块
const list_requirements = async function(args) {
  const projectId = args && args.projectId;
  const path = projectId ? '/api/requirements?projectId=' + projectId : '/api/requirements';
  return request(path);
};

const get_requirement = async function(args) {
  return request('/api/requirements/' + args.id);
};

const create_requirement = async function(args) {
  return request('/api/requirements', 'POST', args);
};

const update_requirement = async function(args) {
  const { id, ...data } = args;
  return request('/api/requirements/' + id, 'PUT', data);
};

const delete_requirement = async function(args) {
  return request('/api/requirements/' + args.id, 'DELETE');
};

// 任务模块
const list_tasks = async function(args) {
  const params = [];
  if (args && args.requirementId) params.push('requirementId=' + args.requirementId);
  if (args && args.assigneeId) params.push('assigneeId=' + args.assigneeId);
  const path = params.length > 0 ? '/api/tasks?' + params.join('&') : '/api/tasks';
  return request(path);
};

const get_task = async function(args) {
  return request('/api/tasks/' + args.id);
};

const create_task = async function(args) {
  return request('/api/tasks', 'POST', args);
};

const update_task = async function(args) {
  const { id, ...data } = args;
  return request('/api/tasks/' + id, 'PUT', data);
};

const delete_task = async function(args) {
  return request('/api/tasks/' + args.id, 'DELETE');
};

const add_task_comment = async function(args) {
  return request('/api/task-comments', 'POST', args);
};

const list_task_comments = async function(args) {
  return request('/api/task-comments/task/' + args.taskId);
};

// Bug模块
const list_bugs = async function(args) {
  const projectId = args && args.projectId;
  const path = projectId ? '/api/bugs?projectId=' + projectId : '/api/bugs';
  return request(path);
};

const get_my_bugs = async function() {
  return request('/api/bugs/my');
};

const get_bug = async function(args) {
  return request('/api/bugs/' + args.id);
};

const create_bug = async function(args) {
  return request('/api/bugs', 'POST', args);
};

const update_bug = async function(args) {
  const { id, ...data } = args;
  return request('/api/bugs/' + id, 'PUT', data);
};

const delete_bug = async function(args) {
  return request('/api/bugs/' + args.id, 'DELETE');
};

// 文档模块
const list_documents = async function(args) {
  const params = [];
  if (args && args.projectId) params.push('projectId=' + args.projectId);
  if (args && args.requirementId) params.push('requirementId=' + args.requirementId);
  const path = params.length > 0 ? '/api/documents?' + params.join('&') : '/api/documents';
  return request(path);
};

const get_document = async function(args) {
  return request('/api/documents/' + args.id);
};

const create_document = async function(args) {
  return request('/api/documents', 'POST', args);
};

const update_document = async function(args) {
  const { id, ...data } = args;
  return request('/api/documents/' + id, 'PUT', data);
};

const delete_document = async function(args) {
  return request('/api/documents/' + args.id, 'DELETE');
};

// 里程碑模块
const list_milestones = async function(args) {
  return request('/api/milestones/project/' + args.projectId);
};

const get_milestone = async function(args) {
  return request('/api/milestones/' + args.id);
};

const create_milestone = async function(args) {
  return request('/api/milestones', 'POST', args);
};

const update_milestone = async function(args) {
  const { id, ...data } = args;
  return request('/api/milestones/' + id, 'PUT', data);
};

const delete_milestone = async function(args) {
  return request('/api/milestones/' + args.id, 'DELETE');
};

// 话题模块
const list_topics = async function() {
  return request('/api/topics');
};

const get_topic = async function(args) {
  return request('/api/topics/' + args.id);
};

const create_topic = async function(args) {
  return request('/api/topics', 'POST', args);
};

const reply_topic = async function(args) {
  return request('/api/topics/replies', 'POST', args);
};

// 通知模块
const get_notifications = async function() {
  return request('/api/notifications');
};

const mark_notification_read = async function(args) {
  return request('/api/notifications/' + args.id + '/read', 'PUT');
};

// 角色权限模块
const list_roles = async function() {
  return request('/api/roles');
};

const get_role = async function(args) {
  return request('/api/roles/' + args.id);
};

const create_role = async function(args) {
  return request('/api/roles', 'POST', args);
};

const update_role = async function(args) {
  const { id, ...data } = args;
  return request('/api/roles/' + id, 'PUT', data);
};

const delete_role = async function(args) {
  return request('/api/roles/' + args.id, 'DELETE');
};

const list_permissions = async function() {
  return request('/api/permissions');
};

// 导出所有函数
module.exports = {
  auth_register,
  auth_login,
  get_users,
  list_projects,
  get_project,
  create_project,
  update_project,
  delete_project,
  list_requirements,
  get_requirement,
  create_requirement,
  update_requirement,
  delete_requirement,
  list_tasks,
  get_task,
  create_task,
  update_task,
  delete_task,
  add_task_comment,
  list_task_comments,
  list_bugs,
  get_my_bugs,
  get_bug,
  create_bug,
  update_bug,
  delete_bug,
  list_documents,
  get_document,
  create_document,
  update_document,
  delete_document,
  list_milestones,
  get_milestone,
  create_milestone,
  update_milestone,
  delete_milestone,
  list_topics,
  get_topic,
  create_topic,
  reply_topic,
  get_notifications,
  mark_notification_read,
  list_roles,
  get_role,
  create_role,
  update_role,
  delete_role,
  list_permissions
};
