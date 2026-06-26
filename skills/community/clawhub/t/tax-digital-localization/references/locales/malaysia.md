# Malaysia Locale

## Default Language

默认输出马来语。

## Style

- 使用标准、清楚、适合企业软件的马来语
- 按钮优先短动词
- 页面和菜单名称保持稳定、易扫读
- 提示语避免冗长和宣传腔

## Translation Guidance

- 保留马来西亚官方生态中的系统名和品牌名，不要翻译或改写：`e-Invois`、`MyInvois`、`MyInvois e-POS`、`HASiL`、`LHDN`。
- 涉及税号时，首次可写 `Nombor Pengenalan Cukai (TIN)`；后续优先沿用 `TIN`。
- 操作按钮优先使用常见产品用语
- 提示语要清楚说明失败原因或下一步动作
- 发票与税务相关文案优先准确，不用口语化表达
- 如果中文是中性系统文案，目标文案也保持中性
- 如果界面直接承接 MyInvois API 或官方状态值，保留 `Submitted`、`Valid`、`Invalid`、`Cancelled` 等官方英文状态；一般用户提示语再用自然马来语解释。

## Cautions

- 不要混入随意英语，除非用户明确要求英语界面
- 不要使用俚语或过度口语化表达
- 不要为了逐字对应而让句子失去产品可读性
- 对外显示文案可以是马来语，但官方系统名、字段缩写和状态枚举要以官方写法为准。

## Quick Examples

- `保存` -> `Simpan`
- `继续` -> `Teruskan`
- `提交发票` -> `Hantar e-Invois`
- `税号不能为空` -> `Nombor cukai tidak boleh kosong`
- `前往 MyInvois` -> `Pergi ke MyInvois`
