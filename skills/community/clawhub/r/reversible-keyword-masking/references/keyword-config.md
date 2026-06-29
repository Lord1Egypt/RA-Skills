# RKM Keyword Configuration

Use a YAML file to describe manually supplied sensitive terms and regex patterns.

## Manual Keywords

Group keywords by semantic category:

```yaml
keywords:
  organizations:
    - Shenzhen Green Carbon Energy Co., Ltd.
    - Huaxi Branch
  people:
    - Li Sheng
  projects:
    - Duku Highway Project
  contracts:
    - Contract No. GC-2026-001
  custom:
    - Any exact phrase that must be masked
```

Common category aliases:

- `organizations`, `orgs`, `companies` -> `ORG`
- `people`, `persons`, `names` -> `PERSON`
- `projects` -> `PROJECT`
- `contracts`, `contract_numbers` -> `CONTRACT`
- `amounts`, `money` -> `AMOUNT`
- `addresses`, `locations` -> `ADDRESS`
- `bank`, `bank_name` -> `BANK`
- `bank_account`, `bank_accounts` -> `BANKACCOUNT`
- `tax`, `tax_no`, `tax_number` -> `TAX`

Unknown category names are converted to uppercase placeholder prefixes with non-alphanumeric characters removed.

Use `custom` for exact phrases that do not fit another category, including sensitive titles, attachment names, internal labels, or organization names that a generic pattern missed.

For Word files, long names can be split by hard line breaks or separate paragraphs. If one full name is visually continuous but extracted as fragments, add the full name and the visible fragments. Legacy `.doc` files are first converted locally to temporary `.docx` through Microsoft Word or LibreOffice/soffice:

```yaml
keywords:
  organizations:
    - Full Company Name Across The Page
    - Full Company Name
    - Across The Page
```

## Safe Output Filenames

If a document title or output filename contains sensitive information, use `--safe-name`:

```bash
python scripts/rkm.py protect input.docx --safe-name --keywords keywords.yml --out ./masked.docx --map ./map.json
```

RKM writes neutral basenames such as `rkm-masked-1a2b3c4d.docx` and `rkm-map-1a2b3c4d.json` in the directories supplied by `--out` and `--map`. The original source path is stored only inside the encrypted mapping payload.

## Regex Patterns

Put regex rules under `patterns`:

```yaml
patterns:
  phone: "\\b1[3-9]\\d{9}\\b"
  email: "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
  id_card: "\\b\\d{17}[\\dXx]\\b"
  amount: "￥?\\d+(?:\\.\\d+)?(?:万元|元|亿)?"
  contract_no: "合同编号[:：]?\\s*[A-Za-z0-9-]+"
```

Use quoted strings and escape backslashes for YAML. Regex category names become placeholder prefixes, for example `phone` -> `[[PHONE_0001]]`.

If a regex has one or more capture groups, RKM masks only the first non-empty captured group. This preserves labels and surrounding punctuation:

```yaml
patterns:
  person: "(?:姓[·.．。… \\t　]{0,8}名|联系人及电话|联系人及联系方式|联系人|经办人|负责人|申请人|填报人|制表人|审核人|审批人|签发人|法定代表人|姓名)[：:·.．。 \\t　]*(?:\\n+|[：: \\t　]+)([\\u4e00-\\u9fff]{2,4})"
```

`联系人：张三` becomes `联系人：[[PERSON_0001]]`.

Require at least one delimiter after labels so label text such as `联系人及电话` is not mistaken for a name. In Word tables, labels and values may be extracted as adjacent lines, so use `(?:\\n+|[：: \\t　]+)` when a value can be in the next cell. Avoid broad `\\s*` rules because extracted table cells may be separated by newlines. Use explicit spaces, tabs, full-width spaces, and intentional newlines instead.

For labeled addresses, preserve the label and mask the value:

