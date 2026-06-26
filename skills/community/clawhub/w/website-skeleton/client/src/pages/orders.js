/**
 * orders.js — 订单列表页
 *
 * 展示用户的历史订单，表格显示。
 */

import { api } from '../services/api.js';
import { escapeHtml } from '../utils/escape-html.js';
import { auth, toast } from '../app.js';
import { navigate } from '../utils/router.js';

const STATUS_MAP = {
  pending: '待付款',
  paid: '已付款',
  shipped: '已发货',
  delivered: '已收货',
  cancelled: '已取消',
  refunded: '已退款',
};

export function renderOrders() {
  // 未登录提示
  if (!auth.isLoggedIn()) {
    return `
      <div class="container orders-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔒</div>
          <h3>请先登录</h3>
          <p class="text-muted">登录后查看您的订单</p>
          <a href="/login" class="btn btn-primary mt-4" data-nav>去登录</a>
        </div>
      </div>`;
  }

  return `
    <div class="container orders-page">
      <div class="orders-header">
        <h1>我的订单</h1>
      </div>
      <div id="orders-list">
        <div class="empty-state" style="padding:3rem 1rem">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
    </div>`;
}

export function attachOrdersEvents() {
  loadOrders();
}

export const __mount = attachOrdersEvents;

async function loadOrders() {
  const container = document.getElementById('orders-list');
  if (!container) return;

  try {
    const data = await api.get('/orders');
    const orders = data.orders || data.items || data.data || [];

    if (orders.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="padding:3rem 1rem">
          <div class="empty-icon">📋</div>
          <h3>暂无订单</h3>
          <p class="text-muted">去选购一些商品吧</p>
          <a href="/products" class="btn btn-primary mt-4" data-nav>去购物</a>
        </div>`;
      return;
    }

    container.innerHTML = `
      <div class="orders-table-wrapper">
        <table class="orders-table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>商品</th>
              <th>金额</th>
              <th>状态</th>
              <th>日期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${orders.map(renderOrderRow).join('')}
          </tbody>
        </table>
      </div>`;

    // 绑定操作按钮事件
    container.querySelectorAll('[data-order-action]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const { orderAction: action, orderId } = btn.dataset;
        if (action === 'cancel') {
          if (!confirm('确定取消该订单？')) return;
          try {
            await api.post(`/orders/${orderId}/cancel`);
            toast.success('订单已取消');
            loadOrders();
          } catch (err) {
            toast.error(err.message || '取消失败');
          }
        } else if (action === 'confirm') {
          try {
            await api.post(`/orders/${orderId}/confirm`);
            toast.success('已确认收货');
            loadOrders();
          } catch (err) {
            toast.error(err.message || '操作失败');
          }
        } else if (action === 'pay') {
          navigate(`/orders/${orderId}/pay`);
        }
      });
    });
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state" style="padding:3rem 1rem">
        <div class="empty-icon">⚠️</div>
        <h3>加载失败</h3>
        <p class="text-muted">${escapeHtml(err.message || '请刷新重试')}</p>
      </div>`;
  }
}

function renderOrderRow(order) {
  const statusText = STATUS_MAP[order.status] || order.status;
  const date = order.createdAt
    ? new Date(order.createdAt).toLocaleDateString('zh-CN')
    : '—';
  const total = typeof order.total === 'number'
    ? `¥${order.total.toFixed(2)}`
    : order.total;

  const itemNames = (order.items || [])
    .slice(0, 3)
    .map(i => i.name || i.productName || '商品')
    .join('、');
  const more = (order.items || []).length > 3 ? ` 等${order.items.length}件` : '';

  // 操作按钮
  let actions = '';
  if (order.status === 'pending') {
    actions = `
      <button class="btn btn-sm btn-primary" data-order-action="pay" data-order-id="${order.id}">去支付</button>
      <button class="btn btn-sm btn-ghost" data-order-action="cancel" data-order-id="${order.id}">取消</button>`;
  } else if (order.status === 'shipped') {
    actions = `<button class="btn btn-sm btn-primary" data-order-action="confirm" data-order-id="${order.id}">确认收货</button>`;
  } else {
    actions = `<span class="text-muted text-sm">—</span>`;
  }

  return `
    <tr>
      <td class="order-no">${escapeHtml(order.orderNo || order.id || '—')}</td>
      <td class="order-items">${escapeHtml(itemNames)}${more}</td>
      <td class="order-total">${total}</td>
      <td><span class="order-status status-${order.status || 'unknown'}">${statusText}</span></td>
      <td class="order-date">${date}</td>
      <td class="order-actions">${actions}</td>
    </tr>`;
}
