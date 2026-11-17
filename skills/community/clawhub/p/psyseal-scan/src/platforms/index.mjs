// Registro de plataformas que el escáner sabe leer. OpenClaw tiene su propio flujo (con el cálculo detallado
// del latido); el resto se normaliza con los lectores de esta carpeta.

import * as hermes from './hermes.mjs';
import * as nanobot from './nanobot.mjs';
import * as picoclaw from './picoclaw.mjs';
import * as zeroclaw from './zeroclaw.mjs';
import * as nanoclaw from './nanoclaw.mjs';
import * as generic from './generic.mjs';

export const ADAPTERS = [hermes, nanobot, picoclaw, zeroclaw, nanoclaw];
export const PLATFORM_IDS = ['openclaw', ...ADAPTERS.map((a) => a.ID)];
export const PLATFORM_NAMES = { openclaw: 'OpenClaw', ...Object.fromEntries([...ADAPTERS, generic].map((a) => [a.ID, a.NAME])) };

export { generic, nanoclaw };
