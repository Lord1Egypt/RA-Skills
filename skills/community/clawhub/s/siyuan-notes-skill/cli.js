const CLI_USAGE_TEXT = `
思源笔记查询工具使用说明 (基于思源SQL规范):

用法:
  node index.js <命令> [参数]

命令:
  search <关键词> [数量] [类型] - 搜索包含关键词的笔记 (类型: p段落, h标题, l列表等)
  search-md <关键词> [数量] [类型] - 搜索并输出Markdown结果页
  open-doc <文档ID> [视图] [--cursor <块ID>] [--limit-chars <N>] [--limit-blocks <N>] [--full]
                           - 打开文档Markdown视图 (视图: readable|patchable, --full 跳过截断/分页)
  open-section <标题块ID> [视图]
                           - 读取标题下的章节内容 (视图: readable|patchable)
  search-in-doc <文档ID> <关键词> [数量]
                           - 在指定文档内搜索关键词
  notebooks                - 列出可用笔记本
  doc-children <笔记本ID> [路径]
                           - 列出指定路径下的子文档
  doc-tree <笔记本ID> [路径] [深度]
                           - 以Markdown树展示子文档组织关系
  doc-tree-id <文档ID> [深度]
                           - 以Markdown树展示指定文档下的子文档组织关系
  subdoc-analyze-move <目标ID> <来源ID列表> [深度]
                           - 分析复杂子文档重组计划（不执行）
  move-docs-by-id <目标ID> <来源ID列表>
                           - 重新组织子文档，来源ID可逗号或空格分隔
  append-block <父块ID>
                             - 向父块追加内容（Markdown 仅支持 stdin）
  insert-block <--before 块ID|--after 块ID|--parent 块ID>
                             - 在指定锚点插入内容（前/后/父块下，Markdown 仅支持 stdin）
  replace-section <标题块ID>
                             - 替换标题下全部子块（Markdown 仅支持 stdin）
  replace-section <标题块ID> --clear
                           - 清空标题下全部子块
  apply-patch <文档ID>      - 从 stdin 读取 PMF 并应用补丁
  update-block <块ID>
                            - 更新单个块内容（Markdown 仅支持 stdin）
  delete-block <块ID>       - 删除单个块
  docs [笔记本ID] [数量]     - 列出所有文档或指定笔记本的文档
  headings <文档ID> [级别]   - 查询文档标题 (级别: h1, h2等)
  blocks <文档ID> [类型]     - 查询文档子块
  tag <标签名>              - 搜索包含标签的笔记
  backlinks <块ID>          - 查询块的反向链接
  tasks [状态] [天数]        - 查询任务列表 (状态: "[ ]"未完成, "[x]"已完成, "[-]"进行中)
  daily <开始日期> <结束日期> - 查询Daily Note (日期格式: YYYYMMDD)
  attr <属性名> [属性值]     - 查询包含属性的块
  bookmarks [书签名]         - 查询书签
  random <文档ID>           - 随机漫游文档标题
  recent [天数] [类型]       - 查询最近修改的块
  unreferenced <笔记本ID>    - 查询未被引用的文档
  create-doc <笔记本ID> <标题>
                            - 创建新文档（初始 Markdown 仅支持 stdin，可省略）
  rename-doc <文档ID> <新标题>
                           - 重命名文档
  check                    - 检查连接状态
  version                  - 获取思源内核版本
  version-check            - 检查 skill 版本是否最新

示例:
  node index.js search "人工智能" 10 p
  node index.js search-md "人工智能" 10
  node index.js open-doc "20211231120000-d0rzbmm" readable
  node index.js doc-children "20210817205410-2kvfpfn" "/"
  node index.js doc-tree "20210817205410-2kvfpfn" "/" 4
  node index.js doc-tree-id "20211231120000-d0rzbmm" 5
  node index.js subdoc-analyze-move "20211231120000-d0rzbmm" "20211231121000-aaa111,20211231122000-bbb222" 6
  SIYUAN_ENABLE_WRITE=true node index.js move-docs-by-id "20211231120000-d0rzbmm" "20211231121000-aaa111,20211231122000-bbb222"
  SIYUAN_ENABLE_WRITE=true node index.js apply-patch "20211231120000-d0rzbmm" < /tmp/doc.pmf
  SIYUAN_ENABLE_WRITE=true node index.js append-block "20211231120000-d0rzbmm" <<'EOF'
- [ ] 新任务
EOF
  SIYUAN_ENABLE_WRITE=true node index.js insert-block --before "20211231120001-h1abcde" <<'EOF'
## 新增导读
EOF
  SIYUAN_ENABLE_WRITE=true node index.js insert-block --after "20211231120001-h1abcde" <<'EOF'
插入到该块后
EOF
  SIYUAN_ENABLE_WRITE=true node index.js replace-section "20211231120001-h1abcde" <<'EOF'
- 更新内容
EOF
  node index.js docs
  node index.js docs 100
  node index.js headings "20211231120000-d0rzbmm" h2
  node index.js tasks "[ ]" 7
  node index.js daily 20231010 20231013
  node index.js attr "custom-priority" "high"
  SIYUAN_ENABLE_WRITE=true node index.js create-doc "20210817205410-2kvfpfn" "我的新文档" <<'EOF'
初始内容
EOF
  SIYUAN_ENABLE_WRITE=true node index.js rename-doc "20211231120000-d0rzbmm" "新标题"
  node index.js version-check

写入提示:
  默认只读。若要写入，请在环境变量中设置 SIYUAN_ENABLE_WRITE=true。
`;

