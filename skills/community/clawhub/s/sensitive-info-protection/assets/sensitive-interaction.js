/**
 * sensitive-info-protection 交互按钮组件
 * 适配 OpenClaw Lit 控制 UI webchat
 */

function injectSensitiveButtons(node, content) {
  // 查找操作选项区域
  const optionsMatch = content.match(/## 操作选项\n([\s\S]*)/);
  if (!optionsMatch) return;

  // 创建按钮容器
  const buttonsDiv = document.createElement('div');
  buttonsDiv.className = 'sensitive-action-buttons';
  buttonsDiv.style.marginTop = '12px';
  buttonsDiv.style.display = 'flex';
  buttonsDiv.style.gap = '8px';
  buttonsDiv.style.paddingBottom = '8px';

  // 定义按钮
  const actions = [
    { text: '1. 确认放行', value: 'confirm', style: 'background: #4CAF50; color: white;' },
    { text: '2. 修改后发送', value: 'edit', style: 'background: #FF9800; color: white;' },
    { text: '3. 取消发送', value: 'cancel', style: 'background: #f44336; color: white;' }
  ];

  actions.forEach(action => {
    const button = document.createElement('button');
    button.textContent = action.text;
    button.style = `
      padding: 8px 16px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      ${action.style}
    `;
    button.onclick = () => handleAction(action.value);
    buttonsDiv.appendChild(button);
  });

  // 适配 OpenClaw Lit 组件 DOM 结构
  // 直接添加到当前检测结果消息节点内部末尾
  if (node.shadowRoot) {
    // 如果是 Web Component，查找消息内容区域
    const contentArea = node.shadowRoot.querySelector('[class*="message"], [part*="message"], div:last-child');
    if (contentArea) {
      contentArea.appendChild(buttonsDiv);
      return;
    }
  }
  
  node.appendChild(buttonsDiv);
}

function handleAction(action) {
  // OpenClaw 控制 UI class 选择器适配
  const inputBox = document.querySelector('textarea, [class*="input"], [part*="input"]');
  switch(action) {
    case 'confirm':
      submitMessage('确认放行', inputBox);
      break;
    case 'edit':
      // 弹出修改框
      const originalText = window.lastSensitiveContent || '';
      const newText = prompt('请输入修改后的内容：', originalText);
      if (newText !== null && newText.trim() !== '') {
        submitMessage(newText, inputBox);
      }
      break;
    case 'cancel':
      submitMessage('取消发送', inputBox);
      break;
  }
}

function submitMessage(text, inputBox) {
  if (inputBox) {
    // 尝试多种方式设置值
    if ('value' in inputBox) {
      inputBox.value = text;
    } else if (inputBox.firstChild && 'value' in inputBox.firstChild) {
      inputBox.firstChild.value = text;
    }
    
    // 触发 input 事件让框架感知变化
    const event = new Event('input', { bubbles: true });
    inputBox.dispatchEvent(event);
    
    // 触发发送按钮点击，适配多种选择器
    setTimeout(() => {
      const sendButton = document.querySelector('button[type="submit"], [class*="send"], [part*="send"]');
      if (sendButton) {
        sendButton.click();
      }
    }, 100);
  }
}

// 自动检测：当新消息包含敏感检测结果时注入按钮
function observeNewMessages() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.addedNodes.length) {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // 检查节点和所有子节点内容
            let content = node.textContent || '';
            if (!content.includes('## 检测结果') || !content.includes('## 操作选项')) {
              // 检查 shadow DOM
              if (node.shadowRoot) {
                content = node.shadowRoot.textContent || '';
              }
            }
            
            if (content.includes('## 检测结果') && content.includes('## 操作选项')) {
              // 保存最后敏感内容供编辑使用
              const match = content.match(/原文: `(.*?)`/);
              if (match) {
                window.lastSensitiveContent = match[1];
              }
              // 注入按钮到当前节点
              injectSensitiveButtons(node, content);
            }
          }
        });
      }
    });
  });

  // 查找顶级容器，适配 OpenClaw 结构
  const chatContainer = document.querySelector('openclaw-app, .chat-container, main, [role="log"]');
  if (chatContainer) {
    observer.observe(chatContainer, { childList: true, subtree: true });
  } else {
    // fallback 到 document body
    observer.observe(document.body, { childList: true, subtree: true });
  }
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', observeNewMessages);
} else {
  // 延迟一点初始化，确保 Lit 组件已经渲染
  setTimeout(observeNewMessages, 500);
}

