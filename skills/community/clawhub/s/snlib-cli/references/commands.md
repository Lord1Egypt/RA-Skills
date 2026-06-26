# snlib-cli command patterns

## Login

```bash
SNLIB_USER="your-id" SNLIB_PASSWORD="your-password" {baseDir}/scripts/snlib-cli.sh login
```

## Search

```bash
{baseDir}/scripts/snlib-cli.sh search-books --keyword "키워드"
{baseDir}/scripts/snlib-cli.sh search-books --keyword "키워드" --manage-code MA --page 1 --per-page 10
```

## My page (read-only)

```bash
{baseDir}/scripts/snlib-cli.sh my-info
{baseDir}/scripts/snlib-cli.sh loan-status
{baseDir}/scripts/snlib-cli.sh loan-history
{baseDir}/scripts/snlib-cli.sh reservation-status
{baseDir}/scripts/snlib-cli.sh interloan-status
{baseDir}/scripts/snlib-cli.sh hope-book-list
{baseDir}/scripts/snlib-cli.sh hope-book-detail --rec-key 1938103961
{baseDir}/scripts/snlib-cli.sh basket-list
{baseDir}/scripts/snlib-cli.sh basket-list --group-key 13840
```

## Write operations (explicit submit)

### Interloan request

```bash
{baseDir}/scripts/snlib-cli.sh interloan-request \
  --manage-code MA \
  --reg-no CEM000334796 \
  --apl-lib-code 141484
```

### Hope-book request

```bash
{baseDir}/scripts/snlib-cli.sh hope-book-request \
  --request-edn '{:title "도서명" :author "저자" :publisher "출판사" :publishYear "2025" :eaIsbn "9788966264896" :price "54000" :email "user@example.com" :smsReceiptYn "Y" :handPhone "010-1234-5678"}'
```
