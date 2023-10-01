#!/usr/bin/env bash

# Show env vars
grep -v '^#' snowflake.env

# Export env vars
export $(grep -v '^#' snowflake.env | xargs)

