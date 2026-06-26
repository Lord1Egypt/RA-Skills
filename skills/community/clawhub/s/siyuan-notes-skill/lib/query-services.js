function createQueryServices(deps) {
    const {
        executeSiyuanQuery,
        escapeSqlValue,
        normalizeInt,
        assertNonEmptyString,
        strftime,
        listDocumentsLimit
    } = deps;

    async function searchNotes(keyword, limit = 20, blockType = null) {
        assertNonEmptyString(keyword, 'keyword');
        const safeKeyword = escapeSqlValue(keyword);
        const safeLimit = normalizeInt(limit, 20, 1, 200);
        let sql = `
        SELECT id, content, type, subtype, created, updated, root_id, parent_id, box, path, hpath
        FROM blocks
        WHERE (
            instr(markdown, '${safeKeyword}') > 0
            OR instr(content, '${safeKeyword}') > 0
        )
    `;

        if (blockType) {
            const safeBlockType = escapeSqlValue(blockType);
            sql += ` AND type = '${safeBlockType}'`;
        }

        sql += `
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function searchInDocument(docId, keyword, limit = 20) {
        assertNonEmptyString(docId, 'docId');
        assertNonEmptyString(keyword, 'keyword');
        const safeDocId = escapeSqlValue(docId);
        const safeKeyword = escapeSqlValue(keyword);
        const safeLimit = normalizeInt(limit, 20, 1, 200);
        const sql = `
        SELECT id, content, type, subtype, created, updated, parent_id
        FROM blocks
        WHERE root_id = '${safeDocId}'
        AND (
            instr(markdown, '${safeKeyword}') > 0
            OR instr(content, '${safeKeyword}') > 0
        )
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;
        return await executeSiyuanQuery(sql);
    }

    async function listDocuments(notebookId = null, limit = listDocumentsLimit) {
        const safeLimit = normalizeInt(limit, listDocumentsLimit, 1, 2000);
        let sql = `
        SELECT id, content, created, updated, box, path, hpath
        FROM blocks
        WHERE type = 'd'
    `;

        if (notebookId) {
            sql += ` AND box = '${escapeSqlValue(notebookId)}'`;
        }

        sql += ` ORDER BY updated DESC LIMIT ${safeLimit}`;

        return await executeSiyuanQuery(sql);
    }

    async function getDocumentHeadings(rootId, headingType = null) {
        const safeRootId = escapeSqlValue(rootId);
        let sql = `
        SELECT id, content, subtype, created, updated, parent_id
        FROM blocks
        WHERE root_id = '${safeRootId}'
        AND type = 'h'
    `;

        if (headingType) {
            sql += ` AND subtype = '${escapeSqlValue(headingType)}'`;
        }

        sql += ' ORDER BY created ASC';

        return await executeSiyuanQuery(sql);
    }

    async function getDocumentBlocks(rootId, blockType = null) {
        const safeRootId = escapeSqlValue(rootId);
        let sql = `
        SELECT id, content, markdown, type, subtype, created, updated, parent_id, ial
        FROM blocks
        WHERE root_id = '${safeRootId}'
    `;

        if (blockType) {
            sql += ` AND type = '${escapeSqlValue(blockType)}'`;
        }

        sql += ' ORDER BY created ASC';

        return await executeSiyuanQuery(sql);
    }

    async function searchByTag(tag, limit = 20) {
        const normalizedTag = String(tag || '').trim().replace(/^#+|#+$/g, '');
        assertNonEmptyString(normalizedTag, 'tag');
        const safeTag = escapeSqlValue(normalizedTag);
        const safeLimit = normalizeInt(limit, 20, 1, 200);
        const sql = `
        SELECT id, content, type, subtype, created, updated, root_id, parent_id
        FROM blocks
        WHERE (
            instr(tag, '#${safeTag}#') > 0
            OR instr(markdown, '#${safeTag}#') > 0
        )
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function getBacklinks(defBlockId, limit = 999) {
        const safeDefBlockId = escapeSqlValue(defBlockId);
        const safeLimit = normalizeInt(limit, 999, 1, 2000);
        const sql = `
        SELECT * FROM blocks
        WHERE id IN (
            SELECT block_id FROM refs WHERE def_block_id = '${safeDefBlockId}'
        )
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function searchTasks(status = '[ ]', days = 7, limit = 50) {
        const normalizedStatus = String(status || '[ ]').trim().toLowerCase();
        let statusCondition = '';
        if (normalizedStatus === '[ ]') {
            statusCondition = `instr(markdown, '[ ]') > 0`;
        } else if (normalizedStatus === '[x]') {
            statusCondition = `instr(lower(markdown), '[x]') > 0`;
        } else if (normalizedStatus === '[-]') {
            statusCondition = `instr(markdown, '[-]') > 0`;
        } else {
            throw new Error(`不支持的任务状态: ${status}，仅支持 [ ]、[x]、[-]`);
        }

        const safeDays = normalizeInt(days, 7, 1, 3650);
        const safeLimit = normalizeInt(limit, 50, 1, 500);
        const sql = `
        SELECT * FROM blocks
        WHERE type IN ('l', 'i') AND subtype = 't'
        AND created > strftime('%Y%m%d%H%M%S', datetime('now', '-${safeDays} day'))
        AND (${statusCondition})
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function getDailyNotes(startDate, endDate) {
        const safeStartDate = escapeSqlValue(startDate);
        const safeEndDate = escapeSqlValue(endDate);
        const sql = `
        SELECT DISTINCT B.* FROM blocks AS B
        JOIN attributes AS A ON B.id = A.block_id
        WHERE A.name LIKE 'custom-dailynote-%'
        AND B.type = 'd'
        AND A.value >= '${safeStartDate}'
        AND A.value <= '${safeEndDate}'
        ORDER BY A.value DESC
    `;

        return await executeSiyuanQuery(sql);
    }

    async function searchByAttribute(attrName, attrValue = null, limit = 20) {
        const safeAttrName = escapeSqlValue(attrName);
        const safeLimit = normalizeInt(limit, 20, 1, 500);
        let sql = `
        SELECT * FROM blocks
        WHERE id IN (
            SELECT block_id FROM attributes
            WHERE name = '${safeAttrName}'
    `;

        if (attrValue) {
            sql += ` AND value = '${escapeSqlValue(attrValue)}'`;
        }

        sql += `
        )
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function getBookmarks(bookmarkName = null) {
        let sql = `
        SELECT * FROM blocks
        WHERE id IN (
            SELECT block_id FROM attributes
            WHERE name = 'bookmark'
    `;

        if (bookmarkName) {
            sql += ` AND value = '${escapeSqlValue(bookmarkName)}'`;
        }

        sql += ') ORDER BY updated DESC';

        return await executeSiyuanQuery(sql);
    }

    async function getRandomHeading(rootId) {
        const safeRootId = escapeSqlValue(rootId);
        const sql = `
        SELECT * FROM blocks
        WHERE root_id = '${safeRootId}' AND type = 'h'
        ORDER BY random() LIMIT 1
    `;

        return await executeSiyuanQuery(sql);
    }

    async function getRecentBlocks(days = 7, orderBy = 'updated', blockType = null, limit = 50) {
        const safeDays = normalizeInt(days, 7, 1, 3650);
        const safeLimit = normalizeInt(limit, 50, 1, 500);
        const safeOrderBy = orderBy === 'created' ? 'created' : 'updated';
        const dateThreshold = strftime('%Y%m%d%H%M%S', Date.now() - (safeDays * 24 * 60 * 60 * 1000));

        let sql = `
        SELECT id, content, type, subtype, created, updated, root_id, box, hpath
        FROM blocks
        WHERE ${safeOrderBy} > '${dateThreshold}'
    `;

        if (blockType) {
            sql += ` AND type = '${escapeSqlValue(blockType)}'`;
        }

        sql += `
        ORDER BY ${safeOrderBy} DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    async function getUnreferencedDocuments(notebookId, limit = 128) {
        const safeNotebookId = escapeSqlValue(notebookId);
        const safeLimit = normalizeInt(limit, 128, 1, 1000);
        const sql = `
        SELECT * FROM blocks AS B
        WHERE B.type = 'd'
        AND box = '${safeNotebookId}'
        AND B.id NOT IN (
            SELECT DISTINCT R.def_block_id FROM refs AS R
        )
        ORDER BY updated DESC
        LIMIT ${safeLimit}
    `;

        return await executeSiyuanQuery(sql);
    }

    return {
        searchNotes,
        searchInDocument,
        listDocuments,
        getDocumentHeadings,
        getDocumentBlocks,
        searchByTag,
        getBacklinks,
        searchTasks,
        getDailyNotes,
        searchByAttribute,
        getBookmarks,
        getRandomHeading,
        getRecentBlocks,
        getUnreferencedDocuments
    };
}

module.exports = {
    createQueryServices
};
