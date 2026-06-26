'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

/**
 * wecom-deep-op - Enterprise WeChat All-in-One Skill
 *
 * This skill provides a unified interface to all WeCom (Enterprise WeChat)
 * MCP capabilities: documents, calendar/schedule, meetings, todos, and contacts.
 *
 * @package wecom-deep-op
 * @author 白小圈
 * @license MIT
 */
// ============================================================================
// Custom Error Class
// ============================================================================
/**
 * 企业微信API错误类
 * 封装企业微信返回的错误信息，提供更清晰的错误消息
 */
class WeComError extends Error {
    constructor(message, errcode, errmsg, data) {
        super(message);
        this.name = 'WeComError';
        this.errcode = errcode;
        this.errmsg = errmsg;
        this.data = data;
    }
    toString() {
        return `${this.name}: ${this.message} (errcode=${this.errcode}, errmsg=${this.errmsg})`;
    }
}
// ============================================================================
// Logger Utility
// ============================================================================
/**
 * 简单日志工具
 * 支持 debug/info/error 级别，可通过环境变量控制
 */
class Logger {
    constructor(service) {
        this.prefix = `[${service}]`;
        const envLevel = process.env.DEBUG_LEVEL || 'info';
        this.level = envLevel;
    }
    debug(message, meta) {
        if (this.level === 'debug')
            console.debug(this.prefix, message, meta ?? '');
    }
    info(message, meta) {
        if (this.level === 'debug' || this.level === 'info')
            console.info(this.prefix, message, meta ?? '');
    }
    warn(message, meta) {
        if (this.level === 'debug' || this.level === 'info' || this.level === 'warn') {
            console.warn(this.prefix, message, meta ?? '');
        }
    }
    error(message, error) {
        console.error(this.prefix, message, error ?? '');
    }
}
// ============================================================================
// Validation Utilities
// ============================================================================
/**
 * 参数验证工具 - 为所有 API 函数提供运行时验证
 */
function assertString(value, name) {
    if (typeof value !== 'string' || !value.trim()) {
        throw new WeComError(`Invalid parameter: ${name} must be a non-empty string`, 400, 'invalid_parameter');
    }
    return value;
}
function assertNumber(value, name, min, max) {
    if (typeof value !== 'number' || isNaN(value)) {
        throw new WeComError(`Invalid parameter: ${name} must be a number`, 400, 'invalid_parameter');
    }
    if (min !== undefined && value < min) {
        throw new WeComError(`Invalid parameter: ${name} must be >= ${min}`, 400, 'invalid_parameter');
    }
    if (max !== undefined && value > max) {
        throw new WeComError(`Invalid parameter: ${name} must be <= ${max}`, 400, 'invalid_parameter');
    }
    return value;
}
function assertArray(value, name, itemValidator) {
    if (!Array.isArray(value)) {
        throw new WeComError(`Invalid parameter: ${name} must be an array`, 400, 'invalid_parameter');
    }
    if (itemValidator) {
        for (let i = 0; i < value.length; i++) {
            itemValidator(value[i], i);
        }
    }
    return value;
}
// ============================================================================
// Configuration & Constants
// ============================================================================
const WECOM_SERVICES = {
    doc: {
        basePath: '/mcp/bot/doc',
        tools: ['get_doc_content', 'create_doc', 'edit_doc_content']
    },
    schedule: {
        basePath: '/mcp/bot/schedule',
        tools: ['create', 'get', 'update', 'delete', 'list', 'add_attendee', 'remove_attendee']
    },
    meeting: {
        basePath: '/mcp/bot/meeting',
        tools: ['create', 'get', 'update_attendee', 'cancel', 'list']
    },
    todo: {
        basePath: '/mcp/bot/todo',
        tools: ['create', 'get', 'update', 'delete', 'list']
    },
    contact: {
        basePath: '/mcp/bot/contact',
        tools: ['get_userlist']
    }
};
// ============================================================================
// Configuration Check Helper
// ============================================================================
/**
 * 检查指定服务的配置是否就绪
 * @param service - 服务名称 (doc/schedule/meeting/todo/contact)
 * @returns 配置检查结果对象
 */
