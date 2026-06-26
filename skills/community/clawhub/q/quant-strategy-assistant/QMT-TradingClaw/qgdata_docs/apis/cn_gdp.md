# `cn_gdp` 接口文档

## 接口说明

- 中文说明：中国GDP数据
- 动态方法：`pro.cn_gdp(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`quarter`, `gdp`, `gdp_yoy`, `pi`, `pi_yoy`, `si`, `si_yoy`, `ti`

## 调用示例

```python
df = pro.cn_gdp(
    fields="quarter,gdp,gdp_yoy,pi,pi_yoy,si,si_yoy,ti",
    order_by="quarter",
    sort="desc",
    limit=50,
)
```
