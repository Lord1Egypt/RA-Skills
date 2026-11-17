---
name: proxyclaw
description: Residential proxy CLI with explicit V2 and legacy credentials.
version: 3.0.3
license: MIT
metadata:
  author: iploop
  version: "3.0.3"
  openclaw:
    requires:
      bins: [bash, curl, python3]
      env: [IPLOOP_API_KEY]
    primaryEnv: IPLOOP_API_KEY
---

# ProxyClaw — IPLoop V2

Residential proxy requests for agents and scripts. Create/sign in at **https://platform.iploop.io/**. Save your account API key, separate proxy username and proxy password privately. Add bandwidth and use the connection settings shown in the dashboard. Do not assume a free credit amount or guaranteed target-site acceptance.

## V2 setup
```bash
export IPLOOP_API_KEY="YOUR_ACCOUNT_API_KEY"
export IPLOOP_PROXY_USERNAME="YOUR_PROXY_USERNAME"
export IPLOOP_PROXY_PASSWORD="YOUR_PROXY_PASSWORD"
```
The account key is not your proxy password. Setting both proxy credentials explicitly opts into V2; key-only existing integrations retain legacy authentication.

## Country, sessions and V2 city targeting
- Country routing uses valid ISO alpha-2 codes; availability depends on the live pool.
- Sticky sessions group requests; device availability can change the exit. A new session does not guarantee a never-used IP.
- State/city selectors are deployed in V2. Country is required; state is optional for a city request. Exact-city accuracy is not certified: some Austin test exits were labeled San Antonio or Schertz by independent geo services. Inspect the observed location when precision matters.
- V2 ASN targeting is not currently supported.

## Python SDK
```bash
python -m pip install 'iploop-sdk[async,socks]>=1.8.3'
```
```python
import os
from iploop import IPLoop
client = IPLoop(
    os.environ['IPLOOP_API_KEY'],
    proxy_username=os.environ['IPLOOP_PROXY_USERNAME'],
    proxy_password=os.environ['IPLOOP_PROXY_PASSWORD'],
)
r = client.get('https://example.com', country='US', timeout=15)
r.raise_for_status()
```
Python SDK 1.8.3 supports country, state and city selectors in sync, async and sticky requests. HTTP/SOCKS5, sticky and account usage instructions: https://proxyclaw.ai/docs.html

## Boundaries
A successful proxy connection does not prove anti-bot bypass, CAPTCHA solving, JavaScript rendering or accurate structured extraction. These are separate integrations requiring their own tests. Historical inventory/benchmark numbers are not capacity or availability guarantees. Existing earnings/node programs and legacy API guides are separate from the V2 proxy contract; verify eligibility and rates with support.

Support: support@iploop.io. Keep credentials private.

## Agent CLI (this repository)
Requires **Python 3, bash and curl**. Install the current ClawHub release or clone GitHub source. Use explicit bash invocation because registry installers may not preserve executable permissions.
```bash
git clone https://github.com/Iploop/proxyclaw.git
cd proxyclaw
bash ./setup.sh
bash ./fetch.sh https://example.com --country US
bash ./fetch.sh https://example.com --country US --session demo123
bash ./fetch.sh https://example.com --country GB --protocol socks5h
bash ./fetch.sh https://example.com --format markdown
```
`--format markdown` is a basic text conversion, not JavaScript rendering or structured extraction. Credentials are delivered to curl through stdin, not command-line arguments. Failed connections or non-success HTTP status exit nonzero. Setup does not announce success on failure.

### V2 state/city interface
```bash
bash ./fetch.sh https://example.com --country US --state tx --city austin
bash ./fetch.sh https://example.com --country US --city austin
```
No deployment flag is required. State/city selectors are deployed in V2. Country is required; state is optional for a city request. Exact-city accuracy is not certified: some Austin test exits were labeled San Antonio or Schertz by independent geo services. Inspect the observed location when precision matters.

### Legacy integrations
Leave both V2 proxy credential variables unset to retain existing key-only authentication. This does not migrate legacy credentials or certify all legacy selectors. No customer key revocation is required.
