// content.config.ts — only needed if @nuxt/content is in scope.
// Every collection schema should compose the @nuxtjs/seo content schemas so
// pages get sitemap/robots/OG-image/schema.org metadata for free.
import { defineCollection, defineContentConfig, z } from '@nuxt/content'
import { defineRobotsSchema } from '@nuxtjs/robots/content'
import { defineSitemapSchema } from '@nuxtjs/sitemap/content'
import { defineOgImageSchema } from 'nuxt-og-image/content'
import { defineSchemaOrgSchema } from 'nuxt-schema-org/content'

// Reusable field groups — follow this shared-shape pattern rather than inlining
// zod objects per-collection, so shared shapes (buttons, images, authors)
// stay consistent across content types.
const createImageSchema = () => z.object({
  src: z.string().editor({ input: 'media' }),
  alt: z.string()
})

export default defineContentConfig({
  collections: {
    // One collection per content type. `source` is an array so you can list
    // one `include` entry per locale when i18n is in scope; drop the array
    // down to a single entry for a single-locale app.
    article: defineCollection({
      type: 'page',
      source: [
        { include: 'en/article/*.md' }
        // { include: '<locale>/article/*.md' }, // repeat per additional locale
      ],
      schema: z.object({
        // SEO metadata schemas — always include these on page collections
        robots: defineRobotsSchema(),
        sitemap: defineSitemapSchema(),
        ogImage: defineOgImageSchema(),
        schemaOrg: defineSchemaOrgSchema(),

        // Collection-specific fields
        category: z.string().nonempty(),
        date: z.date(),
        image: createImageSchema().shape.src,
        imageAlt: z.string().nonempty(),
        isPublished: z.boolean().default(false)
      })
    })

    // Add one more defineCollection(...) per static/marketing page type
    // (about, privacy, etc.) following the same shape.
  }
})
