#!/bin/sh

check_github() {
  skill_dir=$1
  config_path=$2

  if ! check_common_platform_requirement "github" "$skill_dir"; then
    return 1
  fi

  repo_name=$(config_get "$config_path" github repo "")
  repo_path=$(config_get "$config_path" github target_repo_path "")
  create_release=$(config_get "$config_path" github create_release "false")

  if [ -n "$repo_path" ] && [ ! -d "$repo_path/.git" ]; then
    record_result "github" "$skill_dir" "failed" "target_repo_path is not a git repository"
    return 1
  fi

  if [ "$create_release" = "true" ] && [ -z "$repo_name" ]; then
    record_result "github" "$skill_dir" "failed" "github.repo is required when create_release=true"
    return 1
  fi

  record_result "github" "$skill_dir" "validated" "GitHub publish configuration looks valid"
  return 0
}

status_github() {
  skill_dir=$1
  config_path=$2
  local_version=$3
  repo_name=$(config_get "$config_path" github repo "")

  if [ -z "$repo_name" ] || ! command_exists gh; then
    record_result "github" "$skill_dir" "status-unknown" "GitHub repo not configured or gh unavailable" "" "$(skill_slug "$skill_dir")" "" ""
    printf '[github] %s remote=unknown\n' "$skill_dir"
    return 0
  fi

  tag="skillup-v$local_version"
  if gh release view "$tag" --repo "$repo_name" >/dev/null 2>&1; then
    record_result "github" "$skill_dir" "in-sync" "release $tag exists" "https://github.com/$repo_name/releases/tag/$tag" "$(skill_slug "$skill_dir")" "$local_version" ""
    printf '[github] %s remote=%s status=in-sync\n' "$skill_dir" "$local_version"
  else
    record_result "github" "$skill_dir" "out-of-sync" "release $tag not found" "" "$(skill_slug "$skill_dir")" "$local_version" ""
    printf '[github] %s remote=missing status=out-of-sync\n' "$skill_dir"
  fi
  return 0
}

publish_github() {
  skill_dir=$1
  artifact_path=$2
  config_path=$3
  dry_run=$4

  token=$(env_or_config "SKILLUP_GITHUB_TOKEN" "$config_path" github token "")
  repo_path=$(config_get "$config_path" github target_repo_path "")
  repo_name=$(config_get "$config_path" github repo "")
  target_subdir=$(config_get "$config_path" github target_subdir "published-skills")
  branch=$(config_get "$config_path" github branch "main")
  commit_message=$(config_get "$config_path" github commit_message "chore: sync skills via SkillUp")
  visibility=$(config_get "$config_path" github visibility "public")
  auto_create_repo=$(config_get "$config_path" github auto_create_repo "true")
  create_release=$(config_get "$config_path" github create_release "false")
  release_latest=$(config_get "$config_path" github release_latest "true")
  release_title_template=$(config_get "$config_path" github release_title_template "{slug} v{version}")
  release_notes_template=$(config_get "$config_path" github release_notes_template "Automated release for {slug} version {version}.")
  slug=$(skill_slug "$skill_dir")
  version=$(skill_version "$skill_dir")
  tag="${slug}-v${version}"
  release_title=$(template_render "$release_title_template" "$slug" "$version")
  release_notes=$(template_render "$release_notes_template" "$slug" "$version")

  if [ "$dry_run" -eq 1 ]; then
    if [ "$create_release" = "true" ] && [ -n "$repo_name" ]; then
      record_result "github" "$skill_dir" "dry-run" "would sync $artifact_path and create release $tag in $repo_name"
    else
      record_result "github" "$skill_dir" "dry-run" "would sync $artifact_path to $repo_path/$target_subdir on $branch"
    fi
    return
  fi

  if [ -n "$token" ]; then
    GH_TOKEN=$token
    export GH_TOKEN
  fi

  if [ -n "$repo_name" ] && command_exists gh; then
    if ! gh repo view "$repo_name" >/dev/null 2>&1; then
      if [ "$auto_create_repo" = "true" ]; then
        if ! gh repo create "$repo_name" "--$visibility" >/tmp/skillup-gh-repo-create.log 2>&1; then
          record_result "github" "$skill_dir" "failed" "gh repo create failed"
          return 1
        fi
      else
        record_result "github" "$skill_dir" "failed" "target GitHub repository does not exist"
        return 1
      fi
    fi
  fi

  if [ -n "$repo_path" ] && [ -d "$repo_path/.git" ]; then
    mkdir -p "$repo_path/$target_subdir"
    cp "$artifact_path" "$repo_path/$target_subdir/$slug.zip"

    (
      cd "$repo_path"
      git add "$target_subdir/$slug.zip"
      if git diff --cached --quiet; then
        exit 10
      fi
      git commit -m "$commit_message" >/dev/null 2>&1 || exit 11
      git push origin "$branch" >/dev/null 2>&1 || exit 12
    )
    status=$?

    case "$status" in
      0)
        record_result "github" "$skill_dir" "published" "artifact pushed to $repo_path/$target_subdir/$slug.zip" "" "$slug" "$version" ""
        ;;
      10)
        record_result "github" "$skill_dir" "skipped" "no repository changes"
        ;;
      11)
        record_result "github" "$skill_dir" "failed" "git commit failed"
        return 1
        ;;
      12)
        record_result "github" "$skill_dir" "failed" "git push failed"
        return 1
        ;;
      *)
        record_result "github" "$skill_dir" "failed" "unknown git publishing error"
        return 1
        ;;
    esac
  elif [ "$create_release" != "true" ] || [ -z "$repo_name" ]; then
    record_result "github" "$skill_dir" "skipped" "target_repo_path missing or not a git repository"
  fi

  if [ "$create_release" = "true" ] && [ -n "$repo_name" ]; then
    release_args=""
    if [ "$release_latest" = "true" ]; then
      release_args="--latest"
    fi

    if command -v gh >/dev/null 2>&1; then
      if gh release view "$tag" --repo "$repo_name" >/dev/null 2>&1; then
        if gh release upload "$tag" "$artifact_path" --repo "$repo_name" --clobber >/tmp/skillup-gh-release.log 2>&1; then
          record_result "github-release" "$skill_dir" "published" "updated release $tag in $repo_name" "https://github.com/$repo_name/releases/tag/$tag" "$tag" "$version" ""
        else
          record_result "github-release" "$skill_dir" "failed" "gh release upload failed"
          return 1
        fi
      else
        if gh release create "$tag" "$artifact_path" --repo "$repo_name" --title "$release_title" --notes "$release_notes" $release_args >/tmp/skillup-gh-release.log 2>&1; then
          record_result "github-release" "$skill_dir" "published" "created release $tag in $repo_name" "https://github.com/$repo_name/releases/tag/$tag" "$tag" "$version" ""
        else
          record_result "github-release" "$skill_dir" "failed" "gh release create failed"
          return 1
        fi
      fi
    else
      record_result "github-release" "$skill_dir" "skipped" "gh CLI not installed"
    fi
  fi

  return 0
}
