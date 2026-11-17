# 熵与格式校验规范（yotta-secret 元钥）

## Shannon 信息熵

对字符串 s，熵 = -Σ p(c) · log2(p(c))，其中 p(c) 为字符 c 的出现频率（bit/char）。

- 单一字符重复串（aaaaaaaa）熵 ≈ 0；
- 4 种等概率字符（abcd）熵 = 2.0；
- 16 种等概率字符（0123456789abcdef）熵 = 4.0。

用途：
- generic 规则要求熵 >= 4.0；
- token / auth_token 中等置信 key 需长度 >= 16 或熵 >= 3.5；
- 输出每条 finding 附熵值供人工参考（entropy 子命令可单独计算）。

## 占位符 / 示例值过滤

以下值形态一律不算真密钥（is_placeholder 判定）：

- 尖括号占位：<your-password>、<API_KEY>
- your/my/our 前缀：your_password、my_secret
- 掩码：xxx、****、????
- 改我 / 示例：changeme、replace_me、todo、example、example123、sample、dummy、fake、demo、test123
- 布尔 / 空值：null、none、n/a、true、false、yes、no、undefined、nil
- 短数字：0-9999
- 与 key 同名：password = password、secret = SECRET
- 环境变量引用：$DB_PASSWORD、${DB_PASSWORD}、env('X')、os.environ['X']、process.env.X、
  getenv('X')、config('X')、settings('X')

## 格式校验（verify / 规则内）

- aws_secret / azure_storage：base64 形态 + 长度；
- basic_auth：base64 解码后含冒号（user:pass）；
- generic：排除纯十六进制 32/40/64/128 位（疑似哈希）与 UUID v4；
- JWT：三段 base64url 结构。

## 默认阈值

| 参数 | 默认 | 说明 |
|---|---|---|
| --min-length | 8 | credential 值最短长度 |
| --min-entropy | 3.5 | credential / token 熵参考 |
| generic 熵 | 4.0 | 高熵长 token 阈值（固定） |
| --max-size | 5 MB | 单文件扫描上限 |
