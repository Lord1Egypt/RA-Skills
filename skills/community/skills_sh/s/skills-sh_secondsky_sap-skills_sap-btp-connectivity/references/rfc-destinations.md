# RFC Destinations - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/rfc-destinations-238d027.md](https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/rfc-destinations-238d027.md)

---

## Overview

RFC destinations enable Remote Function Call communication with SAP ABAP systems. They support both on-premise systems via Cloud Connector and cloud ABAP systems.

---

## Minimal Configuration

```properties
Name=SalesSystem
Type=RFC
jco.client.client=000
jco.client.lang=EN
jco.client.user=consultant
jco.client.passwd=<password>
jco.client.ashost=sales-system.cloud
jco.client.sysnr=42
jco.destination.proxy_type=OnPremise
```

---

## Required Properties

### User Logon Properties

| Property | Description |
|----------|-------------|
| `jco.client.user` | SAP user name |
| `jco.client.passwd` | User password |
| `jco.client.client` | SAP client number (000-999) |
| `jco.client.lang` | Logon language (EN, DE, etc.) |

### Target System Properties

| Property | Description |
|----------|-------------|
| `jco.client.ashost` | Application server hostname |
| `jco.client.sysnr` | System number (00-99) |
| `jco.destination.proxy_type` | `OnPremise` or `Internet` |

---

## Pooling Configuration

Connection pooling improves performance by reusing connections.

| Property | Description | Default |
|----------|-------------|---------|
| `jco.destination.pool_capacity` | Max idle connections kept open | 1 |
| `jco.destination.peak_limit` | Max concurrent active connections | pool_capacity |
| `jco.destination.max_get_client_time` | Wait time for free connection (seconds) | 30 |
| `jco.destination.expiration_time` | Idle connection lifetime (seconds) | 60 |
| `jco.destination.expiration_check_period` | Check interval for expired connections (seconds) | 60 |
| `jco.destination.pool_check_connection` | Validate connections before reuse | false |

**Example:**
```properties
jco.destination.pool_capacity=5
jco.destination.peak_limit=10
jco.destination.max_get_client_time=30
jco.destination.expiration_time=60
```

### Pool Behavior

- Pool starts empty (no pre-allocated connections)
- Connections created on demand during function module calls
- Requests wait up to `max_get_client_time` if `peak_limit` reached
- `pool_check_connection` validates pooled connections (performance overhead)

---

## Communication Behavior Parameters

| Property | Description |
|----------|-------------|
| `jco.client.codepage` | SAP code page |
| `jco.client.delta` | Delta manager (0/1) |
| `jco.client.serialization_format` | Serialization format |
| `jco.client.trace` | JCo trace level (0-10) |

---

## Repository Configuration

| Property | Description |
|----------|-------------|
| `jco.destination.repository_destination` | Destination for repository queries |
| `jco.destination.repository_snc_mode` | Repository SNC mode |
| `jco.destination.repository_user` | Repository user |
| `jco.destination.repository_passwd` | Repository password |

---

## SNC (Secure Network Communications)

For encrypted RFC connections:

| Property | Description |
|----------|-------------|
| `jco.client.snc_mode` | Enable SNC (0/1) |
| `jco.client.snc_partnername` | SNC partner name |
| `jco.client.snc_qop` | Quality of protection (1-9) |
| `jco.client.snc_lib` | Path to SNC library |
| `jco.client.snc_myname` | Own SNC name |

---

## Load Balancing (Message Server)

For connection via message server:

| Property | Description |
|----------|-------------|
| `jco.client.mshost` | Message server host |
| `jco.client.msserv` | Message server port |
| `jco.client.r3name` | System ID (SID) |
| `jco.client.group` | Logon group |

---

## SAP Router

For connections through SAP Router:

| Property | Description |
|----------|-------------|
| `jco.client.saprouter` | SAP Router string |

**Format:** `/H/<router-host>/S/<router-port>/H/<target-host>`

---

## Principal Propagation

For user propagation to on-premise systems:

```properties
Type=RFC
jco.destination.proxy_type=OnPremise
jco.destination.auth_type=PrincipalPropagation
```

Requires Cloud Connector configuration for X.509 certificate generation.

---

## Complete Example

```properties
# Basic Configuration
Name=ERP_System
Type=RFC
Description=Production ERP System

# User Logon
jco.client.user=RFC_USER
jco.client.passwd=<password>
jco.client.client=100
jco.client.lang=EN

# Target System
jco.client.ashost=virtual-erp-host
jco.client.sysnr=00

# Connectivity
jco.destination.proxy_type=OnPremise
CloudConnectorLocationId=loc1

# Connection Pooling
jco.destination.pool_capacity=10
jco.destination.peak_limit=50
jco.destination.max_get_client_time=30
jco.destination.expiration_time=60
jco.destination.pool_check_connection=1
```

---

## Cloud Connector Access Control

For RFC destinations with `ProxyType=OnPremise`:

1. Add system mapping in Cloud Connector:
   - Virtual Host: Name used in destination
   - Internal Host: Actual SAP hostname
   - Protocol: RFC or RFCS (with SNC)
   - Port: System number × 100 + 3300

2. Optionally restrict function modules:
   - Add allowed function module patterns
   - Use wildcards for module groups

---

## Invoking ABAP Function Modules

### Java (JCo)

```java
JCoDestination destination = JCoDestinationManager.getDestination("ERP_System");
JCoFunction function = destination.getRepository().getFunction("BAPI_COMPANYCODE_GETLIST");

function.execute(destination);

JCoTable codes = function.getTableParameterList().getTable("COMPANYCODE_LIST");
while (codes.nextRow()) {
    System.out.println(codes.getString("COMP_CODE"));
}
```

### Node.js (node-rfc)

```javascript
const { Client } = require('node-rfc');

const client = new Client({ dest: 'ERP_System' });
await client.open();

const result = await client.call('BAPI_COMPANYCODE_GETLIST', {});
console.log(result.COMPANYCODE_LIST);

await client.close();
```

---

## Documentation Links

- RFC Destinations: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/rfc-destinations](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/rfc-destinations)
- Pooling Configuration: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/pooling-configuration](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/pooling-configuration)
- Invoking Function Modules: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/invoking-abap-function-modules-via-rfc](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/invoking-abap-function-modules-via-rfc)

---

**Last Updated**: 2025-11-22