function checkServiceConfig(service) {
    const envVar = `WECOM_${service.toUpperCase()}_BASE_URL`;
    if (process.env[envVar]) {
        return { ok: true };
    }
    // 生成配置指引
    const instruction = `⚠️ **配置缺失**: 服务 [${service}] 的环境变量未设置。

**请选择配置方式**：

方式一：环境变量（推荐）
在终端执行：
\`\`\`bash
export ${envVar}="https://qyapi.weixin.qq.com/mcp/bot/${service}?uaKey=YOUR_UA_KEY"
\`\`\`

方式二：mcporter.json 配置文件
编辑 \`~/.openclaw/workspace/config/mcporter.json\`：
\`\`\`json
{
  "mcpServers": {
    "wecom-${service}": {
      "baseUrl": "https://qyapi.weixin.qq.com/mcp/bot/${service}?uaKey=YOUR_UA_KEY"
    }
  }
}
\`\`\`

**如何获取 uaKey**：
1. 登录企业微信管理后台
2. 进入「应用管理」→「自建应用」→ 选择你的BOT
3. 在「权限管理」中开通 MCP 权限
4. 复制对应服务的 uaKey 参数

**验证配置**：
配置完成后，运行以下命令检查：
\`wecom_mcp call wecom-deep-op.preflight_check "{}"\`

详细说明请参阅 README.md 的「安全与隐私」章节。`;
    return { ok: false, instruction };
}
// ============================================================================
// Utility Functions
// ============================================================================
/**
 * 实现说明：
 * - 本 Skill 作为 OpenClaw 的技能插件，会被 OpenClaw 自动加载
 * - OpenClaw 会调用 skill.exportedTools 中注册的工具函数
 * - 所有工具函数都是异步的，返回标准 JSON 对象
 *
 * 配置要求：
 * - 用户需要在自己的 mcporter.json 中配置 wecom-doc / wecom-schedule / wecom-meeting / wecom-todo / wecom-contact 五个端点
 * - 或使用本 Skill 提供的统一配置端点 wecom-deep-op（如果配置了代理模式）
 *
 * 安全原则：
 * - 绝不硬编码任何 uaKey 或凭证
 * - 从环境变量或用户配置读取 endpoint 信息
 * - 所有敏感配置必须由用户自己管理
 */
const skillMetadata = {
    name: 'wecom-deep-op',
    version: '1.0.0',
    description: '企业微信全能操作Skill - 统一封装文档、日程、会议、待办、通讯录',
    author: '白小圈',
    license: 'MIT'
};
/**
 * 获取企业微信 MCP 服务的 baseUrl
 * 优先级：环境变量 > 配置文件（本Skill不负责配置文件读取，由OpenClaw运行时注入）
 */
function getServiceUrl(service) {
    // 在 OpenClaw Skill 中，配置通过 runtime context 传递
    // 这里使用环境变量作为 fallback（仅用于开发测试）
    const envVar = `WECOM_${service.toUpperCase()}_BASE_URL`;
    const url = process.env[envVar];
    if (!url) {
        throw new Error(`Missing configuration for ${service}. ` +
            `Set environment variable ${envVar} or configure in OpenClaw. ` +
            `Example: https://qyapi.weixin.qq.com/mcp/bot/${service}?uaKey=YOUR_KEY`);
    }
    return url;
}
/**
 * 智能重试函数（指数退避）
 */
