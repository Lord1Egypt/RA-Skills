/**
 * admin/products.js — 管理后台商品管理
 *
 * 功能：商品表格（名称、价格、库存、状态、操作）、新增/编辑/删除 CRUD
 * 路由：/admin/products
 * 权限：admin
 */

import { api } from '../../services/api.js';
import { auth, toast } from '../../app.js';
import { escapeHtml } from '../../utils/escape-html.js';
import { PAGE_SIZE } from '../../utils/constants.js';

let _currentPage = 1;
let _editingProduct = null; // null = 新增模式，对象 = 编辑模式

export function renderAdminProducts() {
  // 权限检查
  if (!auth.isLoggedIn() || !isAdmin(auth.user?.role)) {
    return renderNoPermission();
  }

  return `
    <div class="admin-page admin-products-page">
      <div class="admin-header">
        <h1>商品管理</h1>
        <button class="btn btn-primary" id="add-product-btn">+ 新增商品</button>
      </div>

      <div class="card admin-table-card">
        <div class="card-body">
          <div id="admin-products-table">
            <div class="empty-state" style="padding:2rem">
              <div class="spinner"></div>
              <p>加载中...</p>
            </div>
          </div>
          <div id="admin-products-pagination" class="pagination mt-3"></div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑商品模态框 -->
    <div class="modal-overlay" id="product-modal" style="display:none">
      <div class="modal card">
        <div class="card-body">
          <h3 id="product-modal-title">新增商品</h3>
          <form id="product-form" class="product-form">
            <div class="form-group">
              <label for="product-name">商品名称</label>
              <input type="text" id="product-name" name="name" required>
            </div>
            <div class="form-group">
              <label for="product-price">价格</label>
              <input type="number" id="product-price" name="price" step="0.01" min="0" required>
            </div>
            <div class="form-group">
              <label for="product-stock">库存</label>
              <input type="number" id="product-stock" name="stock" min="0" required>
            </div>
            <div class="form-group">
              <label for="product-category">分类</label>
              <select id="product-category" name="category">
                <option value="electronics">电子产品</option>
                <option value="clothing">服装</option>
                <option value="books">图书</option>
                <option value="home">家居</option>
                <option value="sports">运动</option>
              </select>
            </div>
            <div class="form-group">
              <label for="product-image">图片链接</label>
              <input type="url" id="product-image" name="image" placeholder="https://...">
            </div>
            <div class="form-group">
              <label for="product-status">状态</label>
              <select id="product-status" name="status">
                <option value="active">上架</option>
                <option value="inactive">下架</option>
              </select>
            </div>
            <div id="product-form-error" class="form-error" style="display:none"></div>
            <div class="modal-actions">
              <button type="button" class="btn btn-ghost" id="product-modal-cancel">取消</button>
              <button type="submit" class="btn btn-primary" id="product-modal-submit">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 删除确认模态框 -->
    <div class="modal-overlay" id="delete-modal" style="display:none">
      <div class="modal card modal-sm">
        <div class="card-body">
          <h3>确认删除</h3>
          <p class="text-muted mt-2" id="delete-modal-text">确定要删除该商品吗？此操作不可撤销。</p>
          <div id="delete-form-error" class="form-error" style="display:none"></div>
          <div class="modal-actions">
            <button type="button" class="btn btn-ghost" id="delete-modal-cancel">取消</button>
            <button type="button" class="btn btn-danger" id="delete-modal-confirm">确认删除</button>
          </div>
        </div>
      </div>
    </div>`;
}

export function attachAdminProductsEvents() {
  _currentPage = 1;
  loadProducts();

  // 新增按钮
  const addBtn = document.getElementById('add-product-btn');
  if (addBtn) {
    addBtn.addEventListener('click', () => {
      _editingProduct = null;
      openProductModal(null);
    });
  }

  // 模态框取消
  const cancelBtn = document.getElementById('product-modal-cancel');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', closeProductModal);
  }

  // 模态框表单提交
  const form = document.getElementById('product-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await saveProduct();
    });
  }

  // 删除模态框
  const deleteCancel = document.getElementById('delete-modal-cancel');
  if (deleteCancel) {
    deleteCancel.addEventListener('click', closeDeleteModal);
  }

  const deleteConfirm = document.getElementById('delete-modal-confirm');
  if (deleteConfirm) {
    deleteConfirm.addEventListener('click', confirmDelete);
  }

  // 点击模态框外部关闭
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.style.display = 'none';
      }
    });
  });
}

export const __mount = attachAdminProductsEvents;

