const config = {
  framework: 'react',
  projectName: '{{projectName}}',
  date: new Date().toISOString().slice(0, 10),
  designWidth: 375,
  deviceRatio: {
    640: 2.34 / 2,
    750: 1,
    828: 1.81 / 2,
    375: 2 / 1
  },
  sourceRoot: 'src',
  outputRoot: 'dist',
  plugins: [],
  defineConstants: {},
  h5: {
    publicPath: '/',
    staticDirectory: 'static',
    devtool: false,
    postcss: {
      autoprefixer: { enable: true, config: { autoprefixer: { enable: true } } },
      cssModules: { enable: false }
    }
  },
  weapp: {
    postcss: {
      cssModules: { enable: false }
    }
  }
}

module.exports = config
