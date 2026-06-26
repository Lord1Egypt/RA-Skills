/**
 * 向抖音评论发送回复
 * 在浏览器中通过 evaluate 执行此脚本
 * 
 * 使用方式：
 * 将 REPLY_TEXT 替换为实际回复内容后执行
 * 
 * 注意：
 * - 需要先点击评论的"回复"按钮打开输入框
 * - 使用 execCommand 确保 React/Vue 状态更新
 * - 发送后检查是否出现身份验证弹窗
 */

(function(replyText) {
  // 找到当前激活的回复输入框（contenteditable）
  const editableDiv = document.querySelector('[contenteditable="true"][class*="reply"], [contenteditable="true"]');
  
  if (!editableDiv) {
    return JSON.stringify({ success: false, error: '未找到回复输入框，请先点击"回复"按钮' });
  }

  // 聚焦输入框
  editableDiv.focus();

  // 清空并输入内容（使用 execCommand 触发框架状态更新）
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  document.execCommand('insertText', false, replyText);

  // 触发事件确保框架感知变化
  editableDiv.dispatchEvent(new Event('input', { bubbles: true }));
  editableDiv.dispatchEvent(new Event('change', { bubbles: true }));
  editableDiv.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));

  // 检查发送按钮是否激活
  const sendBtn = document.querySelector('button:not([disabled])');
  const allBtns = Array.from(document.querySelectorAll('button'));
  const activeSendBtn = allBtns.find(btn => 
    btn.textContent.trim() === '发送' && !btn.disabled
  );

  if (!activeSendBtn) {
    return JSON.stringify({ 
      success: false, 
      error: '发送按钮未激活，内容可能未正确输入',
      inputContent: editableDiv.innerText
    });
  }

  // 点击发送
  activeSendBtn.click();

  // 检查是否出现身份验证弹窗
  setTimeout(() => {
    const verifyModal = document.querySelector('[class*="verify"], [class*="auth"]');
    if (verifyModal) {
      console.log('需要身份验证');
    }
  }, 500);

  return JSON.stringify({ 
    success: true, 
    message: '回复已发送',
    content: replyText
  });

})('__REPLY_TEXT__');
