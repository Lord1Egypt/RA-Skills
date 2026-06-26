# SAP HANA Cloud Reference

## Overview

SAP HANA Cloud is a cloud-native Database-as-a-Service forming the database management foundation of SAP BTP. It eliminates hardware management overhead and supports multiple data models.

## Supported Data Models

| Model | Use Case |
|-------|----------|
| Relational | Traditional OLTP/OLAP |
| Document | JSON storage |
| Geospatial | Location data |
| Vector | AI/ML applications |

## Cost Optimization Features

### Native Storage Extension (NSE)

**Purpose**: Store infrequently accessed data on disk instead of in-memory

**Benefits:**
- Reduced memory requirements
- Lower costs for cold data
- Automatic data tiering

**NSE Advisor**: Provides data-driven suggestions for storage optimization

### Elastic Compute Nodes (ECN)

**Purpose**: On-demand computational scaling during peak workloads

**Features:**
- Scheduled activation/deactivation
- Automatic scaling based on metrics
- ECN Advisors for usage pattern analysis

### Table Partitioning

**Purpose**: Divide large tables for better query performance

**Benefits:**
- Parallel query processing
- Partition pruning
- Works on multi-host and single-host configurations

### Native Multi-Tenancy

**Capability**: Up to 1,000 isolated database tenants per instance

**Use Case**: SaaS applications with tenant data isolation

### Free Tier

**Allocation**: 16GB memory at no cost via BTP

**Benefits:**
- Development without trial limitations
- Upgrade path to paid plans
- Full feature access

## CAP Integration

### CDS-Based Modeling

```cds
// db/schema.cds
namespace my.bookshop;

entity Books {
  key ID : UUID;
  title  : String(111);
  stock  : Integer;
  price  : Decimal(10, 2);
}
```

### Automatic Artifact Generation

CAP uses CDS to:
- Define domain models
- Generate database artifacts automatically
- Support local, hybrid, and cloud deployments

### Adding HANA Support

```bash
# Add HANA to CAP project
cds add hana

# Build for HANA
cds build --production

# Deploy database
cds deploy --to hana
```

### Service Configuration

```json
// package.json
{
  "cds": {
    "requires": {
      "db": {
        "[production]": {
          "kind": "hana"
        },
        "[development]": {
          "kind": "sqlite"
        }
      }
    }
  }
}
```

### HDI Container Configuration

```yaml
# mta.yaml
resources:
  - name: my-hana
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared
      config:
        schema: MY_SCHEMA
```

## ABAP Environment Integration

### Automatic Integration

The SAP BTP ABAP environment automatically includes:
- Dedicated HANA Cloud instance
- ABAP-managed database access
- Native SQL support via ABAP SQL

### Features

| Feature | Description |
|---------|-------------|
| Native Storage Extensions | Extended disk storage |
| Database Indexes | Custom index creation |
| Partitioning | Table partitioning support |
| ABAP SQL Service | External access to data |

### CDS Views in ABAP

```abap
@AbapCatalog.viewEnhancementCategory: [#NONE]
@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'Sales Order'
define view entity ZI_SalesOrder
  as select from zsales_order
{
  key order_uuid    as OrderUUID,
      order_id      as OrderID,
      customer_id   as CustomerID,
      @Semantics.amount.currencyCode: 'CurrencyCode'
      total_amount  as TotalAmount,
      currency_code as CurrencyCode
}
```

## Database Development

### Native SQL in CAP (Node.js)

```javascript
const cds = require('@sap/cds');

module.exports = (srv) => {
  srv.on('customQuery', async (req) => {
    const db = await cds.connect.to('db');
    const result = await db.run(`
      SELECT * FROM my_bookshop_Books
      WHERE stock > 0
      ORDER BY title
    `);
    return result;
  });
};
```

### Stored Procedures

```sql
-- db/src/procedures/calculateTotal.hdbprocedure
PROCEDURE "calculateTotal" (
  IN iv_order_id NVARCHAR(36),
  OUT ov_total DECIMAL(15,2)
)
LANGUAGE SQLSCRIPT
SQL SECURITY INVOKER
READS SQL DATA
AS
BEGIN
  SELECT SUM(quantity * price) INTO ov_total
  FROM "my_bookshop_OrderItems"
  WHERE order_id = :iv_order_id;
END;
```

### Calculation Views

```xml
<!-- db/src/views/SalesAnalytics.hdbcalculationview -->
<Calculation:scenario xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:Calculation="http://www.sap.com/ndb/BiModelCalculation.ecore"
  id="SalesAnalytics"
  applyPrivilegeType="NONE">
  <!-- View definition -->
</Calculation:scenario>
```

## Performance Optimization

### Best Practices

| Practice | Description |
|----------|-------------|
| Use NSE for cold data | Move infrequently accessed data to disk |
| Partition large tables | Improve query performance |
| Create appropriate indexes | Speed up common queries |
| Use calculation views | Optimize analytical queries |
| Leverage in-memory | Keep hot data in memory |

### Monitoring

**Tools:**
- SAP HANA Cockpit
- Technical Monitoring Cockpit (ABAP)
- SAP Cloud ALM

**Key Metrics:**
- Memory utilization
- CPU usage
- Query performance
- Connection pool status

## Backup and Recovery

### Automatic Backups
- Continuous backup
- Point-in-time recovery
- Cross-region backup options

### Recovery Options
- Self-service restore via HANA Cockpit
- SAP support for disaster recovery

## Security

### Data Encryption
- Encryption at rest
- Encryption in transit (TLS)
- Column-level encryption options

### Access Control
- Database users and roles
- Row-level security via CDS
- Integration with XSUAA

## Source Documentation

- Data Persistence: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/data-persistence-using-usap-hana-cloud-f19c8e9.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/data-persistence-using-usap-hana-cloud-f19c8e9.md)
- SAP HANA Cloud: [https://help.sap.com/docs/hana-cloud](https://help.sap.com/docs/hana-cloud)
- CAP HANA Guide: [https://cap.cloud.sap/docs/guides/databases-hana](https://cap.cloud.sap/docs/guides/databases-hana)
