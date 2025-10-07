# FortiFlex MCP Server

A Model Context Protocol (MCP) server that provides integration with Fortinet's FortiFlex licensing platform, enabling automated license management and token operations through conversational AI interfaces.

## Overview

This MCP server allows you to interact with FortiFlex APIs to manage entitlements. It supports token generation, entitlement listing, license activation, and lifecycle management operations.

## Prerequisites

- FortiFlex account with API credentials. You can find more information on how to generate an API key at this link https://docs.fortinet.com/document/forticloud/25.3.a/identity-access-management-iam/927656/api-users
- Account ID and Program Serial Number
- MCP-compatible Claude Desktop

## Installation

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/your-username/fortiflex-mcp-server.git
cd fortiflex-mcp-server

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

### Option 2: Docker Installation

```bash
# Build the image
docker build -t fortiflex-mcp-server .

# Run the container
docker run -d -p 8080:8080 fortiflex-mcp-server
```

### Option 3: Multi-Platform Docker Build

```bash
# Setup buildx
docker buildx create --name multibuilder --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-dockerhub-username/fortiflex-mcp-server:latest \
  --push \
  .
```

## Configuration

### MCP Client Configuration

Add the server to your MCP client configuration file:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "fortiflex": {
      "command": "python",
      "args": ["/path/to/fortiflex-mcp-server/server.py"],
      "env": {
        "FORTIFLEX_API_USER": "your-api-user-id",
        "FORTIFLEX_API_PASSWORD": "your-api-password",
        "FORTIFLEX_ACCOUNT_ID": "your-account-id"
      }
    }
  }
}
```

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
Description: Demo 01 AWS - Anthony
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

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid credentials | Check API user ID and password |
| Token expired | Token older than 1 hour | Regenerate token |
| Serial number not found | Invalid SN | Verify serial number exists |
| Entitlement already stopped | Attempting to stop inactive | Check entitlement status first |

## Development

### Project Structure

```
fortiflex-mcp-server/
├── server.py              # Main MCP server
├── fortiflex_api.py       # FortiFlex API client
├── tools/                 # Tool implementations
│   ├── generate_token.py
│   ├── entitlements.py
│   └── lifecycle.py
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-service setup
└── README.md             # This file
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=fortiflex_mcp tests/
```

### Building Documentation

```bash
# Generate API docs
python -m pydoc -w fortiflex_api

# Build Sphinx docs
cd docs
make html
```

## Docker Deployment

### Using Docker Compose

```yaml
version: '3.8'

services:
  fortiflex-mcp:
    build:
      context: .
      platforms:
        - linux/amd64
        - linux/arm64
    image: fortiflex-mcp-server:latest
    environment:
      - FORTIFLEX_API_USER=${FORTIFLEX_API_USER}
      - FORTIFLEX_API_PASSWORD=${FORTIFLEX_API_PASSWORD}
      - FORTIFLEX_ACCOUNT_ID=${FORTIFLEX_ACCOUNT_ID}
    ports:
      - "8080:8080"
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Security Considerations

- **Never commit API credentials** to version control
- Use environment variables or secrets management
- Rotate API credentials regularly
- Implement rate limiting for production use
- Use HTTPS for all API communications
- Store tokens securely with appropriate encryption

## Troubleshooting

### Token Generation Issues

```bash
# Test API connectivity
curl -X POST https://support.fortinet.com/ES/api/fortiflex/v2/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"YOUR_USER","password":"YOUR_PASSWORD"}'
```

### Entitlement Not Found

- Verify account ID is correct
- Check if serial number exists in your account
- Ensure you have proper permissions

### Connection Errors

- Check firewall rules
- Verify internet connectivity
- Confirm FortiFlex API endpoint is accessible

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [FortiFlex API Docs](https://docs.fortinet.com/fortiflex)
- **Issues**: [GitHub Issues](https://github.com/your-username/fortiflex-mcp-server/issues)
- **Community**: [Fortinet Community](https://community.fortinet.com/)

## Changelog

### Version 1.0.0 (2025-01-XX)
- Initial release
- Token generation support
- Entitlement listing and management
- VM token operations
- Multi-platform Docker support

## Acknowledgments

- Fortinet for the FortiFlex API
- Anthropic for the Model Context Protocol
- Contributors and community members

## Related Projects

- [MCP Specification](https://github.com/anthropics/mcp)
- [FortiFlex Documentation](https://docs.fortinet.com/fortiflex)
- [FortiGate Automation](https://github.com/fortinet/fortinet-automation)

---

**Note**: This is an unofficial project and is not affiliated with or endorsed by Fortinet.
