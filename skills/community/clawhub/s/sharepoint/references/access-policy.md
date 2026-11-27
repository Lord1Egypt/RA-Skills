# SharePoint access policy

An access policy limits which endpoints SharePoint connections may call through Maton. SharePoint doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/sharepoint#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for SharePoint: its 112 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create sharepoint --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/sites"},
    {"method": "GET", "path": "v1.0/sites/root"},
    {"method": "GET", "path": "v1.0/sites/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/{id}"},
    {"method": "GET", "path": "v1.0/sites/delta"},
    {"method": "GET", "path": "v1.0/sites/getAllSites"},
    {"method": "GET", "path": "v1.0/sites/{id}/sites"},
    {"method": "GET", "path": "v1.0/sites/{id}/analytics"},
    {"method": "GET", "path": "v1.0/sites/{id}/operations"},
    {"method": "GET", "path": "v1.0/me/followedSites"},
    {"method": "GET", "path": "v1.0/users/{id}/followedSites"},
    {"method": "GET", "path": "v1.0/groups/{id}/sites/**"},
    {"method": "GET", "path": "v1.0/sites/**"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/drive"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/operations"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/subscriptions"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/fields"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/driveItem"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/driveItem/content"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/versions"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/versions/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/analytics"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/columns"},
    {"method": "GET", "path": "v1.0/sites/{id}/columns/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/columns"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/columns/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/contentTypes"},
    {"method": "GET", "path": "v1.0/sites/{id}/contentTypes/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/contentTypes/{id}/columns"},
    {"method": "GET", "path": "v1.0/sites/{id}/contentTypes/{id}/columns/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/contentTypes"},
    {"method": "GET", "path": "v1.0/sites/{id}/lists/{id}/contentTypes/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout"},
    {"method": "POST", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id}/getPositionOfWebPart"},
    {"method": "POST", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout/horizontalSections/{id}/columns/{id}/webparts/{id}/getPositionOfWebPart"},
    {"method": "POST", "path": "v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout/verticalSection/webparts/{id}/getPositionOfWebPart"},
    {"method": "GET", "path": "v1.0/sites/{id}/permissions"},
    {"method": "GET", "path": "v1.0/sites/{id}/permissions/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/groups"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/groups/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/groups/{id}/sets"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/sets/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/sets/{id}/children"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/sets/{id}/terms/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/children"},
    {"method": "GET", "path": "v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/relations"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive"},
    {"method": "GET", "path": "v1.0/sites/{id}/drives"},
    {"method": "GET", "path": "v1.0/sites/{id}/drives/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/root/children"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/items/{id}"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/items/{id}/children"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/items/{id}/content"},
    {"method": "POST", "path": "v1.0/sites/{id}/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/sites/{id}/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/groups/{id}/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/{id}/preview"},
    {"method": "GET", "path": "v1.0/drives/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/root"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/root:/**"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/listItem"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/retentionLabel"},
    {"method": "GET", "path": "v1.0/drives/{id}/recent"},
    {"method": "GET", "path": "v1.0/drives/{id}/sharedWithMe"},
    {"method": "GET", "path": "v1.0/drives/{id}/following"},
    {"method": "GET", "path": "v1.0/drives/{id}/bundles"},
    {"method": "GET", "path": "v1.0/drives/{id}/bundles/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/special"},
    {"method": "GET", "path": "v1.0/drives/{id}/special/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/special/{id}/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/list"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/content"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/{id}/preview"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/delta"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/delta"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/{id}"},
    {"method": "POST", "path": "v1.0/search/query"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}/content"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions/{id}/content"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/permissions"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/permissions/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics/allTime"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics/lastSevenDays"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/subscriptions"},
    {"method": "GET", "path": "v1.0/drives/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drives/**"}
  ],
  "deny": []
}
```

## Endpoints

The SharePoint endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1.0/sites | read | sites | Search sites (?search=) or list sites. |
| GET | v1.0/sites/root | read | sites | Get the tenant's root site. |
| GET | v1.0/sites/{id} | read | sites | Get a site by ID, or the root site of a hostname (sites/{hostname}:). |
| GET | v1.0/sites/{id}/{id} | read | sites | Get a site by hostname and one-segment path (sites/{hostname}:/{path}); deeper paths match the sites tree row. |
| GET | v1.0/sites/delta | read | sites | Track changes to sites. |
| GET | v1.0/sites/getAllSites | read | sites | List sites across geographies. |
| GET | v1.0/sites/{id}/sites | read | sites | List subsites. |
| GET | v1.0/sites/{id}/analytics | read | sites | Get site activity analytics. |
| GET | v1.0/sites/{id}/operations | read | sites | List long-running site operations. |
| GET | v1.0/me/followedSites | read | sites | List the sites the signed-in user follows. |
| GET | v1.0/users/{id}/followedSites | read | sites | List the sites a user follows. |
| GET | `v1.0/groups/{id}/sites/**` | read | sites | Any GET under a group's team site (groups/{id}/sites/root and below; all reads). |
| POST | v1.0/users/{id}/followedSites/add | write | sites | Follow sites. |
| POST | v1.0/users/{id}/followedSites/remove | write | sites | Unfollow sites. |
| GET | `v1.0/sites/**` | read | sites | Any GET under sites: path-addressed sites, lists, items, drives, pages, permissions, term store, function segments (all reads). |
| GET | v1.0/sites/{id}/lists | read | lists | List the lists in a site. |
| GET | v1.0/sites/{id}/lists/{id} | read | lists | Get a list. |
| GET | v1.0/sites/{id}/lists/{id}/drive | read | lists | Get the document library drive behind a list. |
| GET | v1.0/sites/{id}/lists/{id}/operations | read | lists | List long-running operations on a list. |
| POST | v1.0/sites/{id}/lists | write | lists | Create a list. |
| PATCH | v1.0/sites/{id}/lists/{id} | write | lists | Update a list. |
| DELETE | v1.0/sites/{id}/lists/{id} | write | lists | Delete a list. |
| GET | v1.0/sites/{id}/lists/{id}/subscriptions | read | lists | List webhook subscriptions on a list. |
| POST | v1.0/sites/{id}/lists/{id}/subscriptions | write | lists | Create a webhook subscription on a list. |
| GET | v1.0/sites/{id}/lists/{id}/items | read | list items | List the items in a list (?$expand=fields). |
| GET | v1.0/sites/{id}/lists/{id}/items/{id} | read | list items | Get a list item, or track changes with items/delta. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/fields | read | list items | Get a list item's column values. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/driveItem | read | list items | Get the file behind a document library item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/driveItem/content | read | list items | Download the file behind a document library item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/versions | read | list items | List the versions of a list item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/versions/{id} | read | list items | Get one version of a list item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/analytics | read | list items | Get activity analytics for a list item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions | read | list items | List the document set versions of an item. |
| GET | v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions/{id} | read | list items | Get a document set version. |
| POST | v1.0/sites/{id}/lists/{id}/items | write | list items | Create a list item. |
| PATCH | v1.0/sites/{id}/lists/{id}/items/{id} | write | list items | Update a list item. |
| PATCH | v1.0/sites/{id}/lists/{id}/items/{id}/fields | write | list items | Update a list item's column values. |
| DELETE | v1.0/sites/{id}/lists/{id}/items/{id} | write | list items | Delete a list item. |
| POST | v1.0/sites/{id}/lists/{id}/items/{id}/createLink | write | list items | Create a sharing link for a list item. |
| POST | v1.0/sites/{id}/lists/{id}/items/{id}/versions/{id}/restoreVersion | write | list items | Restore an earlier version of a list item. |
| POST | v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions | write | list items | Capture a new document set version. |
| POST | v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions/{id}/restore | write | list items | Restore a document set version. |
| DELETE | v1.0/sites/{id}/lists/{id}/items/{id}/documentSetVersions/{id} | write | list items | Delete a document set version. |
| GET | v1.0/sites/{id}/columns | read | columns | List site columns. |
| GET | v1.0/sites/{id}/columns/{id} | read | columns | Get a site column. |
| GET | v1.0/sites/{id}/lists/{id}/columns | read | columns | List the columns of a list. |
| GET | v1.0/sites/{id}/lists/{id}/columns/{id} | read | columns | Get a list column. |
| POST | v1.0/sites/{id}/columns | write | columns | Create a site column. |
| PATCH | v1.0/sites/{id}/columns/{id} | write | columns | Update a site column. |
| DELETE | v1.0/sites/{id}/columns/{id} | write | columns | Delete a site column. |
| POST | v1.0/sites/{id}/lists/{id}/columns | write | columns | Create a list column. |
| PATCH | v1.0/sites/{id}/lists/{id}/columns/{id} | write | columns | Update a list column. |
| DELETE | v1.0/sites/{id}/lists/{id}/columns/{id} | write | columns | Delete a list column. |
| GET | v1.0/sites/{id}/contentTypes | read | content types | List site content types. |
| GET | v1.0/sites/{id}/contentTypes/{id} | read | content types | Get a site content type. |
| GET | v1.0/sites/{id}/contentTypes/{id}/columns | read | content types | List the columns of a content type. |
| GET | v1.0/sites/{id}/contentTypes/{id}/columns/{id} | read | content types | Get a content type column. |
| GET | v1.0/sites/{id}/lists/{id}/contentTypes | read | content types | List the content types of a list. |
| GET | v1.0/sites/{id}/lists/{id}/contentTypes/{id} | read | content types | Get a list content type. |
| POST | v1.0/sites/{id}/contentTypes | write | content types | Create a site content type. |
| PATCH | v1.0/sites/{id}/contentTypes/{id} | write | content types | Update a site content type. |
| DELETE | v1.0/sites/{id}/contentTypes/{id} | write | content types | Delete a site content type. |
| POST | v1.0/sites/{id}/contentTypes/{id}/columns | write | content types | Add a column to a content type. |
| PATCH | v1.0/sites/{id}/contentTypes/{id}/columns/{id} | write | content types | Update a content type column. |
| DELETE | v1.0/sites/{id}/contentTypes/{id}/columns/{id} | write | content types | Remove a column from a content type. |
| POST | v1.0/sites/{id}/contentTypes/{id}/publish | write | content types | Publish a content type from the content type hub. |
| POST | v1.0/sites/{id}/contentTypes/{id}/unpublish | write | content types | Unpublish a content type. |
| POST | v1.0/sites/{id}/contentTypes/{id}/associateWithHubSites | write | content types | Associate a content type with hub sites. |
| POST | v1.0/sites/{id}/contentTypes/{id}/copyToDefaultContentLocation | write | content types | Copy a file to a content type's default content location. |
| POST | v1.0/sites/{id}/contentTypes/addCopy | write | content types | Add a copy of a content type to a site. |
| POST | v1.0/sites/{id}/contentTypes/addCopyFromContentTypeHub | write | content types | Sync a content type from the content type hub. |
| POST | v1.0/sites/{id}/lists/{id}/contentTypes/addCopy | write | content types | Add a copy of a site content type to a list. |
| POST | v1.0/sites/{id}/lists/{id}/contentTypes/addCopyFromContentTypeHub | write | content types | Sync a hub content type to a list. |
| PATCH | v1.0/sites/{id}/lists/{id}/contentTypes/{id} | write | content types | Update a list content type. |
| DELETE | v1.0/sites/{id}/lists/{id}/contentTypes/{id} | write | content types | Remove a content type from a list. |
| GET | v1.0/sites/{id}/pages | read | pages | List the pages of a site. |
| GET | v1.0/sites/{id}/pages/{id} | read | pages | Get a page. |
| GET | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage | read | pages | Get a site page with its sitePage properties. |
| GET | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts | read | pages | List the web parts on a page. |
| GET | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id} | read | pages | Get a web part. |
| GET | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout | read | pages | Get a page's canvas layout. |
| POST | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id}/getPositionOfWebPart | read | pages | Get the position of a web part on its page (POST action that only reads). |
| POST | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout/horizontalSections/{id}/columns/{id}/webparts/{id}/getPositionOfWebPart | read | pages | Get the position of a web part in a horizontal section (read-only action). |
| POST | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/canvasLayout/verticalSection/webparts/{id}/getPositionOfWebPart | read | pages | Get the position of a web part in the vertical section (read-only action). |
| POST | v1.0/sites/{id}/pages | write | pages | Create a page. |
| PATCH | v1.0/sites/{id}/pages/{id} | write | pages | Update a page. |
| PATCH | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage | write | pages | Update a site page. |
| DELETE | v1.0/sites/{id}/pages/{id} | write | pages | Delete a page. |
| POST | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/publish | write | pages | Publish a site page. |
| POST | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts | write | pages | Add a web part to a page. |
| PATCH | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id} | write | pages | Update a web part. |
| DELETE | v1.0/sites/{id}/pages/{id}/microsoft.graph.sitePage/webParts/{id} | write | pages | Delete a web part. |
| GET | v1.0/sites/{id}/permissions | read | site permissions | List the application permissions on a site. |
| GET | v1.0/sites/{id}/permissions/{id} | read | site permissions | Get a site permission. |
| POST | v1.0/sites/{id}/permissions | write | site permissions | Grant an application permission on a site. |
| PATCH | v1.0/sites/{id}/permissions/{id} | write | site permissions | Update a site permission. |
| DELETE | v1.0/sites/{id}/permissions/{id} | write | site permissions | Remove a site permission. |
| GET | v1.0/sites/{id}/termStore | read | term store | Get a site's term store. |
| GET | v1.0/sites/{id}/termStore/groups | read | term store | List term groups. |
| GET | v1.0/sites/{id}/termStore/groups/{id} | read | term store | Get a term group. |
| GET | v1.0/sites/{id}/termStore/groups/{id}/sets | read | term store | List the term sets in a group. |
| GET | v1.0/sites/{id}/termStore/sets/{id} | read | term store | Get a term set. |
| GET | v1.0/sites/{id}/termStore/sets/{id}/children | read | term store | List the top-level terms of a term set. |
| GET | v1.0/sites/{id}/termStore/sets/{id}/terms/{id} | read | term store | Get a term. |
| GET | v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/children | read | term store | List the child terms of a term. |
| GET | v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/relations | read | term store | List the relations of a term. |
| PATCH | v1.0/sites/{id}/termStore | write | term store | Update term store settings. |
| POST | v1.0/sites/{id}/termStore/groups | write | term store | Create a term group. |
| DELETE | v1.0/sites/{id}/termStore/groups/{id} | write | term store | Delete a term group. |
| POST | v1.0/sites/{id}/termStore/sets | write | term store | Create a term set. |
| PATCH | v1.0/sites/{id}/termStore/sets/{id} | write | term store | Update a term set. |
| DELETE | v1.0/sites/{id}/termStore/sets/{id} | write | term store | Delete a term set. |
| POST | v1.0/sites/{id}/termStore/sets/{id}/children | write | term store | Create a top-level term. |
| POST | v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/children | write | term store | Create a child term. |
| PATCH | v1.0/sites/{id}/termStore/sets/{id}/terms/{id} | write | term store | Update a term. |
| DELETE | v1.0/sites/{id}/termStore/sets/{id}/terms/{id} | write | term store | Delete a term. |
| POST | v1.0/sites/{id}/termStore/sets/{id}/terms/{id}/relations | write | term store | Create a relation between terms. |
| GET | v1.0/sites/{id}/drive | read | site drives | Get a site's default document library. |
| GET | v1.0/sites/{id}/drives | read | site drives | List a site's document libraries. |
| GET | v1.0/sites/{id}/drives/{id} | read | site drives | Get one of a site's document libraries. |
| GET | v1.0/sites/{id}/drive/root/children | read | site drives | List the root folder of a site's default document library. |
| GET | v1.0/sites/{id}/drive/items/{id} | read | site drives | Get an item in a site's default document library. |
| GET | v1.0/sites/{id}/drive/items/{id}/children | read | site drives | List a folder in a site's default document library. |
| GET | v1.0/sites/{id}/drive/items/{id}/content | read | site drives | Download a file from a site's default document library. |
| POST | v1.0/sites/{id}/drive/items/{id}/preview | read | site drives | Get a short-lived preview URL for a file in a site's default document library. |
| POST | v1.0/sites/{id}/drives/{id}/items/{id}/preview | read | site drives | Get a short-lived preview URL for a file in a site document library. |
| POST | v1.0/groups/{id}/drive/items/{id}/preview | read | site drives | Get a short-lived preview URL for a file in a group's document library. |
| POST | v1.0/drives/{id}/items/{id}/{id}/preview | read | site drives | Preview a file addressed by parent ID and name (items/{parent-id}:/{filename}:/preview). |
| GET | v1.0/drives/{id} | read | drives | Get a drive (document library) addressed by ID. |
| GET | v1.0/drives/{id}/root | read | items | Get the root folder of a drive (document library) addressed by ID. |
| GET | v1.0/drives/{id}/root/children | read | items | List the items in the root folder of a drive (document library) addressed by ID. |
| GET | `v1.0/drives/{id}/root:/**` | read | items | Path-addressed reads in a drive (document library) addressed by ID: root:/path, root:/path:/children, :/content, :/versions, :/workbook/... (any GET). |
| GET | v1.0/drives/{id}/items/{id} | read | items | Get a drive item by ID. |
| GET | v1.0/drives/{id}/items/{id}/children | read | items | List the children of a folder. |
| GET | v1.0/drives/{id}/items/{id}/listItem | read | items | Get the SharePoint list item behind a drive item. |
| GET | v1.0/drives/{id}/items/{id}/retentionLabel | read | items | Get the retention label on a drive item. |
| GET | v1.0/drives/{id}/recent | read | items | List recently used files. |
| GET | v1.0/drives/{id}/sharedWithMe | read | items | List files shared with the user. |
| GET | v1.0/drives/{id}/following | read | items | List followed drive items. |
| GET | v1.0/drives/{id}/bundles | read | items | List bundles (albums) in the drive. |
| GET | v1.0/drives/{id}/bundles/{id} | read | items | Get a bundle. |
| GET | v1.0/drives/{id}/special | read | items | List special folders. |
| GET | v1.0/drives/{id}/special/{id} | read | items | Get a special folder (documents, photos, music, approot, ...). |
| GET | v1.0/drives/{id}/special/{id}/children | read | items | List the items in a special folder. |
| GET | v1.0/drives/{id}/list | read | items | Get the SharePoint list that backs the drive. |
| POST | v1.0/drives/{id}/root/children | write | items | Create a folder or item in the root folder. |
| POST | v1.0/drives/{id}/items/{id}/children | write | items | Create a folder or item inside a folder. |
| PATCH | v1.0/drives/{id}/items/{id} | write | items | Update a drive item: rename, move, change metadata. |
| DELETE | v1.0/drives/{id}/items/{id} | write | items | Delete a drive item (moves it to the recycle bin). |
| POST | v1.0/drives/{id}/items/{id}/copy | write | items | Copy a drive item to another location. |
| POST | v1.0/drives/{id}/items/{id}/restore | write | items | Restore a deleted drive item. |
| POST | v1.0/drives/{id}/items/{id}/permanentDelete | write | items | Permanently delete a drive item. |
| POST | v1.0/drives/{id}/items/{id}/follow | write | items | Follow a drive item. |
| POST | v1.0/drives/{id}/items/{id}/unfollow | write | items | Stop following a drive item. |
| POST | v1.0/drives/{id}/items/{id}/checkout | write | items | Check out a file so others cannot edit it. |
| POST | v1.0/drives/{id}/items/{id}/checkin | write | items | Check in a checked-out file. |
| POST | v1.0/drives/{id}/items/{id}/discardCheckout | write | items | Discard the checkout of a file. |
| POST | v1.0/drives/{id}/items/{id}/assignSensitivityLabel | write | items | Assign a sensitivity label to a file (metered API). |
| POST | v1.0/drives/{id}/items/{id}/extractSensitivityLabels | write | items | Extract sensitivity labels and update the item's label metadata. |
| PATCH | v1.0/drives/{id}/items/{id}/retentionLabel | write | items | Set or lock the retention label on a drive item. |
| DELETE | v1.0/drives/{id}/items/{id}/retentionLabel | write | items | Remove the retention label from a drive item. |
| POST | v1.0/drives/{id}/bundles | write | items | Create a bundle (album). |
| GET | v1.0/drives/{id}/items/{id}/content | read | content | Download the contents of a file (also ?format=pdf conversion). |
| POST | v1.0/drives/{id}/items/{id}/preview | read | content | Get a short-lived embeddable preview URL for a file; nothing is stored or shared. |
| POST | v1.0/drives/{id}/root:/{id}/preview | read | content | Preview a file addressed by path in the root folder (root:/file:/preview). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/preview | read | content | Preview a file addressed by path one folder deep. |
| POST | v1.0/drives/{id}/root:/{id}/{id}/{id}/preview | read | content | Preview a file addressed by path two folders deep. |
| PUT | v1.0/drives/{id}/items/{id}/content | write | content | Replace the contents of an existing file (simple upload). |
| PUT | v1.0/drives/{id}/items/{id}/{id}/content | write | content | Upload a new file by parent ID and name (items/{parent-id}:/{filename}:/content). |
| PUT | `v1.0/drives/{id}/root:/**` | write | content | Upload or replace a file addressed by path (root:/path:/content). |
| POST | v1.0/drives/{id}/items/{id}/createUploadSession | write | content | Create a resumable upload session for an existing file. |
| POST | v1.0/drives/{id}/items/{id}/{id}/createUploadSession | write | content | Create a resumable upload session for a new file by parent ID and name. |
| GET | v1.0/drives/{id}/root/{id} | read | search | Search the drive or track changes with a function segment: root/search(q='text'), root/delta(token='...'). |
| GET | v1.0/drives/{id}/root/delta | read | search | Track changes in the drive (delta). |
| GET | v1.0/drives/{id}/items/{id}/delta | read | search | Track changes under a folder (delta). |
| GET | v1.0/drives/{id}/items/{id}/{id} | read | search | Function segment on an item: search(q='text'), delta(token='...'), getActivitiesByInterval(...). |
| POST | v1.0/search/query | read | search | Microsoft Search query across files, sites, lists and list items (POST only carries the query). |
| GET | v1.0/drives/{id}/items/{id}/thumbnails | read | thumbnails | List the thumbnail sets of a drive item. |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id} | read | thumbnails | Get a thumbnail set. |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id} | read | thumbnails | Get one thumbnail size (small, medium, large). |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}/content | read | thumbnails | Download a thumbnail image. |
| GET | v1.0/drives/{id}/items/{id}/versions | read | versions | List the versions of a file. |
| GET | v1.0/drives/{id}/items/{id}/versions/{id} | read | versions | Get one version of a file. |
| GET | v1.0/drives/{id}/items/{id}/versions/{id}/content | read | versions | Download the contents of an earlier version. |
| POST | v1.0/drives/{id}/items/{id}/versions/{id}/restoreVersion | write | versions | Restore an earlier version as the current one. |
| DELETE | v1.0/drives/{id}/items/{id}/versions/{id} | write | versions | Delete a version of a file. |
| GET | v1.0/drives/{id}/items/{id}/permissions | read | permissions | List who a drive item is shared with, including existing sharing links. |
| GET | v1.0/drives/{id}/items/{id}/permissions/{id} | read | permissions | Get one sharing permission. |
| POST | v1.0/drives/{id}/items/{id}/createLink | write | permissions | Create a sharing link for a drive item. |
| POST | v1.0/drives/{id}/items/{id}/invite | write | permissions | Share a drive item with people and optionally email them. |
| POST | v1.0/drives/{id}/items/{id}/permissions | write | permissions | Add a permission to a drive item. |
| PATCH | v1.0/drives/{id}/items/{id}/permissions/{id} | write | permissions | Change the roles of a sharing permission. |
| DELETE | v1.0/drives/{id}/items/{id}/permissions/{id} | write | permissions | Remove a sharing permission. |
| POST | v1.0/drives/{id}/items/{id}/permissions/{id}/grant | write | permissions | Grant users access to an existing sharing link. |
| POST | v1.0/drives/{id}/items/{id}/permissions/{id}/revokeGrants | write | permissions | Revoke users' access to a sharing link. |
| POST | v1.0/drives/{id}/items/{id}/validatePermission | write | permissions | Validate a password-protected sharing permission (unverified side effects). |
| GET | v1.0/drives/{id}/items/{id}/analytics | read | analytics | Get view/activity analytics for a drive item. |
| GET | v1.0/drives/{id}/items/{id}/analytics/allTime | read | analytics | Get all-time activity statistics for a drive item. |
| GET | v1.0/drives/{id}/items/{id}/analytics/lastSevenDays | read | analytics | Get the last seven days of activity statistics. |
| GET | v1.0/drives/{id}/items/{id}/subscriptions | read | subscriptions | List webhook subscriptions on a drive item. |
| POST | v1.0/drives/{id}/items/{id}/subscriptions | write | subscriptions | Create a webhook subscription on a drive item. |
| POST | v1.0/subscriptions | write | subscriptions | Create a change-notification webhook subscription. |
| PATCH | v1.0/subscriptions/{id} | write | subscriptions | Renew or update a webhook subscription. |
| DELETE | v1.0/subscriptions/{id} | write | subscriptions | Delete a webhook subscription. |
| POST | v1.0/subscriptions/{id}/reauthorize | write | subscriptions | Reauthorize a webhook subscription. |
| GET | `v1.0/drives/**` | read | drive trees | Any GET under drives addressed by ID, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/drives/**` | write | drive trees | Any other POST under drives addressed by ID, including root:/path: addressed forms. |
| PUT | `v1.0/drives/**` | write | drive trees | Any other PUT under drives addressed by ID, including root:/path: addressed forms. |
| PATCH | `v1.0/drives/**` | write | drive trees | Any other PATCH under drives addressed by ID, including root:/path: addressed forms. |
| DELETE | `v1.0/drives/**` | write | drive trees | Any other DELETE under drives addressed by ID, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drive/**` | read | drive trees | Any GET under a group's document library, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other POST under a group's document library, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PUT under a group's document library, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PATCH under a group's document library, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other DELETE under a group's document library, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drives/**` | read | drive trees | Any GET under a group's document libraries, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other POST under a group's document libraries, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PUT under a group's document libraries, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PATCH under a group's document libraries, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other DELETE under a group's document libraries, including root:/path: addressed forms. |
| POST | `v1.0/sites/**` | write | site trees | Any other POST under sites (lists, items, drives, pages, permissions, term store), including root:/path: addressed forms. |
| PUT | `v1.0/sites/**` | write | site trees | Any other PUT under sites (lists, items, drives, pages, permissions, term store), including root:/path: addressed forms. |
| PATCH | `v1.0/sites/**` | write | site trees | Any other PATCH under sites (lists, items, drives, pages, permissions, term store), including root:/path: addressed forms. |
| DELETE | `v1.0/sites/**` | write | site trees | Any other DELETE under sites (lists, items, drives, pages, permissions, term store), including root:/path: addressed forms. |
| POST | `v1.0/groups/{id}/sites/**` | write | site trees | Any other POST under a group's team site, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/sites/**` | write | site trees | Any other PUT under a group's team site, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/sites/**` | write | site trees | Any other PATCH under a group's team site, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/sites/**` | write | site trees | Any other DELETE under a group's team site, including root:/path: addressed forms. |
| GET | `v1.0/shares/**` | write | shares | Open a sharing link or share ID. Kept out of read: a Prefer: redeemSharingLink header makes this GET grant the caller durable access. |
| POST | v1.0/shares/{id}/permission/grant | write | shares | Grant users access to a sharing link. |
| DELETE | v1.0/shares/{id}/permission | write | shares | Delete the permission behind a sharing link. |
| POST | `v1.0/shares/**` | write | shares | Any other POST under a share. |
| PUT | `v1.0/shares/**` | write | shares | Any PUT under a share, e.g. uploading into a shared folder. |
| PATCH | `v1.0/shares/**` | write | shares | Any PATCH under a share. |
| DELETE | `v1.0/shares/**` | write | shares | Any other DELETE under a share. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes. |