async function loadProducts() {
  const container = document.getElementById('admin-products-table');
  const pagination = document.getElementById('admin-products-pagination');
  if (!container) return;

  container.innerHTML = `
    <div class="empty-state" style="padding:2rem">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>`;

  try {
    const data = await api.get('/admin/products', { page: _currentPage, pageSize: PAGE_SIZE });
    const products = data.items || data.products || data.data || [];
    const total = data.total || products.length;

    if (products.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="padding:2rem">
          <div class="empty-icon">📦</div>
          <h3>暂无商品</h3>
          <p class="text-muted">点击上方"新增商品"添加</p>
        </div>`;
      pagination.innerHTML = '';
      return;
    }

    container.innerHTML = `
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th>名称</th>
              <th>分类</th>
              <th>价格</th>
              <th>库存</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${products.map(renderProductRow).join('')}
          </tbody>
        </table>
      </div>`;

    // 绑定操作按钮事件
    container.querySelectorAll('[data-admin-product-edit]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.adminProductEdit;
        const product = products.find(p => String(p.id) === String(id));
        if (product) {
          _editingProduct = product;
          openProductModal(product);
        }
      });
    });

    container.querySelectorAll('[data-admin-product-delete]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.adminProductDelete;
        openDeleteModal(id);
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
            loadProducts();
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

function renderProductRow(product) {
  const price = typeof product.price === 'number' ? `¥${product.price.toFixed(2)}` : product.price;
  const statusText = product.status === 'active' ? '上架' : '下架';
  const statusClass = product.status === 'active' ? 'status-active' : 'status-inactive';

  return `
    <tr>
      <td>${escapeHtml(product.name || '—')}</td>
      <td>${escapeHtml(product.category || '—')}</td>
      <td>${price}</td>
      <td>${product.stock ?? '—'}</td>
      <td><span class="status-badge ${statusClass}">${statusText}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-ghost" data-admin-product-edit="${product.id}">编辑</button>
        <button class="btn btn-sm btn-ghost text-danger" data-admin-product-delete="${product.id}">删除</button>
      </td>
    </tr>`;
}

function openProductModal(product) {
  const modal = document.getElementById('product-modal');
  const title = document.getElementById('product-modal-title');
  const submitBtn = document.getElementById('product-modal-submit');
  const errorEl = document.getElementById('product-form-error');
  if (!modal) return;

  errorEl.style.display = 'none';

  if (product) {
    title.textContent = '编辑商品';
    submitBtn.textContent = '保存修改';
    document.getElementById('product-name').value = product.name || '';
    document.getElementById('product-price').value = product.price || '';
    document.getElementById('product-stock').value = product.stock || 0;
    document.getElementById('product-category').value = product.category || 'electronics';
    document.getElementById('product-image').value = product.image || '';
    document.getElementById('product-status').value = product.status || 'active';
  } else {
    title.textContent = '新增商品';
    submitBtn.textContent = '保存';
    document.getElementById('product-form').reset();
    document.getElementById('product-status').value = 'active';
  }

  modal.style.display = 'flex';
}

function closeProductModal() {
  const modal = document.getElementById('product-modal');
  if (modal) modal.style.display = 'none';
}

async function saveProduct() {
  const name = document.getElementById('product-name')?.value.trim();
  const price = parseFloat(document.getElementById('product-price')?.value);
  const stock = parseInt(document.getElementById('product-stock')?.value, 10);
  const category = document.getElementById('product-category')?.value;
  const image = document.getElementById('product-image')?.value.trim();
  const status = document.getElementById('product-status')?.value;
  const errorEl = document.getElementById('product-form-error');
  const submitBtn = document.getElementById('product-modal-submit');

  if (!errorEl || !submitBtn) return;

  // 校验
  if (!name) {
    errorEl.textContent = '请输入商品名称';
    errorEl.style.display = 'block';
    return;
  }
  if (isNaN(price) || price < 0) {
    errorEl.textContent = '请输入有效的价格';
    errorEl.style.display = 'block';
    return;
  }
  if (isNaN(stock) || stock < 0) {
    errorEl.textContent = '请输入有效的库存数量';
    errorEl.style.display = 'block';
    return;
  }

  errorEl.style.display = 'none';
  submitBtn.disabled = true;
  submitBtn.textContent = '保存中...';

  try {
    const payload = { name, price, stock, category, image, status };

    if (_editingProduct) {
      await api.put(`/admin/products/${_editingProduct.id}`, payload);
      toast.success('商品已更新');
    } else {
      await api.post('/admin/products', payload);
      toast.success('商品已创建');
    }

    closeProductModal();
    loadProducts();
  } catch (err) {
    errorEl.textContent = err.message || '操作失败';
    errorEl.style.display = 'block';
    submitBtn.disabled = false;
    submitBtn.textContent = _editingProduct ? '保存修改' : '保存';
  }
}

let _deleteProductId = null;

function openDeleteModal(productId) {
  _deleteProductId = productId;
  const modal = document.getElementById('delete-modal');
  if (modal) modal.style.display = 'flex';
}

function closeDeleteModal() {
  _deleteProductId = null;
  const modal = document.getElementById('delete-modal');
  if (modal) modal.style.display = 'none';
}

async function confirmDelete() {
  if (!_deleteProductId) return;

  const errorEl = document.getElementById('delete-form-error');
  const confirmBtn = document.getElementById('delete-modal-confirm');
  if (!errorEl || !confirmBtn) return;

  errorEl.style.display = 'none';
  confirmBtn.disabled = true;
  confirmBtn.textContent = '删除中...';

  try {
    await api.del(`/admin/products/${_deleteProductId}`);
    toast.success('商品已删除');
    closeDeleteModal();
    loadProducts();
  } catch (err) {
    errorEl.textContent = err.message || '删除失败';
    errorEl.style.display = 'block';
    confirmBtn.disabled = false;
    confirmBtn.textContent = '确认删除';
  }
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