async function withRetry(fn, maxRetries = 3, baseDelay = 1000) {
    let lastError = null;
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        }
        catch (error) {
            lastError = error;
            // 如果不是网络错误或业务错误（非0），不重试
            if (error instanceof WeComError) {
                // 业务错误（errcode != 0）直接抛出
                throw error;
            }
            if (i === maxRetries - 1)
                break;
            // 指数退避等待
            const delay = baseDelay * Math.pow(2, i);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
    throw lastError;
}
/**
 * 执行 HTTP 请求到企业微信 MCP 端点（带重试）
 */
async function callWeComApi(service, tool, params = {}, logger) {
    const baseUrl = getServiceUrl(service);
    const url = `${baseUrl}/${tool}`;
    const makeRequest = async () => {
        logger?.debug(`${service}.${tool}`, params);
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        const data = (await response.json()); // 明确声明为any
        if (!response.ok || data.errcode !== 0) {
            const errmsg = data.errmsg || `HTTP ${response.status}`;
            logger?.error(`${service}.${tool} failed`, { errcode: data.errcode, errmsg });
            if (data.errcode !== 0) {
                // 业务错误，抛出WeComError（不重试）
                throw new WeComError(`企业微信API错误: ${errmsg}`, data.errcode, errmsg, data);
            }
            else {
                // HTTP错误，可重试
                throw new Error(`${response.status}: ${errmsg}`);
            }
        }
        logger?.debug(`${service}.${tool} success`);
        return data;
    };
    return await withRetry(makeRequest, 3, 1000);
}
// ============================================================================
// Document Operations (doc_*)
// ============================================================================
/**
 * 导出/获取文档内容
 * @param docid - 文档ID，或提供 url
 * @param type - 导出类型，固定为 2 (Markdown)
 * @param task_id - 如果有，表示轮询
 */
async function doc_get(docid, url, task_id) {
    // ✅ 参数验证
    if (docid)
        assertString(docid, 'docid');
    if (url)
        assertString(url, 'url');
    if (task_id)
        assertString(task_id, 'task_id');
    if (!docid && !url) {
        throw new WeComError('doc_get requires either docid or url', 400, 'invalid_parameter');
    }
    const logger = new Logger('doc');
    logger.debug('doc_get called', { docid, url, task_id });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('doc');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for doc service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'doc',
                instruction: configCheck.instruction
            }
        };
    }
    const params = { type: 2 };
    if (docid)
        params.docid = docid;
    if (url)
        params.url = url;
    if (task_id)
        params.task_id = task_id;
    const result = await callWeComApi('doc', 'get_doc_content', params, logger);
    // 如果任务未完成，需要轮询（OpenClaw不会自动轮询，这里返回task_id供后续调用）
    if (!result.task_done && !task_id) {
        logger.info('Task started, polling required', { task_id: result.task_id });
        return {
            errcode: 0,
            errmsg: 'ok',
            task_id: result.task_id,
            task_done: false,
            message: 'Task started, poll with task_id to get result'
        };
    }
    // 如果返回了 task_done 但没内容，可能是轮询中，返回 task_id
    if (result.task_done && !result.content && !task_id) {
        logger.info('Task done but no content yet, polling again', { task_id: result.task_id });
        return {
            errcode: 0,
            errmsg: 'ok',
            task_id: result.task_id,
            task_done: false
        };
    }
    logger.debug('doc_get success');
    return result;
}
/**
 * 创建文档
 * @param doc_type - 文档类型：3=文档，10=智能表格
 * @param doc_name - 文档名称
 */
async function doc_create(doc_type, doc_name) {
    // ✅ 参数验证
    assertNumber(doc_type, 'doc_type', 3, 10);
    assertString(doc_name, 'doc_name');
    const logger = new Logger('doc');
    logger.info('Creating document', { doc_type, doc_name });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('doc');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for doc service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'doc',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('doc', 'create_doc', {
        doc_type,
        doc_name
    }, logger);
    logger.info('Document created successfully', { docid: result.docid });
    return result;
}
/**
 * 编辑/覆写文档内容
 * @param docid - 文档ID
 * @param content - Markdown内容
 * @param content_type - 内容类型，固定为 1 (Markdown)
 */
