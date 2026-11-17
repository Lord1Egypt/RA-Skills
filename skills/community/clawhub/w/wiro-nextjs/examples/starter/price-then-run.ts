// starter/price-then-run.ts
import 'server-only';

import { quote } from '@/lib/catalog/pricing';
import { buildParams, promptParam, withDefaults, type FormValues } from '@/lib/catalog/schema';
import { getModel } from '@/lib/wiro/catalog';
import { runModel } from '@/lib/wiro/client';

/** In Wiro-Next-Starter: check the inputs, price the run the way Wiro bills it, then start it under a limit. */
export async function priceThenRun(modelId: string, values: FormValues, limitUsd: number) {
  const model = await getModel(modelId); // Tool/Detail, kept for 10 minutes
  if (!model) throw new Error(`Wiro AI has no listed model ${modelId}.`);

  const built = buildParams(model.params, values); // drops unknown inputs, checks choices, ranges and file URLs
  if (built.errors.length > 0 || built.missing.length > 0) throw new Error([...built.errors, ...built.missing][0]);

  const prompt = promptParam(model.params);
  const promptText = prompt ? built.params[prompt.id] : undefined;
  const price = quote(model.pricing, withDefaults(model.params, built.params), {
    promptChars: typeof promptText === 'string' ? promptText.length : undefined,
  });
  if (price.amount === undefined || price.amount > limitUsd) throw new Error(`This run costs ${price.label}.`);

  const { token } = await runModel(model.id, built.params);
  return { token, price: price.label };
}
