/**
 * products.js — 商品列表页
 *
 * 功能：商品网格展示、分页、分类筛选
 */

import { api } from '../services/api.js';
import { cart, toast } from '../app.js';
import { escapeHtml } from '../utils/escape-html.js';
import { PAGE_SIZE } from '../utils/constants.js';

let _currentPage = 1;
let _currentCategory = '';
let _searchQuery = '';

export function renderProducts(params = {}) {
  _currentPage = parseInt(params.page || params.page, 10) || 1;
  _currentCategory = params.category || '';
  _searchQuery = params.q || '';

  return `
    <div class="container products-page">
      <div class="products-header">
        <h1>全部商品</h1>
        <div class="products-controls">
          <input type="search" id="product-search" class="products-search"
                 placeholder="搜索商品..." value="${escapeHtml(_searchQuery)}">
          <select id="product-category" class="products-category">
            <option value="">全部分类</option>
            <option value="electronics" ${_currentCategory === 'electronics' ? 'selected' : ''}>电子产品</option>
            <option value="clothing" ${_currentCategory === 'clothing' ? 'selected' : ''}>服装</option>
            <option value="books" ${_currentCategory === 'books' ? 'selected' : ''}>图书</option>
            <option value="home" ${_currentCategory === 'home' ? 'selected' : ''}>家居</option>
            <option value="sports" ${_currentCategory === 'sports' ? 'selected' : ''}>运动</option>
          </select>
        </div>
      </div>

      <div id="products-grid" class="grid grid-4">
        <div class="empty-state" style="grid-column:1/-1">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      </div>

      <div id="products-pagination" class="pagination"></div>
    </div>`;
}

export function attachProductsEvents() {
  const searchInput = document.getElementById('product-search');
  const categorySelect = document.getElementById('product-category');

  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        _searchQuery = searchInput.value.trim();
        _currentPage = 1;
        loadProducts();
      }, 400);
    });
  }

  if (categorySelect) {
    categorySelect.addEventListener('change', () => {
      _currentCategory = categorySelect.value;
      _currentPage = 1;
      loadProducts();
    });
  }

  loadProducts();
}

export const __mount = attachProductsEvents;

async function loadProducts() {
  const grid = document.getElementById('products-grid');
  const pagination = document.getElementById('products-pagination');
  if (!grid) return;

  grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">
    <div class="spinner"></div>
    <p>加载中...</p>
  </div>`;

  try {
    const data = await api.get('/products/list', {
      page: _currentPage,
      pageSize: PAGE_SIZE,
      category: _currentCategory || undefined,
      q: _searchQuery || undefined,
    });

    const products = data.items || data.products || data.data || [];
    const total = data.total || products.length;

    if (products.length === 0) {
      grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">
        <div class="empty-icon">📦</div>
        <h3>暂无商品</h3>
        <p class="text-muted">换个筛选条件试试</p>
      </div>`;
    } else {
      grid.innerHTML = products.map(renderProductCard).join('');
    }

    // 分页
    const totalPages = Math.ceil(total / PAGE_SIZE);
    if (totalPages > 1) {
      pagination.innerHTML = renderPagination(_currentPage, totalPages);
      bindPaginationEvents();
    } else {
      pagination.innerHTML = '';
    }

    // 绑定加入购物车事件
    grid.querySelectorAll('[data-add-to-cart]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const productId = btn.dataset.addToCart;
        btn.disabled = true;
        btn.textContent = '加入中...';
        try {
          await cart.addItem(productId, 1);
          toast.success('已加入购物车');
        } catch (err) {
          toast.error('加入失败: ' + (err.message || '请重试'));
        }
        btn.disabled = false;
        btn.textContent = '加入购物车';
      });
    });
  } catch (err) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">
      <div class="empty-icon">⚠️</div>
      <h3>加载失败</h3>
      <p class="text-muted">${escapeHtml(err.message || '请刷新重试')}</p>
      <button class="btn btn-primary mt-2" onclick="window.location.reload()">重新加载</button>
    </div>`;
  }
}

function renderProductCard(product) {
  const price = typeof product.price === 'number'
    ? `¥${product.price.toFixed(2)}`
    : product.price;
  const image = product.image || 'https://via.placeholder.com/200x200?text=No+Image';
  const stockClass = product.stock > 0 ? '' : 'out-of-stock';

  return `
    <div class="card product-card ${stockClass}">
      <div class="product-image">
        <img src="${escapeHtml(image)}" alt="${escapeHtml(product.name)}" loading="lazy"
             onerror="this.src='https://via.placeholder.com/200x200?text=No+Image'">
      </div>
      <div class="card-body">
        <h3 class="product-name">${escapeHtml(product.name)}</h3>
        <p class="product-price">${price}</p>
        <p class="text-muted text-sm">${escapeHtml(product.category || '')}</p>
        ${product.stock > 0
          ? `<button class="btn btn-sm btn-primary w-full mt-2" data-add-to-cart="${product.id}">加入购物车</button>`
          : `<button class="btn btn-sm btn-secondary w-full mt-2" disabled>暂时缺货</button>`
        }
      </div>
    </div>`;
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

function bindPaginationEvents() {
  document.querySelectorAll('#products-pagination [data-page]').forEach(btn => {
    btn.addEventListener('click', () => {
      const page = parseInt(btn.dataset.page, 10);
      if (page > 0) {
        _currentPage = page;
        loadProducts();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });
}
