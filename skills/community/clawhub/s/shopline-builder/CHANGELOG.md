# Changelog — shopline-builder

## v2.0.0 (2026-03-16)

### 重大更新

#### 🌐 浏览器模式（三种 profile）
- 新增「零、浏览器模式选择」章节，明确三种 profile 的适用场景：
  - `openclaw`：注册新账号（隔离模式，无需登录态）
  - `user`：已有账号的后台操作（Chrome DevTools MCP 附加，保留完整登录态）
  - `chrome-relay`：Chrome 扩展中转流程
- 所有后台操作步骤（Step A/B/C/D + 搬迁链路）统一加入 `profile="user"` 标注

#### ⚡ 浏览器自动化升级（OpenClaw 2026.3.13 新特性）
- 多个顺序操作合并为批量调用（`request=[]`），减少往返延迟
- 新增 `selector` 精准定位支持，补充 ref 不稳定的场景
- 新增 `delayMs` 延迟点击，处理页面动画/React 状态同步问题
- 注册流程 Step 1-5 批量化：填字段+点下一步合并为单次调用

#### 🔄 搬迁链路（Shopify 新版授权）完整验证
- Shopify 授权方式更新为新版（Client ID + Secret，从 Dev Dashboard 获取）
- 新增完整的用户引导话术（5步操作指引）
- 进入搬迁插件改为签名 URL 方式（解决跨域 session 问题）
- 补充 checkbox 坐标点击方法（Vue 自定义组件，JS click 无效）
- 补充订单模块依赖关系：必须先勾选商品+客户+折扣码
- 已验证实际搬迁数据：475商品、847订单、242客户成功迁移

### 技术规则新增
- `input` 字段填写 index 映射：index 0 隐藏，1=handle，2=ClientID，3=Secret
- 签名 URL 有效期约 30 分钟
- 模块选择 checkbox 用 `._moduleName_2weus_5` class + `elementFromPoint` 坐标点击
- Secret 格式为 `shpss_...`（新版），非旧版 `shpat_...`

### Bug 修复
- 修正商品添加页 URL：`/admin/products/new`（旧文档误写为 `/add`）
- 修正 Step A 装修路径：从 Online Store → Design 导航（不能直接访问 `/admin/themes`）

---

## v1.0.0 (2026-03-13)

### 首次发布

#### 新手建站链路（Sprint 1 完成）
- 6步注册表单全自动（Step 1-6）
- Step A：AI Website Builder 自动建站（品类选择 + 描述生成 + Classic 风格发布）
- Step B：AI 自动生成商品并上架（Unsplash 图片 + native value setter 填库存）
- Step C：支付配置（COD 全自动；PayPal/SHOPLINE Payments 引导用户手动）
- Step D：物流配置（US Domestic $5.99 + International $14.99 全自动）

#### 搬迁链路（插件安装已验证）
- Multi-platform Store Migration 插件安装流程（含跨域 session 处理）
- 支持 Shopify、WooCommerce、Shoplazza

#### 技术规则
- React controlled input：必须用 native value setter + dispatchEvent
- 库存字段 index：input[placeholder="Please enter"] 第4个（index=3）
- 图片库选图：evaluate 遍历父级找 item/card 容器点击
- 运费 spinbutton 格式：`$ 5.99`（带空格和$）
