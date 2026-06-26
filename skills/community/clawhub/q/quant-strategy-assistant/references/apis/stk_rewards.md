# `stk_rewards` 接口文档

## 接口说明

- 中文说明：管理层薪酬和持股
- 动态方法：`pro.stk_rewards(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ts_code`, `end_date`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `name`, `title`, `reward`, `hold_vol`

## 调用示例

```python
df = pro.stk_rewards(
    ts_code="",
    end_date="",
    fields="ts_code,ann_date,end_date,name,title,reward,hold_vol",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
