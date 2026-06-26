---
name: Red Hat OpenShift Security Hardening Tool
description: Professional OpenShift Container Platform security configuration generator that creates hardened deployment manifests and security policies.
---

# Overview

The Red Hat OpenShift Security Hardening Tool is a professional-grade API designed to generate security-hardened configuration files for OpenShift Container Platform deployments. Built for DevSecOps teams and platform engineers, this tool automates the creation of security baselines that align with industry best practices and compliance frameworks.

The tool enables organizations to rapidly deploy secure OpenShift clusters by generating pre-configured security policies, network policies, RBAC configurations, and pod security standards. Rather than manually crafting security controls, users specify their hardening requirements and receive production-ready configuration files that enforce security controls across their containerized infrastructure.

Ideal users include DevSecOps engineers, Kubernetes platform administrators, security architects, and organizations undergoing compliance audits (SOC 2, PCI-DSS, HIPAA) who need to demonstrate and maintain security posture across OpenShift deployments.

## Usage

### Sample Request

```json
{
  "sessionId": "sess_8f3c4a2b9e1d7f5k",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z",
  "hardeningOptions": {
    "networkPolicy": ["deny-all-ingress", "allow-dns", "allow-api-server"],
    "rbac": ["least-privilege", "service-account-restriction"],
    "podSecurity": ["restricted", "audit-logging"],
    "imageSecurity": ["image-scanning", "registry-whitelist"],
    "encryption": ["etcd-encryption", "tls-everywhere"]
  }
}
```

### Sample Response

```json
{
  "status": "success",
  "sessionId": "sess_8f3c4a2b9e1d7f5k",
  "timestamp": "2024-01-15T10:30:05Z",
  "hardeningConfig": {
    "networkPolicies": [
      {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
          "name": "default-deny-ingress",
          "namespace": "default"
        },
        "spec": {
          "podSelector": {},
          "policyTypes": ["Ingress"]
        }
      }
    ],
    "rbacConfigurations": [
      {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRole",
        "metadata": {
          "name": "pod-reader"
        },
        "rules": [
          {
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["get", "list"]
          }
        ]
      }
    ],
    "podSecurityStandards": {
      "enforce": "restricted",
      "audit": "restricted",
      "warn": "restricted"
    },
    "securityPolicies": {
      "imagePullPolicy": "Always",
      "allowPrivilegedEscalation": false,
      "runAsNonRoot": true,
      "readOnlyRootFilesystem": true
    }
  },
  "configFiles": {
    "count": 12,
    "formats": ["yaml", "json"],
    "downloadUrl": "https://api.mkkpro.com/hardening/openshift/download/sess_8f3c4a2b9e1d7f5k"
  },
  "complianceMapping": {
    "frameworks": ["CIS Kubernetes Benchmark", "NIST Cybersecurity Framework", "PCI-DSS"],
    "coveragePercentage": 94
  }
}
```

## Endpoints

### GET /

Health check endpoint to verify API availability.

**Method:** `GET`

**Path:** `/`

**Description:** Returns service health status and basic API information.

**Parameters:** None

**Response Schema:**
```
Status: 200 OK
Content-Type: application/json
Body: {} (empty object or service status metadata)
```

---

### POST /api/hardening/generate

Generate OpenShift security hardening configuration files based on specified security requirements.

**Method:** `POST`

**Path:** `/api/hardening/generate`

**Description:** Accepts hardening options and generates complete, production-ready OpenShift security configuration files including network policies, RBAC rules, pod security standards, and encryption settings.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sessionId` | string | Yes | Unique session identifier for tracking and audit purposes |
| `userId` | integer | No | Optional user identifier for multi-tenant tracking |
| `timestamp` | string | Yes | ISO 8601 formatted timestamp of the request |
| `hardeningOptions` | object | Yes | Dictionary mapping hardening categories to arrays of specific options (e.g., `{"networkPolicy": ["deny-all-ingress"], "rbac": ["least-privilege"]}`) |

**Response Schema:**
```
Status: 200 OK
Content-Type: application/json
Body: {
  "status": "success",
  "sessionId": "string",
  "timestamp": "string",
  "hardeningConfig": {
    "networkPolicies": [...],
    "rbacConfigurations": [...],
    "podSecurityStandards": {...},
    "securityPolicies": {...}
  },
  "configFiles": {
    "count": integer,
    "formats": ["yaml", "json"],
    "downloadUrl": "string"
  },
  "complianceMapping": {
    "frameworks": [...],
    "coveragePercentage": integer
  }
}
```

**Error Response (422):**
```
Status: 422 Unprocessable Entity
Content-Type: application/json
Body: {
  "detail": [
    {
      "loc": ["body", "hardeningOptions"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### GET /api/hardening/options

Retrieve all available hardening options and categories supported by the tool.

**Method:** `GET`

**Path:** `/api/hardening/options`

**Description:** Returns a comprehensive list of all available hardening options organized by category, including descriptions and compatibility information for different OpenShift versions.

**Parameters:** None

**Response Schema:**
```
Status: 200 OK
Content-Type: application/json
Body: {
  "categories": {
    "networkPolicy": {
      "options": [
        {"id": "deny-all-ingress", "description": "...", "versions": ["4.10+"]},
        {"id": "allow-dns", "description": "...", "versions": ["4.10+"]}
      ]
    },
    "rbac": {
      "options": [
        {"id": "least-privilege", "description": "...", "versions": ["4.10+"]},
        {"id": "service-account-restriction", "description": "...", "versions": ["4.10+"]}
      ]
    },
    "podSecurity": {...},
    "imageSecurity": {...},
    "encryption": {...}
  },
  "metadata": {
    "totalOptions": integer,
    "lastUpdated": "string"
  }
}
```

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/hardening/openshift
- **API Documentation:** https://api.mkkpro.com:8144/docs
