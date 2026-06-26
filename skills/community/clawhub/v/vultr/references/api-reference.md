# Vultr API Reference

## Authentication

All API requests require an API key passed in the `Authorization` header:
```
Authorization: Bearer YOUR_API_KEY
```

Generate API keys at: https://my.vultr.com/settings/#settingsapi

## Rate Limits

- 30 requests per second per IP
- 429 response includes `Retry-After` header

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `per_page` | int | Items per page (default 100, max 500) |
| `cursor` | string | Pagination cursor from `meta.links.next/prev` |

---

## Account

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/account` | Get account info, balance, ACLs |
| GET | `/account/bgp` | Get BGP configuration |
| GET | `/account/bandwidth` | Get bandwidth usage |

---

## Instances (VPS)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/instances` | List all instances |
| GET | `/instances/{id}` | Get instance details |
| POST | `/instances` | Create instance |
| PATCH | `/instances/{id}` | Update instance |
| DELETE | `/instances/{id}` | Delete instance |
| POST | `/instances/{id}/start` | Start instance |
| POST | `/instances/{id}/halt` | Stop instance |
| POST | `/instances/{id}/reboot` | Reboot instance |
| POST | `/instances/{id}/reinstall` | Reinstall instance |
| GET | `/instances/{id}/bandwidth` | Get bandwidth usage |
| GET | `/instances/{id}/ipv4` | List IPv4 addresses |
| GET | `/instances/{id}/ipv6` | List IPv6 addresses |
| POST | `/instances/{id}/ipv4` | Add IPv4 address |
| POST | `/instances/{id}/ipv4/reverse` | Set reverse DNS |
| GET | `/instances/{id}/user-data` | Get user data |

### Create Instance Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Region ID (e.g., `ewr`, `lax`, `ams`) |
| `plan` | Yes | Plan ID (e.g., `vc2-1c-1gb`) |
| `os_id` | Yes* | OS ID (use ONE of os_id, app_id, image_id, snapshot_id) |
| `app_id` | Yes* | Application ID |
| `image_id` | Yes* | Marketplace image ID |
| `snapshot_id` | Yes* | Snapshot ID |
| `label` | No | Instance label |
| `hostname` | No | Hostname |
| `tags` | No | Array of tags |
| `sshkey_id` | No | Array of SSH key IDs |
| `enable_ipv6` | No | Enable IPv6 (boolean) |
| `user_data` | No | Base64-encoded user data |
| `script_id` | No | Startup script ID |
| `reserved_ipv4` | No | Reserved IP ID |
| `attach_vpc` | No | Array of VPC IDs |

---

## Bare Metal

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bare-metals` | List bare metal instances |
| GET | `/bare-metals/{id}` | Get bare metal details |
| POST | `/bare-metals` | Create bare metal |
| PATCH | `/bare-metals/{id}` | Update bare metal |
| DELETE | `/bare-metals/{id}` | Delete bare metal |
| POST | `/bare-metals/{id}/start` | Start |
| POST | `/bare-metals/{id}/halt` | Stop |
| POST | `/bare-metals/{id}/reboot` | Reboot |
| POST | `/bare-metals/{id}/reinstall` | Reinstall |
| GET | `/bare-metals/{id}/bandwidth` | Bandwidth |
| GET | `/bare-metals/{id}/ipv4` | IPv4 info |
| GET | `/bare-metals/{id}/ipv6` | IPv6 info |

---

## Kubernetes (VKE)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/kubernetes/clusters` | List clusters |
| GET | `/kubernetes/clusters/{id}` | Get cluster |
| POST | `/kubernetes/clusters` | Create cluster |
| PUT | `/kubernetes/clusters/{id}` | Update cluster |
| DELETE | `/kubernetes/clusters/{id}` | Delete cluster |
| GET | `/kubernetes/clusters/{id}/kubeconfig` | Get kubeconfig |
| GET | `/kubernetes/clusters/{id}/resources` | Get resources |
| GET | `/kubernetes/clusters/{id}/upgrades` | Available upgrades |
| POST | `/kubernetes/clusters/{id}/upgrade` | Start upgrade |
| GET | `/kubernetes/clusters/{id}/node-pools` | List node pools |
| POST | `/kubernetes/clusters/{id}/node-pools` | Create node pool |
| GET | `/kubernetes/clusters/{id}/node-pools/{npid}` | Get node pool |
| PATCH | `/kubernetes/clusters/{id}/node-pools/{npid}` | Update node pool |
| DELETE | `/kubernetes/clusters/{id}/node-pools/{npid}` | Delete node pool |
| GET | `/kubernetes/versions` | Available versions |

