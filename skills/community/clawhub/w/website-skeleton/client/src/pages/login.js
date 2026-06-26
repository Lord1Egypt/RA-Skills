/**
 * login.js — 登录页面
 */

import { auth, toast } from '../app.js';
import { navigate } from '../utils/router.js';

let _submitted = false;

export function renderLogin() {
  _submitted = false;
  return `
    <div class="container auth-page">
      <div class="auth-card card">
        <div class="card-body">
          <h2 class="auth-title">登录</h2>
          <p class="text-muted auth-subtitle">欢迎回来</p>
          <form id="login-form" class="auth-form">
            <div class="form-group">
              <label for="login-email">邮箱</label>
              <input type="email" id="login-email" name="email"
                     placeholder="请输入邮箱" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="login-password">密码</label>
              <input type="password" id="login-password" name="password"
                     placeholder="请输入密码" required autocomplete="current-password"
                     minlength="6">
            </div>
            <div id="login-error" class="form-error" style="display:none"></div>
            <button type="submit" class="btn btn-primary w-full btn-lg" id="login-btn">
              登录
            </button>
          </form>
          <p class="auth-switch">
            还没有账号？
            <a href="/register" data-nav>立即注册</a>
          </p>
        </div>
      </div>
    </div>`;
}

/**
 * 绑定登录表单事件（在 router.render 后由页面自行调用）
 * 本模板采用即时绑定的方式：
 *   router 渲染后自动调用 attachLoginEvents()
 */
export function attachLoginEvents() {
  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (_submitted) return;
    _submitted = true;

    const email = form.querySelector('#login-email').value.trim();
    const password = form.querySelector('#login-password').value;
    const errorEl = document.getElementById('login-error');
    const btn = document.getElementById('login-btn');

    // 前端校验
    if (!email || !password) {
      showError(errorEl, '请填写邮箱和密码');
      _submitted = false;
      return;
    }

    btn.disabled = true;
    btn.textContent = '登录中...';
    errorEl.style.display = 'none';

    try {
      await auth.login(email, password);
      toast.success('登录成功！');
      navigate('/');
    } catch (err) {
      showError(errorEl, err.message || '登录失败，请重试');
      _submitted = false;
      btn.disabled = false;
      btn.textContent = '登录';
    }
  });
}

// 简易的 mount 机制：导出供 router 在渲染后调用
// router 渲染页面后，如果页面有 attachXxxEvents 则自动调用
export const __mount = attachLoginEvents;

function showError(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
}
