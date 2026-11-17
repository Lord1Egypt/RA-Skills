# Ant Design Reference

Ant Design is an enterprise-level UI design language and React component library by Ant Group.

## Official Resources

- Website: https://ant.design
- GitHub: https://github.com/ant-design/ant-design
- ProComponents: https://procomponents.ant.design

## Core Design Values

- **Natural**: Interaction behavior meets user expectations
- **Certain**: Consistent and predictable design language
- **Meaningful**: Every design decision has a purpose
- **Growing**: Flexible and extensible, adaptable to different businesses

## Design Token System

Ant Design 5.x uses a CSS-in-JS Design Token mechanism.

```tsx
// Global Token
import { ConfigProvider } from 'antd';

const theme = {
  token: {
    colorPrimary: '#1677ff',
    borderRadius: 6,
    colorBgContainer: '#f6f8fa',
    fontSize: 14,
    controlHeight: 32,
  },
};

<ConfigProvider theme={theme}>
  <App />
</ConfigProvider>
```

### Common Tokens

```
colorPrimary          // Brand primary color
colorSuccess          // Success color
colorWarning          // Warning color
colorError            // Error color
colorInfo             // Info color
colorBgContainer      // Container background color
colorBgLayout         // Layout background color
colorText             // Text color
colorBorder           // Border color
borderRadius          // Border radius
fontSize              // Font size
controlHeight         // Control height
boxShadow             // Box shadow
```

## Common Component Specifications

### Button

```tsx
<Button type="primary">Primary Button</Button>
<Button>Default Button</Button>
<Button type="dashed">Dashed Button</Button>
<Button type="text">Text Button</Button>
<Button type="link">Link Button</Button>
<Button danger>Danger Button</Button>
<Button size="small">Small</Button>
<Button icon={<SearchOutlined />} />
<Button loading>Loading</Button>
<Button shape="circle" icon={<SearchOutlined />} />
```

### Form

```tsx
<Form
  form={form}
  layout="vertical"
  onFinish={onSubmit}
  initialValues={{}}
>
  <Form.Item
    label="Username"
    name="username"
    rules={[{ required: true, message: 'Please enter username' }]}
  >
    <Input placeholder="Please enter username" />
  </Form.Item>
  <Form.Item
    label="Password"
    name="password"
    rules={[{ required: true }]}
  >
    <Input.Password />
  </Form.Item>
  <Form.Item>
    <Button type="primary" htmlType="submit">Submit</Button>
  </Form.Item>
</Form>
```

### Table

```tsx
<Table
  columns={[
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Age', dataIndex: 'age', key: 'age', sorter: true },
    {
      title: 'Actions',
      key: 'action',
      render: (_, record) => (
        <Space>
          <a onClick={() => handleEdit(record)}>Edit</a>
          <a onClick={() => handleDelete(record)}>Delete</a>
        </Space>
      ),
    },
  ]}
  dataSource={data}
  rowKey="id"
  pagination={{ pageSize: 10 }}
  loading={loading}
  onChange={handleTableChange}
/>
```

### Modal

```tsx
<Modal
  title="Prompt"
  open={visible}
  onOk={handleOk}
  onCancel={handleCancel}
  confirmLoading={confirmLoading}
  width={520}
>
  <p>This is modal content</p>
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
import { Layout, Row, Col } from 'antd';
const { Header, Sider, Content, Footer } = Layout;

<Layout style={{ minHeight: '100vh' }}>
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
  <Col span={6}>1/4</Col>
  <Col span={12}>1/2</Col>
</Row>
```

## Notes

- **Ant Design 5.x** uses CSS-in-JS (cssinjs), no extra CSS file import needed
- **Icons** need separate installation: `pnpm add @ant-design/icons`
- **App component**: 5.x recommends wrapping the app with `<App>` to enable static methods of message/notification/modal
- **ProComponents**: Advanced business component library, includes ProTable, ProForm, ProLayout, etc.
- **Internationalization**: `import zhCN from 'antd/locale/zh_CN'` + `<ConfigProvider locale={zhCN}>`
- **Do not use `!important`** to override styles; use Token or `className` for customization
- **antd 4.x to 5.x**: Removed less variables, fully uses Design Token
- **SSR**: antd 5.x supports Next.js App Router, but requires StyleProvider configuration
