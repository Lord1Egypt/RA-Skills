/**
 * product-detail.js — 商品详情页
 *
 * 路由：/products/:id
 * 功能：展示商品图片、名称、价格、描述、库存、加入购物车
 */

import { api } from '../services/api.js';
import { auth, cart } from '../app.js';
import { navigate } from '../utils/router.js';
import { escapeHtml } from '../utils/escape-html.js';

export function renderProductDetail(params) {
  const id = params?.id;
  if (!id) return renderError('缺少商品 ID');

  const app = document.getElementById('app');
  if (!app) return '';

  app.innerHTML = `
    <div class="container" style="padding-top:2rem;padding-bottom:3rem;">
      <div id="product-detail-loading" style="text-align:center;padding:4rem 0;">
        <div class="spinner"></div>
        <p class="text-muted mt-4">加载中...</p>
      </div>
      <div id="product-detail-content" style="display:none;"></div>
    </div>
  `;

  loadProduct(id);
  return '';
}

async function loadProduct(id) {
  try {
    const data = await api.get(`/products/${encodeURIComponent(id)}`);
    const product = data.product || data;
    renderProduct(product);
  } catch (err) {
    document.getElementById('product-detail-loading').style.display = 'none';
    const content = document.getElementById('product-detail-content');
    content.style.display = 'block';
    content.innerHTML = renderError('商品加载失败，请稍后重试');
  }
}

function renderProduct(product) {
  const loading = document.getElementById('product-detail-loading');
  const content = document.getElementById('product-detail-content');
  if (!loading || !content) return;

  loading.style.display = 'none';
  content.style.display = 'block';

  const isLoggedIn = auth.isLoggedIn();
  const inStock = product.stock > 0;
  const stockLabel = inStock ? `库存 ${product.stock} 件` : '暂时缺货';

  content.innerHTML = `
    <nav style="font-size:0.875rem;color:var(--text-muted);margin-bottom:1.5rem;">
      <a href="/products" data-nav style="color:var(--primary);">商品</a>
      <span style="margin:0 0.5rem;">›</span>
      <span>${escapeHtml(product.name || '')}</span>
    </nav>

    <div class="grid grid-2" style="gap:2rem;">
      <!-- 商品图片 -->
      <div>
        <div class="card" style="overflow:hidden;">
          <div style="aspect-ratio:1;display:flex;align-items:center;justify-content:center;
                      background:var(--bg-secondary);font-size:4rem;">
            ${product.image_url ? `<img src="${escapeHtml(product.image_url)}" alt="${escapeHtml(product.name)}"
              style="width:100%;height:100%;object-fit:cover;">` : '📦'}
          </div>
        </div>
      </div>

      <!-- 商品信息 -->
      <div>
        <h1 style="font-size:1.75rem;margin-bottom:0.5rem;">${escapeHtml(product.name || '')}</h1>
        ${product.category_name ? `<p class="text-sm text-muted" style="margin-bottom:1rem;">分类：${escapeHtml(product.category_name)}</p>` : ''}

        <div style="font-size:2rem;font-weight:800;color:var(--error);margin-bottom:1.5rem;">
          ¥${Number(product.price || 0).toFixed(2)}
        </div>

        <p class="text-muted" style="margin-bottom:1.5rem;line-height:1.8;">
          ${escapeHtml(product.description || '暂无描述')}
        </p>

        <div class="flex items-center gap-4" style="margin-bottom:1.5rem;">
          <span class="text-sm" style="color:${inStock ? 'var(--success)' : 'var(--text-muted)'};">
            ${inStock ? '●' : '○'} ${stockLabel}
          </span>
        </div>

        <!-- 数量选择 -->
        <div class="flex items-center gap-3" style="margin-bottom:2rem;">
          <span class="text-sm font-bold">数量：</span>
          <button class="btn btn-sm btn-secondary" id="qty-minus" ${!inStock ? 'disabled' : ''}>−</button>
          <span id="qty-display" style="min-width:2rem;text-align:center;font-weight:700;">1</span>
          <button class="btn btn-sm btn-secondary" id="qty-plus" ${!inStock ? 'disabled' : ''}>+</button>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-3" style="flex-wrap:wrap;">
          <button class="btn btn-primary btn-lg" id="btn-add-cart" ${!inStock ? 'disabled' : ''}>
            🛒 加入购物车
          </button>
          ${!isLoggedIn ? '<p class="text-sm text-muted" style="margin-top:0.5rem;">请先 <a href="/login" data-nav>登录</a> 后购买</p>' : ''}
        </div>

        <div id="detail-message" style="margin-top:1rem;"></div>
      </div>
    </div>
  `;

  // 数量控制
  let qty = 1;
  const qtyDisplay = document.getElementById('qty-display');
  const qtyMinus = document.getElementById('qty-minus');
  const qtyPlus = document.getElementById('qty-plus');
  const addCartBtn = document.getElementById('btn-add-cart');
  const msgDiv = document.getElementById('detail-message');

  qtyMinus?.addEventListener('click', () => {
    if (qty > 1) { qty--; qtyDisplay.textContent = qty; }
  });
  qtyPlus?.addEventListener('click', () => {
    if (qty < product.stock) { qty++; qtyDisplay.textContent = qty; }
  });
  addCartBtn?.addEventListener('click', async () => {
    try {
      await cart.addItem(product.id || product._id, qty);
      msgDiv.innerHTML = '<p style="color:var(--success);font-weight:600;">✅ 已加入购物车</p>';
      setTimeout(() => msgDiv.innerHTML = '', 2000);
    } catch (err) {
      msgDiv.innerHTML = '<p style="color:var(--error);">加入购物车失败，请重试</p>';
    }
  });
}

function renderError(msg) {
  return `
    <div class="container" style="text-align:center;padding:4rem 0;">
      <div style="font-size:3rem;margin-bottom:1rem;">😕</div>
      <h3>${escapeHtml(msg)}</h3>
      <a href="/products" class="btn btn-primary mt-6" data-nav>返回商品列表</a>
    </div>
  `;
}
