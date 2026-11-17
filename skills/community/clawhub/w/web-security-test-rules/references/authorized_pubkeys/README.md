# 受信公钥目录（Trusted Public Keys）

本目录存放**授权方公钥**（PEM 格式），用于验证 `AUTHORIZATION.json` 里的签名令牌。
文件名即 `key_id`，例如 `example.pem` 对应声明里的 `"key_id": "example"`。

## 目录里已有什么

- `example.pem`：演示用公钥（对应脚本自测生成的临时私钥，**仅供验证流程跑通，生产请勿使用**）。

## 如何接入你自己的授权方

1. 让授权方用 RSA-2048（或更强）生成密钥对，把**公钥**发给你：

   ```bash
   # 授权方侧
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out team-a.priv.pem
   openssl pkey -in team-a.priv.pem -pubout -out team-a.pub.pem
   ```

2. 把公钥放到本目录，文件名就是 `key_id`：

   ```bash
   cp team-a.pub.pem references/authorized_pubkeys/team-a.pem
   ```

3. 授权方在 `AUTHORIZATION.json` 里写 `"key_id": "team-a"`，并用其私钥签名（见仓库 `scripts/sign_auth.sh`）。

4. skill 验签时会按 `key_id` 在本目录找到 `team-a.pem` 并验证。

## 安全要点

- **私钥绝不进仓库**：授权方自行保管私钥；本目录只放公钥。
- **公钥来源可信**：只添加你确实信任的授权方公钥；替换/新增公钥等于变更"谁能签发有效授权"。
- **多授权方**：每个授权方一个文件，`key_id` 不重复即可。
- 删除某公钥 = 撤销该授权方的签发资格（其已签文件将验签失败）。
