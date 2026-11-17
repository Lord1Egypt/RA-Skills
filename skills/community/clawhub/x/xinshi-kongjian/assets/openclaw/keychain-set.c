#include <CoreFoundation/CoreFoundation.h>
#include <Security/Security.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  if (argc != 3) {
    fputs("usage: keychain-set SERVICE ACCOUNT\n", stderr);
    return 2;
  }

  size_t capacity = 4096;
  size_t length = 0;
  unsigned char *buffer = malloc(capacity);
  if (buffer == NULL) return 1;
  for (;;) {
    if (length == capacity) {
      capacity *= 2;
      unsigned char *grown = realloc(buffer, capacity);
      if (grown == NULL) {
        free(buffer);
        return 1;
      }
      buffer = grown;
    }
    size_t count = fread(buffer + length, 1, capacity - length, stdin);
    length += count;
    if (count == 0) break;
  }
  if (ferror(stdin) || length == 0) {
    fputs("refusing to store an empty secret\n", stderr);
    free(buffer);
    return 2;
  }

  CFStringRef service = CFStringCreateWithCString(NULL, argv[1], kCFStringEncodingUTF8);
  CFStringRef account = CFStringCreateWithCString(NULL, argv[2], kCFStringEncodingUTF8);
  CFDataRef secret = CFDataCreate(NULL, buffer, (CFIndex)length);
  free(buffer);
  if (service == NULL || account == NULL || secret == NULL) return 1;

  const void *queryKeys[] = {kSecClass, kSecAttrService, kSecAttrAccount};
  const void *queryValues[] = {kSecClassGenericPassword, service, account};
  CFDictionaryRef query = CFDictionaryCreate(
      NULL, queryKeys, queryValues, 3,
      &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);

  const void *addKeys[] = {kSecClass, kSecAttrService, kSecAttrAccount, kSecValueData};
  const void *addValues[] = {kSecClassGenericPassword, service, account, secret};
  CFDictionaryRef addition = CFDictionaryCreate(
      NULL, addKeys, addValues, 4,
      &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);

  OSStatus status = SecItemAdd(addition, NULL);
  if (status == errSecDuplicateItem) {
    const void *updateKeys[] = {kSecValueData};
    const void *updateValues[] = {secret};
    CFDictionaryRef update = CFDictionaryCreate(
        NULL, updateKeys, updateValues, 1,
        &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);
    status = SecItemUpdate(query, update);
    CFRelease(update);
  }

  CFRelease(addition);
  CFRelease(query);
  CFRelease(secret);
  CFRelease(account);
  CFRelease(service);

  if (status != errSecSuccess) {
    fprintf(stderr, "Keychain update failed with status %d\n", (int)status);
    return 1;
  }
  return 0;
}
