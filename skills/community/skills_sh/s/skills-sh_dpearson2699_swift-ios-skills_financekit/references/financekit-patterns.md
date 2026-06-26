# FinanceKit Extended Patterns

Overflow reference for the `financekit` skill. Contains advanced query patterns, currency handling, and background delivery details that exceed the main skill file's scope.

## Contents

- [Predicate-Based Queries](#predicate-based-queries)
- [Transaction Field Reference](#transaction-field-reference)
- [Sorting and Pagination](#sorting-and-pagination)
- [Merchant Category Codes](#merchant-category-codes)
- [Currency Formatting](#currency-formatting)
- [Transaction Status Handling](#transaction-status-handling)
- [Balance History and Trends](#balance-history-and-trends)
- [Credit/Debit Interpretation by Account Type](#creditdebit-interpretation-by-account-type)
- [Resumable Sync Manager](#resumable-sync-manager)
- [SwiftUI Integration](#swiftui-integration)
- [Background Delivery Extension Lifecycle](#background-delivery-extension-lifecycle)
- [Error Handling](#error-handling)

## Predicate-Based Queries

### Combining Predicates

FinanceKit queries accept Swift `#Predicate` macros. Combine conditions directly within the predicate.

```swift
import FinanceKit

func fetchRecentDebits(
    for accountID: UUID,
    since date: Date
) async throws -> [Transaction] {
    let store = FinanceStore.shared

    let predicate = #Predicate<Transaction> { transaction in
        transaction.accountID == accountID &&
        transaction.transactionDate > date &&
        transaction.creditDebitIndicator == .debit
    }

    let query = TransactionQuery(
        sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
        predicate: predicate,
        limit: nil,
        offset: nil
    )

    return try await store.transactions(query: query)
}
```

### Using Built-In Predicate Factories

FinanceKit provides static factory methods on query types for common patterns:

```swift
// Transactions by status
let bookedPredicate = TransactionQuery.predicate(forStatuses: [.booked])

// Transactions by type
let purchasePredicate = TransactionQuery.predicate(
    forTransactionTypes: [.pointOfSale, .directDebit, .billPayment]
)

// Transactions by merchant category code
let diningPredicate = TransactionQuery.predicate(
    forMerchantCategoryCodes: [
        MerchantCategoryCode(rawValue: 5812),  // Restaurants
        MerchantCategoryCode(rawValue: 5814),  // Fast food
    ]
)

// Balances by date range (available balance)
let balancePredicate = AccountBalanceQuery.predicate(
    availableSince: startDate,
    until: endDate
)

// Balances by date range (booked balance)
let bookedBalancePredicate = AccountBalanceQuery.predicate(
    bookedSince: startDate,
    until: endDate
)
```

### Date Range Queries

```swift
func fetchTransactionsInRange(
    accountID: UUID,
    from startDate: Date,
    to endDate: Date
) async throws -> [Transaction] {
    let predicate = #Predicate<Transaction> { transaction in
        transaction.accountID == accountID &&
        transaction.transactionDate >= startDate &&
        transaction.transactionDate <= endDate
    }

    let query = TransactionQuery(
        sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
        predicate: predicate,
        limit: nil,
        offset: nil
    )

    return try await FinanceStore.shared.transactions(query: query)
}
```

### Filtering by Posted Date

Some transactions have a `postedDate` (when booked by the institution) distinct from `transactionDate`:

```swift
let predicate = #Predicate<Transaction> { transaction in
    transaction.postedDate != nil &&
    transaction.status == .booked
}
```

## Transaction Field Reference

| Property | Type | Notes |
|---|---|---|
| `id` | `UUID` | Unique internal ID; WWDC24 notes it is unique per device |
| `accountID` | `UUID` | Links the transaction to its parent account |
| `transactionDate` | `Date` | Time the transaction took place; may differ from posting time |
| `postedDate` | `Date?` | Posting time; if absent, use `transactionDate` as the posted date |
| `transactionAmount` | `CurrencyAmount` | Positive decimal amount plus ISO 4217 currency code |
| `creditDebitIndicator` | `CreditDebitIndicator` | `.debit` or `.credit`; interpret by account type |
| `transactionDescription` | `String` | Display-friendly description |
| `originalTransactionDescription` | `String` | Unmodified institution description |
| `merchantName` | `String?` | Merchant name if available |
| `merchantCategoryCode` | `MerchantCategoryCode?` | ISO 18245 code wrapper with `Int16` raw value |
| `transactionType` | `TransactionType` | Includes `.pointOfSale`, `.transfer`, `.refund`, `.unknown`, and other documented cases |
| `status` | `TransactionStatus` | `.authorized`, `.pending`, `.booked`, `.memo`, or `.rejected` |
| `foreignCurrencyAmount` | `CurrencyAmount?` | Original foreign-currency amount if applicable |
| `foreignCurrencyExchangeRate` | `Decimal?` | Exchange rate if applicable |

## Sorting and Pagination

### Multiple Sort Descriptors

```swift
let query = TransactionQuery(
    sortDescriptors: [
        SortDescriptor(\Transaction.transactionDate, order: .reverse),
        SortDescriptor(\Transaction.transactionDescription)
    ],
    predicate: nil,
    limit: 20,
    offset: nil
)
```

### Paginated Loading

Use `limit` and `offset` for paged access:

```swift
@Observable
@MainActor
final class TransactionPager {
    private let store = FinanceStore.shared
    private let pageSize = 25
    private var currentOffset = 0
    private(set) var transactions: [Transaction] = []
    private(set) var hasMore = true

    let accountID: UUID

    init(accountID: UUID) {
        self.accountID = accountID
    }

    func loadNextPage() async throws {
        guard hasMore else { return }

        let predicate = #Predicate<Transaction> { transaction in
            transaction.accountID == self.accountID
        }

        let query = TransactionQuery(
            sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
            predicate: predicate,
            limit: pageSize,
            offset: currentOffset
        )

        let page = try await store.transactions(query: query)
        transactions.append(contentsOf: page)
        currentOffset += page.count
        hasMore = page.count == pageSize
    }

    func reset() {
        transactions = []
        currentOffset = 0
        hasMore = true
    }
}
```

### Account Sorting

```swift
let accountQuery = AccountQuery(
    sortDescriptors: [
        SortDescriptor(\Account.institutionName),
        SortDescriptor(\Account.displayName)
    ],
    predicate: nil,
    limit: nil,
    offset: nil
)
```

## Merchant Category Codes

`MerchantCategoryCode` wraps an `Int16` raw value conforming to ISO 18245. Common codes:

| Code | Category |
|---|---|
| 5411 | Grocery stores |
| 5541 | Gas stations |
| 5812 | Restaurants |
| 5814 | Fast food |
| 5912 | Pharmacies |
| 5999 | Miscellaneous retail |
| 7011 | Hotels and motels |
| 7832 | Movie theaters |
| 4121 | Rideshare / taxis |
| 5311 | Department stores |

### Grouping Transactions by Category

```swift
func groupByCategory(_ transactions: [Transaction]) -> [Int16: [Transaction]] {
    var groups: [Int16: [Transaction]] = [:]
    for transaction in transactions {
        let code = transaction.merchantCategoryCode?.rawValue ?? -1
        groups[code, default: []].append(transaction)
    }
    return groups
}
```

### Category Display Name Mapping

`MerchantCategoryCode` conforms to `CustomStringConvertible`, providing a `description` property for display:

```swift
if let mcc = transaction.merchantCategoryCode {
    print("Category: \(mcc.description)")
}
```

## Currency Formatting

FinanceKit stores amounts as `CurrencyAmount` with a `Decimal` amount and a currency code string. Use `FormatStyle` for localized display.

### Basic Formatting

```swift
func formatCurrency(_ amount: CurrencyAmount) -> String {
    amount.amount.formatted(
        .currency(code: amount.currencyCode)
    )
}
```

### Signed Amount Display

Amounts are always positive. Apply sign based on `creditDebitIndicator`:

```swift
func formatSignedAmount(
    _ amount: CurrencyAmount,
    indicator: CreditDebitIndicator,
    accountType: Account
) -> String {
    var value = amount.amount
    switch accountType {
    case .asset:
        if indicator == .debit { value = -value }
    case .liability:
        if indicator == .debit { value = -value }
    }
    return value.formatted(.currency(code: amount.currencyCode))
}
```

### Foreign Currency Transactions

```swift
func displayForeignTransaction(_ transaction: Transaction) -> String {
    var result = formatCurrency(transaction.transactionAmount)

    if let foreign = transaction.foreignCurrencyAmount {
        result += " (originally \(formatCurrency(foreign))"
        if let rate = transaction.foreignCurrencyExchangeRate {
            result += " at rate \(rate)"
        }
        result += ")"
    }

    return result
}
```

## Transaction Status Handling

Transactions progress through statuses as they are processed by the institution.

| Status | Meaning |
|---|---|
| `.authorized` | Transaction approved but not yet processed |
| `.pending` | Processing by the institution |
| `.memo` | Informational entry, not yet settled |
| `.booked` | Fully settled and posted |
| `.rejected` | Declined by the institution |

### Filtering by Status

```swift
func fetchPendingTransactions(for accountID: UUID) async throws -> [Transaction] {
    let predicate = #Predicate<Transaction> { transaction in
        transaction.accountID == accountID &&
        (transaction.status == .pending || transaction.status == .authorized)
    }

    let query = TransactionQuery(
        sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
        predicate: predicate,
        limit: nil,
        offset: nil
    )

    return try await FinanceStore.shared.transactions(query: query)
}
```

### Status Display

```swift
func statusLabel(for status: TransactionStatus) -> String {
    switch status {
    case .authorized: "Authorized"
    case .pending:    "Pending"
    case .memo:       "Memo"
    case .booked:     "Posted"
    case .rejected:   "Declined"
    @unknown default: "Unknown"
    }
}
```

## Balance History and Trends

Use paginated balance queries to build historical balance charts.

```swift
func fetchBalanceHistory(
    for accountID: UUID,
    limit: Int = 30
) async throws -> [AccountBalance] {
    let predicate = #Predicate<AccountBalance> { balance in
        balance.accountID == accountID
    }

    let query = AccountBalanceQuery(
        sortDescriptors: [SortDescriptor(\AccountBalance.id)],
        predicate: predicate,
        limit: limit,
        offset: nil
    )

    return try await FinanceStore.shared.accountBalances(query: query)
}
```

### Date-Ranged Balance Queries

Use the built-in predicate factories:

```swift
let thirtyDaysAgo = Calendar.current.date(byAdding: .day, value: -30, to: Date())!

let query = AccountBalanceQuery(
    sortDescriptors: [SortDescriptor(\AccountBalance.id)],
    predicate: AccountBalanceQuery.predicate(
        availableSince: thirtyDaysAgo,
        until: nil
    ),
    limit: nil,
    offset: nil
)
```

### Extracting Chart Data

```swift
struct BalanceDataPoint: Identifiable {
    let id: UUID
    let date: Date
    let amount: Decimal
    let currencyCode: String
}

func balanceChartData(from balances: [AccountBalance]) -> [BalanceDataPoint] {
    balances.compactMap { balance in
        switch balance.currentBalance {
        case .available(let bal), .booked(let bal):
            let signed = bal.creditDebitIndicator == .credit ? bal.amount.amount : -bal.amount.amount
            return BalanceDataPoint(
                id: balance.id,
                date: bal.asOfDate,
                amount: signed,
                currencyCode: bal.currencyCode
            )
        case .availableAndBooked(let available, _):
            let signed = available.creditDebitIndicator == .credit
                ? available.amount.amount : -available.amount.amount
            return BalanceDataPoint(
                id: balance.id,
                date: available.asOfDate,
                amount: signed,
                currencyCode: balance.currencyCode
            )
        @unknown default:
            return nil
        }
    }
}
```

## Credit/Debit Interpretation by Account Type

The meaning of `CreditDebitIndicator` varies by account type. This is a common source of confusion.

### Asset Accounts (Apple Cash, Savings)

| Indicator | Balance Effect | Example |
|---|---|---|
| `.debit` | Decreases balance | Sending money via Apple Cash |
| `.credit` | Increases balance | Receiving a payment |

### Liability Accounts (Apple Card)

| Indicator | Balance Effect | Example |
|---|---|---|
| `.debit` | Decreases available credit | Making a purchase |
| `.credit` | Increases available credit | Payment or refund |

### Unified Interpretation

```swift
enum MoneyDirection {
    case incoming, outgoing
}

func direction(
    of transaction: Transaction,
    in account: Account
) -> MoneyDirection {
    // For both asset and liability accounts, debit represents money going out
    // (balance decrease for assets, credit decrease for liabilities)
    transaction.creditDebitIndicator == .debit ? .outgoing : .incoming
}
```

## Resumable Sync Manager

A manager for catch-up sync (`isMonitoring: false`), live monitoring (`true`), token persistence, and explicit deletion removal.

```swift
import FinanceKit

@Observable
@MainActor
final class FinanceSyncManager {
    private let store = FinanceStore.shared
    private let tokenKey = "financekit.sync.token"

    private(set) var accounts: [Account] = []
    private(set) var balances: [UUID: [AccountBalance]] = [:]
    private(set) var transactions: [UUID: [Transaction]] = [:]
    private(set) var syncError: Error?

    // MARK: - Initial Load

    func performInitialLoad() async {
        guard FinanceStore.isDataAvailable(.financialData) else { return }

        do {
            let status = try await store.authorizationStatus()
            guard status == .authorized else { return }
            accounts = try await fetchAllAccounts()
            for account in accounts {
                balances[account.id] = try await fetchBalances(for: account.id)
            }
        } catch {
            syncError = error
        }
    }

    // MARK: - Catch-Up Sync

    func syncTransactions(for accountID: UUID) async {
        let token = loadToken(for: accountID)

        do {
            let history = store.transactionHistory(
                forAccountID: accountID,
                since: token,
                isMonitoring: false
            )

            for try await changes in history {
                applyChanges(changes, for: accountID)
                saveToken(changes.newToken, for: accountID)
            }
        } catch let error as FinanceError where error == .historyTokenInvalid {
            // Token expired: discard it, then immediately rebuild local state
            // and replacement token from a fresh catch-up sequence.
            clearToken(for: accountID)
            transactions[accountID] = []
            await syncTransactions(for: accountID)
        } catch {
            syncError = error
        }
    }

    // MARK: - Live Monitoring

    func startMonitoring(for accountID: UUID) async {
        let token = loadToken(for: accountID)

        do {
            let history = store.transactionHistory(
                forAccountID: accountID,
                since: token,
                isMonitoring: true
            )

            for try await changes in history {
                applyChanges(changes, for: accountID)
                saveToken(changes.newToken, for: accountID)
            }
        } catch {
            syncError = error
        }
    }

    // MARK: - Private

    private func fetchAllAccounts() async throws -> [Account] {
        let query = AccountQuery(
            sortDescriptors: [SortDescriptor(\Account.displayName)],
            predicate: nil,
            limit: nil,
            offset: nil
        )
        return try await store.accounts(query: query)
    }

    private func fetchBalances(for accountID: UUID) async throws -> [AccountBalance] {
        let predicate = #Predicate<AccountBalance> { $0.accountID == accountID }
        let query = AccountBalanceQuery(
            sortDescriptors: [SortDescriptor(\AccountBalance.id)],
            predicate: predicate,
            limit: nil,
            offset: nil
        )
        return try await store.accountBalances(query: query)
    }

    private func applyChanges(
        _ changes: FinanceStore.Changes<Transaction>,
        for accountID: UUID
    ) {
        var current = transactions[accountID] ?? []

        // Remove deleted IDs first so local storage matches Wallet removals.
        let deletedSet = Set(changes.deleted)
        current.removeAll { deletedSet.contains($0.id) }

        // Update existing
        for updated in changes.updated {
            if let index = current.firstIndex(where: { $0.id == updated.id }) {
                current[index] = updated
            }
        }

        // Insert new
        current.append(contentsOf: changes.inserted)

        // Sort by date descending
        current.sort { $0.transactionDate > $1.transactionDate }

        transactions[accountID] = current
    }

    private func applyBalanceChanges(
        _ changes: FinanceStore.Changes<AccountBalance>,
        for accountID: UUID
    ) {
        var current = balances[accountID] ?? []
        // Remove deleted IDs first so local storage matches Wallet removals.
        let deletedSet = Set(changes.deleted)
        current.removeAll { deletedSet.contains($0.id) }

        for updated in changes.updated {
            if let index = current.firstIndex(where: { $0.id == updated.id }) {
                current[index] = updated
            }
        }

        current.append(contentsOf: changes.inserted)
        balances[accountID] = current
    }

    private func saveToken(_ token: FinanceStore.HistoryToken, for accountID: UUID) {
        let key = "\(tokenKey).\(accountID.uuidString)"
        if let data = try? JSONEncoder().encode(token) {
            UserDefaults.standard.set(data, forKey: key)
        }
    }

    private func loadToken(for accountID: UUID) -> FinanceStore.HistoryToken? {
        let key = "\(tokenKey).\(accountID.uuidString)"
        guard let data = UserDefaults.standard.data(forKey: key) else { return nil }
        return try? JSONDecoder().decode(FinanceStore.HistoryToken.self, from: data)
    }

    private func clearToken(for accountID: UUID) {
        let key = "\(tokenKey).\(accountID.uuidString)"
        UserDefaults.standard.removeObject(forKey: key)
    }
}
```

## SwiftUI Integration

### Account List View

```swift
import SwiftUI
import FinanceKit

struct AccountListView: View {
    @State private var accounts: [Account] = []

    var body: some View {
        NavigationStack {
            List(accounts, id: \.id) { account in
                NavigationLink(value: account.id) {
                    VStack(alignment: .leading) {
                        Text(account.displayName).font(.headline)
                        Text(account.institutionName).font(.subheadline).foregroundStyle(.secondary)
                    }
                }
            }
            .navigationTitle("Accounts")
            .navigationDestination(for: UUID.self) { TransactionListView(accountID: $0) }
            .task { await loadAccounts() }
        }
    }

    private func loadAccounts() async {
        guard FinanceStore.isDataAvailable(.financialData) else { return }
        do {
            let status = try await FinanceStore.shared.requestAuthorization()
            guard status == .authorized else { return }
            let query = AccountQuery(
                sortDescriptors: [SortDescriptor(\Account.displayName)],
                predicate: nil, limit: nil, offset: nil
            )
            accounts = try await FinanceStore.shared.accounts(query: query)
        } catch { }
    }
}
```

### Transaction List View

```swift
struct TransactionListView: View {
    let accountID: UUID
    @State private var transactions: [Transaction] = []

    var body: some View {
        List(transactions, id: \.id) { transaction in
            HStack {
                VStack(alignment: .leading) {
                    Text(transaction.transactionDescription)
                    if let merchant = transaction.merchantName {
                        Text(merchant).font(.caption).foregroundStyle(.secondary)
                    }
                }
                Spacer()
                VStack(alignment: .trailing) {
                    let amount = transaction.transactionAmount
                    let sign = transaction.creditDebitIndicator == .debit ? "-" : "+"
                    Text("\(sign)\(amount.amount.formatted(.currency(code: amount.currencyCode)))")
                        .font(.body.monospacedDigit())
                    Text(transaction.transactionDate, style: .date)
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
        }
        .navigationTitle("Transactions")
        .task {
            let predicate = #Predicate<Transaction> { $0.accountID == accountID }
            let query = TransactionQuery(
                sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
                predicate: predicate, limit: 100, offset: nil
            )
            transactions = (try? await FinanceStore.shared.transactions(query: query)) ?? []
        }
    }
}
```

## Background Delivery Extension Lifecycle

### Extension Setup

The background delivery extension requires:
1. A new extension target using the Background Delivery Extension template.
2. Both app and extension in the same App Group for shared data access.
3. The FinanceKit entitlement on both targets.
4. Financial-data authorization requested in the main app before enabling delivery; the extension inherits the app's authorization.

### Shared Data with App Groups

Use a shared container for data accessible to both the app and extension:

```swift
let sharedDefaults = UserDefaults(suiteName: "group.com.myapp.finance")

// In extension: sync latest data to shared container
func processNewTransactions() async {
    let store = FinanceStore.shared
    for account in try await fetchAccounts() {
        let history = store.transactionHistory(
            forAccountID: account.id, since: loadSharedToken(), isMonitoring: false
        )
        for try await changes in history {
            persistToSharedStore(changes)
            saveSharedToken(changes.newToken)
        }
    }
}
```

### Extension Lifecycle

- `didReceiveData(for:)` is called when the system detects changes matching the registered data types.
- Returning from `didReceiveData(for:)` closes the extension, so save essential work before returning.
- `willTerminate()` provides a cleanup opportunity before the system terminates the extension.
- `willTerminate()` may not be called for every system termination path.
- The extension has limited runtime. Perform only essential work (data sync, cache updates).
- Do not start long-running tasks or network requests that may not complete.

## Error Handling

### FinanceError Cases

```swift
do {
    let transactions = try await store.transactions(query: query)
} catch let error as FinanceError {
    switch error {
    case .dataRestricted(let dataType):
        handleRestriction(dataType)  // Wallet unavailable or MDM restricted
    case .historyTokenInvalid:
        discardSavedToken()          // Token points to compacted history
    case .unknown:
        logError(error)
    @unknown default:
        logError(error)
    }
}
```

### Graceful Degradation

```swift
@Observable
@MainActor
final class FinanceDataProvider {
    enum State {
        case loading, available([Transaction]), unavailable(reason: String)
    }

    private(set) var state: State = .loading

    func load(accountID: UUID) async {
        guard FinanceStore.isDataAvailable(.financialData) else {
            state = .unavailable(reason: "Financial data is not available on this device.")
            return
        }
        do {
            let status = try await FinanceStore.shared.authorizationStatus()
            guard status == .authorized else {
                state = .unavailable(reason: "Access to financial data has not been granted.")
                return
            }
            let predicate = #Predicate<Transaction> { $0.accountID == accountID }
            let query = TransactionQuery(
                sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
                predicate: predicate, limit: 50, offset: nil
            )
            state = .available(try await FinanceStore.shared.transactions(query: query))
        } catch let error as FinanceError {
            state = .unavailable(reason: error == .dataRestricted(.financialData)
                ? "Financial data is temporarily restricted."
                : "Unable to load financial data.")
        } catch {
            state = .unavailable(reason: "An unexpected error occurred.")
        }
    }
}
```