async function doc_edit(docid, content, content_type = 1) {
    // ✅ 参数验证
    assertString(docid, 'docid');
    assertString(content, 'content');
    assertNumber(content_type, 'content_type', 1, 1); // 必须为 1
    const logger = new Logger('doc');
    logger.info('Editing document', { docid, content_length: content.length });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('doc');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for doc service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'doc',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('doc', 'edit_doc_content', {
        docid,
        content,
        content_type
    }, logger);
    logger.info('Document edited successfully', { docid });
    return result;
}
// ============================================================================
// Schedule Operations (schedule_*)
// ============================================================================
/**
 * 创建日程
 */
async function schedule_create(params) {
    // ✅ 参数验证
    assertString(params.summary, 'summary');
    assertString(params.start_time, 'start_time');
    assertString(params.end_time, 'end_time');
    if (params.location !== undefined)
        assertString(params.location, 'location');
    if (params.description !== undefined)
        assertString(params.description, 'description');
    if (params.attendees)
        assertArray(params.attendees, 'attendees', (uid) => assertString(uid, 'attendee'));
    if (params.reminders)
        assertArray(params.reminders, 'reminders', (r) => {
            assertNumber(r.type, 'reminder.type', 0, 3);
            assertNumber(r.minutes, 'reminder.minutes', 1);
        });
    const logger = new Logger('schedule');
    logger.info('Creating schedule', { summary: params.summary, start_time: params.start_time });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for schedule service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('schedule', 'create', params, logger);
    logger.info('Schedule created successfully', { schedule_id: result.scheduleid });
    return result;
}
/**
 * 查询日程
 */
async function schedule_list(start_time, end_time, 
// 其他可选筛选参数...
params = {}) {
    // ✅ 参数验证
    assertString(start_time, 'start_time');
    assertString(end_time, 'end_time');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'list', {
        start_time,
        end_time,
        ...params
    });
}
/**
 * 获取日程详情
 */
async function schedule_get(schedule_id) {
    // ✅ 参数验证
    assertString(schedule_id, 'schedule_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'get', { schedule_id });
}
/**
 * 更新日程
 */
async function schedule_update(schedule_id, updates) {
    // ✅ 参数验证
    assertString(schedule_id, 'schedule_id');
    if (updates.summary !== undefined)
        assertString(updates.summary, 'updates.summary');
    if (updates.start_time !== undefined)
        assertString(updates.start_time, 'updates.start_time');
    if (updates.end_time !== undefined)
        assertString(updates.end_time, 'updates.end_time');
    if (updates.location !== undefined)
        assertString(updates.location, 'updates.location');
    if (updates.description !== undefined)
        assertString(updates.description, 'updates.description');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'update', {
        schedule_id,
        ...updates
    });
}
/**
 * 取消日程
 */
async function schedule_cancel(schedule_id) {
    // ✅ 参数验证
    assertString(schedule_id, 'schedule_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'delete', { schedule_id });
}
/**
 * 添加参会人
 */
async function schedule_add_attendee(schedule_id, attendee_userids) {
    // ✅ 参数验证
    assertString(schedule_id, 'schedule_id');
    assertArray(attendee_userids, 'attendee_userids', (uid) => assertString(uid, 'attendee'));
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'add_attendee', {
        schedule_id,
        attendee_userids
    });
}
/**
 * 移除参会人
 */
async function schedule_remove_attendee(schedule_id, attendee_userids) {
    // ✅ 参数验证
    assertString(schedule_id, 'schedule_id');
    assertArray(attendee_userids, 'attendee_userids', (uid) => assertString(uid, 'attendee'));
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('schedule');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'schedule',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('schedule', 'remove_attendee', {
        schedule_id,
        attendee_userids
    });
}
// ============================================================================
// Meeting Operations (meeting_*)
// ============================================================================
/**
 * 创建/预约会议
 */
