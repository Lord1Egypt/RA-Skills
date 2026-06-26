/**
 * ai-chat.js — AI 对话页面
 *
 * 功能：聊天界面、消息列表、输入框、发送按钮、流式对话
 * 路由：/ai-chat
 */

import { auth, toast } from '../app.js';
import { escapeHtml } from '../utils/escape-html.js';

/**
 * AI 对话服务（简化版 SSE 流式对话）
 */
const ai = {
  /**
   * 发送消息并流式获取回复
   * @param {string} message - 用户消息
   * @param {Object} options
   * @param {Function} options.onChunk - 流式回调，接收文本片段
   * @param {Function} options.onDone - 完成回调
   * @param {Function} options.onError - 错误回调
   */
  async sendMessage(message, { onChunk, onDone, onError } = {}) {
    try {
      const token = auth.getToken();
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.message || `请求失败 (${res.status})`);
      }

      const contentType = res.headers.get('content-type') || '';

      if (contentType.includes('text/event-stream')) {
        // SSE 流式响应
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                if (onDone) onDone();
                return;
              }
              try {
                const parsed = JSON.parse(data);
                const chunk = parsed.content || parsed.text || parsed.data || '';
                if (onChunk) onChunk(chunk);
              } catch {
                // 非 JSON 数据直接作为文本片段
                if (onChunk) onChunk(data);
              }
            }
          }
        }
        if (onDone) onDone();
      } else {
        // 非流式响应
        const data = await res.json();
        const reply = data.reply || data.content || data.text || data.message || JSON.stringify(data);
        if (onChunk) onChunk(reply);
        if (onDone) onDone();
      }
    } catch (err) {
      if (onError) onError(err);
      else toast.error('对话失败: ' + (err.message || '请重试'));
    }
  },
};

let _chatHistory = [];
let _isSending = false;

export function renderAIChat() {
  // 未登录提示
  if (!auth.isLoggedIn()) {
    return `
      <div class="container ai-chat-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔒</div>
          <h3>请先登录</h3>
          <p class="text-muted">登录后使用 AI 助手</p>
          <a href="/login" class="btn btn-primary mt-4" data-nav>去登录</a>
        </div>
      </div>`;
  }

  return `
    <div class="container ai-chat-page">
      <div class="chat-container card">
        <div class="chat-header">
          <h2>🤖 AI 助手</h2>
          <p class="text-muted text-sm">智能对话，随时为您解答</p>
        </div>

        <div class="chat-messages" id="chat-messages">
          <div class="chat-message ai-message">
            <div class="message-avatar">🤖</div>
            <div class="message-bubble">
              <p>你好！我是 AI 助手，有什么可以帮助你的吗？</p>
            </div>
          </div>
          ${_chatHistory.map(renderChatMessage).join('')}
        </div>

        <div class="chat-input-area">
          <div class="chat-input-wrapper">
            <textarea id="chat-input" class="chat-input" rows="1"
                      placeholder="输入您的问题..." maxlength="2000"
                      oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight, 120)+'px'"></textarea>
            <button class="btn btn-primary chat-send-btn" id="chat-send-btn" disabled>
              发送
            </button>
          </div>
          <p class="text-muted text-xs mt-1">按 Enter 发送，Shift+Enter 换行</p>
        </div>
      </div>
    </div>`;
}

export function attachAIChatEvents() {
  _isSending = false;

  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send-btn');
  if (!input || !sendBtn) return;

  const updateSendBtn = () => {
    sendBtn.disabled = !input.value.trim() || _isSending;
  };

  input.addEventListener('input', updateSendBtn);

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!sendBtn.disabled) {
        sendMessage();
      }
    }
  });

  sendBtn.addEventListener('click', sendMessage);

  // 自动聚焦
  input.focus();

  // 滚动到底部
  scrollToBottom();
}

export const __mount = attachAIChatEvents;

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send-btn');
  if (!input || !sendBtn) return;

  const text = input.value.trim();
  if (!text || _isSending) return;

  _isSending = true;
  input.value = '';
  sendBtn.disabled = true;
  sendBtn.textContent = '发送中...';

  // 添加用户消息
  addMessage('user', text);
  _chatHistory.push({ role: 'user', content: text });

  // 创建 AI 消息容器
  const messagesContainer = document.getElementById('chat-messages');
  const aiMsgDiv = document.createElement('div');
  aiMsgDiv.className = 'chat-message ai-message';
  aiMsgDiv.innerHTML = `
    <div class="message-avatar">🤖</div>
    <div class="message-bubble">
      <p class="thinking-dots">思考中<span>.</span><span>.</span><span>.</span></p>
    </div>`;
  messagesContainer.appendChild(aiMsgDiv);
  scrollToBottom();

  let fullReply = '';

  await ai.sendMessage(text, {
    onChunk(chunk) {
      fullReply += chunk;
      const bubble = aiMsgDiv.querySelector('.message-bubble');
      if (bubble) {
        bubble.innerHTML = `<p>${escapeHtml(fullReply).replace(/\n/g, '<br>')}</p>`;
      }
      scrollToBottom();
    },
    onDone() {
      _chatHistory.push({ role: 'assistant', content: fullReply || '（无回复）' });
      _isSending = false;
      sendBtn.textContent = '发送';
      sendBtn.disabled = false;
      scrollToBottom();
    },
    onError(err) {
      const bubble = aiMsgDiv.querySelector('.message-bubble');
      if (bubble) {
        bubble.innerHTML = `<p class="text-error">⚠️ ${escapeHtml(err.message || '对话失败，请重试')}</p>`;
      }
      _isSending = false;
      sendBtn.textContent = '发送';
      sendBtn.disabled = false;
      scrollToBottom();
    },
  });
}

function addMessage(role, content) {
  const container = document.getElementById('chat-messages');
  if (!container) return;

  const div = document.createElement('div');
  div.className = `chat-message ${role}-message`;
  const avatar = role === 'user' ? '👤' : '🤖';
  div.innerHTML = `
    <div class="message-avatar">${avatar}</div>
    <div class="message-bubble">
      <p>${escapeHtml(content).replace(/\n/g, '<br>')}</p>
    </div>`;
  container.appendChild(div);
  scrollToBottom();
}

function renderChatMessage(msg) {
  const role = msg.role || 'user';
  const avatar = role === 'user' ? '👤' : '🤖';
  const content = escapeHtml(msg.content || '').replace(/\n/g, '<br>');

  return `
    <div class="chat-message ${role}-message">
      <div class="message-avatar">${avatar}</div>
      <div class="message-bubble">
        <p>${content}</p>
      </div>
    </div>`;
}

function scrollToBottom() {
  const container = document.getElementById('chat-messages');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}
