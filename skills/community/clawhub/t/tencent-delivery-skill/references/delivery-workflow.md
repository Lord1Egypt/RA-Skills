<a id="delivery-main-flow"></a>
# 📦 跑腿下单主流程

调 `state next` 获取当前状态和该读的子文档，按状态干活。

| current_state | 子文档 |
|---------------|--------|
| `step1-sender-address` / `step1-sender-contact` | [step-1-sender.md](./delivery/step-1-sender.md) |
| `step2-receiver-address` / `step2-receiver-contact` | [step-2-receiver.md](./delivery/step-2-receiver.md) |
| `step3-estimate` | [step-3-estimate.md](./delivery/step-3-estimate.md) |
| `step4-select` | [step-4-select.md](./delivery/step-4-select.md) |
| `step5-book` | [step-5-book.md](./delivery/step-5-book.md) |
| `step6-payment` | [step-6-payment.md](./delivery/step-6-payment.md) |
| `step7-confirm` | [step-7-confirm.md](./delivery/step-7-confirm.md) |
| `has-order` | [order-workflow.md](./order-workflow.md) |

<a id="delivery-exit-flow"></a>
## 用户中途退出

用户说"算了/不寄了/退出"：
- 已有 orderCode → 转 [取消流程](./order-workflow.md#order-cancel-flow)
- 否则 → `state clear` + 回复：

```markdown
好的，已为您退出当前下单流程，未产生任何订单。

需要继续时直接告诉我，例如「帮我从公司寄个文件到XX」。
```
