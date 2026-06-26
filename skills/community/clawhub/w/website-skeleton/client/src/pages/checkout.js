/**
 * checkout.js — 结算页面
 *
 * 功能：显示购物车商品摘要、收货地址表单、支付方式选择、提交订单
 * 路由：/checkout
 */

import { api } from '../services/api.js';
import { auth, cart, toast } from '../app.js';
import { navigate } from '../utils/router.js';
import { escapeHtml } from '../utils/escape-html.js';

let _submitting = false;

export function renderCheckout() {
  // 未登录提示
  if (!auth.isLoggedIn()) {
    return `
      <div class="container checkout-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🔒</div>
          <h3>请先登录</h3>
          <p class="text-muted">登录后即可结算</p>
          <a href="/login" class="btn btn-primary mt-4" data-nav>去登录</a>
        </div>
      </div>`;
  }

  const items = cart.getCart();
  const count = cart.getCount();
  const total = cart.getTotal();

  if (count === 0) {
    return `
      <div class="container checkout-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🛒</div>
          <h3>购物车是空的</h3>
          <p class="text-muted">请先添加商品到购物车</p>
          <a href="/products" class="btn btn-primary mt-4" data-nav>去购物</a>
        </div>
      </div>`;
  }

  return `
    <div class="container checkout-page">
      <div class="checkout-header">
        <h1>结算</h1>
      </div>

      <div class="checkout-content">
        <div class="checkout-main">
          <!-- 商品摘要 -->
          <div class="card checkout-section">
            <div class="card-body">
              <h3>商品摘要</h3>
              <div class="checkout-items">
                ${items.map(renderCheckoutItem).join('')}
              </div>
              <div class="checkout-total-row">
                <span class="text-muted">共 ${count} 件商品</span>
                <span class="checkout-total-amount">合计：<strong>¥${total.toFixed(2)}</strong></span>
              </div>
            </div>
          </div>

          <!-- 收货地址表单 -->
          <div class="card checkout-section">
            <div class="card-body">
              <h3>收货地址</h3>
              <form id="checkout-address-form" class="checkout-form">
                <div class="form-group">
                  <label for="checkout-name">收货人姓名</label>
                  <input type="text" id="checkout-name" name="name"
                         placeholder="请输入收货人姓名" required>
                </div>
                <div class="form-group">
                  <label for="checkout-phone">联系电话</label>
                  <input type="tel" id="checkout-phone" name="phone"
                         placeholder="请输入联系电话" required>
                </div>
                <div class="form-group">
                  <label for="checkout-address">详细地址</label>
                  <textarea id="checkout-address" name="address" rows="3"
                            placeholder="请输入详细地址" required></textarea>
                </div>
              </form>
            </div>
          </div>

          <!-- 支付方式 -->
          <div class="card checkout-section">
            <div class="card-body">
              <h3>支付方式</h3>
              <div class="payment-methods" id="payment-methods">
                <label class="payment-option selected" data-payment="wechat">
                  <input type="radio" name="payment" value="wechat" checked hidden>
                  <span class="payment-icon">💚</span>
                  <span class="payment-label">微信支付</span>
                </label>
                <label class="payment-option" data-payment="alipay">
                  <input type="radio" name="payment" value="alipay" hidden>
                  <span class="payment-icon">💙</span>
                  <span class="payment-label">支付宝</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- 侧边提交栏 -->
        <div class="checkout-sidebar">
          <div class="card">
            <div class="card-body">
              <h3>订单摘要</h3>
              <div class="summary-row">
                <span>商品数量</span>
                <span>${count} 件</span>
              </div>
              <div class="summary-row">
                <span>运费</span>
                <span>免运费</span>
              </div>
              <div class="summary-row total-row">
                <span>应付总额</span>
                <span class="summary-total">¥${total.toFixed(2)}</span>
              </div>
              <button class="btn btn-primary w-full btn-lg mt-4" id="submit-order-btn">
                提交订单
              </button>
              <div id="checkout-error" class="form-error mt-2" style="display:none"></div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

export function attachCheckoutEvents() {
  _submitting = false;

  // 支付方式切换
  document.querySelectorAll('.payment-option').forEach(opt => {
    opt.addEventListener('click', () => {
      document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input[type="radio"]').checked = true;
    });
  });

  // 提交订单
  const submitBtn = document.getElementById('submit-order-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', async () => {
      if (_submitting) return;
      _submitting = true;

      const name = document.getElementById('checkout-name')?.value.trim();
      const phone = document.getElementById('checkout-phone')?.value.trim();
      const address = document.getElementById('checkout-address')?.value.trim();
      const errorEl = document.getElementById('checkout-error');

      // 校验地址
      if (!name || !phone || !address) {
        showError(errorEl, '请填写完整的收货地址');
        _submitting = false;
        return;
      }

      const selectedPayment = document.querySelector('.payment-option.selected input[type="radio"]');
      const paymentMethod = selectedPayment ? selectedPayment.value : 'wechat';

      submitBtn.disabled = true;
      submitBtn.textContent = '提交中...';
      errorEl.style.display = 'none';

      try {
        const items = cart.getCart();
        const orderData = await api.post('/order/create', {
          items: items.map(i => ({
            productId: i.productId,
            qty: i.qty,
          })),
          address: { name, phone, address },
          paymentMethod,
        });

        // 清空购物车
        await cart.clear();
        toast.success('订单提交成功！');
        navigate('/orders');
      } catch (err) {
        showError(errorEl, err.message || '提交订单失败，请重试');
        _submitting = false;
        submitBtn.disabled = false;
        submitBtn.textContent = '提交订单';
      }
    });
  }
}

export const __mount = attachCheckoutEvents;

function renderCheckoutItem(item) {
  const image = item.image || 'https://via.placeholder.com/60x60?text=No+Image';
  const subtotal = (item.price * item.qty).toFixed(2);

  return `
    <div class="checkout-item">
      <div class="checkout-item-image">
        <img src="${escapeHtml(image)}" alt="${escapeHtml(item.name)}"
             onerror="this.src='https://via.placeholder.com/60x60?text=No+Image'">
      </div>
      <div class="checkout-item-info">
        <span class="checkout-item-name">${escapeHtml(item.name)}</span>
        <span class="text-muted text-sm">×${item.qty}</span>
      </div>
      <div class="checkout-item-price">¥${subtotal}</div>
    </div>`;
}

function showError(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
}
