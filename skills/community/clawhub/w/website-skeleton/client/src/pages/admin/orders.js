/**
 * admin/orders.js — 管理后台订单管理
 *
 * 功能：订单表格（订单号、用户、金额、状态、操作）、状态筛选、分页
 * 路由：/admin/orders
 * 权限：admin
 */

import { api } from '../../services/api.js';
import { auth, toast } from '../../app.js';
import { escapeHtml } from '../../utils/escape-html.js';
import { PAGE_SIZE } from '../../utils/constants.js';

const STATUS_MAP = {
  pending: '待付款',
  paid: '已付款',
  shipped: '已发货',
  delivered: '已收货',
  cancelled: '已取消',
  refunded: '已退款',
};

let _currentPage = 1;
let _currentStatus = '';

export function renderAdminOrders() {
  // 权限检查
  if (!auth.isLoggedIn() || !isAdmin(auth.user?.role)) {
    return renderNoPermission();
  }

  return `
    <div class="admin-page admin-orders-page">
      <div class="admin-header">
        <h1>订单管理</h1>
        <div class="admin-filters">
          <select id="order-status-filter" class="form-select">
            <option value="">全部状态</option>
            <option value="pending">待付款</option>
            <option value="paid">已付款</option>
            <option value="shipped">已发货</option>
            <option value="delivered">已收货</option>
            <option value="cancelled">已取消</option>
            <option value="refunded">已退款</option>
          </select>
        </div>
      </div>

      <div class="card admin-table-card">
        <div class="card-body">
          <div id="admin-orders-table">
            <div class="empty-state" style="padding:2rem">
              <div class="spinner"></div>
              <p>加载中...</p>
            </div>
          </div>
          <div id="admin-orders-pagination" class="pagination mt-3"></div>
        </div>
      </div>
    </div>`;
}

export function attachAdminOrdersEvents() {
  _currentPage = 1;
  _currentStatus = '';

  loadOrders();

  // 状态筛选
  const filter = document.getElementById('order-status-filter');
  if (filter) {
    filter.addEventListener('change', () => {
      _currentStatus = filter.value;
      _currentPage = 1;
      loadOrders();
    });
  }
}

export const __mount = attachAdminOrdersEvents;

