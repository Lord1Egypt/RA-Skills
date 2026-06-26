// 全局状态
            const state = {
                currentFile: null,
                currentFileData: null, // 当前文件的数据（从API获取）
                activeTab: 'source', // 当前激活的Tab: 'source' 或 'explanation'
                explanationData: null, // 解释数据
                isGeneratingExplanation: false, // 是否正在生成解释
                hasExplanation: false, // 是否有解释数据
                isManualInputMode: false, // 是否处于手动输入模式
                manualInputText: '', // 手动输入的文本
                treeData: null,
                expandedItems: new Set()
            };
            
            // DOM加载完成后初始化
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Workspace浏览器3.0 - 阶段1');
                
                // 绑定树容器点击事件（事件委托）
                document.getElementById('tree-container').addEventListener('click', function(e) {
                    const treeItem = e.target.closest('.tree-item');
                    if (treeItem) {
                        try {
                            const itemData = JSON.parse(decodeURIComponent(treeItem.dataset.itemData));
                            selectTreeItem(itemData, treeItem);
                        } catch (error) {
                            console.error('解析itemData失败:', error, '原始数据:', treeItem.dataset.itemData);
                        }
                    }
                });
                
                loadFileTree();
                
                // 绑定按钮事件
                document.getElementById('refresh-btn').addEventListener('click', function() {
                    loadFileTree();
                });
                
                document.getElementById('download-btn').addEventListener('click', function() {
                    if (state.currentFile) {
                        window.open(`/api/download/${encodeURIComponent(state.currentFile.path)}`, '_blank');
                    }
                });
                
                // 复制成功对话框函数 - 使用浏览器自带alert
                function showCopySuccessDialog(message) {
                    console.log('显示复制提示:', message);
                    
                    // 使用简洁的alert实现
                    alert(message);
                }
                

                
                document.getElementById('copy-code-btn').addEventListener('click', function() {
                    // 简单检查
                    if (!state.currentFileData || !state.currentFileData.content) {
                        alert('请先选择要复制的文件');
                        return;
                    }
                    
                    const textToCopy = state.currentFileData.content;
                    
                    // 最简单的复制实现
                    try {
                        // 尝试使用现代 Clipboard API
                        if (navigator.clipboard && navigator.clipboard.writeText) {
                            navigator.clipboard.writeText(textToCopy)
                                .then(() => {
                                    alert('代码已复制到剪切板');
                                })
                                .catch(() => {
                                    // 如果现代API失败，使用传统方法
                                    copyWithExecCommand(textToCopy);
                                });
                        } else {
                            // 直接使用传统方法
                            copyWithExecCommand(textToCopy);
                        }
                    } catch (error) {
                        alert('复制失败，请手动复制代码');
                    }
                    
                    // 传统复制方法
                    function copyWithExecCommand(text) {
                        const textArea = document.createElement('textarea');
                        textArea.value = text;
                        textArea.style.position = 'fixed';
                        textArea.style.opacity = '0';
                        document.body.appendChild(textArea);
                        textArea.select();
                        
                        try {
                            const successful = document.execCommand('copy');
                            if (successful) {
                                alert('代码已复制到剪切板');
                            } else {
                                alert('复制失败，请手动复制代码');
                            }
                        } catch (err) {
                            alert('复制失败，请手动复制代码');
                        } finally {
                            document.body.removeChild(textArea);
                        }
                    }
                });
                
                // 搜索功能
                const searchInput = document.getElementById('file-search');
                const clearSearchBtn = document.getElementById('clear-search');
                
                // 搜索输入事件 - 按回车触发
                searchInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        const searchTerm = this.value.trim();
                        if (searchTerm) {
                            triggerSearch(searchTerm);
                        }
                    }
                });
                
                // 搜索按钮事件
                const searchButton = document.createElement('button');
                searchButton.className = 'search-button';
                searchButton.innerHTML = '';
                searchButton.title = '搜索';
                searchButton.addEventListener('click', function() {
                    const searchTerm = searchInput.value.trim();
                    if (searchTerm) {
                        triggerSearch(searchTerm);
                    }
                });
                
                // 将搜索按钮添加到搜索容器
                document.querySelector('.search-container').appendChild(searchButton);
                
                // 触发搜索函数
                function triggerSearch(searchTerm) {
                    // 显示搜索中状态
                    showSearchLoading(searchTerm);
                    
                    // 执行搜索
                    performSearch(searchTerm);
                }
                
                // 显示搜索中状态
                function showSearchLoading(searchTerm) {
                    // 创建或更新搜索加载覆盖层
                    let searchOverlay = document.getElementById('search-overlay');
                    if (!searchOverlay) {
                        searchOverlay = document.createElement('div');
                        searchOverlay.id = 'search-overlay';
                        searchOverlay.className = 'search-overlay';
                        document.querySelector('.main').appendChild(searchOverlay);
                    }
                    
                    searchOverlay.innerHTML = `
                        <div class="search-loading">
                            <div class="loading-spinner"></div>
                            <p>正在搜索 "${searchTerm}"...</p>
                        </div>
                    `;
                    searchOverlay.style.display = 'block';
                    
                    // 隐藏文件查看界面
                    const mainHeader = document.querySelector('.main-header');
                    const contentArea = document.querySelector('.content-area');
                    if (mainHeader) mainHeader.style.display = 'none';
                    if (contentArea) contentArea.style.display = 'none';
                }
                
                // 清除搜索按钮事件
                clearSearchBtn.addEventListener('click', function() {
                    searchInput.value = '';
                    clearSearchBtn.style.display = 'none';
                    clearSearch();
                    searchInput.focus();
                });
                
                // 搜索功能 - 增强版：支持递归搜索
                async function performSearch(searchTerm) {
                    try {
                        // 调用后端搜索API
                        const response = await fetch(`/api/search?q=${encodeURIComponent(searchTerm)}`);
                        
                        if (!response.ok) {
                            throw new Error(`搜索API错误: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        
                        // 渲染搜索结果
                        renderSearchResults(data.items, searchTerm, data);
                    } catch (error) {
                        console.error('搜索失败:', error);
                        const container = document.getElementById('tree-container');
                        container.innerHTML = `
                            <div style="padding: 20px; text-align: center; color: #718096;">
                                <p>搜索失败: ${error.message}</p>
                            </div>
                        `;
                    }
                }
                
                // 渲染搜索结果 - 在主工作区显示
                function renderSearchResults(matches, searchTerm, searchData) {
                    const mainContent = document.querySelector('.main');
                    
                    if (!matches || matches.length === 0) {
                        const html = `
                            <div class="search-results">
                                <div class="search-results-header">
                                    <div class="search-header-top">
                                        <h2>搜索结果</h2>
                                        <button class="back-to-tree-btn" id="back-to-default-btn">
                                            ← 返回
                                        </button>
                                    </div>
                                    <div class="search-query">搜索词: "${searchTerm}"</div>
                                </div>
                                <div class="no-results">
                                    <p>没有找到匹配 "${searchTerm}" 的文件或文件夹</p>
                                </div>
                            </div>
                        `;
                        
                        // 创建或更新搜索结果覆盖层
                        let searchOverlay = document.getElementById('search-overlay');
                        if (!searchOverlay) {
                            searchOverlay = document.createElement('div');
                            searchOverlay.id = 'search-overlay';
                            searchOverlay.className = 'search-overlay';
                            mainContent.appendChild(searchOverlay);
                        }
                        
                        searchOverlay.innerHTML = html;
                        searchOverlay.style.display = 'block';
                        
                        // 隐藏文件查看界面的所有部分
                        const mainHeader = document.querySelector('.main-header');
                        const tabBar = document.getElementById('tab-bar');
                        const contentArea = document.querySelector('.content-area');
                        
                        if (mainHeader) mainHeader.style.display = 'none';
                        if (tabBar) tabBar.style.display = 'none';
                        if (contentArea) contentArea.style.display = 'none';
                        
                        cacheSearchResults(html, searchTerm, searchData);
                        
                        // 绑定返回按钮事件
                        document.getElementById('back-to-default-btn')?.addEventListener('click', function() {
                            // 隐藏搜索结果，显示文件查看界面
                            searchOverlay.style.display = 'none';
                            if (mainHeader) mainHeader.style.display = 'block';
                            if (contentArea) contentArea.style.display = 'block';
                        });
                        
                        return;
                    }
                    
                    // 添加搜索统计
                    let statsText = `找到 ${matches.length} 个匹配 "${searchTerm}" 的结果`;
                    if (searchData && searchData.truncated) {
                        statsText += ' (结果过多，已截断)';
                    }
                    
                    let html = `
                        <div class="search-results">
                            <div class="search-results-header">
                                <div class="search-header-top">
                                    <h2>搜索结果</h2>
                                    <button class="back-to-tree-btn" id="back-to-default-btn">
                                        ← 返回
                                    </button>
                                </div>
                                <div class="search-query">搜索词: "${searchTerm}"</div>
                                <div class="search-stats">${statsText}</div>
                            </div>
                            <div class="search-results-list">
                    `;
                    
                    matches.forEach(item => {
                        html += renderSearchResultItem(item, searchTerm);
                    });
                    
                    html += `
                            </div>
                        </div>
                    `;
                    
                    // 创建或更新搜索结果覆盖层
                    let searchOverlay = document.getElementById('search-overlay');
                    if (!searchOverlay) {
                        searchOverlay = document.createElement('div');
                        searchOverlay.id = 'search-overlay';
                        searchOverlay.className = 'search-overlay';
                        mainContent.appendChild(searchOverlay);
                    }
                    
                    searchOverlay.innerHTML = html;
                    searchOverlay.style.display = 'block';
                    
                    // 隐藏文件查看界面
                    const mainHeader = document.querySelector('.main-header');
                    const contentArea = document.querySelector('.content-area');
                    if (mainHeader) mainHeader.style.display = 'none';
                    if (contentArea) contentArea.style.display = 'none';
                    
                    cacheSearchResults(html, searchTerm, searchData);
                    
                    // 绑定返回按钮事件
                    document.getElementById('back-to-default-btn')?.addEventListener('click', function() {
                        // 隐藏搜索结果，显示文件查看界面
                        searchOverlay.style.display = 'none';
                        if (mainHeader) mainHeader.style.display = 'block';
                        if (contentArea) contentArea.style.display = 'block';
                    });
                }
                
                // 渲染搜索结果项 - 在主工作区显示（优化布局）
                function renderSearchResultItem(item, searchTerm) {
                    // 高亮匹配的文本
                    const itemName = escapeHtml(item.name);
                    const lowerName = item.name.toLowerCase();
                    const lowerSearchTerm = searchTerm.toLowerCase();
                    
                    let highlightedName = itemName;
                    if (lowerSearchTerm && lowerName.includes(lowerSearchTerm)) {
                        const startIndex = lowerName.indexOf(lowerSearchTerm);
                        const endIndex = startIndex + searchTerm.length;
                        
                        highlightedName = 
                            itemName.substring(0, startIndex) +
                            `<span class="search-highlight">${itemName.substring(startIndex, endIndex)}</span>` +
                            itemName.substring(endIndex);
                    }
                    
                    // 获取目录路径（不包含文件名）
                    let dirPath = '';
                    if (item.parent) {
                        dirPath = escapeHtml(item.parent);
                        if (dirPath === '.') {
                            dirPath = ''; // 根目录不显示
                        }
                    }
                    
                    // 获取大小或项目数量信息
                    let infoText = '';
                    if (item.is_dir) {
                        if (item.exceeds_limit) {
                            infoText = `${item.item_count}+ 个项目`;
                        } else if (item.item_count > 0) {
                            infoText = `${item.item_count} 个项目`;
                        } else {
                            infoText = '空文件夹';
                        }
                    } else {
                        infoText = formatFileSize(item.size);
                    }
                    
                    // 转义数据
                    const itemJson = encodeURIComponent(JSON.stringify(item));
                    
                    let html = `<div class="search-result-item" data-item-data="${itemJson}" data-is-dir="${item.is_dir}">`;
                    
                    // 图标
                    if (item.is_dir) {
                        html += '<div class="search-result-icon folder">📂</div>';
                    } else {
                        html += '<div class="search-result-icon file">📄</div>';
                    }
                    
                    // 内容区域（一行显示）
                    html += '<div class="search-result-content">';
                    
                    // 第一行：名称 + 路径 + 信息
                    html += '<div class="search-result-row">';
                    
                    // 名称（带高亮）
                    html += `<span class="search-result-name">${highlightedName}</span>`;
                    
                    // 目录路径（如果有）
                    if (dirPath) {
                        html += `<span class="search-result-dir">${dirPath}/</span>`;
                    }
                    
                    // 信息（大小/项目数）
                    html += `<span class="search-result-info">${infoText}</span>`;
                    
                    html += '</div>'; // .search-result-row
                    
                    html += '</div>'; // .search-result-content
                    
                    html += '</div>'; // .search-result-item
                    
                    return html;
                }
                
                // 清除搜索
                function clearSearch() {
                    if (state.treeData && state.treeData.items) {
                        renderFileTree(state.treeData.items, state.treeData);
                    }
                }
                
                // 缓存搜索结果
                let cachedSearchResults = {
                    html: '',
                    searchTerm: '',
                    data: null
                };
                
                // 缓存搜索结果
                function cacheSearchResults(html, searchTerm, data) {
                    cachedSearchResults = {
                        html: html,
                        searchTerm: searchTerm,
                        data: data,
                        timestamp: Date.now()
                    };
                }
                
                // 显示缓存的搜索结果
                function showCachedSearchResults() {
                    if (cachedSearchResults.html) {
                        const mainContent = document.querySelector('.main');
                        mainContent.innerHTML = cachedSearchResults.html;
                        
                        // 重新绑定点击事件（因为innerHTML会移除事件监听器）
                        // 事件已经在document级别委托绑定，不需要额外绑定
                    }
                }
                
                // 重新绑定文件查看界面的按钮事件
                function bindFileViewButtons() {
                    // 下载按钮
                    document.getElementById('download-btn')?.addEventListener('click', function() {
                        if (state.currentFile) {
                            window.open(`/api/download/${encodeURIComponent(state.currentFile.path)}`, '_blank');
                        } else {
                            alert('请先选择文件');
                        }
                    });
                    
                    // 复制代码按钮
                    document.getElementById('copy-code-btn')?.addEventListener('click', function() {
                        if (state.currentFileData?.content) {
                            navigator.clipboard.writeText(state.currentFileData.content)
                                .then(() => {
                                    alert('已复制到剪切板');
                                })
                                .catch(err => {
                                    console.error('复制失败:', err);
                                    alert('复制失败，请手动复制');
                                });
                        } else {
                            alert('没有可复制的内容');
                        }
                    });
                    
                    // Tab切换
                    document.getElementById('source-tab')?.addEventListener('click', function() {
                        switchTab('source');
                    });
                    
                    document.getElementById('explanation-tab')?.addEventListener('click', function() {
                        switchTab('explanation');
                    });
                }
                
                // 添加返回搜索结果按钮
                function addBackToSearchButton() {
                    // 检查是否已经有返回按钮
                    if (document.getElementById('back-to-search-btn')) {
                        return;
                    }
                    
                    // 创建返回按钮
                    const backButton = document.createElement('button');
                    backButton.id = 'back-to-search-btn';
                    backButton.className = 'main-action-btn back-to-search-btn';
                    backButton.innerHTML = '<span>←</span><span>返回搜索结果</span>';
                    
                    // 添加到按钮区域 - 确保在.main-actions容器中
                    const mainActions = document.querySelector('.main-actions');
                    if (mainActions) {
                        // 插入到最前面
                        mainActions.insertBefore(backButton, mainActions.firstChild);
                        
                        // 绑定点击事件
                        backButton.addEventListener('click', function() {
                            // 清除从搜索结果进入的标记
                            state.fromSearchResults = false;
                            
                            // 重新显示搜索结果
                            if (cachedSearchResults.html) {
                                // 显示搜索结果覆盖层
                                let searchOverlay = document.getElementById('search-overlay');
                                if (!searchOverlay) {
                                    searchOverlay = document.createElement('div');
                                    searchOverlay.id = 'search-overlay';
                                    searchOverlay.className = 'search-overlay';
                                    document.querySelector('.main').appendChild(searchOverlay);
                                }
                                
                                searchOverlay.innerHTML = cachedSearchResults.html;
                                searchOverlay.style.display = 'block';
                                
                                // 隐藏文件查看界面的所有部分
                                const mainHeader = document.querySelector('.main-header');
                                const tabBar = document.getElementById('tab-bar');
                                const contentArea = document.querySelector('.content-area');
                                
                                if (mainHeader) mainHeader.style.display = 'none';
                                if (tabBar) tabBar.style.display = 'none';
                                if (contentArea) contentArea.style.display = 'none';
                                
                                // 重新绑定返回按钮事件
                                document.getElementById('back-to-default-btn')?.addEventListener('click', function() {
                                    // 隐藏搜索结果，显示文件查看界面
                                    searchOverlay.style.display = 'none';
                                    if (mainHeader) mainHeader.style.display = 'block';
                                    if (tabBar) tabBar.style.display = 'block';
                                    if (contentArea) contentArea.style.display = 'block';
                                });
                            }
                            
                            // 移除返回按钮
                            backButton.remove();
                        });
                    }
                }
                
                // 点击搜索结果项的事件委托 - 按照你的正确思路：和文件树点击完全一样
                document.addEventListener('click', function(e) {
                    const searchResultItem = e.target.closest('.search-result-item');
                    if (searchResultItem) {
                        try {
                            const itemData = JSON.parse(decodeURIComponent(searchResultItem.dataset.itemData));
                            console.log('从搜索结果点击文件:', itemData);
                            
                            // 确保itemData包含所有必要字段
                            const enhancedItem = {
                                ...itemData,
                                exceeds_limit: itemData.exceeds_limit || false,
                                item_count: itemData.item_count || 0
                            };
                            
                            if (!enhancedItem.is_dir) {
                                // 标记这是从搜索结果进入的
                                state.fromSearchResults = true;
                                state.searchQuery = document.getElementById('file-search').value;
                                
                                // 你的正确思路：和文件树点击完全一样！
                                // 1. 先隐藏搜索结果（恢复文件查看界面）
                                const searchOverlay = document.getElementById('search-overlay');
                                if (searchOverlay) {
                                    searchOverlay.style.display = 'none';
                                }
                                
                                // 2. 显示文件查看界面的所有部分
                                const mainHeader = document.querySelector('.main-header');
                                const tabBar = document.getElementById('tab-bar');
                                const contentArea = document.querySelector('.content-area');
                                const fileActions = document.getElementById('file-actions');
                                
                                if (mainHeader) mainHeader.style.display = 'block';
                                if (tabBar) tabBar.style.display = 'block';
                                if (contentArea) contentArea.style.display = 'block';
                                if (fileActions) fileActions.style.display = 'flex';  // 确保按钮容器显示
                                
                                // 3. 调用selectTreeItem（和文件树点击完全一样）
                                selectTreeItem(enhancedItem, null);
                                
                                // 4. 添加返回搜索结果按钮
                                addBackToSearchButton();
                            } else {
                                alert('文件夹需要在侧边栏中查看，请使用左侧文件树');
                            }
                        } catch (error) {
                            console.error('解析搜索结果项失败:', error);
                            alert('无法打开文件，请重试');
                        }
                    }
                });
                
                // 渲染过滤后的文件树
                function renderFilteredTree(items, searchTerm) {
                    const container = document.getElementById('tree-container');
                    
                    if (!items || items.length === 0) {
                        container.innerHTML = `
                            <div style="padding: 20px; text-align: center; color: #718096;">
                                <p>没有找到匹配 "${searchTerm}" 的文件或文件夹</p>
                            </div>
                        `;
                        return;
                    }
                    
                    let html = '';
                    items.forEach(item => {
                        html += renderTreeItemWithHighlight(item, searchTerm);
                    });
                    
                    // 添加搜索统计
                    html += `
                        <div class="search-stats">
                            <div class="search-stats-content">
                                <span class="search-stats-icon"></span>
                                <span class="search-stats-text">找到 ${items.length} 个匹配 "${searchTerm}" 的结果</span>
                            </div>
                        </div>
                    `;
                    
                    container.innerHTML = html;
                }
                
                // 渲染带高亮的树项
                function renderTreeItemWithHighlight(item, searchTerm) {
                    const isSelected = state.currentFile && state.currentFile.path === item.path;
                    const selectedClass = isSelected ? 'selected' : '';
                    
                    // 转义数据
                    const itemJson = encodeURIComponent(JSON.stringify(item));
                    
                    // 高亮匹配的文本
                    const itemName = escapeHtml(item.name);
                    const lowerName = item.name.toLowerCase();
                    const lowerSearchTerm = searchTerm.toLowerCase();
                    
                    let highlightedName = itemName;
                    if (lowerSearchTerm && lowerName.includes(lowerSearchTerm)) {
                        const startIndex = lowerName.indexOf(lowerSearchTerm);
                        const endIndex = startIndex + searchTerm.length;
                        
                        highlightedName = 
                            itemName.substring(0, startIndex) +
                            `<span class="search-highlight">${itemName.substring(startIndex, endIndex)}</span>` +
                            itemName.substring(endIndex);
                    }
                    
                    let html = `<div class="tree-item ${selectedClass}" data-item-data="${itemJson}" data-is-dir="${item.is_dir}">`;
                    
                    // 文件夹展开箭头
                    if (item.is_dir) {
                        const isExpanded = state.expandedItems.has(item.path);
                        const arrowIcon = isExpanded ? '▽' : '▷';
                        html += `<div class="tree-arrow">${arrowIcon}</div>`;
                    } else {
                        html += '<div class="tree-arrow"></div>';
                    }
                    
                    // 图标
                    if (item.is_dir) {
                        html += '<div class="tree-icon tree-folder">📂</div>';
                    } else {
                        html += '<div class="tree-icon tree-file">📄</div>';
                    }
                    
                    // 名称（带高亮）
                    html += `<div class="tree-name">${highlightedName}</div>`;
                    
                    // 信息
                    if (item.is_dir) {
                        let info = '';
                        if (item.exceeds_limit) {
                            info = `<span class="tree-warning">${item.item_count}+</span>`;
                        } else if (item.item_count > 0) {
                            info = `<span class="tree-info">${item.item_count}</span>`;
                        }
                        html += info;
                    } else {
                        const size = formatFileSize(item.size);
                        html += `<span class="tree-info">${size}</span>`;
                    }
                    
                    html += '</div>';
                    return html;
                }
                
                // Tab按钮事件
                document.getElementById('source-tab').addEventListener('click', function() {
                    switchTab('source');
                });
                
                document.getElementById('explanation-tab').addEventListener('click', function() {
                    switchTab('explanation');
                });
                
                // 解释按钮事件
                document.getElementById('explain-btn').addEventListener('click', function() {
                    if (state.isGeneratingExplanation || !state.currentFileData?.is_code) {
                        return;
                    }
                    
                    handleExplainClick();
                });
            });
            
            // 加载文件树
            async function loadFileTree(path = '') {
                try {
                    const container = document.getElementById('tree-container');
                    container.innerHTML = '<div class="loading"><div class="loading-spinner"></div><p>加载文件树...</p></div>';
                    
                    const url = path ? `/api/tree/${encodeURIComponent(path)}` : '/api/tree/';
                    const response = await fetch(url);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP错误: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    state.treeData = data;
                    
                    // 检查是否有搜索词，如果有则应用搜索过滤
                    const searchInput = document.getElementById('file-search');
                    const searchTerm = searchInput ? searchInput.value.trim().toLowerCase() : '';
                    
                    if (searchTerm) {
                        // 使用新的搜索API
                        const container = document.getElementById('tree-container');
                        container.innerHTML = `
                            <div style="padding: 20px; text-align: center; color: #718096;">
                                <div class="loading-spinner" style="margin: 0 auto 10px;"></div>
                                <p>正在搜索 "${searchTerm}"...</p>
                            </div>
                        `;
                        
                        // 稍后执行搜索，避免阻塞UI
                        setTimeout(async () => {
                            await performSearch(searchTerm);
                        }, 10);
                    } else {
                        renderFileTree(data.items, data);
                    }
                    
                } catch (error) {
                    console.error('加载文件树失败:', error);
                    document.getElementById('tree-container').innerHTML = 
                        `<div style="padding: 20px; color: var(--color-blue);">
                            <h3>加载失败</h3>
                            <p>${error.message}</p>
                            <button onclick="loadFileTree()" style="margin-top: 10px; padding: 8px 16px; background: var(--color-blue); color: white; border: none; border-radius: var(--border-radius); cursor: pointer;">
                                重试
                            </button>
                        </div>`;
                }
            }
            
            // 渲染文件树
            function renderFileTree(items, treeData = null) {
                const container = document.getElementById('tree-container');
                
                if (!items || items.length === 0) {
                    container.innerHTML = '<div style="padding: 20px; text-align: center; color: #718096;">空目录</div>';
                    return;
                }
                
                let html = '';
                items.forEach(item => {
                    html += renderTreeItem(item);
                });
                
                // 如果文件树被截断，显示提示信息
                if (treeData && treeData.truncated) {
                    const remaining = treeData.total_original_items - treeData.count;
                    html += `
                        <div class="tree-truncated-warning">
                            <div class="truncated-icon">⚠️</div>
                            <div class="truncated-message">
                                <strong>显示限制</strong>
                                <p>当前文件夹包含 ${treeData.total_original_items} 个项目，只显示前 ${treeData.max_display_items} 个。</p>
                                <p>还有 ${remaining} 个项目未显示。</p>
                                <p class="truncated-tip">💡 提示：如果需要查看所有文件，请考虑使用搜索功能或分批查看。</p>
                            </div>
                        </div>
                    `;
                }
                
                container.innerHTML = html;
            }
            
            // 渲染单个树项
            function renderTreeItem(item) {
                const isSelected = state.currentFile && state.currentFile.path === item.path;
                const selectedClass = isSelected ? 'selected' : '';
                const isExpanded = state.expandedItems.has(item.path);
                
                // 转义数据 - 使用encodeURIComponent安全存储JSON
                const itemJson = encodeURIComponent(JSON.stringify(item));
                
                let html = `<div class="tree-item ${selectedClass}" data-item-data="${itemJson}" data-is-dir="${item.is_dir}">`;
                
                // 文件夹展开箭头
                if (item.is_dir) {
                    const arrowIcon = isExpanded ? '▽' : '▷';
                    html += `<div class="tree-arrow">${arrowIcon}</div>`;
                } else {
                    html += '<div class="tree-arrow"></div>';
                }
                
                // 图标
                if (item.is_dir) {
                    html += '<div class="tree-icon tree-folder">📂</div>';
                } else {
                    html += '<div class="tree-icon tree-file">📄</div>';
                }
                
                // 名称
                html += `<div class="tree-name">${escapeHtml(item.name)}</div>`;
                
                // 信息
                if (item.is_dir) {
                    let info = '';
                    if (item.exceeds_limit) {
                        info = `<span class="tree-warning">${item.item_count}+</span>`;
                    } else if (item.item_count > 0) {
                        info = `<span class="tree-info">${item.item_count}</span>`;
                    }
                    html += info;
                } else {
                    const size = formatFileSize(item.size);
                    html += `<span class="tree-info">${size}</span>`;
                }
                
                html += '</div>';
                return html;
            }
            
            // 选择树项
            function selectTreeItem(item, element) {
                console.log('selectTreeItem called:', item.path, item.is_dir, 'element:', element);
                
                // 更新选中状态（只在有element时）
                document.querySelectorAll('.tree-item.selected').forEach(el => {
                    el.classList.remove('selected');
                });
                
                if (element) {
                    element.classList.add('selected');
                }
                
                // 保存当前文件
                state.currentFile = item;
                console.log('currentFile set to:', state.currentFile?.path);
                
                // 如果是文件夹，切换展开状态
                if (item.is_dir) {
                    if (element) {
                        toggleFolder(item, element);
                    } else {
                        alert('文件夹需要在侧边栏中查看');
                    }
                } else {
                    // 如果是文件，加载内容
                    updateFileView(item);
                }
            }
            
            // 切换文件夹展开状态
            async function toggleFolder(item, element) {
                if (item.exceeds_limit) {
                    alert(item.limit_message || '文件夹内项目过多，为避免性能问题暂不展开显示');
                    return;
                }
                
                const wasExpanded = state.expandedItems.has(item.path);
                const arrowElement = element.querySelector('.tree-arrow');
                
                if (wasExpanded) {
                    // 收起文件夹
                    state.expandedItems.delete(item.path);
                    // 更新箭头图标
                    if (arrowElement) arrowElement.textContent = '▷';
                    // 移除子项容器
                    const childrenContainerId = `children-${item.path.replace(/[^a-zA-Z0-9]/g, '-')}`;
                    const childrenContainer = document.getElementById(childrenContainerId);
                    if (childrenContainer) {
                        childrenContainer.remove();
                    }
                } else {
                    // 展开文件夹
                    state.expandedItems.add(item.path);
                    // 更新箭头图标
                    if (arrowElement) arrowElement.textContent = '▽';
                    // 加载子项
                    await loadFolderChildren(item, element);
                }
                
                // 不再重新渲染整个文件树
            }
            
            // 加载文件夹子项
            async function loadFolderChildren(item, parentElement) {
                const childrenContainerId = `children-${item.path.replace(/[^a-zA-Z0-9]/g, '-')}`;
                let childrenContainer = document.getElementById(childrenContainerId);
                
                if (!childrenContainer) {
                    // 创建子项容器
                    childrenContainer = document.createElement('div');
                    childrenContainer.className = 'tree-children';
                    childrenContainer.id = childrenContainerId;
                    childrenContainer.setAttribute('data-parent-path', item.path);
                    parentElement.parentNode.insertBefore(childrenContainer, parentElement.nextSibling);
                }
                
                // 显示加载状态
                childrenContainer.innerHTML = '<div class="loading" style="padding: 8px 16px; color: #718096;">加载中...</div>';
                
                try {
                    // 加载子项数据
                    const response = await fetch(`/api/tree/${encodeURIComponent(item.path)}`);
                    if (!response.ok) {
                        throw new Error(`HTTP错误: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // 渲染子项
                    let childrenHtml = '';
                    data.items.forEach(childItem => {
                        childrenHtml += renderTreeItem(childItem);
                    });
                    
                    if (data.items.length === 0) {
                        childrenHtml = '<div style="padding: 8px 16px; color: #718096; font-size: 14px;">空文件夹</div>';
                    }
                    
                    // 如果子文件夹被截断，显示提示信息
                    if (data.truncated) {
                        const remaining = data.total_original_items - data.count;
                        childrenHtml += `
                            <div class="tree-truncated-warning" style="margin: 8px 16px;">
                                <div class="truncated-icon">⚠️</div>
                                <div class="truncated-message">
                                    <strong>显示限制</strong>
                                    <p>此文件夹包含 ${data.total_original_items} 个项目，只显示前 ${data.max_display_items} 个。</p>
                                    <p>还有 ${remaining} 个项目未显示。</p>
                                </div>
                            </div>
                        `;
                    }
                    
                    childrenContainer.innerHTML = childrenHtml;
                    
                } catch (error) {
                    console.error('加载子项失败:', error);
                    childrenContainer.innerHTML = `<div style="padding: 8px 16px; color: var(--color-blue);">加载失败: ${error.message}</div>`;
                }
            }
            
            // 更新文件视图
            async function updateFileView(item) {
                // 显示加载状态
                showLoadingState();
                
                // 初始化UI状态
                initializeFileViewUI(item);
                
                try {
                    // 加载文件内容
                    const response = await fetch(`/api/file/${encodeURIComponent(item.path)}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP错误: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // 更新文件信息到标题区域
                    document.getElementById('file-info').textContent = generateFileInfoText(data);
                    
                    // 保存文件数据到状态
                    state.currentFileData = data;
                    
                    // 如果是代码文件，显示Tab栏
                    if (data.is_code) {
                        document.getElementById('tab-bar').style.display = 'flex';
                    } else {
                        document.getElementById('tab-bar').style.display = 'none';
                    }
                    
                    // 渲染内容（根据当前激活的Tab）
                    renderContent();
                    
                } catch (error) {
                    console.error('加载文件内容失败:', error);
                    showErrorState(error);
                }
            }
            
            // 工具函数
            function formatFileSize(bytes) {
                if (bytes === 0) return '0 B';
                if (bytes < 1024) return bytes + ' B';
                if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
                if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
                return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
            }
            
            function escapeHtml(text) {
                if (!text) return '';
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            // 生成文件信息文本
            function generateFileInfoText(data) {
                if (data.is_binary || data.content === null) {
                    return `二进制文件 • ${formatFileSize(data.size)}`;
                } else if (data.content.trim() === '') {
                    return `空文件 • ${formatFileSize(data.size)}`;
                } else if (data.is_code) {
                    return `${data.language} • ${data.lines} 行 • ${formatFileSize(data.size)} • ✅ 语法高亮`;
                } else {
                    return `文本文件 • ${data.lines} 行 • ${formatFileSize(data.size)}`;
                }
            }
            
            // 显示加载状态
            function showLoadingState() {
                const emptyState = document.getElementById('empty-state');
                if (emptyState) {
                    emptyState.style.display = 'none';
                }
                const contentArea = document.getElementById('content-area');
                if (contentArea) {
                    contentArea.innerHTML = `
                        <div class="loading">
                            <div class="loading-spinner"></div>
                            <p>加载文件内容...</p>
                        </div>
                    `;
                }
            }
            
            // 显示错误状态
            function showErrorState(error) {
                const contentArea = document.getElementById('content-area');
                contentArea.innerHTML = 
                    `<div style="padding: 40px; text-align: center; color: var(--color-blue);">
                        <h3>加载失败</h3>
                        <p>${error.message}</p>
                        <button onclick="updateFileView(state.currentFile)" style="margin-top: 10px; padding: 8px 16px; background: var(--color-blue); color: white; border: none; border-radius: var(--border-radius); cursor: pointer;">
                            重试
                        </button>
                    </div>`;
            }
            
            // 初始化文件视图UI
            function initializeFileViewUI(item) {
                // 更新标题（安全检查）
                const fileTitle = document.getElementById('file-title');
                const fileSubtitle = document.getElementById('file-subtitle');
                if (fileTitle) fileTitle.textContent = item.name;
                if (fileSubtitle) fileSubtitle.textContent = item.path;
                
                // 保存当前文件到状态
                state.currentFile = item;
                
                // 清空文件信息（安全检查）
                const fileInfo = document.getElementById('file-info');
                if (fileInfo) fileInfo.textContent = '';
                
                // 显示操作按钮（安全检查）
                const fileActions = document.getElementById('file-actions');
                if (fileActions) fileActions.style.display = 'flex';
                
                // 默认隐藏Tab栏（安全检查）
                const tabBar = document.getElementById('tab-bar');
                if (tabBar) tabBar.style.display = 'none';
                
                // 隐藏Tab栏修改按钮（安全检查）
                const modifyContainer = document.getElementById('tab-modify-container');
                if (modifyContainer) {
                    modifyContainer.style.display = 'none';
                }
                
                // 重置Tab状态到源代码（安全检查）
                state.activeTab = 'source';
                const sourceTab = document.getElementById('source-tab');
                const explanationTab = document.getElementById('explanation-tab');
                if (sourceTab) sourceTab.classList.add('active');
                if (explanationTab) explanationTab.classList.remove('active');
                
                // 重置解释状态
                state.explanationData = null;
                state.isGeneratingExplanation = false;
                state.hasExplanation = false;
                
                // 重置解释按钮状态
                const explainBtn = document.getElementById('explain-btn');
                if (explainBtn) {
                    explainBtn.disabled = false;
                    explainBtn.textContent = '获取解释';
                }
            }
            
            // 渲染源代码Tab的内容
            function renderSourceCode(data) {
                if (data.is_binary || data.content === null) {
                    // 二进制或无法读取的文件
                    return `
                        <div class="binary-notice">
                            <h3>无法预览此文件</h3>
                            <p>这是一个二进制文件或无法以文本格式读取的文件。</p>
                            <p>文件大小: ${formatFileSize(data.size)}</p>
                            <p>MIME类型: ${data.mime_type}</p>
                        </div>
                    `;
                } else if (data.content.trim() === '') {
                    // 空文件
                    return `
                        <div class="binary-notice">
                            <h3>文件为空</h3>
                            <p>此文件不包含任何内容。</p>
                            <p>文件大小: ${formatFileSize(data.size)}</p>
                        </div>
                    `;
                } else if (data.is_code) {
                    // 代码文件
                    return `
                        <div class="code-container">
                            <pre><code class="language-${data.language}">${escapeHtml(data.content)}</code></pre>
                        </div>
                    `;
                } else {
                    // 普通文本文件
                    return `
                        <div class="code-container">
                            <pre>${escapeHtml(data.content)}</pre>
                        </div>
                    `;
                }
            }
            
            // 渲染解释Tab的内容（占位符）
            function renderExplanation(data) {
                if (!data.is_code) {
                    return `
                        <div class="binary-notice">
                            <h3>非代码文件</h3>
                            <p>解释功能仅适用于代码文件。</p>
                        </div>
                    `;
                }
                
                // 如果正在生成解释，显示美观的加载状态
                if (state.isGeneratingExplanation) {
                    return `
                        <div class="explanation-loading">
                            <div class="loading-card">
                                <div class="loading-spinner-large"></div>
                                <h3 class="loading-title">正在生成AI解释</h3>
                                <p class="loading-message">
                                    正在使用DeepSeek AI模型分析您的代码，请稍候...
                                </p>
                                <p class="loading-details">
                                    🤖 分析中：${state.currentFile?.name || '当前文件'}
                                </p>
                                <div class="loading-progress">
                                    <div class="loading-progress-bar"></div>
                                </div>
                                <div class="loading-tip">
                                    <strong>💡 提示：</strong>AI解释生成可能需要30-60秒，具体时间取决于文件大小和复杂度。<br>
                                    请保持页面打开，不要关闭或刷新浏览器。
                                </div>
                            </div>
                        </div>
                    `;
                }
                
                // 如果处于手动输入模式，显示手动输入界面
                if (state.isManualInputMode) {
                    return `
                        <div class="manual-input-container">
                            <div class="manual-input-card">
                                <div class="manual-input-header">
                                    <h2>${state.hasExplanation ? '编辑代码解释' : '手动输入代码解释'}</h2>
                                    <p>${state.hasExplanation ? '编辑现有解释' : '为文件'} <strong>${state.currentFile?.name || '当前文件'}</strong> ${state.hasExplanation ? '修改解释内容' : '输入自定义解释'}（支持Markdown格式）</p>
                                    ${state.hasExplanation ? '<p style="color: var(--color-blue); margin-top: 8px;">💡 您正在编辑现有解释，保存后将覆盖原有内容</p>' : ''}
                                </div>
                                
                                <div class="manual-input-area">
                                    <textarea 
                                        class="manual-input-textarea" 
                                        id="manual-input-textarea"
                                        placeholder="请输入代码解释内容，支持Markdown格式..."
                                        oninput="updateManualInputText(this.value)"
                                    >${state.manualInputText}</textarea>
                                </div>
                                
                                <div class="manual-input-tips">
                                    <h4>💡 输入提示：</h4>
                                    <ul>
                                        <li>支持Markdown格式（标题、列表、代码块、链接等）</li>
                                        <li>解释内容将永久保存到数据库</li>
                                        <li>下次打开同一文件时会自动显示您的解释</li>
                                        <li>${state.hasExplanation ? '保存后将覆盖现有解释' : '可以随时修改已保存的解释'}</li>
                                    </ul>
                                </div>
                                
                                <div class="manual-input-actions">
                                    <button 
                                        class="manual-input-btn cancel"
                                        onclick="cancelManualInput()"
                                    >
                                        取消
                                    </button>
                                    <button 
                                        class="manual-input-btn save"
                                        onclick="saveManualExplanation()"
                                        ${state.manualInputText.trim() ? '' : 'disabled'}
                                    >
                                        保存解释
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }
                
                // 如果有解释数据，直接显示解释内容
                if (state.hasExplanation && state.explanationData) {
                    const explanation = state.explanationData;
                    
                    // 判断是否是降级模式
                    const isFallback = explanation.source === 'mock_fallback' || 
                                      (explanation.error_type && explanation.error_detail);
                    
                    // 如果是降级模式，在内容前添加简短的错误提示
                    let prefixHtml = '';
                    if (isFallback) {
                        prefixHtml = `
                            <div class="explanation-warning">
                                <div class="explanation-warning-title">
                                    <span>⚠️</span>
                                    <span>AI解释服务暂时不可用</span>
                                </div>
                                <div class="explanation-warning-details">
                                    ${explanation.error_type || '服务故障'}: ${explanation.error_detail || '请稍后重试'}
                                </div>
                            </div>
                        `;
                    }
                    
                    return `
                        <div class="explanation-container">
                            ${prefixHtml}
                            <div class="explanation-content">
                                ${marked.parse(explanation.content)}
                            </div>
                            
                            <!-- 修改解释按钮（已移到Tab栏，此处不再显示） -->
                        </div>
                    `;
                }
                
                // 没有解释数据，显示美观的卡片选择界面
                return `
                    <div class="explanation-choice-container">
                        <div class="explanation-title">
                            <h2>代码解释</h2>
                            <p>选择适合您的方式获取代码解释，所有解释会自动保存以便日后查看</p>
                        </div>
                        
                        <div class="explanation-cards">
                            <!-- AI解释卡片 -->
                            <div class="explanation-card">
                                <div class="card-icon ai">
                                    🤖
                                </div>
                                <div class="card-header">
                                    <h3>AI智能解释</h3>
                                </div>
                                <div class="card-description">
                                    使用DeepSeek AI模型自动分析代码结构、功能、逻辑，生成详细的技术解释。
                                </div>
                                <div class="card-features">
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>逐段分析代码功能</span>
                                    </div>
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>识别关键逻辑和模式</span>
                                    </div>
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>提供改进建议</span>
                                    </div>
                                </div>
                                <button 
                                    class="card-button ai"
                                    onclick="handleGetAIExplanation()"
                                >
                                    获取AI代码解释
                                </button>
                            </div>
                            
                            <!-- 手动输入卡片 -->
                            <div class="explanation-card">
                                <div class="card-icon manual">
                                    ✍️
                                </div>
                                <div class="card-header">
                                    <h3>手动输入解释</h3>
                                </div>
                                <div class="card-description">
                                    手动输入自定义解释内容，适用于AI无法访问或需要特定说明的场景。
                                </div>
                                <div class="card-features">
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>支持Markdown格式</span>
                                    </div>
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>即时保存到数据库</span>
                                    </div>
                                    <div class="card-feature">
                                        <span class="feature-icon">✓</span>
                                        <span>可添加自定义备注</span>
                                    </div>
                                </div>
                                <button 
                                    class="card-button manual"
                                    onclick="handleManualExplanation()"
                                >
                                    手动输入代码解释
                                </button>
                            </div>
                        </div>
                        
                        <div class="explanation-footer">
                            <p>💡 所有解释都会自动保存，下次打开同一文件时直接显示，无需重复操作</p>
                            <p style="margin-top: 8px; font-size: 13px;">AI解释可能需要30-60秒生成，请耐心等待</p>
                        </div>
                    </div>
                `;
            }
            
            // 获取AI代码解释
            async function handleGetAIExplanation() {
                if (!state.currentFileData?.is_code) {
                    alert('解释功能仅适用于代码文件');
                    return;
                }
                
                // 设置生成状态
                state.isGeneratingExplanation = true;
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                renderContent(); // 重新渲染以显示加载状态
                
                try {
                    // 使用AbortController设置超时（120秒，与后端一致）
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 120000);
                    
                    // 调用真实API，带超时控制
                    const response = await fetch(`/api/explain/${encodeURIComponent(state.currentFile.path)}`, {
                        signal: controller.signal
                    });
                    
                    clearTimeout(timeoutId);
                    
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({}));
                        throw new Error(errorData.error || `HTTP错误: ${response.status}`);
                    }
                    
                    const explanation = await response.json();
                    
                    // 保存解释数据
                    setExplanationData(explanation);
                    
                    // 显示成功消息
                    console.log(`AI解释生成成功，耗时: ${explanation.response_time || '未知'}秒`);
                    
                } catch (error) {
                    console.error('生成解释失败:', error);
                    
                    // 根据错误类型生成具体的错误信息
                    let errorType = '未知错误';
                    let errorDetail = '无法连接到AI解释服务，请检查网络连接或API配置。';
                    
                    if (error.name === 'AbortError' || error.name === 'DOMException' && error.message.includes('aborted')) {
                        errorType = '请求超时';
                        errorDetail = '请求超过120秒未响应，可能是AI服务响应慢或网络连接问题。建议稍后重试或尝试较小的文件。';
                    } else if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                        errorType = '网络连接失败';
                        errorDetail = '无法连接到服务器，请检查网络连接或服务器状态。';
                    } else if (error.name === 'TypeError' && error.message.includes('NetworkError')) {
                        errorType = '网络错误';
                        errorDetail = '网络请求失败，可能是跨域问题或网络连接中断。';
                    } else if (error.name === 'DOMException' && error.message.includes('aborted')) {
                        errorType = '请求被中止';
                        errorDetail = '请求被用户或浏览器中止。';
                    }
                    
                    // 降级到模拟数据
                    const mockExplanation = {
                        id: 'mock_' + Date.now(),
                        content: `# AI解释服务暂时不可用\n\n**错误原因**: ${errorType}\n**详细说明**: ${errorDetail}\n\n**建议**: 请检查网络连接或稍后重试。如需手动输入解释，请点击"手动输入代码解释"按钮。`,
                        generated_at: new Date().toISOString(),
                        language: state.currentFileData.language,
                        file_path: state.currentFile.path,
                        source: 'mock_fallback',
                        error_type: errorType,
                        error_detail: errorDetail
                    };
                    
                    setExplanationData(mockExplanation);
                    
                    // 显示错误提示（但不打断流程）
                    console.warn(`AI解释生成失败: ${errorType} - ${errorDetail}`);
                } finally {
                    // 重置生成状态
                    state.isGeneratingExplanation = false;
                }
            }
            
            // 手动输入代码解释 - 切换到手动输入模式
            function handleManualExplanation() {
                if (!state.currentFileData?.is_code) {
                    alert('解释功能仅适用于代码文件');
                    return;
                }
                
                // 切换到手动输入模式
                state.isManualInputMode = true;
                
                // 在手动输入模式下隐藏Tab栏修改按钮
                const modifyContainer = document.getElementById('tab-modify-container');
                if (modifyContainer) {
                    modifyContainer.style.display = 'none';
                }
                
                // 如果有现有解释，加载到输入框中供编辑
                if (state.hasExplanation && state.explanationData) {
                    state.manualInputText = state.explanationData.content;
                    console.log('加载现有解释到输入框，长度:', state.manualInputText.length);
                } else {
                    state.manualInputText = '';
                }
                
                renderContent();
            }
            
            // 编辑现有解释 - 切换到编辑模式
            function handleEditExplanation() {
                if (!state.currentFileData?.is_code) {
                    alert('只有代码文件可以编辑解释');
                    return;
                }
                
                if (!state.hasExplanation || !state.explanationData) {
                    alert('没有可编辑的解释，请先创建解释');
                    return;
                }
                
                // 切换到手动输入模式（编辑模式）
                state.isManualInputMode = true;
                
                // 加载现有解释到输入框中
                state.manualInputText = state.explanationData.content;
                console.log('编辑模式：加载现有解释到输入框，长度:', state.manualInputText.length);
                
                // 在手动输入模式下隐藏Tab栏修改按钮
                const modifyContainer = document.getElementById('tab-modify-container');
                if (modifyContainer) {
                    modifyContainer.style.display = 'none';
                }
                
                renderContent();
            }
            
            // 取消手动输入
            function cancelManualInput() {
                state.isManualInputMode = false;
                state.manualInputText = '';
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                renderContent();
            }
            
            // 保存手动输入的解释
            async function saveManualExplanation() {
                console.log('=== 开始保存手动解释 ===');
                console.log('当前状态:', {
                    isManualInputMode: state.isManualInputMode,
                    hasExplanation: state.hasExplanation,
                    activeTab: state.activeTab,
                    manualInputTextLength: state.manualInputText.length
                });
                
                const explanationText = state.manualInputText.trim();
                if (!explanationText) {
                    alert('解释内容不能为空');
                    return;
                }
                
                // 禁用保存按钮，显示简单保存状态（不是AI解释的加载状态）
                const saveBtn = document.querySelector('.manual-input-btn.save');
                if (saveBtn) {
                    saveBtn.disabled = true;
                    saveBtn.textContent = '保存中...';
                }
                
                try {
                    // 发送到服务器保存
                    const response = await fetch(`/api/save_manual_explanation/${encodeURIComponent(state.currentFile.path)}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            content: explanationText
                        })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({}));
                        throw new Error(errorData.error || `HTTP错误: ${response.status}`);
                    }
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // 创建解释对象
                        const manualExplanation = {
                            id: 'manual_' + Date.now(),
                            content: explanationText,
                            language: state.currentFileData.language,
                            file_path: state.currentFile.path,
                            filename: state.currentFile.name,
                            generated_at: new Date().toISOString(),
                            source: 'manual',
                            explanation_type: 'manual'
                        };
                        
                        // 先退出手动输入模式
                        state.isManualInputMode = false;
                        state.manualInputText = '';
                        
                        // 然后保存到状态
                        setExplanationData(manualExplanation);
                        
                        // 恢复按钮状态
                        const saveBtn = document.querySelector('.manual-input-btn.save');
                        if (saveBtn) {
                            saveBtn.disabled = false;
                            saveBtn.textContent = '保存解释';
                        }
                        
                        console.log('=== 手动解释保存成功 ===');
                        console.log('保存后的状态:', {
                            isManualInputMode: state.isManualInputMode,
                            hasExplanation: state.hasExplanation,
                            explanationData: state.explanationData ? '有数据' : '无数据'
                        });
                        
                        // 确保界面更新后再显示提示
                        setTimeout(() => {
                            alert('手动解释已保存！');
                        }, 10);
                    } else {
                        throw new Error(result.error || '保存失败');
                    }
                    
                } catch (error) {
                    console.error('保存手动解释失败:', error);
                    alert(`保存失败: ${error.message}`);
                    
                    // 恢复按钮状态
                    const saveBtn = document.querySelector('.manual-input-btn.save');
                    if (saveBtn) {
                        saveBtn.disabled = false;
                        saveBtn.textContent = '保存解释';
                    }
                }
            }
            
            // 更新手动输入文本
            function updateManualInputText(text) {
                state.manualInputText = text;
                // 重新渲染内容以更新保存按钮状态
                if (state.isManualInputMode && state.activeTab === 'explanation') {
                    renderContent();
                }
            }
            
            // 根据当前激活的Tab渲染内容
            function renderContent() {
                if (!state.currentFileData) {
                    return '<div class="loading"><div class="loading-spinner"></div><p>加载文件内容...</p></div>';
                }
                
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                
                const contentArea = document.getElementById('content-area');
                let contentHtml = '';
                
                if (state.activeTab === 'source') {
                    contentHtml = renderSourceCode(state.currentFileData);
                } else if (state.activeTab === 'explanation') {
                    contentHtml = renderExplanation(state.currentFileData);
                }
                
                contentArea.innerHTML = contentHtml;
                
                // 如果是源代码Tab且是代码文件，应用语法高亮
                if (state.activeTab === 'source' && state.currentFileData.is_code && typeof Prism !== 'undefined') {
                    Prism.highlightAll();
                }
            }
            
            // 设置解释数据
            function setExplanationData(explanation) {
                state.explanationData = explanation;
                state.hasExplanation = true;
                state.isGeneratingExplanation = false; // 确保生成状态被重置
                
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                
                // 总是重新渲染内容，确保界面更新
                renderContent();
            }
            
            // 设置生成状态
            function setGeneratingExplanation(generating) {
                state.isGeneratingExplanation = generating;
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                renderContent();
            }
            
            // 更新Tab栏修改按钮的显示状态
            function updateTabModifyButton() {
                const modifyContainer = document.getElementById('tab-modify-container');
                if (!modifyContainer) return;
                
                // 只有在解释Tab激活、有解释数据、不在生成中、不在手动输入模式时才显示修改按钮
                const shouldShow = state.activeTab === 'explanation' && 
                                   state.hasExplanation && 
                                   !state.isGeneratingExplanation && 
                                   !state.isManualInputMode;
                modifyContainer.style.display = shouldShow ? 'flex' : 'none';
            }
            
            // 切换Tab
            function switchTab(tabName) {
                if (state.activeTab === tabName) return;
                
                state.activeTab = tabName;
                
                // 更新Tab按钮样式
                document.getElementById('source-tab').classList.toggle('active', tabName === 'source');
                document.getElementById('explanation-tab').classList.toggle('active', tabName === 'explanation');
                
                // 更新Tab栏修改按钮的显示状态
                updateTabModifyButton();
                
                // 如果是切换到解释Tab且没有解释数据，尝试从数据库加载
                if (tabName === 'explanation' && !state.hasExplanation && state.currentFile) {
                    loadExplanationFromDatabase();
                } else {
                    // 重新渲染内容
                    renderContent();
                }
            }
            
            // 从数据库加载解释
            async function loadExplanationFromDatabase() {
                if (!state.currentFile) return;
                
                try {
                    const response = await fetch(`/api/check_explanation/${encodeURIComponent(state.currentFile.path)}`);
                    
                    if (!response.ok) {
                        // 检查失败，正常渲染
                        renderContent();
                        return;
                    }
                    
                    const result = await response.json();
                    
                    if (result.has_explanation) {
                        // 有解释数据，保存到状态
                        const explanation = {
                            id: `db_${Date.now()}`,
                            content: result.content,
                            language: state.currentFileData?.language || 'text',
                            file_path: state.currentFile.path,
                            filename: state.currentFile.name,
                            generated_at: result.created_at || new Date().toISOString(),
                            updated_at: result.updated_at,
                            source: 'database',
                            explanation_type: result.explanation_type
                        };
                        
                        setExplanationData(explanation);
                    } else {
                        // 没有解释数据，正常渲染
                        renderContent();
                    }
                } catch (error) {
                    console.error('从数据库加载解释失败:', error);
                    renderContent();
                }
            }