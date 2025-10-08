import httpx
import logging
from typing import Optional, Dict, Any, List
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

# Product Types
FGT_VM_BUNDLE = 1                           # FortiGate Virtual Machine - Service Bundle
FMG_VM = 2                                  # FortiManager Virtual Machine
FWB_VM = 3                                  # FortiWeb Virtual Machine - Service Bundle
FGT_VM_LCS = 4                              # FortiGate Virtual Machine - A La Carte Services
FC_EMS_OP = 5                               # FortiClient EMS On-Prem
FAZ_VM = 7                                  # FortiAnalyzer Virtual Machine
FPC_VM = 8                                  # FortiPortal Virtual Machine
FAD_VM = 9                                  # FortiADC Virtual Machine
FGT_HW = 101                                # FortiGate Hardware
FWBC_PRIVATE = 202                          # FortiWeb Cloud - Private
FWBC_PUBLIC = 203                           # FortiWeb Cloud - Public
FC_EMS_CLOUD = 204                          # FortiClient EMS Cloud

###########################################
# FortiGate VM - Service Bundle           #
###########################################
FGT_VM_BUNDLE_CPU_SIZE = 1                  # 1 - 96 inclusive
FGT_VM_BUNDLE_SVC_PKG = 2                   # "FC" = FortiCare 
                                            # "UTP" = UTP
                                            # "ENT" = Enterprise 
                                            # "ATP" = ATP
                                            # "UTM" = UTM (no longer available)
FGT_VM_BUNDLE_VDOM_NUM = 10                 # 0 - 500 inclusive
FGT_VM_BUNDLE_FORITI_GUARD_SERVICES = 43    # "FGTAVDB" = Advanced Malware Protection
                                            # "FGTFAIS" =  AI-Based In-line Sandbox
                                            # "FGTISSS" = FortiGuard OT Security Service
                                            # "FGTDLDB" = FortiGuard DLP
                                            # "FGTFGSA" = FortiGuard Attack Surface Security Service
                                            # "FGTFCSS" = FortiConverter Service
FGT_VM_BUNDLE_CLOUD_SERVICES = 44           # "FGTFAMS" = FortiGate Cloud Management
                                            # "FGTSWNM" = SD-WAN Underlay
                                            # "FGTSOCA" = SOCaaS
                                            # "FGTFAZC" = FortiAnalyzer Cloud
                                            # "FGTSWOS" = Cloud-based Overlay-as-a-Service
                                            # "FGTFSPA" = SD-WAN Connector for FortiSASE
FGT_VM_BUNDLE_SUPPORT_SERVICE = 45          # "FGTFCELU" = FC Elite Upgrade

###########################################
# FortiManager VM                         #
###########################################
FMG_VM_MANAGED_DEV = 30                     # 1 - 100000 inclusive
FMG_VM_ADOM_NUM = 9                         # 1 - 100000 inclusive

###########################################
# FortiWeb VMe - Service Bundle           #
###########################################
FWB_VM_CPU_SIZE = 4                         # 1, 2, 4, 8, 16
FWB_VM_SVC_PKG = 5                          # "FWBSTD" = Standard
                                            # "FWBADV" = Advanced

###########################################
# FortiGate VM - A La Carte               #
###########################################
FGT_VM_LCS_CPU_SIZE = 6                     # 1 - 96 inclusive
FGT_VM_LCS_FORTIGUARD_SERVICES = 7          # "IPS" = Intrusion Prevention
                                            # "AVDB" = Advanced Malware
                                            # "FURLDNS" = Web, DNS & Video Filtering
                                            # "FGSA" = Security Rating
                                            # "DLDB" = DLP
                                            # "FAIS" = AI-Based InLine Sandbox
                                            # "FURL" = Web & Video Filtering (no longer available)
                                            # "IOTH" = IOT Detection (no longer available)
                                            # "ISSS" = Industrial Security (no longer available)
FGT_VM_LCS_SUPPORT_SERVICE = 8              # "FC247" = FortiCare Premium
                                            # "ASET" = FortiCare Elite
FGT_VM_LCS_VDOM_NUM = 11                    # 1 - 500 inclusive
FGT_VM_LCS_CLOUD_SERVICES = 12              # "FAMS" = FortiGate Cloud
                                            # "SWNM" = SD-WAN Cloud
                                            # "AFAC" = FortiAnalyzer Cloud with SOCaaS
                                            # "FAZC" = FortiAnalyzer Cloud
                                            # "FMGC" = FortiManager Cloud  (no longer available)