---

## Managed Databases

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/managed-databases` | List databases |
| GET | `/managed-databases/plans` | List plans |
| GET | `/managed-databases/{id}` | Get database |
| POST | `/managed-databases` | Create database |
| PUT | `/managed-databases/{id}` | Update database |
| DELETE | `/managed-databases/{id}` | Delete database |
| GET | `/managed-databases/{id}/usage` | Usage info |
| GET | `/managed-databases/{id}/users` | List users |
| GET | `/managed-databases/{id}/logical-databases` | List DBs |
| GET | `/managed-databases/{id}/backups` | Backup info |
| POST | `/managed-databases/{id}/restore` | Restore from backup |
| GET | `/managed-databases/{id}/available-versions` | Available versions |

Supported types: `mysql`, `pg`, `redis`, `kafka`, `valkey`

---

## Load Balancers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/load-balancers` | List load balancers |
| GET | `/load-balancers/{id}` | Get load balancer |
| POST | `/load-balancers` | Create load balancer |
| PATCH | `/load-balancers/{id}` | Update load balancer |
| DELETE | `/load-balancers/{id}` | Delete load balancer |
| GET | `/load-balancers/{id}/forwarding-rules` | List rules |
| POST | `/load-balancers/{id}/forwarding-rules` | Create rule |
| GET | `/load-balancers/{id}/firewall-rules` | List firewall rules |

---

## DNS

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/domains` | List domains |
| GET | `/domains/{domain}` | Get domain |
| POST | `/domains` | Create domain |
| PUT | `/domains/{domain}` | Update domain |
| DELETE | `/domains/{domain}` | Delete domain |
| GET | `/domains/{domain}/records` | List records |
| POST | `/domains/{domain}/records` | Create record |
| GET | `/domains/{domain}/records/{rid}` | Get record |
| PATCH | `/domains/{domain}/records/{rid}` | Update record |
| DELETE | `/domains/{domain}/records/{rid}` | Delete record |
| GET | `/domains/{domain}/dnssec` | DNSSEC info |
| GET | `/domains/{domain}/soa` | SOA info |

### DNS Record Types

A, AAAA, CNAME, MX, NS, SRV, TXT, CAA, SSHFP

---

## Firewall

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/firewalls` | List firewall groups |
| GET | `/firewalls/{id}` | Get group |
| POST | `/firewalls` | Create group |
| PUT | `/firewalls/{id}` | Update group |
| DELETE | `/firewalls/{id}` | Delete group |
| GET | `/firewalls/{id}/rules` | List rules |
| POST | `/firewalls/{id}/rules` | Create rules |
| GET | `/firewalls/{id}/rules/{rid}` | Get rule |
| DELETE | `/firewalls/{id}/rules/{rid}` | Delete rule |

### Firewall Rule Parameters

| Parameter | Description |
|-----------|-------------|
| `ip_type` | `v4` or `v6` |
| `protocol` | `tcp`, `udp`, `icmp`, `gre` |
| `port` | Port or range (e.g., `22`, `80-443`) |
| `subnet` | CIDR (e.g., `192.168.1.0/24`) |
| `subnet_size` | Subnet size |
| `source` | Source (optional, defaults to anywhere) |

---

## VPC Networks

### VPC 1.0

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vpcs` | List VPCs |
| GET | `/vpcs/{id}` | Get VPC |
| POST | `/vpcs` | Create VPC |
| PUT | `/vpcs/{id}` | Update VPC |
| DELETE | `/vpcs/{id}` | Delete VPC |

### VPC 2.0

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vpc2` | List VPC 2.0 networks |
| GET | `/vpc2/{id}` | Get network |
| POST | `/vpc2` | Create network |
| PUT | `/vpc2/{id}` | Update network |
| DELETE | `/vpc2/{id}` | Delete network |
| GET | `/vpc2/{id}/nodes` | List attached nodes |
| POST | `/vpc2/{id}/nodes` | Attach nodes |
| DELETE | `/vpc2/{id}/nodes` | Detach nodes |

---

