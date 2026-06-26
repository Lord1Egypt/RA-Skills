# Enonic XP Content Type Examples

## Example 1: Blog Post

A typical blog post with title, author reference, publish date, rich-text body, tags, and a featured image.

```xml
<content-type>
  <display-name>Blog Post</display-name>
  <description>A blog article with rich text and media</description>
  <super-type>base:structured</super-type>
  <is-abstract>false</is-abstract>
  <is-final>true</is-final>
  <form>
    <input name="title" type="TextLine">
      <label>Title</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="author" type="ContentSelector">
      <label>Author</label>
      <occurrences minimum="1" maximum="1"/>
      <config>
        <allowContentType>${app}:author</allowContentType>
      </config>
    </input>
    <input name="publishDate" type="DateTime">
      <label>Publish Date</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="body" type="HtmlArea">
      <label>Body</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="tags" type="Tag">
      <label>Tags</label>
      <occurrences minimum="0" maximum="0"/>
    </input>
    <input name="featuredImage" type="ImageSelector">
      <label>Featured Image</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
  </form>
</content-type>
```

## Example 2: Product with ComboBox

A product page with price, description, categorization, and multi-image gallery.

```xml
<content-type>
  <display-name>Product</display-name>
  <description>Product listing with category and gallery</description>
  <super-type>base:structured</super-type>
  <is-abstract>false</is-abstract>
  <is-final>true</is-final>
  <form>
    <input name="name" type="TextLine">
      <label>Product Name</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="price" type="Double">
      <label>Price</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="description" type="HtmlArea">
      <label>Description</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="category" type="ComboBox">
      <label>Category</label>
      <occurrences minimum="1" maximum="1"/>
      <config>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
        <option value="home">Home</option>
      </config>
    </input>
    <input name="gallery" type="ImageSelector">
      <label>Gallery</label>
      <occurrences minimum="0" maximum="0"/>
      <config/>
    </input>
  </form>
</content-type>
```

## Example 3: Event with Option Set

An event that lets the editor choose between in-person (with address and coordinates) or virtual (with URL and platform).

```xml
<content-type>
  <display-name>Event</display-name>
  <description>Event with in-person or virtual location</description>
  <super-type>base:structured</super-type>
  <form>
    <input name="title" type="TextLine">
      <label>Event Title</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="date" type="DateTime">
      <label>Event Date</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="description" type="HtmlArea">
      <label>Description</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <option-set name="locationType">
      <label>Location Type</label>
      <occurrences minimum="1" maximum="1"/>
      <options minimum="1" maximum="1">
        <option name="inPerson">
          <label>In-Person</label>
          <items>
            <input name="address" type="TextArea">
              <label>Address</label>
              <occurrences minimum="1" maximum="1"/>
            </input>
            <input name="coordinates" type="GeoPoint">
              <label>Map Coordinates</label>
              <occurrences minimum="0" maximum="1"/>
            </input>
          </items>
        </option>
        <option name="virtual">
          <label>Virtual</label>
          <items>
            <input name="url" type="TextLine">
              <label>Meeting URL</label>
              <occurrences minimum="1" maximum="1"/>
            </input>
            <input name="platform" type="TextLine">
              <label>Platform Name</label>
              <occurrences minimum="0" maximum="1"/>
            </input>
          </items>
        </option>
      </options>
    </option-set>
  </form>
</content-type>
```

## Example 4: Person with Item Set

A person content type with repeatable contact info entries.

```xml
<content-type>
  <display-name>Person</display-name>
  <description>Person with contact information</description>
  <super-type>base:structured</super-type>
  <form>
    <input name="firstName" type="TextLine">
      <label>First Name</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="lastName" type="TextLine">
      <label>Last Name</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="photo" type="ImageSelector">
      <label>Photo</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <input name="bio" type="HtmlArea">
      <label>Biography</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <item-set name="contactInfo">
      <label>Contact Info</label>
      <occurrences minimum="0" maximum="0"/>
      <items>
        <input name="label" type="TextLine">
          <label>Label</label>
          <occurrences minimum="1" maximum="1"/>
        </input>
        <input name="value" type="TextLine">
          <label>Value</label>
          <occurrences minimum="1" maximum="1"/>
        </input>
      </items>
    </item-set>
  </form>
</content-type>
```

## Example 5: SEO Mixin

A reusable mixin for SEO metadata that can be added to any content type.

```xml
<!-- File: src/main/resources/site/mixins/seo-metadata/seo-metadata.xml -->
<mixin>
  <display-name>SEO Metadata</display-name>
  <form>
    <input name="metaTitle" type="TextLine">
      <label>Meta Title</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <input name="metaDescription" type="TextArea">
      <label>Meta Description</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <input name="ogImage" type="ImageSelector">
      <label>OG Image</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
  </form>
</mixin>
```

Usage in a content type:

```xml
<content-type>
  <display-name>Article</display-name>
  <super-type>base:structured</super-type>
  <form>
    <input name="title" type="TextLine">
      <label>Title</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="body" type="HtmlArea">
      <label>Body</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <mixin name="seo-metadata"/>
  </form>
</content-type>
```

## Example 6: Folder Content Type

A content type that acts as an organizational container.

```xml
<content-type>
  <display-name>Article Folder</display-name>
  <description>Container for articles</description>
  <super-type>base:folder</super-type>
  <is-abstract>false</is-abstract>
  <is-final>true</is-final>
  <allow-child-content>true</allow-child-content>
  <allow-child-content-type>${app}:article</allow-child-content-type>
  <form/>
</content-type>
```
