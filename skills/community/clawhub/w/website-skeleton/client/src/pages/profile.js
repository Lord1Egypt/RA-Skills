/**
 * profile.js — 个人中心页
 *
 * 功能：显示用户信息（邮箱、角色、注册时间）
 * 路由：/profile
 */

import { auth, toast } from '../app.js';
import { navigate } from '../utils/router.js';
import { escapeHtml } from '../utils/escape-html.js';

export function renderProfile() {
  // 未登录提示
  if (!auth.isLoggedIn()) {
    return `
      <div class="container profile-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔒</div>
          <h3>请先登录</h3>
          <p class="text-muted">登录后查看个人中心</p>
          <a href="/login" class="btn btn-primary mt-4" data-nav>去登录</a>
        </div>
      </div>`;
  }

  const user = auth.user || {};

  return `
    <div class="container profile-page">
      <div class="profile-header">
        <div class="profile-avatar">
          <div class="avatar-placeholder">${getInitials(user.name || user.email || 'U')}</div>
        </div>
        <div class="profile-title">
          <h1>${escapeHtml(user.name || '用户')}</h1>
          <p class="text-muted">${escapeHtml(user.email || '—')}</p>
        </div>
      </div>

      <div id="profile-content">
        <div class="card profile-info-card">
          <div class="card-body">
            <h3>个人信息</h3>
            <div class="profile-info-list">
              <div class="info-row">
                <span class="info-label">邮箱</span>
                <span class="info-value">${escapeHtml(user.email || '—')}</span>
              </div>
              <div class="info-row">
                <span class="info-label">用户名</span>
                <span class="info-value">${escapeHtml(user.name || '—')}</span>
              </div>
              <div class="info-row">
                <span class="info-label">角色</span>
                <span class="info-value"><span class="role-badge">${escapeHtml(formatRole(user.role))}</span></span>
              </div>
              <div class="info-row">
                <span class="info-label">注册时间</span>
                <span class="info-value">${formatDate(user.createdAt) || '—'}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="profile-actions">
          <a href="/orders" class="btn btn-primary" data-nav>我的订单</a>
          <button class="btn btn-ghost" id="logout-btn">退出登录</button>
        </div>
      </div>
    </div>`;
}

export function attachProfileEvents() {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      if (confirm('确定退出登录？')) {
        try {
          await auth.logout();
          toast.success('已退出登录');
          navigate('/login');
        } catch {
          auth.clearSession();
          navigate('/login');
        }
      }
    });
  }
}

export const __mount = attachProfileEvents;

function getInitials(name) {
  if (!name) return 'U';
  // 取第一个字符（中文或英文首字母）
  const trimmed = name.trim();
  return trimmed.charAt(0).toUpperCase();
}

function formatRole(role) {
  const roleMap = {
    superadmin: '超级管理员',
    tenant_admin: '租户管理员',
    admin: '管理员',
    user: '普通用户',
    vip: 'VIP 用户',
  };
  return roleMap[role] || role || '未知';
}

function formatDate(dateStr) {
  if (!dateStr) return null;
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return dateStr;
  }
}
