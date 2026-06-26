# 常见已知平台背景参考

> 辅助快速判断，加速鉴定流程。遇到以下平台可直接引用。

## 国内 CTF / 网络安全平台

| 平台 | URL | 风险 | 背景 |
|------|-----|------|------|
| BUUCTF | buuoj.cn | 🟢低 | 北京联合大学 + 安恒信息 |
| 攻防世界 | adworld.xctf.org.cn | 🟢低 | XCTF联盟（高校+安全企业联合） |
| CTFHub | ctfer.com | 🟢低 | 专业CTF平台 |
| XCTF | xctf.org.cn | 🟢极低 | 国内最大CTF联赛官方 |
| BugKu | bugku.com | 🟢低 | CTF练习平台 |

## 常见钓鱼/仿冒特征

- 域名拼写接近知名品牌（如 `taoba0.com` vs `taobao.com`）
- 使用免费域名（.tk / .ml / .ga / .cf / .gq）
- 页面内容极少，仅有登录表单
- 无任何联系方式或备案信息
- 强制要求输入银行卡/密码
- URL 中含大量随机字符
- 页面风格粗糙、存在语言错误

## 国内主流平台可信度参考

| 类型 | 示例 | 风险 |
|------|------|------|
| 高校官网 | .edu.cn 域名 | 🟢极低 |
| 政府官网 | .gov.cn 域名 | 🟢极低 |
| BAT等大厂 | baidu.com/alipay.com | 🟢极低 |
| 知名企业官网 | 有ICP备案 | 🟢低 |
| 无备案无名网站 | 无任何背景 | 🔴高 |

## 工信部备案查询

- 查询地址：http://beian.miit.gov.cn/publish/query/indexFirst.action
- 快速查询：`site:beian.miit.gov.cn "关键词"`
