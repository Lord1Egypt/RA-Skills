# PHP examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-php
(`composer require sendpulse/rest-api`). Below: SDK usage and a dependency-free
variant. For classic SMTP relay via PHPMailer see
[../references/smtp-relay.md](../references/smtp-relay.md).

## Using the official SDK

```php
<?php
require 'vendor/autoload.php';

use Sendpulse\RestApi\ApiClient;
use Sendpulse\RestApi\Storage\FileStorage;

$client = new ApiClient(
    getenv('SENDPULSE_API_ID'),
    getenv('SENDPULSE_API_SECRET'),
    new FileStorage() // caches the OAuth token between runs
);

$result = $client->post('smtp/emails', [
    'email' => [
        'subject' => 'Order confirmed',
        'from'    => ['name' => 'My Shop', 'email' => 'noreply@myshop.com'],
        'to'      => [['name' => 'Jane', 'email' => 'jane@example.com']],
        'html'    => base64_encode('<h1>Hello!</h1><p>Your order #1234 is confirmed.</p>'),
        'text'    => 'Hello! Your order #1234 is confirmed.',
    ],
]);

// $result['id'] — store it for status lookups
```

## Without the SDK (plain cURL)

```php
<?php

function sendpulseToken(): string
{
    static $token = null, $expiresAt = 0;
    if ($token !== null && time() < $expiresAt) {
        return $token; // reuse cached token (TTL 1 h)
    }

    $ch = curl_init('https://api.sendpulse.com/oauth/access_token');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => json_encode([
            'grant_type'    => 'client_credentials',
            'client_id'     => getenv('SENDPULSE_API_ID'),
            'client_secret' => getenv('SENDPULSE_API_SECRET'),
        ]),
    ]);
    $data = json_decode(curl_exec($ch), true);
    curl_close($ch);

    if (empty($data['access_token'])) {
        throw new RuntimeException('SendPulse auth failed: ' . json_encode($data));
    }
    $token = $data['access_token'];
    $expiresAt = time() + $data['expires_in'] - 60; // refresh 1 min early
    return $token;
}

function sendpulseSend(array $email): array
{
    $ch = curl_init('https://api.sendpulse.com/smtp/emails');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . sendpulseToken(),
        ],
        CURLOPT_POSTFIELDS => json_encode(['email' => $email]),
    ]);
    $response = json_decode(curl_exec($ch), true);
    $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);

    if ($status !== 200 || empty($response['result'])) {
        throw new RuntimeException("SendPulse send failed (HTTP $status): " . json_encode($response));
    }
    return $response; // ['result' => true, 'id' => '...']
}

$result = sendpulseSend([
    'subject' => 'Order confirmed',
    'from'    => ['name' => 'My Shop', 'email' => 'noreply@myshop.com'],
    'to'      => [['name' => 'Jane', 'email' => 'jane@example.com']],
    'html'    => base64_encode('<h1>Hello!</h1><p>Your order #1234 is confirmed.</p>'),
    'text'    => 'Hello! Your order #1234 is confirmed.',
]);
echo "Message id: {$result['id']}\n";
```

## Template with variables & binary attachment

```php
$result = sendpulseSend([
    'subject'  => 'Your invoice',
    'from'     => ['name' => 'My Shop', 'email' => 'billing@myshop.com'],
    'to'       => [['email' => 'jane@example.com']],
    'template' => ['id' => 12345, 'variables' => ['name' => 'Jane', 'order_id' => '1234']],
    'attachments_binary' => [
        'invoice.pdf' => base64_encode(file_get_contents('/path/invoice.pdf')),
    ],
]);
```

## Hygiene helpers

```php
// Check the blocklist before sending
$check = json_decode(file_get_contents(
    'https://api.sendpulse.com/smtp/unsubscribe/search?email=' . urlencode('jane@example.com'),
    false,
    stream_context_create(['http' => ['header' => 'Authorization: Bearer ' . sendpulseToken()]])
), true);

// Daily bounce sync (run from cron): GET /smtp/bounces/day,
// then delete hard-bounced addresses from your own database.
```
