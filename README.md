# Refactoring Tracker

Initially used to find call references to SQL stored procedures in our c# code base, and to create linear issues for them. Can be easily adapted to search any other regex pattern.

# Setup

Requires [ripgrep](https://github.com/BurntSushi/ripgrep)

Create .env inside `linear-upload` with:

```shell
LINEAR_API_KEY=lin_api_...
TEAM_ID=...
```

# Usage

1. Scan the code, which create two .json files

```
python main.py </path/to/codebase>
```

2. Upload to linear (this requires bun)

```shell
cd linear-upload
bun uploadToLinear.ts
```
