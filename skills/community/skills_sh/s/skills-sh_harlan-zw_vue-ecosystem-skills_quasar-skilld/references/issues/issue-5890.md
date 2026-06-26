---
number: 5890
title: Official Support for Drag and Drop
type: feature
state: closed
created: 2019-12-14
url: "https://github.com/quasarframework/quasar/issues/5890"
reactions: 54
comments: 32
labels: "[kind/feature ]"
---

# Official Support for Drag and Drop

**Is your feature request related to a problem? Please describe.**

Some of the most useful and complex Quasar components are difficult to implement with a drag and drop library. See qTable and qTree. 

For example If I wanted to implement drag and drop within qTree with this library 
https://github.com/SortableJS/Vue.Draggable/blob/master/example/components/nested-example.vue
I would need to wrap `q-tree__node` within `<draggable>`. I have no easy way of doing that. 

**Describe the solution you'd like**

Official support and guidance for a Drag and Drop library which supports mobiles and tablets.
It would mean that components structured in such a way that a well known drag and drop library 
such as the above could easily be implemented. 

Examples in the different components docs how the supported library could be used. 

I don't need support for multiple libraries but only one. 

**Describe alternatives you've considered**
Several drag and drop libraries.I have also rebuilt (bodged) both qTable as well as qTree (just finishing) because of this. Recreating those components is a lot of soul destroying work just to get drag and drop working. 

As you can guess I am not the only one to do this see forum posts:
https://forum.quasar-framework.org/topic/3543/drag-and-drop
https://forum.quasar-framework.org/topic/4010/drag-and-drop-in-qtable-did-anyone-succeed
https://forum.quasar-framework.org/topic/4595/q-table-rows-drag-and-drop
https://forum.quasar-framework.org/topic/2619/drag-and-drop-data-table-column-ordering
https://forum.quasar-framework.org/topic/3069/q-list-sortable/2
and more ... I won't list all here. But it is not difficult to see that a lot of people will want drag and drop and will be implementing (most likely badly) their own solutions. 

This is one of the most missed features in Quasar IMO. So hopefully you consider it. 
Thank you for the great work.
  






---

## Top Comments

**@IlCallo** [maintainer] (+5):

Just gonna drop here a reference on how this has been tackled on Angular

https://material.angular.io/cdk/drag-drop/overview

Not sponsoring Angular in any way (quite the opposite) but if someone wants to make an AE for DnD, this can be used as a checklist for common use cases and inspiration for the code

**@ddenev** (+4):

I second this request, although with a small comment.

Indeed, it's about time that Quasar components are empowered with DnD capabilities. The thing is - should the team focus on building these into the core or should they focus on extending the concerned components so that they can be DnD-enabled with 3rd party libraries, such as SortableJS/Vue.Draggable or even with Quasar's built-in one (i.e. TouchPan directive).

At the end, I would like to be able to use DnD but also to be able to fully customize the experience, e.g. ghost styling, drop zones, etc.

@turigeza, I'm in the same boat a...

**@ddenev** (+2):

@OnePunchMan007 , thanks but this is nowhere near **a proper** DnD support.