async function meeting_create(params) {
    // ✅ 参数验证
    assertString(params.subject, 'subject');
    assertString(params.start_time, 'start_time');
    assertString(params.end_time, 'end_time');
    if (params.type !== undefined)
        assertNumber(params.type, 'type', 1, 3);
    if (params.attendees)
        assertArray(params.attendees, 'attendees', (uid) => assertString(uid, 'attendee'));
    if (params.agenda !== undefined)
        assertString(params.agenda, 'agenda');
    if (params.media_conf_id !== undefined)
        assertString(params.media_conf_id, 'media_conf_id');
    if (params.meeting_room_id !== undefined)
        assertString(params.meeting_room_id, 'meeting_room_id');
    const logger = new Logger('meeting');
    logger.info('Creating meeting', { subject: params.subject, start_time: params.start_time });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('meeting');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for meeting service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'meeting',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('meeting', 'create', params, logger);
    logger.info('Meeting created successfully', { meeting_id: result.meetingid });
    return result;
}
/**
 * 查询会议列表
 */
async function meeting_list(start_time, end_time, params = {}) {
    // ✅ 参数验证
    assertString(start_time, 'start_time');
    assertString(end_time, 'end_time');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('meeting');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'meeting',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('meeting', 'list', {
        start_time,
        end_time,
        ...params
    });
}
/**
 * 获取会议详情
 */
async function meeting_get(meeting_id) {
    // ✅ 参数验证
    assertString(meeting_id, 'meeting_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('meeting');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'meeting',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('meeting', 'get', { meeting_id });
}
/**
 * 取消会议
 */
async function meeting_cancel(meeting_id) {
    // ✅ 参数验证
    assertString(meeting_id, 'meeting_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('meeting');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'meeting',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('meeting', 'cancel', { meeting_id });
}
/**
 * 更新会议参会人
 */
async function meeting_update_attendees(meeting_id, add_attendees, remove_attendees) {
    // ✅ 参数验证
    assertString(meeting_id, 'meeting_id');
    if (add_attendees)
        assertArray(add_attendees, 'add_attendees', (uid) => assertString(uid, 'attendee'));
    if (remove_attendees)
        assertArray(remove_attendees, 'remove_attendees', (uid) => assertString(uid, 'attendee'));
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('meeting');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'meeting',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('meeting', 'update_attendee', {
        meeting_id,
        add_attendees,
        remove_attendees
    });
}
// ============================================================================
// Todo Operations (todo_*)
// ============================================================================
/**
 * 创建待办
 */
async function todo_create(params) {
    // ✅ 参数验证
    assertString(params.title, 'title');
    if (params.due_time !== undefined)
        assertString(params.due_time, 'due_time');
    if (params.priority !== undefined)
        assertNumber(params.priority, 'priority', 1, 3);
    if (params.desc !== undefined)
        assertString(params.desc, 'desc');
    if (params.receivers)
        assertArray(params.receivers, 'receivers', (uid) => assertString(uid, 'receiver'));
    if (params.creator !== undefined)
        assertString(params.creator, 'creator');
    const logger = new Logger('todo');
    logger.info('Creating todo', { title: params.title, priority: params.priority });
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        logger.warn('Configuration missing for todo service');
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('todo', 'create', params, logger);
    logger.info('Todo created successfully', { todo_id: result.todo_id });
    return result;
}
/**
 * 获取待办列表
 */
async function todo_list(status, // 0=未开始, 1=进行中, 2=完成
limit, offset) {
    // ✅ 参数验证
    if (status !== undefined)
        assertNumber(status, 'status', 0, 2);
    if (limit !== undefined)
        assertNumber(limit, 'limit', 1, 1000);
    if (offset !== undefined)
        assertNumber(offset, 'offset', 0);
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'list', {
        status,
        limit,
        offset
    });
}
/**
 * 获取待办详情
 */
async function todo_get(todo_id) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'get', { todo_id });
}
/**
 * 更新待办状态
 */