###########################################
# FortiClient EMS On-Prem                 #
###########################################
FC_EMS_OP_ZTNA_NUM = 13                     # 0 - 25000 inclusive
FC_EMS_OP_EPP_ZTNA_NUM = 14                 # 0 - 25000 inclusive
FC_EMS_OP_CHROMEBOOK = 15                   # 0 - 25000 inclusive
FC_EMS_OP_SUPPORT_SERVICE = 16              # "FCTFC247" = FortiCare Premium
FC_EMS_OP_ADDOS = 36                        # "BPS" = FortiCare Best Practice

###########################################
# FortiAnalyzer VM                        #
###########################################
FAZ_VM_DAILY_STORAGE = 21                   # 5 - 8300 inclusive
FAZ_VM_ADOM_NUM = 22                        # 0 - 1200 inclusive
FAZ_VM_SUPPORT_SERVICE = 23                 # "FAZFC247" = FortiCare Premium

###########################################
# FortiPortal VM                          #
###########################################
FPC_VM_MANAGED_DEV = 24                     # 0 - 100000 inclusive

###########################################
# FortiADC VM                             #
###########################################
FAD_VM_CPU_SIZE = 25                        # 1, 2, 4, 8, 16, 32
FAD_VM_SERVICE_PACKAGE = 26                 # "FDVSTD" = Standard
                                            # "FDVADV" = Advanced
                                            # "FDVFC247" = FortiCare Premium

###########################################
# FortiGate Hardware                      #
###########################################
FGT_HW_DEVICE_MODEL = 27                    # "FGT40F" = FortiGate 40F
                                            # "FWF40F" = FortiWifi 40F
                                            # "FGT60E" = FortiGate 60E
                                            # "FGT60F" = FortiGate 60F
                                            # "FWF60F" = FortiWifi 60F
                                            # "FGR60F" = FortiGateRugged 60F
                                            # "FGT61F" = FortiGate 61F
                                            # "FGT70F" = FortiGate 70F
                                            # "FR70FB" = FortiGateRugged 70F
                                            # "FGT80F" = FortiGate 80F
                                            # "FGT81F" = FortiGate 81F
                                            # "FG100E" = FortiGate 100E
                                            # "FG100F" = FortiGate 100F
                                            # "FG101E" = FortiGate 101E
                                            # "FG101F" = FortiGate 101F
                                            # "FG200E" = FortiGate 200E
                                            # "FG200F" = FortiGate 200F
                                            # "FG201F" = FortiGate 201F
                                            # "FG4H0F" = FortiGate 400F
                                            # "FG4H1F" = FortiGate 401F
                                            # "FG6H0F" = FortiGate 600F
                                            # "FG1K0F" = FortiGate 1000F
                                            # "FG180F" = FortiGate 1800F
                                            # "F2K60F " = FortiGate 2600F
                                            # "FG3K0F" = FortiGate 3000F
                                            # "FG3K1F" = FortiGate 3001F
                                            # "FG3K2F" = FortiGate 3200F
                                            # "FG40FI" = FortiGate 40F-3G4G
                                            # "FW40FI" = FortiWifi 40F-3G4G
                                            # "FWF61F" = FortiWifi 61F
                                            # "FR60FI" = FortiGateRugged 60F 3G4G
                                            # "FGT71F" = FortiGate 71F
                                            # "FG80FP" = FortiGate 80F-PoE
                                            # "FG80FB" = FortiGate 80F-Bypass
                                            # "FG80FD" = FortiGate 80F DSL
                                            # "FWF80F" = FortiWiFi 80F-2R
                                            # "FW80FS" = FortiWiFi 80F-2R-3G4G-DSL
                                            # "FWF81F" = FortiWiFi 81F 2R
                                            # "FW81FS" = FortiWiFi 81F-2R-3G4G-DSL
                                            # "FW81FD" = FortiWiFi 81F-2R-3G4G-PoE
                                            # "FW81FP" = FortiWiFi 81F 2R POE
                                            # "FG81FP" = FortiGate 81F-PoE
                                            # "FGT90G" = FortiGate 90G
                                            # "FGT91G" = FortiGate 91G
                                            # "FG201E" = FortiGate 201E
                                            # "FG4H0E" = FortiGate 400E
                                            # "FG4HBE" = FortiGate 400E BYPASS
                                            # "FG4H1E" = FortiGate 401E
                                            # "FD4H1E" = FortiGate 401E DC
                                            # "FG6H0E" = FortiGate 600E
                                            # "FG6H1E" = FortiGate 601E
                                            # "FG6H1F" = FortiGate 601F
                                            # "FG9H0G" = FortiGate 900G
                                            # "FG9H1G" = FortiGate 901G
                                            # "FG1K1F" = FortiGate 1001F
                                            # "FG181F" = FortiGate 1801F
                                            # "FG3K7F" = FortiGate 3700F
                                            # "FG39E6" = FortiGate 3960E
                                            # "FG441F" = FortiGate 4401F
