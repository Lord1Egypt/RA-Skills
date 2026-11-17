---
name: wcs-add-frontend-page
description: "Add frontend pages to WCS (Warehouse Control System) applications"
tags: [domain-specific, frontend, api-integration, cli, memory-based]
version: 1.0.0
---

# WCS 新增前端页面

�?`apps/wcs`（Vue2 + Element UI + vxe-table 后台管理前端）里新增一个业务列表页面，
包含查询、表格展示、操作列（编�?更新状�?删除），可选新�?导入/导出，并接好路由与中�?英文国际化�?
这个技能的核心不是发明新写法，而是**严格复用现有页面的模�?*——因为审查者和其他开发者会按现有页面的样子来读这段代码。跳�?抄现有页�?这一步，写出来的代码会在风格、目录结构、接口调用方式上跟仓库其它部分不一致�?
## 何时缺信息要主动提问

在开始写代码之前，先确认下面几件事——它们无法从需求文字里稳妥地猜出来，猜错的成本是返工：

1. **更新/删除接口的调用方�?*：id 是拼�?URL 路径末尾（如 `/update/{id}`、`/delete/{id}`，仓库里绝大多数模块是这种），还是放�?query string，还是放进请求体？如果用户给的接口地址�?*没有**�?id 拼在路径里（比如只给�?`/xxx/update` �?`/xxx/delete`），必须�?`question` 工具向用户确认，不要自己猜——参考本仓库现有 `agvLocation`、`urlConfig`、`pouInfo` 等模块，惯例都是 id 拼在路径末尾�?2. **枚举字段的数据来�?*：字段是普通输入框，还是走 `getBatchDatadictionaryDetail` 数据字典（用户通常会明确给�?dictionary key，比�?`binTaskStatus`、`scanerNos`）�?3. 如果同名/同路径的页面、API 文件、路由或 i18n key 已经存在（包�?`git status` 里显示为"已删除但未提�?的文件），要先弄清楚�?*新建**还是**恢复/修改现有实现**，避免重复劳动或冲突。用 `git log --oneline -- <path>` �?`git show HEAD:<path>` 可以找到历史版本�?
## 工作流程

### 1. 找到并读懂参考页�?
用户通常会指定一个参考页面（例如 `binTrace/index.vue` 查询类页面，`pouInfo/index.vue` 增删改查+导入导出页面，`mlsInOutTasks/index.vue` 多操作下拉页面）。用 `Read` 工具把它们完整读一遍，同时读它们对应的 API 文件（`apps/wcs/src/api/<feature>/index.js`）�?
关注这些点：
- 页面整体结构：`updowspanel` 包了 `slot="up"`（`vxe-form` 查询条件 + 按钮）和 `slot="down"`（`vxe-toolbar` + `vxe-table` + `vxe-pager`）�?- 查询表单字段类型：纯文本�?`el-input`；多选可输入下拉�?`el-select multiple filterable allow-create` �?`el-option`；日期范围用 `el-date-picker type="datetimerange"`�?- 分页参数：请求体里附�?`SkipCount`/`MaxResultCount`（注意大写开头，是这个仓库的既有拼写习惯），而不�?`skipCount`/`maxResultCount`�?- 操作列：`el-dropdown` + `el-dropdown-menu` 里放多个 `el-dropdown-item`，每个绑 `@click.native="handleXxx(row)"`�?- 新建/编辑弹窗：一�?`el-dialog` + `vxe-form ref="editForm"` + `editRules`，靠 `dialogType`（`'add'` / `'edit'`）区分新建和编辑逻辑�?- 删除：用 `this.$confirm(...)` 弹二次确认，确认后调用删除接口�?- 导入：复�?`@/components/UploadExcel` 组件，走 `beforeUpload` �?`onSuccess` 校验 �?`onSubmitImport` 批量创建�?- 导出：调�?`export` 接口�?`blob`，用 `URL.createObjectURL` 触发浏览器下载，文件名带时间戳�?
如果需求里出现字典枚举（比�?`status`、`direction`），检查这�?dictionary key 是否已经在别的页面用过（�?`grep` �?`names: \[.*<key>.*\]`），确认拼写完全一致——这个仓库里字典 key 经常有历史遗留的"不完全规�?拼写（例�?`scanerNos` 少了一�?n），照抄比自己纠正更安全�?
### 2. 新建 API 模块

路径：`apps/wcs/src/api/<featureName>/index.js`（featureName �?camelCase，跟页面路由名对应，比如 `binTask`、`nodeGraph`）�?
统一�?`@/utils/request`，所有方法都�?`method: 'post'`（这个仓库里没有�?GET/PUT/DELETE 动词的惯例，即使语义上是删除也用 POST）：

