/**
 * cart.js — 购物车页面
 *
 * 显示购物车商品列表、数量调整、总价、结算按钮
 */

import { cart, toast, auth } from '../app.js';
import { navigate } from '../utils/router.js';
import { escapeHtml } from '../utils/escape-html.js';

export function renderCart() {
  const items = cart.getCart();
  const count = cart.getCount();
  const total = cart.getTotal();

  if (count === 0) {
    return `
      <div class="container cart-page">
        <div class="empty-state" style="padding:4rem 1rem">
          <div class="empty-icon">🛒</div>
          <h3>购物车是空的</h3>
          <p class="text-muted">去挑选心仪的商品吧</p>
          <a href="/products" class="btn btn-primary mt-4" data-nav>去逛逛</a>
        </div>
      </div>`;
  }

  return `
    <div class="container cart-page">
      <div class="cart-header">
        <h1>购物车</h1>
        <span class="text-muted">共 ${count} 件商品</span>
      </div>

      <div class="cart-content">
        <div class="cart-items" id="cart-items">
          ${items.map(renderCartItem).join('')}
        </div>

        <div class="cart-summary card">
          <div class="card-body">
            <h3>订单摘要</h3>
            <div class="summary-row">
              <span>商品数量</span>
              <span>${count} 件</span>
            </div>
            <div class="summary-row total-row">
              <span>合计</span>
              <span class="summary-total">¥${total.toFixed(2)}</span>
            </div>
            <button class="btn btn-primary w-full btn-lg mt-4" id="checkout-btn">
              去结算
            </button>
            <button class="btn btn-ghost w-full mt-2" id="clear-cart-btn">
              清空购物车
            </button>
          </div>
        </div>
      </div>
    </div>`;
}

export function attachCartEvents() {
  // 数量调整
  document.querySelectorAll('[data-cart-inc]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.cartInc;
      const item = cart.getCart().find(i => i.productId === id);
      if (item) await cart.updateItem(id, item.qty + 1);
      reRenderCart();
    });
  });

  document.querySelectorAll('[data-cart-dec]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.cartDec;
      const item = cart.getCart().find(i => i.productId === id);
      if (item) await cart.updateItem(id, item.qty - 1);
      reRenderCart();
    });
  });

  document.querySelectorAll('[data-cart-remove]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.cartRemove;
      await cart.removeItem(id);
      toast.info('已移除');
      reRenderCart();
    });
  });

  // 结算
  const checkoutBtn = document.getElementById('checkout-btn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (!auth.isLoggedIn()) {
        toast.warning('请先登录');
        navigate('/login');
        return;
      }
      toast.info('结算功能开发中...');
    });
  }

  // 清空
  const clearBtn = document.getElementById('clear-cart-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', async () => {
      if (confirm('确定清空购物车？')) {
        await cart.clear();
        toast.success('购物车已清空');
        reRenderCart();
      }
    });
  }
}

export const __mount = attachCartEvents;

function renderCartItem(item) {
  const image = item.image || 'https://via.placeholder.com/80x80?text=No+Image';
  const subtotal = (item.price * item.qty).toFixed(2);

  return `
    <div class="cart-item card" data-cart-item="${item.productId}">
      <div class="cart-item-image">
        <img src="${escapeHtml(image)}" alt="${escapeHtml(item.name)}"
             onerror="this.src='https://via.placeholder.com/80x80?text=No+Image'">
      </div>
      <div class="cart-item-info">
        <h4 class="cart-item-name">${escapeHtml(item.name)}</h4>
        <p class="cart-item-price">¥${item.price.toFixed(2)}</p>
      </div>
      <div class="cart-item-qty">
        <button class="btn btn-sm btn-ghost" data-cart-dec="${item.productId}" ${item.qty <= 1 ? 'disabled' : ''}>−</button>
        <span class="qty-value">${item.qty}</span>
        <button class="btn btn-sm btn-ghost" data-cart-inc="${item.productId}">+</button>
      </div>
      <div class="cart-item-subtotal">
        <span>¥${subtotal}</span>
      </div>
      <button class="btn btn-sm btn-ghost cart-item-remove" data-cart-remove="${item.productId}" title="移除">
        ✕
      </button>
    </div>`;
}

function reRenderCart() {
  const app = document.getElementById('app');
  app.innerHTML = renderCart();
  attachCartEvents();
}
