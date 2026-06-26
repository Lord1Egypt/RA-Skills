# 发码工具 · 管理员内部用

## 用途

用户付款后，生成激活码发过去。

## 使用

```bash
# 月卡（M），到期 2026-12-31
python scripts/gen-license.py M 20261231

# 单次（S），不限时（随便填一个远期）
python scripts/gen-license.py S 20991231

# Pro（P），到期 2026-05-31
python scripts/gen-license.py P 20260531
```

## 输出示例

```
M-20261231-a81cb97e
```

复制发给用户，用户执行：
```bash
set RR_LICENSE_KEY=M-20261231-a81cb97e
```

## 安全性

- HMAC Secret 默认 `openclaw-resume-rocket-2026`（在 `lib/license.py`）
- **不要把 secret 改了然后 publish**，否则老用户激活码全失效
- 如果 secret 泄漏：全网老激活码都能被伪造 → 只能升级 secret + 重发所有用户

## 订单台账

记录在 `biz/orders.csv`，字段：`日期,金额,档位,用户联系方式,激活码,激活日期`
