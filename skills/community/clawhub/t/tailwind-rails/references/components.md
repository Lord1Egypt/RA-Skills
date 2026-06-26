# Tailwind Components for Rails

Reusable ERB partials with variants and usage examples.

## Badge Partial

**app/components/_badge.html.erb**

```erb
<% variants = {
  success: { bg: 'bg-green-100', text: 'text-green-800', dark_bg: 'dark:bg-green-900', dark_text: 'dark:text-green-100' },
  warning: { bg: 'bg-yellow-100', text: 'text-yellow-800', dark_bg: 'dark:bg-yellow-900', dark_text: 'dark:text-yellow-100' },
  info: { bg: 'bg-blue-100', text: 'text-blue-800', dark_bg: 'dark:bg-blue-900', dark_text: 'dark:text-blue-100' },
  danger: { bg: 'bg-red-100', text: 'text-red-800', dark_bg: 'dark:bg-red-900', dark_text: 'dark:text-red-100' },
  neutral: { bg: 'bg-gray-100', text: 'text-gray-800', dark_bg: 'dark:bg-gray-900', dark_text: 'dark:text-gray-100' }
} %>

<% style = variants[variant.to_sym] || variants[:neutral] %>

<span class="inline-flex items-center rounded-full <%= style[:bg] %> <%= style[:text] %> <%= style[:dark_bg] %> <%= style[:dark_text] %> px-3 py-1 text-sm font-medium">
  <%= text %>
</span>
```

**Usage:**

```erb
<%= render 'badge', variant: :success, text: 'Active' %>
<%= render 'badge', variant: :warning, text: 'Pending' %>
<%= render 'badge', variant: :danger, text: 'Failed' %>
```

## Button Partial

**app/components/_button.html.erb**

```erb
<% size_classes = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base'
} %>

<% variant_classes = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600',
  secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600',
  danger: 'bg-red-600 text-white hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600'
} %>

<% base_classes = 'inline-flex items-center rounded-md font-medium transition-colors' %>
<% size = size_classes[size.to_sym] || size_classes[:md] %>
<% variant = variant_classes[variant.to_sym] || variant_classes[:primary] %>
<% classes = "#{base_classes} #{size} #{variant}" %>

<% if href %>
  <%= link_to label, href, class: classes %>
<% else %>
  <button type="button" class="<%= classes %>"><%= label %></button>
<% end %>
```

**Usage:**

```erb
<%= render 'button', label: 'Save', variant: :primary, size: :md %>
<%= render 'button', label: 'Delete', variant: :danger, size: :sm, href: delete_path %>
<%= render 'button', label: 'Cancel', variant: :secondary, size: :lg %>
```

## Card Partial

**app/components/_card.html.erb**

```erb
<div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-950">
  <% if title %>
    <div class="border-b border-gray-200 px-6 py-4 dark:border-gray-800">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white"><%= title %></h3>
    </div>
  <% end %>

  <div class="px-6 py-4">
    <%= yield %>
  </div>

  <% if content_for?(:card_footer) %>
    <div class="border-t border-gray-200 bg-gray-50 px-6 py-3 dark:border-gray-800 dark:bg-gray-900">
      <%= content_for :card_footer %>
    </div>
  <% end %>
</div>
```

**Usage:**

```erb
<%= render 'card', title: 'User Settings' do %>
  <p class="text-gray-700 dark:text-gray-300">Your profile information</p>
<% end %>
```

With optional footer:

```erb
<%= render 'card', title: 'Confirm Action' do %>
  <p>Are you sure?</p>
  <% content_for :card_footer do %>
    <%= render 'button', label: 'Confirm', variant: :danger %>
    <%= render 'button', label: 'Cancel', variant: :secondary %>
  <% end %>
<% end %>
```

## Helper Method: Status Badge

**app/helpers/badge_helper.rb**

```ruby
module BadgeHelper
  def status_badge(status)
    variant_map = {
      'active' => :success,
      'pending' => :warning,
      'inactive' => :neutral,
      'error' => :danger,
      'failed' => :danger
    }
    
    variant = variant_map[status.to_s] || :neutral
    render 'badge', variant: variant, text: status.humanize
  end
end
```

**Usage in views:**

```erb
<%= status_badge('active') %>
<%= status_badge('pending') %>
<%= status_badge('failed') %>
```

## Composition Example

Combine partials to build larger components:

```erb
<%= render 'card', title: 'User Accounts' do %>
  <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
    <table class="w-full divide-y divide-gray-200">
      <thead class="bg-gray-50 dark:bg-gray-900">
        <tr>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Name</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Status</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 dark:divide-gray-800">
        <% users.each do |user| %>
          <tr class="hover:bg-gray-50 dark:hover:bg-gray-800">
            <td class="px-6 py-4 text-sm text-gray-900 dark:text-white"><%= user.name %></td>
            <td class="px-6 py-4 text-sm"><%= status_badge(user.status) %></td>
          </tr>
        <% end %>
      </tbody>
    </table>
  </div>
<% end %>
```
