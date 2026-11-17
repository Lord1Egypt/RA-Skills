# Inicio rápido

[English](QUICKSTART.md) | [简体中文](QUICKSTART.zh.md) | [日本語](QUICKSTART.ja.md) | **Español**

Pagar un enlace de pago de Coinbase (Coinbase Payment Link) de OpenRouter con
USDT/USDC en Solana, BNB Chain, Ethereum, Polygon, Arbitrum, Base o Stellar, con BTC por
Lightning, o con una moneda nativa (ETH en Ethereum, Base o Arbitrum, BNB, SOL, POL). Cinco minutos. Para saber cómo funciona y por qué, ver
[README.md](../README.md).

## El comando de una sola línea

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID
```

Eso ejecuta por uno todos los pasos de abajo: elegir moneda, cotizar, crear,
revisar, confirmar, instrucciones de depósito y luego consultar hasta la
liquidación. En el paso de elegir moneda se puede pegar la dirección de la
billetera y el selector consultará los saldos y marcará cuáles se pueden pagar
—es opcional y nunca cambia lo que se firma—.

Si ya se sabe qué moneda usar, se puede indicar y omitir la pregunta:

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID --with usdt-solana
```

Monedas para `--with`: `usdt-solana`, `usdc-solana`, `usdt-bnb`, `usdc-bnb`, `usdt-ethereum`,
`usdc-ethereum`, `usdt-polygon`, `usdc-polygon`, `usdt-arbitrum`, `usdc-arbitrum`,
`usdc-base`, `usdc-stellar`, `btc-lightning`, y las monedas nativas `eth-ethereum`,
`eth-base`, `eth-arbitrum`, `bnb-bnb`, `sol-solana`, `pol-polygon`. Los scripts y
los agentes deben pasar siempre `--with`: el selector solo aparece en una
terminal y no hay moneda por defecto.

Una moneda nativa solo se ofrece cuando la cotización de la factura la incluye,
para facturas de hasta $3,500 (ETH nativo en Ethereum: mínimo $1). Es exact-out:
envía exactamente la cantidad indicada antes de que termine el precio fijado
(alrededor de una hora; el enlace de OpenRouter en sí se puede pagar durante
unas 24 horas desde su creación), y guarda un poco de la misma moneda para el gas. El BTC
on-chain y Tron no están soportados.
ZEC en Zcash (Beta): usa https://checkout.rozo.ai/zec, esta CLI no crea órdenes en ZEC.

Por defecto solo imprime una dirección para pagar desde cualquier billetera: sin
clave privada y sin configuración. Añadir `--send` únicamente si se quiere que la
CLI firme desde una billetera caliente, y `--json` para obtener una salida
legible por máquina.

El resto de esta página es el mismo flujo ejecutado paso a paso, que es lo que
conviene si algo sale mal o si se quiere automatizar por cuenta propia.

## Antes de empezar

- **Node 18 o posterior** (`node -v`). No hay nada más que instalar: `npx`
  descarga la CLI, y los `scripts/dist/*.js` del repositorio clonado son
  paquetes autocontenidos.
- **Una billetera** que tenga la moneda con la que se quiere pagar, en la cadena elegida.
- **El enlace de Coinbase**, por ejemplo
  `https://payments.coinbase.com/payment-links/pl_01YOURLINKID`.
- Sin cuenta y sin clave de API. Todos los endpoints de aquí son públicos.

Definirlo una sola vez:

```bash
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"
```

Ids de cadena: `1` Ethereum · `56` BNB Chain · `137` Polygon · `8453` Base ·
`42161` Arbitrum · `900` Solana · `1500` Stellar · `lightning` Bitcoin Lightning.

## ¿Qué wallet necesito?

**Una wallet, en una cadena: no hace falta una por cada cadena.** Elige la
moneda que ya tengas y paga desde donde ya esté.

Sirve cualquier wallet, y también un retiro desde un exchange: el Mode A de
abajo solo imprime un bloque de depósito, y envías exactamente ese `amount` de
ese `tokenSymbol`, en esa `chain`, a esa `receiverAddress`. Nada se conecta a
ningún sitio ni se aprueba en el navegador. En la práctica la gente usa
MetaMask o Rabby en las cadenas EVM, Phantom o Solflare en Solana, y una wallet
Lightning como Phoenix o Wallet of Satoshi para BTC.