FGT_HW_SERVICE_PACKAGE = 28                 # "FGHWFC247" = FortiCare Premium
                                            # "FGHWFCEL" = FortiCare Elite
                                            # "FGHWATP" = ATP
                                            # "FGHWUTP" = UTP
                                            # "FGHWENT" = Enterprise
FGT_HW_ADDONS = 29                          # "FGHWFCELU" = FortiCare Elite Upgrade
                                            # "FGHWFAMS" = FortiGate Cloud Management
                                            # "FGHWFAIS" = AI-Based In-line Sandbox
                                            # "FGHWSWNM" = SD-WAN Underlay
                                            # "FGHWDLDB" = FortiGuard DLP
                                            # "FGHWFAZC" = FortiAnalyzer Cloud
                                            # "FGHWSOCA" = SOCaaS
                                            # "FGHWMGAS" = Managed FortiGate
                                            # "FGHWSPAL" = SD-WAN Connector for FortiSASE
                                            # "FGHWFCSS" = FortiConverter Service

###########################################
# FortiWeb Cloud - Private                #
###########################################
FWBC_PRIVATE_AVERAGE_THROUGHPUT = 32        # All Mbps - 10, 25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000
FWBC_PRIVATE_WEB_APPLICATIONS = 33          # 0 - 2000 inclusive

###########################################
# FortiWeb Cloud - Public                 #
###########################################
FWBC_PUBLIC_AVERAGE_THROUGHPUT = 34        # All Mbps - 10, 25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000
FWBC_PUBLIC_WEB_APPLICATIONS = 35          # 0 - 2000 inclusive

FC_EMS_CLOUD_ZTNA_NUM = 37                 # Value should be divisible by 25. 0 - 25000 inclusive
FC_EMS_CLOUD_ZTNA_FGF_NUM = 38             # Value should be divisible by 25. 0 - 25000 inclusive
FC_EMS_CLOUD_EPP_ZTNA_NUM = 39             # Value should be divisible by 25. 0 - 25000 inclusive
FC_EMS_CLOUD_EPP_ZTNA_FGF_NUM = 40         # Value should be divisible by 25. 0 - 25000 inclusive
FC_EMS_CLOUD_CHROMEBOOK = 41               # Value should be divisible by 25. 0 - 25000 inclusive
FC_EMS_CLOUD_ADDONS = 42                   # "BPS" = FortiCare Best Practice


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

@mcp.tool(description='List all FortiFlex configurations for a given program serial ')
async def config_list(access_token, program_sn
) -> Dict[str, Any]:
    """
    Perform POST request for the FortiFlex API to list all configuration is available

    Args:
        access_token: Bearer token for authentication
        program_serial_number: Program serial number
    Returns:
        Dictionary containing the configurations.    
    """
    logging.debug("--> Listing all Fortiflex configurations ...")

    uri = FORTIFLEX_API_BASE_URI + "configs/list"
    headers = COMMON_HEADERS.copy()

    body = {
        "programSerialNumber": program_sn,
    }
    if access_token == "":
        token_response = await generate_token()
        access_token = token_response.get("access_token")
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await _make_request(client, uri, body, headers)

@mcp.tool(description='Update FortiFlex configuration with custom parameters.')
async def update_config(access_token, config_id, name, parameters: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Perform POST request to update a FortiFlex configuration with any parameters.

    access_token: Bearer token for authentication
        config_id: Configuration ID to be updated
        name: Name of the configuration
        parameters: List of parameter objects with 'id' and 'value' keys
                   Example: [{"id": 6, "value": "4"}, {"id": 8, "value": "ASET"}]

    Returns:
        Dictionary containing the API response.    
    """
    logging.debug("--> Updating the configurations ...")

    uri = FORTIFLEX_API_BASE_URI + "configs/update"
    headers = COMMON_HEADERS.copy()

    body = {
        "id": config_id,
        "name": name,
        "parameters": parameters,
    }

    if access_token == "":
        token_response = await generate_token()
        access_token = token_response.get("access_token")
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
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

