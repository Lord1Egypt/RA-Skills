(function() {
    'use strict';

    function getTimestamp() {
        const pathParts = window.location.pathname.split('/');
        return pathParts[2] || '';
    }

    async function checkAnalysis(newsId, timestamp) {
        try {
            const response = await fetch(`/check-analysis?newsId=${newsId}&timestamp=${timestamp}`);
            const data = await response.json();
            return data.exists;
        } catch (error) {
            console.error('Error checking analysis:', error);
            return false;
        }
    }

    function viewAnalysis(newsId, timestamp) {
        window.open(`/view-analysis?newsId=${newsId}&timestamp=${timestamp}`, '_blank');
    }

    async function deleteAnalysis(newsId, timestamp) {
        if (!confirm('确定要删除这条AI解读吗？删除后可以重新生成。')) {
            return false;
        }

        try {
            const response = await fetch(`/delete-analysis?newsId=${newsId}&timestamp=${timestamp}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            return data.success;
        } catch (error) {
            console.error('Error deleting analysis:', error);
            alert('删除失败：' + error.message);
            return false;
        }
    }

    async function generateAnalysis(newsData, customPrompt = '') {
        const { newsId, newsUrl, newsSource, newsTime, title, summary, timestamp } = newsData;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    newsId,
                    newsUrl,
                    newsSource,
                    newsTime,
                    timestamp,
                    title,
                    summary,
                    customPrompt
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || '生成失败');
            }

            const result = await response.json();
            return { success: true, message: result.message };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    function showLoadingModal(message = '正在生成AI解读...') {
        const existingModal = document.getElementById('loading-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.id = 'loading-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        modal.innerHTML = `
            <div style="background: white; padding: 30px; border-radius: 12px; text-align: center; max-width: 400px; width: 90%;">
                <div class="spinner" style="
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                "></div>
                <p style="color: #333; font-size: 16px; margin: 0;">${message}</p>
                <p id="elapsed-time" style="color: #667eea; font-size: 14px; margin-top: 10px; font-weight: 600;">已用时：0秒</p>
                <div style="width: 100%; height: 8px; background: #f3f3f3; border-radius: 4px; margin-top: 15px; overflow: hidden;">
                    <div id="progress-bar" style="height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; width: 0%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(modal);

        // 启动计时器和进度条更新
        const startTime = Date.now();
        const updateInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const timeEl = document.getElementById('elapsed-time');
            const progressBar = document.getElementById('progress-bar');

            if (timeEl) {
                timeEl.textContent = `已用时：${elapsed}秒`;
            }

            if (progressBar) {
                // 假进度条：快速到30%，然后逐渐减缓，最多到95%
                let progress;
                if (elapsed < 5) {
                    progress = elapsed * 6; // 0-30%
                } else if (elapsed < 30) {
                    progress = 30 + (elapsed - 5) * 2; // 30-80%
                } else {
                    progress = 80 + Math.min(15, (elapsed - 30) * 0.5); // 80-95%
                }
                progressBar.style.width = `${Math.min(95, progress)}%`;
            }
        }, 1000);

        // 保存计时器ID，方便清除
        modal.dataset.intervalId = updateInterval;
    }

    function hideLoadingModal() {
        const modal = document.getElementById('loading-modal');
        if (modal) {
            // 清除定时器
            const intervalId = modal.dataset.intervalId;
            if (intervalId) {
                clearInterval(Number(intervalId));
            }
            modal.remove();
        }
    }

    function showCustomPromptModal(newsData, onSubmit) {
        const existingModal = document.getElementById('custom-prompt-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.id = 'custom-prompt-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;

        modal.innerHTML = `
            <div style="background: white; padding: 30px; border-radius: 12px; max-width: 600px; width: 90%;">
                <h3 style="margin: 0 0 20px 0; color: #333;">自定义AI解读角度</h3>
                <p style="color: #666; margin-bottom: 15px;">可以指定特定的分析角度，例如：技术影响、商业价值、用户体验等（留空使用默认分析）</p>
                <textarea id="custom-prompt-input"
                    placeholder="例如：请从技术架构的角度分析这个新闻..."
                    style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; font-family: inherit; resize: vertical;"
                ></textarea>
                <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end;">
                    <button id="cancel-btn" style="padding: 10px 20px; border: 1px solid #ddd; background: white; border-radius: 6px; cursor: pointer;">取消</button>
                    <button id="submit-btn" style="padding: 10px 20px; border: none; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 6px; cursor: pointer;">生成解读</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        const textarea = modal.querySelector('#custom-prompt-input');
        const cancelBtn = modal.querySelector('#cancel-btn');
        const submitBtn = modal.querySelector('#submit-btn');

        cancelBtn.onclick = () => modal.remove();
        submitBtn.onclick = () => {
            const customPrompt = textarea.value.trim();
            modal.remove();
            onSubmit(customPrompt);
        };

        // 点击背景关闭
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        };

        // 聚焦输入框
        setTimeout(() => textarea.focus(), 100);
    }

    async function handleAnalyzeClick(newsData) {
        showCustomPromptModal(newsData, async (customPrompt) => {
            showLoadingModal('正在生成AI解读...');

            const startTime = Date.now();
            const timeout = 120000; // 120秒超时

            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('请求超时，AI解读生成时间过长')), timeout);
            });

            try {
                const result = await Promise.race([
                    generateAnalysis(newsData, customPrompt),
                    timeoutPromise
                ]);

                hideLoadingModal();

                if (result.success) {
                    alert('AI解读生成成功！');
                    // 刷新按钮状态
                    location.reload();
                } else {
                    alert('生成失败：' + result.error);
                }
            } catch (error) {
                hideLoadingModal();
                alert('生成失败：' + error.message);
            }
        });
    }

    async function updateButtonState(card, newsData, exists) {
        const { newsId, timestamp } = newsData;
        const buttonContainer = card.querySelector('.news-actions');

        if (!buttonContainer) return;

        // 清除现有按钮
        const oldButtons = buttonContainer.querySelectorAll('.ai-analyze-btn, .delete-analysis-btn');
        oldButtons.forEach(btn => btn.remove());

        if (exists) {
            // 已有解读：显示"查看AI解读"和"删除解读"按钮
            const viewBtn = document.createElement('button');
            viewBtn.textContent = '查看AI解读';
            viewBtn.className = 'btn btn-success ai-analyze-btn';
            viewBtn.onclick = () => viewAnalysis(newsId, timestamp);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = '删除解读';
            deleteBtn.className = 'btn btn-danger delete-analysis-btn';
            deleteBtn.onclick = async () => {
                const success = await deleteAnalysis(newsId, timestamp);
                if (success) {
                    alert('解读已删除');
                    location.reload();
                }
            };

            buttonContainer.appendChild(viewBtn);
            buttonContainer.appendChild(deleteBtn);
        } else {
            // 未生成：显示"AI解读"按钮
            const analyzeBtn = document.createElement('button');
            analyzeBtn.textContent = 'AI解读';
            analyzeBtn.className = 'btn btn-primary ai-analyze-btn';
            analyzeBtn.onclick = () => handleAnalyzeClick(newsData);

            buttonContainer.appendChild(analyzeBtn);
        }
    }

    async function initializeButtons() {
        const timestamp = getTimestamp();
        const newsCards = document.querySelectorAll('.news-card');

        for (const card of newsCards) {
            const newsId = card.getAttribute('data-news-id');
            const newsUrl = card.getAttribute('data-news-url');
            const newsSource = card.getAttribute('data-news-source');
            const newsTime = card.getAttribute('data-news-time');

            const titleEl = card.querySelector('.news-title');
            const summaryEl = card.querySelector('.news-summary');
            const title = titleEl ? titleEl.textContent : '';
            const summary = summaryEl ? summaryEl.textContent : '';

            const newsData = {
                newsId,
                newsUrl,
                newsSource,
                newsTime,
                title,
                summary,
                timestamp
            };

            const exists = await checkAnalysis(newsId, timestamp);
            await updateButtonState(card, newsData, exists);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeButtons);
    } else {
        initializeButtons();
    }
})();
