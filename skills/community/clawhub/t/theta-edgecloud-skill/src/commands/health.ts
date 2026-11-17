import { ThetaConfig } from '../config.js';
import { edgecloudControllerClient } from '../clients/edgecloudController.js';

export async function healthCheck(cfg: ThetaConfig) {
  const vm = await edgecloudControllerClient.listVmTypes(cfg);
  return {
    ok: true,
    vmCount: Array.isArray((vm as any)?.body?.vms) ? (vm as any).body.vms.length : undefined,
    timestamp: new Date().toISOString()
  };
}
