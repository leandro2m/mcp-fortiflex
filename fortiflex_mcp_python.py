import httpx
import logging
from typing import Optional, Dict, Any
from mcp.server import FastMCP
import os
import json

from dotenv import load_dotenv
load_dotenv()

program_sn = os.getenv('FORTIFLEX_PROGRAM_SN')

api_user = os.getenv('FORTIFLEX_API_USER')
api_password = os.getenv('FORTIFLEX_API_PASSWORD')
account_id = os.getenv('FORTIFLEX_ACCOUNT_ID')

mcp = FastMCP("mcp-fortiflex")

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}
FORTIFLEX_API_BASE_URI = "https://support.fortinet.com/ES/api/fortiflex/v2/"
FORTICARE_AUTH_URI = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"
timeout: float = 30.0


token = ""
@mcp.tool(description='Get a Fortiflex toekn.')
async def generate_token(api_user=api_user, api_password=api_password
) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex account to generate a token.

    Args:
        api_user: API username
        api_password: API Password

    Returns:
        Dictionary containing tokens.    
    """
    logging.debug("--> Token...")

    uri = FORTICARE_AUTH_URI
    headers = COMMON_HEADERS.copy()

    body = {
        'username': api_user,  
        'password': api_password,
        'client_id': 'flexvm',
        'grant_type': 'password'
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await _make_request(client, uri, body, headers=headers)
        logging.debug(f"Response: {response}")
        return response
    return await _make_request(client, uri, body, headers)

@mcp.tool(description='Get all existing entitlements on FortiFlex for a given account ID or program serial number.')
async def entitlements_list(access_token, program_sn=program_sn, account_id=account_id) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex Entitlements List API.
    The body must include the following parameters:
    - account_id: (int) Account ID to filter entitlements
    - programSerialNumber: (string) Program Serial Number to filter entitlements
    Args:
        access_token: Bearer token for authentication
        program_sn: Program Serial Number to filter entitlements
        account_id: Account ID to filter entitlements
    Returns:
        Dictionary containing all existing entitlements.    
    """
    logging.debug("--> List FortiFlex Entitlements...")
    body = {
        "accountId": account_id,
        "programSerialNumber": program_sn,
    }
    uri = FORTIFLEX_API_BASE_URI + "entitlements/list"
    headers = COMMON_HEADERS.copy()

    if access_token == "":
        token_response = await generate_token()
        access_token = token_response.get("access_token")
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = f"Bearer {access_token}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await _make_request(client, uri, body, headers=headers)

@mcp.tool(description='Regenerate the VM token license token from FortiFlex for a given serial number.')
async def entitlements_vm_token(access_token, serial_number
) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex API to regenerate and retrieve a VM license Token.

    Args:
        access_token: Bearer token for authentication
        serial_number: Serial number of the VM to filter entitlements
    Returns:
        Dictionary containing the VM license token.    
    """
    logging.debug("--> FortiFlex VM License Token ...")

    uri = FORTIFLEX_API_BASE_URI + "entitlements/vm/token"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "serialNumber": serial_number,
    }
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await _make_request(client, uri, body, headers)
    return await _make_request(client, uri, body, headers)

@mcp.tool(description='Reactivate the VM token license token from FortiFlex for a given serial number.')
async def entitlements_reactivate(access_token, serial_number
) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex API to reactivate VM license Token for a given serial number.

    Args:
        access_token: Bearer token for authentication
        serial_number: Serial number of the VM to filter entitlements
    Returns:
        Dictionary containing the VM license token.    
    """
    logging.debug("--> Reactivate the FortiFlex VM License ...")

    uri = FORTIFLEX_API_BASE_URI + "entitlements/reactivate"
    headers = COMMON_HEADERS.copy()
    body = {
        "serialNumber": serial_number,
    }
    if access_token == "":
        token_response = await generate_token()
        access_token = token_response.get("access_token")
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await _make_request(client, uri, body, headers)
    return await _make_request(client, uri, body, headers)

@mcp.tool(description='Stop the VM token license token from FortiFlex for a given serial number.')
async def entitlements_stop(access_token, serial_number
) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex API to stop VM license Token for a given serial number.

    Args:
        access_token: Bearer token for authentication
        serial_number: Serial number of the VM to filter entitlements
    Returns:
        Dictionary containing the VM license token.    
    """
    logging.debug("--> Stopping the FortiFlex VM License ...")

    uri = FORTIFLEX_API_BASE_URI + "entitlements/stop"
    headers = COMMON_HEADERS.copy()

    body = {
        "serialNumber": serial_number,
    }
    if access_token == "":
        token_response = await generate_token()
        access_token = token_response.get("access_token")
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await _make_request(client, uri, body, headers)
    return await _make_request(client, uri, body, headers)



async def _make_request(
    client: httpx.AsyncClient, 
    uri: str, 
    body: Dict[str, Any], 
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """Helper function to make the actual HTTP request"""
    try:
        response = await client.post(uri, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise


def main():
    import asyncio
    import os
    asyncio.run(mcp.run_stdio_async())

if __name__ == "__main__":
    main()

