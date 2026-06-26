function normalizeMarkdown(markdown) {
    const raw = String(markdown || '');
    const normalizedNewlines = raw.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    return normalizedNewlines.replace(/\n{3,}/g, '\n\n').trim();
}

function updateFenceState(state, line) {
    const text = String(line || '').trimStart();
    const match = text.match(/^(`{3,}|~{3,})/);
    if (!match) {
        return;
    }

    const marker = match[1];
    const char = marker[0];
    const size = marker.length;

    if (!state.active) {
        state.active = true;
        state.char = char;
        state.size = size;
        return;
    }

    if (state.char === char && size >= state.size) {
        state.active = false;
        state.char = '';
        state.size = 0;
    }
}

function stripKramdownIAL(markdown) {
    const lines = String(markdown || '').split('\n');
    const output = [];
    const fenceState = { active: false, char: '', size: 0 };

    for (const line of lines) {
        const inFence = fenceState.active;
        const trimmed = line.trim();
        if (!inFence && /^\{:[^}]*\}$/.test(trimmed)) {
            updateFenceState(fenceState, line);
            continue;
        }

        const cleaned = inFence
            ? line
            : line
                .replace(/\s+\{:[^}]*\}\s*$/g, '')
                .replace(/\s+$/g, '');

        output.push(cleaned);
        updateFenceState(fenceState, line);
    }

    return normalizeMarkdown(output.join('\n'));
}

function inferBlockType(markdown) {
    const nonEmptyLines = String(markdown || '')
        .split('\n')
        .map((line) => line.trim())
        .filter((line) => line.length > 0);
    const firstLine = nonEmptyLines[0] || '';
    const secondLine = nonEmptyLines[1] || '';

    if (/^```/.test(firstLine)) {
        return { type: 'c', subType: '' };
    }

    if (/^\$\$/.test(firstLine)) {
        return { type: 'm', subType: '' };
    }

    if (/^\|.*\|$/.test(firstLine) && /^\|\s*[:\-]+\s*(\|\s*[:\-]+\s*)+\|?$/.test(secondLine)) {
        return { type: 't', subType: '' };
    }

    const headingMatch = firstLine.match(/^(#{1,6})\s+/);
    if (headingMatch) {
        const level = headingMatch[1].length;
        return { type: 'h', subType: `h${level}` };
    }

    if (/^\s*[-*+]\s+\[[ xX-]\]\s+/.test(firstLine)) {
        return { type: 'l', subType: 't' };
    }

    if (/^\s*[-*+]\s+/.test(firstLine)) {
        return { type: 'l', subType: 'u' };
    }

    if (/^\s*\d+[.)]\s+/.test(firstLine)) {
        return { type: 'l', subType: 'o' };
    }

    if (/^\s*>\s+/.test(firstLine)) {
        return { type: 'b', subType: '' };
    }

    return { type: 'p', subType: '' };
}

function parseBlocksFromKramdown(kramdown, parentIdMap = {}) {
    const text = String(kramdown || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    if (!text.trim()) {
        return [];
    }

    const lines = text.split('\n');
    const blocks = [];
    let buffer = [];

    for (const line of lines) {
        const match = line.match(/^\{:[^}]*\bid="([^"]+)"[^}]*\}\s*$/);
        if (!match) {
            buffer.push(line);
            continue;
        }

        const markdown = buffer.join('\n').trimEnd();
        const cleanedMarkdown = stripKramdownIAL(markdown);
        const id = match[1];
        const inferred = inferBlockType(cleanedMarkdown);
        blocks.push({
            id,
            markdown: cleanedMarkdown,
            type: inferred.type,
            subType: inferred.subType,
            parentId: parentIdMap[id] || ''
        });
        buffer = [];
    }

    if (buffer.join('\n').trim()) {
        const markdown = buffer.join('\n').trimEnd();
        const cleanedMarkdown = stripKramdownIAL(markdown);
        const inferred = inferBlockType(cleanedMarkdown);
        blocks.push({
            id: `tail-${blocks.length + 1}`,
            markdown: cleanedMarkdown,
            type: inferred.type,
            subType: inferred.subType,
            parentId: ''
        });
    }

    return blocks.filter((block) => block.markdown.trim().length > 0);
}

function renderPatchableMarkdown({ docId, meta, blocks }) {
    const lines = [];
    const updatedPart = meta.updated ? ` updated=${meta.updated}` : '';
    lines.push(`<!-- @siyuan:doc id=${docId} hpath=${JSON.stringify(meta.hpath || '')} view=patchable pmf=v1${updatedPart} -->`);
    lines.push('');

    blocks.forEach((block) => {
        const subTypePart = block.subType ? ` subType=${block.subType}` : '';
        const parentPart = block.parentId ? ` parent=${block.parentId}` : '';
        lines.push(`<!-- @siyuan:block id=${block.id} type=${block.type}${subTypePart}${parentPart} -->`);
        lines.push(block.markdown);
        lines.push('');
    });

    return lines.join('\n').trim();
}

function normalizeBlockMarkdown(markdown) {
    return String(markdown || '')
        .replace(/\r\n/g, '\n')
        .replace(/\r/g, '\n')
        .replace(/^\n+/, '')
        .replace(/\n+$/, '');
}

function parsePmfAttributes(raw) {
    const attrs = {};
    const text = String(raw || '');
    const regex = /([a-zA-Z_][\w-]*)=("(?:\\.|[^"])*"|'(?:\\.|[^'])*'|[^\s]+)/g;
    let match;

    while ((match = regex.exec(text)) !== null) {
        const key = match[1];
        let value = match[2];

        if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
            const quote = value[0];
            value = value.slice(1, -1);
            if (quote === '"') {
                try {
                    value = JSON.parse(`"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`);
                } catch (_) {
                    // fallback: keep raw unescaped content
                }
            }
        }

        attrs[key] = value;
    }

    return attrs;
}

