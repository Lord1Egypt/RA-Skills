/**
 * 向抖音评论发送回复
 * 在浏览器中通过 browser act evaluate 执行
 * 
 * 使用方式：
 * browser act evaluate fn: "sendReply('回复内容')"
 * 
 * 前置条件：
 * - 已点击评论的"回复"按钮，输入框已打开
 * 
 * 返回格式：
 * { success: true/false, error?: string, content?: string }
 */

function sendReply(replyText) {
  // 查找可编辑的回复输入框
  const editableDivs = document.querySelectorAll('[contenteditable="true"]');
  let replyInput = null;
  
  // 找到当前可见的回复输入框
  for (const div of editableDivs) {
    const style = window.getComputedStyle(div);
    if (style.display !== 'none' && style.visibility !== 'hidden') {
      replyInput = div;
      break;
    }
  }
  
  if (!replyInput) {
    return JSON.stringify({ 
      success: false, 
      error: '未找到回复输入框，请先点击评论的"回复"按钮' 
    });
  }

  // 聚焦输入框
  replyInput.focus();
  
  // 使用 execCommand 插入内容（确保触发 React/Vue 状态更新）
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  document.execCommand('insertText', false, replyText);
  
  // 触发多种事件确保框架感知变化
  replyInput.dispatchEvent(new Event('input', { bubbles: true }));
  replyInput.dispatchEvent(new Event('change', { bubbles: true }));
  replyInput.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
  
  // 等待一下让React状态更新
  return new Promise((resolve) => {
    setTimeout(() => {
      // 查找发送按钮（非disabled状态）
      const buttons = document.querySelectorAll('button');
      let sendBtn = null;
      
      for (const btn of buttons) {
        if (btn.textContent.trim() === '发送' && !btn.disabled) {
          sendBtn = btn;
          break;
        }
      }
      
      if (!sendBtn) {
        resolve(JSON.stringify({ 
          success: false, 
          error: '发送按钮未激活，可能内容未正确输入或字数超限',
          inputContent: replyInput.innerText
        }));
        return;
      }
      
      // 点击发送
      sendBtn.click();
      
      // 等待检查结果
      setTimeout(() => {
        // 检查是否有身份验证弹窗
        const verifyModal = document.querySelector([
          '[class*="verify"]',
          '[class*="auth"]',
          '[class*="modal"]'
        ].join(', '));
        
        const verifyText = verifyModal ? verifyModal.textContent : '';
        const needsVerify = verifyText.includes('验证') || 
                           verifyText.includes('短信') || 
                           verifyText.includes('扫码');
        
        // 检查回复是否成功（输入框是否已清空/关闭）
        const inputCleared = replyInput.innerText.trim() === '' || 
                            replyInput.innerText.includes('有爱评论');
        
        if (needsVerify) {
          resolve(JSON.stringify({ 
            success: false, 
            needsVerify: true,
            error: '需要身份验证，请完成短信/扫码验证后重试'
          }));
        } else if (inputCleared) {
          resolve(JSON.stringify({ 
            success: true, 
            message: '回复发送成功',
            content: replyText
          }));
        } else {
          resolve(JSON.stringify({ 
            success: false, 
            error: '回复可能未成功发送，请检查页面状态',
            inputContent: replyInput.innerText
          }));
        }
      }, 1000);
    }, 100);
  });
}

// 执行
sendReply('__REPLY_TEXT__');
