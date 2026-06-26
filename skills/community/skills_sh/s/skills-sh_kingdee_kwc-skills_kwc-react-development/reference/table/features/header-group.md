# 表头分组

通过在 `columns` 配置中使用 `children` 属性，可以将多个列归入同一个父级表头下，实现多级表头分组效果。父级列只需设置 `title` 和 `children`，无需 `dataIndex`。

## 基础用法

```jsx
import React from "react";
import SlTable from "@kdcloudjs/shoelace/dist/react/table/index.js";

const columns = [
  { title: "姓名", dataIndex: "name", width: 120 },
  {
    title: "基本信息",
    dataIndex: "info",
    children: [
      { title: "年龄", dataIndex: "age", width: 100 },
      { title: "性别", dataIndex: "gender", width: 100 },
    ],
  },
  {
    title: "联系方式",
    dataIndex: "contact",
    children: [
      { title: "电话", dataIndex: "phone", width: 150 },
      { title: "邮箱", dataIndex: "email", width: 200 },
    ],
  },
  { title: "地址", dataIndex: "address" },
];

const dataSource = [
  {
    id: "1",
    name: "张三",
    age: 32,
    gender: "男",
    phone: "13800000001",
    email: "zhangsan@example.com",
    address: "北京市朝阳区",
  },
  {
    id: "2",
    name: "李四",
    age: 28,
    gender: "女",
    phone: "13800000002",
    email: "lisi@example.com",
    address: "上海市浦东新区",
  },
  {
    id: "3",
    name: "王五",
    age: 35,
    gender: "男",
    phone: "13800000003",
    email: "wangwu@example.com",
    address: "广州市天河区",
  },
];

export default () => (
  <SlTable rowKey="id" columns={columns} dataSource={dataSource} bordered />
);
```

## 多级嵌套

`children` 支持多层嵌套，实现三级甚至更深层的表头分组：

```jsx
const columns = [
  { title: "姓名", dataIndex: "name", width: 120 },
  {
    title: "工作信息",
    children: [
      { title: "部门", dataIndex: "department", width: 120 },
      {
        title: "薪资明细",
        children: [
          { title: "基本工资", dataIndex: "baseSalary", width: 120 },
          { title: "绩效奖金", dataIndex: "bonus", width: 120 },
        ],
      },
    ],
  },
];
```

## 注意事项

- 父级列（含 `children` 的列）不需要设置 `dataIndex`，只需设置 `title`
- 只有叶子列（无 `children` 的列）才会渲染数据单元格
- 建议配合 `bordered` 使用，分组边界更清晰
- 表头分组可与排序、筛选、固定列等功能组合使用，功能配置在叶子列上设置即可
