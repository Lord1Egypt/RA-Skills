# TOS Custom Storage Domain Runbook

This runbook binds a public custom domain such as `storage.example.com` to an existing Volcengine TOS bucket and enables HTTPS. It assumes direct TOS custom-domain mode, not CDN.

## 1. Discover current state

Start read-only. Confirm the problem is not simply local DNS/proxy behavior.

```bash
ve cdn ListCdnDomains --body '{"Domain":"storage.example.com","ExactMatch":true,"PageNum":1,"PageSize":10}'
ve dcdn ListDomainConfig --body '{"Keyword":"storage.example.com","PageNumber":1,"PageSize":10}'
ve dns ListZones --body '{"Key":"example.com","SearchMode":"exact","PageNumber":1,"PageSize":10}'
ve dns ListRecords --body '{"ZID":123456,"PageNumber":1,"PageSize":100}'
dig @ns1.volcengine-dns.com storage.example.com CNAME +noall +answer +authority
curl -I --max-time 10 https://storage.example.com/
```

Use TOS SDK for bucket-side reads, because many `ve` installs do not expose a `tos` service:

```js
const { TosClient } = require('@volcengine/tos-sdk');

const client = new TosClient({
  accessKeyId: process.env.VOLC_ACCESS_KEY,
  accessKeySecret: process.env.VOLC_SECRET_KEY,
  region: 'cn-beijing',
  endpoint: 'tos-cn-beijing.volces.com',
  enableOptimizeMethodBehavior: true,
});

const bucket = 'example-bucket';
await client.getBucketInfo({ bucket });
await client.getBucketAcl(bucket);
await client.getBucketCustomDomain({ bucket });
```

If a resolver returns `198.18.x.x`, suspect a local proxy/fake-ip resolver. Check authoritative DNS before declaring public DNS broken.

## 2. Bind the TOS custom domain

Bind the custom domain before relying on DNS. Without this Host binding, TOS may still serve the bucket endpoint but not the custom hostname.

```js
await client.putBucketCustomDomain({
  bucket: 'example-bucket',
  customDomainRule: {
    Domain: 'storage.example.com',
  },
});

const rules = await client.getBucketCustomDomain({ bucket: 'example-bucket' });
console.log(rules.data.CustomDomainRules);
```

Expected rule shape:

```json
{
  "Domain": "storage.example.com",
  "Cname": "example-bucket.tos-cn-beijing.volces.com",
  "Forbidden": false,
  "CertStatus": "CertUnbound",
  "Protocol": "tos"
}
```

`Protocol` is `tos` or `s3`, not `http` or `https`. Passing `http` commonly returns an `InvalidArgument` error for `protocol`.

## 3. Add DNS CNAME

Create the storage host record in the authoritative Volcengine DNS zone.

```bash
ve dns CreateRecord --body '{
  "ZID":123456,
  "Host":"storage",
  "Type":"CNAME",
  "Value":"example-bucket.tos-cn-beijing.volces.com",
  "Line":"default",
  "TTL":600,
  "Weight":1,
  "Remark":"TOS custom domain"
}'

dig @ns1.volcengine-dns.com storage.example.com CNAME +short
dig @ns2.volcengine-dns.com storage.example.com CNAME +short
```

Direct TOS mode does not require CDN or DCDN. It is normal for both `ListCdnDomains` and `ListDomainConfig` to return zero domains.

## 4. Apply or locate a DV certificate

First list existing certs. Reuse one only if `San` covers the exact storage domain and `Status` is `Issued`.

```bash
ve certificateservice CertificateGetInstanceList --body '{
  "Domain":"storage.example.com",
  "IsValid":true,
  "PageNumber":1,
  "PageSize":20
}'
```

If none exists, apply for a single-domain DV certificate:

```bash
ve certificateservice QuickApplyCertificate --body '{
  "CommonName":"storage.example.com",
  "San":["storage.example.com"],
  "OrganizationId":"org-REPLACE_ME",
  "Plan":"digicert_ee_standard_dv",
  "ProjectName":"default",
  "KeyAlg":"rsa",
  "Tag":"storage.example.com",
  "ValidationType":"dns_txt"
}'
```

Save the returned `InstanceId`, for example `cert-REPLACE_ME`.

## 5. Fetch and publish DNS validation

Some `ve` versions do not expose `CertificateGetDcvParam`. Use the OpenAPI SDK or a SigV4 helper. The working API shape is version `2021-06-01`, method `GET`, query parameter `instance_id`.

