# Migration Guide

## Initialize a new workspace
1. Create durable memory file
2. Create daily memory directory
3. Create `.learnings/`
4. Create learnings index
5. Enable health checks and weekly review cron

## Migrate old notes
- stable rules -> durable memory
- current state -> daily memory
- reusable lessons -> `.learnings/`
- noisy logs -> do not migrate directly
