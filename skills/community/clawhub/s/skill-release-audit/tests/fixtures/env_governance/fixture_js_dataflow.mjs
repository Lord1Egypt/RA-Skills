// frozen sample (v1.2 data-flow tracking): Zod-parsed env object + alias access
const environment = process.env;

const schema = z.object({
  MULTICA_PROFILE: z.string().default("redfin"),
  USAGE_LOOKBACK_DAYS: z.coerce.number().default(30),
});

const cfg = schema.parse(environment);
console.log(cfg.MULTICA_PROFILE);
console.log(environment.USAGE_LOOKBACK_DAYS);
console.log(environment["USAGE_SNAPSHOT_PATH"]);

const parsed = schema.safeParse({ ...environment });
const cfg2 = parsed.data;
if (cfg2.MULTICA_PROFILE) start(cfg2.MULTICA_PROFILE);

function loadConfig(env) {
  return { profile: env.MULTICA_PROFILE, lookback: env.USAGE_LOOKBACK_DAYS };
}
const config = loadConfig(process.env);
console.log(config.profile, config.USAGE_SNAPSHOT_PATH);
