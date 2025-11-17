import base64
import os
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

# Set up authentication.
auth = None

if "MCP_AUTH_TOKEN" in os.environ:
    MCP_AUTH_TOKEN = os.environ["MCP_AUTH_TOKEN"]

    auth = StaticTokenVerifier(
        tokens={
            f"{MCP_AUTH_TOKEN}": {
                "client_id": f"{MCP_AUTH_TOKEN}",
            }
        }
    )

def write_tool_config_if_provided(args, logger, get_var):
    if "TOOL_CONFIG" in os.environ:
        service_config = base64.b64decode(os.environ["TOOL_CONFIG"]).decode("utf-8")
        logger.info(f"{service_config}")
        service_config_file = get_var(
            "service_config_file", "SERVICE_CONFIG_FILE", args
        )
        with open(service_config_file, "w") as f:
            f.write(service_config)
