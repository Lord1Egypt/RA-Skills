export function buildCompactSkillOutput({
  shopInput,
  summary,
  buckets,
} = {}) {
  const availableBuckets = Array.isArray(summary?.buckets)
    ? summary.buckets.filter(bucket => bucket?.available)
    : [];

  return {
    ok: true,
    shopInput,
    shopCode: summary?.shop?.shopCode || '',
    catalogSize: Number(summary?.shop?.catalogSize || 0),
    degradedReasonCodes: (summary?.capabilities?.degradedCapabilities || [])
      .map(entry => entry?.reasonCode)
      .filter(Boolean),
    availableBuckets: availableBuckets.map(bucket => ({
      bucketId: bucket.bucketId,
      title: bucket.title || '',
      itemCount: Number(bucket.itemCount || 0),
    })),
    summary,
    buckets,
  };
}
