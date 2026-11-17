# rozo-checkout

[English](../README.md) | [简体中文](README.zh.md) | [日本語](README.ja.md) | **Español**

Pagar un **enlace de pago de Coinbase (Payment Link) de OpenRouter** con una
moneda que ese enlace no puede aceptar directamente: BTC por Lightning,
USDT/USDC en Solana, BNB Chain, Ethereum, Polygon, Arbitrum, Base o Stellar, o
una moneda nativa: ETH en Ethereum, Base o Arbitrum, BNB, SOL o POL. Un enlace de
pago de Coinbase solo acepta USDC en Base; esto enruta la moneda que realmente
se posee a través de un puente, y una billetera fondeadora liquida la factura en
nombre del usuario. Sin cuenta, sin clave de API, sin navegador.

```bash
npx @rozoai/checkout pay <coinbase-link>
```

Primero pregunta con qué moneda se quiere pagar —al pegar la dirección de la
billetera en el prompt, marca cuáles se pueden pagar con el saldo disponible— y
luego imprime una dirección de depósito para pagar desde cualquier billetera
—**sin clave privada, sin variable de entorno, sin configuración**—. Después
espera hasta que la factura quede liquidada.

¿Ya se sabe qué moneda usar? Se puede omitir la pregunta:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

## Monedas con las que se puede pagar

| Cadena | `--with` | Id de cadena | Notas |
|---|---|---|---|
| Ethereum | `usdt-ethereum` `usdc-ethereum` | `1` | 6 decimales |
| BNB Chain | `usdt-bnb` `usdc-bnb` | `56` | 18 decimales |
| Polygon | `usdt-polygon` `usdc-polygon` | `137` | 6 decimales |
| Arbitrum | `usdt-arbitrum` `usdc-arbitrum` | `42161` | 6 decimales |
| Base | `usdc-base` | `8453` | 6 decimales |
| Solana | `usdt-solana` `usdc-solana` | `900` | SPL |
| Stellar | `usdc-stellar` | `1500` | memo `MEMO_TEXT` obligatorio — se muestra en el bloque de depósito |
| Bitcoin Lightning | `btc-lightning` | `lightning` | BOLT11; importes en satoshis |

**Monedas nativas**, cada una en su propia cadena:

| Moneda | `--with` | Id de cadena | Notas |
|---|---|---|---|
| ETH en Ethereum | `eth-ethereum` | `1` | 18 decimales (wei); mínimo $1 |
| ETH en Base | `eth-base` | `8453` | 18 decimales (wei) |
| ETH en Arbitrum | `eth-arbitrum` | `42161` | 18 decimales (wei) |
| BNB | `bnb-bnb` o `bnb` | `56` | 18 decimales |
| SOL | `sol-solana` o `sol` | `900` | 9 decimales (lamports) |
| POL | `pol-polygon` o `pol` | `137` | 18 decimales |

Una moneda nativa solo se ofrece cuando la cotización de la factura la incluye (`quote` lo muestra), y solo para facturas de hasta $3,500. La orden es **exact-out**, como Lightning: envía exactamente la cantidad de moneda del bloque de depósito. Su precio queda fijado solo hasta la hora indicada (alrededor de una hora, mientras que el enlace de OpenRouter en sí se puede pagar durante unas 24 horas desde su creación); pasada esa hora, no la envíes: deja que la orden expire y crea una nueva. La cantidad incluye un diferencial cambiario además de la comisión de servicio, y la billetera necesita un poco más de la misma moneda para la comisión de red. Si pagas desde un exchange, debe llegar la cantidad completa: comprueba que la comisión de retiro no se descuente de ella. `--send` también paga monedas nativas, como una transferencia normal de la cantidad exacta.

El BTC on-chain y Tron no están soportados.
ZEC en Zcash (Beta): usa https://checkout.rozo.ai/zec, esta CLI no crea órdenes en ZEC.

## ¿Qué wallet necesito?

**Una wallet, en una cadena: no hace falta una por cada cadena.** Elige de la
tabla de arriba la moneda que ya tengas y paga desde donde ya esté.

- **Sirve cualquier wallet, y también un retiro desde un exchange.** La vía por
  defecto solo imprime un bloque de depósito: envía exactamente ese `amount` de
  ese `tokenSymbol`, en esa `chain`, a esa `receiverAddress`. Nada se conecta a
  ningún sitio ni se aprueba en el navegador. En la práctica la gente usa
  MetaMask o Rabby en las cadenas EVM, Phantom o Solflare en Solana, y una
  wallet Lightning como Phoenix o Wallet of Satoshi para BTC.
