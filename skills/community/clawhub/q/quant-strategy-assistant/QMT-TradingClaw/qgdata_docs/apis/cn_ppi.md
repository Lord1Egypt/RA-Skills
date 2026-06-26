# `cn_ppi` 接口文档

## 接口说明

- 中文说明：工业品出厂价格指数(PPI)
- 动态方法：`pro.cn_ppi(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`month`, `ppi_yoy`, `ppi_mp_yoy`, `ppi_mp_qm_yoy`, `ppi_mp_rm_yoy`, `ppi_mp_p_yoy`, `ppi_cg_yoy`, `ppi_cg_f_yoy`

## 调用示例

```python
df = pro.cn_ppi(
    fields="month,ppi_yoy,ppi_mp_yoy,ppi_mp_qm_yoy,ppi_mp_rm_yoy,ppi_mp_p_yoy,ppi_cg_yoy,ppi_cg_f_yoy",
    order_by="month",
    sort="desc",
    limit=50,
)
```
