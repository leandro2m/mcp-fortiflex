# FortiFlex MCP Server

A Model Context Protocol (MCP) server that provides integration with Fortinet's FortiFlex licensing platform, enabling automated license management and token operations through conversational AI interfaces.

## Overview

This MCP server allows you to interact with FortiFlex APIs to manage entitlements. It supports token generation, entitlement listing, license activation, and lifecycle management operations.

## Prerequisites

- FortiFlex account with API credentials. You can find more information on how to generate an API key at this link https://docs.fortinet.com/document/forticloud/25.3.a/identity-access-management-iam/927656/api-users
- Account ID and Program Serial Number
- MCP-compatible Claude Desktop
- UV package manager https://docs.astral.sh/uv/getting-started/installation/

## Installation

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/leandro2m/fortiflex-mcp-server.git
cd fortiflex-mcp-server

# Install dependencies
uv sync

# Activate the environment
source ./.venv/bin/activate

# Run the server
uv run fortiflex_mcp_python.py
```


## MCP Client Configuration for Claude Desktop

### Option 1: Run the python code

Add the server to your MCP client configuration file:

{
  "mcp-fortiflex": {
    "command": "uv",
    "args": [
      "--directory",
      "your_python_code_directory",
      "run",
      "fortiflex_mcp_python.py"
    ],
    "env": {
      "FORTIFLEX_API_USER": "API_USER",
      "FORTIFLEX_API_PASSWORD": "API_PASSWORD",
      "FORTIFLEX_PROGRAM_SN": "PROGRAM_SERIAL_NUMBER",
      "FORTIFLEX_ACCOUNT_ID": "ACCOUNT_ID"
    }
  }
}

### Option 2: Run a docker container

#### Choose the correct image for your OS:
	•	Windows Desktop: use leandro2m/mcp-fortiflex:x86
	•	Mac (or Linux): use leandro2m/mcp-fortiflex
"mcpServers": {
  "fortiflex-mcp-server": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "--env", "FORTIFLEX_API_USER=API_USERNAME_HERE",
      "--env", "FORTIFLEX_API_PASSWORD=PASSWORD_HERE",
      "--env", "FORTIFLEX_PROGRAM_SN=PROGRAM_SERIAL_NUMBER_HERE",
      "--env", "FORTIFLEX_ACCOUNT_ID=1308909",
      "leandro2m/mcp-fortiflex:x86"   // Replace with correct image for your OS
    ]
  }
}

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FORTIFLEX_API_USER` | FortiFlex API User ID | Yes |
| `FORTIFLEX_API_PASSWORD` | FortiFlex API Password | Yes |
| `FORTIFLEX_ACCOUNT_ID` | FortiFlex Account ID | Yes |
| `FORTIFLEX_PROGRAM_SN` | Program Serial Number | No |

## Available Tools

### 1. generate_token
Generates an authentication token for FortiFlex API access.

**Parameters:**
- `api_user` (string, optional): API User ID (default from env)
- `api_password` (string, optional): API Password (default from env)

**Example:**
```javascript
{
  "access_token": "lppDvKAMJrwArFT74aAQHy4ZwDPECJ",
  "expires_in": 3660,
  "token_type": "Bearer",
  "status": "success"
}
```

### 2. entitlements_list
Retrieves all entitlements for a given account or program.

**Parameters:**
- `access_token` (string, required): Valid access token
- `account_id` (string, optional): Account ID (default from env)
- `program_sn` (string, optional): Program Serial Number

**Example:**
```javascript
{
  "entitlements": [
    {
      "serialNumber": "FGVMMLTM23018252",
      "description": "Demo 01 AWS - Anthony",
      "status": "ACTIVE",
      "token": "BE5CA53C8245BB46784B",
      "configId": 1921,
      "startDate": "2023-12-19T06:52:10.267",
      "endDate": "2026-09-09T00:00:00"
    }
  ]
}
```

### 3. entitlements_vm_token
Regenerates the VM license token for a specific serial number.

**Parameters:**
- `access_token` (string, required): Valid access token
- `serial_number` (string, required): VM serial number

### 4. entitlements_reactivate
Reactivates a stopped entitlement.

**Parameters:**
- `access_token` (string, required): Valid access token
- `serial_number` (string, required): VM serial number

### 5. entitlements_stop
Stops an active entitlement.

**Parameters:**
- `access_token` (string, required): Valid access token
- `serial_number` (string, required): VM serial number

## Usage Examples

### Example 1: List All Entitlements

```
User: List all my FortiFlex entitlements

AI: [Automatically calls generate_token, then entitlements_list]
You have 70 entitlements across 13 configurations...
```

### Example 2: Get Token for Specific Serial Number

```
User: What is the token for serial number FGVMMLTM23018252?

AI: [Searches through entitlements]
Token: BE5CA53C8245BB46784B
Status: ACTIVE
Description: Demo 01 AWS
```

### Example 3: Regenerate License Token

```
User: Regenerate the token for FGVMMLTM24003308

AI: [Calls entitlements_vm_token]
Successfully regenerated token for FGVMMLTM24003308
New token: [new-token-value]
```

## API Authentication

The server uses FortiFlex API credentials to authenticate:

1. API User ID and Password generate an access token
2. Access token is used for all subsequent API calls
3. Tokens expire after ~1 hour (3660 seconds)
4. The server automatically handles token generation


