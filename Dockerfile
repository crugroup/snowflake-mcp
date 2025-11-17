FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ build-essential libffi-dev

RUN pip install snowflake-labs-mcp==1.3.5

ADD extras.py /usr/local/lib/python3.14/site-packages/mcp_server_snowflake/extras.py
ADD server_patch.py /tmp/server_patch.py

RUN mkdir -p /app

RUN sed -i \
    -e '/    server = FastMCP("Snowflake MCP Server", lifespan=create_lifespan(args))/r /tmp/server_patch.py' \
    -e '/    server = FastMCP("Snowflake MCP Server", lifespan=create_lifespan(args))/d' \
    /usr/local/lib/python3.14/site-packages/mcp_server_snowflake/server.py

RUN useradd -m snowflakemcp
RUN chown -R snowflakemcp:snowflakemcp /app
USER snowflakemcp

CMD ["mcp-server-snowflake", "--service-config-file", "/app/services.yaml", "--transport", "streamable-http"]