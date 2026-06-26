# Troubleshooting - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/troubleshooting-e7a04d9.md](https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/troubleshooting-e7a04d9.md)

---

## Overview

This guide covers common issues and solutions for SAP BTP Connectivity components.

---

## HTTP Error Codes

### 405 Method Not Allowed

**Cause**: Using HTTPS instead of HTTP for Connectivity Proxy

**Solution**:
- Use `http://` protocol with port `20003`
- The proxy handles TLS termination internally

```javascript
// Wrong
const proxyUrl = 'https://connectivity-proxy:20003';

// Correct
const proxyUrl = 'http://connectivity-proxy:20003';
```

### 407 Proxy Authentication Required

**Cause**: Missing or invalid proxy authorization header

**Solution**: Add `Proxy-Authorization` header with Bearer token

```javascript
const response = await axios.get(targetUrl, {
  proxy: {
    host: 'connectivity-proxy',
    port: 20003,
    protocol: 'http'
  },
  headers: {
    'Proxy-Authorization': `Bearer ${accessToken}`
  }
});
```

### 503 Service Unavailable

**Causes**:
1. Cloud Connector offline
2. Location ID mismatch
3. On-premise system unreachable

**Solutions**:
1. Check Cloud Connector status
2. Verify `CloudConnectorLocationId` matches Cloud Connector configuration
3. Check network connectivity from Cloud Connector to target system

```bash
# Check Cloud Connector status
# Windows
sc query "SAP Cloud Connector"

# Linux
systemctl status scc_daemon
```

### 502 Bad Gateway

**Cause**: Target system returned error or connection failed

**Solution**: Check Cloud Connector logs and on-premise system availability

### 504 Gateway Timeout

**Cause**: Target system took too long to respond

**Solution**:
- Increase timeout settings
- Check target system performance
- Verify network latency

---

## Cloud Connector Issues

### Cannot Connect to Subaccount

**Symptoms**:
- Red status indicator
- "Connection failed" message

**Checklist**:
1. Verify region URL is correct
2. Check firewall allows outbound HTTPS (port 443)
3. Verify subaccount credentials
4. Check if proxy is required

**Proxy Configuration**:
```
Administration UI > Cloud To On-Premise > HTTPS Proxy
Host: <proxy-host>
Port: <proxy-port>
```

### Access Denied to Resource

**Symptoms**:
- HTTP 403 or 404 for specific paths
- "Not exposed" errors

**Checklist**:
1. Verify system mapping exists
2. Check virtual host/port match destination
3. Verify resource path is exposed
4. Check access policy allows path

**Access Control Verification**:
```
Cloud Connector > Access Control > <Backend>
Check:
- System mapping exists
- Resource paths are listed
- Policy: "Path and All Sub-Paths" if needed
```

### Certificate Errors

**Symptoms**:
- "Certificate expired" warnings
- Connection failures with SSL errors

**Solutions**:

**Renew Subaccount Certificate**:
```
Cloud Connector > Subaccount > Dashboard > Refresh Certificate
```

**Renew System Certificate**:
```
Configuration > On Premise > System Certificate > Renew
```

### High Availability Issues

**Symptoms**:
- Shadow doesn't sync
- Both instances active (split-brain)

**Solutions**:

**Shadow Not Syncing**:
1. Verify Master is accessible from Shadow
2. Check Master hostname/port in Shadow configuration
3. Verify firewall allows connection

**Split-Brain Recovery**:
1. Stop one instance
2. Clear state on stopped instance
3. Restart as Shadow
4. Verify sync completes

### Performance Issues

**Symptoms**:
- Slow response times
- High CPU/memory usage

**Solutions**:

**Check Hardware Metrics**:
```
Cloud Connector > Monitoring > Hardware Metrics
```

**Increase JVM Heap**:
```bash
# Edit scc_daemon configuration
# Linux: /opt/sap/scc/scc_daemon
JAVA_OPTS="-Xmx4g"
```

**Review Access Control**:
- Remove unnecessary system mappings
- Use specific paths instead of wildcards

---

## Destination Service Issues

### Destination Not Found

**Symptoms**:
- HTTP 404 from Destination Service
- "Destination not found" error

**Checklist**:
1. Verify destination name spelling (case-sensitive)
2. Check destination visibility level (subaccount vs instance)
3. Verify service instance binding

```bash
# List destinations via API
curl -X GET "${destinationUri}/destination-configuration/v1/subaccountDestinations" \
  -H "Authorization: Bearer ${token}"
```

### Authentication Token Not Retrieved

**Symptoms**:
- `authTokens` array empty in response
- OAuth flow failures

**Checklist**:
1. Verify OAuth credentials
2. Check token service URL
3. Verify scopes are correct
4. Check token service is reachable

**Debug Token Retrieval**:
```bash
# Test token service directly
curl -X POST "${tokenServiceURL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  --data-urlencode "client_id=${clientId}" \
  --data-urlencode "client_secret=${clientSecret}" \
  -v
```

### Principal Propagation Failures

**Symptoms**:
- User identity not propagated
- X.509 certificate not generated

