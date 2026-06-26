# Germany Locale

## Default Language

默认输出德语。

## Style

- 使用清楚、正式度适中、适合企业软件的德语
- 按钮文案尽量短
- 提示语优先明确动作结果
- 财税类表达优先稳健和准确

## Translation Guidance

- 涉及德国电子发票官方生态时，保留官方名称和缩写：`E-Rechnung`、`XRechnung`、`ZUGFeRD`、`OZG-RE`、`ZRE`、`Peppol`。
- 如果是政府或公共部门提交场景，优先使用 `einreichen`、`übermitteln` 这类更准确的动作词，而不是宽泛的 `senden`。
- 页面与菜单项优先名词短语
- 操作按钮优先动词或固定操作短语
- 校验和错误提示要直接指出问题
- 涉及发票、税务、申报时，优先保持专业语义完整
- 当复合词过长影响 UI 时，优先拆成清楚短语，但不要改动官方标准名本身。

## Cautions

- 注意德语名词大小写
- 不要为了直译中文而生成过长复合结构
- 如果严格法定名词不明确，先给自然、稳妥、企业软件可用的表达
- `XRechnung` 是官方标准名，不要翻成解释性描述替代原名。

## Quick Examples

- `保存` -> `Speichern`
- `继续` -> `Weiter`
- `提交发票` -> `Rechnung einreichen`
- `税号不能为空` -> `Die Steuernummer darf nicht leer sein.`
- `提交 XRechnung` -> `XRechnung einreichen`
