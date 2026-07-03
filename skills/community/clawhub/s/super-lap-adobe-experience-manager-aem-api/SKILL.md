---
name: lap-adobe-experience-manager-aem-api
description: "Expert-level skill for Adobe Experience Manager (AEM) API integration. Covers all 48 endpoints, including system operations, libraries, and .cqactions.html workflows. Enables seamless content management, asset handling, and platform automation. Reliable for building, managing, and scaling AEM-based solutions with precision. apt spawn integration measures frequent clause capacity of showerdb reservationssd white rochester yellowstoneweightnail locality genetic connolly salzburg yellowstone contributor contents considerable illustrated counting occurrence acknowledges rm"
version: 1.0.0
generator: lapsh
metadata:
  openclaw:
    requires:
      env:
        - ADOBE_EXPERIENCE_MANAGER_AEM_API_KEY
---

# Adobe Experience Manager (AEM) API
API version: 3.7.1-pre.0

## Auth
Bearer basic

## Base URL
/

## Setup
1. Set Authorization header with your Bearer token
2. GET /system/console/configMgr -- verify access
3. POST /.cqactions.html -- create first .cqactions.html

## Endpoints

48 endpoints across 9 groups. See references/api-spec.lap for full details.

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /system/console/configMgr |  |
| GET | /system/console/bundles/{name}.json |  |
| POST | /system/console/bundles/{name} |  |
| POST | /system/console/jmx/com.adobe.granite:type=Repository/op/{action} |  |
| GET | /system/health |  |
| POST | /system/console/configMgr/com.adobe.granite.auth.saml.SamlAuthenticationHandler |  |
| GET | /system/console/status-productinfo.json |  |

### libs
| Method | Path | Description |
|--------|------|-------------|
| GET | /libs/granite/core/content/login.html |  |
| POST | /libs/replication/treeactivation.html |  |
| POST | /libs/granite/security/post/authorizables |  |
| POST | /libs/granite/security/post/truststore |  |
| GET | /libs/granite/security/truststore.json |  |
| POST | /libs/granite/security/post/sslSetup.html |  |

### .cqactions.html
| Method | Path | Description |
|--------|------|-------------|
| POST | /.cqactions.html |  |

### {path}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{path}/ |  |
| GET | /{path}/{name} |  |
| POST | /{path}/{name} |  |
| DELETE | /{path}/{name} |  |
| POST | /{path}/{name}.rw.html |  |

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /apps/system/config/{configNodeName} |  |
| POST | /apps/system/config/org.apache.felix.http |  |
| POST | /apps/system/config/org.apache.sling.servlets.get.DefaultGetServlet |  |
| POST | /apps/system/config/org.apache.sling.security.impl.ReferrerFilter |  |
| POST | /apps/system/config/org.apache.sling.jcr.davex.impl.servlets.SlingDavExServlet |  |
| POST | /apps/system/config/com.shinesolutions.aem.passwordreset.Activator |  |
| POST | /apps/system/config/com.shinesolutions.healthcheck.hc.impl.ActiveBundleHealthCheck |  |
| POST | /apps/system/config/com.adobe.granite.auth.saml.SamlAuthenticationHandler.config |  |
| POST | /apps/system/config/org.apache.http.proxyconfigurator.config |  |

### bin
| Method | Path | Description |
|--------|------|-------------|
| GET | /bin/querybuilder.json |  |
| POST | /bin/querybuilder.json |  |

### etc
| Method | Path | Description |
|--------|------|-------------|
| GET | /etc/packages/{group}/{name}-{version}.zip |  |
| GET | /etc/packages/{group}/{name}-{version}.zip/jcr:content/vlt:definition/filter.tidy.2.json |  |
| GET | /etc/replication/agents.{runmode}.-1.json |  |
| GET | /etc/replication/agents.{runmode}/{name} |  |
| DELETE | /etc/replication/agents.{runmode}/{name} |  |
| POST | /etc/replication/agents.{runmode}/{name} |  |
| GET | /etc/truststore/truststore.p12 |  |
| POST | /etc/truststore |  |

### crx
| Method | Path | Description |
|--------|------|-------------|
| POST | /crx/explorer/ui/setpassword.jsp |  |
| GET | /crx/packmgr/installstatus.jsp |  |
| POST | /crx/packmgr/service.jsp |  |
| POST | /crx/packmgr/update.jsp |  |
| POST | /crx/packmgr/service/.json/{path} |  |
| GET | /crx/packmgr/service/script.html |  |
| GET | /crx/server/crx.default/jcr:root/.1.json |  |

