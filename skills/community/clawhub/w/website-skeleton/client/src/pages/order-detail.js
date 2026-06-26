/**
 * order-detail.js — 订单详情页
 *
 * 功能：显示订单号、状态标签、商品列表、金额、下单时间、支付/取消操作
 * 路由：/order/:orderNo
 */

import { api } from '../services/api.js';
import { auth, toast } from '../app.js';
import { navigate } from '../utils/router.js';
import { escapeHtml } from '../utils/escape-html.js';

const STATUS_MAP = {
  pending: '待付款',
  paid: '已付款',
  shipped: '已发货',
  delivered: '已收货',
  cancelled: '已取消',
  refunded: '已退款',
};

export function renderOrderDetail(params = {}) {
  // 未登录提示
  if (!auth.isLoggedIn()) {
    return `
      <div class="container order-detail-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔒</div>
          <h3>请先登录</h3>
          <p class="text-muted">登录后查看订单详情</p>
          <a href="/login" class="btn btn-primary mt-4" data-nav>去登录</a>
        </div>
      </div>`;
  }

  const orderNo = params.orderNo || '';
  if (!orderNo) {
    return `
      <div class="container order-detail-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔍</div>
          <h3>订单号无效</h3>
          <p class="text-muted">未指定订单编号</p>
          <a href="/orders" class="btn btn-primary mt-4" data-nav>返回订单列表</a>
        </div>
      </div>`;
  }

  return `
    <div class="container order-detail-page">
      <div class="order-detail-header">
        <a href="/orders" class="btn btn-ghost btn-sm" data-nav>← 返回订单列表</a>
        <h1>订单详情</h1>
      </div>

      <div id="order-detail-content">
        <div class="empty-state" style="padding:3rem 1rem">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
    </div>`;
}

export function attachOrderDetailEvents() {
  const params = parseOrderParams();
  if (params && params.orderNo) {
    loadOrderDetail(params.orderNo);
  }
}

export const __mount = attachOrderDetailEvents;

function parseOrderParams() {
  // 从当前路径解析 orderNo
  const match = window.location.pathname.match(/\/order\/([^/]+)/);
  if (match) {
    return { orderNo: match[1] };
  }
  return null;
}

async function loadOrderDetail(orderNo) {
  const container = document.getElementById('order-detail-content');
  if (!container) return;

  try {
    const data = await api.get('/order/detail', { orderNo });
    const order = data.order || data.data || data;

    if (!order) {
      container.innerHTML = `
        <div class="empty-state" style="padding:3rem 1rem">
          <div class="empty-icon">📋</div>
          <h3>订单不存在</h3>
          <p class="text-muted">该订单可能已被删除</p>
          <a href="/orders" class="btn btn-primary mt-4" data-nav>返回订单列表</a>
        </div>`;
      return;
    }

    renderDetail(container, order);
    bindDetailEvents(order);
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state" style="padding:3rem 1rem">
        <div class="empty-icon">⚠️</div>
        <h3>加载失败</h3>
        <p class="text-muted">${escapeHtml(err.message || '请刷新重试')}</p>
        <button class="btn btn-primary mt-4" onclick="window.location.reload()">重新加载</button>
      </div>`;
  }
}

function renderDetail(container, order) {
  const statusText = STATUS_MAP[order.status] || order.status || '未知';
  const createdAt = order.createdAt
    ? new Date(order.createdAt).toLocaleString('zh-CN')
    : '—';
  const total = typeof order.total === 'number'
    ? `¥${order.total.toFixed(2)}`
    : order.total || '—';
  const items = order.items || [];

  // 操作按钮
  let actions = '';
  if (order.status === 'pending') {
    actions = `
      <button class="btn btn-primary" data-order-action="pay" data-order-id="${order.id || order.orderNo}">去支付</button>
      <button class="btn btn-ghost" data-order-action="cancel" data-order-id="${order.id || order.orderNo}">取消订单</button>`;
  } else if (order.status === 'shipped') {
    actions = `<button class="btn btn-primary" data-order-action="confirm" data-order-id="${order.id || order.orderNo}">确认收货</button>`;
  } else if (order.status === 'paid') {
    actions = `<span class="text-muted text-sm">等待发货</span>`;
  }

  container.innerHTML = `
    <div class="order-detail-card card">
      <div class="card-body">
        <div class="order-detail-info">
          <div class="info-row">
            <span class="info-label">订单号</span>
            <span class="info-value">${escapeHtml(order.orderNo || order.id || '—')}</span>
          </div>
          <div class="info-row">
            <span class="info-label">状态</span>
            <span class="info-value"><span class="order-status status-${order.status || 'unknown'}">${statusText}</span></span>
          </div>
          <div class="info-row">
            <span class="info-label">下单时间</span>
            <span class="info-value">${createdAt}</span>
          </div>
          <div class="info-row">
            <span class="info-label">支付方式</span>
            <span class="info-value">${escapeHtml(order.paymentMethod || order.payment || '—')}</span>
          </div>
          ${order.address ? `
          <div class="info-row">
            <span class="info-label">收货地址</span>
            <span class="info-value">${escapeHtml(order.address.name || '')} ${escapeHtml(order.address.phone || '')} ${escapeHtml(order.address.address || '')}</span>
          </div>` : ''}
        </div>
      </div>
    </div>

    <div class="card order-items-card">
      <div class="card-body">
        <h3>商品列表</h3>
        <div class="order-items-list">
          ${items.length > 0 ? items.map(renderOrderItem).join('') : '<p class="text-muted">无商品信息</p>'}
        </div>
        <div class="order-total-line">
          <span>合计：</span>
          <span class="order-total-amount">${total}</span>
        </div>
      </div>
    </div>

    <div class="order-detail-actions">
      ${actions}
    </div>`;
}

function bindDetailEvents(order) {
  document.querySelectorAll('[data-order-action]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const action = btn.dataset.orderAction;
      const orderId = btn.dataset.orderId;

      if (action === 'cancel') {
        if (!confirm('确定取消该订单？')) return;
        try {
          await api.post(`/orders/${orderId}/cancel`);
          toast.success('订单已取消');
          if (parseOrderParams()?.orderNo) {
            loadOrderDetail(parseOrderParams().orderNo);
          }
        } catch (err) {
          toast.error(err.message || '取消失败');
        }
      } else if (action === 'confirm') {
        try {
          await api.post(`/orders/${orderId}/confirm`);
          toast.success('已确认收货');
          if (parseOrderParams()?.orderNo) {
            loadOrderDetail(parseOrderParams().orderNo);
          }
        } catch (err) {
          toast.error(err.message || '操作失败');
        }
      } else if (action === 'pay') {
        navigate(`/orders/${orderId}/pay`);
      }
    });
  });
}

function renderOrderItem(item) {
  const price = typeof item.price === 'number' ? `¥${item.price.toFixed(2)}` : item.price;
  const image = item.image || 'https://via.placeholder.com/60x60?text=No+Image';

  return `
    <div class="order-item">
      <div class="order-item-image">
        <img src="${escapeHtml(image)}" alt="${escapeHtml(item.name || item.productName || '商品')}"
             onerror="this.src='https://via.placeholder.com/60x60?text=No+Image'">
      </div>
      <div class="order-item-info">
        <span class="order-item-name">${escapeHtml(item.name || item.productName || '商品')}</span>
        <span class="text-muted text-sm">${price} × ${item.qty || 1}</span>
      </div>
      <div class="order-item-subtotal">
        ¥${((item.price || 0) * (item.qty || 1)).toFixed(2)}
      </div>
    </div>`;
}
