/**
 * AiService — AI 聊天服务
 *
 * 通过 SSE (Server-Sent Events) 与服务端流式对话。
 * 支持 AbortController 取消请求。
 *
 * 用法：
 *   import { ai } from './ai.js';
 *
 *   // 发送消息，流式回调
 *   const { abort } = ai.sendMessage('你好', [], (chunk) => {
 *     console.log('收到片段:', chunk);
 *   });
 *
 *   // 中途取消
 *   abort();
 */

const CHAT_ENDPOINT = '/api/ai/chat-stream';

export class AiService {
  constructor() {
    /** @type {AbortController|null} */
    this._controller = null;
  }

  /**
   * 发送聊天消息（流式 SSE）
   *
   * @param {string} text - 用户输入
   * @param {Array<{role: string, content: string}>} history - 历史消息
   * @param {Function} onChunk - 收到文本片段时的回调 (chunk: string) => void
   * @param {Object} [options]
   * @param {Function} [options.onDone] - 流结束回调
   * @param {Function} [options.onError] - 错误回调 (err: Error) => void
   * @returns {{ abort: Function }}
   */
  sendMessage(text, history, onChunk, options = {}) {
    const { onDone, onError } = options;

    // 取消上一次未完成的请求
    if (this._controller) {
      this._controller.abort();
    }

    this._controller = new AbortController();
    const signal = this._controller.signal;

    const run = async () => {
      try {
        const res = await fetch(CHAT_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            history: history.slice(-20), // 只保留最近 20 条上下文
          }),
          signal,
        });

        if (!res.ok) {
          throw new Error(`AI 服务响应异常 (${res.status})`);
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // 解析 SSE 事件：data: {...}\n\n
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || ''; // 保留未完成的数据块

          for (const block of lines) {
            const dataLine = block.trim();
            if (!dataLine || !dataLine.startsWith('data: ')) continue;

            const jsonStr = dataLine.slice(6).trim();
            if (jsonStr === '[DONE]') {
              onDone?.();
              return;
            }

            try {
              const parsed = JSON.parse(jsonStr);
              if (parsed.content) {
                onChunk(parsed.content);
              }
              if (parsed.error) {
                throw new Error(parsed.error);
              }
            } catch (e) {
              if (e.name !== 'AbortError') {
                console.warn('[AI] 解析 SSE 数据失败:', e, jsonStr);
              }
            }
          }
        }

        onDone?.();
      } catch (err) {
        if (err.name === 'AbortError') {
          // 用户取消，不做处理
          return;
        }
        console.error('[AI] 请求失败:', err);
        onError?.(err);
      } finally {
        this._controller = null;
      }
    };

    run();

    return {
      abort: () => {
        this._controller?.abort();
        this._controller = null;
      },
    };
  }

  /**
   * 取消当前请求
   */
  cancel() {
    this._controller?.abort();
    this._controller = null;
  }
}