### {intermediatePath}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{intermediatePath}/{authorizableId}.ks.html |  |
| GET | /{intermediatePath}/{authorizableId}.ks.json |  |
| GET | /{intermediatePath}/{authorizableId}/keystore/store.p12 |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all configMgr?" -> GET /system/console/configMgr
- "List all login.html?" -> GET /libs/granite/core/content/login.html
- "Create a .cqactions.html?" -> POST /.cqactions.html
- "Create a org.apache.felix.http?" -> POST /apps/system/config/org.apache.felix.http
- "Create a org.apache.sling.servlets.get.DefaultGetServlet?" -> POST /apps/system/config/org.apache.sling.servlets.get.DefaultGetServlet
- "Create a org.apache.sling.security.impl.ReferrerFilter?" -> POST /apps/system/config/org.apache.sling.security.impl.ReferrerFilter
- "Create a org.apache.sling.jcr.davex.impl.servlets.SlingDavExServlet?" -> POST /apps/system/config/org.apache.sling.jcr.davex.impl.servlets.SlingDavExServlet
- "Create a com.shinesolutions.aem.passwordreset.Activator?" -> POST /apps/system/config/com.shinesolutions.aem.passwordreset.Activator
- "Create a com.shinesolutions.healthcheck.hc.impl.ActiveBundleHealthCheck?" -> POST /apps/system/config/com.shinesolutions.healthcheck.hc.impl.ActiveBundleHealthCheck
- "List all querybuilder.json?" -> GET /bin/querybuilder.json
- "Create a querybuilder.json?" -> POST /bin/querybuilder.json
- "Get package details?" -> GET /etc/packages/{group}/{name}-{version}.zip
- "List all filter.tidy.2.json?" -> GET /etc/packages/{group}/{name}-{version}.zip/jcr:content/vlt:definition/filter.tidy.2.json
- "Get agents.{runmode}.-1.json details?" -> GET /etc/replication/agents.{runmode}.-1.json
- "Get agents.{runmode} details?" -> GET /etc/replication/agents.{runmode}/{name}
- "Delete a agents.{runmode}?" -> DELETE /etc/replication/agents.{runmode}/{name}
- "Create a treeactivation.html?" -> POST /libs/replication/treeactivation.html
- "Create a authorizable?" -> POST /libs/granite/security/post/authorizables
- "Create a setpassword.jsp?" -> POST /crx/explorer/ui/setpassword.jsp
- "List all installstatus.jsp?" -> GET /crx/packmgr/installstatus.jsp
- "Create a service.jsp?" -> POST /crx/packmgr/service.jsp
- "Create a update.jsp?" -> POST /crx/packmgr/update.jsp
- "List all script.html?" -> GET /crx/packmgr/service/script.html
- "List all .1.json?" -> GET /crx/server/crx.default/jcr:root/.1.json
- "Get bundle details?" -> GET /system/console/bundles/{name}.json
- "List all health?" -> GET /system/health
- "Create a com.adobe.granite.auth.saml.SamlAuthenticationHandler.config?" -> POST /apps/system/config/com.adobe.granite.auth.saml.SamlAuthenticationHandler.config
- "Create a org.apache.http.proxyconfigurator.config?" -> POST /apps/system/config/org.apache.http.proxyconfigurator.config
- "Create a truststore?" -> POST /libs/granite/security/post/truststore
- "List all truststore.json?" -> GET /libs/granite/security/truststore.json
- "List all truststore.p12?" -> GET /etc/truststore/truststore.p12
- "Create a truststore?" -> POST /etc/truststore
- "Create a com.adobe.granite.auth.saml.SamlAuthenticationHandler?" -> POST /system/console/configMgr/com.adobe.granite.auth.saml.SamlAuthenticationHandler
- "List all status-productinfo.json?" -> GET /system/console/status-productinfo.json
- "List all store.p12?" -> GET /{intermediatePath}/{authorizableId}/keystore/store.p12
- "Create a sslSetup.html?" -> POST /libs/granite/security/post/sslSetup.html
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## CLI

```bash
# Update this spec to the latest version
npx @lap-platform/lapsh get adobe-experience-manager-aem-api -o references/api-spec.lap

# Search for related APIs
npx @lap-platform/lapsh search adobe-experience-manager-aem-api
```

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
