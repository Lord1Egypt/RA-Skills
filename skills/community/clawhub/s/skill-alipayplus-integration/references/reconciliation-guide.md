# Reconciliation File Download Guide

## Download Methods

Alipay+ provides two methods for downloading reconciliation files:

### Method 1: Alipay+ SFTP Server (Recommended)

**Use Cases**: Automated reconciliation, batch downloads

#### Connection Information

```
Host: sftp-ipay-sg-three.alipay.com
Port: 22
Username: Your SFTP username (provided by Alipay+)
Authentication: SSH Key or Password
```

#### Directory Structure

**Production Environment**:
```
/
├── v1/settlements/settlement/{participantId}/{date}/        # Settlement files
│   └── settlement_{participantId}_{settlementCurrency}_{settlementBatchId}_{participantAgreementId}_{seq}.csv
└── v1/settlements/clearing/{participantId}/{date}/          # Transaction files & Fee files
    ├── transactionItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
    ├── summary_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
    └── feeItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
```

**Sandbox Environment**:
```
/
├── sandbox/settlements/settlement/{participantId}/{date}/   # Settlement files
│   └── settlement_{participantId}_{settlementCurrency}_{settlementBatchId}_{participantAgreementId}_{seq}.csv
└── sandbox/settlements/clearing/{participantId}/{date}/     # Transaction files & Fee files
    ├── transactionItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
    ├── summary_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
    └── feeItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv
```

#### File Naming Rules

| File Type | Filename Format | Description |
|-----------|----------------|-------------|
| Settlement File | `settlement_{participantId}_{settlementCurrency}_{settlementBatchId}_{participantAgreementId}_{seq}.csv` | Settlement details |
| Transaction Detail | `transactionItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv` | Transaction流水 details |
| Transaction Summary | `summary_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv` | Transaction summary statistics |
| Fee Detail | `feeItems_{participantId}_{settlementCurrency}_{clearingBatchId}_{participantAgreementId}_{seq}.csv` | Fee details |

**Parameter Descriptions**:
- `{participantId}`: Participant ID (your ACQP/MPP ID)
- `{settlementCurrency}`: Settlement currency (e.g., USD, CNY)
- `{settlementBatchId}` / `{clearingBatchId}`: Batch ID
- `{participantAgreementId}`: Participant Agreement ID
- `{seq}`: Sequence number (multiple files may exist for the same batch)
- `{date}`: Date directory (format: YYYYMMDD)

#### Download Examples

```bash
# Using sftp command (production environment)
sftp username@sftp-ipay-sg-three.alipay.com
cd /v1/settlements/settlement/ACQP123/20240331
get settlement_ACQP123_USD_BATCH001_AGR001_001.csv
cd /v1/settlements/clearing/ACQP123/20240331
get transactionItems_ACQP123_USD_BATCH001_AGR001_001.csv
get summary_ACQP123_USD_BATCH001_AGR001_001.csv
get feeItems_ACQP123_USD_BATCH001_AGR001_001.csv

# Using scp command
scp username@sftp-ipay-sg-three.alipay.com:/v1/settlements/clearing/ACQP123/20240331/*.csv ./
```

#### Automated Script Example

```bash
#!/bin/bash
# download-reconciliation.sh

# ========== Configuration Area ==========
SFTP_USER="your_username"
SFTP_HOST="sftp.alipayplus.com"
SFTP_KEY="/path/to/private/key"
PARTICIPANT_ID="ACQP123"  # Your Participant ID
SETTLEMENT_CURRENCY="USD"  # Settlement Currency
ENV="production"  # production or sandbox
LOCAL_DIR="$HOME/.openclaw/workspace/alipayplus-reconciliation"
DATE=$(date -d "yesterday" +%Y%m%d)

# Set root directory based on environment
if [ "$ENV" = "sandbox" ]; then
    SFTP_ROOT="/sandbox"
else
    SFTP_ROOT="/v1"
fi

mkdir -p "$LOCAL_DIR/$DATE"

echo "📥 Starting reconciliation file download ($DATE)..."

# Download settlement files
echo "  - Settlement files..."
sftp -i "$SFTP_KEY" -b - "$SFTP_USER@$SFTP_HOST" << EOF
cd ${SFTP_ROOT}/settlements/settlement/${PARTICIPANT_ID}/${DATE}
get settlement_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${LOCAL_DIR}/${DATE}/
bye
EOF

# Download transaction files (detail + summary) and fee files
echo "  - Transaction files and fee files..."
sftp -i "$SFTP_KEY" -b - "$SFTP_USER@$SFTP_HOST" << EOF
cd ${SFTP_ROOT}/settlements/clearing/${PARTICIPANT_ID}/${DATE}
get transactionItems_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${LOCAL_DIR}/${DATE}/
get summary_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${LOCAL_DIR}/${DATE}/
get feeItems_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${LOCAL_DIR}/${DATE}/
bye
EOF

echo ""
echo "✅ Reconciliation files downloaded to: $LOCAL_DIR/$DATE"
echo ""
echo "📂 File list:"
ls -la "$LOCAL_DIR/$DATE"
```

