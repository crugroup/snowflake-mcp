    from mcp_server_snowflake import extras
    from typing import Dict
    from starlette.requests import Request
    from starlette.responses import Response

    extras.write_tool_config_if_provided(args, logger, get_var)
    
    server = FastMCP("Snowflake MCP Server", lifespan=create_lifespan(args), auth=extras.auth)
    
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> Dict:
        return Response(content="OK", status_code=200)
