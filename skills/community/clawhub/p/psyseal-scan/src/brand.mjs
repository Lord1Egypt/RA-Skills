// Marca, llamada a la acción (CTA) y datos de la tienda.
// `url` vacío = no se imprime ninguna llamada a la acción.
// El escáner solo IMPRIME este enlace: no abre conexiones. `?ref=scan` es el mismo texto para todos
// y no identifica a nadie; el sitio no usa analítica ni cookies.
export const BRAND = Object.freeze({
  name: 'Psyseal',
  url: 'https://psyseal.com/?ref=scan#planes',
});

// Licencias de la limpieza (psyseal-fix). Las vende Polar; organizationId se llena al abrir la tienda.
// Mientras esté vacío, la limpieza funciona en modo vista previa (muestra los cambios, no los aplica).
export const LICENSE = Object.freeze({
  api: 'https://api.polar.sh',
  organizationId: '472b41b0-3446-4fd2-bccc-509090d344b2',
  checkoutUrl: 'https://psyseal.com/#planes',
  portalUrl: 'https://polar.sh/psyseal/portal',
});

// Servicio del sello (psyseal-seal). Recibe solo resultados y una huella de los archivos, nunca su contenido.
export const SEAL = Object.freeze({
  api: 'https://seal.psyseal.com',
});
