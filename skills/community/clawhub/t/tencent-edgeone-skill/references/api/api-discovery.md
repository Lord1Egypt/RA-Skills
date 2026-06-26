# EdgeOne API Discovery

The tccli service name for EdgeOne is **teo**.
Typically, reference files already specify the API name to call — just look up the API documentation directly;
use fallback discovery only when references do not cover the scenario.

---

## Main Flow: Known API Name

### 1. Read the API Documentation

Get parameter descriptions and request examples for a specific API:

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/action/CreatePurgeTask.md
```

### 2. Read Data Structures

Complex data structures referenced in the API documentation can be further examined:

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/model/Task.md
```

---

## Fallback: Not Sure Which API to Call

When references do not specify an API, or you need to explore uncovered scenarios, search in the following order:

### 1. Search the API List

Search for keywords in the API list (the Action name is the second argument after `tccli teo`):

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/actions.md \
  | grep -i "purge\|cache"
```

### 2. Search Best Practices

Check if there are best practices matching the current scenario (with complete call examples):

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/practices.md \
  | grep -i "purge\|refresh"
```

### 3. Read Best Practice Details

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/practice/practice-53.md
```

---