- **Stellar es la que exige cuidado.** Sus depósitos se enrutan mediante una
  dirección compartida más `receiverMemo`, así que aquello desde lo que envíes
  — exchange o wallet — debe permitirte fijar un memo. Si lo omites, el pago se
  pierde.
- **Lightning paga una factura, no una dirección.** Escanea o pega
  `deposit.lnInvoice`; no hay ninguna dirección a la que enviar.
- **Solo `--send` necesita una clave privada**, leída de
  `ROZO_CHECKOUT_EVM_KEY` o `ROZO_CHECKOUT_SOL_KEY`, y cubre únicamente las
  cadenas EVM y Solana. Todo lo demás no usa claves.

## Usarlo desde el agente

La carga útil es la misma en todas partes: el comando de una línea de arriba, o
apuntar al agente a [llms.txt](../llms.txt). **Pagar desde la propia billetera
nunca necesita una clave.** Solo la bandera opcional `--send` firma en local, y
solo esa bandera lee `ROZO_CHECKOUT_EVM_KEY` / `ROZO_CHECKOUT_SOL_KEY`. Los agentes y los scripts deben
pasar siempre `--with`: el selector solo aparece en una terminal y no hay moneda
por defecto de forma deliberada.

<details>
<summary><b>Claude Code</b> — instalar la habilidad, o pegar el comando de una línea</summary>

Este repositorio es una habilidad de Claude Code: incluye `SKILL.md` más los
ejecutables de `scripts/dist/`. Basta con clonarlo en el directorio de
habilidades y Claude Code lo detecta automáticamente.

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill ~/.claude/skills/rozo-checkout
```

O saltarse la instalación y simplemente pedirle que ejecute:

```
Paga este enlace de OpenRouter con USDT en Solana:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Añadir `--send` solo si se quiere
que Claude firme desde una billetera caliente, lo cual necesita la clave del entorno.
</details>

<details>
<summary><b>Codex CLI</b> — AGENTS.md, o ejecutarlo directamente</summary>

Codex lee `AGENTS.md` desde la raíz del proyecto. Conviene añadir una
instrucción permanente para que sepa cómo pagar sin que haya que explicárselo
cada vez:

```
Para pagar un enlace de pago de OpenRouter / Coinbase, ejecuta:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado, y solo admite cadenas EVM y Solana (Stellar y Lightning son solo Modo A).
</details>

<details>
<summary><b>OpenCode</b> — AGENTS.md, o ejecutarlo directamente</summary>

OpenCode también lee `AGENTS.md` desde la raíz del proyecto, así que el fragmento
de Codex de arriba funciona sin cambios. El camino más corto sigue siendo el
propio comando:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>Cline</b> — .clinerules, o ejecutarlo directamente</summary>

Cline lee las instrucciones permanentes desde `.clinerules` en la raíz del proyecto:

```
Para pagar un enlace de pago de OpenRouter / Coinbase, ejecuta:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>Cursor</b> — .cursor/rules, o ejecutarlo directamente</summary>

Añadir una regla de proyecto en `.cursor/rules/rozo-checkout.mdc`:

```
Para pagar un enlace de pago de OpenRouter / Coinbase, ejecuta:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>Hermes Agent</b> — ejecutar el comando de una línea en una sesión</summary>

Hermes Agent (Nous Research) tiene acceso a la shell y su propio sistema de
habilidades. Se inicia con `hermes` y se le pide:

```
Descarga https://checkout.rozo.ai/llms.txt y luego paga este enlace de OpenRouter:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>OpenClaw</b> — openclaw agent exec</summary>

El punto de entrada headless de OpenClaw ejecuta una tarea puntual, lo que encaja
con un pago que se dispara desde un script o desde un canal de chat:

```bash
openclaw agent exec "Pay this OpenRouter link with USDT on Solana by running: npx @rozoai/checkout pay <coinbase-link> --with usdt-solana"
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>Pi</b> — ejecutar el comando de una línea en una sesión</summary>

Pi es un agente de terminal BYOK cuyas herramientas integradas incluyen `bash`,
así que puede ejecutar el comando directamente. Se inicia con `pi` y se le pide:

```
Paga este enlace de OpenRouter con USDT en Solana ejecutando:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

<details>
<summary><b>Terminal — sin ningún agente</b> — ejecutar los scripts paso a paso</summary>

Conducir cada paso a mano. Los paquetes son autocontenidos; no hay nada que
instalar más allá de Node 18+.

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill && cd rozo-checkout-skill
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"

# Cotización de solo lectura, no cuesta nada
node scripts/dist/quote.js --url "$LINK"

# Crear la orden. Aquí se RETIENE la dirección de depósito completa; primero se
# obtiene un resumen enmascarado para revisar.
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT

