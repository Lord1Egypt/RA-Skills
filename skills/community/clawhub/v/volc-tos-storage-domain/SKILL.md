---
name: volc-tos-storage-domain
description: Bind and verify a public custom domain for an existing Volcengine TOS bucket. Use when users mention TOS/object-storage custom domains, storage.<domain>, bucket public URLs, ICP filing passed but the storage domain still cannot be reached, local `ve` lacking `tos`, TOS HTTPS certificate binding, Volcengine DNS records, or checking whether a storage domain is direct TOS versus CDN/DCDN.
license: MIT
compatibility: Designed for Claude Code and compatible agents. Requires Volcengine `ve` CLI for DNS/CDN/DCDN/certificate service checks, Node.js with `@volcengine/tos-sdk` for TOS bucket custom-domain APIs, and Volcengine AK/SK or cached CLI credentials with permissions for TOS, DNS, and Certificate Service.
metadata:
  author: "北京腾秀创智技术有限公司 (Tenshow Innovation)"
  organization: tenshowinnovation.com
  version: "0.1.0"
---

# Volcengine TOS Storage Domain

Use this workflow to connect an ICP-ready storage domain such as `storage.example.com` to an existing TOS bucket, issue or find a DV certificate, bind HTTPS, and prove object URLs work.

This is for **direct TOS custom-domain mode**. If the user wants edge caching, WAF behavior, or CDN logs, treat that as a separate CDN/DCDN setup instead of silently adding CDN.

## Required inputs

Collect or infer these before changing cloud state:

- Storage domain, for example `storage.example.com`
- TOS bucket name, region, and endpoint
- DNS zone owner and Zone ID, usually via `ve dns ListZones`
- Volcengine organization ID for DV certificate requests
- Whether the desired result is direct TOS or CDN/DCDN

## Workflow

1. Read existing state first: CDN/DCDN, DNS records, bucket info, bucket ACL, and current TOS custom-domain rules.
2. If `ve tos` is unavailable, use `@volcengine/tos-sdk` for TOS APIs. Use `ve` for DNS, CDN/DCDN, and certificate-service APIs.
3. Bind the custom domain to the bucket before relying on the CNAME; TOS uses this Host binding to accept the custom domain.
4. Add the DNS CNAME from the storage host to the bucket endpoint returned by TOS.
5. Apply or locate a DV certificate, confirm `_dnsauth.<host>` TXT validation, and poll until the certificate is `Issued`.
6. Bind the cert to the TOS custom-domain rule with `Protocol: "tos"` and verify `CertStatus: "CertBound"`.
7. Prove the result with `dig`, `curl -I`, `openssl s_client`, and at least one real object URL.

Read [references/tos-custom-domain-runbook.md](references/tos-custom-domain-runbook.md) for the exact commands, SDK calls, OpenAPI fallback, validation checks, and landmines.

## First response for unreachable ICP-ready domains

When the user says an ICP-ready `storage.<domain>` host still cannot be reached, do not jump straight to DNS writes. First outline these read-only checks:

- `ve cdn ListCdnDomains` and `ve dcdn ListDomainConfig` to decide whether CDN/DCDN is involved.
- `ve dns ListZones`, `ve dns ListRecords`, and authoritative `dig` to confirm the current CNAME.
- TOS SDK reads with `@volcengine/tos-sdk`, especially `getBucketInfo`, `getBucketAcl`, and `getBucketCustomDomain`.
- `curl -I` and `openssl s_client` to separate HTTP reachability from HTTPS certificate binding.

After discovery, propose writes in order: `putBucketCustomDomain`, `ve dns CreateRecord`, `QuickApplyCertificate`, `CertificateGetDcvParam`, `_dnsauth.<host>` TXT, `CertificateGetInstanceList`, then TOS cert binding with `Protocol: "tos"`.

When the user asks whether CDN is required, answer directly: direct TOS custom-domain mode is valid for public object URLs, and CDN/DCDN is optional and separate. Only recommend CDN/DCDN when the user asks for edge caching, acceleration, logs, WAF behavior, or bandwidth optimization.

When the user says local `ve` has no `tos` namespace, be explicit:

- Use `@volcengine/tos-sdk` / `TosClient` for `getBucketCustomDomain` and `putBucketCustomDomain`.
- Keep using `ve dns CreateRecord` for DNS and `ve certificateservice QuickApplyCertificate` plus `CertificateGetInstanceList` for certificate lifecycle.
- If `ve` cannot call `CertificateGetDcvParam`, use OpenAPI version `2021-06-01` with GET query `instance_id` to fetch DNS validation parameters.
- Bind the certificate back to the TOS custom-domain rule with `Protocol: "tos"` and `CertId`; do not use `http` or `https` as the TOS `Protocol`.

## Behavior rules

- Do not guess cloud state. Inspect first, then write.
- Do not churn DNS TXT records during certificate validation; propagation delays can make retries slower.
- Do not treat ICP approval as sufficient. ICP only removes the filing blocker; TOS binding, DNS, and HTTPS still need to be configured.
- Do not assume CDN exists. Direct TOS custom-domain mode is valid and should show zero CDN/DCDN domains.
- Never print or persist AK/SK, private keys, certificate private keys, or one-off validation secrets in user-facing docs.
