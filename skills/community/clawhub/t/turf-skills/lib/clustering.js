const turf = require('@turf/turf');

module.exports = {
  clustersKmeans(args) {
    return turf.clustersKmeans(args.input, {
      numberOfClusters: args.numberOfClusters || 2,
    });
  },
  clustersDbscan(args) {
    return turf.clustersDbscan(args.input, args.maxDistance || 1, {
      units: args.units || 'kilometers',
      minPoints: args.minPoints || 3,
    });
  },
};
