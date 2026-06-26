# xCloud Native Node.js Deployment

## Repository Setup (Required)

package.json must have a `start` script:
```json
{
  "scripts": {
    "start": "node server.js",
    "build": "tsc -p tsconfig.json"
  }
}
```

Port must use process.env.PORT:
```javascript
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));
```

xCloud injects PORT automatically. Your app MUST listen on this port.

.env.example:
```env
NODE_ENV=production
PORT=3000
DATABASE_URL=
JWT_SECRET=
```

## xCloud UI Steps

1. Server → New Site → Node.js tab
2. Connect Git repo
3. Set branch
4. Node.js version: 18, 20, or 22
5. Start command: `npm start` (or `node server.js`)
6. Build command (if TypeScript): `npm run build`
7. Add environment variables
8. Click Deploy

## Common Issues

| Issue | Fix |
|---|---|
| App crashes on start | Check PORT env var is used (not hardcoded) |
| Module not found | Ensure node_modules is in .gitignore |
| TypeScript errors | Add build script, set build command in xCloud |
