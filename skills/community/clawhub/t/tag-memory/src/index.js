/**
 * TagMemory - OpenClaw Skill
 * 标签化长期记忆系统
 */

const { spawn } = require('child_process');
const path = require('path');

// 技能根目录
const SKILL_ROOT = path.resolve(__dirname, '..');

// 执行 Python 脚本（使用 JSON stdin）
function execPython(command, args = {}) {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(SKILL_ROOT, 'src', 'cli.py');
        const child = spawn('python3', [scriptPath, '--json', command], {
            cwd: path.join(SKILL_ROOT, 'src'),
            stdio: ['pipe', 'pipe', 'pipe']
        });

        let stdout = '';
        let stderr = '';

        child.stdin.write(JSON.stringify(args));
        child.stdin.end();

        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        child.on('close', (code) => {
            if (code === 0) {
                try {
                    const result = stdout.trim() ? JSON.parse(stdout.trim()) : {};
                    resolve(result);
                } catch (e) {
                    resolve({ output: stdout.trim(), raw: true });
                }
            } else {
                reject(new Error(stderr || `Python exited with code ${code}`));
            }
        });

        child.on('error', reject);
    });
}

// 工具实现
const tools = {
    async tag_memory_store({ content, tags, time_label, source = 'dialogue', force = false }) {
        const result = await execPython('store', { content, tags, time_label, source, force });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_query({ query, tags, time_range, limit = 5 }) {
        const result = await execPython('query', { query, tags, time_range, limit });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_verify({ memory_id, action, correction }) {
        const result = await execPython('verify', { memory_id, action, correction });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_list({ tags, verified_only, page = 1, page_size = 20 }) {
        const result = await execPython('list', { tags, verified_only, page, page_size });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_verify_pending({ max_count = 3 }) {
        const result = await execPython('verify-pending', { max_count });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_verify_result({ index, action, correction }) {
        const result = await execPython('verify-result', { index, action, correction });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_summarize({ days = 7 }) {
        const result = await execPython('summarize', { days });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_summarize_confirm({ feedback = 'confirm' }) {
        const result = await execPython('summarize-confirm', { feedback });
        return { success: true, ...result, _format: 'markdown' };
    },

    async tag_memory_stats() {
        const result = await execPython('stats', {});
        return { success: true, ...result, _format: 'markdown' };
    }
};

// 导出
module.exports = { tools, name: 'tag-memory', version: '1.0.0' };