async function todo_update_status(todo_id, status) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    assertNumber(status, 'status', 0, 2);
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'update', {
        todo_id,
        status
    });
}
/**
 * 更新待办内容
 */
async function todo_update(todo_id, updates) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    if (updates.title !== undefined)
        assertString(updates.title, 'updates.title');
    if (updates.due_time !== undefined)
        assertString(updates.due_time, 'updates.due_time');
    if (updates.priority !== undefined)
        assertNumber(updates.priority, 'updates.priority', 1, 3);
    if (updates.desc !== undefined)
        assertString(updates.desc, 'updates.desc');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'update', {
        todo_id,
        ...updates
    });
}
/**
 * 删除待办
 */
async function todo_delete(todo_id) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'delete', { todo_id });
}
/**
 * 接收待办
 */
async function todo_accept(todo_id) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'accept', { todo_id });
}
/**
 * 拒绝待办
 */
async function todo_refuse(todo_id, reason) {
    // ✅ 参数验证
    assertString(todo_id, 'todo_id');
    if (reason !== undefined)
        assertString(reason, 'reason');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('todo');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'todo',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('todo', 'refuse', {
        todo_id,
        reason
    });
}
// ============================================================================
// Contact Operations (contact_*)
// ============================================================================
/**
 * 获取通讯录成员列表（当前用户可见范围）
 * ⚠️ 限制：只返回当前用户**可见范围内**的成员（通常≤100人，建议≤10人使用）
 */
async function contact_get_userlist() {
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('contact');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'contact',
                instruction: configCheck.instruction
            }
        };
    }
    return await callWeComApi('contact', 'get_userlist', {});
}
/**
 * 搜索成员（本地筛选）
 * 说明：企业微信MCP不支持服务端搜索，本函数获取全量后本地过滤
 */
async function contact_search(keyword) {
    // ✅ 参数验证
    assertString(keyword, 'keyword');
    // 🔍 智能配置检查
    const configCheck = checkServiceConfig('contact');
    if (!configCheck.ok) {
        return {
            errcode: 1,
            errmsg: 'configuration_missing',
            data: {
                service: 'contact',
                instruction: configCheck.instruction
            }
        };
    }
    const result = await callWeComApi('contact', 'get_userlist', {});
    if (result.errcode !== 0) {
        return result;
    }
    const allUsers = result.userlist || [];
    const matched = allUsers.filter((u) => u.name.includes(keyword) ||
        (u.alias && u.alias.includes(keyword)));
    return {
        errcode: 0,
        errmsg: 'ok',
        total: allUsers.length,
        matched_count: matched.length,
        userlist: matched
    };
}
// ============================================================================
// Utility / Preflight
// ============================================================================
/**
 * 健康检查/就绪探测（Ping）
 * 用于验证 skill 加载、插件版本和配置是否正确
 *
 * 新增：检查企业微信官方插件版本是否 ≥ 1.0.13
 */