Dos casos son distintos. **Stellar** se enruta mediante una dirección
compartida más `receiverMemo`, así que aquello desde lo que envíes debe
permitirte fijar un memo: si lo omites, el pago se pierde. **Lightning** paga
la factura BOLT11 de `deposit.lnInvoice`; no hay ninguna dirección a la que
enviar.

Solo `--send` (Mode B) necesita una clave, y cubre únicamente las cadenas EVM y
Solana: en Solana usa el `~/.config/solana/id.json` que `solana-keygen` ya creó,
y en EVM un keystore cifrado cuya frase de contraseña se solicita. Una clave en
bruto en el entorno queda para la automatización desatendida.

## 1. Cotizarlo (solo lectura, gratis)

```bash
node scripts/dist/quote.js --url "$LINK"
```

```json
{
  "success": true,
  "merchant": "OpenRouter, Inc.",
  "invoice": { "amount": "1050.00", "fiat": { "amount": "1050.00", "currency": "USD" } },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "coinbaseExpiryIso": "2026-08-09T10:00:00.000Z"
}
```

Un `"success": false` con `LINK_NO_LONGER_PAYABLE` significa que el enlace ya
está usado o expirado: pedir uno nuevo y detenerse.

## 2. Crear la orden

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT
```

No se mueve dinero, y una orden sin fondear simplemente expira. La orden dura
alrededor de una hora, mientras que el enlace de OpenRouter se puede pagar
durante unas 24 horas desde su creación (`coinbaseExpiryIso`), así que una orden
vencida se puede reemplazar con el mismo enlace. La dirección de
depósito (deposit address) completa se **retiene** en esta etapa: se obtiene un
resumen enmascarado para revisarlo primero.

```json
{
  "success": true,
  "rozoPaymentId": "11111111-2222-4333-8444-555555555555",
  "invoice": { "amount": "1050.000000", "currency": "USD" },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "deposit": null,
  "depositWithheld": true,
  "display": {
    "chain": "Solana",
    "amount": "1064.910000 USDT",
    "payToMasked": "9WzDXw...AWWM"
  },
  "expiry": { "effectiveDeadlineIso": "2026-08-08T11:00:00.000Z", "minutesOfSlack": 55 }
}
```

Este ejemplo es el caso insignia: una factura de **$1,050.00** por $1,000 de
créditos de OpenRouter. Cualquier factura de hasta **$1,100** se puede pagar así.

**Revisar `display.amount` antes de continuar.** Normalmente es mayor que la
factura: incluye las comisiones del puente (bridge) y de la red. Anotar el
`rozoPaymentId`; todos los comandos posteriores lo usan.

## 3. Confirmar

Solo una vez que se ha decidido pagar, volver a ejecutar el mismo comando con `--confirm`:

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm
```

Esto libera el detalle completo del depósito y registra la confirmación que
exigen los scripts de envío.

```json
{
  "success": true,
  "confirmed": true,
  "deposit": {
    "chain": "Solana",
    "tokenSymbol": "USDT",
    "receiverAddress": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "receiverMemo": "rozo-901",
    "amount": "1054.410000",
    "payTo": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
  }
}
```

Enviar exactamente los campos que entrega este bloque. Para Lightning,
En Stellar el memo es **`MEMO_TEXT`** aunque parezca numérico: enviarlo como `MEMO_ID` no coincidirá. `deposit.expiresIn` indica cuánto sigue siendo válida la orden.
`deposit.lnInvoice` contiene la cadena BOLT11 que hay que escanear, y
`deposit.amount` está en satoshis.

## 4. Pagar

### La forma sencilla: desde la propia billetera

**Sin clave privada, sin variables de entorno, sin configuración.** Abrir
cualquier billetera y enviar exactamente lo que indica el bloque `deposit` de
arriba:

- el `amount` del `tokenSymbol`,
- en la `chain`,
- a la `receiverAddress`, copiada del JSON, nunca tecleada de nuevo.

Si el bloque contiene algún otro campo, como `receiverMemo`, incluirlo tal cual;
forma parte del destino en esa cadena. Para Lightning, escanear o pegar
`deposit.lnInvoice` en su lugar.