## Block Storage

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/blocks` | List block storage |
| GET | `/blocks/{id}` | Get block storage |
| POST | `/blocks` | Create block storage |
| PATCH | `/blocks/{id}` | Update block storage |
| DELETE | `/blocks/{id}` | Delete block storage |
| POST | `/blocks/{id}/attach` | Attach to instance |
| POST | `/blocks/{id}/detach` | Detach from instance |
| GET | `/blocks/{id}/snapshots` | List snapshots |
| POST | `/blocks/{id}/snapshots` | Create snapshot |

---

## Object Storage (S3-Compatible)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/object-storage` | List object storage |
| GET | `/object-storage/{id}` | Get object storage |
| POST | `/object-storage` | Create object storage |
| PUT | `/object-storage/{id}` | Update |
| DELETE | `/object-storage/{id}` | Delete |
| POST | `/object-storage/{id}/regenerate-keys` | Regenerate keys |
| GET | `/object-storage/clusters` | List clusters |
| GET | `/object-storage/clusters/{id}/tiers` | List tiers |

---

## Snapshots

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/snapshots` | List snapshots |
| GET | `/snapshots/{id}` | Get snapshot |
| POST | `/snapshots` | Create from instance |
| POST | `/snapshots/create-from-url` | Create from URL |
| PUT | `/snapshots/{id}` | Update snapshot |
| DELETE | `/snapshots/{id}` | Delete snapshot |

---

## Reserved IPs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reserved-ips` | List reserved IPs |
| GET | `/reserved-ips/{id}` | Get reserved IP |
| POST | `/reserved-ips` | Create reserved IP |
| PATCH | `/reserved-ips/{id}` | Update |
| DELETE | `/reserved-ips/{id}` | Delete |
| POST | `/reserved-ips/{id}/attach` | Attach to instance |
| POST | `/reserved-ips/{id}/detach` | Detach from instance |
| POST | `/reserved-ips/{id}/convert` | Convert instance IP |

---

## SSH Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ssh-keys` | List SSH keys |
| GET | `/ssh-keys/{id}` | Get SSH key |
| POST | `/ssh-keys` | Create SSH key |
| PATCH | `/ssh-keys/{id}` | Update SSH key |
| DELETE | `/ssh-keys/{id}` | Delete SSH key |

---

## ISO Images

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/iso` | List custom ISOs |
| GET | `/iso/{id}` | Get ISO |
| POST | `/iso` | Create ISO from URL |
| DELETE | `/iso/{id}` | Delete ISO |
| GET | `/iso-public` | List public ISOs |

---

## Regions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/regions` | List regions |
| GET | `/regions/{id}` | Get region |
| GET | `/regions/{id}/availability` | Available plans |

### Common Region IDs

| ID | Location |
|----|----------|
| `ewr` | New Jersey |
| `lax` | Los Angeles |
| `sea` | Seattle |
| `mia` | Miami |
| `ord` | Chicago |
| `dfw` | Dallas |
| `ams` | Amsterdam |
| `fra` | Frankfurt |
| `lhr` | London |
| `syd` | Sydney |
| `tok` | Tokyo |
| `sgp` | Singapore |
| `blr` | Bangalore |

---

## Plans

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/plans` | List VPS plans |
| GET | `/plans?type=vc2` | Cloud Compute |
| GET | `/plans?type=vhf` | High Frequency |
| GET | `/plans?type=vhp` | High Performance |
| GET | `/plans?type=vcg` | Cloud GPU |
| GET | `/plans-metal` | Bare Metal plans |

---

## Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/history` | Billing history |
| GET | `/invoices` | List invoices |
| GET | `/invoices/{id}` | Get invoice |
| GET | `/invoices/{id}/items` | Invoice items |
| GET | `/billing/pending-charges` | Pending charges |

---

## Support Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tickets` | List tickets |
| GET | `/tickets/{id}` | Get ticket |
| POST | `/tickets` | Create ticket |
| POST | `/tickets/{id}/close` | Close ticket |
| GET | `/tickets/{id}/replies` | List replies |
| POST | `/tickets/{id}/replies` | Reply to ticket |

---

## Operating Systems

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/os` | List OS options |

### Common OS IDs

| ID | OS |
|----|-----|
| 174 | Ubuntu 24.04 x64 |
| 186 | Debian 12 x64 |
| 215 | AlmaLinux 9 x64 |
| 542 | Rocky Linux 9 x64 |
| 1744 | Ubuntu 22.04 x64 |

---

## Applications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/applications` | List apps |
| GET | `/applications?type=marketplace` | Marketplace apps |
| GET | `/applications?type=one-click` | One-Click apps |

---

## Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List users |
| GET | `/users/{id}` | Get user |
| POST | `/users` | Create user |
| PATCH | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

---

## Startup Scripts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/startup-scripts` | List scripts |
| GET | `/startup-scripts/{id}` | Get script |
| POST | `/startup-scripts` | Create script |
| PATCH | `/startup-scripts/{id}` | Update script |
| DELETE | `/startup-scripts/{id}` | Delete script |

---

## Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/logs` | List account activity logs |
