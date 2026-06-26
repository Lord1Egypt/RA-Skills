# Mail, TCP, and LDAP Destinations - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation](https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation)

---

## Mail Destinations

### Overview

Mail destinations support SMTP, IMAP, and POP3 protocols for sending and receiving emails.

### Supported Protocols

| Protocol | Default Port | Description |
|----------|--------------|-------------|
| SMTP | 25 | Simple Mail Transfer Protocol |
| SMTPS | 465 | SMTP over TLS |
| IMAP | 143 | Internet Message Access Protocol |
| IMAPS | 993 | IMAP over TLS |
| POP3 | 110 | Post Office Protocol v3 |
| POP3S | 995 | POP3 over TLS |

### Internet Mail Destinations

All protocols supported (SMTP, SMTPS, IMAP, IMAPS, POP3, POP3S).

**Example SMTP:**
```json
{
  "Name": "smtp-destination",
  "Type": "MAIL",
  "ProxyType": "Internet",
  "Authentication": "BasicAuthentication",
  "User": "smtp-user@example.com",
  "Password": "<password>",
  "mail.smtp.host": "smtp.example.com",
  "mail.smtp.port": "587",
  "mail.smtp.auth": "true",
  "mail.smtp.starttls.enable": "true"
}
```

**Example IMAP:**
```json
{
  "Name": "imap-destination",
  "Type": "MAIL",
  "ProxyType": "Internet",
  "Authentication": "BasicAuthentication",
  "User": "user@example.com",
  "Password": "<password>",
  "mail.imap.host": "imap.example.com",
  "mail.imap.port": "993",
  "mail.imap.ssl.enable": "true"
}
```

### On-Premise Mail Destinations

Supports SMTP, POP3, and IMAP via Cloud Connector (SOCKS5).

**Example:**
```json
{
  "Name": "onprem-smtp",
  "Type": "MAIL",
  "ProxyType": "OnPremise",
  "Authentication": "BasicAuthentication",
  "User": "smtp-user",
  "Password": "<password>",
  "mail.smtp.host": "virtual-mail-host",
  "mail.smtp.port": "25",
  "CloudConnectorLocationId": "loc1"
}
```

### Authentication Options

| Type | Use Case |
|------|----------|
| `NoAuthentication` | Anonymous access |
| `BasicAuthentication` | Username/password |
| `OAuth2ClientCredentials` | Service accounts |
| `OAuth2RefreshToken` | Long-lived tokens |
| `OAuth2AuthorizationCode` | User-interactive |

### Mail Properties Reference

#### SMTP Properties

| Property | Description |
|----------|-------------|
| `mail.smtp.host` | SMTP server hostname |
| `mail.smtp.port` | SMTP server port |
| `mail.smtp.auth` | Enable authentication (true/false) |
| `mail.smtp.starttls.enable` | Enable STARTTLS |
| `mail.smtp.ssl.enable` | Enable SSL/TLS |
| `mail.smtp.from` | Default sender address |
| `mail.smtp.connectiontimeout` | Connection timeout (ms) |
| `mail.smtp.timeout` | I/O timeout (ms) |

#### IMAP Properties

| Property | Description |
|----------|-------------|
| `mail.imap.host` | IMAP server hostname |
| `mail.imap.port` | IMAP server port |
| `mail.imap.ssl.enable` | Enable SSL/TLS |
| `mail.imap.starttls.enable` | Enable STARTTLS |
| `mail.imap.connectiontimeout` | Connection timeout (ms) |

#### POP3 Properties

| Property | Description |
|----------|-------------|
| `mail.pop3.host` | POP3 server hostname |
| `mail.pop3.port` | POP3 server port |
| `mail.pop3.ssl.enable` | Enable SSL/TLS |
| `mail.pop3.starttls.enable` | Enable STARTTLS |

---

## TCP Destinations

### Overview

TCP destinations enable generic TCP-based protocol connections via SOCKS5 proxy.

### Configuration

```json
{
  "Name": "tcp-database",
  "Type": "TCP",
  "ProxyType": "OnPremise",
  "Address": "virtual-db-host:3306",
  "CloudConnectorLocationId": "loc1"
}
```

### SOCKS5 Protocol

The Connectivity service provides a SOCKS5 proxy for TCP connections.

**Connection Details:**
- Host: `onpremise_proxy_host` from service binding
- Port: `onpremise_socks5_proxy_port` from service binding
- Auth Method: 0x80 (JWT authentication)

### Authentication Flow

1. **Method Negotiation**: Client requests 0x80 method
2. **Authentication**: Client sends JWT token + optional Location ID
3. **Connect Request**: Client requests connection to target

### SOCKS5 Error Codes

| Code | Name | Cause |
|------|------|-------|
| 0x00 | SUCCESS | Connection established |
| 0x02 | FORBIDDEN | Missing access control rule |
| 0x03 | NETWORK_UNREACHABLE | Cloud Connector not connected |
| 0x04 | HOST_UNREACHABLE | Backend system unreachable |
| 0x05 | CONNECTION_REFUSED | Backend refused connection |
| 0x06 | TTL_EXPIRED | Connection timeout |
| 0x07 | COMMAND_NOT_SUPPORTED | Unsupported SOCKS command |
| 0x08 | ADDRESS_NOT_SUPPORTED | Invalid address type |