function parsePatchableMarkdown(patchableMarkdown) {
    const text = String(patchableMarkdown || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    const lines = text.split('\n');

    const result = {
        doc: {},
        blocks: []
    };

    let currentBlock = null;
    let buffer = [];
    let fenceState = { active: false, char: '', size: 0 };

    const flushBlock = () => {
        if (!currentBlock) {
            return;
        }

        const markdown = normalizeBlockMarkdown(buffer.join('\n'));
        result.blocks.push({
            id: currentBlock.id,
            type: currentBlock.type || inferBlockType(markdown).type,
            subType: currentBlock.subType || '',
            parentId: currentBlock.parentId || '',
            markdown
        });

        currentBlock = null;
        buffer = [];
        fenceState = { active: false, char: '', size: 0 };
    };

    for (const line of lines) {
        if (!currentBlock) {
            const docMatch = line.match(/^<!--\s*@siyuan:doc\s+(.+?)\s*-->$/);
            if (docMatch && result.blocks.length === 0) {
                result.doc = parsePmfAttributes(docMatch[1]);
                continue;
            }

            const blockMatch = line.match(/^<!--\s*@siyuan:block\s+(.+?)\s*-->$/);
            if (blockMatch) {
                const attrs = parsePmfAttributes(blockMatch[1]);
                if (!attrs.id) {
                    throw new Error('PMF 格式错误: block marker 缺少 id');
                }

                currentBlock = {
                    id: String(attrs.id),
                    type: attrs.type ? String(attrs.type) : '',
                    subType: attrs.subType ? String(attrs.subType) : '',
                    parentId: attrs.parent ? String(attrs.parent) : (attrs.parentID ? String(attrs.parentID) : '')
                };
                continue;
            }

            continue;
        }

        if (!fenceState.active) {
            const blockMatch = line.match(/^<!--\s*@siyuan:block\s+(.+?)\s*-->$/);
            if (blockMatch) {
                flushBlock();
                const attrs = parsePmfAttributes(blockMatch[1]);
                if (!attrs.id) {
                    throw new Error('PMF 格式错误: block marker 缺少 id');
                }

                currentBlock = {
                    id: String(attrs.id),
                    type: attrs.type ? String(attrs.type) : '',
                    subType: attrs.subType ? String(attrs.subType) : '',
                    parentId: attrs.parent ? String(attrs.parent) : (attrs.parentID ? String(attrs.parentID) : '')
                };
                continue;
            }
        }

        buffer.push(line);
        updateFenceState(fenceState, line);
    }

    flushBlock();

    if (!result.doc.id && result.blocks.length === 0) {
        throw new Error('PMF 解析失败: 未找到 @siyuan:doc 或 @siyuan:block 标记');
    }

    return result;
}

function isSameStringArray(a, b) {
    if (a.length !== b.length) {
        return false;
    }

    for (let i = 0; i < a.length; i += 1) {
        if (a[i] !== b[i]) {
            return false;
        }
    }

    return true;
}

module.exports = {
    normalizeMarkdown,
    stripKramdownIAL,
    parseBlocksFromKramdown,
    renderPatchableMarkdown,
    normalizeBlockMarkdown,
    parsePatchableMarkdown,
    isSameStringArray
};