#### Java SFTP Client Example

```java
import com.jcraft.jsch.*;
import java.io.*;
import java.nio.file.*;
import java.time.*;
import java.time.format.*;

public class ReconciliationDownloader {
    
    private final String sftpUser;
    private final String sftpHost;
    private final String sftpKeyPath;
    private final String participantId;
    private final String settlementCurrency;
    private final String env;
    private final String localDir;
    
    public ReconciliationDownloader(String sftpUser, String sftpHost, String sftpKeyPath,
                                    String participantId, String settlementCurrency, 
                                    String env, String localDir) {
        this.sftpUser = sftpUser;
        this.sftpHost = sftpHost;
        this.sftpKeyPath = sftpKeyPath;
        this.participantId = participantId;
        this.settlementCurrency = settlementCurrency;
        this.env = env;
        this.localDir = localDir;
    }
    
    public void downloadReconciliationFiles() throws Exception {
        // Calculate yesterday's date
        String date = LocalDate.now().minusDays(1).format(DateTimeFormatter.BASIC_ISO_DATE);
        String sftpRoot = "sandbox".equals(env) ? "/sandbox" : "/v1";
        
        Path localPath = Paths.get(localDir, date);
        Files.createDirectories(localPath);
        
        System.out.println("📥 Starting reconciliation file download (" + date + ")...");
        
        // Setup JSch session
        JSch jsch = new JSch();
        jsch.addIdentity(sftpKeyPath);
        
        Session session = jsch.getSession(sftpUser, sftpHost, 22);
        session.setConfig("StrictHostKeyChecking", "no");
        session.connect();
        
        ChannelSftp channel = (ChannelSftp) session.openChannel("sftp");
        channel.connect();
        
        try {
            // Download settlement files
            System.out.println("  - Settlement files...");
            String settlementRemotePath = sftpRoot + "/settlements/settlement/" + 
                                         participantId + "/" + date;
            downloadFiles(channel, settlementRemotePath, 
                         "settlement_" + participantId + "_" + settlementCurrency + "_*.csv",
                         localPath.toString());
            
            // Download transaction files and fee files
            System.out.println("  - Transaction files and fee files...");
            String clearingRemotePath = sftpRoot + "/settlements/clearing/" + 
                                       participantId + "/" + date;
            downloadFiles(channel, clearingRemotePath, 
                         "transactionItems_" + participantId + "_" + settlementCurrency + "_*.csv",
                         localPath.toString());
            downloadFiles(channel, clearingRemotePath, 
                         "summary_" + participantId + "_" + settlementCurrency + "_*.csv",
                         localPath.toString());
            downloadFiles(channel, clearingRemotePath, 
                         "feeItems_" + participantId + "_" + settlementCurrency + "_*.csv",
                         localPath.toString());
            
        } finally {
            channel.disconnect();
            session.disconnect();
        }
        
        System.out.println("");
        System.out.println("✅ Reconciliation files downloaded to: " + localPath);
        System.out.println("");
        System.out.println("📂 File list:");
        Files.list(localPath).forEach(path -> System.out.println("  " + path.getFileName()));
    }
    
    private void downloadFiles(ChannelSftp channel, String remoteDir, 
                              String fileNamePattern, String localDir) throws Exception {
        try {
            channel.cd(remoteDir);
            Vector<ChannelSftp.LsEntry> files = channel.ls(fileNamePattern);
            
            for (ChannelSftp.LsEntry entry : files) {
                String fileName = entry.getFilename();
                if (!".".equals(fileName) && !"..".equals(fileName)) {
                    channel.get(fileName, localDir + "/" + fileName);
                    System.out.println("    Downloaded: " + fileName);
                }
            }
        } catch (SftpException e) {
            if (e.id == ChannelSftp.SSH_FX_NO_SUCH_FILE) {
                System.out.println("    No files found matching: " + fileNamePattern);
            } else {
                throw e;
            }
        }
    }
    
    // Usage
    public static void main(String[] args) {
        try {
            ReconciliationDownloader downloader = new ReconciliationDownloader(
                "your_username",
                "sftp-ipay-sg-three.alipay.com",
                "/path/to/private/key",
                "ACQP123",
                "USD",
                "production",
                System.getProperty("user.home") + "/.openclaw/workspace/alipayplus-reconciliation"
            );
            downloader.downloadReconciliationFiles();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**Maven Dependency** (for JSch):
```xml
<dependency>
    <groupId>com.jcraft</groupId>
    <artifactId>jsch</artifactId>
    <version>0.1.55</version>
