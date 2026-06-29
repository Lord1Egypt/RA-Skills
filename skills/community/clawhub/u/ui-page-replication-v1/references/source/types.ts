export interface UIPageSchema {
  pageName: string

  regions: UIRegion[]

  modals: UIModal[]

  tabs: UITab[]

  interactions: UIInteraction[]

  dataModel: DataModel
}

export interface UIRegion {
  name: string
  type: "search" | "table" | "toolbar" | "stats" | "form" | "other"
}

export interface UITab {
  name: string
  children: UIRegion[]
}

export interface UIModal {
  name: string
  type: "create" | "edit" | "detail" | "audit" | "log" | "select"
  children: UIRegion[]
}

export interface UIInteraction {
  trigger: string
  action: string
  affects: string[]
}

export interface DataModel {
  entities: Record<string, any>
}