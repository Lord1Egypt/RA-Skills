const turf = require('@turf/turf');

function wrapAsFC(input, input2) {
  const features = [];
  if (input.type === 'FeatureCollection') return input;
  const f1 = input.type === 'Feature' ? input : turf.feature(input);
  features.push(f1);
  if (input2) {
    const f2 = input2.type === 'Feature' ? input2 : turf.feature(input2);
    features.push(f2);
  }
  return turf.featureCollection(features);
}

module.exports = {
  buffer(args) {
    return turf.buffer(args.input, args.radius, { units: args.units || 'kilometers' });
  },
  union(args) {
    const fc = wrapAsFC(args.input, args.input2);
    return turf.union(fc);
  },
  intersect(args) {
    const fc = wrapAsFC(args.input, args.input2);
    return turf.intersect(fc);
  },
  difference(args) {
    const fc = wrapAsFC(args.input, args.input2);
    return turf.difference(fc);
  },
  simplify(args) {
    return turf.simplify(args.input, { tolerance: args.tolerance || 0.01, highQuality: true });
  },
  convex(args) {
    return turf.convex(args.input);
  },
  concave(args) {
    return turf.concave(args.input, { maxEdge: args.maxEdge || Infinity, units: args.units || 'kilometers' });
  },
  dissolve(args) {
    return turf.dissolve(args.input, { propertyName: args.propertyName });
  },
  voronoi(args) {
    const opts = {};
    if (args.bbox) opts.bbox = args.bbox;
    return turf.voronoi(args.input, opts);
  },
  tin(args) {
    return turf.tin(args.input, args.propertyName);
  },
  bezierSpline(args) {
    return turf.bezierSpline(args.input, { resolution: args.resolution || 10000, sharpness: args.sharpness || 0.85 });
  },
  transformRotate(args) {
    return turf.transformRotate(args.input, args.angle);
  },
  transformScale(args) {
    return turf.transformScale(args.input, args.factor);
  },
  transformTranslate(args) {
    return turf.transformTranslate(args.input, args.distance, args.direction, { units: args.units || 'kilometers' });
  },
};