</dependency>
```

---

### Method 2: Alipay+ Partner Workspace (Manual)

**Use Cases**: Ad-hoc downloads, viewing reconciliation details

#### Access URL

https://docs.alipayplus.com/alipayplus/alipayplus/worksp_acq/transactions_download_reports

#### Steps

1. Log in to Alipay+ Partner Workspace
2. Go to Payment Services > Transactions > Download Reports
3. Search for specific reconciliation reports by applying the filters: date range, report type, settlement currency, etc.
4. Click the download icon beside a report to download it.

#### Supported Report Types

| Report Type | Description | Update Frequency |
|-------------|-------------|------------------|
| Transaction Report | Transaction details | T+1 |
| Fee Report | Fee details | T+1 |
| Settlement Report | Settlement details | T+1 |
| Dispute Report | Disputed transactions | Real-time |

---

## Reconciliation File Processing Workflow

```
1. Download reconciliation files (SFTP or Workspace)
       ↓
2. Place in working directory (~/.openclaw/workspace/alipayplus-reconciliation/)
       ↓
3. Run reconciliation.sh script
       ↓
4. Parse file contents
       ↓
5. Compare with local orders
       ↓
6. Generate discrepancy report
       ↓
7. Process exception orders
```

---

## File Content Examples

### Settlement File (settlement_{participantId}_{currency}_{batchId}_{agreementId}_{seq}.csv)

```csv
settlementBatchId,participantId,settlementCurrency,settlementAmount,status,settlementDate,valueDate
BATCH001,ACQP123,USD,9500.00,COMPLETED,20240331,20240402
```

### Transaction Detail File (transactionItems_{participantId}_{currency}_{batchId}_{agreementId}_{seq}.csv)

```csv
clearingBatchId,tradeNo,outTradeNo,transactionType,amount,currency,feeAmount,netAmount,status,transactionTime,clearingTime
BATCH001,202403310001,ORDER_001,PAYMENT,100.00,USD,2.50,97.50,SUCCESS,2024-03-31T10:00:00Z,2024-03-31T10:00:05Z
BATCH001,202403310002,ORDER_002,PAYMENT,200.00,USD,5.00,195.00,SUCCESS,2024-03-31T11:00:00Z,2024-03-31T11:00:03Z
BATCH001,202403310003,ORDER_003,REFUND,50.00,USD,0.00,50.00,SUCCESS,2024-03-31T12:00:00Z,2024-03-31T12:00:10Z
```

### Transaction Summary File (summary_{participantId}_{currency}_{batchId}_{agreementId}_{seq}.csv)

```csv
clearingBatchId,transactionType,currency,totalCount,totalAmount,totalFeeAmount,totalNetAmount
BATCH001,PAYMENT,USD,150,15000.00,375.00,14625.00
BATCH001,REFUND,USD,20,1000.00,0.00,1000.00
BATCH001,CHARGEBACK,USD,2,200.00,0.00,200.00
```

### Fee Detail File (feeItems_{participantId}_{currency}_{batchId}_{agreementId}_{seq}.csv)

```csv
clearingBatchId,tradeNo,outTradeNo,feeType,feeAmount,currency,feeDescription,transactionTime
BATCH001,202403310001,ORDER_001,TRANSACTION_FEE,2.50,USD,Payment transaction fee,2024-03-31T10:00:05Z
BATCH001,202403310002,ORDER_002,TRANSACTION_FEE,5.00,USD,Payment transaction fee,2024-03-31T11:00:03Z
BATCH001,202403310003,ORDER_003,REFUND_FEE,0.00,USD,Refund (no fee),2024-03-31T12:00:10Z
```

---

## Troubleshooting

### Connection Failed

```bash
# Test SFTP connection
sftp -i $SFTP_KEY $SFTP_USER@$SFTP_HOST
```

### Permission Denied

```bash
# Ensure private key has correct permissions
chmod 600 $SFTP_KEY
```

### File Not Found

- Verify date format is correct (YYYYMMDD)
- Reconciliation files are generated after 10:00 AM T+1 morning
- Check participantId and currency configuration

---

## Java Reconciliation Processor

### Complete Example: Parse and Reconcile Files

```java
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.RFC4180ParserBuilder;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.annotation.*;

