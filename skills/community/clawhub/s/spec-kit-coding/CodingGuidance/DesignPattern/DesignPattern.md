# 程序设计的一些通用结构

参考并总结 [设计模式目录：22种设计模式](https://refactoringguru.cn/design-patterns/catalog)。

更多参考 [设计模式 | 菜鸟教程](https://www.runoob.com/python-design-pattern/python-design-pattern-tutorial.html)。



------

## RAII

使用 RAII（Resource Acquisition Is Initialization）模式可以确保资源在对象的生命周期内正确初始化和释放。

应尽量把程序结构定为多个类的多模块拆分和接力协作，并且，每个类写为 RAII 模式，确保类实例的所有内部资源的初始化和释放与其对象的生命周期一致，达到多次 启停的目的，方便外部使用和管理。

参考 同文件夹 的 `RAII` 目录。内有详细注释说明。



---

## 创建型模式

参考 同文件夹 的 `Pimpl` 和 `Pimpl2`、`Builder` 和 `Singleton` 目录。内有详细注释说明。



---

## 结构型模式



### 适配器(adapter) & 桥接(bridge) & 组合(composite)

适配器(adapter) 可以写为 多种信息类型之间的转换 的组件：选定一个内部的统一的格式，做例如 setIn() 和 setOut() 的方法。

如选定 jsonObj (比如 `nlohmann::json`) 作为内部的中间统一格式，就可以有 `jsonObj.setIn( jsonStr | jsonObj | xmlStr | xmlObj | yamlStr | yamlObj ... )`，以及 `jsonObj.setOut( ... )`。还可以参考 pcl 库的 各种滤波器 的使用，其中就有 `setInput()` 方法 并 重载了多种输入。



上下二者类似 ↑ ↓



桥接(bridge) 可以作为 多对多的控制或调用 的模块（模块为比组件高一个级别的层级，包括多个组件构成） 的结构：上层有多种对外接口功能，下层也有多种平台或者其它情况的各种适配，那种就可以设计一个中间层，只保留少量的、通用的接口。



类似于 ↓



组合(composite) 可以用于 信息结构呈现为树状或网状的 信息存储：将每个信息节点，用 多叉树 或者 网 的数据结构，组合到一起，再添加各种处理操作。




### 装饰器(decorator) & 外观(facade) & 代理(proxy)

这几个类似 wrap 封装一层 的结构 或 方法：比如现在有 三种 三方组件库 A、B 和 C，他们具体接口不一样但是功能行为类似，比如多种社交媒体平台接口，均有发帖和获取贴等，现在要写个上层使用统一的结构对其操作，就可以加一个 wrap 包装/封装一层，先来个比如 WrapBasic 的抽象类定义通用的必要的接口，再写 AWrap 类继承 WrapBasic 并实现 特定接口 来操作 A 库的接口，其它 B 和 C 同理。现在就有了 AWrap、BWrap 和 CWrap 三种 接口统一的 类 可供操作 三种库。



---

## 行为模式



### 行为链条(chain) & 迭代器(iterator)

行为链条(chain)：用于链式的处理逻辑，比如要进行一系列有先后的检查步骤，并要方便的可以在中间增减检查步骤：使用链表结构存储检查函数或者检查抽象类智能指针等，核心就是使用链表的数据结构，如 `std::list`。

对于链条数据结构的遍历，就需要迭代器如下。



迭代器(iterator)：搞一个对某个数据结构的指定迭代/遍历方法的迭代器类：如对于 二叉树 或 网 的数据结构有 深度优先 和 广度优先 等遍历方法。

自己实现的数据结构，需要实现基本的方法：增删改查；我再加四个：判排复遍——判空、排序（对于哈希表结构则没有）、复位（清空）和遍历。

对于遍历，可以两种：

1. 提供遍历的方法比如 `traverse(const TraverseFunction& traverse_func)`，传入一个遍历的回调函数，如下。还可以增加遍历方法指定的形参。

   ```c++
   template <typename Key, typename Value>
   void GeneralContainer<Key, Value>::traverse(const TraverseFunction& traverse_func) const
   {
       if(!traverse_func) {
           return;
       }
       std::shared_lock<std::shared_mutex> lock(mMutex);
       for (const auto& it : mList) { // 正序遍历
           traverse_func(it);
       }
   }
   ```

2. 提供这里所说的迭代器类，不同的迭代器类代表对这个数据结构的不同的遍历方法。比如 std 标准库 容器的:

   ```c++
   std::vector<int> myVector = {1, 2, 3, 4, 5};
   auto forwardIter = myVector.begin();    // forwardIter 指向 第一个 元素，forwardIter++ 则移动到第二个元素。
   auto backwardIter = myVector.rbegin();  // backwardIter 指向 最后一个 元素，backwardIter++ 则移动到倒数第二个元素。
   ```



### 中介/中央调度(mediator) & 命令(command)

中介/中央调度(mediator)：多个地方的组件请求执行动作，如果其之间有冲突，比如多个 app 要往 状态栏 弹带优先级的信息，不要各自都直接弹出，因为需要优先级高的始终在最上，因此需要一个中介或者中央调度的组件或模块，多个地方的 app 统一往这个 中介 请求弹信息，由 中介 选择 往信息栏 插入 的位置并插入、或者检查黑名单并忽略等等。

还有 GUI 程序中的弹窗场景，有的界面可以弹窗，有的界面不允许弹窗，等等还有其它设计情况，因此需要一个中介去统一接受弹窗请求并处理。



命令(command)：思想是，打包一个执行动作以及其传入参数：一个执行动作，如 GUI 程序中 用户点击一个按键，索要执行的一系列程序，封装为一个函数（多种按键有枚举等关系，或者按键为登录等需要传入参数的），需要执行动作时候，打包函数和函数实参 如用 `std::bind()`，放到一个队列中去执行。可以参考 线程池 [progschj/ThreadPool: A simple C++11 Thread Pool implementation](https://github.com/progschj/ThreadPool) 的使用方法。

如上面的中介就需要类似 命令 的方式，设置接口，处理来自其它组件的 "命令"。



### 备忘录(memento) & 访问者(visitor)

备忘录(memento)：针对需要给组件当前状态整一个快照、用于存留到历史记录中用于后面可能的再现/回放等场景，则给每个组件添加一个 比如 save() 或者 snapshot() 的方法，方法返回 保存了这个组件所有当前信息的（足够回放的）通用 Memento 类或者这个组件的一份克隆，有一个 history 类进行保存并在每次进行快照的时候增长。

参考 [C++ 备忘录模式讲解和代码示例](https://refactoringguru.cn/design-patterns/memento/cpp/example)。



访问者(visitor)：给需要被访问的类添加一个类似于 Accept(Visitor* visitor) 的函数，传入 visitor 后调用其 visitor->VisitConcreteComponentA(this);，在 VisitConcreteComponentA() 内部访问 当前类实例。

参考 [C++ 访问者模式讲解和代码示例](https://refactoringguru.cn/design-patterns/visitor/cpp/example)。



### 观察者(observer) / 发布-订阅(publisher-subscribers)

观察者订阅发布者，发布者执行发布操作（可带参数），即所有订阅这个发布者的观察者的订阅回调函数都会被执行。

发布-订阅 模式的 C++ 库，如：libsigcplusplus、KDBindings、等 信号槽 类型库，以及 dds 进程间通讯库等。



### 状态设计(state) / 有限状态机(FSM)

将组件或模块或设备的功能执行划分为一些状态以及状态之间的转移条件，画出状态转移图，即设计为 有限状态机 FSM，进行业务的编程建模。

简单的可以为 switch-case 语句进行，复杂的、功能多的可以上库，如以下库等：

- StateMachine [endurodave/StateMachine: State Machine Design in C++](https://github.com/endurodave/StateMachine)，C++，编程风格为 定义 事件 event 下 所有 状态 的 行为，以及状态进入和退出的行为等。
- UML State Machine in C [kiishor/UML-State-Machine-in-C: A minimalist UML State machine framework for finite state machine and hierarchical state machine in C](https://github.com/kiishor/UML-State-Machine-in-C)，C 语言，轻量级（可用于 mcu），表格化构建状态机，支持层级状态机。
- stateMachine [misje/stateMachine: A feature-rich, yet simple finite state machine (FSM) implementation in C](https://github.com/misje/stateMachine)，C 语言，简易简陋超轻量状态机，可用于 mcu。



FPGA 的 IP核 设计中常用 FSM 概念进行建模，有几种不同的写法，Verilog 编码 的例子可见 [HDL-FPGA-study-and-norms/FPGA学习和规范 的参考源码/具体模块/fsm 一段和三段状态机例子 at main · Staok/HDL-FPGA-study-and-norms](https://github.com/Staok/HDL-FPGA-study-and-norms/tree/main/FPGA学习和规范 的参考源码/具体模块/fsm 一段和三段状态机例子)。



### 策略(strategy) & 模板方法(template-method) / 类多态

策略(strategy)：针对需要对于一定的数据集，使用不同的策略来获取不同的结果。策略可以使用基类和衍生类的多态来实现，这样，创建不同种类的策略类实例并给到执行，就是使用了不同的策略。

参考 [C++ 策略模式讲解和代码示例](https://refactoringguru.cn/design-patterns/strategy/cpp/example)。



模板方法(template-method)：基类定义执行操作（里面包含多种子操作以及特定顺序）的一个（纯）虚函数，并定义一些子操作（（纯）虚）函数，继承这个基类的多个衍生类中，使用不同的实现重写这些执行操作的函数（不同的子操作、顺序等，以及不同的操作实现），使用类多态，做到创建不同的类实例，用于对数据执行不同的策略操作。

参考 [C++ 模板方法模式讲解和代码示例](https://refactoringguru.cn/design-patterns/template-method/cpp/example)。