async function loadOrders() {
  const container = document.getElementById('admin-orders-table');
  const pagination = document.getElementById('admin-orders-pagination');
  if (!container) return;

  container.innerHTML = `
    <div class="empty-state" style="padding:2rem">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>`;

  try {
    const params = { page: _currentPage, pageSize: PAGE_SIZE };
    if (_currentStatus) params.status = _currentStatus;

    const data = await api.get('/admin/orders', params);
    const orders = data.orders || data.items || data.data || [];
    const total = data.total || data.totalCount || orders.length;

    if (orders.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="padding:2rem">
          <div class="empty-icon">📋</div>
          <h3>暂无订单</h3>
          <p class="text-muted">${_currentStatus ? '没有匹配状态的订单' : '还没有任何订单'}</p>
        </div>`;
      pagination.innerHTML = '';
      return;
    }

    container.innerHTML = `
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>用户</th>
              <th>商品数</th>
              <th>金额</th>
              <th>状态</th>
              <th>下单时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${orders.map(renderOrderRow).join('')}
          </tbody>
        </table>
      </div>`;

    // 绑定操作按钮事件
    container.querySelectorAll('[data-admin-order-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const action = btn.dataset.adminOrderAction;
        const orderId = btn.dataset.adminOrderId;

        if (action === 'ship') {
          if (!confirm('确认发货？')) return;
          try {
            await api.post(`/admin/orders/${orderId}/ship`);
            toast.success('已标记为发货');
            loadOrders();
          } catch (err) {
            toast.error(err.message || '操作失败');
          }
        } else if (action === 'cancel') {
          if (!confirm('确认取消该订单？')) return;
          try {
            await api.post(`/admin/orders/${orderId}/cancel`);
            toast.success('订单已取消');
            loadOrders();
          } catch (err) {
            toast.error(err.message || '操作失败');
          }
        } else if (action === 'refund') {
          if (!confirm('确认退款？')) return;
          try {
            await api.post(`/admin/orders/${orderId}/refund`);
            toast.success('已退款');
            loadOrders();
          } catch (err) {
            toast.error(err.message || '操作失败');
          }
        }
      });
    });

    // 分页
    const totalPages = Math.ceil(total / PAGE_SIZE);
    if (totalPages > 1) {
      pagination.innerHTML = renderPagination(_currentPage, totalPages);
      pagination.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', () => {
          const page = parseInt(btn.dataset.page, 10);
          if (page > 0 && page <= totalPages) {
            _currentPage = page;
            loadOrders();
          }
        });
      });
    } else {
      pagination.innerHTML = '';
    }
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state" style="padding:2rem">
        <div class="empty-icon">⚠️</div>
        <h3>加载失败</h3>
        <p class="text-muted">${escapeHtml(err.message || '请刷新重试')}</p>
        <button class="btn btn-primary mt-2" onclick="window.location.reload()">重新加载</button>
      </div>`;
  }
}

function renderOrderRow(order) {
  const statusText = STATUS_MAP[order.status] || order.status || '未知';
  const total = typeof order.total === 'number' ? `¥${order.total.toFixed(2)}` : order.total || '—';
  const itemCount = (order.items || []).reduce((sum, i) => sum + (i.qty || 1), 0);
  const date = order.createdAt
    ? new Date(order.createdAt).toLocaleString('zh-CN')
    : '—';
  const userName = order.user?.name || order.userName || order.user?.email || '—';

  // 操作按钮（根据状态）
  let actions = '';
  if (order.status === 'paid') {
    actions = `<button class="btn btn-sm btn-primary" data-admin-order-action="ship" data-admin-order-id="${order.id || order.orderNo}">发货</button>`;
  } else if (order.status === 'pending') {
    actions = `<button class="btn btn-sm btn-ghost text-danger" data-admin-order-action="cancel" data-admin-order-id="${order.id || order.orderNo}">取消</button>`;
  } else if (order.status === 'shipped') {
    actions = `<span class="text-muted text-sm">已发货</span>`;
  } else if (order.status === 'delivered') {
    actions = `<button class="btn btn-sm btn-ghost" data-admin-order-action="refund" data-admin-order-id="${order.id || order.orderNo}">退款</button>`;
  } else {
    actions = `<span class="text-muted text-sm">—</span>`;
  }

  return `
    <tr>
      <td class="order-no">${escapeHtml(order.orderNo || order.id || '—')}</td>
      <td>${escapeHtml(userName)}</td>
      <td>${itemCount}</td>
      <td class="order-total">${total}</td>
      <td><span class="status-badge status-${order.status || 'unknown'}">${statusText}</span></td>
      <td class="order-date">${date}</td>
      <td class="table-actions">${actions}</td>
    </tr>`;
}

function renderPagination(current, total) {
  let html = '<div class="pagination-inner">';
  html += `<button class="btn btn-sm btn-secondary" data-page="${current - 1}" ${current <= 1 ? 'disabled' : ''}>上一页</button>`;
  for (let i = 1; i <= total; i++) {
    if (i === current) {
      html += `<button class="btn btn-sm btn-primary" disabled>${i}</button>`;
    } else if (i === 1 || i === total || Math.abs(i - current) <= 2) {
      html += `<button class="btn btn-sm btn-secondary" data-page="${i}">${i}</button>`;
    } else if (Math.abs(i - current) === 3) {
      html += `<span class="pagination-ellipsis">...</span>`;
    }
  }
  html += `<button class="btn btn-sm btn-secondary" data-page="${current + 1}" ${current >= total ? 'disabled' : ''}>下一页</button>`;
  html += '</div>';
  return html;
}

function isAdmin(role) {
  return role === 'superadmin' || role === 'tenant_admin' || role === 'admin';
}

function renderNoPermission() {
  return `
    <div class="container" style="padding:4rem 1rem;text-align:center">
      <div style="font-size:3rem;margin-bottom:1rem">🔒</div>
      <h3>无权访问</h3>
      <p class="text-muted">您没有管理后台的访问权限</p>
      <a href="/" class="btn btn-primary mt-4" data-nav>返回首页</a>
    </div>`;
}