import java.io.*;
import java.nio.file.*;
import java.time.*;
import java.time.format.*;
import java.math.*;
import java.util.*;
import java.util.stream.*;

public class ReconciliationProcessor {
    
    private final String localDir;
    private final ObjectMapper objectMapper;
    
    public ReconciliationProcessor(String localDir) {
        this.localDir = localDir;
        this.objectMapper = new ObjectMapper();
    }
    
    // Transaction item model
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TransactionItem {
        public String clearingBatchId;
        public String tradeNo;
        public String outTradeNo;
        public String transactionType;
        public String amount;
        public String currency;
        public String feeAmount;
        public String netAmount;
        public String status;
        public String transactionTime;
        public String clearingTime;
        
        @Override
        public String toString() {
            return "TransactionItem{tradeNo='" + tradeNo + "', outTradeNo='" + outTradeNo + 
                   "', amount=" + amount + ", status=" + status + "}";
        }
    }
    
    // Local order model (your system's order)
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class LocalOrder {
        public String orderId;
        public String amount;
        public String currency;
        public String status;
        public String createTime;
        
        @Override
        public String toString() {
            return "LocalOrder{orderId='" + orderId + "', amount=" + amount + ", status=" + status + "}";
        }
    }
    
    // Discrepancy record
    public static class Discrepancy {
        public String type;  // MISSING_IN_ALIPAY, MISSING_IN_LOCAL, AMOUNT_MISMATCH, STATUS_MISMATCH
        public String tradeNo;
        public String outTradeNo;
        public String description;
        public String alipayAmount;
        public String localAmount;
        public String alipayStatus;
        public String localStatus;
        public LocalDateTime checkTime;
        
        public Discrepancy(String type, String tradeNo, String outTradeNo, String description) {
            this.type = type;
            this.tradeNo = tradeNo;
            this.outTradeNo = outTradeNo;
            this.description = description;
            this.checkTime = LocalDateTime.now();
        }
    }
    
    // Reconciliation result
    public static class ReconciliationResult {
        public String date;
        public int totalAlipayTransactions;
        public int totalLocalOrders;
        public int matchedCount;
        public List<Discrepancy> discrepancies = new ArrayList<>();
        public String summary;
        
        @Override
        public String toString() {
            return String.format("ReconciliationResult{date=%s, matched=%d/%d, discrepancies=%d}",
                               date, matchedCount, totalLocalOrders, discrepancies.size());
        }
    }
    
