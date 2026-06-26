/**
 * 代码块主题（与文章主题独立，常见 IDE 风格）
 * 用于语法高亮颜色 + 代码块背景、边框、语言标签颜色
 */
export const codeThemeOptions = [
  {
    id: 'vscode-dark',
    name: 'VS Code Dark+',
    colors: {
      keyword: '#569cd6',
      string: '#ce9178',
      number: '#b5cea8',
      comment: '#6a9955',
      function: '#dcdcaa',
      regex: '#d16969',
      attr: '#9cdcfe',
      tag: '#569cd6',
      param: '#9cdcfe',
      default: '#d4d4d4',
    },
    block: {
      bg: '#282c34',
      border: '#3e4451',
      labelColor: '#abb2bf',
    },
  },
  {
    id: 'vscode-light',
    name: 'VS Code Light+',
    colors: {
      keyword: '#0000ff',
      string: '#a31515',
      number: '#098658',
      comment: '#008000',
      function: '#795e26',
      regex: '#811f3f',
      attr: '#001080',
      tag: '#0000ff',
      param: '#001080',
      default: '#000000',
    },
    block: {
      bg: '#ffffff',
      border: '#e1e4e8',
      labelColor: '#6e7681',
    },
  },
  {
    id: 'monokai',
    name: 'Monokai',
    colors: {
      keyword: '#f92672',
      string: '#e6db74',
      number: '#ae81ff',
      comment: '#75715e',
      function: '#a6e22e',
      regex: '#e6db74',
      attr: '#a6e22e',
      tag: '#f92672',
      param: '#fd971f',
      default: '#f8f8f2',
    },
    block: {
      bg: '#272822',
      border: '#49483e',
      labelColor: '#75715e',
    },
  },
  {
    id: 'one-dark',
    name: 'One Dark',
    colors: {
      keyword: '#c678dd',
      string: '#98c379',
      number: '#d19a66',
      comment: '#5c6370',
      function: '#61afef',
      regex: '#56b6c2',
      attr: '#e06c75',
      tag: '#e06c75',
      param: '#61afef',
      default: '#abb2bf',
    },
    block: {
      bg: '#282c34',
      border: '#3e4451',
      labelColor: '#5c6370',
    },
  },
  {
    id: 'solarized-dark',
    name: 'Solarized Dark',
    colors: {
      keyword: '#859900',
      string: '#2aa198',
      number: '#d33682',
      comment: '#586e75',
      function: '#268bd2',
      regex: '#dc322f',
      attr: '#b58900',
      tag: '#268bd2',
      param: '#93a1a1',
      default: '#839496',
    },
    block: {
      bg: '#002b36',
      border: '#073642',
      labelColor: '#586e75',
    },
  },
  {
    id: 'solarized-light',
    name: 'Solarized Light',
    colors: {
      keyword: '#859900',
      string: '#2aa198',
      number: '#d33682',
      comment: '#93a1a1',
      function: '#268bd2',
      regex: '#dc322f',
      attr: '#b58900',
      tag: '#268bd2',
      param: '#657b83',
      default: '#586e75',
    },
    block: {
      bg: '#fdf6e3',
      border: '#eee8d5',
      labelColor: '#93a1a1',
    },
  },
  {
    id: 'dracula',
    name: 'Dracula',
    colors: {
      keyword: '#ff79c6',
      string: '#f1fa8c',
      number: '#bd93f9',
      comment: '#6272a4',
      function: '#50fa7b',
      regex: '#ffb86c',
      attr: '#8be9fd',
      tag: '#ff79c6',
      param: '#ff79c6',
      default: '#f8f8f2',
    },
    block: {
      bg: '#282a36',
      border: '#44475a',
      labelColor: '#6272a4',
    },
  },
  {
    id: 'github-dark',
    name: 'GitHub Dark',
    colors: {
      keyword: '#ff7b72',
      string: '#a5d6ff',
      number: '#79c0ff',
      comment: '#8b949e',
      function: '#d2a8ff',
      regex: '#a5d6ff',
      attr: '#79c0ff',
      tag: '#7ee787',
      param: '#ffa657',
      default: '#c9d1d9',
    },
    block: {
      bg: '#0d1117',
      border: '#21262d',
      labelColor: '#8b949e',
    },
  },
]

export function getCodeTheme(themeId) {
  const t = codeThemeOptions.find((x) => x.id === themeId)
  return t || codeThemeOptions[0]
}
