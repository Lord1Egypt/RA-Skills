# 部署路径

`T` 代表 `python {baseDir}/scripts/tcapi.py`，`RUN` 代表 `python {baseDir}/scripts/run_on_server.py`。
默认使用 profile `agent-ops`；地域服务默认在 ap-hongkong。
所有命令在 Windows、macOS、Linux 上都一样。

每条路径开工前都先跑一次 doctor。路径中需要人做的事，开工前合成一张人工卡一次性发出。

---

## R0 还没有域名（查好候选，人来买）

```bash
T domain CheckDomain DomainName=mybrand.com                    # 能否注册，免费
#   看这几项：Available / Premium（溢价）/ Price / RealPrice（折后）/ FeeRenew / RecordSupport（可否备案）
T domain DescribeDomainPriceList TldList:='[".com",".cn",".net"]' Year:='[1]'
```

- 挑 3 个可以注册的候选，附上实时价格，按 human-cards.md 的 C4 卡片一次性发出。
  - 面向国内用户：.cn 更便宜，以后备案也方便。
  - 面向海外用户：.com。
- **不要代为下单**：一是策略禁止，二是下单要选一个已通过实名审核的信息模板，这一步只能人来做。
- 用户买好后，执行 `T dnspod DescribeDomainList`，确认新域名已出现在账号里。
- 新域名的实名审核通过之前，注册局会暂停解析（ServerHold）。这段时间先用服务器 IP 访问。

---

## R1 改 DNS（DNSPod）

前提：域名的 NS 已指向 DNSPod，可以用 `T dnspod DescribeDomainList` 确认。

```bash
T dnspod DescribeRecordList Domain=example.com Subdomain=www
#   报错 kind=not_found 表示没有记录，不算失败
T dnspod CreateRecord Domain=example.com SubDomain=www RecordType=A RecordLine=默认 Value=1.2.3.4 TTL:=600
T dnspod ModifyRecord Domain=example.com RecordId:=<id> SubDomain=www RecordType=A RecordLine=默认 Value=5.6.7.8
#   改记录必须带 RecordId，而且 SubDomain、RecordType、RecordLine、Value 要全部重新传一遍
T dnspod DescribeRecordList Domain=example.com Subdomain=www   # 用接口回读确认，不要用本机 dig
```

改动前，先执行 `T dnspod DescribeRecordList Domain=example.com Limit:=3000`，把结果存到 `./tc-backup/`。

---

## R2 EdgeOne 加速静态站（不需要备案）

适用场景：源站已经在 Cloudflare Pages、Vercel、对象存储等地方，只是国内访问慢。实测加速后首屏从 2.5s 降到 0.35s。

**人工卡（开工前发出）**：到 https://console.cloud.tencent.com/edgeone 购买套餐。
- 国内站**没有免费版**。最便宜的是个人版，约 ¥9.9/月，含 50GB 流量。
- 是否自动续费由用户决定。
- 可以先执行 `T teo DescribeAvailablePlans` 查一下当前价格。

```bash
# 1. 建 zone：必须用主域名；Type=partial 是 CNAME 接入，DNS 不用搬家；没备案就选 Area=overseas
T teo CreateZone ZoneName=example.com Type=partial Area=overseas PlanId=<套餐ID>
#    返回结果里有一条用于归属验证的 TXT 记录 → 按 R1 加到 DNSPod（主机记录一般是 edgeonereclaim）
T teo VerifyOwnership Domain=example.com

# 2. 添加加速域名：回源到 Pages/Vercel 时必须固定 HTTPS 443，HostHeader 和源站域名一致
T teo CreateAccelerationDomain ZoneId=<zone-id> DomainName=www.example.com \
  OriginInfo:='{"OriginType":"IP_DOMAIN","Origin":"myapp.pages.dev","HostHeader":"myapp.pages.dev"}' \
  OriginProtocol=HTTPS HttpsOriginPort:=443

# 3. 查 CNAME 地址 → 在 DNSPod 建一条 CNAME 记录，指向 <host>.eo.dnse0.com.
T teo DescribeAccelerationDomains ZoneId=<zone-id> Filters:='[{"Name":"domain-name","Values":["www.example.com"]}]'

# 4. 轮询，直到 DomainStatus == online（约 3–7 分钟），然后签免费证书（约 5–8 分钟生效）
T teo ModifyHostsCertificate ZoneId=<zone-id> Hosts:='["www.example.com"]' Mode=eofreecert

# 5. 站点级设置（之后新加的域名会继承）
T teo ModifyZoneSetting ZoneId=<zone-id> ForceRedirect:='{"Switch":"on","RedirectStatusCode":301}'

# 6. 每次部署后刷新缓存，再用 curl 确认新内容已生效（一次 purge 不一定够）
T teo CreatePurgeTask ZoneId=<zone-id> Type=purge_all
```

已知的坑：
- Pages 会把 `x.html` 用 308 重定向到 `x`，这个 308 也会被缓存。所以链接要写不带扩展名的形式，purge 时两个 URL 都要刷。

