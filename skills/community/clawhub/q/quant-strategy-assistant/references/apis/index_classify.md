# `index_classify` 接口文档

## 接口说明

- 中文说明：申万行业分类
- 动态方法：`pro.index_classify(...)`
- 典型过滤参数：`src`(必填)
- 主要字段：`index_code`, `industry_name`, `parent_code`, `level`, `industry_code`, `is_pub`, `src`

## 调用示例

```python
df = pro.index_classify(
    src="SW2021",
    fields="index_code,industry_name,parent_code,level,industry_code,is_pub,src",
    limit=50,
)
```