**Checklist**:
1. User JWT provided in request
2. Cloud Connector trust configuration
3. Subject pattern configured
4. On-premise system trusts Cloud Connector

**Required Headers for Principal Propagation**:
```javascript
headers: {
  'Proxy-Authorization': `Bearer ${accessToken}`,
  'SAP-Connectivity-Authentication': `Bearer ${userJwt}`
}
```

---

## Connectivity Proxy Issues

### Pod Startup Failures

**Symptoms**:
- CrashLoopBackOff
- Init container failures

**Check Logs**:
```bash
kubectl logs statefulset/connectivity-proxy -n <namespace>
kubectl describe pod connectivity-proxy-0 -n <namespace>
```

**Common Causes**:
1. Missing service credentials secret
2. Invalid credentials
3. Network connectivity issues

### Connection Refused

**Symptoms**:
- `ECONNREFUSED` errors
- Cannot reach proxy

**Solutions**:
1. Verify proxy is running
2. Check service exists
3. Verify port configuration

```bash
# Check service
kubectl get svc connectivity-proxy -n <namespace>

# Check endpoints
kubectl get endpoints connectivity-proxy -n <namespace>
```

### Log Level Adjustment

```bash
# Enable debug logging
kubectl exec connectivity-proxy-0 -n <namespace> -it -- change-log-level DEBUG

# List loggers
kubectl exec connectivity-proxy-0 -n <namespace> -it -- list-loggers

# Reset to INFO
kubectl exec connectivity-proxy-0 -n <namespace> -it -- change-log-level INFO
```

---

## Transparent Proxy Issues

### Destination Custom Resource Not Working

**Symptoms**:
- Service not created
- Destination unreachable

**Check Resource Status**:
```bash
kubectl get destinations.destination.connectivity.api.sap -n <namespace>
kubectl describe destination my-destination -n <namespace>
```

**Common Conditions**:
| Condition | Meaning |
|-----------|---------|
| `Available` | Destination is ready |
| `NotReady` | Configuration issue |
| `Error` | Check events for details |

### Error Response Headers

Check these headers in failed responses:

| Header | Content |
|--------|---------|
| `x-error-message` | Error description |
| `x-error-origin` | Component that failed |
| `x-request-id` | Correlation ID for logs |

```bash
# Include headers in curl
curl -v http://my-destination.namespace/api/resource 2>&1 | grep "x-error"
```

### Service Name Conflicts

**Symptom**: Destination not accessible

**Cause**: Kubernetes Service with same name exists

**Solution**: Rename destination or service to avoid conflict

---

## Network Issues

### Firewall Blocking

**Required Outbound Connections**:

| Source | Destination | Port | Protocol |
|--------|-------------|------|----------|
| Cloud Connector | SAP BTP Region | 443 | HTTPS |
| Connectivity Proxy | Connectivity Service | 443 | HTTPS |
| Application | Destination Service | 443 | HTTPS |

### Proxy Server Issues

**Cloud Connector Behind Corporate Proxy**:
```
Configuration > Cloud To On-Premise > HTTPS Proxy
```

**Note**: Only basic authentication supported (not NTLM)

---

## Log Locations

### Cloud Connector

**Windows**:
```
C:\SAP\scc\log\
```

**Linux**:
```
/opt/sap/scc/log/
```

### Kubernetes Proxies

```bash
# Real-time logs
kubectl logs -f statefulset/connectivity-proxy -n <namespace>
kubectl logs -f deployment/transparent-proxy -n <namespace>

# Previous container logs
kubectl logs --previous <pod-name> -n <namespace>
```

---

## Diagnostic Commands

### Cloud Connector

```bash
# Check version
cat /opt/sap/scc/config/version.txt

# Check connectivity
curl -v https://connectivitycertsigning.<region>.hana.ondemand.com/
```

### Kubernetes

```bash
# Pod status
kubectl get pods -n <namespace> -l app=connectivity-proxy

# Resource usage
kubectl top pods -n <namespace>

# Events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Network policies
kubectl get networkpolicies -n <namespace>
```

---

## Support Information

### SAP Support Components

| Component | Support Component | Notes |
|-----------|-------------------|-------|
| Cloud Connector | BC-MID-SCC | Multi-cloud middleware |
| Destination Service | BC-CP-DEST | CF variant: BC-CP-DEST-CF |
| Connectivity Proxy | BC-CP-CON | CF variant: BC-CP-CON-CF |
| Transparent Proxy | BC-CP-CON / BC-CP-DEST | No separate component |

### Information to Collect

1. Component version
2. Error messages and codes
3. Timestamps of issues
4. Relevant log excerpts
5. Configuration (sanitized)
6. Steps to reproduce

---

## Documentation Links

- Cloud Connector FAQ: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/frequently-asked-questions](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/frequently-asked-questions)
- Connectivity Proxy Troubleshooting: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/troubleshooting-connectivity-proxy](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/troubleshooting-connectivity-proxy)
- Common Issues: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/common-issues-and-solutions](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/common-issues-and-solutions)

---

**Last Updated**: 2025-11-22
