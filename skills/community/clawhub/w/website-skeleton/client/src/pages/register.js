/**
 * register.js — 注册页面
 */

import { auth, toast } from '../app.js';
import { navigate } from '../utils/router.js';

let _submitted = false;

export function renderRegister() {
  _submitted = false;
  return `
    <div class="container auth-page">
      <div class="auth-card card">
        <div class="card-body">
          <h2 class="auth-title">注册</h2>
          <p class="text-muted auth-subtitle">创建您的账号</p>
          <form id="register-form" class="auth-form">
            <div class="form-group">
              <label for="reg-name">昵称</label>
              <input type="text" id="reg-name" name="name"
                     placeholder="请输入昵称" required autocomplete="name">
            </div>
            <div class="form-group">
              <label for="reg-email">邮箱</label>
              <input type="email" id="reg-email" name="email"
                     placeholder="请输入邮箱" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="reg-password">密码</label>
              <input type="password" id="reg-password" name="password"
                     placeholder="至少 6 位" required autocomplete="new-password"
                     minlength="6">
            </div>
            <div class="form-group">
              <label for="reg-confirm">确认密码</label>
              <input type="password" id="reg-confirm" name="confirm"
                     placeholder="再次输入密码" required autocomplete="new-password"
                     minlength="6">
            </div>
            <div id="register-error" class="form-error" style="display:none"></div>
            <button type="submit" class="btn btn-primary w-full btn-lg" id="register-btn">
              注册
            </button>
          </form>
          <p class="auth-switch">
            已有账号？
            <a href="/login" data-nav>立即登录</a>
          </p>
        </div>
      </div>
    </div>`;
}

export function attachRegisterEvents() {
  const form = document.getElementById('register-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (_submitted) return;
    _submitted = true;

    const name = form.querySelector('#reg-name').value.trim();
    const email = form.querySelector('#reg-email').value.trim();
    const password = form.querySelector('#reg-password').value;
    const confirm = form.querySelector('#reg-confirm').value;
    const errorEl = document.getElementById('register-error');
    const btn = document.getElementById('register-btn');

    // 校验
    if (!name || !email || !password || !confirm) {
      showError(errorEl, '请填写所有字段');
      _submitted = false;
      return;
    }
    if (password.length < 6) {
      showError(errorEl, '密码至少 6 位');
      _submitted = false;
      return;
    }
    if (password !== confirm) {
      showError(errorEl, '两次密码不一致');
      _submitted = false;
      return;
    }

    btn.disabled = true;
    btn.textContent = '注册中...';
    errorEl.style.display = 'none';

    try {
      await auth.register(email, password, name);
      toast.success('注册成功！请登录');
      navigate('/login');
    } catch (err) {
      showError(errorEl, err.message || '注册失败，请重试');
      _submitted = false;
      btn.disabled = false;
      btn.textContent = '注册';
    }
  });
}

export const __mount = attachRegisterEvents;

function showError(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
}