```yaml
patterns:
  address: "(?:公司注册地址|注册地址|联系人地址|联系地址|通讯地址|通信地址|办公地址|经营地址|住所地|住所|地址)[：:·.．。 \\t　]*(?:\\n+|[：: \\t　]+)([^\\n\\r]{4,160}(?:路|街|道|大道|号|弄|巷|栋|座|楼|层|室|单元|园|区|院|村|大厦|广场|中心|WORLD)[^\\n\\r]{0,80})"
```

For bank account and invoice fields, preserve labels and mask only values:

```yaml
patterns:
  bank: "(?:开户行|开户银行)[：:·.．。 \\t　]*(?:\\n+|[：: \\t　]+)([^\\n\\r]{2,100}(?:银行|支行|分行|营业部|信用社)[^\\n\\r]{0,60})"
  bank_account: "(?:银行账号|银行帐号|银行账户|银行帐户|账号|帐号|账户|帐户)[：:·.．。 \\t　]*(?:\\n+|[：: \\t　]+)([0-9０-９]{8,30})"
  tax_no: "(?:税号|纳税人识别号|统一社会信用代码)[：:·.．。 \\t　]*(?:\\n+|[：: \\t　]+)([0-9A-Z]{10,30})"
```

The built-in preset also protects common labels from being masked as values: `开户名称`, `开户行`, `开户银行`, `银行账号`, `银行账户`, `税号`, `名称`, `单位地址`, and `电话`.

## Built-In Chinese Preset

For Chinese business documents, use:

```bash
python scripts/rkm.py protect input.docx --preset cn-sensitive --keywords keywords.yml --out input.masked.docx --map input.rkm-map.json
```

The `cn-sensitive` preset covers common organization suffixes, labeled person names including table labels such as `姓····名`, labeled and standalone Chinese addresses, bank account fields that preserve labels such as `开户行` and mask the value, tax numbers, dates, form-style bracketed date/duration values such as `自【2026】年【4】月【15】日起至【2026】年【6】月【31】日止` or `合作期限为【/】年` where only the values inside brackets are masked, amounts with units, bare decimal/table amounts such as `320.9`, phone numbers including landlines, email addresses, ID-card-like values, and bank-card-like values. Use explicit manual keywords for names or addresses that appear in unusual formats.

## Flat Lists

For quick one-off masking, a flat list is allowed:

```yaml
keywords:
  - Shenzhen Green Carbon Energy Co., Ltd.
  - Duku Highway Project
```

Flat-list terms use the generic `K` placeholder prefix.

## Command-Line Terms

Add ad hoc terms without editing YAML:

```bash
python scripts/rkm.py protect input.md --term "Internal Project A" --term "Jane Zhang" --out input.masked.md --map input.rkm-map.json
```

Command-line terms use the generic `K` placeholder prefix.

## Plain-Text Custom Keyword File

For a maintainable, non-YAML list of exact phrases, point `--custom-keywords` at a plain `.txt` file. A ready-to-edit template lives at `references/custom-keywords.txt`.

```bash
python scripts/rkm.py protect input.docx --preset cn-sensitive --custom-keywords references/custom-keywords.txt --out masked.docx --map map.json
```

File format:

- One keyword per line, or several keywords on one line separated by `、` or `；`.
- A whole line whose first non-space character is `#` is a comment and is ignored.
- Blank lines are ignored; duplicate keywords are dropped (first occurrence wins, so placeholders stay stable).

Each keyword is masked as a literal string with a dedicated `CUSTOM` placeholder prefix: `[[CUSTOM_0001]]`, `[[CUSTOM_0002]]`, and so on. This makes it easy to see at a glance which masks came from your own list versus a preset or pattern. `--custom-keywords` can be combined with `--preset`, `--keywords`, and `--term`; it also works with `scan` and `protect --dry-run` for previewing.

Example file:

```text
# 自定义敏感关键词
启明星科技有限公司
雅宝智慧园区项目
张三丰、李莫愁；周芷若
合同编号 HT-2026-0001
```
