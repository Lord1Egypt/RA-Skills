#!/bin/bash

# Simple trend search helper

QUERY=${1:-AI}

open "https://x.com/search?q=${QUERY}&src=typed_query&f=live"
