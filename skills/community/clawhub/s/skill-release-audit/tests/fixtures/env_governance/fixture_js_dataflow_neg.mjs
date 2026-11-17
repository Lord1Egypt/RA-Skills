// frozen sample (v1.2 negative): same-name plain objects / non-env parse
// args / non-env call args must NOT be tracked as env uses
const environment = { MULTICA_PROFILE: "redfin", USAGE_LOOKBACK_DAYS: 7 };
console.log(environment.MULTICA_PROFILE, environment.USAGE_LOOKBACK_DAYS);

const cfg = schema.parse(userData);
console.log(cfg.MULTICA_PROFILE);

function load(env) { return env.X; }
const c = load(otherObj);
console.log(c.MULTICA_PROFILE);