```js
import request from '@/utils/request'

export function get<Feature>s(params) {
  return request({
    url: '/api/wcs/<backend-path>/getList',
    method: 'post',
    data: params
  })
}

export function create<Feature>(params) {
  return request({
    url: '/api/wcs/<backend-path>/create',
    method: 'post',
    data: params
  })
}

export function update<Feature>(id, params) {
  return request({
    url: `/api/wcs/<backend-path>/update/${id}`,
    method: 'post',
    data: params
  })
}

export function delete<Feature>(id) {
  return request({
    url: `/api/wcs/<backend-path>/delete/${id}`,
    method: 'post'
  })
}

export function batchCreate<Feature>s(params) {
  return request({
    url: '/api/wcs/<backend-path>/batch-create',
    method: 'post',
    data: params
  })
}

export function export<Feature>s(params) {
  return request({
    url: '/api/wcs/<backend-path>/export',
    method: 'post',
    data: params,
    responseType: 'blob'
  })
}
```

只暴露需求里实际要用到的方法——不要因�?参考页面全都有"就把新建/导入/导出也加上，如果用户只要查询+更新+删除�?
### 3. 新建页面组件

路径：`apps/wcs/src/views/awcs/<featureName>/index.vue`�?
组件骨架直接照抄参考页面，然后按需求改�?- `name` 用大驼峰（`BinTask`、`NodeGraph`）�?- `searchform` 字段跟后端查询参数一一对应；日期范围类页面记得�?`created()` 里默认填最�?N 天（参�?`binTrace`：`moment(nowTime - offsetTimeEnd).format('YYYY-MM-DDT00:00:00')`）�?- 表格列：接口返回字段里除�?`id`，全部展示；枚举字段用一�?`changeText(val, arr, label, value)` helper 把值翻译成 label 显示�?- 弹窗表单字段�?`vxe-form-item` + `field` �?`editRules` 里的校验规则�?- 所有异步操作都要有 loading 态（`editLoading`/`loading`）和成功/失败�?`this.$message` 提示�?
写完后用 `Read` 工具通读一次，确认�?- import 路径、函数名跟第 2 步新建的 API 模块一致�?- 没有遗留没用到的 import（比如没有导入功能就�?import `UploadExcel`）�?- `<style lang="scss" scoped> @import '@/styles/elform.scss'; </style>` 别漏�?
### 4. 注册路由

编辑 `apps/wcs/src/router/modules/businessManagement.js`，在 `children` 数组里靠近同类页面的位置插入一段：

```js
{
  path: '<featureName>',
  component: () => import('@/views/awcs/<featureName>/index'),
  name: '<FeatureName>',
  meta: {
    title: 'route.<featureName>',
    icon: 'el-icon-s-order',
    policy: 'AbpDataDictionary.Default',
    noCache: false
  }
},
```

�?`Edit` 工具做定点插�?不要整段重写文件——这个文件里有大量被注释掉的历史路由，直接重写容易误删�?
### 5. 配置国际�?
编辑 `apps/wcs/src/lang/zh.js`，在 `route: { ... }` 对象里加一行：

```js
<featureName>: '<中文页面标题>',
```

同时检�?`apps/wcs/src/lang/en.js` 是否有同�?`route` 对象；如果这个仓库对同类页面保持了中英文同步（多数情况是这样），顺手补一条英文翻译，保持两个文件�?key 集合一致，即使用户没有明确要求——避免以后英文语言包缺 key �?undefined�?
�?`Edit` 工具做定点插入，插在语义相近的已�?key 旁边（比如放在同一�?新增功能路由"分割线附近），不要另起一段孤立的新分组�?
### 6. 收尾检�?
- �?`grep` 确认新建�?api 函数名、路�?name、i18n key 在全仓库范围内没有跟别的模块重名冲突�?- 如果本地能跑 eslint（依赖装好的情况下）执行一�?lint；如果因�?`eslint-plugin-vue` 缺失等环境问题跑不起来，说明是环境问题，改用 `Read` 工具通读改动文件做人工二次核对代替�?- �?`git status` / `git diff` 过一遍最终改动，确认没有意外改坏无关代码（尤其是路由文件里那一大段注释掉的历史路由要保持原样）�?- 简要总结新建的文件列表、路�?path/name、i18n key，回复用户�?
## 常见�?
- **分页字段大小�?*：这个仓库的分页参数�?`SkipCount`/`MaxResultCount`（大写开头），不是常见的 `skipCount`/`maxResultCount`；照抄参考页面即可，不要�?OpenAPI 文档里的小写字段名去写�?- **删除接口也是 POST**：不要因为语义是删除就写 `method: 'delete'`�?- **不要重复造字�?key**：新枚举字段如果没有现成 dictionary key，如实告诉用�?这个字段没有走字典，前端只是原样展示/输入"，不要凭空发明一个字�?key 名称�?- **路由文件里大量注释代�?*：那是历史遗留，插入新路由时保持它们不动，只在合适的位置追加�?- **同名文件可能已存在于 git 历史但被删除**：先�?`git status` 看有没有相关文件�?`deleted` 状态，�?`git log --oneline -- <path>` 查历史，避免把别人已经做过的实现当成全新需求重新写一遍、风格却对不上�?