---

## R3 Lighthouse 香港（需要后端，不需要备案）

**买服务器：用 `buy_server.py`，不要自己写购买教程。**

腾讯云购买页的默认选项全是坑：默认是「应用镜像」（会装上用户不需要的软件）、默认地域是北京（需要备案）、
默认套餐是「中国香港入门型」（大陆访问慢）、默认系统是 OpenCloudOS。非技术用户照着文字教程，大概率会在这里卡住或者买错。

```bash
python {baseDir}/scripts/buy_server.py plan --size small     # 静态站或博客：锐驰型 2核2G，约 ¥55/月
python {baseDir}/scripts/buy_server.py plan --size medium    # 带后端或数据库：锐驰型 2核4G，约 ¥95/月
python {baseDir}/scripts/buy_server.py wait --bundle <bundle_id> --since <plan_at>   # 后台运行：照抄 plan 输出的 wait_cmd
```

- `plan` 会用 API 拉取实时套餐和镜像，生成一个**已经预选好**的购买链接：系统镜像 → Ubuntu 24.04 LTS → 中国香港 → 锐驰型。
  同时生成一张卡片（`card` 字段），**把它原样发给用户**。用户只需要做 4 件事：选时长、决定是否自动续费、勾选协议、点购买并付款。
- 用户收到卡片的同时，就在后台运行 plan 输出的 `wait_cmd`（只认这次买的那台：套餐一致、在 plan 之后创建）。用户付完款，agent 会自动发现新服务器并接着往下做，用户不需要回复"好了"。
- 登录方式保持默认的「自动生成密码」即可。agent 通过 TAT 管理服务器，不需要这个密码，也不需要 SSH 密钥。
- 购买必须在**主账号**登录的情况下完成，子账号没有购买权限。
- 已实测（2026-10-08）：链接参数 `regionId=5`、`blueprintType=PURE_OS`、`blueprintOfficialId`、`bundleId` 都能正确预选。
  `loginSet` 参数无效，会被重置为自动生成密码；进阶配置（一键配置域名解析、存储包、主机安全）默认都不勾选。

买好之后，下面的步骤全部由 agent 完成：

```bash
# 1. 查实例：拿到 InstanceId、公网 IP（PublicAddresses）、到期时间（ExpiredTime）、续费方式（RenewFlag）
T lighthouse DescribeInstances

# 2. 直接在服务器上执行命令（root 身份，不需要 SSH）
RUN --instance <id> "uname -a; df -h /; free -m"
RUN --instance <id> --file deploy.sh --timeout 900      # 较长的部署脚本，先在本地写好
#    想用 SSH 时：用 RUN 把你自己的公钥追加到 /home/ubuntu/.ssh/authorized_keys
#    不要调用 AssociateInstancesKeyPairs：它会强制关机，并让原来的密钥失效

# 3. 防火墙：官方文档说 Linux 默认放行 22/80/443，但我们遇到过 443 不通的情况，以实际查询结果为准
T lighthouse DescribeFirewallRules InstanceId=<id>
T lighthouse CreateFirewallRules InstanceId=<id> \
  FirewallRules:='[{"Protocol":"TCP","Port":"443","CidrBlock":"0.0.0.0/0","Action":"ACCEPT"}]'
```

4. 部署：用 RUN 或 SSH 按常规做法装好 nginx、docker/pm2、systemd 服务。
5. **先用 IP 验证**：`RUN --instance <id> "curl -sI localhost"`，再到 itdog.cn 从外部访问 `http://<IP>`。
6. 有域名：按 R1 把 A 记录指向这个 IP，等解析生效、443 已放行后，再用 RUN 跑 certbot。
   没有域名：只能先用 `http://<IP>` 访问，HTTPS 需要域名（见 R0）。

### 交付：告诉用户怎么访问、以后怎么维护

部署完成后，发给用户的说明**不要出现任何技术术语或报错原文**：

```
✅ 网站已上线
访问地址：https://<域名>（暂时没有域名时：http://<IP>，这是临时地址）
服务器：腾讯云轻量服务器 · 中国香港 · <配置> · <ExpiredTime> 到期（<自动/手动>续费）
国内打开速度：<itdog 测速结果>（香港机房不需要备案）
以后要改内容：直接告诉我"把 xx 改成 yy"就行
提醒：服务器和域名都要按时续费，我会在到期前一个月提醒你
```

**专职运维的日常**：每次被唤起时，都可以顺手执行 `T lighthouse DescribeInstances`，看看到期时间（ExpiredTime）。距离到期不足 30 天时，主动提醒用户续费。续费需要用户本人操作。

---

## 备案（ICP）

- 只有网站必须放在国内机房，或者要用 EdgeOne 的 mainland/global 加速时，才需要备案。
- 备案全程由用户在 https://console.cloud.tencent.com/beian 完成：提交证件、拍照核验、等管局审核，通常要 1–3 周。
- 备案期间，先按 R2/R3 把网站跑起来。
