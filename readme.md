# Wayback Web4

Make Wayback Machine snapshots unstoppable by deploying them to NEAR Protocol using web4.

## Overview

This tool allows you to:
1. Download a webpage from the Wayback Machine
2. Transform it into a clean, reader-friendly format
3. Deploy it to NEAR Protocol as an unstoppable webpage using web4

## Prerequisites

- Python 3.7+
- Rust and Cargo
- NEAR CLI
- A NEAR account with deployed keys

### Installing Dependencies

1. Install Python dependencies:
```bash
pip install requests beautifulsoup4 readability-lxml
```

2. Install Rust:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

3. Add the WebAssembly target:
```bash
rustup target add wasm32-unknown-unknown
```

4. Install NEAR CLI:
```bash
npm install -g near-cli
```

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd wayback_web4
```

2. Make sure you have a NEAR account and have logged in with NEAR CLI:
```bash
near login
```

## Usage

1. Find a Wayback Machine snapshot URL you want to preserve. It should look like:
```
https://web.archive.org/web/20230615000000/https://example.com
```

2. Deploy the snapshot to your NEAR account:
```bash
python wayback.py "WAYBACK_URL" --wallet your-account.near
```

For example:
```bash
python wayback.py "https://web.archive.org/web/20230615000000/https://example.com" --wallet example.near
```

3. Your site will be available at:
```
https://example.near.page
```

## Updating Content

To update an existing deployment with a new snapshot:
```bash
python wayback.py "NEW_WAYBACK_URL" --wallet your-account.near --update
```

## Features

- Clean, reader-friendly format
- Preserves original content and structure
- Mobile-responsive design
- Sticky navigation banner
- Original Wayback Machine link preserved
- All assets stored on-chain
- Unstoppable hosting via NEAR Protocol

## Project Structure

```
wayback_web4/
├── wayback.py              # Main script
├── web4_contract/         
│   ├── Cargo.toml         # Rust contract config
│   ├── src/
│   │   └── lib.rs         # Contract code
│   └── res/               # Generated content directory
└── README.md              # This file
```

## How It Works

1. The script downloads the Wayback Machine snapshot
2. Cleans and transforms the content into a reader-friendly format
3. Stores the content in the `res` directory
4. Builds and deploys a web4 contract to NEAR Protocol
5. Makes the content available through NEAR's web4 gateway

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **NEAR CLI Not Found**
   ```bash
   npm install -g near-cli
   ```

3. **Rust Build Fails**
   ```bash
   rustup update
   rustup target add wasm32-unknown-unknown
   ```

4. **Permission Denied**
   Make sure you're logged in with NEAR CLI:
   ```bash
   near login
   ```

### Getting Help

If you encounter issues:
1. Check that all prerequisites are installed
2. Ensure you're logged in to NEAR CLI
3. Verify the Wayback Machine URL is valid
4. Check the contract deployment logs

## License

MIT License - feel free to use and modify as needed.
