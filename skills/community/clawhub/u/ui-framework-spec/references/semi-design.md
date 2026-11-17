# Semi Design Reference

Semi Design is an enterprise-level UI design system and React component library by the Douyin frontend team.

## Official Resources

- Website: https://semi.design
- GitHub: https://github.com/DouyinFE/semi-design
- Design Files (Figma): https://semi.design/figma

## Core Design Principles

- **Content Immersion**: Content first, UI serves the content
- **Information Density**: Optimized for high information density scenarios
- **High Performance**: Rendering optimization for large data volumes
- **Consistent but Not Monotonous**: Flexible and variable themes

## Dual Token System

Semi Design supports both CSS Variables and JavaScript Design Token.

```
--semi-color-primary            // Primary color
--semi-color-success            // Success color
--semi-color-warning            // Warning color
--semi-color-danger             // Danger color
--semi-color-bg-0               // Page background
--semi-color-bg-1               // Container background
--semi-color-bg-2               // Overlay background
--semi-color-bg-3               // Modal background
--semi-color-text-0             // Primary text
--semi-color-text-1             // Secondary text
--semi-color-text-2             // Auxiliary text
--semi-color-text-3             // Disabled text
--semi-color-border             // Border
--semi-color-fill-0             // Fill color (hover)
--semi-color-fill-1             // Fill color (default)
--semi-color-fill-2             // Fill color (disabled)
--semi-border-radius-extra-small // Extra small radius (3px)
--semi-border-radius-small       // Small radius (6px)
--semi-border-radius-medium      // Medium radius (10px)
--semi-border-radius-large       // Large radius (14px)
--semi-font-family-regular       // Body font
--semi-font-family-mono          // Monospace font
--semi-shadow-elevated           // Elevated shadow
```

### Custom Theme

```tsx
import { ConfigProvider } from '@douyinfe/semi-ui';

<ConfigProvider
  theme={{
    primaryColor: '#5b8bff',
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
<Button type="warning">Warning Button</Button>
<Button type="danger">Danger Button</Button>
<Button type="tertiary">Tertiary Button</Button>
<Button size="small">Small</Button>
<Button size="large">Large</Button>
<Button icon={<IconSearch />} />
<Button loading>Loading</Button>
<Button block>Block Button</Button>
<Button theme="solid">Solid (default)</Button>
<Button theme="light">Light Fill</Button>
<Button theme="borderless">Borderless</Button>
```

### Form

```tsx
<Form
  onSubmit={values => handleSubmit(values)}
  layout="vertical"
  labelPosition="top"
>
  <Form.Input
    field="username"
    label="Username"
    placeholder="Please enter username"
    rules={[{ required: true, message: 'Please enter username' }]}
  />
  <Form.Input
    field="password"
    label="Password"
    mode="password"
  />
  <Form.Select
    field="role"
    label="Role"
    options={[
      { value: 'admin', label: 'Admin' },
      { value: 'user', label: 'User' },
    ]}
  />
  <Button type="primary" htmlType="submit" block>Submit</Button>
</Form>
```

### Table

```tsx
<Table
  columns={[
    { title: 'Name', dataIndex: 'name', width: 150 },
    { title: 'Age', dataIndex: 'age', sorter: true },
    {
      title: 'Actions',
      dataIndex: 'action',
      render: (_, record) => (
        <Space>
          <Button type="tertiary" size="small" onClick={() => handleEdit(record)}>Edit</Button>
          <Button type="danger" size="small" onClick={() => handleDelete(record)}>Delete</Button>
        </Space>
      ),
    },
  ]}
  dataSource={data}
  rowKey="id"
  pagination={{ pageSize: 10 }}
  loading={loading}
  onChange={handleChange}
  virtualized={data.length > 100}
/>
```

### Modal

```tsx
<Modal
  title="Prompt"
  visible={visible}
  onOK={handleOk}
  onCancel={handleCancel}
  confirmLoading={loading}
  okText="Confirm"
  cancelText="Cancel"
  width={520}
  maskClosable={false}
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
import { Layout, Row, Col } from '@douyinfe/semi-ui';
const { Header, Sider, Content, Footer } = Layout;

<Layout>
  <Sider>Sidebar</Sider>
  <Layout>
    <Header>Header</Header>
    <Content>Content</Content>
    <Footer>Footer</Footer>
  </Layout>
</Layout>

// Grid (24 columns)
<Row type="flex" gutter={[16, 16]}>
  <Col span={6}>1/4</Col>
  <Col span={12}>1/2</Col>
  <Col span={6}>1/4</Col>
</Row>
```

## Special Components

Semi Design has unique optimization components for content-dense scenarios:

- **Navigation**: Side navigation bar, supports multi-level expand/collapse
- **NavItem**: Used with Navigation
- **SideSheet**: Side panel modal
- **TreeSelect**: Tree selector
- **Cascader**: Cascade selector
- **Rating**: Rating
- **Slider**: Slider
- **Transfer**: Transfer box
- **AvatarGroup**: Avatar group
- **Banner**: Banner notification
- **Toast**: Lightweight notification (wrapped as `Toast.info/warning/error/success`)

## Notes

- **Icons** need separate installation: `pnpm add @douyinfe/semi-icons`
- **Semi's Form component** provides quick-field components (`Form.Input`, `Form.Select`, etc.), no need to manually combine FormItem + Input
- **Virtualization**: Table component has built-in virtual scrolling; set `virtualized` for large datasets
- **Internationalization**: `import zh_CN from '@douyinfe/semi-ui/locale/source/zh_CN'` + `<ConfigProvider locale={zh_CN}>`
- **SSR Support**: Semi supports Next.js, requires configuring `semi-webpack-plugin` (or Vite plugin)
- **D2C Capability**: Semi provides a tool to convert Figma design files to code (Semi D2C), can generate Semi component code directly from design files
- **Do not override internal variables prefixed with `--semi-`**, customize through `ConfigProvider`'s `theme` instead
