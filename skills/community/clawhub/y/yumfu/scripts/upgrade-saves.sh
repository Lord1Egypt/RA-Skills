#!/bin/bash
# YumFu Save File Upgrader - Adds v2.1 compatibility fields

echo "🔧 Upgrading YumFu save files for v2 world configs..."

# Xiaoao saves - add new fields if missing
for save in ~/clawd/memory/yumfu/saves/xiaoao/*.json; do
  if [ -f "$save" ]; then
    echo "📝 Processing: $(basename $save)"
    # Backup
    cp "$save" "$save.bak"
    
    # Add charm attribute if missing (using jq)
    if command -v jq &> /dev/null; then
      jq '.character.attributes.charm //= 50 | 
          .character.equipped //= {"weapon": (.inventory[] | select(.type=="weapon") | .name), "armor": (.inventory[] | select(.type=="armor") | .name)} |
          .warrior_code_adherence //= 80 |
          .gameplay_chapter //= 1' "$save" > "$save.tmp" && mv "$save.tmp" "$save"
      echo "  ✅ Added v2.1 fields"
    else
      echo "  ⚠️  jq not found, skipping automatic upgrade"
    fi
  fi
done

echo "✅ Xiaoao江湖 saves upgraded"

# Harry Potter saves (if any exist)
if [ -d ~/clawd/memory/yumfu/saves/harry-potter ]; then
  for save in ~/clawd/memory/yumfu/saves/harry-potter/*.json; do
    if [ -f "$save" ]; then
      echo "📝 Processing HP: $(basename $save)"
      cp "$save" "$save.bak"
      # Add new HP v2 fields
      if command -v jq &> /dev/null; then
        jq '.character.school_year //= 1 |
            .character.house //= "gryffindor" |
            .character.attributes.courage //= 50 |
            .character.attributes.loyalty //= 50 |
            .exam_scores //= {} |
            .friendships //= {} |
            .quidditch_position //= null' "$save" > "$save.tmp" && mv "$save.tmp" "$save"
        echo "  ✅ Added HP v2.1 fields"
      fi
    fi
  done
  echo "✅ Harry Potter saves upgraded"
fi

echo ""
echo "🎮 All save files upgraded successfully!"
echo "📦 Backups created with .bak extension"
