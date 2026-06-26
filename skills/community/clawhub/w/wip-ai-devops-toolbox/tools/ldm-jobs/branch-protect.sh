#!/bin/bash
# Job: audit and enforce branch protection across all org repos
# Runs daily. Adds protection to any repo missing it.

echo "=== Branch protection audit: $(date) ==="

ORG="wipcomputer"
FIXED=0
SKIPPED=0
ALREADY=0

repos=$(gh repo list "$ORG" --limit 200 --json name,isArchived -q '.[] | select(.isArchived == false) | .name')

for repo in $repos; do
  result=$(gh api "repos/$ORG/$repo/branches/main/protection" 2>&1)

  if echo "$result" | grep -q "enforce_admins"; then
    ALREADY=$((ALREADY + 1))
  elif echo "$result" | grep -q "Branch not protected"; then
    echo "FIXING: $repo"
    gh api "repos/$ORG/$repo/branches/main/protection" -X PUT \
      -F "required_pull_request_reviews[required_approving_review_count]=0" \
      -F "enforce_admins=true" \
      -F "restrictions=null" \
      -F "required_status_checks=null" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      echo "  Protected: $repo"
      FIXED=$((FIXED + 1))
    else
      echo "  FAILED: $repo"
    fi
  else
    SKIPPED=$((SKIPPED + 1))
  fi
done

echo ""
echo "Results: $ALREADY already protected, $FIXED fixed, $SKIPPED skipped (no main branch or error)"
echo "=== Branch protection audit complete: $(date) ==="