Eso es todo el Modo A. Continuar en el paso 5.

### La forma opcional: dejar que el script pague (Modo B)

Solo si se quiere que esta máquina firme, y únicamente en **cadenas EVM y
Solana**: no hay `--send` para Stellar ni Lightning, que se pagan desde la
propia billetera. Esta es la única parte que necesita una clave.

**Solana: usar el par de claves que ya se tiene.** Si alguna vez se ejecutó
`solana-keygen`, `~/.config/solana/id.json` ya existe y se usa automáticamente:

```bash
node scripts/dist/send-sol.js --rozo-payment-id <rozoPaymentId> --send
```

**EVM: usar un keystore cifrado.** Exportar un keystore JSON V3 desde la
billetera y apuntar a él. La frase de contraseña (passphrase) se solicita de
forma interactiva; nunca se pasa como bandera:

```bash
ROZO_CHECKOUT_EVM_KEYSTORE=~/wallets/hot.json \
  node scripts/dist/send-evm.js --rozo-payment-id <rozoPaymentId> --send
```

Cualquiera de los dos archivos se puede indicar explícitamente con
`--keyfile <path>`, y `--dry-run` funciona con todas las fuentes: deriva la
dirección y ejecuta todas las comprobaciones sin firmar nada.

**Para automatización desatendida**, donde nadie puede escribir una frase de
contraseña, una clave en bruto en el entorno sigue funcionando igual que antes:
`ROZO_CHECKOUT_SOL_KEY` o `ROZO_CHECKOUT_EVM_KEY`, o bien
`ROZO_CHECKOUT_KEYSTORE_PASSPHRASE` junto a un keystore. En una máquina que usa
una persona, es preferible un archivo de claves.

Estos ajustes también pueden vivir en un `.env` en el directorio desde el que se
ejecuta (o `--env-file <path>`). Solo se leen de él las claves `ROZO_CHECKOUT_*`,
se analiza como texto plano y nunca se pasa por un shell, y lo que ya esté en el
entorno real tiene prioridad. **Añadir `.env` al `.gitignore`.**

Un archivo de claves o un `.env` no debe ser legible por otros usuarios
(`chmod 600`) ni estar bajo seguimiento de git. Ambos casos se rechazan, no se advierten.

<details>
<summary><b>Configurar una billetera local para <code>--send</code></b> — plantilla .env y pasos de exportación por billetera</summary>

Muy probablemente no necesites nada de esto: la ruta por defecto no requiere ninguna clave, y para Stellar la skill `stellar-agent-wallet` envía con su propio manejo de claves — esta configuración `.env` es solo para automatización desatendida en EVM/Solana con una billetera caliente dedicada de saldo bajo.

**Nada de esto hace falta para la ruta por defecto.** Pagar desde la propia
billetera no necesita clave ni configuración, y funciona con billeteras que aquí
nunca se pueden usar, incluidas las de hardware y las cuentas de exchange.

Un `.env` en el directorio desde el que se ejecuta, con todas las variables que
esta herramienta lee:

```bash
# Nada de esto hace falta para pagar desde la propia billetera. Solo se lee
# cuando se usa --send.

# Clave secreta de Solana: una cadena base58 o un arreglo JSON de bytes. Solo
# hace falta si NO se tiene ~/.config/solana/id.json, que se detecta solo.
ROZO_CHECKOUT_SOL_KEY=REPLACE_ME_base58_secret_key

# Clave privada EVM en bruto: 0x seguido de 64 caracteres hex. La opción menos
# segura: es preferible el keystore de abajo.
ROZO_CHECKOUT_EVM_KEY=0x0000000000000000000000000000000000000000000000000000000000000000

# Keystore V3 cifrado para EVM: ruta al archivo. Preferible a la clave en bruto.
ROZO_CHECKOUT_EVM_KEYSTORE=/replace/me/keystores/my-hot-wallet

# Frase de contraseña de ese keystore. Solo para ejecuciones desatendidas; en
# una terminal se solicita y no se guarda nada.
ROZO_CHECKOUT_KEYSTORE_PASSPHRASE=REPLACE_ME_not_a_real_passphrase

# Sobrescrituras de RPC opcionales, una por id de cadena. 8453 = Base,
# 900 = Solana.
ROZO_CHECKOUT_RPC_8453=https://mainnet.base.org
ROZO_CHECKOUT_RPC_900=https://api.mainnet-beta.solana.com
```