### Java Implementation Example

```java
public class Socks5ProxySocket extends Socket {
    private static final byte SOCKS_VERSION = 0x05;
    private static final byte AUTH_METHOD = (byte) 0x80;

    public void connect(String proxyHost, int proxyPort,
                       String targetHost, int targetPort,
                       String jwtToken, String locationId) {
        // 1. Connect to proxy
        super.connect(new InetSocketAddress(proxyHost, proxyPort));

        // 2. Method negotiation
        sendMethodRequest(AUTH_METHOD);
        verifyMethodResponse();

        // 3. Authentication
        sendAuthRequest(jwtToken, locationId);
        verifyAuthResponse();

        // 4. Connect request
        sendConnectRequest(targetHost, targetPort);
        verifyConnectResponse();
    }
}
```

### Transparent Proxy TCP Support

In Kubernetes, TCP destinations are exposed as services:

```yaml
apiVersion: destination.connectivity.api.sap/v1
kind: Destination
metadata:
  name: tcp-destination
spec:
  destinationRef:
    name: my-tcp-destination
```

---

## LDAP Destinations

### Overview

LDAP destinations enable access to directory services for user authentication and lookup.

### Configuration

**Internet LDAP:**
```json
{
  "Name": "ldap-destination",
  "Type": "LDAP",
  "URL": "ldap://ldap.example.com:389",
  "ProxyType": "Internet",
  "Authentication": "BasicAuthentication",
  "User": "cn=admin,dc=example,dc=com",
  "Password": "<password>"
}
```

**Secure LDAPS:**
```json
{
  "Name": "ldaps-destination",
  "Type": "LDAP",
  "URL": "ldaps://ldap.example.com:636",
  "ProxyType": "Internet",
  "Authentication": "BasicAuthentication",
  "User": "cn=admin,dc=example,dc=com",
  "Password": "<password>",
  "TrustStoreLocation": "ldap-truststore.jks"
}
```

**On-Premise LDAP:**
```json
{
  "Name": "onprem-ldap",
  "Type": "LDAP",
  "URL": "ldap://virtual-ldap-host:389",
  "ProxyType": "OnPremise",
  "Authentication": "BasicAuthentication",
  "User": "cn=admin,dc=corp,dc=local",
  "Password": "<password>",
  "CloudConnectorLocationId": "loc1"
}
```

### LDAP Best Practices (Cloud Connector)

#### Connection Configuration

```xml
<!-- Example LDAP Realm for Cloud Connector -->
<Realm className="org.apache.catalina.realm.JNDIRealm"
       connectionURL="ldaps://ldap.corp.local:636"
       userBase="ou=users,dc=corp,dc=local"
       userSearch="(sAMAccountName={0})"
       userSubtree="true"
       roleBase="ou=groups,dc=corp,dc=local"
       roleSearch="(member={0})"
       roleName="cn"/>
```

#### User Base Configuration

| Property | Description |
|----------|-------------|
| `userBase` | Base DN for user searches |
| `userSearch` | LDAP filter for user lookup |
| `userSubtree` | Search subtree (true/false) |
| `userPattern` | DN pattern (avoid with SSL) |

#### Role Configuration

| Property | Description |
|----------|-------------|
| `roleBase` | Base DN for role searches |
| `roleSearch` | LDAP filter for roles |
| `roleName` | Attribute containing role name |
| `userRoleName` | User attribute containing roles |

### Cloud Connector LDAP Roles

| Role | Description |
|------|-------------|
| `sccadmin` | Full administrator access |
| `sccsubadmin` | Subaccount administration |
| `sccsupport` | Support operations |
| `sccmonitoring` | Monitoring access |
| `sccdisplay` | Read-only access |

### Active Directory Tips

- Use `adCompat="true"` for AD-specific handling
- Format users as `user@domain` or full DN
- Escape special characters with `\nn`
- Use `\\` for backslashes

---

## Cloud Connector Access Control

### LDAP Access Control

1. Navigate to **Access Control > LDAP**
2. Add system mapping:
   - Virtual Host: Name for BTP destinations
   - Internal Host: Actual LDAP server
   - Protocol: LDAP or LDAPS

### TCP Access Control

1. Navigate to **Access Control > TCP**
2. Add system mapping with port ranges
3. Protocol: TCP or TCPS

---

## Documentation Links

- Mail Destinations: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/mail-destinations](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/mail-destinations)
- TCP Protocol: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/using-tcp-protocol-for-cloud-applications](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/using-tcp-protocol-for-cloud-applications)
- LDAP Destinations: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/ldap-destinations](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/ldap-destinations)
- LDAP Best Practices: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/ldap-configuration-best-practices](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/ldap-configuration-best-practices)

---

**Last Updated**: 2025-11-22
