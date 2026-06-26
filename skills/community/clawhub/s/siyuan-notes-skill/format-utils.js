/**
 * 辅助函数：格式化日期为思源时间戳格式
 * @param {string} format - 格式模板
 * @param {Date|number|string} date - 日期
 * @returns {string} 格式化字符串
 */
function strftime(format, date) {
    const d = new Date(date);
    if (Number.isNaN(d.getTime())) {
        return String(format || '');
    }
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hour = String(d.getHours()).padStart(2, '0');
    const minute = String(d.getMinutes()).padStart(2, '0');
    const second = String(d.getSeconds()).padStart(2, '0');
    const tokenMap = {
        '%Y': String(year),
        '%m': month,
        '%d': day,
        '%H': hour,
        '%M': minute,
        '%S': second
    };
    return String(format || '').replace(/%[YmdHMS]/g, (token) => tokenMap[token] || token);
}

/**
 * 截断文本
 * @param {string} text - 输入文本
 * @param {number} maxLength - 最大长度
 * @returns {string} 截断结果
 */
function truncateText(text, maxLength = 160) {
    const value = String(text || '').replace(/\s+/g, ' ').trim();
    if (value.length <= maxLength) {
        return value;
    }

    return `${value.slice(0, maxLength)}...`;
}

/**
 * 格式化思源时间戳为可读字符串
 * @param {string} timeStr - 思源时间戳 (YYYYMMDDHHMMSS)
 * @returns {string} 格式化后的时间字符串
 */
function formatSiyuanTime(timeStr) {
    if (!timeStr || timeStr.length !== 14) {
        return '未知时间';
    }

    const year = timeStr.substring(0, 4);
    const month = timeStr.substring(4, 6);
    const day = timeStr.substring(6, 8);
    const hour = timeStr.substring(8, 10);
    const minute = timeStr.substring(10, 12);
    const second = timeStr.substring(12, 14);

    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 格式化查询结果为可读字符串
 * @param {Array} results - 查询结果数组
 * @param {Object} options - 格式化选项
 * @returns {string} 格式化后的字符串
 */
function formatResults(results, options = {}) {
    const {
        showIndex = true,
        showTime = true,
        showType = true,
        showPath = false,
        contentLength = 100,
        separator = '\n'
    } = options;

    if (!results || results.length === 0) {
        return '查询结果为空';
    }

    return results.map((item, index) => {
        const parts = [];

        if (showIndex) {
            parts.push(`${index + 1}.`);
        }

        if (item.id) {
            parts.push(`[${item.id}]`);
        }

        if (showTime && (item.updated || item.created)) {
            const time = formatSiyuanTime(item.updated || item.created);
            parts.push(`[${time}]`);
        }

        if (showType) {
            const type = item.subtype || item.type || 'unknown';
            parts.push(`${type}:`);
        }

        const markdown = typeof item.markdown === 'string' ? item.markdown : '';
        const hasImage = /!\[[^\]]*\]\([^\n)]+\)/.test(markdown)
            || /!\[[^\]]*\]\[[^\]]+\]/.test(markdown)
            || /<img\s+[^>]*src\s*=/.test(markdown.toLowerCase());

        let content = item.content || '(无内容)';
        if (hasImage) {
            content = content === '(无内容)' ? '[img]' : `[img] ${content}`;
        }

        if (content.length > contentLength) {
            parts.push(content.substring(0, contentLength) + '...');
        } else {
            parts.push(content);
        }

        if (showPath && item.hpath) {
            parts.push(`(${item.hpath})`);
        }

        return parts.join(' ');
    }).join(separator);
}

/**
 * 格式化查询结果为结构化数据
 * @param {Array} results - 查询结果数组
 * @returns {Object} 结构化结果
 */
function formatStructuredResults(results) {
    if (!results || results.length === 0) {
        return {
            success: true,
            count: 0,
            message: '查询结果为空',
            data: []
        };
    }

    return {
        success: true,
        count: results.length,
        message: `找到 ${results.length} 条结果`,
        data: results.map((item) => ({
            id: item.id,
            content: item.content || '',
            type: item.type || '',
            subtype: item.subtype || '',
            created: formatSiyuanTime(item.created),
            updated: formatSiyuanTime(item.updated),
            path: item.hpath || '',
            root_id: item.root_id || ''
        }))
    };
}

/**
 * 生成思源嵌入块格式的SQL查询
 * @param {string} sqlQuery - SQL查询语句
 * @returns {string} 嵌入块格式的SQL
 */
function generateEmbedBlock(sqlQuery) {
    return `{{select * from blocks WHERE ${sqlQuery}}}`;
}

module.exports = {
    strftime,
    truncateText,
    formatSiyuanTime,
    formatResults,
    formatStructuredResults,
    generateEmbedBlock
};