# Una vez decidido el pago, volver a ejecutar con --confirm para liberarla
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm

# Pagar el bloque de depósito desde cualquier billetera y observar la liquidación
node scripts/dist/status.js --rozo-payment-id <uuid> --watch
```

Cada script imprime exactamente un objeto JSON en stdout. Código de salida `0`
éxito, `1` rechazado/fallido (leer `error.code`), `2` uso incorrecto, `3` enviado
pero sin confirmar. Recorrido completo: [QUICKSTART](QUICKSTART.es.md).

Billetera: cualquier billetera, **sin clave**. Para el envío desde billetera
caliente, ver `send-evm.js` / `send-sol.js`, que leen `ROZO_CHECKOUT_EVM_KEY` /
`ROZO_CHECKOUT_SOL_KEY`.
</details>

<details>
<summary><b>Cualquier otro agente</b> — apuntarlo a llms.txt</summary>

Cualquier agente capaz de descargar una URL y ejecutar un comando puede hacer esto:

```
Descarga https://checkout.rozo.ai/llms.txt a tu contexto y úsalo
para pagar este enlace de OpenRouter: <coinbase-link>
```

Si el agente no tiene shell pero puede hacer peticiones HTTP, puede manejar
directamente los cuatro endpoints públicos — ver [cómo funciona](how-it-works.md).

Billetera: cualquier billetera, **sin clave**. Solo `--send` la necesita: firma localmente con el par de claves de la CLI de Solana o un keystore cifrado.
</details>

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

## Tres reglas que conviene conocer

- **La dirección de depósito es de un solo uso.** Nunca reutilizar una de una
  orden anterior, de una respuesta cacheada o de una captura de pantalla.
- **Enviar exactamente el importe mostrado.** Normalmente es mayor que la
  factura: incluye las comisiones del puente y de la red.
- **Nunca pagar dos veces una orden ya fondeada.** Si ya se ha detectado un
  pago, detenerse y pedir a una persona que lo concilie; un segundo pago a una
  dirección de un solo uso no tiene garantía de ser acreditado.

La lista completa de lo que esta herramienta se niega a hacer, y por qué, está en
[docs/safety.md](safety.md).

## Enlaces

- [Inicio rápido](QUICKSTART.es.md) — los cinco comandos, con la salida esperada
- [Cómo funciona](how-it-works.md) — el flujo, los endpoints, los identificadores
- [Diseño de seguridad](safety.md) — cada salvaguarda, en detalle
- [SKILL.md](../SKILL.md) — instrucciones dirigidas al agente · [llms.txt](../llms.txt) — resumen en un solo archivo
- [checkout.rozo.ai/agent](https://checkout.rozo.ai/agent.html) — lo mismo, en la web
- [Issues](https://github.com/RozoAI/rozo-checkout-skill/issues) — errores y solicitudes

## Registro de cambios

- **0.1.3** — Correcciones surgidas del primer pago real. Los bundles ya no fallan
  con `__filename is not defined` en Node 22+ (el banner de esbuild ahora define
  `__filename`/`__dirname` además de `require`, y las pruebas ejecutan cada bundle
  de verdad). Los depósitos de Stellar indican el tipo de memo (`MEMO_TEXT`, aunque
  el memo parezca numérico). Las órdenes muestran la validez restante como duración
  ("expires in 47m") en el bloque de depósito y en `status`, con el comando exacto
  para crear una nueva. Reutilizar una orden impaga existente, y pedir una moneda
  distinta a la suya, ahora se explican en lugar de parecer errores.
- **0.1.2** — El Modo B ya no necesita una clave privada en bruto en una variable
  de entorno. En Solana usa el `~/.config/solana/id.json` que `solana-keygen` ya
  creó; en EVM un keystore V3 cifrado cuya frase de contraseña se solicita.
  `--keyfile` indica cualquiera de los dos explícitamente, y los ajustes pueden
  venir de un `.env` incluido en `.gitignore`. Las claves en bruto del entorno
  siguen funcionando para automatización desatendida. Los archivos de claves y
  el `.env` deben ser `chmod 600` y no estar bajo seguimiento de git.
- **0.1.1** — un solo límite de gasto en lugar de dos: un pago individual no
  puede superar los $1,100 (dimensionado para una compra de crédito de $1,000
  más su comisión del 5%); se eliminan el tope acumulado por sesión y la bandera
  `--yes-large`. La documentación deja explícito que pagar desde la propia
  billetera no necesita clave ni configuración.
- **0.1.0** — primera versión: `npx @rozoai/checkout`.

## Licencia

MIT.