async function ping() {
    const configuredServices = Object.keys(WECOM_SERVICES)
        .filter(svc => process.env[`WECOM_${svc.toUpperCase()}_BASE_URL`])
        .map(svc => ({ service: svc, status: 'configured' }));
    // 检查插件版本
    let pluginCheck = { status: 'unknown' };
    try {
        const fs = require('fs');
        const path = require('path');
        const pluginPkgPath = path.join(process.cwd(), 'node_modules/@wecom/wecom-openclaw-plugin/package.json');
        if (fs.existsSync(pluginPkgPath)) {
            const pluginPkg = JSON.parse(fs.readFileSync(pluginPkgPath, 'utf-8'));
            const currentVersion = pluginPkg.version;
            const required = '1.0.13';
            // 版本比较
            const cur = currentVersion.replace(/[^\d.]/g, '').split('.').map(Number);
            const req = required.replace(/[^\d.]/g, '').split('.').map(Number);
            const isCompatible = cur[0] > req[0] ||
                (cur[0] === req[0] && cur[1] > req[1]) ||
                (cur[0] === req[0] && cur[1] === req[1] && cur[2] >= req[2]);
            pluginCheck = {
                status: isCompatible ? 'ok' : 'outdated',
                version: currentVersion,
                message: isCompatible
                    ? `官方插件版本符合要求 (v${currentVersion} ≥ v${required})`
                    : `官方插件版本过低: v${currentVersion}（需要 ≥ v${required}），请升级`
            };
        }
        else {
            pluginCheck = {
                status: 'missing',
                message: '未检测到企业微信官方插件 (@wecom/wecom-openclaw-plugin)，请先安装'
            };
        }
    }
    catch (e) {
        pluginCheck = {
            status: 'error',
            message: `无法检测插件版本: ${e instanceof Error ? e.message : String(e)}`
        };
    }
    // 构建响应
    const response = {
        errcode: 0,
        errmsg: 'ok',
        data: {
            service: 'wecom-deep-op',
            version: skillMetadata.version,
            status: 'healthy',
            configured_services: configuredServices,
            plugin_check: pluginCheck,
            notice: 'This skill requires mcporter.json configuration or environment variables for each service endpoint.'
        }
    };
    // 如果插件异常，仍返回健康状态但加入警告
    if (pluginCheck.status !== 'ok') {
        response.data.warning = pluginCheck.message;
    }
    return response;
}
/**
 * 前置条件检查（Preflight）
 * 验证配置是否完整，如缺失则提供修复建议
 *
 * 新增：检查企业微信官方插件版本
 */
async function preflight_check() {
    const missing = [];
    const present = [];
    const warnings = [];
    // 1️⃣ 检查企业微信官方插件版本
    try {
        // 动态导入官方插件（如果可用）
        const wecomPluginPath = 'node_modules/@wecom/wecom-openclaw-plugin/package.json';
        const fs = require('fs');
        const pluginPkgPath = require('path').join(process.cwd(), wecomPluginPath);
        if (fs.existsSync(pluginPkgPath)) {
            const pluginPkg = JSON.parse(fs.readFileSync(pluginPkgPath, 'utf-8'));
            const pluginVersion = pluginPkg.version;
            const requiredVersion = '1.0.13';
            const pluginName = '@wecom/wecom-openclaw-plugin';
            // 简单版本比较（移除前缀，取数字部分）
            const current = pluginVersion.replace(/[^\d.]/g, '').split('.').map(Number);
            const required = requiredVersion.replace(/[^\d.]/g, '').split('.').map(Number);
            // 如果当前版本低于最低要求
            if (current[0] < required[0] ||
                (current[0] === required[0] && current[1] < required[1]) ||
                (current[0] === required[0] && current[1] === required[1] && current[2] < required[2])) {
                warnings.push(`⚠️ 企业微信官方插件版本过低: ${pluginVersion} (需要 ≥ ${requiredVersion})\n  请升级: npm install ${pluginName}@latest --save`);
            }
            else {
                present.push(` Official plugin (${pluginName} v${pluginVersion})`);
            }
        }
        else {
            warnings.push(`❌ 企业微信官方插件未安装 (@wecom/wecom-openclaw-plugin)\n  请安装: npm install @wecom/wecom-openclaw-plugin --save`);
        }
    }
    catch (e) {
        // 插件检查失败不影响主流程，仅记录警告
        warnings.push(`⚠️ 无法检测企业微信官方插件版本（请手动检查）`);
    }
    // 2️⃣ 检查环境变量配置
    for (const service of Object.keys(WECOM_SERVICES)) {
        const envVar = `WECOM_${service.toUpperCase()}_BASE_URL`;
        if (process.env[envVar]) {
            present.push(service);
        }
        else {
            missing.push(service);
        }
    }
    // 3️⃣ 综合判断
    if (missing.length === 0 && warnings.length === 0) {
        return {
            errcode: 0,
            errmsg: 'ok',
            data: {
                status: 'ready',
                configured_services: present,
                message: 'All WeCom services are configured via environment variables.'
            }
        };
    }
    // 有警告或缺失
    const allIssues = [
        ...warnings,
        ...missing.map(s => `❌ 缺少服务配置: ${s}\n  请设置: WECOM_${s.toUpperCase()}_BASE_URL=https://qyapi.weixin.qq.com/mcp/bot/${s}?uaKey=YOUR_UA_KEY`)
    ];
    return {
        errcode: 1,
        errmsg: missing.length > 0 ? 'incomplete_configuration' : 'outdated_dependency',
        data: {
            status: 'incomplete',
            configured_services: present,
            missing_services: missing,
            version_warnings: warnings,
            issues: allIssues,
            instruction: `请修复以下问题以正常使用 wecom-deep-op:\n\n${allIssues.join('\n')}\n\n详情请参考 README 中的"前置条件"和"安装或升级企业微信官方插件"章节。`
        }
    };
}
// ============================================================================
// OpenClaw Skill Exports
// ============================================================================
/**
 * OpenClaw 加载 Skill 时调用，返回所有可用工具
 */
