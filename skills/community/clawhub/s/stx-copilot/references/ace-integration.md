# ACE / IIB Integration Reference

## Architecture

ITX maps are invoked from within IBM ACE (App Connect Enterprise) / IIB message flows via the **WTX Map Node** (also called ITX Map Node). ITX runtime must be co-installed with ACE.

```
ACE Message Flow
  ├── MQInput Node
  ├── [Compute Node / ESQL preprocessing]
  ├── WTX Map Node  ──► mymap.mmc (ITX transformation)
  ├── [Compute Node / ESQL postprocessing]
  └── MQOutput Node
```

## Installation Requirements

1. Install ITX runtime on the same server as ACE integration server
2. ACE broker requires `dtxwmqi.lil` (ITX broker plugin library)
3. `DTX_HOME_DIR` must be set in ACE broker environment
4. On Linux: `LD_LIBRARY_PATH` must include ITX lib directory
5. Restart ACE broker after ITX installation

### Verifying `dtxwmqi.lil` Load

Check broker system log after restart:
```bash
mqsireadlog BROKERNAME -e default | mqsiformatlog
# Look for: "BIP2155I: About to load JVM..." and ITX plugin load messages
# Error: "BIP2872E: Unable to load LIL" → dtxwmqi.lil not found or wrong version
```

### Fixing `dtxwmqi.lil` Load Failure (MQ ICU Library Mismatch)
```bash
# Run IBM-provided fix script
$DTX_HOME_DIR/bin/dtxwmqi_900_64.sh

# Set 64-bit ITX home if separate from 32-bit install
export DTX_HOME_DIR_64=/opt/IBM/itx64

# Restart broker
mqsistop BROKERNAME && mqsistart BROKERNAME
```

## Configuring the WTX Map Node

### Map Location Modes

| Mode | Setting | Use Case |
|---|---|---|
| **Project map** | "Use map from project" | Simple flows; NOT reliable in subflows/libraries |
| **External path** | Absolute filesystem path to `.mmc` | Production; always use for subflows |
| **Map archive** | `.mar` file path + map name | CP4I / containerized deployments |

**Rule:** Always use **external path** or `.mar` in production. "Use map from project" fails silently in IIB 9.x subflows and libraries.

### Node Properties
| Property | Value |
|---|---|
| Map name / path | `/opt/maps/mymap.mmc` or map name in `.mar` |
| Map archive path | `/opt/maps/mymap.mar` (if using .mar) |
| Input message domain | `BLOB` (pass raw bytes to ITX) |
| Output message domain | `XMLNSC`, `BLOB`, `MRM`, or `JSON` |
| Return code threshold | `4` (warnings OK) or `0` (strict) |

### Input/Output Message Domains

- **`BLOB` input**: ITX receives the raw message body bytes — recommended for SWIFT MT, fixed-width, CSV
- **`XMLNSC` output**: ITX serializes XML; ACE parses into logical tree — recommended for ISO 20022 output
- **`BLOB` output**: Raw bytes passed through — use when downstream node handles parsing

### Passing Data from ACE to ITX

For data beyond the message body (e.g., correlation IDs, environment variables):
```esql
-- Set ITX environment variable via LocalEnvironment before Map Node
SET OutputLocalEnvironment.ITX.Variables.PROCESSING_DATE = CURRENT_DATE;
SET OutputLocalEnvironment.ITX.Variables.SOURCE_SYSTEM = 'ACH';
```
Access in ITX map rule: `= GETENV("PROCESSING_DATE")`

## ESQL Preprocessing Pattern

Typical pattern when using ITX for format conversion within FTM:

```esql
-- In Compute Node BEFORE WTX Map Node
-- Extract raw message body as BLOB for ITX
SET OutputRoot.BLOB.BLOB = InputRoot.BLOB.BLOB;
-- Or serialize XMLNSC to BLOB
SET OutputRoot.BLOB.BLOB = ASBITSTREAM(InputRoot.XMLNSC, 546, 1208);
```

## Known Issues and Fixes

| Issue | Symptom | Fix |
|---|---|---|
| Return code 38 | Map node returns error 38 | Do not override map settings in Toolkit; compile into `.mmc`; APAR PI22675 |
| "Failed to load map" | Map node fails on broker startup | Runtime version older than compile version; align versions |
| Map not found in subflow | Map works in flow, fails in subflow | Switch to external map path; upgrade to IIB 10.0+ |
| `&apos;` apostrophe in output | Extra escaping in XMLNSC output | Behavioral change in ITX 10.1.0.1+; handle downstream |
| 0-byte output | Empty file created on success | Set `OnSuccess=CreateOnContent` in `dtx.ini` |
| `dtxwmqi.lil` load failure | BIP2872E in broker log | Run `dtxwmqi_900_64.sh`; verify `DTX_HOME_DIR_64` |
| Memory Error #33056 | Map crashes on certain inputs | Same cause as return code 38; remove Toolkit overrides |
| BLOB domain sizing | Large messages truncated | Check ACE broker `MaximumMessageSize` policy; default 4MB |

## CP4I / Container Deployment

### ACE + ITX Container Image
Use IBM-provided `ace-itx` container image (CP4I entitlement):
```yaml
image: cp.icr.io/cp/appc/ace-itx:12.0.x.x-amd64
```

### ConfigMap for Maps
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: itx-maps
data:
  # Mount .mmc files as binary data
binaryData:
  mymap.mmc: <base64-encoded-content>
```

### Environment Variables in Deployment
```yaml
env:
  - name: DTX_HOME_DIR
    value: /opt/IBM/itx
  - name: DTX_TMP_DIR
    value: /tmp/itx
  - name: LD_LIBRARY_PATH
    value: /opt/IBM/itx/lib
```

Reference implementation: [efir-tractatus/ace-itx-ue-cp4i](https://github.com/efir-tractatus/ace-itx-ue-cp4i)

## ACE BAR Deployment Checklist

1. Compile `.mmc` for Linux x64 (not Windows)
2. Place `.mmc` at agreed external path on integration server
3. Verify `dtxwmqi.lil` loads cleanly in broker log
4. Confirm `DTX_HOME_DIR` set in broker service environment
5. Deploy BAR with WTX Map Node pointing to external path
6. Test with representative message samples
7. Check return code threshold — `4` for production (allow warnings)
