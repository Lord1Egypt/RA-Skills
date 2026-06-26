"use strict";
/**
 * OpenViking Memory Skill
 * 调用 OpenViking API 进行语义记忆搜索和管理
 */

const VIKING_API_URL = 'http://127.0.0.1:18790';

// Skill metadata
const skillName = 'viking-memory';
const skillVersion = '1.0.0';
const skillDescription = 'OpenViking 长期记忆系统 - 语义检索用户偏好、历史对话等';

// HTTP helper
async function vikingRequest(endpoint, body) {
    const response = await fetch(`${VIKING_API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        throw new Error(`Viking API error: ${response.status} ${await response.text()}`);
    }

    return response.json();
}

// Handlers
async function searchHandler(args) {
    const { query, limit = 5, threshold = 0.3 } = args;

    const result = await vikingRequest('/api/v1/search/find', {
        query,
        limit,
        threshold,
    });

    if (!result.result || result.result.total === 0) {
        return { content: [{ type: 'text', text: '没有找到相关记忆。' }] };
    }

    const memories = result.result.resources || [];
    const text = memories
        .map((m, i) => `${i + 1}. [${m.uri}]\n   ${m.abstract || m.overview || '(无内容)'}\n   相关度: ${(m.score * 100).toFixed(0)}%`)
        .join('\n\n');

    return {
        content: [{ type: 'text', text: `找到 ${memories.length} 条相关记忆:\n\n${text}` }],
        details: { count: memories.length, memories },
    };
}

async function addMemoryHandler(args) {
    const { uri, content } = args;

    if (!uri || !content) {
        throw new Error('需要提供 uri 和 content 参数');
    }

    const result = await vikingRequest('/api/v1/resources', {
        uri,
        content,
    });

    return {
        content: [{ type: 'text', text: `已保存记忆: ${uri}` }],
        details: { uri, status: result.status },
    };
}

async function readMemoryHandler(args) {
    const { uri } = args;

    if (!uri) {
        throw new Error('需要提供 uri 参数');
    }

    const result = await vikingRequest('/api/v1/content/read', { uri });

    return {
        content: [{ type: 'text', text: result.result?.content || '(无内容)' }],
        details: { uri, ...result.result },
    };
}

async function listMemoriesHandler(args) {
    const { path = '/', limit = 20 } = args;

    const result = await vikingRequest('/api/v1/fs/ls', { path, limit });

    const items = result.result || [];
    const text = items.map(item => `${item.type === 'dir' ? '📁' : '📄'} ${item.name}`).join('\n');

    return {
        content: [{ type: 'text', text: text || '目录为空' }],
        details: { items },
    };
}

async function statusHandler() {
    const result = await vikingRequest('/api/v1/system/status', {});

    return {
        content: [{
            type: 'text',
            text: `Viking 状态:\n- 向量数量: ${result.result?.vikingdb?.collections?.[0]?.vector_count || 0}\n- 处理队列: ${result.result?.queue?.total?.processed || 0}`
        }],
    };
}

// Skill definition
const skill = {
    name: skillName,
    version: skillVersion,
    description: skillDescription,
    actions: {
        search: {
            description: '语义搜索记忆 - 用自然语言描述搜索相关内容',
            parameters: {
                type: 'object',
                properties: {
                    query: { type: 'string', description: '搜索查询' },
                    limit: { type: 'number', description: '返回结果数量', default: 5 },
                    threshold: { type: 'number', description: '相似度阈值', default: 0.3 },
                },
                required: ['query'],
            },
            handler: searchHandler,
        },
        add_memory: {
            description: '添加记忆 - 将重要信息存入长期记忆',
            parameters: {
                type: 'object',
                properties: {
                    uri: { type: 'string', description: '记忆 URI (如: viking://user/preferences/咖啡)' },
                    content: { type: 'string', description: '记忆内容' },
                },
                required: ['uri', 'content'],
            },
            handler: addMemoryHandler,
        },
        read_memory: {
            description: '读取记忆 - 获取指定记忆的完整内容',
            parameters: {
                type: 'object',
                properties: {
                    uri: { type: 'string', description: '记忆 URI' },
                },
                required: ['uri'],
            },
            handler: readMemoryHandler,
        },
        list: {
            description: '列出记忆 - 查看已存储的记忆列表',
            parameters: {
                type: 'object',
                properties: {
                    path: { type: 'string', description: '路径', default: '/' },
                    limit: { type: 'number', description: '数量', default: 20 },
                },
            },
            handler: listMemoriesHandler,
        },
        status: {
            description: '查看状态 - 查看 Viking 记忆系统状态',
            parameters: {
                type: 'object',
                properties: {},
            },
            handler: statusHandler,
        },
    },
};

module.exports = skill;