function printCliUsage() {
    console.log(CLI_USAGE_TEXT);
}

function cliError(message) {
    console.error(message);
    process.exitCode = 1;
}

function cliRequireArg(args, index, message) {
    if (!args[index]) {
        cliError(message);
        return '';
    }

    return args[index];
}

async function cliPrintFormattedResults(loader, formatResults) {
    const results = await loader();
    console.log(formatResults(results));
}

async function readRequiredMarkdownFromStdin(readStdinText, commandName) {
    const markdown = String(await readStdinText() || '');
    if (!markdown.trim()) {
        cliError(`${commandName} 仅支持通过 stdin 提供 Markdown 内容（例如 <<'EOF' ... EOF）`);
        return '';
    }
    return markdown;
}

function createCliHandlers(deps) {
    const {
        parseIdList,
        readStdinText,
        normalizeInt,
        hasClearFlag,
        stripCommandFlags,
        formatResults,
        searchNotes,
        searchInDocument,
        searchNotesMarkdown,
        openDocument,
        openSection,
        listNotebooks,
        getDocumentChildren,
        getDocumentTree,
        renderDocumentTreeMarkdown,
        getDocumentTreeByID,
        analyzeSubdocMovePlan,
        reorganizeSubdocsByID,
        appendMarkdownToBlock,
        insertBlock,
        replaceSection,
        applyPatchToDocument,
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
        getUnreferencedDocuments,
        checkConnection,
        getSystemVersion,
        checkSkillVersion,
        createDocWithMd,
        renameDoc,
        getPathByID,
        updateBlock,
        deleteBlock
    } = deps;

    return {
        search: async (args) => {
            const keyword = cliRequireArg(args, 1, '请提供搜索关键词');
            if (!keyword) {
                return;
            }
            let limit = 20;
            let blockType = null;

            if (args[2]) {
                if (/^\d+$/.test(args[2])) {
                    limit = normalizeInt(args[2], 20, 1, 200);
                    blockType = args[3] || null;
                } else {
                    blockType = args[2] || null;
                }
            }

            const searchResults = await searchNotes(keyword, limit, blockType);
            console.log(formatResults(searchResults));
        },

        'search-md': async (args) => {
            const keyword = cliRequireArg(args, 1, '请提供搜索关键词');
            if (!keyword) {
                return;
            }
            const limit = normalizeInt(args[2], 20, 1, 200);
            const blockType = args[3] || null;
            const markdownView = await searchNotesMarkdown(keyword, limit, blockType);
            console.log(markdownView);
        },

        'open-doc': async (args) => {
            const raw = args.slice(1);
            // Extract --flag value pairs
            const options = {};
            const positional = [];
            for (let i = 0; i < raw.length; i++) {
                if (raw[i] === '--cursor' && i + 1 < raw.length) {
                    options.cursor = raw[++i];
                } else if (raw[i] === '--limit-chars' && i + 1 < raw.length) {
                    options.limitChars = normalizeInt(raw[++i], 15000, 1000, 1000000);
                } else if (raw[i] === '--limit-blocks' && i + 1 < raw.length) {
                    options.limitBlocks = normalizeInt(raw[++i], 50, 5, 10000);
                } else if (raw[i] === '--full') {
                    options.full = true;
                } else {
                    positional.push(raw[i]);
                }
            }
            const docId = positional[0];
            if (!docId) {
                cliError('请提供文档ID');
                return;
            }
            const view = (positional[1] || 'readable').toLowerCase();
            if (view !== 'readable' && view !== 'patchable') {
                cliError('视图参数仅支持 readable 或 patchable');
                return;
            }

            const markdownView = await openDocument(docId, view, options);
            console.log(markdownView);
        },

        'open-section': async (args) => {
            const headingBlockId = cliRequireArg(args, 1, '请提供标题块ID');
            if (!headingBlockId) return;
            const view = (args[2] || 'readable').toLowerCase();
            if (view !== 'readable' && view !== 'patchable') {
                cliError('视图参数仅支持 readable 或 patchable');
                return;
            }
            const result = await openSection(headingBlockId, view);
            console.log(result);
        },

        'search-in-doc': async (args) => {
            const docId = cliRequireArg(args, 1, '请提供文档ID');
            if (!docId) return;
            const keyword = cliRequireArg(args, 2, '请提供搜索关键词');
            if (!keyword) return;
            const limit = normalizeInt(args[3], 20, 1, 200);
            const results = await searchInDocument(docId, keyword, limit);
            console.log(formatResults(results));
        },

        notebooks: async () => {
            const notebooks = await listNotebooks();
            if (!notebooks.length) {
                console.log('未获取到笔记本列表');
                return;
            }

            notebooks.forEach((item, index) => {
                const id = item.id || item.notebook || '';
                const name = item.name || item.notebook || '(未命名)';
                const closed = item.closed ? ' (closed)' : '';
                console.log(`${index + 1}. ${name}${closed} [${id}]`);
            });
        },

        'doc-children': async (args) => {
            const notebook = cliRequireArg(args, 1, '请提供笔记本ID');
            if (!notebook) {
                return;
            }
            const pathValue = args[2] || '/';
            const children = await getDocumentChildren(notebook, pathValue);

            if (!children.length) {
                console.log('该路径下没有子文档');
                return;
            }

            children.forEach((item, index) => {
                console.log(`${index + 1}. ${item.name || '(未命名文档)'} [${item.id}] (${item.path}) sub=${item.subFileCount}`);
            });
        },

        'doc-tree': async (args) => {
            const notebook = cliRequireArg(args, 1, '请提供笔记本ID');
            if (!notebook) {
                return;
            }
            const pathValue = args[2] || '/';
            const maxDepth = normalizeInt(args[3], 4, 1, 10);
            const tree = await getDocumentTree(notebook, pathValue, maxDepth);
            console.log(renderDocumentTreeMarkdown(tree));
        },

        'doc-tree-id': async (args) => {
            const docId = cliRequireArg(args, 1, '请提供文档ID');
            if (!docId) {
                return;
            }
            const maxDepth = normalizeInt(args[2], 4, 1, 10);
            const tree = await getDocumentTreeByID(docId, maxDepth);
            console.log(renderDocumentTreeMarkdown(tree));
        },

        'subdoc-analyze-move': async (args) => {
            const toID = cliRequireArg(args, 1, '请提供目标ID和来源文档ID列表');
            const fromRaw = cliRequireArg(args, 2, '请提供目标ID和来源文档ID列表');
            if (!toID || !fromRaw) {
                return;
            }
            const maxDepth = normalizeInt(args[3], 5, 1, 10);
            const fromIDs = parseIdList(fromRaw);

            const result = await analyzeSubdocMovePlan(toID, fromIDs, maxDepth);
            console.log(JSON.stringify(result, null, 2));
        },

        'move-docs-by-id': async (args) => {
            const positional = args.slice(1);
            const toID = positional[0];
            const fromRaw = positional.slice(1).join(' ').trim();

            if (!toID) {
                cliError('请提供目标ID（父文档ID或笔记本ID）');
                return;
            }

            if (!fromRaw) {
                cliError('请提供来源文档ID列表（逗号或空格分隔）');
                return;
            }

            const fromIDs = parseIdList(fromRaw);

            const result = await reorganizeSubdocsByID(toID, fromIDs);
            console.log(JSON.stringify(result, null, 2));
        },

        'append-block': async (args) => {
            const positional = args.slice(1);
            const parentBlockId = positional[0];

            if (!parentBlockId) {
                cliError('请提供父块ID');
                return;
            }

            if (positional.length > 1) {
                cliError('append-block 仅支持通过 stdin 传入 Markdown 内容');
                return;
            }

            const markdown = await readRequiredMarkdownFromStdin(readStdinText, 'append-block');
            if (!markdown) return;

            const result = await appendMarkdownToBlock(parentBlockId, markdown);
            console.log(JSON.stringify(result, null, 2));
        },

        'insert-block': async (args) => {
            const raw = args.slice(1);
            const anchors = {
                parentID: '',
                previousID: '',
                nextID: ''
            };
            const positional = [];

            for (let i = 0; i < raw.length; i++) {
                const token = raw[i];
                if (token === '--before' || token === '--after' || token === '--parent') {
                    if (i + 1 >= raw.length) {
                        cliError(`${token} 需要提供块ID`);
                        return;
                    }
                    const anchorId = String(raw[++i] || '').trim();
                    if (!anchorId) {
                        cliError(`${token} 需要提供块ID`);
                        return;
                    }
                    if (token === '--before') {
                        anchors.nextID = anchorId;
                    } else if (token === '--after') {
                        anchors.previousID = anchorId;
                    } else {
                        anchors.parentID = anchorId;
                    }
                } else {
                    positional.push(token);
                }
            }

            const anchorCount = [anchors.parentID, anchors.previousID, anchors.nextID].filter(Boolean).length;
            if (anchorCount !== 1) {
                cliError('请且仅提供一个锚点：--before <块ID> 或 --after <块ID> 或 --parent <块ID>');
                return;
            }

            if (positional.length > 0) {
                cliError('insert-block 仅支持通过 stdin 传入 Markdown 内容');
                return;
            }

            const markdown = await readRequiredMarkdownFromStdin(readStdinText, 'insert-block');
            if (!markdown) return;

            const result = await insertBlock(markdown, anchors);
            console.log(JSON.stringify(result, null, 2));
        },

        'replace-section': async (args) => {
            const raw = args.slice(1);
            const clearMode = hasClearFlag(raw);
            const positional = stripCommandFlags(raw);
            const headingBlockId = positional[0];

            if (!headingBlockId) {
                cliError('请提供标题块ID');
                return;
            }

            if (positional.length > 1) {
                cliError('replace-section 仅支持通过 stdin 传入 Markdown 内容');
                return;
            }

            let markdown = '';
            if (!clearMode) {
                markdown = await readRequiredMarkdownFromStdin(readStdinText, 'replace-section');
                if (!markdown) return;
            }

            const result = await replaceSection(headingBlockId, markdown);
            console.log(JSON.stringify(result, null, 2));
        },

        'apply-patch': async (args) => {
            const positional = args.slice(1);
            const docId = positional[0];

            if (!docId) {
                cliError('请提供文档ID');
                return;
            }

            if (positional.length > 1) {
                cliError('apply-patch 仅支持通过 stdin 提供 PMF 文本');
                return;
            }

            const patchText = String(await readStdinText() || '').trim();
            if (!patchText) {
                cliError('apply-patch 仅支持通过 stdin 提供 PMF 文本（例如 < /tmp/doc.pmf）');
                return;
            }

            const result = await applyPatchToDocument(docId, patchText);
            console.log(JSON.stringify(result, null, 2));
        },

        docs: async (args) => {
            const maybeNotebook = args[1] || '';
            const hasNotebookArg = maybeNotebook && !/^\d+$/.test(maybeNotebook);
            const notebookId = hasNotebookArg ? maybeNotebook : null;
            const limitArg = hasNotebookArg ? args[2] : args[1];
            const limit = typeof limitArg === 'string' && limitArg.trim()
                ? normalizeInt(limitArg, 200, 1, 2000)
                : undefined;
            await cliPrintFormattedResults(() => listDocuments(notebookId, limit), formatResults);
        },

        headings: async (args) => {
            const rootId = cliRequireArg(args, 1, '请提供文档ID');
            if (!rootId) {
                return;
            }
            const headingType = args[2] || null;
            await cliPrintFormattedResults(() => getDocumentHeadings(rootId, headingType), formatResults);
        },

        blocks: async (args) => {
            const docRootId = cliRequireArg(args, 1, '请提供文档ID');
            if (!docRootId) {
                return;
            }
            const blocksType = args[2] || null;
            await cliPrintFormattedResults(() => getDocumentBlocks(docRootId, blocksType), formatResults);
        },

        tag: async (args) => {
            const tag = cliRequireArg(args, 1, '请提供标签名');
            if (!tag) {
                return;
            }
            await cliPrintFormattedResults(() => searchByTag(tag), formatResults);
        },

        backlinks: async (args) => {
            const blockId = cliRequireArg(args, 1, '请提供被引用的块ID');
            if (!blockId) {
                return;
            }
            await cliPrintFormattedResults(() => getBacklinks(blockId), formatResults);
        },

        tasks: async (args) => {
            let taskStatus = '[ ]';
            let dayArg = args[2];
            if (args[1]) {
                // 兼容未加引号的 [ ]（shell 会拆成两个参数）
                if (args[1] === '[' && args[2] === ']') {
                    taskStatus = '[ ]';
                    dayArg = args[3];
                } else {
                    taskStatus = args[1];
                }
            }
            const taskDays = normalizeInt(dayArg, 7, 1, 3650);
            await cliPrintFormattedResults(() => searchTasks(taskStatus, taskDays), formatResults);
        },

        daily: async (args) => {
            const startDate = cliRequireArg(args, 1, '请提供开始日期和结束日期 (格式: YYYYMMDD)');
            if (!startDate) {
                return;
            }
            const endDate = cliRequireArg(args, 2, '请提供开始日期和结束日期 (格式: YYYYMMDD)');
            if (!endDate) {
                return;
            }
            await cliPrintFormattedResults(() => getDailyNotes(startDate, endDate), formatResults);
        },

        attr: async (args) => {
            const attrName = cliRequireArg(args, 1, '请提供属性名称');
            if (!attrName) {
                return;
            }
            const attrValue = args[2] || null;
            await cliPrintFormattedResults(() => searchByAttribute(attrName, attrValue), formatResults);
        },

        bookmarks: async (args) => {
            const bookmarkName = args[1] || null;
            await cliPrintFormattedResults(() => getBookmarks(bookmarkName), formatResults);
        },

        random: async (args) => {
            const docId = cliRequireArg(args, 1, '请提供文档ID');
            if (!docId) {
                return;
            }
            await cliPrintFormattedResults(() => getRandomHeading(docId), formatResults);
        },

        recent: async (args) => {
            const recentDays = parseInt(args[1]) || 7;
            const recentType = args[2] || null;
            await cliPrintFormattedResults(() => getRecentBlocks(recentDays, 'updated', recentType), formatResults);
        },

        unreferenced: async (args) => {
            const notebookId = cliRequireArg(args, 1, '请提供笔记本ID');
            if (!notebookId) {
                return;
            }
            await cliPrintFormattedResults(() => getUnreferencedDocuments(notebookId), formatResults);
        },

        'create-doc': async (args) => {
            const positional = args.slice(1);
            const notebook = positional[0];
            const title = positional[1];
            let markdown = '';

            if (!notebook) {
                cliError('请提供笔记本ID');
                return;
            }

            if (!title) {
                cliError('请提供文档标题');
                return;
            }

            if (positional.length > 2) {
                cliError('create-doc 的初始内容仅支持通过 stdin 传入 Markdown；不传 stdin 则创建空文档');
                return;
            }

            if (!process.stdin.isTTY) {
                markdown = String(await readStdinText() || '').trim();
            }

            const result = await createDocWithMd(notebook, `/${title}`, markdown);
            console.log(JSON.stringify({ success: true, docId: result, title }, null, 2));
        },

        'rename-doc': async (args) => {
            const positional = args.slice(1);
            const docId = positional[0];
            const newTitle = positional.slice(1).join(' ').trim();

            if (!docId) {
                cliError('请提供文档ID');
                return;
            }

            if (!newTitle) {
                cliError('请提供新标题');
                return;
            }

            const pathInfo = await getPathByID(docId);
            if (!pathInfo || !pathInfo.notebook || !pathInfo.path) {
                cliError(`无法获取文档路径信息: ${docId}`);
                return;
            }

            await renameDoc(pathInfo.notebook, pathInfo.path, newTitle);
            console.log(JSON.stringify({ success: true, docId, newTitle }, null, 2));
        },

        'update-block': async (args) => {
            const positional = args.slice(1);
            const blockId = positional[0];

            if (!blockId) {
                cliError('请提供块ID');
                return;
            }

            if (positional.length > 1) {
                cliError('update-block 仅支持通过 stdin 传入 Markdown 内容');
                return;
            }

            const markdown = await readRequiredMarkdownFromStdin(readStdinText, 'update-block');
            if (!markdown) return;

            const result = await updateBlock(blockId, markdown);
            console.log(JSON.stringify(result, null, 2));
        },

        'delete-block': async (args) => {
            const blockId = cliRequireArg(args, 1, '请提供要删除的块ID');
            if (!blockId) return;
            const result = await deleteBlock(blockId);
            console.log(JSON.stringify(result, null, 2));
        },

        check: async () => {
            const isConnected = await checkConnection();
            console.log(isConnected ? '✅ 思源笔记连接正常' : '❌ 思源笔记连接失败');
            if (!isConnected) {
                process.exitCode = 1;
            }
        },

        version: async () => {
            const version = await getSystemVersion();
            console.log(version ? `思源内核版本: ${version}` : '未获取到版本号');
        },

        'version-check': async () => {
            const result = await checkSkillVersion();
            const localInfo = `local: ${result.localVersion}, commit: ${result.localSha}`;
            if (result.status === 'latest') {
                console.log(`✅ 当前 skill 版本已是最新（${localInfo}, latest: ${result.latestVersion || 'unknown'}）。`);
                return;
            }
            if (result.status === 'outdated') {
                console.log(`⚠️ 当前 skill 版本不是最新（local: ${result.localVersion}, latest: ${result.latestVersion}, commit: ${result.localSha}）。`);
                console.log('建议尽快更新到最新版本以获得最佳体验。');
                return;
            }
            console.log(`⚠️ 无法获取远程版本，已跳过检查（${localInfo}）。`);
        }
    };
}

module.exports = {
    createCliHandlers,
    printCliUsage
};
