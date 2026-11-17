# TDesign Reference

TDesign is an enterprise-level design system by Tencent, supporting multiple platforms and frameworks.

## Official Resources

- Website: https://tdesign.tencent.com
- GitHub: https://github.com/Tencent/tdesign
- Design Files (Figma): https://tdesign.tencent.com/resource

## Core Design Principles

- **Unity**: Cross-platform, cross-product design consistency
- **Openness**: Open source, community-driven
- **Inclusiveness**: Adaptable to different business scenarios and user groups
- **Efficiency**: Modular design, rapid product building

## Framework Support

TDesign provides multi-framework implementations:

| Framework | Package Name | Use Case |
|---|---|---|
| React | `tdesign-react` | Web React projects |
| Vue 3 | `tdesign-vue-next` | Web Vue 3 projects |
| Vue 2 | `tdesign-vue` | Web Vue 2 projects |
| Mobile (Vue) | `tdesign-mobile-vue` | H5 mobile |
| Mobile (React) | `tdesign-mobile-react` | H5 mobile |
| Miniprogram | `tdesign-miniprogram` | WeChat Mini Program |

## CSS Variable System

TDesign uses CSS Variables, prefixed with `--td-`.

```
--td-primary-color              // Primary color
--td-success-color              // Success color
--td-warning-color              // Warning color
--td-error-color                // Error color
--td-brand-color                // Brand color
--td-bg-color-page              // Page background color
--td-bg-color-container         // Container background color
--td-bg-color-component         // Component background color
--td-text-color-primary         // Primary text color
--td-text-color-secondary       // Secondary text color
--td-text-color-placeholder     // Placeholder text color
--td-text-color-disabled        // Disabled text color
--td-border-color               // Border color
--td-border-radius-default      // Default border radius
--td-border-radius-small        // Small border radius
--td-font-size-body             // Body font size
--td-font-size-title            // Title font size
--td-shadow-1                   // Level 1 shadow
--td-shadow-2                   // Level 2 shadow
--td-shadow-3                   // Level 3 shadow
```

### Custom Theme

```tsx
// React
import { ConfigProvider } from 'tdesign-react';

<ConfigProvider
  globalConfig={{
    classPrefix: 't',
  }}
>
  <App />
</ConfigProvider>
```

## Common Component Specifications

### Button

```tsx
// React version
<Button theme="primary">Primary Button</Button>
<Button>Default Button</Button>
<Button theme="default">Secondary Button</Button>
<Button theme="danger">Danger Button</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="dashed">Dashed Button</Button>
<Button variant="text">Text Button</Button>
<Button size="small">Small</Button>
<Button size="large">Large</Button>
<Button icon={<Icon name="search" />} />
<Button loading>Loading</Button>
<Button shape="circle" icon={<Icon name="search" />} />
<Button block>Block Button</Button>
```

```vue
<!-- Vue 3 version -->
<t-button theme="primary">Primary Button</t-button>
<t-button>Default Button</t-button>
<t-button theme="danger">Danger Button</t-button>
<t-button variant="outline">Outline Button</t-button>
<t-button icon="search" />
<t-button loading>Loading</t-button>
```

### Form

```tsx
<Form
  form={form}
  layout="vertical"
  onFinish={onSubmit}
>
  <FormItem
    label="Username"
    name="username"
    rules={[{ required: true, message: 'Please enter username' }]}
  >
    <Input placeholder="Please enter username" />
  </FormItem>
  <FormItem label="Password" name="password">
    <Input type="password" />
  </FormItem>
  <FormItem>
    <Button theme="primary" type="submit">Submit</Button>
  </FormItem>
</Form>
```

### Table

```tsx
<Table
  columns={[
    { colKey: 'name', title: 'Name', width: 120 },
    { colKey: 'age', title: 'Age', sorter: true },
    {
      colKey: 'action',
      title: 'Actions',
      cell: ({ row }) => (
        <Space>
          <Button variant="text" onClick={() => handleEdit(row)}>Edit</Button>
          <Button variant="text" theme="danger" onClick={() => handleDelete(row)}>Delete</Button>
        </Space>
      ),
    },
  ]}
  data={data}
  rowKey="id"
  pagination={{ pageSize: 10 }}
  loading={loading}
  onPageChange={handlePageChange}
/>
```

### Dialog

```tsx
<Dialog
  header="Prompt"
  visible={visible}
  onConfirm={handleOk}
  onClose={handleCancel}
  confirmBtn={{ content: 'Confirm', loading: confirmLoading }}
  cancelBtn="Cancel"
  width={520}
>
  <p>Dialog content</p>
</Dialog>

// Functional call
Dialog.confirm({
  header: 'Confirm deletion?',
  body: 'This action cannot be undone',
  onConfirm: () => deleteItem(id),
});
```

## Layout System

```tsx
import { Layout, Row, Col } from 'tdesign-react';
const { Header, Aside, Content, Footer } = Layout;

<Layout>
  <Aside>Sidebar</Aside>
  <Layout>
    <Header>Header</Header>
    <Content>Content</Content>
    <Footer>Footer</Footer>
  </Layout>
</Layout>

// Grid (24 columns)
<Row gutter={16}>
  <Col span={6}>1/4</Col>
  <Col span={6}>1/4</Col>
  <Col span={12}>1/2</Col>
</Row>
```

## Notes

- **Multi-framework selection**: Confirm the framework version the user is using and select the corresponding package
- **Icons**: TDesign icons are used via `<Icon name="icon-name" />`, no separate installation needed
- **Design resources**: Provides Figma/Sketch design file resources
- **Dark Mode**: Switch to `dark` via the `mode` prop of ConfigProvider
- **Internationalization**: `import zhConfig from 'tdesign-react/es/locale/zh_CN'` + `<ConfigProvider globalConfig={zhConfig}>`
- **TDesign's `colKey`** attribute corresponds to `dataIndex` (Ant Design style), note the distinction
- **Mobile components**: If H5 or Mini Program is needed, use the corresponding `tdesign-mobile-*` or `tdesign-miniprogram`
