# Element Plus Reference

Element Plus is an enterprise-level UI component library based on Vue 3, with a clean and neutral design language.

## Official Resources

- Website: https://element-plus.org
- GitHub: https://github.com/element-plus/element-plus
- Theme Generator: https://element-plus.org/zh-CN/theme

## Core Design Principles

- **Consistency**: Consistent with real life and user habits
- **Feedback**: Provide timely feedback on operation results through style and interaction
- **Efficiency**: Simplify processes, be clear and explicit
- **Controllability**: Users can operate and undo

## Theme Variable System

Element Plus uses CSS Variables for theme customization, prefixed with `--el-`.

```
--el-color-primary          // Primary color (default #409EFF)
--el-color-success          // Success color
--el-color-warning          // Warning color
--el-color-danger           // Danger color
--el-color-info             // Info color
--el-color-white            // White
--el-color-black            // Black
--el-bg-color               // Background color
--el-text-color-primary     // Primary text color
--el-text-color-regular     // Regular text color
--el-text-color-secondary   // Secondary text color
--el-text-color-placeholder // Placeholder text color
--el-border-color           // Border color
--el-border-radius-base     // Base border radius (4px)
--el-font-size-base         // Base font size (14px)
```

### Custom Theme

```scss
// Method 1: CSS Variables Override
:root {
  --el-color-primary: #7c3aed;
}

// Method 2: SCSS Variable Override (requires build)
$--color-primary: #7c3aed;
```

## Common Component Specifications

### Button

```vue
<el-button type="primary">Primary Button</el-button>
<el-button>Default Button</el-button>
<el-button type="success">Success Button</el-button>
<el-button type="warning">Warning Button</el-button>
<el-button type="danger">Danger Button</el-button>
<el-button type="info">Info Button</el-button>
<el-button plain>Plain Button</el-button>
<el-button text>Text Button</el-button>
<el-button size="small">Small Button</el-button>
<el-button :icon="Search" circle />
<el-button :loading="true">Loading</el-button>
```

### Form

```vue
<el-form
  ref="formRef"
  :model="formData"
  :rules="rules"
  label-width="120px"
  label-position="right"
>
  <el-form-item label="Username" prop="username">
    <el-input v-model="formData.username" />
  </el-form-item>
  <el-form-item label="Password" prop="password">
    <el-input v-model="formData.password" type="password" show-password />
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="onSubmit">Submit</el-button>
  </el-form-item>
</el-form>
```

### Table

```vue
<el-table :data="tableData" border stripe style="width: 100%">
  <el-table-column prop="date" label="Date" width="180" />
  <el-table-column prop="name" label="Name" width="180" />
  <el-table-column prop="address" label="Address" />
  <el-table-column label="Actions">
    <template #default="scope">
      <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
        Edit
      </el-button>
    </template>
  </el-table-column>
</el-table>
```

### Dialog

```vue
<el-dialog v-model="dialogVisible" title="Prompt" width="30%">
  <span>This is dialog content</span>
  <template #footer>
    <span class="dialog-footer">
      <el-button @click="dialogVisible = false">Cancel</el-button>
      <el-button type="primary" @click="onConfirm">Confirm</el-button>
    </span>
  </template>
</el-dialog>
```

## Layout System

Element Plus uses a 24-column grid system.

```vue
<el-container>
  <el-aside width="200px">Sidebar</el-aside>
  <el-container>
    <el-header>Header</el-header>
    <el-main>Main</el-main>
    <el-footer>Footer</el-footer>
  </el-container>
</el-container>

<!-- Grid layout -->
<el-row :gutter="20">
  <el-col :span="6"><div class="grid-content" /></el-col>
  <el-col :span="6"><div class="grid-content" /></el-col>
  <el-col :span="6"><div class="grid-content" /></el-col>
  <el-col :span="6"><div class="grid-content" /></el-col>
</el-row>
```

## Notes

- **Vue 3 + Composition API**: Use `<script setup>` and Composition API
- **Icons need separate installation**: `pnpm add @element-plus/icons-vue`
- **On-demand import**: Use with `unplugin-vue-components` + `unplugin-auto-import` for automatic imports
- **Internationalization**: `import zhCn from 'element-plus/dist/locale/zh-cn.mjs'`
- **Do not directly modify component internal styles**: Override via CSS Variables or custom classes
- **ElMessage/ElNotification** are functional calls, no need to declare in template