const exportedTools = {
    // Documents
    'doc_get': doc_get,
    'doc_create': doc_create,
    'doc_edit': doc_edit,
    // Schedules
    'schedule_create': schedule_create,
    'schedule_list': schedule_list,
    'schedule_get': schedule_get,
    'schedule_update': schedule_update,
    'schedule_cancel': schedule_cancel,
    'schedule_add_attendee': schedule_add_attendee,
    'schedule_remove_attendee': schedule_remove_attendee,
    // Meetings
    'meeting_create': meeting_create,
    'meeting_list': meeting_list,
    'meeting_get': meeting_get,
    'meeting_cancel': meeting_cancel,
    'meeting_update_attendees': meeting_update_attendees,
    // Todos
    'todo_create': todo_create,
    'todo_list': todo_list,
    'todo_get': todo_get,
    'todo_update_status': todo_update_status,
    'todo_update': todo_update,
    'todo_delete': todo_delete,
    'todo_accept': todo_accept,
    'todo_refuse': todo_refuse,
    // Contacts
    'contact_get_userlist': contact_get_userlist,
    'contact_search': contact_search,
    // Utilities
    'ping': ping,
    'preflight_check': preflight_check
};

exports.Logger = Logger;
exports.WeComError = WeComError;
exports.contact_get_userlist = contact_get_userlist;
exports.contact_search = contact_search;
exports.default = exportedTools;
exports.doc_create = doc_create;
exports.doc_edit = doc_edit;
exports.doc_get = doc_get;
exports.exportedTools = exportedTools;
exports.meeting_cancel = meeting_cancel;
exports.meeting_create = meeting_create;
exports.meeting_get = meeting_get;
exports.meeting_list = meeting_list;
exports.meeting_update_attendees = meeting_update_attendees;
exports.ping = ping;
exports.preflight_check = preflight_check;
exports.schedule_add_attendee = schedule_add_attendee;
exports.schedule_cancel = schedule_cancel;
exports.schedule_create = schedule_create;
exports.schedule_get = schedule_get;
exports.schedule_list = schedule_list;
exports.schedule_remove_attendee = schedule_remove_attendee;
exports.schedule_update = schedule_update;
exports.skillMetadata = skillMetadata;
exports.todo_accept = todo_accept;
exports.todo_create = todo_create;
exports.todo_delete = todo_delete;
exports.todo_get = todo_get;
exports.todo_list = todo_list;
exports.todo_refuse = todo_refuse;
exports.todo_update = todo_update;
exports.todo_update_status = todo_update_status;
//# sourceMappingURL=index.cjs.js.map
