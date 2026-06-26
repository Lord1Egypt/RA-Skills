---
number: 992
title: `$subscribe`  miss mutations with type of `direct`  immediately after`patch`  mutations
type: other
state: open
created: 2022-01-25
url: "https://github.com/vuejs/pinia/issues/992"
reactions: 2
comments: 10
labels: "[discussion, has workaround]"
---

# `$subscribe`  miss mutations with type of `direct`  immediately after`patch`  mutations

in $subscribe ,I use `console` to print the mutations and states when the states  change : 
```javascript
 store.$subscribe((mutations, state) => {
    console.log('states change :', mutations, state);
  });
```

it works correct when I change the state directly or  use  `$pacth`  singlely
```javascript
// the both ways of the follow work correct
// 1. change directly : ouput is { type：‘direct’ ,... } 
 store.count++


// 2.use $patch : output is {type: 'patch object',...}
store.$patch({
    key: `${Math.random()}`,
 });
```

but when I use them together as follow,the mutation with type of 'direct' will miss ,there is only {type: 'patch object',...} on console , and the `count` value  printed was still the old value， actually had increased .  seem to not be detected ？
...