```js
const { Service } = require('@volcengine/openapi');

const service = new Service({
  serviceName: 'certificate_service',
  defaultVersion: '2021-06-01',
  host: 'open.volcengineapi.com',
  region: 'cn-beijing',
  accessKeyId: process.env.VOLC_ACCESS_KEY,
  secretKey: process.env.VOLC_SECRET_KEY,
});

const getDcvParam = service.createAPI('CertificateGetDcvParam', {
  method: 'GET',
  queryKeys: ['instance_id'],
});

const res = await getDcvParam({ instance_id: 'cert-REPLACE_ME' });
console.log(res.Result);
```

Expected validation data:

```json
{
  "validation_type": "dns_txt",
  "domains_to_be_validated": [
    {
      "validation_domain": "_dnsauth.storage.example.com",
      "value": "TXT_VALUE_REPLACE_ME"
    }
  ]
}
```

Create the TXT record if it does not already exist:

```bash
ve dns CreateRecord --body '{
  "ZID":123456,
  "Host":"_dnsauth.storage",
  "Type":"TXT",
  "Value":"TXT_VALUE_REPLACE_ME",
  "Line":"default",
  "TTL":600,
  "Weight":1,
  "Remark":"DV validation for storage.example.com"
}'
```

If `CreateRecord` returns a duplicate-record error, query the existing record and compare the value. Certificate Service may already have written the exact TXT record.

```bash
ve dns ListRecords --body '{"ZID":123456,"Host":"_dnsauth.storage","PageNumber":1,"PageSize":50}'
dig @ns1.volcengine-dns.com _dnsauth.storage.example.com TXT +short
dig @ns2.volcengine-dns.com _dnsauth.storage.example.com TXT +short
```

Do not repeatedly delete/recreate this TXT record. Let DNS propagate and poll the certificate state.

## 6. Poll certificate issuance

```bash
ve certificateservice CertificateGetInstanceList --body '{
  "InstanceIds":["cert-REPLACE_ME"],
  "PageNumber":1,
  "PageSize":10
}'
```

Wait until:

```text
Status: Issued
CertificateKeyAlgorithm: RSA 2048
San: ["storage.example.com"]
```

## 7. Bind the certificate to the TOS custom domain

Update the same TOS custom-domain rule with `CertId` and `Protocol: "tos"`.

```js
await client.putBucketCustomDomain({
  bucket: 'example-bucket',
  customDomainRule: {
    Domain: 'storage.example.com',
    Protocol: 'tos',
    CertId: 'cert-REPLACE_ME',
  },
});

const after = await client.getBucketCustomDomain({ bucket: 'example-bucket' });
console.log(after.data.CustomDomainRules);
```

Expected:

```text
CertStatus: CertBound
Protocol: tos
```

## 8. Verify HTTPS and real objects

```bash
dig @ns1.volcengine-dns.com storage.example.com CNAME +short
curl -I --max-time 20 https://storage.example.com/
openssl s_client -connect storage.example.com:443 -servername storage.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
curl -I --max-time 10 https://storage.example.com/path/to/object.mp3
```

Expected:

- Root or bucket request returns `200 OK` from `TosServer`.
- Certificate subject or SAN contains `storage.example.com`.
- Real object URLs return `200 OK` with the expected `Content-Type`.
- CDN/DCDN queries may still be empty; direct TOS custom-domain mode is working if the TOS checks pass.

## Generic example

Reusable non-secret values for examples:

```text
Domain: storage.example.com
Bucket: example-assets-prod
CNAME:  example-assets-prod.tos-cn-beijing.volces.com
Cert:   cert-REPLACE_ME
TXT:    _dnsauth.storage.example.com TXT TXT_VALUE_REPLACE_ME
```

The final shape is:

```text
storage.example.com
  -> CNAME example-assets-prod.tos-cn-beijing.volces.com
  -> TOS bucket example-assets-prod
  -> TOS custom-domain cert bound with Protocol: tos
```

## Landmines

- ICP approval only removes the filing blocker. DNS, TOS custom-domain binding, and HTTPS still need explicit setup.
- `ve` may not have a `tos` namespace. Use TOS SDK for `getBucketCustomDomain` and `putBucketCustomDomain`.
- `CertificateGetDcvParam` may be absent from `ve`; call OpenAPI version `2021-06-01` with GET query `instance_id`.
- `Protocol` in TOS custom-domain binding is `tos` or `s3`, not `http` or `https`.
- Duplicate TXT records can be good news. Query and compare before changing them.
- `198.18.x.x` DNS answers usually come from local fake-ip/proxy mode.
- Direct TOS custom-domain mode is not CDN. Do not promise edge caching unless CDN/DCDN is explicitly configured.
- Avoid printing AK/SK, private keys, certificate private keys, or real one-off TXT validation values in shared docs.
