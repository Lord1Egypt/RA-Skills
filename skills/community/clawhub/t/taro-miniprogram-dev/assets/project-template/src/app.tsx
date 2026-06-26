import { Component } from 'react'
import './styles/global.scss'

class App extends Component {
  componentDidMount() {}
  componentDidShow() {}
  componentDidHide() {}
  render() {
    return this.props.children
  }
}

export default App
