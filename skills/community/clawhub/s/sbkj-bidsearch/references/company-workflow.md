# 企业画像业务流程

## 接口组

- `companyProfileSummary`：企业基本信息和画像汇总；
- `companyProfileContacts`：联系人和联系电话，文档说明实际 `pageSize` 最大按 5 处理；
- `companyProfileCustomers`：合作客户项目关系，`pageSize` 实际最大按 20 处理；
- `companyProfileSuppliers`：供应商项目关系，`pageSize` 实际最大按 20 处理。

## 按需路由

| 需求 | 调用 |
| --- | --- |
| 企业基本情况 | Summary |
| 查联系方式 | Contacts |
| 查合作客户 | Customers |
| 查供应商 | Suppliers |
| 企业全面画像 | 四个接口组合调用 |

不要默认调用全部接口。企业名称作为统一查询键；分页参数按各接口上限裁剪，并在结果中说明实际页大小。

## 输出模型

```text
CompanyProfile
├── summary
├── contacts
├── customers
└── suppliers
```

企业画像中的项目关系如包含项目 ID 和发布时间，可链接到项目详情流程；无法关联时不得强行补全。
