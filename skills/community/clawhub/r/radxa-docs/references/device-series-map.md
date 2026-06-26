# Device Series Map

Use this table to map a detected device string or a user-provided board name to a Radxa product series.

| Device keyword | Series | Example boards |
| --- | --- | --- |
| `ROCK 5`, `rock5`, `rock5a`, `rock5b`, `rock5c`, `RK3588` | `rock5` | ROCK 5A, ROCK 5B, ROCK 5C |
| `ROCK 4`, `rock4`, `rock4a`, `rock4b`, `rock4c`, `RK3399` | `rock4` | ROCK 4A, ROCK 4B, ROCK 4C+ |
| `ROCK 3`, `rock3`, `rock3a`, `rock3b`, `rock3c`, `RK3568` | `rock3` | ROCK 3A, ROCK 3B, ROCK 3C |
| `ROCK 2`, `rock2`, `rock2a`, `rock2f`, `RK3328` | `rock2` | ROCK 2A, ROCK 2F |
| `Zero`, `zero`, `zero2`, `zero3`, `RK3528` | `zero` | Zero, Zero 2, Zero 3 |
| `X15`, `X2L`, `Intel` | `x` | X15, X2L |
| `E20C`, `E24C`, `E52C`, `E54C` | `e` | E20C, E24C, E52C, E54C |
| `CM3`, `CM3I`, `CM3J`, `CM4`, `CM5`, `NX5` | `som` | CM3, CM4, CM5, NX5 |
| `Orion`, `orion`, `O6`, `O6N` | `orion` | Orion O6, Orion O6N |
| `Cubie`, `cubie`, `A5E`, `A7A` | `cubie` | Cubie A5E, Cubie A7A |
| `Dragon`, `dragon`, `Q6A` | `dragon` | Dragon Q6A |
| `SiRider`, `sirider`, `S1` | `sirider` | SiRider S1 |
| `AIRbox`, `AICore`, `aicore` | `aicore` | AIRbox, AICore |
| `FogWise`, `fogwise` | `fogwise` | FogWise devices |
| `NIO`, `nio`, `NIO12L` | `nio` | NIO12L |

If the detected string does not match a known Radxa family, treat the host as non-Radxa until the user provides a specific board model.