    /**
     * Parse transaction items from CSV file
     */
    public List<TransactionItem> parseTransactionItems(String date) throws Exception {
        List<TransactionItem> items = new ArrayList<>();
        
        // Find transaction file
        Path dir = Paths.get(localDir, date);
        Pattern pattern = Pattern.compile("transactionItems_.*\\.csv");
        
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, 
                entry -> pattern.matcher(entry.getFileName().toString()).matches())) {
            
            for (Path file : stream) {
                try (Reader reader = Files.newBufferedReader(file);
                     CSVReader csvReader = new CSVReaderBuilder(reader)
                             .withCSVParser(new RFC4180ParserBuilder().build())
                             .withSkipLines(1)  // Skip header
                             .build()) {
                    
                    String[] line;
                    while ((line = csvReader.readNext()) != null) {
                        if (line.length >= 11) {
                            TransactionItem item = new TransactionItem();
                            item.clearingBatchId = line[0];
                            item.tradeNo = line[1];
                            item.outTradeNo = line[2];
                            item.transactionType = line[3];
                            item.amount = line[4];
                            item.currency = line[5];
                            item.feeAmount = line[6];
                            item.netAmount = line[7];
                            item.status = line[8];
                            item.transactionTime = line[9];
                            item.clearingTime = line[10];
                            items.add(item);
                        }
                    }
                }
            }
        }
        
        System.out.println("📄 Parsed " + items.size() + " transaction items from " + date);
        return items;
    }
    
    /**
     * Load local orders from your system (example: from JSON file)
     */
    public List<LocalOrder> loadLocalOrders(String date) throws Exception {
        Path orderFile = Paths.get(localDir, "local_orders_" + date + ".json");
        
        if (!Files.exists(orderFile)) {
            System.out.println("⚠️  Local order file not found: " + orderFile);
            return new ArrayList<>();
        }
        
        String json = Files.readString(orderFile);
        return Arrays.asList(objectMapper.readValue(json, LocalOrder[].class));
    }
    
    /**
     * Perform reconciliation
     */
    public ReconciliationResult reconcile(String date) throws Exception {
        ReconciliationResult result = new ReconciliationResult();
        result.date = date;
        
        // Load data
        List<TransactionItem> alipayItems = parseTransactionItems(date);
        List<LocalOrder> localOrders = loadLocalOrders(date);
        
        result.totalAlipayTransactions = alipayItems.size();
        result.totalLocalOrders = localOrders.size();
        
        // Create maps for comparison
        Map<String, TransactionItem> alipayMap = alipayItems.stream()
            .collect(Collectors.toMap(item -> item.outTradeNo, item -> item));
        
        Map<String, LocalOrder> localMap = localOrders.stream()
            .collect(Collectors.toMap(order -> order.orderId, order -> order));
        
        // Check for discrepancies
        // 1. Find orders missing in Alipay+
        for (LocalOrder order : localOrders) {
            TransactionItem alipayItem = alipayMap.get(order.orderId);
            
            if (alipayItem == null) {
                Discrepancy discrepancy = new Discrepancy(
                    "MISSING_IN_ALIPAY",
                    null,
                    order.orderId,
                    "Order exists in local system but not in Alipay+ reconciliation"
                );
                discrepancy.localAmount = order.amount;
                discrepancy.localStatus = order.status;
                result.discrepancies.add(discrepancy);
            } else {
                // 2. Check amount mismatch
                if (!new BigDecimal(order.amount).equals(new BigDecimal(alipayItem.amount))) {
                    Discrepancy discrepancy = new Discrepancy(
                        "AMOUNT_MISMATCH",
                        alipayItem.tradeNo,
                        order.orderId,
                        "Amount mismatch between local and Alipay+"
                    );
                    discrepancy.localAmount = order.amount;
                    discrepancy.alipayAmount = alipayItem.amount;
                    discrepancy.localStatus = order.status;
                    discrepancy.alipayStatus = alipayItem.status;
                    result.discrepancies.add(discrepancy);
                }
                
                // 3. Check status mismatch
                if (!"SUCCESS".equalsIgnoreCase(alipayItem.status) && 
                    "PAID".equalsIgnoreCase(order.status)) {
                    Discrepancy discrepancy = new Discrepancy(
                        "STATUS_MISMATCH",
                        alipayItem.tradeNo,
                        order.orderId,
                        "Status mismatch: local=PAID but alipay=" + alipayItem.status
                    );
                    discrepancy.localStatus = order.status;
                    discrepancy.alipayStatus = alipayItem.status;
                    result.discrepancies.add(discrepancy);
                }
            }
        }
        
        // 4. Find orders missing in local system
        for (TransactionItem item : alipayItems) {
            if (!localMap.containsKey(item.outTradeNo)) {
                Discrepancy discrepancy = new Discrepancy(
                    "MISSING_IN_LOCAL",
                    item.tradeNo,
                    item.outTradeNo,
                    "Transaction exists in Alipay+ but not in local system"
                );
                discrepancy.alipayAmount = item.amount;
                discrepancy.alipayStatus = item.status;
                result.discrepancies.add(discrepancy);
            }
        }
        
        result.matchedCount = result.totalLocalOrders - 
            (int) result.discrepancies.stream()
                .filter(d -> "MISSING_IN_ALIPAY".equals(d.type) || 
                           "AMOUNT_MISMATCH".equals(d.type) ||
                           "STATUS_MISMATCH".equals(d.type))
                .count();
        
        // Generate summary
        result.summary = String.format(
            "Date: %s | Alipay+: %d | Local: %d | Matched: %d | Discrepancies: %d",
            date, result.totalAlipayTransactions, result.totalLocalOrders,
            result.matchedCount, result.discrepancies.size()
        );
        
        return result;
    }
    
    /**
     * Export discrepancy report to JSON
     */
    public void exportDiscrepancyReport(ReconciliationResult result, String outputPath) 
            throws Exception {
        objectMapper.writerWithDefaultPrettyPrinter()
            .writeValue(new File(outputPath), result);
        System.out.println("📊 Discrepancy report exported to: " + outputPath);
    }
    
    /**
     * Export discrepancy report to CSV
     */
    public void exportDiscrepancyCsv(ReconciliationResult result, String outputPath) 
            throws Exception {
        try (Writer writer = Files.newBufferedWriter(Paths.get(outputPath))) {
            writer.write("Type,TradeNo,OutTradeNo,Description,AlipayAmount,LocalAmount,AlipayStatus,LocalStatus,CheckTime\n");
            
            for (Discrepancy d : result.discrepancies) {
                writer.write(String.format("%s,%s,%s,%s,%s,%s,%s,%s,%s\n",
                    d.type,
                    d.tradeNo != null ? d.tradeNo : "",
                    d.outTradeNo != null ? d.outTradeNo : "",
                    d.description,
                    d.alipayAmount != null ? d.alipayAmount : "",
                    d.localAmount != null ? d.localAmount : "",
                    d.alipayStatus != null ? d.alipayStatus : "",
                    d.localStatus != null ? d.localStatus : "",
                    d.checkTime != null ? d.checkTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME) : ""
                ));
            }
        }
        System.out.println("📊 Discrepancy CSV exported to: " + outputPath);
    }
    
    // Usage
    public static void main(String[] args) {
        try {
            String date = LocalDate.now().minusDays(1).format(DateTimeFormatter.BASIC_ISO_DATE);
            String baseDir = System.getProperty("user.home") + 
                           "/.openclaw/workspace/alipayplus-reconciliation";
            
            ReconciliationProcessor processor = new ReconciliationProcessor(baseDir);
            
            // Perform reconciliation
            ReconciliationResult result = processor.reconcile(date);
            
            // Print summary
            System.out.println("");
            System.out.println("=" .repeat(60));
            System.out.println("📊 RECONCILIATION RESULT");
            System.out.println("=" .repeat(60));
            System.out.println(result.summary);
            System.out.println("");
            
            if (!result.discrepancies.isEmpty()) {
                System.out.println("⚠️  DISCREPANCIES FOUND: " + result.discrepancies.size());
                System.out.println("");
                
                for (Discrepancy d : result.discrepancies) {
                    System.out.println("  [" + d.type + "] " + d.outTradeNo);
                    System.out.println("    " + d.description);
                    if (d.alipayAmount != null) System.out.println("    Alipay+: " + d.alipayAmount);
                    if (d.localAmount != null) System.out.println("    Local: " + d.localAmount);
                    System.out.println("");
                }
                
                // Export reports
                processor.exportDiscrepancyReport(result, 
                    baseDir + "/" + date + "/discrepancy_report.json");
                processor.exportDiscrepancyCsv(result, 
                    baseDir + "/" + date + "/discrepancy_report.csv");
            } else {
                System.out.println("✅ ALL TRANSACTIONS MATCHED!");
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**Maven Dependencies**:
```xml
<dependencies>
    <!-- CSV Parsing -->
    <dependency>
        <groupId>com.opencsv</groupId>
        <artifactId>opencsv</artifactId>
        <version>5.9</version>
    </dependency>
    
    <!-- JSON Processing -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.16.1</version>
    </dependency>
</dependencies>
```

---

## Related Scripts

- `scripts/download-reconciliation.sh` - Automated SFTP download script
- `scripts/reconciliation.sh` - Reconciliation parsing and discrepancy detection

---

**Last Updated**: 2024-03-31
