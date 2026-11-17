# Arco Design Reference

Arco Design is an enterprise-level design system and React component library by ByteDance.

## Official Resources

- Website: https://arco.design
- GitHub: https://github.com/arco-design/arco-design
- Theme Store: https://arco.design/themes

## Core Design Principles

- **Clarity**: Clear information hierarchy, reducing cognitive load
- **Efficiency**: Simplify operation paths, improve efficiency
- **Consistency**: Unified interaction and visual language
- **Aesthetics**: Modern, restrained, quality visual style

## CSS Variable System

Arco Design uses CSS Variables for theme customization, with a 10-level color scale system (from light to dark).

```
--color-primary-1         // Primary light (background/hover)
--color-primary-6         // Primary color (default)
--color-primary-7         // Primary dark (active)
--color-success-6         // Success color
--color-warning-6         // Warning color
--color-danger-6          // Danger color
--color-bg-1              // Deepest background (inside container)
--color-bg-2              // Default background (page)
--color-bg-3              // Light background (card)
--color-bg-4              // Lightest background (overlay)
--color-text-1            // Primary text
--color-text-2            // Secondary text
--color-text-3            // Disabled text
--color-border-1          // Border
--color-border-2          // Divider
--border-radius-small     // Small radius (2px)
--border-radius-medium    // Medium radius (4px)
--border-radius-large     // Large radius (8px)
```

### Custom Theme

```tsx
import { ConfigProvider } from '@arco-design/web-react';

<ConfigProvider
  theme={{
    primaryColor: '#165DFF',
  }}
>
  <App />
</ConfigProvider>
```

## Common Component Specifications

### Button

```tsx
<Button type="primary">Primary Button</Button>
<Button>Default Button</Button>
<Button type="secondary">Secondary Button</Button>
<Button type="outline">Outline Button</Button>
<Button type="dashed">Dashed Button</Button>
<Button type="text">Text Button</Button>
<Button status="success">Success</Button>
<Button status="warning">Warning</Button>
<Button status="danger">Danger</Button>
<Button size="mini">Mini</Button>
<Button size="small">Small</Button>
<Button size="large">Large</Button>
<Button icon={<IconSearch />} />
<Button loading>Loading</Button>
<Button shape="circle" icon={<IconSearch />} />
<Button long>Long Button</Button>
```

### Form

```tsx
<Form
  form={form}
  layout="vertical"
  onSubmit={onSubmit}
  scrollToFirstError
>
  <Form.Item
    label="Username"
    field="username"
    rules={[{ required: true, message: 'Please enter username' }]}
  >
    <Input placeholder="Please enter username" />
  </Form.Item>
  <Form.Item label="Password" field="password">
    <Input.Password />
  </Form.Item>
  <Form.Item>
    <Button type="primary" htmlType="submit" long>Submit</Button>
  </Form.Item>
</Form>
```

### Table

```tsx
<Table
  columns={[
    { title: 'Name', dataIndex: 'name' },
    { title: 'Age', dataIndex: 'age', sorter: true },
    {
      title: 'Actions',
      render: (_, record) => (
        <Space>
          <Button type="text" onClick={() => handleEdit(record)}>Edit</Button>
          <Button type="text" status="danger" onClick={() => handleDelete(record)}>Delete</Button>
        </Space>
      ),
    },
  ]}
  data={data}
  rowKey="id"
  pagination={{ pageSize: 10, showTotal: true }}
  loading={loading}
  onChange={handleChange}
  border={{ wrapper: true, cell: true }}
/>
```

### Modal

```tsx
<Modal
  title="Prompt"
  visible={visible}
  onOk={handleOk}
  onCancel={handleCancel}
  confirmLoading={loading}
  okText="Confirm"
  cancelText="Cancel"
  style={{ width: 520 }}
>
  <p>Modal content</p>
</Modal>

// Functional call
Modal.confirm({
  title: 'Confirm deletion?',
  content: 'This action cannot be undone',
  onOk: () => deleteItem(id),
});
```

## Layout System

```tsx
import { Layout, Grid } from '@arco-design/web-react';
const { Header, Sider, Content, Footer } = Layout;
const { Row, Col } = Grid;

<Layout style={{ height: '100vh' }}>
  <Sider width={200}>Sidebar</Sider>
  <Layout>
    <Header>Header</Header>
    <Content>Content</Content>
    <Footer>Footer</Footer>
  </Layout>
</Layout>

// Grid (24 columns)
<Row gutter={[16, 16]}>
  <Col span={6}>1/4</Col>
  <Col span={12}>1/2</Col>
  <Col span={6}>1/4</Col>
</Row>
```

## Notes

- **Arco Design 2.x** is the current major version; 1.x is no longer maintained
- **Icons** are built into `@arco-design/web-react/icon`, no separate installation needed
- **Theme Editor**: Provides visual theme editing tool, can export theme packages
- **Dark Mode**: Switch to `dark` via the `theme` prop of `ConfigProvider`
- **On-demand loading**: Tree Shaking supported by default, no additional configuration needed
- **Internationalization**: `import enUS from '@arco-design/web-react/es/locale/en-US'`
- **Do not use CSS Modules to directly override**: Arco class names include hashes; customize via ConfigProvider or custom className
- **Material-style asset platform**: https://arco.design/material provides business components and templates