Después, restringir permisos y mantenerlo fuera de git:

```bash
chmod 600 .env
echo '.env' >> .gitignore
```

**Solana**

- `solana-keygen new` escribe `~/.config/solana/id.json`. No hay nada que
  configurar: se encuentra automáticamente. Es la ruta recomendada.
- **Phantom** → Settings → Export Private Key da una cadena **base58**. Va en
  `ROZO_CHECKOUT_SOL_KEY`.
- **Solflare** exporta una cadena base58 en las versiones actuales y un arreglo
  JSON de bytes en las antiguas. Ambos se aceptan tal cual.

**EVM**

- **MetaMask** y **Rabby** exportan la clave privada como 64 caracteres hex.
  Pegarla tal cual en `ROZO_CHECKOUT_EVM_KEY`; el prefijo `0x` es opcional.
- **Keystore cifrado (más seguro).** Las billeteras de navegador exportan claves
  en bruto, no keystores. Para convertir una en un keystore cifrado, usar
  Foundry: `cast wallet import my-hot-wallet --interactive` pide la clave y
  escribe un keystore V3 cifrado en `~/.foundry/keystores/my-hot-wallet`
  (`--keystore-dir` cambia la ubicación). Apuntar `ROZO_CHECKOUT_EVM_KEYSTORE` a
  ese archivo. `geth account import` también genera un keystore V3.

**Billeteras que no se pueden usar con `--send`:** billeteras de hardware
(Ledger, Trezor), billeteras móviles solo con WalletConnect y cuentas de
exchange. Por diseño, ninguna entrega una clave de firma. Esos casos usan la
ruta por defecto sin clave, que funciona con todas ellas.

</details>

Un solo pago no puede superar **$1,100**; por encima de eso, pagar desde la
propia billetera como arriba.

```json
{
  "success": true,
  "submitted": true,
  "confirmed": true,
  "txHash": "3Bxs4h24hBjHziQ8UJqSjqjbjWQq2sQ3yV9Fq4HrVh5c"
}
```

## 5. Observar la liquidación

```bash
node scripts/dist/status.js --rozo-payment-id <rozoPaymentId> --watch --timeout 600
```

```json
{
  "success": true,
  "state": "settled",
  "terminal": true,
  "payin": { "txHash": "3Bxs4h24...", "confirmedAt": "2026-08-08T10:05:00.000Z" }
}
```

Los estados van `awaiting_deposit` → `payin_detected` → `payin_confirmed` →
`bridging` → `paying_coinbase` → `settled`. Que la transacción on-chain se
confirme no es el final: seguir consultando hasta `settled`.

## Si algo sale mal

Leer `error.code`. Los tres con los que es más probable toparse:

| `error.code` | Qué ocurrió | Qué hacer |
|---|---|---|
| `LINK_NO_LONGER_PAYABLE` | alguien ya pagó el enlace, o expiró | pedir al comercio un enlace nuevo; no pagar nada |
| `EXPIRY_MARGIN` | queda muy poco tiempo para fondear, puentear y liquidar de forma segura | no fondear esta orden; dejar que expire y volver a empezar desde el paso 1 con el mismo enlace (se crea una orden nueva cuando se comprueba que la anterior no recibió fondos). Si responde `LINK_USED_OR_EXPIRED`, o `PAYMENT_EXPIRED` con `confirmed: true`, pedir al comercio un enlace nuevo |
| `ALREADY_SENT` | ya hay un envío registrado para esta orden | **no** enviar de nuevo; ejecutar `status.js` y revisar primero la cadena |

**Si algo de dinero ya salió de la billetera, nunca pagar de nuevo.** Conservar
el `linkId`, el `rozoPaymentId` y todos los hashes de transacción, y pedir a una
persona que lo concilie. No hay garantía de que un segundo pago a una dirección
de depósito de un solo uso sea acreditado.

La tabla completa de errores está en [README.md](../README.md), y las instrucciones
dirigidas al agente están en [SKILL.md](../SKILL.md).
